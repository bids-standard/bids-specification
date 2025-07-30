import sys

sys.path.insert(0, "src")

import bidsschematools.schema


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


def pdm_build_update_files(context, files):
    # Dereference symlinks
    files.update({relpath: path.resolve() for relpath, path in files.items()})
