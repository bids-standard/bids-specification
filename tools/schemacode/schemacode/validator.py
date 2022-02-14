import datetime
import json
import os
import re
import yaml

from copy import deepcopy

from . import schema


# The list of which entities create directories could be dynamically specified by the YAML, but for now, it is not.
# Ordering is important, as "subject" follows "session" alphabetically, but is hierarchically above it.
DIR_ENTITIES = ['subject', 'session']

def _get_paths(bids_paths):
    """Get all paths from a list of directories, excluding hidden subdirectories from data distribution.

    Parameters
    ----------
    bids_paths : list or str
        Directories from which to get paths, may also contain file paths, which will remain unchanged.

    Notes
    -----
    * Figure out how to return paths from BIDS root.
    * Deduplicate paths (if input dirs are subsets of other input dirs), might best be done at the very end.
    * Specifying file paths currently breaks because they are truncated based on the bids_paths input.
    """
    exclude_subdirs=[
        '/.dandi',
        '/.datalad',
        '/.git',
        ]
    # `.bidsignore` is not, in fact, a BIDS file, as per:
    # https://github.com/bids-standard/bids-specification/issues/980
    exclude_files = [
        '.gitattributes',
        '.gitignore',
        '.bidsignore',
        'dandiset.yaml',
        ]
    # Inelegant hard-coded solution.
    # Could be replaced by a maximum depth limit if BIDS root auto-detection is implemented.
    treat_as_file_suffix = [".ngff"]

    if isinstance(bids_paths, str):
        bids_paths = [bids_paths]

    path_list=[]
    for bids_path in bids_paths:
        bids_path = os.path.abspath(os.path.expanduser(bids_path))
        if os.path.isfile(bids_path):
            path_list.append(bids_path)
            continue
        for root, dirs, file_names in os.walk(bids_path, topdown=False):
            if any(root.endswith(i) for i in treat_as_file_suffix):
                continue
            # will break if BIDS ever puts meaningful data under `/.{dandi,datalad,git}*/`
            if any(exclude_subdir in root for exclude_subdir in exclude_subdirs):
                continue
            for file_name in file_names:
                if file_name in exclude_files:
                    continue
                file_path = os.path.join(root,file_name)
                # This will need to be replaced with bids root finding.
                path_list.append(file_path)
    return path_list

def _add_entity(regex_entities, entity, entity_shorthand, variable_field, requirement_level):
    """Add entity pattern to filename template based on requirement level."""

    # We need to do this here, although it would be easier to back-reference in the directory.
    # This is because regex evaluates sequentially and we can not forward-reference a group.
    if entity in DIR_ENTITIES:
        variable_regex = f'(?P={entity})'
    else:
        variable_regex = f'(?P<{entity}>{variable_field})'

    if requirement_level == "required":
        if len(regex_entities.strip()):
            regex_entities += f'_{entity_shorthand}-{variable_regex}'
        else:
            # Only the first entity doesn't need an underscore
            regex_entities += f'{entity_shorthand}-{variable_regex}'
    else:
        if len(regex_entities.strip()):
            regex_entities += f'(|_{entity_shorthand}-{variable_regex})'
        else:
            # Only the first entity doesn't need an underscore
            regex_entities += f'(|{entity_shorthand}-{variable_regex})'

    return regex_entities

def _add_extensions(regex_string, variant):
    """Add extensions to a regex string."""
    if len(variant['extensions']) == 1:
        # This only happens in `rules/datatypes/meg.yaml` once:
        if variant['extensions'][0] == '*':
            regex_extensions = '.*?'
        else:
            # Making it period-safe:
            if variant['extensions'][0][0] == '.':
                regex_extensions = variant['extensions'][0][1:]
            else:
                regex_extensions = variant['extensions'][0]
    else:
        # Making it period-safe:
        fixed_variant_extensions = []
        for variant_extension in variant['extensions']:
            if variant_extension[0] == '.':
                fixed_variant_extensions.append(variant_extension[1:])
            else:
                fixed_variant_extensions.append(variant_extension)

        regex_extensions = '({})'.format(
            '|'.join(fixed_variant_extensions)
            )
    regex_string = f'{regex_string}\.{regex_extensions}'

    return regex_string

def _add_subdirs(regex_string, variant, datatype, entity_definitions, modality_datatypes):
    """Add appropriate subdirectories as required by entities present."""

    label = '([a-z,A-Z,0-9]*?)'

    regex_dirs = '/'
    for dir_entity in DIR_ENTITIES:
        if dir_entity in variant['entities'].keys():
            shorthand = entity_definitions[dir_entity]['entity']
            if variant['entities'][dir_entity] == 'required':
                regex_subdir = f'{shorthand}-(?P<{dir_entity}>{label})/'
            else:
                regex_subdir = f'(|{shorthand}-(?P<{dir_entity}>{label})/)'
            regex_dirs = f'{regex_dirs}{regex_subdir}'
    if datatype in modality_datatypes:
        regex_dirs = f'{regex_dirs}{datatype}/'
    regex_string = f'{regex_dirs}{regex_string}'

    return regex_string

def _add_suffixes(regex_string, variant):
    """Add suffixes to a regex string."""
    if len(variant['suffixes']) == 1:
        regex_suffixes = variant['suffixes'][0]
    else:
        regex_suffixes = '({})'.format(
            '|'.join(variant['suffixes'])
            )
    regex_string = f'{regex_string}_{regex_suffixes}'

    return regex_string


def load_top_level(
    schema_dir='schemacode/data/schema',
    debug=True,
    ):
    """Create full path regexes for top level files, as documented by a target BIDS YAML schema version.

    Parameters
    ----------
    schema_dir : str, optional
        A string pointing to a BIDS directory for which paths should be validated.
    debug : tuple, optional
        Whether to print itemwise notices for checks on the console, and include them in the validation result.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    schema_dir = os.path.abspath(os.path.expanduser(schema_dir))
    my_schema = schema.load_schema(schema_dir)
    top_level_files = my_schema['rules']['top_level_files']

    regex_schema = []
    for top_level_filename in top_level_files.keys():
        top_level_file = top_level_files[top_level_filename]
        if debug:
            print(
            json.dumps(top_level_file,
                sort_keys=True,
                indent=4,
                ),
            )
        # None value gets passed as list of strings...
        extensions = top_level_file['extensions']
        if extensions != ['None']:
            periodsafe_extensions = []
            for extension in extensions:
                if extension[0] == '.':
                    periodsafe_extensions.append(extension[1:])
                else:
                    periodsafe_extensions.append(extension)
                extensions_regex = '|'.join(periodsafe_extensions)
                regex = f'^/{top_level_filename}\.({extensions_regex})$'
        else:
            regex = f'.*?/{top_level_filename}$'
        regex_entry = {
            'regex':regex,
            'mandatory':top_level_file['required'],
            }
        regex_schema.append(regex_entry)

    return regex_schema

def load_entities(
    schema_dir='schemacode/data/schema',
    debug=False,
    ):
    """Create full path regexes for entities, as documented by a target BIDS YAML schema version.

    Parameters
    ----------
    schema_dir : str, optional
        A string pointing to a BIDS directory for which paths should be validated.
    debug : tuple, optional
        Whether to print itemwise notices for checks on the console, and include them in the validation result.

    Notes
    -----

    * Couldn't find where the `label` type is defined as alphanumeric, hard-coding `entity_definitions["subject"]["format"]`-type entries as`[a-z,A-Z,0-9]*?` for the time being.
        Apparently there is a `label` (alphanumeric) versus `index` (integer) specification:
        https://github.com/bids-standard/bids-specification/issues/956#issuecomment-992967479
        but this is not yet used in the YAML.
    * Suggest to BIDS-specification to remove the periods from the extensions, the leading period is not part of the extension, but a delimiter defining the fact that it's an extension. Code sections marked as `Making it period-safe` should be edited when this fix is in, though they will work in any case.
        https://github.com/bids-standard/bids-specification/issues/990
    * More issues in comments.
    * Using pre 3.8 string formatting for legibility.

    Returns
    -------
    regex_schema : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    schema_dir = os.path.abspath(os.path.expanduser(schema_dir))
    my_schema = schema.load_schema(schema_dir)

    label = '([a-z,A-Z,0-9]*?)'

    datatypes = my_schema['rules']['datatypes']
    entity_order = my_schema["rules"]["entities"]
    entity_definitions = my_schema["objects"]["entities"]

    # Needed for non-modality file separation as per:
    # https://github.com/bids-standard/bids-specification/pull/985#issuecomment-1019573787
    modalities = my_schema['rules']['modalities']
    modality_datatypes = []
    for modality_key in modalities.keys():
        for modality_datatype in modalities[modality_key]['datatypes']:
            modality_datatypes.append(modality_datatype)

    regex_schema = []
    for datatype in datatypes:
        for variant in datatypes[datatype]:
            if debug:
                print(
                json.dumps(variant,
                    sort_keys=True,
                    indent=4,
                    ),
                )
            regex_entities = ''
            for entity in entity_order:
                # Slightly awkward construction to account for new-style file specification.
                # As in:
                # https://github.com/bids-standard/bids-specification/pull/987
                try:
                    if entity in variant['entities']:
                        if debug:
                            print(
                                json.dumps(entity_definitions[entity],
                                    sort_keys=True,
                                    indent=4,
                                    ),
                                )
                        entity_shorthand = entity_definitions[entity]['entity']
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
                            variant['entities'][entity],
                            )
                except KeyError:
                    pass

            regex_string = _add_suffixes(regex_entities, variant)
            regex_string = _add_extensions(regex_string, variant)
            regex_string = _add_subdirs(regex_string, variant, datatype, entity_definitions, modality_datatypes)

            regex_string = f'.*?{regex_string}$'
            regex_entry = {
                'regex':regex_string,
                'mandatory':False,
                }
            regex_schema.append(regex_entry)

    return regex_schema


def load_all(
    schema_dir='schemacode/data/schema',
    debug=False,
    ):
    """
    Create full path regexes for all BIDS specification files.

    Parameters
    ----------
    schema_dir : str, optional
        A string pointing to a BIDS directory for which paths should be validated.
    debug : tuple, optional
        Whether to print itemwise notices for checks on the console, and include them in the validation result.

    Returns
    -------
    all_regex : list of dict
        A list of dictionaries, with keys including 'regex' and 'mandatory'.
    """

    all_regex = load_entities(
        schema_dir=schema_dir,
        debug=debug,
        )
    top_level_regex = load_top_level(
        schema_dir=schema_dir,
        debug=debug,
        )
    all_regex.extend(top_level_regex)

    return all_regex

def validate_all(bids_paths, regex_schema,
    debug=False,
    ):
    """
    Validate all paths in `bids_paths` based on a `regex_schema` dictionary list, including regexes.

    Parameters
    ----------
    bids_paths : list or str
        A string pointing to a BIDS directory for which paths should be validated.
    regex_schema : list of dict
        A list of dictionaries as generated by `load_all()`.
    debug : tuple, optional
        Whether to print itemwise notices for checks on the console, and include them in the validation result.

    Returns
    -------
    results : dict
        A dictionary reporting the target files for validation, the unmatched files and unmatched regexes, and optionally the itemwise comparison results.
        Keys include "schema_tracking", "path_tracking", "path_listing", and, optionally "itemwise"

    Notes
    -----
    * Multi-source validation could be accomplished by distributing the resulting tracking_schema dictionary and further eroding it.
    * Currently only entities are captured in named groups, edit `load_top_level()` to name other groups as well.
    """

    tracking_schema = deepcopy(regex_schema)
    paths_list = _get_paths(bids_paths)
    tracking_paths = deepcopy(paths_list)
    if debug:
        itemwise_results = []
    matched = False
    for target_path in paths_list:
        if debug:
            print(f'Checking file `{target_path}`.')
            print('Trying file types:')
        for regex_entry in tracking_schema:
            target_regex = regex_entry['regex']
            if debug:
                print(f'\t* {target_path}, with pattern: {target_regex}')
            matched = re.match(target_regex,target_path)
            if debug:
                itemwise_result = {}
                itemwise_result['path'] = target_path
                itemwise_result['regex'] = target_regex
            if matched:
                if debug:
                    print('Match identified.')
                    itemwise_result['match'] = True
                    itemwise_results.append(itemwise_result)
                break
            if debug:
                itemwise_result['match'] = False
                itemwise_results.append(itemwise_result)
        if matched:
            tracking_paths.remove(target_path)
            # Might be fragile since it relies on where the loop broke:
            if regex_entry['mandatory']:
                tracking_schema.remove(regex_entry)
        else:
            if debug:
                print(f'The `{target_path}` file could not be matched to any regex schema entry.')
    results={}
    if debug:
        results['itemwise'] = itemwise_results
    results['schema_tracking'] = tracking_schema
    results['schema_listing'] = regex_schema
    results['path_tracking'] = tracking_paths
    results['path_listing'] = paths_list
    if matched:
        results['bids_entities'] = matched.groupdict()

    return results


def write_report(validation_result,
    report_path='bids-validator-report_{}.log',
    datetime_format='%Y%m%d-%H%M%S',
    ):
    """Write a human-readable report based on the validation result.

    Parameters
    ----------
    validation_result : dict
        A dictionary as returned by `validate_all()` with keys including "schema_tracking", "path_tracking", "path_listing", and, optionally "itemwise".
        The "itemwise" value, if present, should be a list of dictionaries, with keys including "path", "regex", and "match".
    report_path : str, optional
        A path under which the report is to be saved, the `{}` string, if included, will be expanded to current datetime, as per the `datetime_format` parameter.
    datetime_format : str, optional
        A datetime format, optionally used for the report path.

    Notes
    -----
    * Not using f-strings in order to prevent arbitrary code execution.
    """

    report_path = report_path.format(datetime.datetime.now().strftime(datetime_format))
    total_file_count = len(validation_result['path_listing'])
    validated_files_count = total_file_count - len(validation_result['path_tracking'])
    with open(report_path, 'w') as f:
        try:
            for comparison in validation_result['itemwise']:
                if comparison['match']:
                    comparison_result = 'A MATCH'
                else:
                    comparison_result = 'no match'
                f.write(f'- Comparing the `{comparison["path"]}` path to the `{comparison["regex"]}` resulted in {comparison_result}.\n')
        except KeyError:
            pass
        f.write(f'\nSUMMARY:\n{validated_files_count} out of {total_file_count} files were successfully validated, using the following regular expressions:')
        for regex_entry in validation_result['schema_listing']:
            f.write(f'\n\t- `{regex_entry["regex"]}`')
        f.write('\n')
        f.write('The following files were not matched by any regex schema entry:')
        f.write('\n\t* `')
        f.write('`\n\t* `'.join(validation_result['path_tracking']))
        f.write('\nThe following mandatory regex schema entries did not match any files:')
        f.write('\n')
        if len(validation_result['schema_tracking']) >= 1:
            for entry in validation_result['schema_tracking']:
                if entry['mandatory']:
                    f.write(f'\t** `{entry["regex"]}`\n')
        else:
            f.write('All mandatory BIDS files were found.\n')
        f.close()

def test_regex(
    #bids_paths='~/.data2/datalad/000108',
    #bids_paths='~/.data2/datalad/000026/rawdata',
    bids_paths=[
        '~/.data2/datalad/000026/rawdata/sub-EXC022/',
        '/home/chymera/.data2/datalad/000026/rawdata/sub-I38/ses-MRI/anat/sub-I38_ses-MRI-echo-1_flip-1_VFA.json',
        ],
    #bids_paths='~/datalad/openneuro/ds000030',
    #bids_paths='~/DANDI/000108',
    #bids_schema='/usr/share/bids-schema/',
    #bids_schema='schemacode/data/schema',
    bids_schema='~/src/bids-schemadata',
    debug=False,
    ):
    """
    Test with `python -c "from validator import *; test_regex()"`
    """

    regex_schema = load_all(bids_schema)
    #print(regex_schema)
    validation_result = validate_all(bids_paths, regex_schema,
            debug=debug,
            )
    write_report(validation_result)
