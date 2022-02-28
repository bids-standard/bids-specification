"""Tests for the schemacode package."""
import pytest
import os

from schemacode import render

def test_make_entity_definitions(schema_obj):
    schema_text = render.make_entity_definitions(schema_obj)
    assert "Format: `sub-<label>`" in schema_text
    assert "Format: `ses-<label>`" in schema_text
    assert "Format: `sample-<label>`" in schema_text
    assert "Format: `task-<label>`" in schema_text
    assert "Format: `acq-<label>`" in schema_text
    assert "Format: `ce-<label>`" in schema_text

def test_make_glossary(schema_obj, schema_dir):
    # Test consistency
    object_files = []
    for root, dirs, files in os.walk(schema_dir, topdown=False):
       if "objects" in root:
           for object_file in files:
               object_base, _ = os.path.splitext(object_file)
               object_files.append(object_base)
    rule_files = []
    for root, dirs, files in os.walk(schema_dir, topdown=False):
       if "rules" in root:
           for rule_file in files:
               rule_base, _ = os.path.splitext(rule_file)
               rule_files.append(rule_base)
    objects_only = list(filter(lambda a: a not in rule_files, object_files))
    rules_only = list(filter(lambda a: a not in object_files, rule_files))

    glossary = render.make_glossary(schema_obj)
    for line in glossary.split('\n'):
        if line.startswith('<a name="objects.'):
            # Are all objects objects?
            assert any([line.startswith(f'<a name="objects.{i}') for i in object_files])
            assert not any([line.startswith(f'<a name="objects.{i}') for i in rules_only])

def test_make_filename_template(schema_obj, schema_dir):
    filename_template = render.make_filename_template(schema_obj)

    # Test predefined substrings
    expected_template_part = """
sub-<label>/
    [ses-<label>/]
        anat/
    """
    assert expected_template_part in filename_template

    # Test consistency
    datatype_bases = []
    for root, dirs, files in os.walk(schema_dir, topdown=False):
       if "datatype" in root:
           for datatype_file in files:
               datatype_base, _ = os.path.splitext(datatype_file)
               datatype_bases.append(datatype_base)

    datatype_count = len(datatype_bases)
    datatype_bases = [f'        {i}/' for i in datatype_bases]
    datatype_level = False
    datatype_file_start = '            sub-<label>'
    datatype_bases_found = 0
    for line in filename_template.split('\n'):
        if datatype_level:
            # Is there at least one file pattern per datatype?
            assert line.startswith(datatype_file_start)
            datatype_level = False
        if line in datatype_bases:
            datatype_level = True
            datatype_bases_found+=1
    # Are all datatypes listed?
    assert datatype_bases_found == datatype_count
