"""Utility functions for the bids-specification schema."""

from __future__ import annotations

import logging
import os
import sys
import warnings
from functools import wraps

from . import data

TYPE_CHECKING = False
if TYPE_CHECKING:
    from typing import Any, NotRequired, TypedDict

    from jsonschema import FormatChecker
    from jsonschema.protocols import Validator as JsonschemaValidator

    class ValidatorKwargs(TypedDict):
        """Type for the keyword arguments used to create a JSON schema validator."""

        format_checker: NotRequired[FormatChecker]


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


def jsonschema_validator(
    schema: dict[str, Any],
    *,
    check_format: bool,
    default_cls: type[JsonschemaValidator] | None = None,
) -> JsonschemaValidator:
    """
    Create a jsonschema validator appropriate for validating instances against a given
    JSON schema

    Parameters
    ----------
    schema : dict[str, Any]
        The JSON schema to validate against
    check_format : bool
        Indicates whether to check the format against format specifications in the
        schema
    default_cls : type[JsonschemaValidator] or None, optional
        The default JSON schema validator class to use to create the
        validator should the appropriate validator class cannot be determined based on
        the schema (by assessing the `$schema` property). If `None`, the class
        representing the latest JSON schema draft supported by the `jsonschema` package

    Returns
    -------
    JsonschemaValidator
        The JSON schema validator

    Raises
    ------
    jsonschema.exceptions.SchemaError
        If the JSON schema is invalid
    """
    try:
        from jsonschema.validators import validator_for
    except ImportError as e:
        raise RuntimeError(
            "The `jsonschema` package is required to validate schemas. "
            "Please install it with `pip install jsonschema`."
        ) from e

    cls_kwargs = {} if default_cls is None else {"default": default_cls}
    # Retrieve appropriate validator class for validating the given schema
    validator_cls = validator_for(schema, **cls_kwargs)

    # Ensure the schema is valid
    validator_cls.check_schema(schema)

    validator_kwargs: ValidatorKwargs
    validator_kwargs = {"format_checker": validator_cls.FORMAT_CHECKER} if check_format else {}
    return validator_cls(schema, **validator_kwargs)  # type: ignore[call-arg]


def in_context(context_manager):
    """Convert a context manager into a function decorator.

    Parameters
    ----------
    context_manager : context manager
        The context manager to use.

    Returns
    -------
    Callable
        The function decorator.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with context_manager:
                return func(*args, **kwargs)

        return wrapper

    return decorator


class WarningsFilter:
    """Context manager to apply warning filters.

    Arguments are lists of positional arguments to :func:`warnings.filterwarnings`.
    """

    def __init__(self, *filters):
        self.filters = filters

    def __enter__(self):
        self.catcher = warnings.catch_warnings()
        self.catcher.__enter__()
        for filt in self.filters:
            warnings.filterwarnings(*filt)

    def __exit__(self, exc_type, exc_value, traceback):
        self.catcher.__exit__(exc_type, exc_value, traceback)
