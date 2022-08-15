"""Functions for rendering portions of the schema as text."""
import logging
import os
import posixpath
from collections.abc import Mapping

import pandas as pd
from tabulate import tabulate

from . import utils
from .schema import filter_schema

lgr = utils.get_logger()
# Basic settings for output, for now just basic
utils.set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
logging.basicConfig(format="%(asctime)-15s [%(levelname)8s] %(message)s")


def get_relpath(src_path):
    """Retrieve relative path to the source root from the perspective of a Markdown file.

    As a convenience, ``None`` is interpreted as the empty string, and a value of ``'.'``
    is returned.

    Examples
    --------
    >>> get_relpath("02-common-principles.md")
    '.'
    >>> get_relpath("04-modality-specific-files/01-magnetic-resonance-imaging-data.md")
    '..'
    >>> get_relpath("we/lack/third_levels.md")
    '../..'
    >>> get_relpath(None)
    '.'
    """
    return posixpath.relpath(".", posixpath.dirname(src_path or ""))


def make_entity_definitions(schema, src_path=None):
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
        entity_shorthand = entity_info["name"]
        text += "\n"
        text += "## {}".format(entity_shorthand)
        text += "\n\n"
        text += "Full name: {}".format(entity_info["display_name"])
        text += "\n\n"
        text += "Format: `{}-<{}>`".format(
            entity_info["name"],
            entity_info.get("format", "label"),
        )
        text += "\n\n"
        if "enum" in entity_info.keys():
            text += "Allowed values: `{}`".format("`, `".join(entity_info["enum"]))
            text += "\n\n"

        description = entity_info["description"]
        description = description.replace("SPEC_ROOT", get_relpath(src_path))
        text += "Definition: {}".format(description)
    return text


def make_glossary(schema, src_path=None):
    """Generate glossary.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    text : str
        A string containing descriptions and some formatting
        information about the entities in the schema.
    """
    all_objects = {}

    for group, group_objects in schema["objects"].items():
        group_obj_keys = list(group_objects.keys())
        # Remove private objects
        group_obj_keys = [k for k in group_obj_keys if not k.startswith("_")]

        multi_sense_objects = []
        # Identify multi-sense objects (multiple entries, some with __ in them)
        for key in group_obj_keys:
            if "__" in key:
                temp_key = key.split("__")[0]
                multi_sense_objects.append(temp_key)

        multi_sense_objects = sorted(list(set(multi_sense_objects)))
        sense_keys = {mso: [] for mso in multi_sense_objects}

        for key in group_obj_keys:
            for sense_key in sense_keys.keys():
                if (key == sense_key) or (key.startswith(sense_key + "__")):
                    sense_keys[sense_key].append(key)

        sense_names = {}
        for sense_key, key_list in sense_keys.items():
            for i_key, key in enumerate(key_list):
                new_key_name = f"{sense_key} _sense {i_key + 1}_"
                sense_names[key] = new_key_name

        for key in group_obj_keys:
            new_name = sense_names.get(key, key)
            new_name = f"{new_name} ({group})"
            all_objects[new_name] = {}
            all_objects[new_name]["key"] = f"objects.{group}.{key}"
            all_objects[new_name]["definition"] = group_objects[key]

    text = ""
    for obj_key in sorted(all_objects.keys()):
        obj = all_objects[obj_key]
        obj_marker = obj["key"]
        obj_def = obj["definition"]
        obj_name = obj_def["display_name"]
        obj_desc = obj_def["description"]
        # A backslash before a newline means continue a string
        obj_desc = obj_desc.replace("\\\n", "")
        # Two newlines should be respected
        obj_desc = obj_desc.replace("\n\n", "<br>")
        # Otherwise a newline corresponds to a space
        obj_desc = obj_desc.replace("\n", " ")
        # Spec internal links need to be replaced
        obj_desc = obj_desc.replace("SPEC_ROOT", get_relpath(src_path))

        text += f'\n<a name="{obj_marker}"></a>'
        text += f"\n## {obj_key}\n\n"
        text += f"name: {obj_name}\n\n"
        text += f"description:\n>{obj_desc}\n\n"

        temp_obj_def = {k: v for k, v in obj_def.items() if k not in ("description", "name")}
        text += f"schema information:\n```yaml\n{temp_obj_def}\n```"

    return text


def _add_entity(filename_template, entity_pattern, requirement_level):
    """Add entity pattern to filename template based on requirement level."""
    if requirement_level == "required":
        if len(filename_template.strip()):
            filename_template += "_" + entity_pattern
        else:
            # Only the first entity doesn't need an underscore
            filename_template += entity_pattern
    else:
        if len(filename_template.strip()):
            filename_template += "[_" + entity_pattern + "]"
        else:
            # Only the first entity doesn't need an underscore
            filename_template += "[" + entity_pattern + "]"

    return filename_template


def make_filename_template(schema, n_dupes_to_combine=6, **kwargs):
    """Create codeblocks containing example filename patterns for a given datatype.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.
    n_dupes_to_combine : int
        The minimum number of suffixes/extensions to combine in the template as
        <suffix>/<extension>.
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
    entity_order = schema["rules"]["entities"]

    paragraph = ""
    # Parent directories
    paragraph += "{}-<{}>/\n\t[{}-<{}>/]\n".format(
        schema["objects"]["entities"]["subject"]["name"],
        schema["objects"]["entities"]["subject"]["format"],
        schema["objects"]["entities"]["session"]["name"],
        schema["objects"]["entities"]["session"]["format"],
    )

    datatypes = filter_schema(schema.rules.datatypes, **kwargs)

    for datatype in datatypes:
        # XXX We should have a full rethink of the schema hierarchy...
        if datatype == "derivatives":
            continue
        paragraph += "\t\t{}/\n".format(datatype)

        # Unique filename patterns
        for group in datatypes[datatype].values():
            string = "\t\t\t"
            for ent in entity_order:
                if "enum" in schema["objects"]["entities"][ent].keys():
                    # Entity key-value pattern with specific allowed values
                    ent_format = "{}-<{}>".format(
                        schema["objects"]["entities"][ent]["name"],
                        "|".join(schema["objects"]["entities"][ent]["enum"]),
                    )
                else:
                    # Standard entity key-value pattern with simple label/index
                    ent_format = "{}-<{}>".format(
                        schema["objects"]["entities"][ent]["name"],
                        schema["objects"]["entities"][ent].get("format", "label"),
                    )

                if ent in group["entities"]:
                    if isinstance(group["entities"][ent], dict):
                        if "enum" in group["entities"][ent].keys():
                            # Overwrite the filename pattern based on the valid values
                            ent_format = "{}-<{}>".format(
                                schema["objects"]["entities"][ent]["name"],
                                "|".join(group["entities"][ent]["enum"]),
                            )

                        string = _add_entity(
                            string,
                            ent_format,
                            group["entities"][ent]["requirement"],
                        )
                    else:
                        string = _add_entity(string, ent_format, group["entities"][ent])

            # In cases of large numbers of suffixes,
            # we use the "suffix" variable and expect a table later in the spec
            if len(group["suffixes"]) >= n_dupes_to_combine:
                suffix = "_<suffix>"
                string += suffix
                strings = [string]
            else:
                strings = [string + "_" + suffix for suffix in group["suffixes"]]

            # Add extensions
            full_strings = []
            extensions = group["extensions"]
            extensions = [ext if ext != "*" else ".<extension>" for ext in extensions]
            extensions = utils.combine_extensions(extensions)
            if len(extensions) >= n_dupes_to_combine:
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
        Directory containing schema, which is stored in yaml files.
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
    table = [formats]

    # Compose header and formats first
    all_entities = schema["rules"]["entities"]
    for entity in all_entities:
        entity_spec = schema["objects"]["entities"][entity]
        entity_shorthand = entity_spec["name"]
        header.append(entity_spec["display_name"])
        formats.append(
            f'[`{entity_shorthand}-<{entity_spec.get("format", "label")}>`]'
            f"({ENTITIES_FILE}#{entity_shorthand})"
        )

    # Go through data types
    for dtype, dtype_specs in schema["rules"]["datatypes"].items():
        dtype_rows = {}
        duplicate_row_counter = 0

        # each dtype could have multiple specs
        for dtype_spec in dtype_specs.values():
            if dtype == "derivatives":
                continue
            suffixes = dtype_spec.get("suffixes")

            # Skip this part of the schema if no suffixes are found.
            # This is a hack to work around filter_schema's limitations.
            if not len(suffixes):
                continue

            # TODO: <br> is specific for html form
            suffixes_str = " ".join(suffixes) if suffixes else ""
            dtype_row = [dtype] + ([""] * len(all_entities))
            for ent, ent_info in dtype_spec.get("entities", {}).items():
                if isinstance(ent_info, Mapping):
                    requirement_level = ent_info["requirement"]
                else:
                    requirement_level = ent_info

                dtype_row[all_entities.index(ent) + 1] = requirement_level.upper()

            if dtype_row in dtype_rows.values():
                # Merge specs within dtypes if they share all of the same entities
                for existing_suffixes_str, existing_entities in dtype_rows.items():
                    if dtype_row == existing_entities:
                        # Combine suffixes from the existing row with ones from the new row
                        dtype_rows.pop(existing_suffixes_str)
                        old_suffix_list = existing_suffixes_str.split(" ")
                        new_suffix_list = suffixes_str.split(" ")
                        comb_suffix_list = sorted(list(set(new_suffix_list + old_suffix_list)))

                        # Identify if the list of suffixes comes from an existing alternate row
                        number_suffixes = list(filter(str.isnumeric, comb_suffix_list))
                        if len(number_suffixes) == 1:
                            # Suffixes come from an existing alternate row
                            number = number_suffixes[0]
                            comb_suffix_list.remove(number)
                            new_suffixes_str = " ".join(comb_suffix_list)
                            # Retain the old number
                            new_suffixes_str = number + " " + new_suffixes_str
                        elif len(number_suffixes) > 1:
                            # The row exists already, but contains multiple numbers
                            raise Exception("Something's wrong here.")
                        else:
                            # It's a new row
                            new_suffixes_str = " ".join(comb_suffix_list)

                        dtype_rows[new_suffixes_str] = existing_entities
                        break

            elif suffixes_str in dtype_rows.keys():
                # Create new lines for multiple specs with the same dtype and suffix,
                # but different entities
                # Unfortunately, the keys need to be unique, so we include a number
                # NOTE: This assumes that no suffix in BIDS will ever be purely numeric.
                dtype_rows[str(duplicate_row_counter) + " " + suffixes_str] = dtype_row
                duplicate_row_counter += 1

            else:
                # Otherwise, just add the new suffix group
                dtype_rows[suffixes_str] = dtype_row

        # Add datatype to first column and reformat it
        dtype_rows = {dtype + "<br>({})".format(k): v for k, v in dtype_rows.items()}
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

    # Remove fake numeric suffixes from first column
    def _remove_numeric_suffixes(string):
        import re

        suffix_str = re.findall(r"\((.+)\)", string)
        # The "Format" row should be skipped
        if not suffix_str:
            return string

        suffix_str = suffix_str[0]  # Only one parenthesis should appear
        suffixes = suffix_str.split(" ")
        suffixes = list(filter(lambda v: not str.isnumeric(v), suffixes))
        suffix_str2 = " ".join(suffixes)
        new_string = string.replace(f"({suffix_str})", f"({suffix_str2})")
        return new_string

    table[table.index.name] = table.index
    table[table.index.name] = table[table.index.name].apply(_remove_numeric_suffixes)
    table = table.set_index(table.index.name, drop=True)

    # Print it as markdown
    table_str = tabulate(table, headers="keys", tablefmt=tablefmt)
    return table_str


def make_suffix_table(schema, suffixes, src_path=None, tablefmt="github"):
    """Produce suffix table (markdown) based on requested suffixes.

    Parameters
    ----------
    schema : dict
    suffixes : list of str
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : str

    Returns
    -------
    table_str : str
        Tabulated table as a string.
    """
    # The filter function doesn't work here.
    suffix_schema = schema["objects"]["suffixes"]

    all_suffixes = pd.DataFrame.from_records(list(suffix_schema.values()))
    df = all_suffixes[all_suffixes.value.isin(suffixes)][["value", "display_name", "description"]]

    suffixes_not_found = set(suffixes) - set(df.value)
    if suffixes_not_found:
        raise Exception("Warning: Missing suffixes: {}".format(", ".join(suffixes_not_found)))

    def preproc(desc):
        return (
            desc.replace("\\\n", "")  # A backslash before a newline means continue a string
            .replace("\n\n", "<br>")  # Two newlines should be respected
            .replace("\n", " ")  # Otherwise a newline corresponds to a space
            .replace("SPEC_ROOT", get_relpath(src_path))  # Spec internal links need to be replaced
        )

    df.description = df.description.apply(preproc)
    df.columns = ["`suffix`", "**Name**", "**Description**"]
    df = df.reset_index(drop=False)
    df = df.set_index("**Name**")
    df = df[["`suffix`", "**Description**"]]

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    return table_str


def make_obj_table(subschema, field_info, src_path=None, tablefmt="github"):
    # Use the "name" field in the table, to allow for filenames to not match
    # "names".
    df = pd.DataFrame(
        index=[subschema[f]["name"] for f in subschema.keys()],
        columns=["**Requirement Level**", "**Data type**", "**Description**"],
    )
    df.index.name = "**Key name**"
    for field in subschema.keys():
        field_name = subschema[field]["name"]
        requirement_info = field_info[field]
        description_addendum = ""
        if isinstance(requirement_info, tuple):
            requirement_info, description_addendum = requirement_info

        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](/02-common-principles.html#definitions)",
        )

        type_string = utils.resolve_metadata_type(subschema[field])

        description = subschema[field]["description"] + " " + description_addendum

        # Try to add info about valid values
        valid_values_str = utils.describe_valid_values(subschema[field])
        if valid_values_str:
            description += "\n\n\n\n" + valid_values_str

        # A backslash before a newline means continue a string
        description = description.replace("\\\n", "")
        # Two newlines should be respected
        description = description.replace("\n\n", "<br>")
        # Otherwise a newline corresponds to a space
        description = description.replace("\n", " ")
        # Spec internal links need to be replaced
        description = description.replace("SPEC_ROOT", get_relpath(src_path))

        df.loc[field_name] = [requirement_info, type_string, description]

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    return table_str


def make_metadata_table(schema, field_info, src_path=None, tablefmt="github"):
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
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
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

    metadata_schema = {k: v for k, v in metadata_schema.items() if k in retained_fields}

    table_str = make_obj_table(
        metadata_schema,
        field_info=field_info,
        src_path=src_path,
        tablefmt=tablefmt,
    )

    return table_str


def make_subobject_table(schema, object_tuple, field_info, src_path=None, tablefmt="github"):
    """Create a table of properties within an object.

    Parameters
    ----------
    schema
    object_tuple : tuple of strings
        A tuple of keys within the schema linking down to the object
        that will be rendered.
        For example, ("objects", "metadata", "Genetics") will result in a table
        rendering the properties specified in
        schema["object"]["metadata"]["Genetics"].
    field_info : dict of strings or tuples
        A dictionary mapping metadata keys to requirement levels in the
        rendered metadata table.
        The dictionary values may be strings, in which case the string
        is the requirement level information, or two-item tuples of strings,
        in which case the first string is the requirement level information
        and the second string is additional table-specific information
        about the metadata field that will be appended to the field's base
        definition from the schema.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).
    """
    assert isinstance(object_tuple, tuple)
    assert all([isinstance(i, str) for i in object_tuple])

    temp_dict = schema[object_tuple[0]]
    for i in range(1, len(object_tuple)):
        level_str = object_tuple[i]
        temp_dict = temp_dict[level_str]

    temp_dict = temp_dict["properties"]
    assert isinstance(temp_dict, Mapping)
    table_str = make_obj_table(
        temp_dict,
        field_info=field_info,
        src_path=src_path,
        tablefmt=tablefmt,
    )

    return table_str


def make_columns_table(schema, column_info, src_path=None, tablefmt="github"):
    """Produce columns table (markdown) based on requested fields.

    Parameters
    ----------
    schema : dict
        The BIDS schema.
    column_info : dict of strings or tuples
        A dictionary mapping column names to requirement levels in the
        rendered columns table.
        The dictionary values may be strings, in which case the string
        is the requirement level information, or two-item tuples of strings,
        in which case the first string is the requirement level information
        and the second string is additional table-specific information
        about the column that will be appended to the column's base
        definition from the schema.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).

    Returns
    -------
    table_str : str
        The tabulated table as a Markdown string.
    """
    fields = list(column_info.keys())
    # The filter function doesn't work here.
    column_schema = schema["objects"]["columns"]

    retained_fields = [f for f in fields if f in column_schema.keys()]
    dropped_fields = [f for f in fields if f not in column_schema.keys()]
    if dropped_fields:
        print("Warning: Missing fields: {}".format(", ".join(dropped_fields)))

    # Use the "name" field in the table, to allow for filenames to not match
    # "names".
    df = pd.DataFrame(
        index=[column_schema[f]["name"] for f in retained_fields],
        columns=["**Requirement Level**", "**Data type**", "**Description**"],
    )
    df.index.name = "**Column name**"
    for field in retained_fields:
        field_name = column_schema[field]["name"]
        requirement_info = column_info[field]
        description_addendum = ""
        if isinstance(requirement_info, tuple):
            requirement_info, description_addendum = requirement_info

        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](/02-common-principles.html#definitions)",
        )

        type_string = utils.resolve_metadata_type(column_schema[field])

        description = column_schema[field]["description"] + " " + description_addendum

        description = description.replace("SPEC_ROOT", get_relpath(src_path))

        # Try to add info about valid values
        valid_values_str = utils.describe_valid_values(column_schema[field])
        if valid_values_str:
            description += "\n\n\n\n" + valid_values_str

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


def define_common_principles(schema, src_path=None):
    """Enumerate the common principles defined in the schema.

    Parameters
    ----------
    schema : dict
        The BIDS schema.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    string : str
        The definitions of the common principles in a multiline string.
    """
    string = ""
    common_principles = schema["objects"]["common_principles"]
    order = schema["rules"]["common_principles"]
    for i_prin, principle in enumerate(order):
        principle_name = common_principles[principle]["display_name"]
        principle_desc = common_principles[principle]["description"].replace(
            "SPEC_ROOT",
            get_relpath(src_path),
        )
        substring = f"{i_prin + 1}. **{principle_name}** - {principle_desc}"
        string += substring
        if i_prin < len(order) - 1:
            string += "\n\n"

    return string
