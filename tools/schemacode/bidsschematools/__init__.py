"""A Python package for working with the BIDS schema."""
from . import render, schema, utils

try:
    from importlib.resources import as_file, files
except ImportError:  # PY<3.9
    from importlib_resources import as_file, files

__all__ = [
    "render",
    "schema",
    "utils",
]

version_file = files("bidsschematools.data") / "schema" / "SCHEMA_VERSION"
with as_file(version_file) as path:
    __version__ = path.read_text().strip()

bids_version_file = files("bidsschematools.data") / "schema" / "BIDS_VERSION"
with as_file(bids_version_file) as path:
    __bids_version__ = path.read_text().strip()
