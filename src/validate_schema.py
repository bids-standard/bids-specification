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


schema = load_schema(schema_path)

with open("metaschema.json", "r") as f:
    metaschema = json.load(f)

try:
    validate(instance=schema, schema=metaschema)
except ValidationError as e:
    with open("error_log.txt", "w") as file:
        file.write(str(e))
        raise e
