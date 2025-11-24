"""Typing symbols for the bidsschematools package.

This module aims to make the types used by the bidsschematools package available for
type checking without requiring the original packages to be imported at runtime.

The expected usage is::

    from __future__ import annotations

    import bidsschematools._lazytypes as lt

    def func(arg: lt.Any) -> ReturnType:
        ...


If used outside of type annotations, for example, in an ``isinstance()`` check,
the attribute will trigger an import.
"""

import sys

__all__ = (
    "Any",
    "TYPE_CHECKING",
    "Self",
    "TypeVar",
)

RUNTIME_IMPORT: bool

TYPE_CHECKING = False
if TYPE_CHECKING or "sphinx.ext.autodoc" in sys.modules:  # pragma: no cover
    from typing import Any, Self, TypeVar

    # Helpful TypeVars for generic classes and functions.
    # These should never be accessed at runtime, only for type checking, so exclude from __all__.
    T = TypeVar("T")
    T_co = TypeVar("T_co", covariant=True)
    T_contra = TypeVar("T_contra", contravariant=True)
else:  # pragma: no cover

    def __getattr__(name: str):
        # Set the BIDSSCHEMATOOLS_DISABLE_RUNTIME_TYPES environment variable to
        # crash out if attributes are ever accessed at runtime.
        # Currently, we do not use this feature.
        global RUNTIME_IMPORT
        if name == "RUNTIME_IMPORT":
            import os

            RUNTIME_IMPORT = not os.getenv("BIDSSCHEMATOOLS_DISABLE_RUNTIME_TYPES", "")
            return RUNTIME_IMPORT

        if not RUNTIME_IMPORT:
            raise RuntimeError(
                f"Attribute {name!r} in module {__name__!r} should only be used for type checking."
            )

        if name in __all__:
            import typing

            globals()[name] = getattr(typing, name)
            return globals()[name]

        msg = f"Module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)
