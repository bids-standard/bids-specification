import logging
import os

import click

from .migrations import migrate_dataset as migrate_dataset_
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
@click.argument("dataset_paths", type=click.Path(dir_okay=True, file_okay=False), nargs=-1)
@click.pass_context
def migrate_datasets(ctx, dataset_paths):
    """Migrate BIDS 1.x dataset to BIDS 2.0

    Example of running in bids-examples to apply to all and review the diff

    \b
    git clean -dfx && git reset --hard \\
      && { /bin/ls */dataset_description.json | sed -e 's,/.*,,g' | xargs bst migrate-datasets } \\
      && git add . && git diff --cached
    """
    for dataset_path in dataset_paths:
        migrate_dataset_(dataset_path)


if __name__ == "__main__":
    cli()
