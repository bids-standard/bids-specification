import json
import logging
import os
import re
import sys
from itertools import chain
from pathlib import Path

import click

from .rules import regexify_filename_rules
from .schema import load_schema
from .utils import configure_logger, get_logger
from .validator import _bidsignore_check

lgr = get_logger()


@click.group()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
def cli(verbose, quiet):
    """BIDS Schema Tools"""
    verbose = verbose - quiet
    configure_logger(get_logger(level=logging.WARNING - verbose * 10))


@cli.command()
@click.option("--schema")
@click.option("--output", default="-")
@click.pass_context
def export(ctx, schema, output):
    """Export BIDS schema to JSON document"""
    schema = load_schema(schema)
    text = schema.to_json()
    if output == "-":
        lgr.debug("Writing to stdout")
        print(text)
    else:
        output = os.path.abspath(output)
        lgr.debug(f"Writing to {output}")
        with open(output, "w") as fobj:
            fobj.write(text)


@cli.command()
@click.option("--output", default="-")
@click.pass_context
def export_metaschema(ctx, output):
    """Export BIDS schema to JSON document"""
    from .data import load

    metaschema = load.readable("metaschema.json").read_text()
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
            lgr.critical("Protocol error: invalid JSON in description")
            lgr.critical("Dataset description must be one JSON object, written to a single line")
            lgr.critical("Received: %s", description_str)
            stream.close()
            sys.exit(2)
    else:
        # Legacy: ignore patterns, followed by "0001", followed by filenames
        stream = chain([first_line], stream)
        description = {}

    dataset_type = description.get("DatasetType", "raw")
    lgr.info("Dataset type: %s", dataset_type)

    ignore = []
    for line in stream:
        if line == "0001\n":
            break
        ignore.append(line.strip())
    lgr.info("Ignore patterns found: %d", len(ignore))

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

    output = sys.stdout if output == "-" else open(output, "w")

    rc = 0
    any_files = False
    valid_files = 0
    with output:
        for filename in stream:
            if not any_files:
                lgr.debug("Validating files, first file: %s", filename)
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
        lgr.error("No files to validate")
        rc = 2

    stream.close()
    sys.exit(rc)


@cli.group()
def migrate():
    """Migrate BIDS datasets to adopt standardized conventions"""
    pass


def _validate_bids_dataset(dataset_path: Path) -> None:
    """Validate that a path contains a BIDS dataset.

    Parameters
    ----------
    dataset_path : Path
        Path to check for BIDS dataset

    Raises
    ------
    SystemExit
        If dataset_description.json is not found
    """
    if not (dataset_path / "dataset_description.json").exists():
        lgr.error(
            f"No dataset_description.json found in {dataset_path}. "
            "Is this a valid BIDS dataset?"
        )
        sys.exit(1)


@migrate.command("list")
def migrate_list():
    """List all available migrations"""
    from .migrate import registry
    from . import migrations  # noqa: F401 - Import to register migrations
    
    migrations_list = registry.list_migrations()
    
    if not migrations_list:
        lgr.info("No migrations available")
        return
    
    click.echo("Available migrations:\n")
    for mig in sorted(migrations_list, key=lambda x: x["version"]):
        click.echo(f"  {mig['name']} (version {mig['version']})")
        click.echo(f"    {mig['description']}\n")


@migrate.command("run")
@click.argument("migration_name")
@click.argument("dataset_path", type=click.Path(exists=True))
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be changed without modifying files",
)
def migrate_run(migration_name, dataset_path, dry_run):
    """Run a specific migration on a BIDS dataset

    MIGRATION_NAME is the name of the migration to run (use 'migrate list' to see available)

    DATASET_PATH is the path to the BIDS dataset root directory
    """
    from .migrate import registry
    from . import migrations  # noqa: F401 - Import to register migrations

    dataset_path = Path(dataset_path).resolve()
    _validate_bids_dataset(dataset_path)
    
    try:
        result = registry.run(migration_name, dataset_path, dry_run=dry_run)
    except ValueError as e:
        lgr.error(str(e))
        lgr.info("Use 'bst migrate list' to see available migrations")
        sys.exit(1)
    
    # Display results
    if result.get("modified_files"):
        click.echo(f"\nModified files ({len(result['modified_files'])}):")
        for filepath in result["modified_files"]:
            click.echo(f"  - {filepath}")
    
    if result.get("warnings"):
        click.echo(f"\nWarnings ({len(result['warnings'])}):")
        for warning in result["warnings"]:
            click.echo(f"  - {warning}")
    
    if result.get("suggestions"):
        click.echo(f"\nSuggestions ({len(result['suggestions'])}):")
        for suggestion in result["suggestions"]:
            click.echo(f"  - {suggestion}")
    
    click.echo(f"\n{result['message']}")
    
    if not result["success"]:
        sys.exit(1)


@migrate.command("all")
@click.argument("dataset_path", type=click.Path(exists=True))
@click.option(
    "--dry-run",
    is_flag=True,
    help="Show what would be changed without modifying files",
)
@click.option(
    "--skip",
    multiple=True,
    help="Skip specific migrations (can be used multiple times)",
)
def migrate_all(dataset_path, dry_run, skip):
    """Run all available migrations on a BIDS dataset

    DATASET_PATH is the path to the BIDS dataset root directory
    """
    from .migrate import registry
    from . import migrations  # noqa: F401 - Import to register migrations

    dataset_path = Path(dataset_path).resolve()
    _validate_bids_dataset(dataset_path)
    
    migrations_list = registry.list_migrations()
    skip_set = set(skip)
    
    if not migrations_list:
        click.echo("No migrations available")
        return
    
    click.echo(f"Running {len(migrations_list)} migration(s) on {dataset_path}")
    if dry_run:
        click.echo("DRY RUN: No files will be modified\n")
    
    results = []
    for mig in sorted(migrations_list, key=lambda x: x["version"]):
        if mig["name"] in skip_set:
            click.echo(f"Skipping: {mig['name']}")
            continue
        
        click.echo(f"\nRunning: {mig['name']} (version {mig['version']})")
        result = registry.run(mig["name"], dataset_path, dry_run=dry_run)
        results.append((mig["name"], result))
        
        if result.get("modified_files"):
            click.echo(f"  Modified {len(result['modified_files'])} file(s)")
        if result.get("warnings"):
            click.echo(f"  {len(result['warnings'])} warning(s)")
        if result.get("suggestions"):
            click.echo(f"  {len(result['suggestions'])} suggestion(s)")
        click.echo(f"  {result['message']}")
    
    # Summary
    click.echo("\n" + "=" * 60)
    click.echo("Migration Summary:")
    click.echo("=" * 60)
    
    for name, result in results:
        status = "✓" if result["success"] else "✗"
        click.echo(f"{status} {name}: {result['message']}")


if __name__ == "__main__":
    cli()
