"""A Python package for working with the BIDS schema.

.. autodata:: __version__
.. autodata:: __bids_version__
"""

try:  # Prefer backport to leave consistency to dependency spec
    from importlib_resources import files
except ImportError:
    from importlib.resources import files  # type: ignore

version_file = files("bidsschematools.data") / "schema" / "SCHEMA_VERSION"
__version__ = version_file.read_text().strip()
"Schema version"

bids_version_file = files("bidsschematools.data") / "schema" / "BIDS_VERSION"
__bids_version__ = bids_version_file.read_text().strip()
"BIDS specification version"
