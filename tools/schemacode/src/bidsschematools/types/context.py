"""Loader for dynamically-generated context.

This module is accessed when the package is installed in editable mode.
This source code should not be found in the installed package.
"""

from ..schema import load_schema
from ._generator import generate_module

schema = load_schema()
exec(generate_module(schema, "dataclasses"), globals())
