import json
import logging
import os
import re
import sys
from itertools import chain

import click

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files

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

    The expected input takes the following form:

    ```
    bids-hook-v2
    {"Name": "My dataset", "BIDSVersion": "1.9.0", "DatasetType": "raw"}
    ignore-pattern1
    ...
    ignore-patternN
    0001
    .datalad/config
    .gitattributes
    CHANGES
    README
    dataset_description.json
    participants.tsv
    sub-01/anat/sub-01_T1w.nii.gz
    ...
    ```

    The header identifies the protocol version. For protocol ``bids-hook-v2``,
    the second line MUST be the dataset_description.json file, with any newlines removed.
    The following lines, up to the line containing "0001", are ignore patterns
    from the .bidsignore file. The lines following "0001" are the filenames to
    be validated.

    This is intended to be used in a git pre-receive hook.
    """
    logger = logging.getLogger("bidsschematools")
    schema = load_schema(schema)

    # Slurp inputs for now; we can think about streaming later
    if input_ == "-":
        stream = sys.stdin
    else:
        stream = open(input_)

    first_line = next(stream)
    if first_line == "bids-hook-v2\n":
        # V2 format: header line, description JSON, followed by legacy format
        description_str = next(stream)
        fail = False
        try:
            description: dict = json.loads(description_str)
        except json.JSONDecodeError:
            fail = True
        if fail or not isinstance(description, dict):
            logger.critical("Protocol error: invalid JSON in description")
            logger.critical(
                "Dataset description must be one JSON object, written to a single line"
            )
            logger.critical("Received: %s", description_str)
            stream.close()
            sys.exit(2)
    else:
        # Legacy: ignore patterns, followed by "0001", followed by filenames
        stream = chain([first_line], stream)
        description = {}

    dataset_type = description.get("DatasetType", "raw")
    logger.info("Dataset type: %s", dataset_type)

    ignore = []
    for line in stream:
        if line == "0001\n":
            break
        ignore.append(line.strip())
    logger.info("Ignore patterns found: %d", len(ignore))

    all_rules = chain.from_iterable(
        regexify_filename_rules(group, schema, level=2)
        for group in (schema.rules.files.common, schema.rules.files.raw)
    )
    if dataset_type == "derivative":
        all_rules = chain(
            all_rules,
            regexify_filename_rules(schema.rules.files.derivatives, schema, level=2),
        )

    regexes = [rule["regex"] for rule in all_rules]
    # XXX Hack for phenotype files - this can be removed once we
    # have a schema definition for them
    regexes.append(r"phenotype/.*\.(tsv|json)")

    output = sys.stdout if output == "-" else open(output, "w")

    rc = 0
    any_files = False
    valid_files = 0
    with output:
        for filename in stream:
            if not any_files:
                logger.debug("Validating files, first file: %s", filename)
                any_files = True
            filename = filename.strip()
            if filename.startswith(".") or any(
                _bidsignore_check(pattern, filename, "") for pattern in ignore
            ):
                continue
            if not any(re.match(regex, filename) for regex in regexes):
                print(filename, file=output)
                rc = 1
            else:
                valid_files += 1

    if valid_files == 0:
        logger.error("No files to validate")
        rc = 2

    stream.close()
    sys.exit(rc)


if __name__ == "__main__":
    cli()
