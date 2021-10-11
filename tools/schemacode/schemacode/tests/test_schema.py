"""Tests for the schemacode package."""
import pytest

from schemacode import schema


def test_load_schema(schema_dir):
    bad_path = "/path/to/nowhere"
    with pytest.raises(ValueError):
        schema.load_schema(bad_path)

    schema_obj = schema.load_schema(schema_dir)
    assert isinstance(schema_obj, dict)
