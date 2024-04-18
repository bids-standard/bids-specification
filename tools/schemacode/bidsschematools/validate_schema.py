import json
from importlib.resources import files

from jsonschema import ValidationError, validate


def validate_schema(schema):
    metaschema = json.loads(files("bidsschematools.data").joinpath("metaschema.json").read_text())

    # validate is put in this try/except clause because the error is sometimes too long to
    # print in the terminal
    try:
        validate(instance=schema.to_dict(), schema=metaschema)
    except ValidationError as e:
        with open("error_log.txt", "w") as file:
            file.write(str(e))
            raise e
