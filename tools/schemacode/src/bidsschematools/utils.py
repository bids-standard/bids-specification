"""Utility functions for the bids-specification schema."""

import logging
import os

from . import data


def get_bundled_schema_path():
    """Get the path to the schema directory.

    Returns
    -------
    str
        Absolute path to the directory containing schema-related files.
    """
    return str(data.load_resource("schema"))


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
    logger = logging.getLogger("bidsschematools" + (".%s" % name if name else ""))
    # Basic settings for output, for now just basic
    set_logger_level(logger, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
    format = "%(asctime)-15s [%(levelname)8s] %(message)s"
    if len(logger.handlers) == 0:
        # add a handler if there isn't one
        ch = logging.StreamHandler()
        logger.addHandler(ch)
    # Set the formatter for the handlers
    for lh in logger.handlers:
        lh.setFormatter(logging.Formatter(format))

    return logger


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
