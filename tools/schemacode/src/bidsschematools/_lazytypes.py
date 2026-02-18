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
    # typing
    "Any",
    "Callable",
    "Literal",
    "NotRequired",
    "Protocol",
    "Self",
    "TYPE_CHECKING",
    "TypeVar",
    "TypedDict",
    # collections.abc
    "Iterator",
    "Mapping",
    # contextlib
    "AbstractContextManager",
    # third-party
    "FormatChecker",
    "JsonschemaValidator",
    "Traversable",
)

_type_map = {
    "AbstractContextManager": ("contextlib", "AbstractContextManager"),
    "Iterator": ("collections.abc", "Iterator"),
    "Mapping": ("collections.abc", "Mapping"),
    "Traversable": ("acres.typ", "Traversable"),
    "FormatChecker": ("jsonschema", "FormatChecker"),
    "JsonschemaValidator": ("jsonschema.protocols", "JsonschemaValidator"),
}

RUNTIME_IMPORT: bool

TYPE_CHECKING = False
if TYPE_CHECKING or "sphinx.ext.autodoc" in sys.modules:  # pragma: no cover
    from collections.abc import Callable, Iterator, Mapping
    from contextlib import AbstractContextManager
    from typing import Any, Literal, Protocol, TypedDict, TypeVar

    # Missing imports in 3.10. Avoid breaking third-party autodoc generation.
    try:
        from typing import NotRequired, Self
    except ImportError:  # PY310
        NotRequired = tuple  # type: ignore[misc,assignment]
        Self = object  # type: ignore[misc,assignment]

    from acres.typ import Traversable

    # Optional dependency, avoid breaking third-party autodoc generation.
    try:
        from jsonschema import FormatChecker
        from jsonschema.protocols import Validator as JsonschemaValidator
    except ImportError:
        FormatChecker = object  # type: ignore[misc,assignment]
        JsonschemaValidator = object  # type: ignore[misc,assignment]

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
        try:
            throw = not RUNTIME_IMPORT
        except NameError:
            import os

            RUNTIME_IMPORT = not os.getenv("BIDSSCHEMATOOLS_DISABLE_RUNTIME_TYPES", "")
            if name == "RUNTIME_IMPORT":
                return RUNTIME_IMPORT
            throw = not RUNTIME_IMPORT

        if throw:
            raise AttributeError(
                f"Attribute {name!r} in module {__name__!r} should only be used for type checking."
            )

        if name in __all__:
            if name in _type_map:
                mod, attr = _type_map[name]
            else:
                mod, attr = "typing", name
            globals()[name] = getattr(__import__(mod), attr)
            return globals()[name]

        msg = f"Module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)
