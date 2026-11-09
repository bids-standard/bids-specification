"""A partial implementation of schema-based validation in Python."""

import datetime
import fnmatch
import json
import os
import re
from copy import deepcopy
from pathlib import Path

import bidsschematools as bst
import bidsschematools.rules
import bidsschematools.schema
import bidsschematools.types
import bidsschematools.utils

lgr = bst.utils.get_logger()

VALIDATOR_SCHEMA_COMPATIBILITY_LEVEL = "minor"


def _bids_schema_versioncheck(schema_dir, compatibility=VALIDATOR_SCHEMA_COMPATIBILITY_LEVEL):
    """
    Use the `SCHEMA_VERSION` descriptor file to determine whether a selected schema directory is
    compatible with the validator.

    Parameters
    ----------
    schema_dir : str
        A string which specifies a path.
    compatibility : "major" or "minor", optional
        Compatibility range of the validator. Major means "M.*" are considered compatible, minor
        means "M.m.*" are considered compatible.

    Returns
    -------
    bool:
        Whether the schema is compatible with the validator.
    """

    if compatibility not in ("major", "minor"):
        raise ValueError("Schema compatibility needs to be set to either “major” or “minor”.")

    if isinstance(schema_dir, str):
        schema_dir = Path(schema_dir)

    schema_version_file = schema_dir.joinpath("SCHEMA_VERSION")
    try:
        schema_version = schema_version_file.read_text().strip()
    except FileNotFoundError:
        lgr.warning(
            "The selected schema directory, `%s`, does not contain a SCHEMA_VERSION file. "
            "Cannot ascertain compatibility. Attempting to query the BIDS reference for "
            "compatible versions.",
            schema_dir,
        )
    else:
        nparts = 1 if compatibility == "major" else 2
        return schema_version.split(".", nparts)[:-1] == bst.__version__.split(".", nparts)[:-1]
        lgr.warning(
            "The selected schema `%s`, has a schema version (`%s`) which is "
            "incompatible with the validator. Attempting to query the BIDS reference "
            "for compatible versions.",
            schema_dir,
            schema_version,
        )
    return False


def _find_bids_root(in_paths, accept_non_bids_dir):
    """
    Return BIDS root for a list of paths.
    Raise error if more than one root is found and, optionally, if none is found.
    """

    dataset_descriptions = []
    for in_path in in_paths:
        in_path = os.path.abspath(os.path.expanduser(in_path))
        dataset_description = _find_dataset_description(in_path)
        if dataset_description and dataset_description not in dataset_descriptions:
            dataset_descriptions.append(dataset_description)
    if len(dataset_descriptions) > 1:
        raise ValueError(
            f"You have selected files belonging to {len(dataset_descriptions)} "
            "different datasets. Please run the validator once per dataset."
        )
    elif len(dataset_descriptions) == 0:
        if accept_non_bids_dir:
            lgr.warning(
                "None of the files in the input list are part of a BIDS dataset. Proceeding."
            )
            return ""
        else:
            raise ValueError(
                "None of the files in the input list are part of a BIDS dataset. Aborting."
            )
    return os.path.dirname(dataset_descriptions[0])


def _find_dataset_description(my_path):
    my_path = Path(my_path)
    for path in (my_path, *my_path.parents):
        candidate = path / "dataset_description.json"
        if candidate.is_file():
            return candidate
    return None


def _get_directory_suffixes(my_schema):
    """Query schema for suffixes which identify directory entities.

    Parameters
    ----------
    my_schema : dict
        Nested directory as produced by `bidsschematools.schema.load_schema()`.

    Returns
    -------
    list of str
        Directory pseudofile suffixes excluding trailing slashes.

    Notes
    -----
    * Yes this seems super-awkward to do explicitly, after all, the trailing slash is
        already in so it should automagically work, but no:
        - Subdirectory names need to be dynamically excluded from validation input.
        - Backslash directory delimiters are still in use, which is regrettable.
    """
    return [
        ext.value[:-1]
        for ext in my_schema.objects.extensions.values()
        if len(ext.value) > 1 and ext.value.endswith("/")
    ]


def _get_paths(
    bids_paths,
    pseudofile_suffixes=None,
    dummy_paths=False,
    exclude_files=None,
):
    """
    Get all paths from a list of directories, excluding hidden subdirectories from distribution.

    Parameters
    ----------
    bids_paths : list or str
        Directories from which to get paths, may also contain file paths, which will remain
        unchanged.
    pseudofile_suffixes : list of str
        Directory suffixes prompting the validation of the directory name and limiting further
        directory walk.
    dummy_paths : bool, optional
        Whether to accept path strings which do not correspond to either files or directories.
    exclude_files : list, optional
        Files to exclude from listing.
        Dot files (`.*`) do not need to be explicitly listed, as these are excluded by default.

    Notes
    -----
    * Deduplicate paths (if input dirs are subsets of other input dirs), might best be done at the
        very end. This is only relevant for poor usage (e.g. passing parent *and* child
        directories), and has thus far not caused problems, but it would be good to brace for
        that.
    * The `dataset_description.json` and `.bidsignore` handling should be split out of the main
        loop, since we now have BIDS root detection called before file detection. This is
        non-critical however, since the topdown `os.walk` makes sure top-level files are detected
        first.
    """

    if exclude_files is None:
        exclude_files = []
    if pseudofile_suffixes is None:
        pseudofile_suffixes = []

    path_list = []
    bidsignore_list = []
    bids_root_found = False
    for bids_path in bids_paths:
        if not dummy_paths:
            bids_path = os.path.abspath(os.path.expanduser(bids_path))
        if os.path.isdir(bids_path):
            for root, dirs, file_names in os.walk(bids_path, topdown=True):
                if "dataset_description.json" in file_names:
                    if bids_root_found:
                        # No nested BIDS.
                        dirs[:] = []
                        file_names[:] = []
                    else:
                        try:
                            with open(os.path.join(root, ".bidsignore")) as f:
                                bidsignore_list = f.read().splitlines()
                        except FileNotFoundError:
                            pass
                        bids_root_found = True
                if root.endswith(tuple(pseudofile_suffixes)):
                    # Add the directory name to the validation paths list.
                    path_list.append(Path(root).as_posix() + "/")
                    # Do not index the contents of the directory.
                    dirs[:] = []
                    file_names[:] = []
                if os.path.basename(root).startswith("."):
                    dirs[:] = []
                    file_names[:] = []
                for file_name in file_names:
                    if file_name in exclude_files or file_name.startswith("."):
                        continue
                    if bidsignore_list:
                        ignored = False
                        for ignore_expression in bidsignore_list:
                            ignored = _bidsignore_check(ignore_expression, file_name, root)
                            if ignored:
                                break
                        if ignored:
                            continue
                    file_path = os.path.join(root, file_name)
                    path_list.append(Path(file_path).as_posix())
        elif os.path.isfile(bids_path) or dummy_paths:
            path_list.append(Path(bids_path).as_posix())
        else:
            raise FileNotFoundError(
                f"The input path `{bids_path}` could not be located. If this is a string "
                "intended for path validation which does not correspond to an actual "
                "path, please set the `dummy_paths` parameter to True."
            )

    return path_list


def _bidsignore_check(ignore_expression, file_name, file_root):
    """
    Check whether a file is set to be ignored as per `.bidsignore`

    Parameters
    ----------
    ignore_expression : str
        A string following git-wildcard conventions (including `**/`).
    file_name : str
        A string which represents a filename.
    file_root : str
        The directory containing the file specifiled in `file_name`.

    Returns
    -------
    bool:
        Whether the file should be ignored.

    Notes
    -----
    * We cannot use `glob` since that would preempt working with theoretical or non-local
        paths, therefore we use `fnmatch`.
    * `fnmatch` does not support `**/` matching as that is an optional convention from e.g.
        globstar and git, and not part of the standard Unix shell. As we formalize `.bidsignore`
        we may choose drop it, since we already treat simple filenames as to-be-ignored in
        all directories, and with BIDS having only up to 4 hierarchical levels, the utility of
        other usage is limited and expansion to `..*/*..` would only mean at maximum a duplication
        of entries.
    """

    if ignore_expression.startswith("**/"):
        ignore_expression = ignore_expression.lstrip("**/")
    elif any(i in ignore_expression for i in ["/", "\\"]):
        file_name = os.path.join(file_root, file_name)

    return fnmatch.fnmatch(file_name, ignore_expression)


def log_errors(validation_result):
    """
    Raise errors for validation result.

    Parameters
    ----------
    validation_result : dict
        A dictionary as returned by `validate_all()` with keys including "schema_tracking",
        "path_tracking", "path_listing", and, optionally "itemwise".
        The "itemwise" value, if present, should be a list of dictionaries, with keys including
        "path", "regex", and "match".
    """
    total_file_count = len(validation_result["path_listing"])
    validated_files_count = total_file_count - len(validation_result["path_tracking"])
    errorless = True
    for i in validation_result["path_tracking"]:
        lgr.warning("The `%s` file was not matched by any regex schema entry.", i)
        errorless = False
    if validated_files_count == 0:
        lgr.error("No valid BIDS files were found.")
        errorless = False
    else:
        # No use reporting this separately if no BIDS files were found
        for entry in validation_result["schema_tracking"]:
            if entry["mandatory"]:
                lgr.error(
                    "The `%s` regex pattern file required by BIDS was not found.",
                    entry["regex"],
                )
                errorless = False
    if errorless:
        lgr.info("SUCCESS: All files are BIDS valid and no BIDS-required files are missing.")


def select_schema_path(
    bids_version=None,
    bids_root=None,
    bids_reference_root=None,
):
    """
    Select schema directory, according to a priority logic whereby the schema path is
    either:

    (1) a concatenation of `bids_reference_root` and `bids_version`, if the latter is
        specified, and the BIDS version schema is compatible with the validator,
    (2) a concatenation of `bids_reference_root` the detected version specification
        inside the BIDS root directory, if such a directory is provided and the BIDS version
        schema is compatible with the validator.
    (3) `None`, expanded to the bundled schema.

    Parameters
    ----------
    bids_root : str or None, optional
        The path to the BIDS root for the paths to be validated.
    bids_reference_root : str, optional
        Path where schema versions are stored, and which contains directories named exactly
        according to the respective schema version, e.g. "1.7.0".
    bids_version : str or None, optional
        BIDS version desired for validation.
        If empty, the `dataset_description.json` fie will be queried for the dataset schema
        version.


    Returns
    -------
    str
        A string which is a path to the selected schema directory.

    Notes
    -----
    * This is a purely aspirational function, and is preempted by logic inside
        `bst.validator.validate_bids()`, and further contingent on better schema stability and
        ongoing work in: https://github.com/bids-standard/bids-schema
    * The default `bids_reference_root` value is based on the FHS and ideally should be enforced.
        Alternatively this could be handled by an environment variable, though that also requires
        enforcement on the package distribution side.
    """

    if bids_reference_root is None:
        lgr.warning("No BIDS reference root provided.")
        return None

    bids_reference_root = os.path.abspath(os.path.expanduser(bids_reference_root))

    schema_dir = False
    if bids_root and not bids_version:
        dataset_description = os.path.join(bids_root, "dataset_description.json")
        with open(dataset_description) as f:
            try:
                dataset_info = json.load(f)
            except json.decoder.JSONDecodeError:
                lgr.error(
                    "The `%s` file cannot be loaded. Please check whether it is valid JSON.",
                    dataset_description,
                )
            else:
                try:
                    bids_version = dataset_info["BIDSVersion"]
                except KeyError:
                    lgr.warning("BIDSVersion is not specified in `dataset_description.json`.")
    if bids_version:
        schema_dir = os.path.join(bids_reference_root, bids_version)
        if _bids_schema_versioncheck(schema_dir):
            return schema_dir

    try:
        for schema_dir_candidate in os.listdir(bids_reference_root):
            schema_dir = os.path.join(bids_reference_root, schema_dir_candidate)
            if _bids_schema_versioncheck(schema_dir):
                return schema_dir
    except FileNotFoundError:
        pass
    lgr.warning(
        "No suitable schema could be found in the BIDS reference root (`%s`).",
        bids_reference_root,
    )
    return None


def validate_all(
    paths_list,
    regex_schema,
):
    """
    Validate `bids_paths` based on a `regex_schema` dictionary list, including regexes.

    Parameters
    ----------
    paths_list : list or str
        A string pointing to a BIDS directory for which paths should be validated, or a list
        of strings pointing to individual files or subdirectories which *all* reside within
        one and only one BIDS directory root (i.e. nested datasets should be validated
        separately).
    regex_schema : list of dict
        A list of dictionaries as generated by `regexify_all()`.

    Returns
    -------
    results : dict
        A dictionary reporting the target files for validation, the unmatched files and unmatched
        regexes, and optionally the itemwise comparison results.
        Keys include "schema_tracking", "path_tracking", "path_listing", "match_listing", and
        optionally "itemwise"

    Notes
    -----
    * Multi-source validation could be accomplished by distributing the resulting tracking_schema
        dictionary and further eroding it.
    * Currently only entities are captured in named groups, edit `load_top_level()` to name other
        groups as well.
    """

    tracking_paths = deepcopy(paths_list)
    tracking_schema = []
    itemwise_results = []
    matched = False
    match_listing = []
    for target_path in paths_list:
        lgr.debug("Checking file `%s`.", target_path)
        lgr.debug("Trying file types:")
        for regex_entry in regex_schema:
            target_regex = r"(?:.*/)?" + regex_entry["regex"]
            # We need to record the actual expressions we query.
            _regex_entry = deepcopy(regex_entry)
            _regex_entry.update({"regex": target_regex})
            lgr.debug("\t* `%s`, with pattern: `%s`", target_path, target_regex)
            matched = re.match(target_regex, target_path)
            itemwise_result = {}
            itemwise_result["path"] = target_path
            itemwise_result["regex"] = target_regex
            if matched:
                lgr.debug("Match identified.")
                itemwise_result["match"] = True
                itemwise_results.append(itemwise_result)
                break
            itemwise_result["match"] = False
            itemwise_results.append(itemwise_result)
        if matched:
            tracking_paths.remove(target_path)
            # Might be fragile since it relies on where the loop broke:
            if not regex_entry["mandatory"]:
                tracking_schema.append(_regex_entry)
            match_entry = matched.groupdict()
            match_entry["path"] = target_path
            match_listing.append(match_entry)
        else:
            tracking_schema.append(_regex_entry)
            lgr.debug(
                "The `%s` file could not be matched to any regex schema entry.",
                target_path,
            )
    results = {}
    results["itemwise"] = itemwise_results
    results["schema_tracking"] = tracking_schema
    results["schema_listing"] = regex_schema
    results["path_tracking"] = tracking_paths
    results["path_listing"] = paths_list
    results["match_listing"] = match_listing

    return results


def write_report(
    validation_result,
    report_path="~/.cache/bidsschematools/validator-report_{datetime}-{pid}.log",
    datetime_format="%Y%m%d%H%M%SZ",
):
    """Write a human-readable report based on the validation result.

    Parameters
    ----------
    validation_result : dict
        A dictionary as returned by `validate_all()` with keys including "schema_tracking",
        "path_tracking", "path_listing", and, optionally "itemwise".
        The "itemwise" value, if present, should be a list of dictionaries, with keys including
        "path", "regex", and "match".
    report_path : str, optional
        A path under which the report is to be saved, `datetime`, and `pid`
        are available as variables for string formatting, and will be expanded to the
        current datetime (as per the `datetime_format` parameter)
        and process ID, respectively.
    datetime_format : str, optional
        A datetime format, optionally used for the report path.

    Notes
    -----
    * Not using f-strings in order to prevent arbitrary code execution.
    """

    report_path = report_path.format(
        datetime=datetime.datetime.now(datetime.timezone.utc).strftime(datetime_format),
        pid=os.getpid(),
    )
    report_path = os.path.abspath(os.path.expanduser(report_path))
    report_dir = os.path.dirname(report_path)
    try:
        os.makedirs(report_dir)
    except OSError:
        pass

    total_file_count = len(validation_result["path_listing"])
    validated_files_count = total_file_count - len(validation_result["path_tracking"])
    with open(report_path, "w") as f:
        try:
            for comparison in validation_result["itemwise"]:
                if comparison["match"]:
                    comparison_result = "A MATCH"
                else:
                    comparison_result = "no match"
                f.write(
                    f"- Comparing the `{comparison['path']}` path to the `{comparison['regex']}` "
                    f"pattern resulted in {comparison_result}.\n"
                )
        except KeyError:
            pass
        f.write(
            f"\nSUMMARY:\n{validated_files_count} out of {total_file_count} files were "
            "successfully validated, using the following regular expressions:"
        )
        for regex_entry in validation_result["schema_listing"]:
            f.write(f"\n\t- `{regex_entry['regex']}`")
        f.write("\n")
        if len(validation_result["path_tracking"]) > 0:
            f.write("The following files were not matched by any regex schema entry:")
            f.write("\n\t* `")
            f.write("`\n\t* `".join(validation_result["path_tracking"]))
        else:
            f.write("All files were matched by a regex schema entry.")
        if len(validation_result["schema_tracking"]) > 0:
            f.write("\nThe following mandatory regex schema entries did not match any files:")
            f.write("\n")
            for entry in validation_result["schema_tracking"]:
                if entry["mandatory"]:
                    f.write(f"\t** `{entry['regex']}`\n")
        else:
            f.write("All mandatory BIDS files were found.\n")
        f.close()
    lgr.info("BIDS validation log written to %s", report_path)


def validate_bids(
    in_paths,
    dummy_paths=False,
    bids_reference_root=None,
    schema_path=None,
    bids_version=None,
    report_path=False,
    suppress_errors=False,
    accept_non_bids_dir=False,
    exclude_files=None,
):
    """
    Validate paths according to BIDS schema.

    Parameters
    ----------
    in_paths : str or list of str
        Paths which to validate, may be individual files or directories.
    dummy_paths : bool, optional
        Whether to accept path strings which do not correspond to either files or directories.
    bids_reference_root : str, optional
        Path where schema versions are stored, and which contains directories named exactly
        according to the respective schema version, e.g. "1.7.0".
        Currently this is untested.
    bids_version : str or None, optional
        Version of BIDS schema, or path to schema. This supersedes the specification detected in
        `dataset_description.json` and is itself superseded if `schema_path` is specified.
    schema_path : str or None, optional
        If a path is given, this will be expanded and used directly, ignoring all other BIDS
        version specification logic. This is not relative to `bids_reference_root`.
    report_path : bool or str, optional
        If `True` a log will be written using the standard output path of `.write_report()`.
        If string, the string will be used as the output path.
        If the variable evaluates as False, no log will be written.
    accept_non_bids_dir : bool, optional
    exclude_files : str, optional
        Files which will not be indexed for validation, use this if your data is in an archive
        standard which requires the presence of archive-specific files (e.g. DANDI requiring
        `dandiset.yaml`).
        Dot files (`.*`) do not need to be explicitly listed, as these are excluded by default.

    Returns
    -------
    results : dict
        A dictionary reporting the target files for validation, the unmatched files and unmatched
        regexes, and optionally the itemwise comparison results.
        Keys include "schema_tracking", "path_tracking", "path_listing", "match_listing", and
        optionally "itemwise"

    Examples
    --------

    ::

        from bidsschematools import validator
        bids_paths = '~/.data2/datalad/000026/noncompliant'
        validator.validate_bids(bids_paths)

    Notes
    -----
    * Needs to account for inheritance principle, probably somewhere deeper in the logic, might be
        as simple as pattern parsing and multiplying patterns to which inheritance applies.
        https://github.com/bids-standard/bids-specification/pull/969#issuecomment-1132119492
    """

    if exclude_files is None:
        exclude_files = []

    if isinstance(in_paths, str):
        in_paths = [in_paths]

    # Are we dealing with real paths?
    if dummy_paths:
        bids_root = None
    else:
        bids_root = _find_bids_root(in_paths, accept_non_bids_dir)

    # Select schema path:
    if not schema_path:
        schema_path = select_schema_path(
            bids_version,
            bids_root,
            bids_reference_root=bids_reference_root,
        )

    regex_schema, my_schema = bst.rules.regexify_all(schema_path)
    pseudofile_suffixes = _get_directory_suffixes(my_schema)

    # Get list of all paths since inputs can be directories.
    bids_paths = _get_paths(
        in_paths,
        dummy_paths=dummy_paths,
        pseudofile_suffixes=pseudofile_suffixes,
        exclude_files=exclude_files,
    )

    # Go!
    validation_result = validate_all(
        bids_paths,
        regex_schema,
    )

    # Record schema version.
    validation_result["bids_version"] = my_schema["bids_version"]

    log_errors(validation_result)

    if report_path:
        if isinstance(report_path, str):
            write_report(validation_result, report_path=report_path)
        else:
            write_report(validation_result)

    return validation_result
