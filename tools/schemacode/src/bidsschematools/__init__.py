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
        "__version__": ("schema/SCHEMA_VERSION", "Schema version"),
        "__bids_version__": ("schema/BIDS_VERSION", "BIDS specification version"),
    }

    if attr in versions:
        resource, docstring = versions[attr]
        globals()[attr] = document(load.readable(resource).read_text().strip(), docstring)
        return globals()[attr]

    raise AttributeError(f"module {__spec__.name!r} has no attribute {attr!r}")
