"""A Python package for working with the BIDS schema."""
from . import render, schema, utils

__all__ = [
    "render",
    "schema",
    "utils",
]

from . import _version

__version__ = _version.get_versions()["version"]
