"""Functions for rendering portions of the schema as text."""

from __future__ import annotations

import pandas as pd
from tabulate import tabulate

from bidsschematools.render import utils
from bidsschematools.schema import BIDSSchemaError, Namespace, filter_schema
from bidsschematools.utils import get_logger

lgr = get_logger()

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
    src_path : str or None
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
    first_column = "**Column name**" if table_type == "columns" else "**Key name**"
    df = pd.DataFrame(
        index=field_info.keys(),
        columns=[
            first_column,
            "**Requirement Level**",
            "**Data type**",
            "**Description**",
        ],
    )
    element_type = {
        "metadata": "field",
        "subobject": "subfield",
        "columns": "column",
    }.get(table_type)

    for element, field in subschema.items():
        field_name = field["name"]
        # NOTE: Link to the glossary entry,
        # except for subobjects (if table_type) and
        # "additional columns" (field_name.startswith("**"))
        if table_type and not field_name.startswith("**"):
            sub = table_type if table_type != "subobject" else "metadata"
            field_name = f"[{field_name}]({GLOSSARY_PATH}.md#objects.{sub}.{element})"

        # Grab any requirement level information and text to be added to the description string
        requirement_info, description_addendum = field_info[element]["table_info"]
        requirement_info = utils.normalize_requirements(requirement_info)
        requirement_info = requirement_info.replace(
            "DEPRECATED",
            "[DEPRECATED](SPEC_ROOT/common-principles.md#definitions)",
        )

        type_string = utils.resolve_metadata_type(field)

        description = utils.normalize_requirements(
            f"{field['description']} {description_addendum}".strip()
        )

        # Append a list of valid values, if provided, to the description.
        # If there are a lot of valid values, this will add a link to the description linking to
        # the associated glossary entry.
        levels = subschema[element].get("enum", []) or subschema[element].get(
            "definition", {}
        ).get("Levels", [])
        if len(levels) >= n_values_to_combine:
            glossary_entry = f"{GLOSSARY_PATH}.md#objects.{table_type}.{element}"
            valid_values_str = (
                f"For a list of valid values for this {element_type}, see the "
                f"[associated glossary entry]({glossary_entry})."
            )
        else:
            # Try to add info about valid values
            valid_values_str = utils.describe_valid_values(subschema[element])

        if valid_values_str:
            description += "\n\n\n\n" + valid_values_str

        # Add entry to DataFrame
        df.loc[element] = [
            field_name,
            utils.normalize_breaks(requirement_info),
            type_string,
            utils.normalize_breaks(description),
        ]

    df = df.set_index(first_column, drop=True)
    df.index.name = first_column

    # Print it as markdown
    table_str = tabulate(df, headers="keys", tablefmt=tablefmt)

    # Spec internal links need to be replaced
    table_str = table_str.replace("SPEC_ROOT", utils.get_relpath(src_path))

    return table_str


def _make_table_from_rule(
    schema: Namespace,
    table_type: str,
    table_name: str | list[str],
    src_path: str | None = None,
    tablefmt: str = "github",
):
    """Create a table for one or more rules.

    If ``table_type`` is "columns", only one table may be provided.

    Parameters
    ----------
    schema : Namespace
        The BIDS schema.
    table_type : {"metadata", "columns"}
        The type of table. Either "metadata" or "columns".
    table_name : str or list of str
        Qualified name(s) in schema.rules.tabular_data (for "columns" tables) or
        schema.rules.sidecars (for "metadata" files).
        Only one item may be provided for columns tables.
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).

    Returns
    -------
    table_str : str
        The tabulated table as a Markdown string.
    """
    if isinstance(table_name, str):
        table_name = [table_name]

    elements: dict[str, str | dict[str, str]] = {}
    for table in table_name:
        if table_type == "metadata":
            table_schema = schema.rules[table]
            new_elements = table_schema.fields
        elif table_type == "columns":
            table_schema = schema.rules.tabular_data[table]
            new_elements = table_schema.columns
            # Since only one table may be provided for columns, we can just use this directly.
            additional_columns = table_schema.get("additional_columns", "not_allowed")
            initial_columns = table_schema.get("initial_columns", [])
            index_columns = table_schema.get("index_columns", [])
        else:
            raise ValueError(f"Unsupported 'table_type': '{table_type}'")

        overlap = set(new_elements) & set(elements)
        if overlap:
            raise BIDSSchemaError(
                f"Schema tables {table_name} share overlapping fields: {overlap}"
            )
        elements.update(new_elements)

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

        if table_type == "columns" and element in index_columns:
            if len(index_columns) == 1:
                msg = f"Values in `{schema.objects.columns[element].name}`"
            else:
                cols = [f"`{schema.objects.columns[col].name}`" for col in index_columns]
                msg = f"The combination of {', '.join(cols[:-1])} and {cols[-1]}"
            description_addendum += f"\n\n\n\n{msg} MUST be unique."

        if table_type == "columns" and initial_columns:
            if element in initial_columns:
                order = initial_columns.index(element) + 1
                order_str = utils.num2words(order, to="ordinal")
                description_addendum += (
                    f"\n\n\n\nThis column must appear **{order_str}** in the file."
                )
            else:
                description_addendum += "\n\n\n\nThis column may appear anywhere in the file."

        element_info[element] = {"table_info": (level, description_addendum)}

    if table_type == "columns":
        # Add info about additional columns to table.
        # its_complicated won't add any info about additional columns.
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
        elif additional_columns == "allowed":
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
    schema : str
        Directory containing schema, which is stored in yaml files.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table_str : str
        Markdown string containing the table.
    """
    schema = Namespace(filter_schema(schema.to_dict(), **kwargs))

    # prepare the table based on the schema
    header = ["Entity"]
    formats = ["Format"]
    table = [formats]

    suffix_map = {obj.value: key for key, obj in schema.objects.suffixes.items()}

    # Compose header and formats first
    for long_name in schema.rules.entities:
        entity = schema.objects.entities[long_name]
        header.append(entity.display_name)
        formats.append(f"[`{entity.name}-<{entity.format}>`]({ENTITIES_PATH}.md#{entity.name})")

    rows = {}
    for rule in schema.rules.files.raw.values(level=2):
        suffixes = rule.get("suffixes")
        if not suffixes:
            continue

        entities = []
        for ent in schema.rules.entities:
            val = rule.entities.get(ent, "")
            entities.append((ent, val if isinstance(val, str) else val["level"]))

        for dtype in rule.datatypes:
            row = rows.setdefault((dtype, tuple(entities)), [])
            row.extend(suffixes)

    for (dtype, entities), suffixes in rows.items():
        suf_str = " ".join(
            f"[{suffix}]({GLOSSARY_PATH}.md#objects.suffixes.{suffix_map[suffix]})"
            for suffix in suffixes
        )
        # TODO: <br> is specific for html form
        fmt_str = f"[{dtype}]({GLOSSARY_PATH}.md#objects.datatypes.{dtype})<br>({suf_str})"
        table.append([fmt_str] + [level.upper() for ent, level in entities])

    # Create multi-level index because first two rows are headers
    cols = list(zip(header, table[0]))
    cols = pd.MultiIndex.from_tuples(cols)
    table = pd.DataFrame(data=table[1:], columns=cols)
    table = table.set_index(("Entity", "Format"))

    # Remove unnecessary columns
    table = utils.drop_unused_entities(table)
    table = utils.flatten_multiindexed_columns(table)

    table[table.index.name] = table.index
    table = table.set_index(table.index.name, drop=True).sort_index()

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
    src_path : str or None
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


def make_json_table(
    schema: Namespace,
    table_name: str | list[str],
    src_path: str | None = None,
    tablefmt: str = "github",
):
    """Produce metadata table (markdown) based on requested fields.

    Parameters
    ----------
    schema : Namespace
        The BIDS schema.
    table_name : str or list of str
        Qualified name(s) in schema.rules.sidecars
    src_path : str or None
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


def make_sidecar_table(
    schema: Namespace,
    table_name: str | list[str],
    src_path: str | None = None,
    tablefmt: str = "github",
):
    """Produce metadata table (markdown) based on requested fields.

    Parameters
    ----------
    schema : Namespace
        The BIDS schema.
    table_name : str or list of str
        Qualified name(s) in schema.rules.sidecars
    src_path : str or None
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
        table_name=[
            f"sidecars.{table}"
            for table in ([table_name] if isinstance(table_name, str) else table_name)
        ],
        src_path=src_path,
        tablefmt=tablefmt,
    )

    return table_str


def make_metadata_table(schema, field_info, src_path=None, tablefmt="github"):
    """Produce metadata table (markdown) based on requested fields.

    Parameters
    ----------
    schema : Namespace
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
    src_path : str or None
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


def make_subobject_table(
    schema: Namespace,
    object_name: str,
    src_path: str | None = None,
    tablefmt: str = "github",
):
    """Create a metadata table (markdown) based on the properties of an object

    Parameters
    ----------
    schema : Namespace
        The BIDS schema.
    object_name : str
        Qualified name in schema.objects
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    tablefmt : string, optional
        The target table format. The default is "github" (GitHub format).

    Returns
    -------
    table_str : str
        The tabulated table as a Markdown string.
    """
    obj = schema.objects[object_name]
    required_fields = set(obj.get("required", ()))
    recommended_fields = set(obj.get("recommended", ()))

    field_info = {}
    for field in obj.properties:
        if field in required_fields:
            req_level = "required"
        elif field in recommended_fields:
            req_level = "recommended"
        else:
            req_level = "optional"
        field_info[field] = {"table_info": (req_level, "")}

    table_str = _make_object_table(
        obj.properties,
        field_info=field_info,
        table_type="subobject",
        src_path=src_path,
        tablefmt=tablefmt,
        n_values_to_combine=10000,  # no combination
    )

    return table_str


def make_columns_table(
    schema: Namespace,
    table_name: str,
    src_path: str | None = None,
    tablefmt: str = "github",
):
    """Produce columns table (markdown) based on requested fields.

    Parameters
    ----------
    schema : Namespace
        The BIDS schema.
    table_name : str
        Qualified name in schema.rules.tabular_data.
        Only one table may be provided in this function.
    src_path : str or None
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
