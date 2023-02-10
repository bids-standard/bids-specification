import argh

from .schema import export
from .validator import validate_bids


def cli():
    validate_bids.__name__ = "validate"
    argh.dispatch_commands([export, validate_bids])
