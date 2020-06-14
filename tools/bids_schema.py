#!/usr/bin/env python3
#
# pip install click click-didyoumean tabulate

from itertools import chain
import logging
import os
from pathlib import Path
import yaml
import sys
from warnings import warn

import pandas as pd
#
import click
from click_didyoumean import DYMGroup
# from yamlinclude import YamlIncludeConstructor

# helper to debug
from pprint import pprint

#
# Aux utilities
#


def is_interactive():
    """Return True if all in/outs are tty"""
    # TODO: check on windows if hasattr check would work correctly and add value:
    #
    return sys.stdin.isatty() and sys.stdout.isatty() and sys.stderr.isatty()


def setup_exceptionhook(ipython=False):
    """Overloads default sys.excepthook with our exceptionhook handler.

       If interactive, our exceptionhook handler will invoke
       pdb.post_mortem; if not interactive, then invokes default handler.
    """

    def _pdb_excepthook(type, value, tb):
        import traceback

        traceback.print_exception(type, value, tb)
        print()
        if is_interactive():
            import pdb

            pdb.post_mortem(tb)

    if ipython:
        from IPython.core import ultratb

        sys.excepthook = ultratb.FormattedTB(
            mode="Verbose",
            # color_scheme='Linux',
            call_pdb=is_interactive(),
        )
    else:
        sys.excepthook = _pdb_excepthook


def get_logger(name=None):
    """Return a logger to use
    """
    return logging.getLogger("bids-schema" + (".%s" % name if name else ""))


def set_logger_level(lgr, level):
    if isinstance(level, int):
        pass
    elif level.isnumeric():
        level = int(level)
    elif level.isalpha():
        level = getattr(logging, level)
    else:
        lgr.warning("Do not know how to treat loglevel %s" % level)
        return
    lgr.setLevel(level)


_DEFAULT_LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

lgr = get_logger()
# Basic settings for output, for now just basic
set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
FORMAT = "%(asctime)-15s [%(levelname)8s] %(message)s"
logging.basicConfig(format=FORMAT)

#
# Constants and defaults
#
BIDS_SCHEMA = Path(__file__).parent.parent / "src" / "schema"

#
# Main group
#


def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    click.echo(__version__)
    ctx.exit()


def upper(ctx, param, value):
    import pdb

    pdb.set_trace()
    return value.upper()

#
# Common options to reuse
#
# Functions to provide customizations where needed
def _updated_option(*args, **kwargs):
    args, d = args[:-1], args[-1]
    kwargs.update(d)
    return click.option(*args, **kwargs)


def schema_path_option():
    return click.option(
        "--schema-path",
        type=click.Path(exists=True, dir_okay=True),
        default=str(BIDS_SCHEMA),
        help="Path to the directory with the schema")


# group to provide commands
@click.group(cls=DYMGroup)
@click.option(
    "--version", is_flag=True, callback=print_version, expose_value=False, is_eager=True
)
@click.option(
    "-l",
    "--log-level",
    help="Log level name",
    # TODO: may be bring also handling of  int  values.  For now -- no need
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]),
    default="INFO",
    # callback=upper,  # TODO: not in effect! seems to come to play only after type validation
    show_default=True,
)
@click.option("--pdb", help="Fall into pdb if errors out", is_flag=True)
def main(log_level, pdb=False):
    """A client to support BIDS schema manipulations.
    """
    set_logger_level(get_logger(), log_level)
    if pdb:
        #map_to_click_exceptions._do_map = False
        setup_exceptionhook()


def _get_entry_name(path):
    if path.suffix == '.yaml':
        return path.name[:-5]  # no .yaml
    else:
        return path.name


def load_schema(schema_path):
    """The schema loader

    It allows for schema, like BIDS itself, to be specified in
    a hierarchy of directories and files.
    File (having .yaml stripped) and directory names become keys
    in the associative array (dict) of entries composed from content
    of files and entire directories.
    """
    schema_path = Path(schema_path)
    if schema_path.is_file() and (schema_path.suffix == '.yaml'):
        with open(schema_path) as f:
            return yaml.load(f, Loader=yaml.SafeLoader)
    elif schema_path.is_dir():
        # iterate through files and subdirectories
        res = {
            _get_entry_name(path): load_schema(path)
            for path in sorted(schema_path.iterdir())
        }
        return {k: v for k, v in res.items() if v is not None}
    else:
        warn(f"{schema_path} is somehow nothing we can load")


@main.command()
# TODO: may be add "format" and make it also json?
@schema_path_option()
def show(schema_path):
    """Print full schema."""
    schema = load_schema(schema_path)
    print(yaml.safe_dump(schema, default_flow_style=False))


@main.command()
# TODO: output path, for now just print
@schema_path_option()
def entity_table(schema_path, tablefmt="github"):
    """Produce entity table (markdown) based on schema.
    This only works if the top-level schema *directory* is provided.
    """
    from tabulate import tabulate
    schema = load_schema(schema_path)
    # prepare the table based on the schema
    # import pdb; pdb.set_trace()
    header = ['Entity', 'DataType']
    formats = ['Format', 'DataType']
    entity_to_col = {}
    table = [formats]

    # Compose header and formats first
    for i, (entity, spec) in enumerate(schema['entities'].items()):
        header.append(spec["name"])
        formats.append(f'`{entity}-<{spec["format"]}>`')
        entity_to_col[entity] = i + 1

    # Go through data types
    for dtype, specs in chain(schema['datatypes'].items(),
                              schema['auxdatatypes'].items()):
        dtype_rows = {}

        # each dtype could have multiple specs
        for spec in specs:
            # datatypes use suffixes, while
            # for auxdatatypes we need to use datatypes
            # TODO: RF to avoid this guesswork
            suffixes = spec.get('datatypes') or spec.get('suffixes')
            # TODO: <br> is specific for html form
            suffixes_str = ' '.join(suffixes) if suffixes else ''
            dtype_row = [dtype] + ([''] * len(entity_to_col))
            for ent, req in spec.get('entities', []).items():
                dtype_row[entity_to_col[ent]] = req.upper()

            # Merge specs within dtypes if they share all of the same entities
            if dtype_row in dtype_rows.values():
                for k, v in dtype_rows.items():
                    if dtype_row == v:
                        dtype_rows.pop(k)
                        new_k = k + ' ' + suffixes_str
                        new_k = new_k.strip()
                        dtype_rows[new_k] = v
                        break
            else:
                dtype_rows[suffixes_str] = dtype_row

        # Reformat first column
        dtype_rows = {dtype+'<br>({})'.format(k): v for k, v in dtype_rows.items()}
        dtype_rows = [[k] + v for k, v in dtype_rows.items()]
        table += dtype_rows

    # Create multi-level index because first two rows are headers
    cols = list(zip(header, table[0]))
    cols = pd.MultiIndex.from_tuples(cols)
    table = pd.DataFrame(data=table[1:], columns=cols)
    table = table.set_index(('Entity', 'Format'))

    # Now we can split as needed

    # Flatten multi-index
    vals = table.index.tolist()
    table.loc['Format'] = table.columns.get_level_values(1)
    table.columns = table.columns.get_level_values(0)
    table = table.loc[['Format'] + vals]
    table.index.name = 'Entity'

    # print it as markdown
    table = table.drop(columns=['DataType'])
    header.remove('DataType')
    print(tabulate(table, header, tablefmt=tablefmt))
    return table


if __name__ == '__main__':
    main()
