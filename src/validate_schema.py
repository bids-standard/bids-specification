import glob
import json
from pathlib import Path

import jsonschema
import yaml
from jsonschema import Draft7Validator

objects_schema_path = Path(__file__).resolve().parent / "schema" / "metaschema" / "objects.schema.yaml"
schema_path = Path(__file__).resolve().parent / "schema"

with open(objects_schema_path, "r") as f:
    objects_schema = yaml.safe_load(f)

for rel_path, spec in objects_schema.items():

    with open(schema_path / f"{rel_path}.yaml", "r") as f:
        instance = yaml.safe_load(f)

    # Validate keys
    for key, fields in instance.items():
        required_fields = spec.get("required", [])
        all_fields = required_fields + spec.get("optional", [])

        # Check if all required fields are present
        missing_required = [field for field in required_fields if field not in fields]
        if missing_required:
            raise AssertionError(f"Missing required fields {missing_required} in {key}")

        # Check if all fields are valid (either required or optional)
        invalid_fields = [field for field in fields if field not in all_fields]
        if invalid_fields:
            raise AssertionError(f"Invalid fields {invalid_fields} in {key}")

    # Validate values against json schema
    instance_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": instance,
    }

    jsonschema.validate(instance_schema, Draft7Validator.META_SCHEMA)
    print(f"Schema {rel_path} is valid.")


# validate associations
with open(schema_path / "meta" / "associations.yaml", "r") as f:
    associations = yaml.safe_load(f)

with open(schema_path / "metaschema" / "associations.schema.json", "r") as f:
    associations_schema = json.load(f)

jsonschema.validate(associations, associations_schema)


def validate_dir(dir, schema_path):
    with open(schema_path, "r") as f:
        schema = json.load(f)

    for fpath in glob.glob(str(dir / "*.yaml")):
        with open(fpath, "r") as f:
            instance = yaml.safe_load(f)
        jsonschema.validate(instance, schema)


validate_dir(
    schema_path / "rules" / "checks",
    schema_path / "metaschema" / "checks.schema.json"
)

validate_dir(
    schema_path / "rules" / "files" / "raw",
    schema_path / "metaschema" / "raw.schema.json",
)


