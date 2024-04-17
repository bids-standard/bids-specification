import json
from pathlib import Path

from jsonschema.exceptions import ValidationError
from jsonschema.validators import validate


metaschema_path = Path("src") / "metaschema.json"


def validate_schema(schema):
    with open(metaschema_path, "r") as f:
        metaschema = json.load(f)

    # validate is put in this try/except clause because the error is sometimes too long to
    # print in the terminal
    try:
        validate(instance=schema.to_dict(), schema=metaschema)
    except ValidationError as e:
        with open("error_log.txt", "w") as file:
            file.write(str(e))
            raise e
