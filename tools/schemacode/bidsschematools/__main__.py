import logging
import os

import click

from .schema import export_schema, load_schema


@click.group()
@click.option("-v", "--verbose", count=True)
def cli(verbose):
    """BIDS Schema Tools"""
    logging.getLogger("bidsschematools").setLevel(logging.INFO - verbose * 10)


@cli.command()
@click.option("--schema")
@click.option("--output", default="-")
@click.pass_context
def export(ctx, schema, output):
    """Export BIDS schema to JSON document"""
    logger = logging.getLogger("bidsschematools")
    schema = load_schema(schema)
    text = export_schema(schema)
    if output == "-":
        logger.debug("Writing to stdout")
        print(text)
    else:
        output = os.path.abspath(output)
        logger.debug(f"Writing to {output}")
        with open(output, "w") as fobj:
            fobj.write(text)


if __name__ == "__main__":
    cli()
