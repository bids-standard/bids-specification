"""Schema loading- and processing-related functions."""
import logging
import os
import re
from collections.abc import Mapping
from copy import deepcopy
from pathlib import Path

import yaml

from . import utils

lgr = utils.get_logger()
# Basic settings for output, for now just basic
utils.set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
logging.basicConfig(format="%(asctime)-15s [%(levelname)8s] %(message)s")


def _get_entry_name(path):
    if path.suffix == ".yaml":
        return path.name[:-5]  # no .yaml
    else:
        return path.name


def _get_bids_version(bids_schema_dir):
    """Determine schema version, with directory name, file specification, and string fallback."""

    bids_version_path = os.path.join(bids_schema_dir, "BIDS_VERSION")
    try:
        with open(bids_version_path) as f:
            bids_version = f.readline().rstrip()
    # If this file is not in the schema, fall back to placeholder heuristics:
    except FileNotFoundError:
        # Maybe the directory encodes the version, as in:
        # https://github.com/bids-standard/bids-schema
        _, bids_version = os.path.split(bids_schema_dir)
        if not re.match(r"^.*?[0-9]*?\.[0-9]*?\.[0-9]*?.*?$", bids_version):
            # Then we don't know, really.
            bids_version = bids_schema_dir
    return bids_version


def _expand_dots(entry):
    # Helper function for expand
    key, val = entry
    if "." in key:
        init, post = key.split(".", 1)
        return init, dict([_expand_dots((post, val))])
    return key, expand(val)


def expand(element):
    """Expand a dict, recursively, to replace dots in keys with recursive dictionaries

    Examples
    --------
    >>> expand({"a": 1, "b.c": 2, "d": [{"e": 3, "f.g": 4}]})
    {'a': 1, 'b': {'c': 2}, 'd': [{'e': 3, 'f': {'g': 4}}]}
    """
    if isinstance(element, dict):
        return {key: val for key, val in map(_expand_dots, element.items())}
    elif isinstance(element, list):
        return [expand(el) for el in element]
    return element


class Namespace(Mapping):
    """Provides recursive attribute style access to a dict-like structure

    Examples
    --------
    >>> ns = Namespace.build({"a": 1, "b.c": "val"})
    >>> ns.a
    1
    >>> ns["a"]
    1
    >>> ns.b
    <Namespace {'c': 'val'}>
    >>> ns["b"]
    <Namespace {'c': 'val'}>
    >>> ns.b.c
    'val'
    >>> ns["b.c"]
    'val'
    >>> ns["b"]["c"]
    'val'
    >>> ns.b["c"]
    'val'
    >>> ns["b"].c
    'val'
    """

    def __init__(self, *args, **kwargs):
        self._properties = dict(*args, **kwargs)

    def to_dict(self):
        ret = {}
        for key, val in self._properties.items():
            if isinstance(val, Namespace):
                val = val.to_dict()
            ret[key] = val
        return ret

    def __deepcopy__(self, memo):
        return self.build(self.to_dict())

    @classmethod
    def build(cls, mapping):
        """Expand mapping recursively and return as namespace"""
        return cls(expand(mapping))

    def __getattribute__(self, key):
        # Return actual properties first
        err = None
        try:
            return super().__getattribute__(key)
        except AttributeError as e:
            err = e

        # Utilize __getitem__ but keep original error on failure
        try:
            return self[key]
        except KeyError:
            raise err

    def __getitem__(self, key):
        key, dot, subkey = key.partition(".")
        val = self._properties[key]
        if isinstance(val, dict):
            val = self.__class__(val)
        if dot:
            # Recursive step
            val = val[subkey]
        return val

    def __repr__(self):
        return f"<Namespace {self._properties}>"

    def __len__(self):
        return len(self._properties)

    def __iter__(self):
        return iter(self._properties)

    @classmethod
    def from_directory(cls, path, fmt="yaml"):
        mapping = {}
        fullpath = Path(path)
        if fmt == "yaml":
            for subpath in sorted(fullpath.iterdir()):
                if subpath.is_dir():
                    submapping = cls.from_directory(subpath)
                    if submapping:
                        mapping[subpath.name] = submapping
                elif subpath.name.endswith("yaml"):
                    mapping[subpath.stem] = yaml.safe_load(subpath.read_text())
            return cls.build(mapping)
        raise NotImplementedError(f"Unknown format: {fmt}")


def dereference_mapping(schema, struct):
    """Recursively search a dictionary-like object for $ref keys.

    Each $ref key is replaced with the contents of the referenced field in the overall
    dictionary-like object.
    """
    if isinstance(struct, Mapping):
        struct = dict(struct)
        if "$ref" in struct:
            ref_field = struct["$ref"]
            template = schema[ref_field]
            struct.pop("$ref")
            # Result is template object with local overrides
            struct = {**template, **struct}

        struct = {key: dereference_mapping(schema, val) for key, val in struct.items()}

        # For the rare case of multiple sets of valid values (enums) from multiple references,
        # anyOf is used. Here we try to flatten our anyOf of enums into a single enum list.
        if "anyOf" in struct.keys():
            if all("enum" in obj for obj in struct["anyOf"]):
                all_enum = [v["enum"] for v in struct["anyOf"]]
                all_enum = [item for sublist in all_enum for item in sublist]

                struct.pop("anyOf")
                struct["type"] = "string"
                struct["enum"] = all_enum

    elif isinstance(struct, list):
        struct = [dereference_mapping(schema, item) for item in struct]

    return struct


def load_schema(schema_path):
    """Load the schema into a dictionary.

    This function allows the schema, like BIDS itself, to be specified in
    a hierarchy of directories and files.
    File names (minus extensions) and directory names become keys
    in the associative array (dict) of entries composed from content
    of files and entire directories.

    Parameters
    ----------
    schema_path : str
        Directory containing yaml files or yaml file.

    Returns
    -------
    dict
        Schema in dictionary form.
    """
    schema_path = Path(schema_path)
    schema = Namespace.from_directory(schema_path)
    if not schema.objects:
        raise ValueError(f"objects subdirectory path not found in {schema_path}")
    if not schema.rules:
        raise ValueError(f"rules subdirectory path not found in {schema_path}")

    dereferenced = dereference_mapping(schema, schema)
    return Namespace.build(dereferenced)


def filter_schema(schema, **kwargs):
    """Filter the schema based on a set of keyword arguments.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.
    kwargs : dict
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
