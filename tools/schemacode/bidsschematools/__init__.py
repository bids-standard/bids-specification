"""A Python package for working with the BIDS schema."""
from . import _lazy

try:
    from importlib.resources import as_file, files
except ImportError:  # PY<3.9
    from importlib_resources import as_file, files

version_file = files("bidsschematools.data") / "schema" / "SCHEMA_VERSION"
with as_file(version_file) as f:
    __version__ = f.read_text().strip()

bids_version_file = files("bidsschematools.data") / "schema" / "BIDS_VERSION"
with as_file(bids_version_file) as f:
    __bids_version__ = f.read_text().strip()

subpackages = [
    "render",
    "schema",
    "types",
    "utils",
    "validator",
]
__getattr__, __dir__, _ = _lazy.attach(__name__, subpackages)
