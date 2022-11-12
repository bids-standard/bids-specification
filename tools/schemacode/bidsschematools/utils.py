"""Utility functions for the bids-specification schema."""
import logging
import os.path as op


def get_schema_path():
    """Get the path to the schema directory.

    Returns
    -------
    str
        Absolute path to the directory containing schema-related files.
    """
    return op.abspath(op.join(op.dirname(__file__), "data", "schema"))


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
