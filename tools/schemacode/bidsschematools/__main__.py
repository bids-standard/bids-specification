import logging
import os
import sys

import click

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files


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


@cli.command()
@click.option("--output", default="-")
@click.pass_context
def export_metaschema(ctx, output):
    """Export BIDS schema to JSON document"""
    metaschema = files("bidsschematools.data").joinpath("metaschema.json").read_text()
    if output == "-":
        print(metaschema, end="")
    else:
        output = os.path.abspath(output)
        with open(output, "w") as fobj:
            fobj.write(metaschema)


if __name__ == "__main__":
    cli()
