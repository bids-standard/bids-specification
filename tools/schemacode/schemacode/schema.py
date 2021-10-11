"""Schema loading- and processing-related functions."""
import logging
import os
import os.path as op
from copy import deepcopy
from glob import glob
from pathlib import Path

import pandas as pd
import yaml
from tabulate import tabulate

from . import utils

lgr = utils.get_logger()
# Basic settings for output, for now just basic
utils.set_logger_level(
    lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO)
)
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
        Folder containing yaml files or yaml file.

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
    object_group_files = sorted(glob(str(objects_dir / "*.yaml")))
    for object_group_file in object_group_files:
        group_name = op.splitext(op.basename(object_group_file))[0]
        lgr.info(f"Loading {group_name} objects.")
        with open(object_group_file, "r") as fo:
            dict_ = yaml.load(fo, Loader=yaml.SafeLoader)
            dict_ = dereference_yaml(dict_, dict_)
            schema["objects"][group_name] = dict_

    # Grab single-file rule groups
    rule_group_files = sorted(glob(str(rules_dir / "*.yaml")))
    rule_group_folders = sorted(glob(str(rules_dir / "*")))
    rule_group_folders = [f for f in rule_group_folders if op.isdir(f)]
    for rule_group_file in rule_group_files:
        group_name = op.splitext(op.basename(rule_group_file))[0]
        lgr.info(f"Loading {group_name} rules.")
        with open(rule_group_file, "r") as fo:
            dict_ = yaml.load(fo, Loader=yaml.SafeLoader)
            dict_ = dereference_yaml(dict_, dict_)
            schema["rules"][group_name] = dict_

    # Load folders of rule subgroups.
    for rule_group_folder in rule_group_folders:
        group_name = op.basename(rule_group_folder)
        rule_subgroup_files = sorted(glob(op.join(rule_group_folder, "*.yaml")))
        schema["rules"][group_name] = {}
        for rule_subgroup_file in rule_subgroup_files:
            subgroup_name = op.splitext(op.basename(rule_subgroup_file))[0]
            lgr.info(f"Loading {subgroup_name} rules.")
            with open(rule_subgroup_file, "r") as fo:
                dict_ = yaml.load(fo, Loader=yaml.SafeLoader)
                dict_ = dereference_yaml(dict_, dict_)
                schema["rules"][group_name][subgroup_name] = dict_

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
                    filtered_item = {
                        k1: v1 for k1, v1 in filtered_item.items() if k1 in v
                    }
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


def make_entity_definitions(schema):
    """Generate definitions and other relevant information for entities in the specification.

    Each entity gets its own heading.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.

    Returns
    -------
    text : str
        A string containing descriptions and some formatting
        information about the entities in the schema.
    """
    entity_order = schema["rules"]["entities"]
    entity_definitions = schema["objects"]["entities"]

    text = ""
    for entity in entity_order:
        entity_info = entity_definitions[entity]
        entity_shorthand = entity_info["entity"]
        text += "\n"
        text += "## {}".format(entity_shorthand)
        text += "\n\n"
        text += "Full name: {}".format(entity_info["name"])
        text += "\n\n"
        text += "Format: `{}-<{}>`".format(
            entity_info["entity"],
            entity_info.get("format", "label"),
        )
        text += "\n\n"
        if "enum" in entity_info.keys():
            text += "Allowed values: `{}`".format("`, `".join(entity_info["enum"]))
            text += "\n\n"

        text += "Definition: {}".format(entity_info["description"])
    return text


def make_filename_template(schema, **kwargs):
    """Create codeblocks containing example filename patterns for a given datatype.

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
    codeblock : str
        A multiline string containing the filename templates for file types
        in the schema, after filtering.
    """
    schema = filter_schema(schema, **kwargs)

    entity_order = schema["rules"]["entities"]

    paragraph = ""
    # Parent folders
    paragraph += "{}-<{}>/\n\t[{}-<{}>/]\n".format(
        schema["objects"]["entities"]["subject"]["entity"],
        schema["objects"]["entities"]["subject"]["format"],
        schema["objects"]["entities"]["session"]["entity"],
        schema["objects"]["entities"]["session"]["format"],
    )

    for datatype in schema["rules"]["datatypes"].keys():
        paragraph += "\t\t{}/\n".format(datatype)

        # Unique filename patterns
        for group in schema["rules"]["datatypes"][datatype]:
            string = "\t\t\t"
            for ent in entity_order:
                ent_format = "{}-<{}>".format(
                    schema["objects"]["entities"][ent]["entity"],
                    schema["objects"]["entities"][ent].get("format", "label")
                )
                if ent in group["entities"]:
                    if group["entities"][ent] == "required":
                        if len(string.strip()):
                            string += "_" + ent_format
                        else:
                            # Only the first entity doesn't need an underscore
                            string += ent_format
                    else:
                        if len(string.strip()):
                            string += "[_" + ent_format + "]"
                        else:
                            # Only the first entity doesn't need an underscore
                            string += "[" + ent_format + "]"

            # In cases of large numbers of suffixes,
            # we use the "suffix" variable and expect a table later in the spec
            if len(group["suffixes"]) > 5:
                suffix = "_<suffix>"
                string += suffix
                strings = [string]
            else:
                strings = [
                    string + "_" + suffix for suffix in group["suffixes"]
                ]

            # Add extensions
            full_strings = []
            extensions = group["extensions"]
            extensions = [
                ext if ext != "*" else ".<extension>" for ext in extensions
            ]
            extensions = utils.combine_extensions(extensions)
            if len(extensions) > 5:
                # Combine exts when there are many, but keep JSON separate
                if ".json" in extensions:
                    extensions = [".<extension>", ".json"]
                else:
                    extensions = [".<extension>"]

            for extension in extensions:
                for string in strings:
                    new_string = string + extension
                    full_strings.append(new_string)

            full_strings = sorted(full_strings)
            if full_strings:
                paragraph += "\n".join(full_strings) + "\n"

    paragraph = paragraph.rstrip()
    codeblock = "Template:\n```Text\n" + paragraph + "\n```"
    codeblock = codeblock.expandtabs(4)
    return codeblock


def make_entity_table(schema, tablefmt="github", **kwargs):
    """Produce entity table (markdown) based on schema.

    Parameters
    ----------
    schema_path : str
        Folder containing schema, which is stored in yaml files.
    entities_file : str, optional
        File in which entities are described.
        This is used for hyperlinks in the table, so the path to the file
        should be considered from the location of out_file.
        Default is '09-entities.md'.

    Returns
    -------
    table_str : str
        Markdown string containing the table.
    """
    schema = filter_schema(schema, **kwargs)

    ENTITIES_FILE = "09-entities.md"

    # prepare the table based on the schema
    # import pdb; pdb.set_trace()
    header = ["Entity", "DataType"]
    formats = ["Format", "DataType"]
    entity_to_col = {}
    table = [formats]

    # Compose header and formats first
    for i, (entity, spec) in enumerate(schema["objects"]["entities"].items()):
        entity_shorthand = schema["objects"]["entities"][entity]["entity"]
        header.append(spec["name"])
        formats.append(
            f'[`{entity_shorthand}-<{spec.get("format", "label")}>`]'
            f"({ENTITIES_FILE}#{entity_shorthand})"
        )
        entity_to_col[entity] = i + 1

    # Go through data types
    for dtype, dtype_specs in schema["rules"]["datatypes"].items():
        dtype_rows = {}

        # each dtype could have multiple specs
        for spec in dtype_specs:
            suffixes = spec.get("suffixes")

            # Skip this part of the schema if no suffixes are found.
            # This is a hack to work around filter_schema's limitations.
            if not len(suffixes):
                continue

            # TODO: <br> is specific for html form
            suffixes_str = " ".join(suffixes) if suffixes else ""
            dtype_row = [dtype] + ([""] * len(entity_to_col))
            for ent, req in spec.get("entities", []).items():
                dtype_row[entity_to_col[ent]] = req.upper()

            # Merge specs within dtypes if they share all of the same entities
            if dtype_row in dtype_rows.values():
                for k, v in dtype_rows.items():
                    if dtype_row == v:
                        dtype_rows.pop(k)
                        new_k = k + " " + suffixes_str
                        new_k = new_k.strip()
                        dtype_rows[new_k] = v
                        break
            else:
                dtype_rows[suffixes_str] = dtype_row

        # Reformat first column
        dtype_rows = {
            dtype + "<br>({})".format(k): v for k, v in dtype_rows.items()
        }
        dtype_rows = [[k] + v for k, v in dtype_rows.items()]
        table += dtype_rows

    # Create multi-level index because first two rows are headers
    cols = list(zip(header, table[0]))
    cols = pd.MultiIndex.from_tuples(cols)
    table = pd.DataFrame(data=table[1:], columns=cols)
    table = table.set_index(("Entity", "Format"))

    # Remove unnecessary columns
    table = utils.drop_unused_entities(table)
    table = utils.flatten_multiindexed_columns(table)

    # Print it as markdown
    table_str = tabulate(table, headers="keys", tablefmt=tablefmt)
    return table_str


def make_suffix_table(schema, suffixes, tablefmt="github"):
    """Produce suffix table (markdown) based on requested suffixes.

    Parameters
    ----------
    schema : dict
    suffixes : list of str
    tablefmt : str

    Returns
    -------
    table_str : str
        Tabulated table as a string.
    """
    # The filter function doesn't work here.
    suffix_schema = schema["objects"]["suffixes"]

    suffixes_found = [f for f in suffixes if f in suffix_schema.keys()]
    suffixes_not_found = [f for f in suffixes if f not in suffix_schema.keys()]
    if suffixes_not_found:
        raise Exception(
            "Warning: Missing suffixes: {}".format(
                ", ".join(suffixes_not_found)
            )
        )

    df = pd.DataFrame(
        index=suffixes_found,
        columns=["**Name**", "**Description**"],
    )
    # Index by suffix because name cannot be assumed to be unique
    df.index.name = "`suffix`"
    for suffix in suffixes_found:
        suffix_info = suffix_schema[suffix]
        description = suffix_info["description"]
        # A backslash before a newline means continue a string
        description = description.replace("\\\n", "")
        # Two newlines should be respected
        description = description.replace("\n\n", "<br>")
        # Otherwise a newline corresponds to a space
        description = description.replace("\n", " ")

        df.loc[suffix] = [suffix_info["name"], description]

    df = df.reset_index(drop=False)
    df = df.set_index("**Name**")
    df = df[["`suffix`", "**Description**"]]

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    return table_str


def make_metadata_table(schema, field_info, tablefmt="github"):
    """Produce metadata table (markdown) based on requested fields.

    Parameters
    ----------
    schema : dict
        The BIDS schema.
    field_info : dict of strings or tuples
        A dictionary mapping metadata keys to requirement levels in the
        rendered metadata table.
        The dictionary values may be strings, in which case the string
        is the requirement level information, or two-item tuples of strings,
        in which case the first string is the requirement level information
        and the second string is additional table-specific information
        about the metadata field that will be appended to the field's base
        definition from the schema.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).

    Returns
    -------
    table_str : str
        The tabulated table as a Markdown string.
    """
    fields = list(field_info.keys())
    # The filter function doesn't work here.
    metadata_schema = schema["objects"]["metadata"]

    retained_fields = [f for f in fields if f in metadata_schema.keys()]
    dropped_fields = [f for f in fields if f not in metadata_schema.keys()]
    if dropped_fields:
        print("Warning: Missing fields: {}".format(", ".join(dropped_fields)))

    # Use the "name" field in the table, to allow for filenames to not match
    # "names".
    df = pd.DataFrame(
        index=[metadata_schema[f]["name"] for f in retained_fields],
        columns=["**Requirement Level**", "**Data type**", "**Description**"],
    )
    df.index.name = "**Key name**"
    for field in retained_fields:
        field_name = metadata_schema[field]["name"]
        requirement_info = field_info[field]
        description_addendum = ""
        if isinstance(requirement_info, tuple):
            requirement_info, description_addendum = requirement_info

        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](/02-common-principles.html#definitions)",
        )

        type_string = utils.resolve_metadata_type(metadata_schema[field])

        description = (
            metadata_schema[field]["description"] + " " + description_addendum
        )
        # A backslash before a newline means continue a string
        description = description.replace("\\\n", "")
        # Two newlines should be respected
        description = description.replace("\n\n", "<br>")
        # Otherwise a newline corresponds to a space
        description = description.replace("\n", " ")

        df.loc[field_name] = [requirement_info, type_string, description]

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    return table_str
