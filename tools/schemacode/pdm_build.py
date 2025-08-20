import sys

sys.path.insert(0, "src")

import bidsschematools.schema
from bidsschematools.types._generator import generate_module


def pdm_build_initialize(context):
    context.ensure_build_dir()

    # Retrieve package version from schema
    schema = bidsschematools.schema.load_schema()
    context.config.metadata["version"] = schema.schema_version

    if context.target == "editable":
        return

    # src/ layout makes sdists different from wheels
    base_dir = context.build_dir / ("src" if context.target == "sdist" else "")

    # Write compiled schema to JSON
    schema_json = base_dir / "bidsschematools/data/schema.json"
    schema_json.parent.mkdir(parents=True, exist_ok=True)
    schema_json.write_text(schema.to_json())

    # Write generated code for types
    # Limit to wheel to avoid duplication while allowing building
    # the wheel directly from source
    if context.target == "wheel":
        context_py = base_dir / "bidsschematools/types/context.py"
        context_py.parent.mkdir(parents=True, exist_ok=True)
        context_py.write_text(generate_module(schema, "dataclasses"))

        protocols_py = base_dir / "bidsschematools/types/protocols.py"
        protocols_py.parent.mkdir(parents=True, exist_ok=True)
        protocols_py.write_text(generate_module(schema, "protocol"))


def pdm_build_update_files(context, files):
    # Dereference symlinks
    files.update({relpath: path.resolve() for relpath, path in files.items()})
    # Remove code generator, which is not used once installed
    if context.target == "wheel":
        del files["bidsschematools/types/_generator.py"]
