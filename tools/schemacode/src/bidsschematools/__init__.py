"""A Python package for working with the BIDS schema.

.. autodata:: __version__
.. autodata:: __bids_version__
"""

__version__: str
__bids_version__: str

__all__ = ("__version__", "__bids_version__")


def __getattr__(attr: str) -> str:
    if attr in __all__:
        from . import _version

        globals()[attr] = getattr(_version, attr)
        return globals()[attr]

    raise AttributeError(f"module {__spec__.name!r} has no attribute {attr!r}")
