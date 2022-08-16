import datetime
import json
import os
import re
from copy import deepcopy
from functools import lru_cache
from pathlib import Path

from . import schema, utils

lgr = utils.get_logger()

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
    exclude_subdirs = [
        rf"{os.sep}.dandi",
        rf"{os.sep}.datalad",
        rf"{os.sep}.git",
    ]
    # `.bidsignore` is not, in fact, a BIDS file, as per:
    # https://github.com/bids-standard/bids-specification/issues/980
    exclude_files = [
        ".gitattributes",
        ".gitignore",
        ".bidsignore",
        "dandiset.yaml",
    ]

    path_list = []
    bids_root_found = False
    for bids_path in bids_paths:
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
                if os.path.basename(root) in exclude_subdirs:
                    continue
                for file_name in file_names:
                    if file_name in exclude_files:
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


def _add_entity(regex_entities, entity, entity_shorthand, variable_field, requirement_level):
    """Add entity pattern to filename template based on requirement level."""

    # We need to do this here, although it would be easier to back-reference in the directory.
    # This is because regex evaluates sequentially and we can not forward-reference a group.
    if entity in DIR_ENTITIES:
        variable_regex = f"(?P={entity})"
    else:
        variable_regex = f"(?P<{entity}>{variable_field})"

    if requirement_level == "required":
        if len(regex_entities.strip()):
            regex_entities += f"_{entity_shorthand}-{variable_regex}"
        else:
            # Only the first entity doesn't need an underscore
            regex_entities += f"{entity_shorthand}-{variable_regex}"
    else:
        if len(regex_entities.strip()):
            regex_entities += f"(|_{entity_shorthand}-{variable_regex})"
        else:
            # Only the first entity doesn't need an underscore
            regex_entities += f"(|{entity_shorthand}-{variable_regex})"

    return regex_entities


def _extension_safety(extension):
    """
    Making extensions formatting-safe.
    Issues covered by this function are listed under “Notes”

    Parameters
    ----------
    extension : str
        Extension string, as present in the BIDS YAML schema.

    Returns
    -------
    str
        Extension string, safe for use in validator Regex formatting.

    Notes
    -----
    * Bash-wildcard safety: https://github.com/bids-standard/bids-specification/issues/990
    * Period safety: https://github.com/bids-standard/bids-specification/issues/1055
    * Hopefully this function will be deprecated soon, but it will not break safe entries.
    """
    if extension == "None":
        return ""
    if "." in extension:
        extension = extension.replace(".", "\\.")
    if "*" in extension:
        extension = extension.replace("*", ".*?")

    return extension


def _add_extensions(regex_string, variant):
    """Add extensions to a regex string."""
    fixed_variant_extensions = []
    for variant_extension in variant["extensions"]:
        variant_extension = _extension_safety(variant_extension)
        fixed_variant_extensions.append(variant_extension)
    if len(fixed_variant_extensions) > 1:
        regex_extensions = "({})".format("|".join(fixed_variant_extensions))
    else:
        regex_extensions = fixed_variant_extensions[0]
    regex_string = f"{regex_string}{regex_extensions}"

    return regex_string


def _add_subdirs(regex_string, variant, datatype, entity_definitions, formats, modality_datatypes):
    """Add appropriate subdirectories as required by entities present."""

    regex_dirs = "/"
    for dir_entity in DIR_ENTITIES:
        if dir_entity in variant["entities"].keys():
            format_selection = formats[entity_definitions[dir_entity]["format"]]
            variable_field = format_selection["pattern"]
            shorthand = entity_definitions[dir_entity]["name"]
            if variant["entities"][dir_entity] == "required":
                regex_subdir = f"{shorthand}-(?P<{dir_entity}>{variable_field})/"
            else:
                regex_subdir = f"(|{shorthand}-(?P<{dir_entity}>{variable_field})/)"
            regex_dirs = f"{regex_dirs}{regex_subdir}"
    if datatype in modality_datatypes:
        regex_dirs = f"{regex_dirs}{datatype}/"
    regex_string = f"{regex_dirs}{regex_string}"

    return regex_string


def _add_suffixes(regex_string, variant):
    """Add suffixes to a regex string."""
    if len(variant["suffixes"]) == 1:
        regex_suffixes = variant["suffixes"][0]
    else:
        regex_suffixes = "({})".format("|".join(variant["suffixes"]))
    regex_string = f"{regex_string}_{regex_suffixes}"

    return regex_string


def load_top_level(
    my_schema,
):
    """
    Create full path regexes for top level files, as documented by a target BIDS YAML schema
    version.


    Parameters
    ----------
    my_schema : dict
        A nested dictionary, as returned by `bidsschematools.schema.load_schema()`.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    top_level_files = my_schema["rules"]["top_level_files"]

    regex_schema = []
    for top_level_filename in top_level_files.keys():
        top_level_file = top_level_files[top_level_filename]
        # None value gets passed as list of strings...
        extensions = top_level_file["extensions"]
        if extensions != ["None"]:
            extensions_regex = "|".join(map(_extension_safety, extensions))
            regex = f".*?/{top_level_filename}({extensions_regex})$"
        else:
            regex = f".*?/{top_level_filename}$"
        regex_entry = {
            "regex": regex,
            "mandatory": top_level_file["required"],
        }
        regex_schema.append(regex_entry)

    return regex_schema


def load_entities(
    my_schema,
    inheritance_regex=r".*?\\\.(tsv|bvec|json)(\$|\||\)).*?",
):
    """Create full path regexes for entities, as documented by a target BIDS YAML schema version.

    Parameters
    ----------
    my_schema : dict
        A nested dictionary, as returned by `bidsschematools.schema.load_schema()`.
    inheritance_regex : str, optional
        Valid regex string identifying filenames to which inheritance expansion should be applied.

    Notes
    -----

    * Suggest to BIDS-specification to remove the periods from the extensions, the leading period
        is not part of the extension, but a delimiter defining the fact that it's an extension.
        Code sections marked as `Making it period-safe` should be edited when this fix is in,
        though they will work in any case.
        https://github.com/bids-standard/bids-specification/issues/990
    * More issues in comments.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    # Parsing tabular_metadata as a datatype, might be done automatically if the YAML is moved
    # to the same subdirectory
    datatypes = {
        "tabular_metadata": my_schema.rules.tabular_metadata,
        **my_schema.rules.datatypes,
    }
    entity_order = my_schema["rules"]["entities"]
    entity_definitions = my_schema["objects"]["entities"]
    formats = my_schema["objects"]["formats"]

    # # Descriptions are not needed and very large.
    # for i in entity_definitions.values():
    #     i.pop("description", None)

    # Needed for non-modality file separation as per:
    # https://github.com/bids-standard/bids-specification/pull/985#issuecomment-1019573787
    modalities = my_schema["rules"]["modalities"]
    modality_datatypes = []
    for modality_key in modalities.keys():
        for modality_datatype in modalities[modality_key]["datatypes"]:
            modality_datatypes.append(modality_datatype)

    regex_schema = []
    for datatype in datatypes:
        if datatype == "derivatives":
            continue
        for variant in datatypes[datatype].values():
            regex_entities = ""
            for entity in entity_order:
                # Slightly awkward construction to account for new-style file specification.
                # As in:
                # https://github.com/bids-standard/bids-specification/pull/987
                try:
                    if entity in variant["entities"]:
                        entity_shorthand = entity_definitions[entity]["name"]
                        if "enum" in entity_definitions[entity].keys():
                            # Entity key-value pattern with specific allowed values
                            # tested, works!
                            variable_field = "|".join(entity_definitions[entity]["enum"])
                        else:
                            format_selection = formats[entity_definitions[entity]["format"]]
                            variable_field = format_selection["pattern"]
                        regex_entities = _add_entity(
                            regex_entities,
                            entity,
                            entity_shorthand,
                            variable_field,
                            variant["entities"][entity],
                        )
                except KeyError:
                    pass

            regex_string = _add_suffixes(regex_entities, variant)
            regex_string = _add_extensions(regex_string, variant)
            regex_string = _add_subdirs(
                regex_string,
                variant,
                datatype,
                entity_definitions,
                formats,
                modality_datatypes,
            )

            regex_string = f".*?{regex_string}$"
            regex_entry = {
                "regex": regex_string,
                "mandatory": False,
            }
            regex_schema.append(regex_entry)
            if re.match(inheritance_regex, regex_string):
                expansion_list = _inheritance_expansion(regex_string, datatype)
                for expansion in expansion_list:
                    expansion_entry = {
                        "regex": expansion,
                        "mandatory": False,
                    }
                    regex_schema.append(expansion_entry)

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
    my_schema : list of dict
        Nested dictionaries representing the full schema.
    """

    my_schema = schema.load_schema(schema_dir)
    all_regex = load_entities(
        my_schema=my_schema,
    )
    top_level_regex = load_top_level(
        my_schema=my_schema,
    )
    all_regex.extend(top_level_regex)

    return all_regex, my_schema


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
    report_path="/var/tmp/bids-validator/report_{datetime}-{pid}.log",
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
    try:
        os.makedirs(os.path.dirname(report_path))
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


def _inheritance_expansion(
    regex_string,
    datatype=None,
):
    """
    Generate regex strings applying BIDS inheritance expansion to an input string.

    Parameters
    ----------
    regex_string : str
        String representing the regex to which inheritance expansion should be applied.
    datatype : str, optional
        Datatype string to remove as part of inheritance expansion.

    Returns
    -------
    expanded_regexes : list of str
    """

    # Order is important as the string is eroded.
    # Session is eroded *together with* and *after* subject, as it is always optional
    # and the erosion is:
    #   * only required if a dangling leading underscore is present after subject removal.
    #   * only BIDS-valid after the subject field is eroded from the filename.
    expansions = [
        {
            "regex": [
                r".*?(?P<remove>sub-\(\?P<subject>\[0\-9a\-zA\-Z\]\+\)/).*?",
                r".*?(?P<remove>sub-\(\?P=subject\))",
                r".*?/(?P<remove>\(\|ses-\(\?P<session>\[0\-9a\-zA\-Z\]\+\)/\)\(\|_ses-\("
                r"\?P=session\)\)_).*?",
            ],
            "replace": ["", "", ""],
        },
    ]
    if datatype:
        # Inserting at the beginning, since datatype goes first.
        expansions.insert(
            0,
            {
                "regex": [
                    f".*?(?P<remove>{datatype}/).*?",
                ],
                "replace": [
                    "",
                ],
            },
        )

    expanded_regexes = []
    lgr.debug("Applying inheritance expansion to:\n`%s`", regex_string)
    for expansion in expansions:
        modified = False
        for ix, regex in enumerate(expansion["regex"]):
            matched = re.match(regex, regex_string)
            if matched:
                matched = matched.groupdict()["remove"]
                regex_string = regex_string.replace(matched, expansion["replace"][ix])
                modified = True
        if modified:
            expanded_regexes.append(regex_string)
            lgr.debug("\t* Generated expansion:\n\t%s", regex_string)

    return expanded_regexes


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
    >>> from bidsschematools import validator
    >>> bids_paths = '~/.data2/datalad/000026/rawdata'
    >>> schema_version='{module_path}/data/schema/'
    >>> validator.validate_bids(bids_paths, schema_version=schema_version)"

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
    bids_version = schema._get_bids_version(bids_schema_dir)
    validation_result["bids_version"] = bids_version

    log_errors(validation_result)

    if report_path:
        if isinstance(report_path, str):
            write_report(validation_result, report_path=report_path)
        else:
            write_report(validation_result)

    return validation_result
