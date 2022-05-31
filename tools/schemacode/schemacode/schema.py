"""Schema loading- and processing-related functions."""
import logging
import os
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


def dereference_yaml(schema, struct):
    """Recursively search a dictionary-like object for $ref keys.

    Each $ref key is replaced with the contents of the referenced field in the overall
    dictionary-like object.
    """
    if isinstance(struct, dict):
        if "$ref" in struct:
            ref_field = struct["$ref"]
            template = schema[ref_field]
            struct.pop("$ref")
            # Result is template object with local overrides
            struct = {**template, **struct}

        struct = {key: dereference_yaml(schema, val) for key, val in struct.items()}

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
        struct = [dereference_yaml(schema, item) for item in struct]

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
    objects_dir = schema_path / "objects/"
    rules_dir = schema_path / "rules/"

    if not objects_dir.is_dir() or not rules_dir.is_dir():
        raise ValueError(
            f"Schema path or paths do not exist:\n\t{str(objects_dir)}\n\t{str(rules_dir)}"
        )

    schema = {}
    schema["objects"] = {}
    schema["rules"] = {}

    # Load object definitions. All are present in single files.
    for object_group_file in sorted(objects_dir.glob("*.yaml")):
        lgr.debug(f"Loading {object_group_file.stem} objects.")
        dict_ = yaml.safe_load(object_group_file.read_text())
        schema["objects"][object_group_file.stem] = dereference_yaml(dict_, dict_)

    # Grab single-file rule groups
    for rule_group_file in sorted(rules_dir.glob("*.yaml")):
        lgr.debug(f"Loading {rule_group_file.stem} rules.")
        dict_ = yaml.safe_load(rule_group_file.read_text())
        schema["rules"][rule_group_file.stem] = dereference_yaml(dict_, dict_)

    # Load directories of rule subgroups.
    for rule_group_file in sorted(rules_dir.glob("*/*.yaml")):
        rule = schema["rules"].setdefault(rule_group_file.parent.name, {})
        lgr.debug(f"Loading {rule_group_file.stem} rules.")
        dict_ = yaml.safe_load(rule_group_file.read_text())
        rule[rule_group_file.stem] = dereference_yaml(dict_, dict_)

    return schema


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
