import pytest
from jsonschema.exceptions import ValidationError

from bidsschematools.schema import load_schema
from bidsschematools.validate_schema import validate_schema


def test_valid_schema():
    """Test that a valid schema does not raise an error."""
    schema = load_schema()
    validate_schema(schema)


def test_add_legal_field():
    """Test that adding a legal field does not raise an error."""
    schema = load_schema()
    schema["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "optional"
    validate_schema(schema)


def test_invalid_value():
    """Test that an invalid value raises an error."""
    schema = load_schema()
    schema["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "invalid"
    with pytest.raises(ValidationError) as e:
        validate_schema(schema)

    assert "invalid" in str(e.value)
