"""A Python package for working with the BIDS schema.

.. autodata:: __version__
.. autodata:: __bids_version__
"""

global __version__
global __bids_version__

__all__ = ("__version__", "__bids_version__")


def __getattr__(attr):
    from .data import load_resource

    if attr == "__version__":
        global __version__
        __version__ = load_resource("schema/SCHEMA_VERSION").read_text().strip()
        __version__.__doc__ = "Schema version"
        return __version__
    elif attr == "__bids_version__":
        global __bids_version__
        __bids_version__ = load_resource("schema/BIDS_VERSION").read_text().strip()
        __bids_version__.__doc__ = "BIDS specification version"
        return __bids_version__

    raise AttributeError(f"module {__spec__.name!r} has no attribute {attr!r}")
