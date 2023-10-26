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
@click.option("--dummy_paths", is_flag=True)
@click.option("--bids_reference_root")
@click.option("--schema_path")
@click.option("--bids_version")
@click.option("--report_path", is_flag=True)
@click.option("--suppress_errors", is_flag=True)
@click.option("accept_non_bids_dir", is_flag=True)
@click.pass_context
def validate(
    ctx,
    schema,
    in_paths,
    dummy_paths,
    bids_reference_root,
    schema_path,
    bids_version,
    report_path,
    suppress_errors,
    accept_non_bids_dir,
):
    """Validate BIDS Schema"""
    logger = logging.getLogger("bidsschematools")
    if schema:
        schema_path = schema
    validation_result = validate_bids(
        in_paths,
        dummy_paths,
        bids_reference_root,
        schema_path,
        bids_version,
        report_path,
        suppress_errors,
        accept_non_bids_dir,
    )
    logger.debug("Printing out path_tracking in validation_result dictionary")
    if validation_result["path_tracking"]:
        print(validation_result["path_tracking"])

    # print validation_result["path_tracking"] if not empty
    # return 0 = success, non-zero = fail use Click exception handling


if __name__ == "__main__":
    cli()
