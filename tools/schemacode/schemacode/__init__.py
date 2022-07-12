"""A Python package for working with the BIDS schema."""
from . import render, schema, utils

from importlib import resources as ilr

__all__ = [
    "render",
    "schema",
    "utils",
]

version_file = ilr.files("schemacode.data") / "schema" / "SCHEMA_VERSION"
with ilr.as_file(version_file) as path:
    __version__ = path.read_text().strip()
