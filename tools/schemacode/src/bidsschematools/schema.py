"""Schema loading- and processing-related functions."""

import json
import os
import re
import sys
import tempfile
from collections.abc import Iterable, Mapping
from copy import deepcopy
from functools import lru_cache

from jsonschema import ValidationError, validate

if sys.version_info < (3, 9):
    from importlib_resources import files
else:
    from importlib.resources import files

from . import __bids_version__, __version__, utils
from .types import Namespace

lgr = utils.get_logger()


class BIDSSchemaError(Exception):
    """Errors indicating invalid values in the schema itself"""


def _get_schema_version(schema_dir):
    """
    Determine schema version for given schema directory, based on file specification.
    """

    schema_version_path = os.path.join(schema_dir, "SCHEMA_VERSION")
    with open(schema_version_path) as f:
        schema_version = f.readline().rstrip()
    return schema_version


def _get_bids_version(schema_dir):
    """
    Determine BIDS version for given schema directory, with directory name, file specification,
    and string fallback.
    """

    bids_version_path = os.path.join(schema_dir, "BIDS_VERSION")
    try:
        with open(bids_version_path) as f:
            bids_version = f.readline().rstrip()
    # If this file is not in the schema, fall back to placeholder heuristics:
    except FileNotFoundError:
        # Maybe the directory encodes the version, as in:
        # https://github.com/bids-standard/bids-schema
        _, bids_version = os.path.split(schema_dir)
        if not re.match(r"^.*?[0-9]*?\.[0-9]*?\.[0-9]*?.*?$", bids_version):
            # Then we don't know, really.
            bids_version = schema_dir
    return bids_version


def _find(obj, predicate):
    """Find objects in an arbitrary object that satisfy a predicate.

    Note that this does not cut branches, so every iterable sub-object
    will be fully searched.

    Parameters
    ----------
    obj : object
    predicate : function

    Returns
    -------
    generator
        A generator of entries in ``obj`` that satisfy the predicate.
    """
    try:
        if predicate(obj):
            yield obj
    except Exception:
        pass

    iterable = ()
    if isinstance(obj, Mapping):
        iterable = obj.values()
    elif not isinstance(obj, str) and isinstance(obj, Iterable):
        iterable = obj

    for item in iterable:
        yield from _find(item, predicate)


def _dereference(namespace, base_schema):
    # In-place, recursively dereference objects
    # This allows a referenced object to itself contain a reference
    # A dependency graph could be constructed, but would likely be slower
    # to build than to duplicate a couple dereferences
    for struct in _find(namespace, lambda obj: "$ref" in obj):
        target = base_schema.get(struct["$ref"])
        if target is None:
            raise ValueError(f"Reference {struct['$ref']} not found in schema.")
        if isinstance(target, Mapping):
            struct.pop("$ref")
            _dereference(target, base_schema)
            struct.update({**target, **struct})


def dereference(namespace, inplace=True):
    """Replace references in namespace with the contents of the referred object.

    Parameters
    ----------
    namespace : Namespace
        Namespace for which to dereference.

    inplace : bool, optional
        Whether to modify the namespace in place or create a copy, by default True.

    Returns
    -------
    namespace : Namespace
        Dereferenced namespace
    """
    if not inplace:
        namespace = deepcopy(namespace)

    _dereference(namespace, namespace)

    # At this point, any remaining refs are one-off objects in lists
    for struct in _find(namespace, lambda obj: any("$ref" in sub for sub in obj)):
        for i, item in enumerate(struct):
            try:
                target = item.pop("$ref")
            except (AttributeError, KeyError):
                pass
            else:
                struct[i] = namespace.get(target)

    return namespace


def flatten_enums(namespace, inplace=True):
    """Replace enum collections with a single enum, merging enums contents.

    The function helps reducing the complexity of the schema by assuming
    that the values in the conditions (anyOf) are mutually exclusive.

    Parameters
    ----------
    namespace : dict
        Schema in dictionary form to be flattened.

    Returns
    -------
    schema : dict
        Schema with flattened enums.

    Examples
    --------

    >>> struct = {
    ...   "anyOf": [
    ...      {"type": "string", "enum": ["A", "B", "C"]},
    ...      {"type": "string", "enum": ["D", "E", "F"]},
    ...   ]
    ... }
    >>> flatten_enums(struct)
    {'type': 'string', 'enum': ['A', 'B', 'C', 'D', 'E', 'F']}
    """
    if not inplace:
        namespace = deepcopy(namespace)
    for struct in _find(namespace, lambda obj: "anyOf" in obj):
        try:
            # Deduplicate because JSON schema validators may not like duplicates
            # Long run, we should get rid of this function and have the rendering
            # code handle anyOfs
            all_enum = list(dict.fromkeys(val for item in struct["anyOf"] for val in item["enum"]))
        except KeyError:
            continue

        del struct["anyOf"]
        struct.update({"type": "string", "enum": all_enum})
    return namespace


@lru_cache()
def load_schema(schema_path=None):
    """Load the schema into a dictionary.

    This function allows the schema, like BIDS itself, to be specified in
    a hierarchy of directories and files.
    Filenames (minus extensions) and directory names become keys
    in the associative array (dict) of entries composed from content
    of files and entire directories.

    Parameters
    ----------
    schema_path : str, optional
        Directory containing yaml files or yaml file. If ``None``, use the
        default schema packaged with ``bidsschematools``.

    Returns
    -------
    dict
        Schema in dictionary form.

    Notes
    -----
    This function is cached, so it will only be called once per schema path.
    """
    if schema_path is None:
        schema_path = utils.get_bundled_schema_path()
        lgr.info("No schema path specified, defaulting to the bundled schema, `%s`.", schema_path)
    schema = Namespace.from_directory(schema_path)
    if not schema.objects:
        raise ValueError(f"objects subdirectory path not found in {schema_path}")
    if not schema.rules:
        raise ValueError(f"rules subdirectory path not found in {schema_path}")

    dereference(schema)
    flatten_enums(schema)

    schema["bids_version"] = _get_bids_version(schema_path)
    schema["schema_version"] = _get_schema_version(schema_path)

    return schema


def export_schema(schema):
    """Export the schema to JSON format.

    Parameters
    ----------
    schema : dict
        The schema object, in dictionary form.

    Returns
    -------
    json : str
        The schema serialized as a JSON string.
    """
    versioned = Namespace.build({"schema_version": __version__, "bids_version": __bids_version__})
    versioned.update(schema)
    return versioned.to_json()


def filter_schema(schema, **kwargs):
    """Filter the schema based on a set of keyword arguments.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.

    Other Parameters
    ----------------
    **kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    new_schema : dict
        The filtered version of the schema.

    Notes
    -----
    This function calls itself recursively, in order to apply filters at
    arbitrary depth.

    Warning
    -------
    This function employs a *very* simple filter. It is very limited.
    """
    new_schema = deepcopy(schema)
    if isinstance(new_schema, dict):
        # Reduce values in dict to only requested
        for k, v in kwargs.items():
            if k in new_schema.keys():
                filtered_item = deepcopy(new_schema[k])
                if isinstance(filtered_item, dict):
                    filtered_item = {k1: v1 for k1, v1 in filtered_item.items() if k1 in v}
                else:
                    filtered_item = [i for i in filtered_item if i in v]
                new_schema[k] = filtered_item

            for k2, v2 in new_schema.items():
                new_schema[k2] = filter_schema(new_schema[k2], **kwargs)

    elif isinstance(new_schema, list):
        for i, item in enumerate(new_schema):
            if isinstance(item, dict):
                new_schema[i] = filter_schema(item, **kwargs)
    return new_schema


def validate_schema(schema: Namespace):
    """Validate a schema against the BIDS metaschema."""
    metaschema = json.loads(files("bidsschematools.data").joinpath("metaschema.json").read_text())

    # validate is put in this try/except clause because the error is sometimes too long to
    # print in the terminal
    try:
        validate(instance=schema.to_dict(), schema=metaschema)
    except ValidationError as e:
        with tempfile.NamedTemporaryFile(
            prefix="schema_error_", suffix=".txt", delete=False, mode="w+"
        ) as file:
            file.write(str(e))
            # ValidationError does not have an add_note method yet
            # e.add_note(f"See {file.name} for full error log.")
            raise e
