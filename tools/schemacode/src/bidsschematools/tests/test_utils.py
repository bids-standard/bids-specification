from contextlib import nullcontext
from typing import Any, cast

import pytest
from jsonschema.exceptions import SchemaError, ValidationError
from jsonschema.protocols import Validator as JsonschemaValidator
from jsonschema.validators import Draft7Validator, Draft202012Validator

from bidsschematools.utils import jsonschema_validator

DRAFT_7_SCHEMA = {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {"name": {"type": "string"}},
    "required": ["name"],
}
"""
A minimal valid Draft 7 schema requiring a 'name' property of type 'string'.
"""


DRAFT_202012_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"title": {"type": "string"}},
    "required": ["title"],
}
"""
A minimal valid Draft 2020-12 schema requiring a 'title' property of type 'string'.
"""

DRAFT_202012_FORMAT_SCHEMA = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "type": "object",
    "properties": {"email": {"type": "string", "format": "email"}},
    "required": ["email"],
}
"""
Draft 2020-12 schema that includes a 'format' requirement (e.g., 'email').
Used to test the 'check_format' parameter.
"""


SCHEMA_NO_DOLLAR_SCHEMA = {
    "type": "object",
    "properties": {"foo": {"type": "string"}},
    "required": ["foo"],
}
"""
Schema that lacks the '$schema' property altogether.
Used to test that 'default_cls' is applied.
"""


class TestJsonschemaValidator:
    @pytest.mark.parametrize(
        ("schema", "expected_validator_cls"),
        [
            pytest.param(DRAFT_202012_FORMAT_SCHEMA, Draft202012Validator, id="Draft202012"),
            pytest.param(DRAFT_7_SCHEMA, Draft7Validator, id="Draft7"),
        ],
    )
    @pytest.mark.parametrize("check_format", [True, False])
    def test_set_by_dollar_schema(
        self,
        schema: dict[str, Any],
        expected_validator_cls: type,
        check_format: bool,
    ) -> None:
        """
        Test that the correct validator class is returned for different '$schema' values
        """
        validator = jsonschema_validator(schema, check_format=check_format)

        assert isinstance(validator, expected_validator_cls)

    @pytest.mark.parametrize(
        ("check_format", "instance", "expect_raises"),
        [
            (True, {"email": "test@example.com"}, False),
            (True, {"email": "not-an-email"}, True),
            (False, {"email": "not-an-email"}, False),
        ],
        ids=[
            "check_format=True, valid email",
            "check_format=True, invalid email",
            "check_format=False, invalid email",
        ],
    )
    def test_check_format_email_scenarios(
        self,
        check_format: bool,
        instance: dict,
        expect_raises: bool,
    ) -> None:
        """
        Parametrized test for check_format usage on valid/invalid email addresses under
        Draft202012Validator.
        """
        validator = jsonschema_validator(DRAFT_202012_FORMAT_SCHEMA, check_format=check_format)

        # If expect_raises is True, we use pytest.raises(ValidationError)
        # Otherwise, we enter a no-op context
        ctx = pytest.raises(ValidationError) if expect_raises else nullcontext()

        with ctx:
            validator.validate(instance)  # Should raise or not raise as parametrized

    @pytest.mark.parametrize(
        ("schema", "expected_validator_cls"),
        [
            # Scenario 1: no $schema => we expect the default_cls=Draft7Validator is used
            pytest.param(SCHEMA_NO_DOLLAR_SCHEMA, Draft7Validator, id="no-$schema"),
            # Scenario 2: has $schema => draft 2020-12 overrides the default_cls
            pytest.param(DRAFT_202012_SCHEMA, Draft202012Validator, id="with-$schema"),
        ],
    )
    def test_default_cls(
        self,
        schema: dict[str, Any],
        expected_validator_cls: type,
    ) -> None:
        """
        If the schema has no '$schema' property, and we provide a 'default_cls',
        the returned validator should be an instance of that class.

        If the schema *does* have '$schema', then the default_cls is ignored, and
        the validator class is inferred from the schema's '$schema' field.
        """
        # Provide default_cls=Draft7Validator
        validator = jsonschema_validator(
            schema,
            check_format=False,
            default_cls=cast(type[JsonschemaValidator], Draft7Validator),
        )
        assert isinstance(validator, expected_validator_cls)

    def test_invalid_schema_raises_schema_error(self) -> None:
        """
        Provide an invalid schema, ensuring that 'SchemaError' is raised.
        """
        invalid_schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": 123,  # 'type' must be string/array, so this is invalid
        }
        with pytest.raises(SchemaError):
            jsonschema_validator(invalid_schema, check_format=False)
