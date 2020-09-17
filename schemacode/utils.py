"""
Utility functions for the bids-specification schema.
"""
import logging
import os.path as op


def get_schema_path():
    return op.abspath(
        op.join(op.dirname(op.dirname(__file__)), "src", "schema") + op.sep
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
