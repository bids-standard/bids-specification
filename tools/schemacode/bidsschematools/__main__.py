import logging
import os
import re
import sys
from itertools import chain

import click

from .rules import regexify_filename_rules
from .schema import export_schema, load_schema
from .validator import _bidsignore_check


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
def cli(verbose, quiet):
    """BIDS Schema Tools"""
    verbose = verbose - quiet
    logging.getLogger("bidsschematools").setLevel(logging.WARNING - verbose * 10)


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


@cli.command("pre-receive-hook")
@click.option("--schema", "-s", type=click.Path(), help="Path to the BIDS schema")
@click.option(
    "--input", "-i", "input_", default="-", type=click.Path(), help="Input file (default: stdin)"
)
@click.option(
    "--output",
    "-o",
    "output",
    default="-",
    type=click.Path(),
    help="Output file (default: stdout)",
)
def pre_receive_hook(schema, input_, output):
    """Validate filenames from a list of files against the BIDS schema

    The input should be a list of ignore patterns followed by a line containing
    "0001" and then a list of filenames. The output will be a list of filenames
    that do not match the schema.

    This is intended to be used in a git pre-receive hook.
    """
    # Slurp inputs for now; we can think about streaming later
    if input_ == "-":
        lines = sys.stdin.readlines()
    else:
        with open(input_) as fobj:
            lines = fobj.readlines()

    split = lines.index("0001\n")
    ignore = [line.rstrip() for line in lines[:split]]
    filenames = [line.rstrip() for line in lines[split + 1 :]]

    schema = load_schema(schema)
    all_rules = chain.from_iterable(
        regexify_filename_rules(group, schema, level=2)
        for group in (schema.rules.files.common, schema.rules.files.raw)
    )
    regexes = [rule["regex"] for rule in all_rules]
    # XXX Hack for phenotype files - this can be removed once we
    # have a schema definition for them
    regexes.append(r"phenotype/.*\.tsv")

    output = sys.stdout if output == "-" else open(output, "w")

    rc = 0
    with output:
        for filename in filenames:
            if any(_bidsignore_check(pattern, filename, "") for pattern in ignore):
                continue
            if not any(re.match(regex, filename) for regex in regexes):
                output.write(f"{filename}\n")
                rc = 1

    sys.exit(rc)


if __name__ == "__main__":
    cli()
