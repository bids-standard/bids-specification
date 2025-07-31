"""A Python package for working with the BIDS schema.

.. autodata:: __version__
.. autodata:: __bids_version__
"""

__version__: str
__bids_version__: str

__all__ = ("__version__", "__bids_version__")


def __getattr__(attr: str) -> str:
    """Lazily load the schema version and BIDS version from the filesystem."""
    from typing import TypeVar

    from .data import load

    T = TypeVar("T")

    def document(obj: T, docstring: str) -> T:
        tp = type(obj)
        return type(tp.__name__, (tp,), {"__doc__": docstring})(obj)

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
