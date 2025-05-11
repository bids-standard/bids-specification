"""Utility functions for the bids-specification schema."""

import logging
import os
import sys

from . import data


def get_bundled_schema_path():
    """Get the path to the schema directory.

    Returns
    -------
    str
        Absolute path to the directory containing schema-related files.
    """
    return str(data.load_resource("schema"))


def get_logger(name=None, level=None):
    """Return a logger to use.

    Parameters
    ----------
    name : None or str, optional
        Name of the logger. Defaults to None.
    level: None or int, optional
        Level to set for the logger. Defaults to None.
        BIDS_SCHEMA_LOG_LEVEL environment variable can
        be used to set the level and will overwrite
        this value.

    Returns
    -------
    logging.Logger
        logger object.
    """
    logger = logging.getLogger("bidsschematools" + (f".{name}" if name else ""))
    # If explicitly instructed via env var -- set log level
    if log_level := os.getenv("BIDS_SCHEMA_LOG_LEVEL", level):
        set_logger_level(logger, log_level)
    return logger


def configure_logger(lgr):
    """Configuring formatting and stream handler for the logger.

    Should not be used when bidsschematools is used as a library.

    Parameters
    ----------
    lgr: logging.Logger

    """
    if len(lgr.handlers) == 0:
        # add a handler if there isn't one
        ch = logging.StreamHandler(stream=sys.stderr)
        lgr.addHandler(ch)
    # Set the formatter for the handlers
    for lh in lgr.handlers:
        lh.setFormatter(logging.Formatter("%(asctime)-15s [%(levelname)8s] %(message)s"))


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
        lgr.warning("Do not know how to treat loglevel %s", level)
        return
    lgr.setLevel(level)
