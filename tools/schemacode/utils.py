"""
Utility functions for the bids-specification schema.
"""
import logging
import os.path as op

import numpy as np


def get_schema_path():
    return op.abspath(
        op.join(
            op.dirname(op.dirname(op.dirname(__file__))),
            "src",
            "schema"
        ) + op.sep
    )


def combine_extensions(lst):
    """
    This is a basic solution to combining extensions with their
    compressed versions in a list. Something more robust could
    be written in the future.
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
    """Return a logger to use"""
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
