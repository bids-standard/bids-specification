import pytest
from jsonschema.exceptions import ValidationError

from bidsschematools.validate_schema import (
    dereference_schema,
    load_schema,
    validate_schema,
    schema_path
)


def test_load_schema():
    """Test that a valid schema does not raise an error."""
    load_schema(schema_path)


def test_derefence_schema():
    """Test that a valid schema does not raise an error."""
    schema = load_schema(schema_path)
    dereference_schema(schema)


def test_valid_schema():
    """Test that a valid schema does not raise an error."""
    schema = load_schema(schema_path)
    validate_schema(schema)


def test_broken_reference():
    """Test that a broken reference raises an error."""
    schema = load_schema(schema_path)
    schema["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "$ref"
    ] = "broken.reference"
    with pytest.raises(KeyError) as e:
        dereference_schema(schema)

    assert "'broken'" in str(e.value)


def test_add_legal_field():
    """Test that adding a legal field does not raise an error."""
    schema = load_schema(schema_path)
    schema["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "optional"
    validate_schema(schema)


def test_invalid_value():
    """Test that an invalid value raises an error."""
    schema = load_schema(schema_path)
    schema["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "invalid"
    with pytest.raises(ValidationError) as e:
        validate_schema(schema)

    assert "invalid" in str(e.value)
