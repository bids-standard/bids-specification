"""Tests for the schemacode package."""
import pytest

from schemacode import schema


def test_load_schema(schema_dir):
    """Smoke test for schemacode.schema.load_schema."""
    # Pointing to a nonexistent folder should raise a ValueError
    bad_path = "/path/to/nowhere"
    with pytest.raises(ValueError):
        schema.load_schema(bad_path)

    # Otherwise the function should return a dictionary
    schema_obj = schema.load_schema(schema_dir)
    assert isinstance(schema_obj, dict)


def test_object_definitions(schema_obj):
    """Ensure that object definitions in the schema contain required fields."""
    for obj_type, obj_type_def in schema_obj["objects"].items():
        for obj_key, obj_def in obj_type_def.items():
            # Private/inheritable definitions (ones starting with "_") do not need to conform to
            # the same rules as user-facing terms, so we skip them
            if obj_key.startswith("_"):
                continue

            assert "name" in obj_def.keys(), obj_key
            assert "description" in obj_def.keys(), obj_key


def test_formats(schema_obj):
    """Test valid string patterns allowed by the specification."""
    import re

    # Check that valid strings match the search pattern.
    GOOD_PATTERNS = {
        "label": ["01", "test", "test01", "Test01"],
        "index": ["01", "1", "10000", "00001"],
        "string": ["any string is valid."],
        "integer": ["5", "10", "-5", "-10"],
        "number": ["5", "3.14", "-5", "-3.14"],
        "boolean": ["true", "false"],
        "date": ["2022-01-05", "2022-01-05UTC", "2022-50-50"],
        "datetime": [
            "2022-01-05T13:16:30",
            "2022-01-05T13:16:30.05",
            "2022-01-05T13:16:30UTC",
            "2022-01-05T13:16:30.05UTC",
        ],
        "time": ["13:16:30"],
        "unit": ["any string is valid."],
        "stimuli_relative": ["any/arbitrary/path/file.txt"],
        "dataset_relative": ["any/arbitrary/path/file.txt"],
        "participant_relative": ["any/arbitrary/path/file.txt"],
        "rrid": ["RRID:SCR_017398"],
        "uri": ["foo://example.com:8042/over/there?name=ferret#nose"],
        "bids_uri": [
            "bids::sub-01/fmap/sub-01_dir-AP_epi.nii.gz",
            "bids:ds000001:sub-02/anat/sub-02_T1w.nii.gz",
            "bids:myderivatives:sub-03/func/sub-03_task-rest_space-MNI152_bold.nii.gz",
        ],
    }
    for pattern, test_list in GOOD_PATTERNS.items():
        pattern_format = schema_obj["objects"]["formats"][pattern]["pattern"]
        search_pattern = "^" + pattern_format + "$"
        search = re.compile(search_pattern)
        for test_string in test_list:
            assert bool(
                search.fullmatch(test_string)
            ), f"'{test_string}' is not a valid match for the pattern '{search.pattern}'"

    # Check that invalid strings do not match the search pattern.
    BAD_PATTERNS = {
        "label": ["test_01", "!", "010101-"],
        "index": ["test", "0.1", "0-1", "0_1"],
    }
    for pattern, test_list in BAD_PATTERNS.items():
        pattern_format = schema_obj["objects"]["formats"][pattern]["pattern"]
        search_pattern = "^" + pattern_format + "$"
        search = re.compile(search_pattern)
        for test_string in test_list:
            assert not bool(search.fullmatch(test_string))
