import datetime
import json
import os
import re
import typing as ty
from collections.abc import Mapping
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

import bidsschematools as bst
import bidsschematools.schema
import bidsschematools.types
import bidsschematools.utils

lgr = bst.utils.get_logger()

# The list of which entities create directories could be dynamically specified by the YAML, but for
# now, it is not.
# Ordering is important, as "subject" follows "session" alphabetically, but is hierarchically
# above it.
DIR_ENTITIES = ["subject", "session"]


def _get_paths(
    bids_paths,
    pseudofile_suffixes=[],
    accept_dummy_paths=False,
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
    accept_dummy_paths : bool, optional
        Whether to accept path strings which do not correspond to either files or directories.

    Notes
    -----
    * Figure out how to return paths from BIDS root.
    * Deduplicate paths (if input dirs are subsets of other input dirs), might best be done at the
        very end.
    """
    # `.bidsignore` is not, in fact, a BIDS file, as per:
    # https://github.com/bids-standard/bids-specification/issues/980
    # Perhaps this should be parameterized for downstream flexibility and not having to keep track
    # of downstream nuisance files here.
    exclude_files = [
        "dandiset.yaml",
    ]

    path_list = []
    bids_root_found = False
    for bids_path in bids_paths:
        if not accept_dummy_paths:
            bids_path = os.path.abspath(os.path.expanduser(bids_path))
        if os.path.isdir(bids_path):
            for root, dirs, file_names in os.walk(bids_path, topdown=True):
                if "dataset_description.json" in file_names:
                    if bids_root_found:
                        dirs[:] = []
                        file_names[:] = []
                    else:
                        bids_root_found = True
                if root.endswith(tuple(pseudofile_suffixes)):
                    # Add the directory name to the validation paths list.
                    path_list.append(Path(root).as_posix() + "/")
                    # Do not index the contents of the directory.
                    dirs[:] = []
                    file_names[:] = []
                # will break if BIDS ever puts meaningful data under `/.{dandi,datalad,git}*/`
                if os.path.basename(root).startswith("."):
                    dirs[:] = []
                    file_names[:] = []
                for file_name in file_names:
                    if file_name in exclude_files or file_name.startswith("."):
                        continue
                    file_path = os.path.join(root, file_name)
                    # This will need to be replaced with bids root finding.
                    path_list.append(Path(file_path).as_posix())
        elif os.path.isfile(bids_path) or accept_dummy_paths:
            path_list.append(Path(bids_path).as_posix())
        else:
            raise FileNotFoundError(
                f"The input path `{bids_path}` could not be located. If this is a string "
                "intended for path validation which does not correspond to an actual "
                "path, please set the `accept_dummy_paths` parameter to True."
            )

    return path_list


def _capture_regex(name, pattern, backref):
    """Capture pattern to name or match back-reference to name

    >>> _capture_regex("run", "[0-9]+", False)
    '(?P<run>[0-9]+)'
    >>> _capture_regex("run", "[0-9]+", True)
    '(?P=run)'
    >>> re.match(_capture_regex("run", "[0-9]+", False), "123_").groupdict()
    {'run': '123'}
    """
    return f"(?P={name})" if backref else f"(?P<{name}>{pattern})"


def _optional_regex(regex, optional):
    """Return an optional version of a regex if optional is True

    A required regex is passed through unchanged:

    >>> pattern = _optional_regex("xyz", False)
    >>> pattern
    'xyz'
    >>> re.match(pattern, "xyz").groups()
    ()
    >>> re.match(pattern, "") is None
    True

    An optional regex uses a non-capturing group, to avoid interfering
    with existing groups

    >>> pattern = _optional_regex("x(?P<name>[a-z])z", True)
    >>> pattern
    '(?:x(?P<name>[a-z])z)?'
    >>> re.match(pattern, "xyz").groups()
    ('y',)
    >>> re.match(pattern, "xyz").groupdict()
    {'name': 'y'}
    >>> re.match(pattern, "").groups()
    (None,)
    >>> re.match(pattern, "").groupdict()
    {'name': None}
    """
    return f"(?:{regex})?" if optional else regex


@lru_cache()
def _format_entity(entity, name, pattern, level, directory=False):
    if directory and entity not in DIR_ENTITIES:
        return ""

    label = _capture_regex(entity, pattern, not directory and entity in DIR_ENTITIES)
    post = "/" if directory else "_"

    return _optional_regex(f"{name}-{label}{post}", level != "required")


def split_inheritance_rules(rule: Mapping) -> ty.List[Mapping]:
    """Break composite rules into main and sidecar rules

    Implements the inheritance principle for file naming.
    """
    heritable_exts = {".tsv", ".json", ".bval", ".bvec"}
    rule_exts = set(rule["extensions"])

    main_exts = rule_exts - heritable_exts
    # If a rule only has TSV or JSON files, entities can be
    # made required
    if not main_exts:
        if ".tsv" in rule_exts:
            main_exts = {".tsv"}
        elif ".json" in rule_exts:
            main_exts = {".json"}

    sidecar_exts = rule_exts - main_exts
    if not sidecar_exts:
        return [rule]

    sidecar_dtypes = [""] + rule.get("datatypes", [])
    sidecar_entities = {ent: "optional" for ent in rule.get("entities")}

    main_rule = {**rule, **{"extensions": list(main_exts)}}
    sidecar_rule = {
        **rule,
        **{
            "extensions": list(sidecar_exts),
            "datatypes": sidecar_dtypes,
            "entities": sidecar_entities,
        },
    }

    return [main_rule, sidecar_rule]


def _path_rule(rule: bst.types.Namespace):
    return {"regex": re.escape(rule.path), "mandatory": rule.level == "required"}


def _sanitize_extension(ext: str) -> str:
    if ext == ".*":
        return r"\.[a-zA-Z0-9.]+"
    return re.escape(ext)


def _stem_rule(rule: bst.types.Namespace):
    stem_regex = re.escape(rule.stem)
    ext_match = "|".join(_sanitize_extension(ext) for ext in rule.extensions)
    ext_regex = f"(?P<extension>{ext_match})"

    return {"regex": stem_regex + ext_regex, "mandatory": rule.level == "required"}


def _entity_rule(rule: Mapping, schema: bst.types.Namespace):
    dir_regex = []
    entity_regex = []
    for ent in schema.rules.entities:
        if ent not in rule["entities"]:
            continue
        ent_obj = rule["entities"][ent]
        if isinstance(ent_obj, str):
            ent_obj = {"level": ent_obj}
        # Allow filename rule to override original entity fields
        entity = {**schema.objects.entities[ent], **ent_obj}

        if "enum" in entity:
            pattern = "|".join(entity["enum"])
        else:
            pattern = schema.objects.formats[entity["format"]].pattern

        dir_regex.append(
            _format_entity(ent, entity["name"], pattern, entity["level"], directory=True)
        )
        entity_regex.append(_format_entity(ent, entity["name"], pattern, entity["level"]))

    dtypes = set(rule.get("datatypes", ()))
    optional_dtype = "" in dtypes
    if optional_dtype:
        dtypes.remove("")
    if dtypes:
        pattern = f"(?P<datatype>{'|'.join(dtypes)})/"
        if optional_dtype:
            pattern = f"(?:{pattern})?"
        dir_regex += pattern

    # If we move to referring to suffixes by keys in the object table:
    # suffixes = [schema.objects.suffixes[suffix].value for suffix in rule["suffixes"]]
    suffixes = rule["suffixes"]
    suffix_regex = f"(?P<suffix>{'|'.join(suffixes)})"

    # If we move to referring to extensions by keys in the object table:
    # extensions = [schema.objects.extensions[ext].value for ext in rule["extensions"]]
    extensions = rule["extensions"]
    ext_match = "|".join(_sanitize_extension(ext) for ext in extensions)
    ext_regex = f"(?P<extension>{ext_match})"

    return {
        "regex": "".join(dir_regex + entity_regex + [suffix_regex, ext_regex]),
        "mandatory": False,
    }


def load_filename_rules(
    rule_group: bst.types.Namespace,
    schema: bst.types.Namespace,
    level: int,
):
    """Load schema rules into regular expressions

    Parameters
    ----------
    rule_group : Namespace
        The set of rules to load from the schema
    schema : Namespace
        A nested dictionary, as returned by `bidsschematools.schema.load_schema()`.
    level : int
        The depth in rule_group to look for rules

    Returns
    -------
    rules : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """
    regex_schema = []
    for rule_template in rule_group.values(level=level):
        # Simple rules, e.g. dataset_description.json, README
        if "path" in rule_template:
            regex_schema.append(_path_rule(rule_template))
        elif "stem" in rule_template:
            regex_schema.append(_stem_rule(rule_template))
        else:
            regex_schema.extend(
                _entity_rule(rule, schema) for rule in split_inheritance_rules(rule_template)
            )

    return regex_schema


@lru_cache()
def load_all(
    schema_dir,
):
    """
    Create full path regexes for all BIDS specification files.

    Parameters
    ----------
    schema_dir : str, optional
        A string pointing to a BIDS directory for which paths should be validated.

    Returns
    -------
    all_regex : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    my_schema : Mapping
        Nested dictionaries representing the full schema.
    """

    schema = bst.schema.load_schema(schema_dir)
    all_regex = []
    for group in (schema.rules.files.common, schema.rules.files.raw):
        all_regex.extend(load_filename_rules(group, schema, level=2))

    return all_regex, schema


def validate_all(
    paths_list,
    regex_schema,
):
    """
    Validate `bids_paths` based on a `regex_schema` dictionary list, including regexes.

    Parameters
    ----------
    bids_paths : list or str
        A string pointing to a BIDS directory for which paths should be validated, or a list
        of strings pointing to individual files or subdirectories which *all* reside within
        one and only one BIDS directory root (i.e. nested datasets should be validated
        separately).
    regex_schema : list of dict
        A list of dictionaries as generated by `load_all()`.

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

    tracking_schema = deepcopy(regex_schema)
    tracking_paths = deepcopy(paths_list)
    itemwise_results = []
    matched = False
    match_listing = []
    for target_path in paths_list:
        lgr.debug("Checking file `%s`.", target_path)
        lgr.debug("Trying file types:")
        for regex_entry in tracking_schema:
            target_regex = regex_entry["regex"]
            lgr.debug("\t* `%s`, with pattern: `%`", target_path, target_regex)
            matched = re.match(r"(?:.*/)?" + target_regex, target_path)
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
            if regex_entry["mandatory"]:
                tracking_schema.remove(regex_entry)
            match_entry = matched.groupdict()
            match_entry["path"] = target_path
            match_listing.append(match_entry)
        else:
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
        datetime=datetime.datetime.utcnow().strftime(datetime_format),
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
                    f'- Comparing the `{comparison["path"]}` path to the `{comparison["regex"]}` '
                    f"pattern resulted in {comparison_result}.\n"
                )
        except KeyError:
            pass
        f.write(
            f"\nSUMMARY:\n{validated_files_count} out of {total_file_count} files were "
            "successfully validated, using the following regular expressions:"
        )
        for regex_entry in validation_result["schema_listing"]:
            f.write(f'\n\t- `{regex_entry["regex"]}`')
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
                    f.write(f'\t** `{entry["regex"]}`\n')
        else:
            f.write("All mandatory BIDS files were found.\n")
        f.close()
    lgr.info("BIDS validation log written to %s", report_path)


def _find_dataset_description(my_path):
    candidate = os.path.join(my_path, "dataset_description.json")
    # Windows support... otherwise we could do `if my_path == "/"`.
    if my_path == "/" or not any(i in my_path for i in ["/", "\\"]):
        return None
    if os.path.isfile(candidate):
        return candidate
    else:
        level_up = os.path.dirname(my_path.rstrip("/\\"))
        return _find_dataset_description(level_up)


def select_schema_dir(
    bids_paths,
    schema_reference_root,
    schema_version,
    schema_min_version,
):
    """
    Select schema directory, according to a fallback logic whereby the schema path is
    either (1) `schema_version` if the value is a path, (2) a concatenation of
    `schema_reference_root` and `schema_version`, (3) a concatenation of the detected
    version specification from a `dataset_description.json` file if one is found in
    parents of the input path, (4) `schema_min_version` if no other version can be found
    or if the detected version from `dataset_description.json` is smaller than
    `schema_min_version`.

    Parameters
    ----------
    bids_paths : list of str
        Paths to be validated.
        Entries in this list will be used to crawl the directory tree upwards until a
        dataset_description.json file is found.
    schema_reference_root : str, optional
        Path where schema versions are stored, and which contains directories named exactly
        according to the respective schema version, e.g. "1.7.0".
        If the path starts with the string "{module_path}" it will be expanded relative to the
        module path.
    schema_version : str or None
        Version of BIDS schema, or path to schema.
        If a path is given, this will be expanded and used directly, not concatenated with
        `schema_reference_root`.
        If the path starts with the string "{module_path}" it will be expanded relative to the
        module path.
        If None, the `dataset_description.json` fie will be queried for the dataset schema version.
    schema_min_version : str
        Minimal version to use UNLESS the schema version is manually specified.
        If the version is auto-detected and the version is smaller than schema_min_version,
        schema_min_version will be selected instead.


    Returns
    -------

    """
    # Expand module_path
    module_path = os.path.abspath(os.path.dirname(__file__))
    if schema_reference_root.startswith("{module_path}"):
        schema_reference_root = schema_reference_root.format(module_path=module_path)
    schema_reference_root = os.path.abspath(os.path.expanduser(schema_reference_root))

    # Handle path schema specification
    if schema_version:
        if "/" in schema_version:
            schema_dir = schema_version
            if schema_version.startswith("{module_path}"):
                schema_dir = schema_version.format(module_path=module_path)
            schema_dir = os.path.abspath(os.path.expanduser(schema_dir))
            return schema_dir
        schema_dir = os.path.join(schema_reference_root, schema_version)
        return schema_dir

    dataset_descriptions = []
    for bids_path in bids_paths:
        bids_path = os.path.abspath(os.path.expanduser(bids_path))
        dataset_description = _find_dataset_description(bids_path)
        if dataset_description and dataset_description not in dataset_descriptions:
            dataset_descriptions.append(dataset_description)
    if len(dataset_descriptions) > 1:
        raise ValueError(
            f"You have selected files belonging to {len(dataset_descriptions)} "
            "different datasets. Please run the validator once per dataset."
        )
    if dataset_descriptions:
        dataset_description = dataset_descriptions[0]
        with open(dataset_description) as f:
            try:
                dataset_info = json.load(f)
            except json.decoder.JSONDecodeError:
                lgr.error(
                    "The `%s` file could not be loaded. "
                    "Please check whether the file is valid JSON. "
                    "Falling back to the `%s` BIDS version.",
                    dataset_description,
                    schema_min_version,
                )
                schema_version = schema_min_version
            else:
                try:
                    schema_version = dataset_info["BIDSVersion"]
                except KeyError:
                    lgr.warning(
                        "BIDSVersion is not specified in "
                        "`dataset_description.json`. "
                        "Falling back to `%s`.",
                        schema_min_version,
                    )
                    schema_version = schema_min_version
    if not schema_version:
        lgr.warning(
            "No BIDSVersion could be found for the dataset. Falling back to `%s`.",
            schema_min_version,
        )
        schema_version = schema_min_version
    elif schema_min_version:
        if schema_version < schema_min_version:
            lgr.warning(
                "BIDSVersion `%s` is less than the minimal working "
                "`%s`. "
                "Falling back to `%s`. "
                "To force the usage of earlier versions specify them explicitly "
                "when calling the validator.",
                schema_version,
                schema_min_version,
                schema_min_version,
            )
            schema_version = schema_min_version
    schema_dir = os.path.join(schema_reference_root, schema_version)
    if os.path.isdir(schema_dir):
        return schema_dir
    else:
        raise ValueError(
            f"The expected schema directory {schema_dir} does not exist on the system. "
            "Please ensure the file exists or manually specify a schema version for "
            "which the bidsschematools files are available on your system."
        )


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
    if validated_files_count == 0:
        lgr.error("No valid BIDS files were found.")
    for entry in validation_result["schema_tracking"]:
        if entry["mandatory"]:
            lgr.error(
                "The `%s` regex pattern file required by BIDS was not found.",
                entry["regex"],
            )
    for i in validation_result["path_tracking"]:
        lgr.warning("The `%s` file was not matched by any regex schema entry.", i)


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
    pseudofile_suffixes = []
    for i in my_schema["objects"]["extensions"].values():
        i_value = i["value"]
        if i_value.endswith("/") and i_value != "/":
            pseudofile_suffixes.append(i_value[:-1])
    return pseudofile_suffixes


def validate_bids(
    in_paths,
    accept_dummy_paths=False,
    schema_reference_root="{module_path}/data/",
    schema_version=None,
    report_path=False,
    suppress_errors=False,
    schema_min_version="schema",
):
    """
    Validate paths according to BIDS schema.

    Parameters
    ----------
    in_paths : str or list of str
        Paths which to validate, may be individual files or directories.
    accept_dummy_paths : bool, optional
        Whether to accept path strings which do not correspond to either files or directories.
    schema_reference_root : str, optional
        Path where schema versions are stored, and which contains directories named exactly
        according to the respective schema version, e.g. "1.7.0".
        If the path starts with the string "{module_path}" it will be expanded relative to the
        module path.
    schema_version : str or None, optional
        Version of BIDS schema, or path to schema.
        If a path is given, this will be expanded and used directly, not concatenated with
        `schema_reference_root`.
        If the path starts with the string "{module_path}" it will be expanded relative to the
        module path.
        If None, the `dataset_description.json` fie will be queried for the dataset schema version.
    report_path : bool or str, optional
        If `True` a log will be written using the standard output path of `.write_report()`.
        If string, the string will be used as the output path.
        If the variable evaluates as False, no log will be written.
    schema_min_version : str, optional
        Minimal working schema version, used by the `bidsschematools.select_schema_dir()` function
        only if no schema version is found or a lower schema version is specified by the dataset.

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
        bids_paths = '~/.data2/datalad/000026/rawdata'
        schema_version='{module_path}/data/schema/'
        validator.validate_bids(bids_paths, schema_version=schema_version)

    Notes
    -----
    * Needs to account for inheritance principle, probably somewhere deeper in the logic, might be
        as simple as pattern parsing and multiplying patterns to which inheritance applies.
        https://github.com/bids-standard/bids-specification/pull/969#issuecomment-1132119492
    """

    if isinstance(in_paths, str):
        in_paths = [in_paths]

    bids_schema_dir = select_schema_dir(
        in_paths,
        schema_reference_root,
        schema_version,
        schema_min_version=schema_min_version,
    )
    regex_schema, my_schema = load_all(bids_schema_dir)
    pseudofile_suffixes = _get_directory_suffixes(my_schema)
    bids_paths = _get_paths(
        in_paths,
        accept_dummy_paths=accept_dummy_paths,
        pseudofile_suffixes=pseudofile_suffixes,
    )
    validation_result = validate_all(
        bids_paths,
        regex_schema,
    )

    # Record schema version.
    bids_version = bst.schema._get_bids_version(bids_schema_dir)
    validation_result["bids_version"] = bids_version

    log_errors(validation_result)

    if report_path:
        if isinstance(report_path, str):
            write_report(validation_result, report_path=report_path)
        else:
            write_report(validation_result)

    return validation_result
