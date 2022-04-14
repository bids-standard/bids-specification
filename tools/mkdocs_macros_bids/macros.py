"""Functions used by the macros mkdocs plugin."""
import os
import sys

from schemacode import render, schema, utils

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from examplecode import example


def make_filename_template(**kwargs):
    """Generate a filename template snippet from the schema, based on specific
    filters.

    Parameters
    ----------
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
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    codeblock = render.make_filename_template(schema_obj, **kwargs)
    return codeblock


def make_entity_table(**kwargs):
    """Generate an entity table from the schema, based on specific filters.

    Parameters
    ----------
    kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding entity table for
        a subset of the schema.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_entity_table(schema_obj, **kwargs)
    return table


def make_entity_definitions():
    """Generate definitions and other relevant information for entities in the
    specification.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    text = render.make_entity_definitions(schema_obj)
    return text


def make_glossary():
    """Generate glossary.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    text = render.make_glossary(schema_obj)
    return text


def make_suffix_table(suffixes):
    """Generate a markdown table of suffix information.

    Parameters
    ----------
    suffixes : list of str
        A list of the suffixes to include in the table.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_suffix_table(schema_obj, suffixes)
    return table


def make_metadata_table(field_info):
    """Generate a markdown table of metadata field information.

    Parameters
    ----------
    field_names : dict
        A list of the field names.
        Field names correspond to filenames in the "metadata" directory of the
        schema.
        Until requirement levels can be codified in the schema,
        this argument will be dictionary, with the field names as keys and
        the requirement levels as values.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_metadata_table(schema_obj, field_info)
    return table


def make_columns_table(column_info):
    """Generate a markdown table of TSV column information.

    Parameters
    ----------
    column_info : dict
        A list of the column names.
        Column names correspond to filenames in the "columns" directory of the
        schema.
        Until requirement levels can be codified in the schema,
        this argument will be a dictionary, with the column names as keys and
        the requirement levels as values.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested columns.
    """
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = render.make_columns_table(schema_obj, column_info)
    return table


def make_filetree_example(filetree_info, use_pipe=True):
    """Generate a filetree snippet from example content.

    Parameters
    ----------
    filetree_info : dict
        Dictionary to represent the directory content.
    use_pipe : bool
        Set to ``False`` to avoid using pdf unfriendly pipes: "│ └─ ├─"

    Returns
    -------
    tree : str
        A multiline string containing the filetree example.
    """
    tree = example.DirectoryTree(filetree_info, use_pipe)
    return tree.generate()
