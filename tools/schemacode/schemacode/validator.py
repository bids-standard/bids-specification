import datetime
import json
import os
import re
from copy import deepcopy

from . import schema, utils

lgr = utils.get_logger()

# The list of which entities create directories could be dynamically specified by the YAML, but for
# now, it is not.
# Ordering is important, as "subject" follows "session" alphabetically, but is hierarchically
# above it.
DIR_ENTITIES = ["subject", "session"]


def _get_paths(bids_paths):
    """
    Get all paths from a list of directories, excluding hidden subdirectories from distribution.

    Parameters
    ----------
    bids_paths : list or str
        Directories from which to get paths, may also contain file paths, which will remain
        unchanged.

    Notes
    -----
    * Figure out how to return paths from BIDS root.
    * Deduplicate paths (if input dirs are subsets of other input dirs), might best be done at the
        very end.
    * Specifying file paths currently breaks because they are truncated based on the bids_paths
        input.
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
    # Inelegant hard-coded solution.
    # Could be replaced by a maximum depth limit if BIDS root auto-detection is implemented.
    treat_as_file_suffix = [".ngff"]

    path_list = []
    for bids_path in bids_paths:
        bids_path = os.path.abspath(os.path.expanduser(bids_path))
        if os.path.isfile(bids_path):
            path_list.append(bids_path)
            continue
        for root, dirs, file_names in os.walk(bids_path, topdown=False):
            if any(root.endswith(i) for i in treat_as_file_suffix):
                continue
            if any(f"{i}/" in root for i in treat_as_file_suffix):
                continue
            if any(f"{i}\\" in root for i in treat_as_file_suffix):
                continue
            # will break if BIDS ever puts meaningful data under `/.{dandi,datalad,git}*/`
            if any(exclude_subdir in root for exclude_subdir in exclude_subdirs):
                continue
            for file_name in file_names:
                if file_name in exclude_files:
                    continue
                file_path = os.path.join(root, file_name)
                # This will need to be replaced with bids root finding.
                path_list.append(file_path)

    # Standardize Windows paths
    if "\\" in path_list[0]:
        for ix, i in enumerate(path_list):
            path_list[ix] = i.replace("\\", "/")

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


def _add_subdirs(regex_string, variant, datatype, entity_definitions, modality_datatypes):
    """Add appropriate subdirectories as required by entities present."""

    label = "([a-z,A-Z,0-9]*?)"

    regex_dirs = "/"
    for dir_entity in DIR_ENTITIES:
        if dir_entity in variant["entities"].keys():
            shorthand = entity_definitions[dir_entity]["entity"]
            if variant["entities"][dir_entity] == "required":
                regex_subdir = f"{shorthand}-(?P<{dir_entity}>{label})/"
            else:
                regex_subdir = f"(|{shorthand}-(?P<{dir_entity}>{label})/)"
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
    schema_dir,
):
    """
    Create full path regexes for top level files, as documented by a target BIDS YAML schema
    version.

    Parameters
    ----------
    schema_dir : str
        A string pointing to a BIDS directory for which paths should be validated.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    my_schema = schema.load_schema(schema_dir)
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
    schema_dir,
):
    """Create full path regexes for entities, as documented by a target BIDS YAML schema version.

    Parameters
    ----------
    schema_dir : str
        A string pointing to a BIDS directory for which paths should be validated.

    Notes
    -----

    * Couldn't find where the `label` type is defined as alphanumeric, hard-coding
        `entity_definitions["subject"]["format"]`-type entries as`[a-z,A-Z,0-9]*?` for the time
        being.
        Apparently there is a `label` (alphanumeric) versus `index` (integer) specification:
        https://github.com/bids-standard/bids-specification/issues/956#issuecomment-992967479
        but this is not yet used in the YAML.
    * Suggest to BIDS-specification to remove the periods from the extensions, the leading period
        is not part of the extension, but a delimiter defining the fact that it's an extension.
        Code sections marked as `Making it period-safe` should be edited when this fix is in,
        though they will work in any case.
        https://github.com/bids-standard/bids-specification/issues/990
    * More issues in comments.
    * Using pre 3.8 string formatting for legibility.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    my_schema = schema.load_schema(schema_dir)

    label = "([a-z,A-Z,0-9]*?)"

    # Parsing tabular_metadata as a datatype, might be done automatically if the YAML is moved
    # to the same subdirectory
    my_schema["rules"]["datatypes"]["tabular_metadata"] = my_schema["rules"]["tabular_metadata"]
    datatypes = my_schema["rules"]["datatypes"]
    entity_order = my_schema["rules"]["entities"]
    entity_definitions = my_schema["objects"]["entities"]
    # Descriptions are not needed and very large.
    for i in entity_definitions.values():
        i.pop("description", None)

    # Needed for non-modality file separation as per:
    # https://github.com/bids-standard/bids-specification/pull/985#issuecomment-1019573787
    modalities = my_schema["rules"]["modalities"]
    modality_datatypes = []
    for modality_key in modalities.keys():
        for modality_datatype in modalities[modality_key]["datatypes"]:
            modality_datatypes.append(modality_datatype)

    regex_schema = []
    for datatype in datatypes:
        for variant in datatypes[datatype]:
            regex_entities = ""
            for entity in entity_order:
                # Slightly awkward construction to account for new-style file specification.
                # As in:
                # https://github.com/bids-standard/bids-specification/pull/987
                try:
                    if entity in variant["entities"]:
                        entity_shorthand = entity_definitions[entity]["entity"]
                        if "enum" in entity_definitions[entity].keys():
                            # Entity key-value pattern with specific allowed values
                            # tested, works!
                            variable_field = "({})".format(
                                "|".join(entity_definitions[entity]["enum"]),
                            )
                        else:
                            variable_field = label
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
                regex_string, variant, datatype, entity_definitions, modality_datatypes
            )

            regex_string = f".*?{regex_string}$"
            regex_entry = {
                "regex": regex_string,
                "mandatory": False,
            }
            regex_schema.append(regex_entry)

    return regex_schema


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
    """

    all_regex = load_entities(
        schema_dir=schema_dir,
    )
    top_level_regex = load_top_level(
        schema_dir=schema_dir,
    )
    all_regex.extend(top_level_regex)

    return all_regex


def validate_all(
    bids_paths,
    regex_schema,
    debug=False,
):
    """
    Validate `bids_paths` based on a `regex_schema` dictionary list, including regexes.

    Parameters
    ----------
    bids_paths : list or str
        A string pointing to a BIDS directory for which paths should be validated.
    regex_schema : list of dict
        A list of dictionaries as generated by `load_all()`.
    debug : tuple, optional
        Whether to print itemwise notices for checks on the console, and include them in the
        validation result.

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
    paths_list = _get_paths(bids_paths)
    tracking_paths = deepcopy(paths_list)
    if debug:
        itemwise_results = []
    matched = False
    match_listing = []
    for target_path in paths_list:
        if debug:
            print(f"Checking file `{target_path}`.")
            print("Trying file types:")
        for regex_entry in tracking_schema:
            target_regex = regex_entry["regex"]
            if debug:
                print(f"\t* {target_path}, with pattern: {target_regex}")
            matched = re.match(target_regex, target_path)
            if debug:
                itemwise_result = {}
                itemwise_result["path"] = target_path
                itemwise_result["regex"] = target_regex
            if matched:
                if debug:
                    print("Match identified.")
                    itemwise_result["match"] = True
                    itemwise_results.append(itemwise_result)
                break
            if debug:
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
            if debug:
                print(f"The `{target_path}` file could not be matched to any regex schema entry.")
    results = {}
    if debug:
        results["itemwise"] = itemwise_results
    results["schema_tracking"] = tracking_schema
    results["schema_listing"] = regex_schema
    results["path_tracking"] = tracking_paths
    results["path_listing"] = paths_list
    results["match_listing"] = match_listing

    return results


def write_report(
    validation_result,
    report_path="/var/tmp/bids-validator/report_{}.log",
    datetime_format="%Y%m%d-%H%M%S",
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
        A path under which the report is to be saved, the `{}` string, if included, will be
        expanded to current datetime, as per the `datetime_format` parameter.
    datetime_format : str, optional
        A datetime format, optionally used for the report path.

    Notes
    -----
    * Not using f-strings in order to prevent arbitrary code execution.
    """

    report_path = report_path.format(datetime.datetime.now().strftime(datetime_format))
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
                    f'- Comparing the `{comparison["path"]}` path to the `{comparison["regex"]}` "\
                    resulted in {comparison_result}.\n'
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


def _find_dataset_description(my_path):
    candidate = os.path.join(my_path, "dataset_description.json")
    if my_path == "/":
        return None
    if os.path.isfile(candidate):
        return candidate
    else:
        level_up = os.path.dirname(my_path.rstrip("/"))
        return _find_dataset_description(level_up)


def select_schema_dir(
    bids_paths,
    schema_reference_root,
    schema_version,
    schema_min_version="1.7.0",
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
    schema_version : str or None, optional
        Version of BIDS schema, or path to schema.
        If a path is given, this will be expanded and used directly, not concatenated with
        `schema_reference_root`.
        If the path starts with the string "{module_path}" it will be expanded relative to the
        module path.
        If None, the `dataset_description.json` fie will be queried for the dataset schema version.
    schema_min_version : str, optional
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
    if schema_version:
        if "/" in schema_version:
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
        if dataset_description:
            if dataset_description in dataset_descriptions:
                raise ValueError(
                    "You have selected files belonging to 2 different datasets."
                    "Please run the validator once per dataset."
                )
            else:
                with open(dataset_description) as f:
                    dataset_info = json.load(f)
                    try:
                        schema_version = dataset_info["BIDSVersion"]
                    except KeyError:
                        lgr.warning(
                            "BIDSVersion is not specified in "
                            "`dataset_description.json`. "
                            f"Falling back to {schema_min_version}."
                        )
                        schema_version = schema_min_version
        if schema_min_version:
            if schema_version < schema_min_version:
                lgr.warning(
                    f"BIDSVersion {schema_version} is less than the minimal working "
                    "{schema_min_version}. "
                    "Falling back to {schema_min_version}. "
                    "To force the usage of earlier versions specify them explicitly "
                    "when calling the validator."
                )
                schema_version = schema_min_version
    schema_dir = os.path.join(schema_reference_root, schema_version)
    if os.path.isdir(schema_dir):
        return schema_dir
    else:
        raise ValueError(
            f"The expected schema directory {schema_dir} does not exist on the system."
            "Please ensure the file exists or manually specify a schema version for "
            "which the schemacode files are available on your system."
        )


def validate_bids(
    bids_paths,
    schema_reference_root="/usr/share/bids-schema/",
    schema_version=None,
    debug=False,
    report_path=False,
):
    """
    Validate paths according to BIDS schema.

    Parameters
    ----------
    paths : str or list of str
        Paths which to validate, may be individual files or directories.
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

    Returns
    -------
    results : dict
        A dictionary reporting the target files for validation, the unmatched files and unmatched
        regexes, and optionally the itemwise comparison results.
        Keys include "schema_tracking", "path_tracking", "path_listing", "match_listing", and
        optionally "itemwise"

    Examples
    --------
    >>> from schemacode import validator
    >>> bids_paths = '~/.data2/datalad/000026/rawdata'
    >>> schema_version='{module_path}/data/schema/'
    >>> validator.validate_bids(bids_paths, schema_version=schema_version, debug=False)"

    Can be run from the Bash shell as:
        python -c "from schemacode import validator; validator.validate_bids\
                ('~/.data2/datalad/000026/rawdata', schema_version='{module_path}/data/schema/',\
                report_path=True, debug=False)"`
    """

    if isinstance(bids_paths, str):
        bids_paths = [bids_paths]

    bids_schema_dir = select_schema_dir(bids_paths, schema_reference_root, schema_version)
    regex_schema = load_all(bids_schema_dir)
    validation_result = validate_all(
        bids_paths,
        regex_schema,
        debug=debug,
    )
    # Record schema version.
    # Not sure whether to incorporate in validation_result.
    if bids_schema_dir == os.path.join(os.path.abspath(os.path.dirname(__file__)),"data/schema",):
        schema_version = 9999
    else:
        _, schema_version = os.path.split(bids_schema_dir)
    validation_result["bids_schema_version"] = schema_version

    if report_path:
        if isinstance(report_path, str):
            write_report(validation_result, report_path=report_path)
        else:
            write_report(validation_result)

    return validation_result
