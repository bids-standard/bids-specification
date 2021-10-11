"""Utility functions for the bids-specification schema."""
import logging
import os.path as op
from pprint import pprint

import numpy as np


def get_schema_path():
    """Get the path to the schema folder.

    Returns
    -------
    str
        Absolute path to the folder containing schema-related files.
    """
    schema_dir = op.abspath(
        op.join(op.dirname(op.dirname(op.dirname(op.dirname(__file__)))), "src", "schema") + op.sep
    )
    return schema_dir


def combine_extensions(lst):
    """Combine extensions with their compressed versions in a list.

    This is a basic solution to combining extensions with their
    compressed versions in a list. Something more robust could
    be written in the future.

    Parameters
    ----------
    lst : list of str
    """
    new_lst = []
    # First, sort by length
    lst = sorted(lst, key=len)
    for item in lst:
        temp_lst = new_lst[:]

        item_found = False
        for j, new_item in enumerate(temp_lst):
            if new_item in item:
                temp_item = new_item + "[" + item.replace(new_item, "", 1) + "]"
                new_lst[j] = temp_item
                item_found = True

        if not item_found:
            new_lst.append(item)

    return new_lst


def get_logger(name=None):
    """Return a logger to use.

    Parameters
    ----------
    name : None or str, optional
        Name of the logger. Defaults to None.

    Returns
    -------
    logging.Logger
        logger object.
    """
    return logging.getLogger("bids-schema" + (".%s" % name if name else ""))


def set_logger_level(lgr, level):
    """Set the logger level.

    Parameters
    ----------
    lgr : logging.Logger
        logger object for which to change the level.
    level : int or str
        The desired level for the logger.
    """
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


def drop_unused_entities(df):
    """Remove columns from a dataframe where all values in the column are NaNs.

    For entity tables, this limits each table to only entities that are used
    within the modality.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing entities and datatypes/suffixes.
        Rows are datatype/suffix combinations and columns are entities.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with columns associated with unused entities removed.
    """
    df = df.replace("", np.nan).dropna(axis=1, how="all").fillna("")
    return df


def flatten_multiindexed_columns(df):
    """Remove multi-indexing of multi-indexed column headers.

    The first layer is the "DataType", while the second layer is the "Format".
    This second layer will become a new row.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with two header levels: "Datatype" and "Format".

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with the second header level ("Format") converted to a
        normal row.
    """
    # Flatten multi-index
    vals = df.index.tolist()
    df.loc["Format"] = df.columns.get_level_values(1)
    df.columns = df.columns.get_level_values(0)
    df = df.loc[["Format"] + vals]
    df.index.name = "Entity"
    df = df.drop(columns=["DataType"])
    return df


def get_link(string):
    refs = {
        "array": "https://www.w3schools.com/js/js_json_arrays.asp",
        "string": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "number": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "object": "https://www.json.org/json-en.html",
        "integer": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "boolean": "https://www.w3schools.com/js/js_json_datatypes.asp",
    }
    # Allow plurals (e.g., strings -> links to string)
    dtype = string[:-1] if string[-1] == "s" else string
    url = refs.get(dtype)
    if url:
        return f"[{string}]({url})"
    return string


def resolve_metadata_type(definition):
    """Generate string of metadata type from dictionary."""
    if "type" in definition.keys():
        string = get_link(definition["type"])

        if definition.get("enum") == ["n/a"]:
            # Special string case of n/a
            string = '`"n/a"`'

        elif "type" in definition.get("items", {}):
            # Items within arrays
            string += " of " + get_link(definition["items"]["type"] + "s")

        elif "type" in definition.get("additionalProperties", {}):
            # Values within objects
            string += " of " + get_link(
                definition["additionalProperties"]["type"] + "s"
            )

    elif "anyOf" in definition:
        # Use dictionary to get unique substrings while preserving insertion order
        substrings = {resolve_metadata_type(subdict): None
                      for subdict in definition["anyOf"]}

        string = " or ".join(substrings)

    else:
        # A hack to deal with $ref in the current schema
        print(f"Type could not be inferred for {definition['name']}")
        pprint(definition)
        string = "unknown"

    return string
