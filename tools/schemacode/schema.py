#!/usr/bin/env python3
import logging
import os
from copy import deepcopy
from pathlib import Path
from warnings import warn

import numpy as np
import pandas as pd
import yaml

from . import utils

lgr = utils.get_logger()
# Basic settings for output, for now just basic
utils.set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
logging.basicConfig(format="%(asctime)-15s [%(levelname)8s] %(message)s")

BIDS_SCHEMA = Path(__file__).parent.parent / "src" / "schema"


def _get_entry_name(path):
    if path.suffix == ".yaml":
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

    Parameters
    ----------
    schema_path : str
        Folder containing yaml files or yaml file.

    Returns
    -------
    dict
        Schema in dictionary form.
    """
    schema_path = Path(schema_path)
    if schema_path.is_file() and (schema_path.suffix == ".yaml"):
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


def filter_schema(schema, **kwargs):
    """A simple filtering function. You can limit the schema to specific
    values."""
    new_schema = deepcopy(schema)
    if isinstance(new_schema, dict):
        # Reduce values in dict to only requested
        for k, v in kwargs.items():
            if k in new_schema.keys():
                temp = deepcopy(new_schema[k])
                if isinstance(temp, dict):
                    temp = {k1: v1 for k1, v1 in temp.items() if k1 in v}
                else:
                    temp = [i for i in temp if i in v]
                new_schema[k] = temp

            for k2, v2 in new_schema.items():
                new_schema[k2] = filter_schema(new_schema[k2], **kwargs)
    elif isinstance(new_schema, list):
        for i, item in enumerate(new_schema):
            if isinstance(item, dict):
                new_schema[i] = filter_schema(item, **kwargs)
    return new_schema


def make_entity_definitions(schema):
    """Save entity definitions to a markdown file.
    Each entity gets its own heading.
    """
    entities = schema["entities"]

    text = ""
    for entity, entity_info in entities.items():
        entity_shorthand = entity_info["entity"]
        text += "\n"
        text += "## {}".format(entity_shorthand)
        text += "\n\n"
        text += "Full name: {}".format(entity_info["name"])
        text += "\n\n"
        text += "Format: `{}-<{}>`".format(entity_info["entity"], entity_info["format"])
        text += "\n\n"
        text += "Definition: {}".format(entity_info["description"])
    return text


def drop_unused_entities(df):
    """Remove columns from a dataframe where all values in the column are NaNs.
    For entity tables, this limits each table to only entities thare are used
    within the modality.
    """
    df = df.replace("", np.nan).dropna(axis=1, how="all").fillna("")
    return df


def flatten_multiindexed_columns(df):
    """Remove multi-indexing of multi-indexed column headers.
    The first layer is the "DataType", while the second layer is the "Format".
    This second layer will become a new row.
    """
    # Flatten multi-index
    vals = df.index.tolist()
    df.loc["Format"] = df.columns.get_level_values(1)
    df.columns = df.columns.get_level_values(0)
    df = df.loc[["Format"] + vals]
    df.index.name = "Entity"
    df = df.drop(columns=["DataType"])
    return df


def build_filename_format(schema, **kwargs):
    """Create codeblocks containing example filename patterns for a given datatype."""
    schema = filter_schema(schema, **kwargs)
    entities = list(schema["entities"].keys())

    paragraph = ""
    # Parent folders
    paragraph += "{}-{}/[{}-{}/]\n".format(
        "sub",
        "<" + schema["entities"]["subject"]["format"] + ">",
        "ses",
        "<" + schema["entities"]["session"]["format"] + ">",
    )

    for datatype in schema["datatypes"].keys():
        paragraph += "\t{}/\n".format(datatype)

        # Unique filename patterns
        for group in schema["datatypes"][datatype]:
            string = "\t\t"
            for ent in entities:
                entity_shorthand = schema["entities"][ent]["entity"]
                ent_format = "{}-<{}>".format(entity_shorthand, schema["entities"][ent]["format"])
                if ent in group["entities"]:
                    if group["entities"][ent] == "required":
                        if len(string.strip()):
                            string += "_" + ent_format
                        else:
                            string += ent_format
                    else:
                        if len(string):
                            string += "[_" + ent_format + "]"
                        else:
                            string += "[" + ent_format + "]"

            # In cases of large numbers of suffixes,
            # we use the "suffix" variable and expect a table later in the spec
            if len(group["suffixes"]) > 4:
                suffix = "_<suffix>"
                string += suffix
                strings = [string]
            else:
                strings = [string + "_" + suffix for suffix in group["suffixes"]]

            # Add extensions
            full_strings = []
            extensions = utils.combine_extensions(group["extensions"])
            if len(extensions) > 5:
                # Combine exts when there are many, but keep JSON separate
                if ".json" in extensions:
                    extensions = [".<extension>", ".json"]
                else:
                    extensions = [".<extension>"]

            for extension in extensions:
                for string in strings:
                    new_string = string + extension
                    full_strings.append(new_string)
            full_strings = sorted(full_strings)
            if full_strings:
                paragraph += "\n".join(full_strings) + "\n"
    paragraph = paragraph.rstrip()
    codeblock = "Template:\n```Text\n" + paragraph + "\n```"
    codeblock = codeblock.expandtabs(4)
    return codeblock


def make_entity_table(schema, tablefmt="github", **kwargs):
    """Produce entity table (markdown) based on schema.

    Parameters
    ----------
    schema_path : str
        Folder containing schema, which is stored in yaml files.
    entities_file : str, optional
        File in which entities are described.
        This is used for hyperlinks in the table, so the path to the file
        should be considered from the location of out_file.
        Default is '09-entities.md'.

    Returns
    -------
    table : pandas.DataFrame
        DataFrame of entity table, with two layers of column headers.
    """
    from tabulate import tabulate

    schema = filter_schema(schema, **kwargs)

    ENTITIES_FILE = "09-entities.md"

    # prepare the table based on the schema
    # import pdb; pdb.set_trace()
    header = ["Entity", "DataType"]
    formats = ["Format", "DataType"]
    entity_to_col = {}
    table = [formats]

    # Compose header and formats first
    for i, (entity, spec) in enumerate(schema["entities"].items()):
        entity_shorthand = schema["entities"][entity]["entity"]
        header.append(spec["name"])
        formats.append(f'[`{entity_shorthand}-<{spec["format"]}>`]'
                       f"({ENTITIES_FILE}#{entity_shorthand})")
        entity_to_col[entity] = i + 1

    # Go through data types
    for dtype, dtype_specs in schema["datatypes"].items():
        dtype_rows = {}

        # each dtype could have multiple specs
        for spec in dtype_specs:
            suffixes = spec.get("suffixes")
            # TODO: <br> is specific for html form
            suffixes_str = " ".join(suffixes) if suffixes else ""
            dtype_row = [dtype] + ([""] * len(entity_to_col))
            for ent, req in spec.get("entities", []).items():
                dtype_row[entity_to_col[ent]] = req.upper()

            # Merge specs within dtypes if they share all of the same entities
            if dtype_row in dtype_rows.values():
                for k, v in dtype_rows.items():
                    if dtype_row == v:
                        dtype_rows.pop(k)
                        new_k = k + " " + suffixes_str
                        new_k = new_k.strip()
                        dtype_rows[new_k] = v
                        break
            else:
                dtype_rows[suffixes_str] = dtype_row

        # Reformat first column
        dtype_rows = {dtype + "<br>({})".format(k): v for k, v in dtype_rows.items()}
        dtype_rows = [[k] + v for k, v in dtype_rows.items()]
        table += dtype_rows

    # Create multi-level index because first two rows are headers
    cols = list(zip(header, table[0]))
    cols = pd.MultiIndex.from_tuples(cols)
    table = pd.DataFrame(data=table[1:], columns=cols)
    table = table.set_index(("Entity", "Format"))

    # Remove unnecessary columns
    table = drop_unused_entities(table)
    table = flatten_multiindexed_columns(table)

    # Print it as markdown
    table_str = tabulate(table, headers="keys", tablefmt=tablefmt)
    return table_str
