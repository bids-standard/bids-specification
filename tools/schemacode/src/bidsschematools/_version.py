"""Lazy version strings

.. autodata:: __version__
.. autodata:: __bids_version__
"""

from __future__ import annotations

from . import _lazytypes as lt

__version__: str
__bids_version__: str

__all__ = ("__version__", "__bids_version__")


def document(obj: lt.T, docstring: str) -> lt.T:
    tp = type(obj)
    return type(tp.__name__, (tp,), {"__doc__": docstring})(obj)


def __getattr__(attr: str) -> str:
    """Lazily load the schema version and BIDS version from the filesystem."""
    from .data import load

    versions = {
        "__version__": (
            "schema/SCHEMA_VERSION",
            "schema_version",
            "Schema version",
        ),
        "__bids_version__": (
            "schema/BIDS_VERSION",
            "bids_version",
            "BIDS specification version",
        ),
    }

    if attr in versions:
        dir_path, schema_path, docstring = versions[attr]

        # Fast path if the schema directory is present (editable mode)
        if (version_file := load.readable(dir_path)).is_file():
            version = version_file.read_text().strip()
        else:
            # If version files are absent, the schema.json has been packaged.
            # If we're going to read it, we might as well cache it with load_schema().
            from .schema import load_schema

            version = load_schema()[schema_path]
        globals()[attr] = document(version, docstring)
        return globals()[attr]

    raise AttributeError(f"module {__spec__.name!r} has no attribute {attr!r}")
