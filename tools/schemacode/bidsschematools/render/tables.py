"""Functions for rendering portions of the schema as text."""
import logging
import os
import typing as ty
from collections.abc import Mapping

import pandas as pd
from tabulate import tabulate

from bidsschematools.render import utils
from bidsschematools.schema import BIDSSchemaError, Namespace, filter_schema
from bidsschematools.utils import get_logger, set_logger_level

lgr = get_logger()
# Basic settings for output, for now just basic
set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
logging.basicConfig(format="%(asctime)-15s [%(levelname)8s] %(message)s")

# Remember to add extension (.html or .md) to the paths when using them.
ENTITIES_PATH = "SPEC_ROOT/appendices/entities"
GLOSSARY_PATH = "SPEC_ROOT/glossary"


def _make_object_table(
    subschema,
    field_info,
    table_type=None,
    src_path=None,
    tablefmt="github",
    n_values_to_combine=15,
):
    """Make a generic table describing objects in the schema.

    This does shared work between describing metadata fields and subobjects in the schema.

    Parameters
    ----------
    subschema : Namespace or dict
        Subset of the overall schema, including only the target object definitions.
    field_info : dict
        Additional information about each row in the table to be added to schema information.
        Keys should match "name" entries in ``subschema``.
        Values should be either a string (in which case, it's requirement information) or
        a tuple (in which case, the first entry is requirement info and the second is
        information to be added to the object's description).
    table_type : str
        The name of the field type. For example, "metadata".
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).
    n_values_to_combine : int, optional
        When there are many valid values for a given object,
        instead of listing each one in the table,
        link to the associated glossary entry.
    """
    # Use the "name" field in the table, to allow for filenames to not match "names".
    df = pd.DataFrame(
        index=field_info.keys(),
        columns=["**Key name**", "**Requirement Level**", "**Data type**", "**Description**"],
    )
    for field in subschema.keys():
        field_name = subschema[field]["name"]
        # NOTE: Link to the glossary entry,
        # except for subobjects (if table_type) and
        # "additional columns" (field_name.startswith("**"))
        if table_type and not field_name.startswith("**"):
            field_name = f"[{field_name}]({GLOSSARY_PATH}.md#objects.{table_type}.{field})"

        # Grab any requirement level information and text to be added to the description string
        requirement_info, description_addendum = field_info[field]["table_info"]
        requirement_info = utils.normalize_requirements(requirement_info)
        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](/02-common-principles.html#definitions)",
        )

        type_string = utils.resolve_metadata_type(subschema[field])

        description = utils.normalize_requirements(
            subschema[field]["description"] + " " + description_addendum
        )

        # Append a list of valid values, if provided, to the description.
        # If there are a lot of valid values, this will add a link to the description linking to
        # the associated glossary entry.
        if (
            "enum" in subschema[field].keys()
            and len(subschema[field]["enum"]) >= n_values_to_combine
        ):
            glossary_entry = f"{GLOSSARY_PATH}.md#objects.{table_type}.{field}"
            valid_values_str = (
                "For a list of valid values for this field, see the "
                f"[associated glossary entry]({glossary_entry})."
            )
        else:
            # Try to add info about valid values
            valid_values_str = utils.describe_valid_values(subschema[field])

        if valid_values_str:
            description += "\n\n\n\n" + valid_values_str

        # Add entry to DataFrame
        df.loc[field] = [
            field_name,
            utils.normalize_breaks(requirement_info),
            type_string,
            utils.normalize_breaks(description),
        ]

    df = df.set_index("**Key name**", drop=True)
    df.index.name = "**Key name**"

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)

    # Spec internal links need to be replaced
    table_str = table_str.replace("SPEC_ROOT", utils.get_relpath(src_path))

    return table_str


def _make_table_from_rule(
    schema: Namespace,
    table_type: str,
    table_name: ty.Union[str, ty.List[str]],
    src_path: ty.Optional[str] = None,
    tablefmt: str = "github",
):
    """Create a table for one or more rules."""
    if isinstance(table_name, str):
        table_name = [table_name]

    elements = {}
    additional_columns = []
    for table in table_name:
        if table_type == "metadata":
            table_schema = schema.rules.sidecars[table]
            new_elements = table_schema.fields
        elif table_type == "columns":
            table_schema = schema.rules.tabular_data[table]
            new_elements = table_schema.columns
            additional_columns.append(table_schema.get("additional_columns", "not_allowed"))
        else:
            raise ValueError(f"Unsupported 'table_type': '{table_type}'")

        overlap = set(new_elements) & set(elements)
        if overlap:
            raise BIDSSchemaError(
                f"Schema tables {table_name} share overlapping fields: {overlap}"
            )
        elements.update(new_elements)

    if table_type == "columns":
        if len(set(additional_columns)) > 1:
            print(
                "Warning: Conflicting additional column information: "
                f"{', '.join(additional_columns)}."
            )
            additional_columns = "its_complicated"
        else:
            additional_columns = additional_columns[0]

    subschema = schema.objects[table_type]
    retained_elements = [f for f in elements if f in subschema]
    dropped_elements = [f for f in elements if f not in subschema]
    if dropped_elements:
        print("Warning: Missing elements: {}".format(", ".join(dropped_elements)))

    subschema = {k: v for k, v in subschema.items() if k in retained_elements}
    element_info = {}
    for element, val in elements.items():
        if isinstance(val, str):
            level = val
            level_addendum = ""
            description_addendum = ""
        else:
            level = val["level"]
            level_addendum = val.get("level_addendum", "")
            description_addendum = val.get("description_addendum", "")

        if level_addendum:
            if level_addendum.startswith(("required", "recommended", "optional")):
                level = f"{level}, but {level_addendum}"
            else:
                # Typically begins with "if"
                level = f"{level} {level_addendum}"

        element_info[element] = {"table_info": (level, description_addendum)}

    if table_type == "columns":
        if additional_columns == "not_allowed":
            element_info["Additional Columns"] = {
                "table_info": ("NOT ALLOWED", "Additional columns are not allowed.")
            }
        elif additional_columns == "allowed_if_defined":
            element_info["Additional Columns"] = {
                "table_info": (
                    "OPTIONAL",
                    (
                        "Additional columns are allowed if they are defined in the associated "
                        "metadata file."
                    ),
                )
            }
        else:
            element_info["Additional Columns"] = {
                "table_info": ("OPTIONAL", "Additional columns are allowed.")
            }

        subschema.update(
            {
                "Additional Columns": {
                    "name": "**Additional Columns**",
                    "description": "",
                    "type": "`n/a`",
                }
            }
        )

    table_str = _make_object_table(
        subschema,
        field_info=element_info,
        table_type=table_type,
        src_path=src_path,
        tablefmt=tablefmt,
    )
    return table_str


def make_entity_table(schema, tablefmt="github", src_path=None, **kwargs):
    """Produce entity table (markdown) based on schema.

    Parameters
    ----------
    schema_path : str
        Directory containing schema, which is stored in yaml files.
    entities_file : str, optional
        File in which entities are described.
        This is used for hyperlinks in the table, so the path to the file
        should be considered from the location of out_file.
        Default is 'entities.md'.

    Returns
    -------
    table_str : str
        Markdown string containing the table.
    """
    schema = Namespace(filter_schema(schema.to_dict(), **kwargs))

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
            f"({ENTITIES_PATH}.md#{entity_shorthand})"
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
            suffixes = [
                f"[{suffix}]({GLOSSARY_PATH}.md#objects.suffixes.{suffix})" for suffix in suffixes
            ]
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
        dtype_rows = {
            f"[{dtype}]({GLOSSARY_PATH}.md#objects.datatypes.{dtype})<br>({k})": v
            for k, v in dtype_rows.items()
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
    table_str = table_str.replace("SPEC_ROOT", utils.get_relpath(src_path))
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
    table_type = "suffixes"

    # The filter function doesn't work here.
    subschema = schema["objects"][table_type]

    all_suffixes = pd.DataFrame.from_dict(subschema, orient="index")
    df = all_suffixes[all_suffixes.value.isin(suffixes)]
    df = df.reset_index(drop=False)

    suffixes_not_found = set(suffixes) - set(df.value)
    if suffixes_not_found:
        raise Exception("Warning: Missing suffixes: {}".format(", ".join(suffixes_not_found)))

    def preproc_desc(desc):
        return (
            desc.replace("\\\n", "")  # A backslash before a newline means continue a string
            .replace("\n\n", "<br>")  # Two newlines should be respected
            .replace("\n", " ")  # Otherwise a newline corresponds to a space
        )

    def preproc_suffix(row):
        return f"[{row['value']}]({GLOSSARY_PATH}.md#objects.{table_type}.{row['index']})"

    df.description = df.description.apply(preproc_desc)
    df["suffix"] = df.apply(preproc_suffix, axis=1)
    df = df[["suffix", "display_name", "description"]]
    df.columns = ["`suffix`", "**Name**", "**Description**"]
    df = df.reset_index(drop=False)
    df = df.set_index("**Name**")
    df = df[["`suffix`", "**Description**"]]

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    # Spec internal links need to be replaced
    table_str = table_str.replace("SPEC_ROOT", utils.get_relpath(src_path))
    return table_str


def make_sidecar_table(
    schema: Namespace,
    table_name: ty.Union[str, ty.List[str]],
    src_path: ty.Optional[str] = None,
    tablefmt: str = "github",
):
    """Produce metadata table (markdown) based on requested fields.

    Parameters
    ----------
    schema : dict
        The BIDS schema.
    table_name : str or list of str
        Qualified name(s) in schema.rules.sidecars
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
    table_str = _make_table_from_rule(
        schema=schema,
        table_type="metadata",
        table_name=table_name,
        src_path=src_path,
        tablefmt=tablefmt,
    )

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
    table_type = "metadata"
    subschema = schema["objects"][table_type]

    retained_fields = [f for f in fields if f in subschema.keys()]
    dropped_fields = [f for f in fields if f not in subschema.keys()]
    if dropped_fields:
        print("Warning: Missing fields: {}".format(", ".join(dropped_fields)))

    subschema = {k: v for k, v in subschema.items() if k in retained_fields}
    # inverted_schema = {v["name"]: k for k, v in subschema.items()}

    # Reformat the field info (requirement level and description addendum)
    field_info_2 = {}
    for field, val in field_info.items():
        if isinstance(val, tuple):
            field_info_2[field] = {"table_info": val}
        else:
            field_info_2[field] = {"table_info": (val, "")}

    table_str = _make_object_table(
        subschema,
        field_info=field_info_2,
        table_type=table_type,
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

    # Reformat the field info (requirement level and description addendum)
    field_info_2 = {}
    for field, val in field_info.items():
        if isinstance(val, tuple):
            field_info_2[field] = {"table_info": val}
        else:
            field_info_2[field] = {"table_info": (val, "")}

    temp_dict = schema[object_tuple[0]]
    for i in range(1, len(object_tuple)):
        level_str = object_tuple[i]
        temp_dict = temp_dict[level_str]

    temp_dict = temp_dict["properties"]
    assert isinstance(temp_dict, Mapping)
    table_str = _make_object_table(
        temp_dict,
        field_info=field_info_2,
        table_type="subobject",
        src_path=src_path,
        tablefmt=tablefmt,
        n_values_to_combine=10000,  # no combination
    )

    return table_str


def make_columns_table(
    schema,
    column_info,
    src_path=None,
    tablefmt="github",
    n_values_to_combine=15,
):
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
    n_values_to_combine : int, optional
        When there are many valid values for a given column,
        instead of listing each one in the table,
        link to the associated glossary entry.

    Returns
    -------
    table_str : str
        The tabulated table as a Markdown string.
    """
    src_path = utils.get_relpath(src_path)
    fields = list(column_info.keys())
    # The filter function doesn't work here.
    table_type = "columns"
    subschema = schema["objects"][table_type]

    retained_fields = [f for f in fields if f in subschema.keys()]
    dropped_fields = [f for f in fields if f not in subschema.keys()]
    if dropped_fields:
        print("Warning: Missing fields: {}".format(", ".join(dropped_fields)))

    # Use the "name" field in the table, to allow for filenames to not match
    # "names".
    df = pd.DataFrame(
        index=retained_fields,
        columns=["**Column name**", "**Requirement Level**", "**Data type**", "**Description**"],
    )
    for field in retained_fields:
        field_name = subschema[field]["name"]
        requirement_info = column_info[field]
        description_addendum = ""
        if isinstance(requirement_info, tuple):
            requirement_info, description_addendum = requirement_info

        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](SPEC_ROOT/02-common-principles.html#definitions)",
        )
        field_name = f"[{field_name}]({GLOSSARY_PATH}.md#objects.columns.{field})"

        type_string = utils.resolve_metadata_type(subschema[field])

        description = subschema[field]["description"] + " " + description_addendum

        if (
            "enum" in subschema[field].keys()
            and len(subschema[field]["enum"]) >= n_values_to_combine
        ):
            glossary_entry = f"{GLOSSARY_PATH}.md#objects.{table_type}.{field}"
            valid_values_str = (
                "For a list of valid values for this field, see the "
                f"[associated glossary entry]({glossary_entry})."
            )
        else:
            # Try to add info about valid values
            valid_values_str = utils.describe_valid_values(subschema[field])

        if valid_values_str:
            description += "\n\n\n\n" + valid_values_str

        df.loc[field] = [
            field_name,
            utils.normalize_breaks(requirement_info),
            type_string,
            utils.normalize_breaks(description),
        ]

    df = df.set_index("**Column name**", drop=True)
    df.index.name = "**Column name**"

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)
    table_str = table_str.replace("SPEC_ROOT", src_path)
    return table_str


def make_columns_table_2(
    schema: Namespace,
    table_name: ty.Union[str, ty.List[str]],
    src_path: ty.Optional[str] = None,
    tablefmt: str = "github",
):
    """Produce columns table (markdown) based on requested fields.

    Parameters
    ----------
    schema : dict
        The BIDS schema.
    table_name : str or list of str
        Qualified name(s) in schema.rules.tabular_data
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
    table_str = _make_table_from_rule(
        schema=schema,
        table_type="columns",
        table_name=table_name,
        src_path=src_path,
        tablefmt=tablefmt,
    )

    return table_str
