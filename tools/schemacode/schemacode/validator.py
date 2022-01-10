import datetime
import re
import os
import yaml
import json

from copy import deepcopy

def _get_paths(bids_dir):

	bids_dir = os.path.abspath(os.path.expanduser(bids_dir))
	path_list=[]
	for root, dirs, file_names in os.walk(bids_dir, topdown=False):
		for file_name in file_names:
			file_path = os.path.join(root,file_name)
			file_path = file_path[len(bids_dir):]
			path_list.append(file_path)
	return path_list

def _add_entity(regex_entities, entity_shorthand, variable_field, requirement_level):
	"""Add entity pattern to filename template based on requirement level."""
	if requirement_level == "required":
		if len(regex_entities.strip()):
			regex_entities += f'_{entity_shorthand}-{variable_field}'
		else:
			# Only the first entity doesn't need an underscore
			regex_entities += f'{entity_shorthand}-{variable_field}'
	else:
		if len(regex_entities.strip()):
			regex_entities += f'(|_{entity_shorthand}-{variable_field})'
		else:
			# Only the first entity doesn't need an underscore
			regex_entities += f'(|{entity_shorthand}-{variable_field})'

	return regex_entities

def create_regex_schema(
	schema_path='schemacode/data/schema',
	top_level_path = 'rules/top_level_files.yaml',
	datatypes_path = 'rules/datatypes/',
	debug=True,
	):
	"""
	Create a regex schema dictionary from the bids-specification YAML files directly.

	Notes
	-----
	Currently only a very small part of the schema is parsed.
	Problems may arise with files further down the hierarchy where custom (fragile) logic might be needed for schema assembly.
	Top-lefel files can be identified easily, but datatypes aren't named in a readable form in the YAML.
	The code used to generate this HTML, might be usable for regex autogeneration as well:
		https://bids-specification.readthedocs.io/en/latest/99-appendices/04-entity-table.html
	"""

	schema_path = os.path.abspath(os.path.expanduser(schema_path))
	top_level_path = os.path.join(schema_path,top_level_path)
	datatypes_path = os.path.join(schema_path,datatypes_path)
	regex_schema = {}
	with open(top_level_path) as yaml_file:
		yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
	for file_type in yaml_data.keys():
		if yaml_data[file_type]['extensions'] != ['None']:
			extensions = yaml_data[file_type]['extensions']
			# The presence of the dot is determined by them being extensions.
			harmonized_extensions = []
			for extension in extensions:
				if extension[0] == '.':
					harmonized_extensions.append(extension[1:])
				else:
					harmonized_extensions.append(extension)
			extensions_regex = '|'.join(harmonized_extensions)
			pattern = '^/{file_type}\.({extensions})$'.format(
					file_type=file_type,
					extensions=extensions_regex,
					)
		else:
			pattern = '^/{file_type}$'.format(file_type=file_type)
		yaml_data[file_type]['regex'] = pattern
		yaml_data[file_type]['unique'] = True
	regex_schema.update(yaml_data)

	for datatype_file in os.listdir(datatypes_path):
		datatype_path = os.path.join(datatypes_path,datatype_file)
		if debug:
			print('Parsing `{}`'.format(datatype_path))
		with open(datatype_path) as yaml_file:
			yaml_data = yaml.load(yaml_file, Loader=yaml.FullLoader)
		# Ufff, the hash-line is not parsed, and sufixes can be multiple, not really a way to refer to these types unambiguously.
		# Unless we parse the hash-lines.....
		if debug:
			print(yaml_data)

	return regex_schema

def validate(bids_dir, regex_schema,
	report=True,
	debug=True,
	):
	"""
	Validate all paths described in the `regex_schema` dictionary.

	Notes
	-----
	Multi-source validation could be accomplished by distributing the resulting tracking_schema dictionary and further eroding it.
	"""

	tracking_schema = deepcopy(regex_schema)
	paths_list = _get_paths(bids_dir)
	tracking_paths = deepcopy(paths_list)
	for path in paths_list:
		if debug:
			print('Checking file `{}`.'.format(path))
			print('Trying file types:')
		for file_type in tracking_schema.keys():
			regex = tracking_schema[file_type]['regex']
			if debug:
				print('\t* {}, with pattern: {}'.format(
					file_type,
					regex,
					))
			matched = re.match(regex,path)
			if matched:
				if debug:
					print('\t > Identified `{}` as a {} file type.'.format(
						path,
						file_type,
						))
				# the following may be nondeterministic if a file matches more than one pattern.
				# If this is the case, however, the schema is probably broken, because the matching is strict.
				if tracking_schema[file_type]['unique']:
					tracking_schema.pop(file_type)
				break
		if matched:
			tracking_paths.remove(path)
		else:
			if debug:
				print('The `{}` file could not be matched to any regex schema entry.'.format(path))

	if report:
		print('The following files were not matched by any regex schama entry:')
		print('\n-'.join(tracking_paths))
		print('The following mandatory regex schama entries did not match any files:')
		for file_type in tracking_schema:
			if tracking_schema[file_type]['required']:
				print('*{}'.format(file_type))


def load_all(
	schema_dir='schemacode/data/schema',
	debug=False,
	):
	"""Create full path regexes while trying to go by preexisting code.

	Notes
	-----

	* Couldn't find where the `label` type is defined as alphanumeric, hard-coding `entity_definitions["subject"]["format"]`-type entries as`[a-z,A-Z,0-9]*?` for the time being.
	* Suggest to BIDS-specification to remove the periods from the extensions, the leading period is not part of the extension, but a delimiter defining the fact that it's an extension. Code sections marked as `Making it period-safe` should be edited when this fix is in, though they will work in any case.
	* More issues in comments.
	* Using pre 3.8 string formatting for legibility.
	"""

	from . import schema

	my_schema = schema.load_schema(schema_dir)
	if debug:
		print(
			json.dumps(schema['rules'],
				sort_keys=True,
				indent=4,
				),
			)

	label = '([a-z,A-Z,0-9]*?)'

	datatypes = my_schema['rules']['datatypes']
	entity_order = my_schema["rules"]["entities"]
	entity_definitions = my_schema["objects"]["entities"]

	# This should be further broken up:
	# IF there is a session dir, there should be a session field in the file name, so there should be two entries for all entities below the session directory.
	regex_directories = "{}-{}/(|{}-{}/)".format(
		entity_definitions["subject"]["entity"],
		label,
		entity_definitions["session"]["entity"],
		label,
		)

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
						entity_shorthand,
						variable_field,
						variant['entities'][entity],
						)

			if len(variant['suffixes']) == 1:
				regex_suffixes = variant['suffixes'][0]
			else:
				regex_suffixes = '({})'.format(
					'|'.join(variant['suffixes'])
					)
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
			regex = '{}{}/{}_{}\.{}'.format(
				regex_directories,
				datatype,
				regex_entities,
				regex_suffixes,
				regex_extensions,
				)
			# Adding decoration, not sure why `get_path()` path listings end up starting with `/`.
			regex = '^/{}$'.format(regex)
			regex_entry = {
				'regex':regex,
				'mandatory':False,
				}
			regex_schema.append(regex_entry)

	return regex_schema

def validate_all(bids_dir, regex_schema,
	report=None,
	debug=True,
	):
	"""
	Validate all paths in `bids_dir` based on a `regex_schema` dictionary list, including regexes.

	Parameters
	----------
	bnids_dir : str
		A string pointing to a BIDS directory for which paths should be validated.
	regex_schema : list of dict
		A list of dictionaries as generated by `load_all()`.
	report : str or tuple
		A path to which to write a report file, or a tuple, controlling whether a report log should be generated under a default path.

	Notes
	-----
	* Multi-source validation could be accomplished by distributing the resulting tracking_schema dictionary and further eroding it.
	* Maybe add formattable string support for `report` rather than hard-inject it in the code.
	"""

	tracking_schema = deepcopy(regex_schema)
	paths_list = _get_paths(bids_dir)
	tracking_paths = deepcopy(paths_list)
	for path in paths_list:
		if debug:
			print(f'Checking file `{path}`.')
			print('Trying file types:')
		for regex_entry in tracking_schema:
			regex = regex_entry['regex']
			if debug:
				print(f'\t* {path}, with pattern: {regex}')
			matched = re.match(regex,path)
			if matched:
				if debug:
					print('Match identified.')
				break
		if matched:
			tracking_paths.remove(path)
			# Might be fragile since it relies on where the loop broke:
			if regex_entry['mandatory']:
				tracking_schema.remove(regex_entry)
		else:
			if debug:
				print(f'The `{path}` file could not be matched to any regex schema entry.')

	if report:
		if isinstance(report,str):
			report_str = report
		else:
			report_str = 'bids-validator-report'
		report_filename = '{}-{}.log'.format(
			report_str,
			datetime.datetime.now().strftime("%Y%m%d-%H%M%S"),
			)
		validated_files_count = len(paths_list) - len(tracking_paths)
		with open(report_filename, 'w') as f:
			f.write(f'{validated_files_count} files were successfully validated.')
			f.write('The following files were not matched by any regex schama entry:')
			f.write('\n')
			f.write('\n-'.join(tracking_paths))
			f.write('The following mandatory regex schama entries did not match any files:')
			f.write('\n')
			for entry in tracking_schema:
				if entry['mandatory']:
					f.write(f'*{file_type}')
			f.close()

def _test_regex(
	bids_dir='~/DANDI/000108',
	#bids_schema='/usr/share/bids-schema/',
	bids_schema='schemacode/data/schema',
	):
	"""
	Test with `python -c "from validator import *; _test_regex()"`
	"""

	regex_schema = create_regex_schema(bids_schema)
	print(regex_schema)
	validate(bids_dir, regex_schema)

def test_regex(
	bids_dir='~/datalad/openneuro/ds000030',
	#bids_dir='~/DANDI/000108',
	#bids_schema='/usr/share/bids-schema/',
	bids_schema='schemacode/data/schema',
	):
	"""
	Test with `python -c "from validator import *; test_regex()"`
	"""

	regex_schema = load_all(bids_schema)
	print(regex_schema)
	validate_all(bids_dir, regex_schema, report=True)
