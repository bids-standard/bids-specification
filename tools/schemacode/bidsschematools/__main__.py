import argparse

import argh

from .schema import export
from .validator import validate_bids


def cli():
    parser = argparse.ArgumentParser(
        description="BIDS Schema Tools Interface",
        formatter_class=argparse.RawTextHelpFormatter,
        # add_help=False,
    )
    validate_bids.__name__ = "validate"
    argh.add_commands(parser, [export, validate_bids])
    argh.dispatch(parser)
