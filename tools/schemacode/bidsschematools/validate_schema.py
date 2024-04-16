import json
from pathlib import Path
from typing import Any, Dict, Union

import yaml
from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

schema_path = Path(__file__).resolve().parents[3] / "src" / "schema"


def load_schema(schema_path: Union[str, Path]) -> Union[Dict[str, Any], str]:
    """Load a schema from a file or directory"""
    if Path(schema_path).is_dir():
        return {f.stem: load_schema(f) for f in Path(schema_path).iterdir()}
    elif Path(schema_path).is_file() and (
        str(schema_path).endswith(".yaml") or str(schema_path).endswith(".yml")
    ):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)
    else:
        with open(schema_path, "r") as f:
            return f.read()


def dereference_schema(schema: dict):
    """Dereference a schema by replacing $ref with the actual schema it points to"""

    def _dereference_obj(obj):
        if isinstance(obj, dict):
            out = dict()
            for k, v in obj.items():
                if k == "$ref":
                    address = v.split(".")
                    here = schema
                    for part in address:
                        here = here[part]
                    if isinstance(here, dict):
                        out.update(_dereference_obj(here))
                    else:
                        return _dereference_obj(here)
                else:
                    out[k] = _dereference_obj(v)
            return out
        if isinstance(obj, list):
            return [_dereference_obj(x) for x in obj]
        return obj

    return _dereference_obj(schema)


def validate_schema(schema: dict):
    schema = dereference_schema(schema)
    with open("metaschema.json", "r") as f:
        metaschema = json.load(f)

    # validate is put in this try/except clause because the error is sometimes too long to
    # print in the terminal
    try:
        validate(instance=schema, schema=metaschema)
    except ValidationError as e:
        with open("error_log.txt", "w") as file:
            file.write(str(e))
            raise e


def main():
    schema = load_schema(schema_path)
    validate_schema(schema)


if __name__ == "__main__":
    main()
