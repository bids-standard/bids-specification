"""Tests for the schemacode package."""
import os

from schemacode import render


def test_make_entity_definitions(schema_obj):
    """
    Test whether expected format strings are present.
    This should be stable with respect to schema format.
    """
    schema_text = render.make_entity_definitions(schema_obj)
    expected_formats = [
        "Format: `sub-<label>`",
        "Format: `ses-<label>`",
        "Format: `sample-<label>`",
        "Format: `task-<label>`",
        "Format: `acq-<label>`",
        "Format: `ce-<label>`",
        "Format: `trc-<label>`",
        "Format: `stain-<label>`",
        "Format: `rec-<label>`",
        "Format: `dir-<label>`",
        "Format: `run-<index>`",
        "Format: `mod-<label>`",
        "Format: `echo-<index>`",
        "Format: `flip-<index>`",
        "Format: `inv-<index>`",
        "Format: `mt-<label>`",
    ]
    for expected_format in expected_formats:
        assert expected_format in schema_text


def test_make_glossary(schema_obj, schema_dir):
    """
    Test whether files under the schema objects subdirectory correspond to entries, and
    that rules are not mis-loaded as objects.
    This may need to be updated for schema hierarchy changes.
    """
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
    rules_only = list(filter(lambda a: a not in object_files, rule_files))

    glossary = render.make_glossary(schema_obj)
    for line in glossary.split("\n"):
        if line.startswith('<a name="objects.'):
            # Are all objects objects?
            assert any([line.startswith(f'<a name="objects.{i}') for i in object_files])
            # Are rules loaded incorrectly?
            assert not any([line.startswith(f'<a name="objects.{i}') for i in rules_only])


def test_make_filename_template(schema_obj, schema_dir):
    """
    Test whether:
        * the base hierarchy structure of mandatory subject and optional session is
        returned. This should be robust with respect to schema format.
        * each directory contains at least one possible pattern.
        This should be robust with respect to schema format.
        * all files under the datatype rules subdirectory have corresponding entries.
        This may need to be updated for schema hierarchy changes.
    """
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
    datatype_bases = [f"        {i}/" for i in datatype_bases]
    datatype_level = False
    datatype_file_start = "            sub-<label>"
    datatype_bases_found = 0
    for line in filename_template.split("\n"):
        if datatype_level:
            # Is there at least one file pattern per datatype?
            assert line.startswith(datatype_file_start)
            datatype_level = False
        if line in datatype_bases:
            datatype_level = True
            datatype_bases_found += 1
    # Are all datatypes listed?
    assert datatype_bases_found == datatype_count


def test_make_entity_table(schema_obj):
    """
    Test whether expected entities are present and listed correctly.
    This should be robust with respect to schema format.
    """
    entity_table = render.make_entity_table(schema_obj)

    # Non-exhaustive list covering both value and index formats
    expected_entities = [
        "[`acq-<label>`](09-entities.md#acq)",
        "[`ses-<label>`](09-entities.md#ses)",
        "[`sample-<label>`](09-entities.md#sample)",
        "[`task-<label>`](09-entities.md#task)",
        "[`acq-<label>`](09-entities.md#acq)",
        "[`ce-<label>`](09-entities.md#ce)",
        "[`trc-<label>`](09-entities.md#trc)",
        "[`stain-<label>`](09-entities.md#stain)",
        "[`rec-<label>`](09-entities.md#rec)",
        "[`dir-<label>`](09-entities.md#dir)",
        "[`run-<index>`](09-entities.md#run)",
    ]

    for expected_entity in expected_entities:
        assert expected_entity in entity_table


def test_make_suffix_table(schema_obj):
    """
    Test whether expected suffixes are present and listed with correct names.
    Values are hard-coded from the present YAML, but should nevertheless be robust
    with respect to schema format, other than case changes for the names.
    """
    target_suffixes = [
        "beh",
        "cbv",
        "dwi",
    ]
    suffix_table = render.make_suffix_table(schema_obj, target_suffixes)

    expected_names = [
        "Behavioral recording",
        "Cerebral blood volume image",
        "Diffusion-weighted image",
    ]

    for expected_name in expected_names:
        assert expected_name in suffix_table


def test_make_metadata_table(schema_obj):
    """
    Test whether expected metadata fields are present and the requirement level is
    applied correctly.
    This should be robust with respect to schema format.
    """
    target_metadata = {
        "Authors": "required",
        "BIDSVersion": "required",
        "DatasetDOI": "optional",
    }
    metadata_table = render.make_metadata_table(schema_obj, target_metadata).split("\n")

    metadata_tracking = list(target_metadata.keys())

    for line in metadata_table:
        for i in metadata_tracking:
            if i in line:
                # Is the requirement level displayed correctly?
                assert target_metadata[i] in line
                # Mark found
                metadata_tracking.remove(i)

    # Have we found all fields?
    assert len(metadata_tracking) == 0


def test_make_columns_table(schema_obj):
    """
    Test whether expected columns are present and the requirement level is applied
    correctly.
    This should be robust with respect to schema format.
    """
    target_columns = {
        "time": "required",
        "trial_type": "required",
        "units": "optional",
    }
    columns_table = render.make_columns_table(schema_obj, target_columns).split("\n")

    columns_tracking = list(target_columns.keys())

    for line in columns_table:
        for i in columns_tracking:
            if i in line:
                # Is the requirement level displayed correctly?
                assert target_columns[i] in line
                # Mark found
                columns_tracking.remove(i)

    # Have we found all fields?
    assert len(columns_tracking) == 0
