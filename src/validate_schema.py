import json
from pathlib import Path
from typing import Any, Dict, Union

import yaml

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate

schema_path = Path(__file__).resolve().parent.parent / "src" / "schema"


def load_schema(schema_path: Union[str, Path]) -> Union[Dict[str, Any], str]:
    if Path(schema_path).is_dir():
        return {f.stem: load_schema(f) for f in Path(schema_path).iterdir()}
    elif Path(schema_path).is_file() and (str(schema_path).endswith(".yaml") or str(schema_path).endswith(".yml")):
        with open(schema_path, "r") as f:
            return yaml.safe_load(f)
    else:
        with open(schema_path, "r") as f:
            return f.read()


def derefence_schema(obj):
    if isinstance(obj, dict):
        out = dict()
        for k, v in obj.items():
            if k == "$ref":
                #print(v)
                address = v.split(".")
                here = schema
                for part in address:
                    here = here[part]
                if isinstance(here, dict):
                    out.update(derefence_schema(here))
                else:
                    return derefence_schema(here)
            else:
                out[k] = derefence_schema(v)
        return out
    if isinstance(obj, list):
        return [derefence_schema(x) for x in obj]
    return obj


schema = load_schema(schema_path)
schema = derefence_schema(schema)

with open("metaschema.json", "r") as f:
    metaschema = json.load(f)

try:
    validate(instance=schema, schema=metaschema)
except ValidationError as e:
    with open("error_log.txt", "w") as file:
        file.write(str(e))
        raise e
