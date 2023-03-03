import argparse
import logging

import argh

from .schema import export
from .validator import validate_bids


def cli():
    parser = argparse.ArgumentParser(
        description="BIDS Schema Tools Interface",
        formatter_class=argparse.RawTextHelpFormatter,
        # add_help=False,
    )
    parser.add_argument("-v", "--verbose", default=0, type=int)
    validate_bids.__name__ = "validate"
    argh.add_commands(parser, [export, validate_bids])
    args = parser.parse_args()
    logging.getLogger("bidsschematools").setLevel(logging.INFO - args.verbose * 10)
    argh.dispatch(parser)
