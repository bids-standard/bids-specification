import argparse
import logging

from argh import add_commands, dispatch  # type: ignore

from .schema import export
from .validator import validate_bids


def cli():
    parser = argparse.ArgumentParser(
        description="BIDS Schema Tools Interface",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--verbose", "-v", action="count", default=0)
    validate_bids.__name__ = "validate"
    add_commands(parser, [export, validate_bids])
    args = parser.parse_args()
    logging.getLogger("bidsschematools").setLevel(logging.WARNING - args.verbose * 10)
    dispatch(parser)
