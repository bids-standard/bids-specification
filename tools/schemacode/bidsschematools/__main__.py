import logging
import os

from clize import run

from .schema import export
from .validator import validate_bids


def cli():
    run({
        'validate': validate_bids,
        'export': export,
        })

if __name__ == "__main__":
    cli()
