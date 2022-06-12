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
