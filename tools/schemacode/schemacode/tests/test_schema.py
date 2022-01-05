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
    }
    for pattern, test_list in GOOD_PATTERNS.items():
        pattern_format = schema_obj["objects"]["formats"][pattern]["pattern"]
        search_pattern = "^" + pattern_format + "$"
        search = re.compile(search_pattern)
        for test_string in test_list:
            assert bool(search.fullmatch(test_string))

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
