import logging
import os

import click

from .schema import export_schema, load_schema
from .validator import validate_bids


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
@click.argument("in_paths", nargs=-1, required=True)
@click.option("--schema")
@click.option("--report", is_flag=False, flag_value=True, default=False)
@click.pass_context
def validate(
    ctx,
    schema,
    in_paths,
    report,
):
    """Validate BIDS Schema"""
    logger = logging.getLogger("bidsschematools")
    validation_result = validate_bids(
        in_paths,
        schema_path=schema,
        report_path=report,
    )
    logger.debug("Printing out path_tracking in validation_result dictionary")
    if validation_result["path_tracking"]:
        print(validation_result["path_tracking"])

    sys.exit(bool(validation_result["path_tracking"]))


if __name__ == "__main__":
    cli()
