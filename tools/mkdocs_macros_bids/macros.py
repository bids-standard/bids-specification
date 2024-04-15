"""Functions used by the macros mkdocs plugin."""

import os
import sys

from bidsschematools import render, schema

code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(code_path)

from examplecode import example


def _get_source_path(level=1):
    """Detect the path of the file we are rendering a macro in.

    This (ab)uses the Python call stack to find its way to the Jinja2 function
    that is calling the macro. From there, it looks at Jinja2's Context object,
    which contains all the variables available to the Markdown snippet that is
    calling the macro.

    One variable provided by mkdocs-macros is called ``page``, which includes a
    ``file`` attribute that would allow us to insert the page name into the text
    of the page, or in this case, pass it as a variable. The ``file`` attribute
    has a ``src_path`` attribute of its own that is a path relative to the ``src/``
    directory.

    The level parameter indicates how many steps above the calling function Jinja2
    is. Currently it's always 1, but refactors may justify passing a larger number.

    This allows us to use

    ```{markdown}
    {{ MACRO__make_glossary() }}
    ```

    instead of:

    ```{markdown}
    {{ MACRO__make_glossary(page.file.src_path) }}
    ```

    Why are we doing all this? We need to render links that are defined in the schema
    relative to the source tree as paths relative to the Markdown file they're being
    rendered in. So [SPEC_ROOT/02-common-principles.md](Common principles) becomes
    [./02-common-principles.md](Common principles) or
    [../02-common-principles.md](Common principles), depending on which file it
    appears in.

    If a future maintainer decides that this is terrible, or a bug can't be fixed,
    just go back to explicitly using the ``page.file`` variable throughout the macros.
    """
    import inspect

    # currentframe = _get_source_path()
    # caller = the macro calling this function, e.g. make_glossary()
    caller = inspect.currentframe().f_back
    # We need to go one level higher to find Jinja2
    for _ in range(level):
        caller = caller.f_back
    # Jinja2 equivalent: {{ page.file.src_path }}
    return caller.f_locals["_Context__self"]["page"].file.src_path


def make_filename_template(dstype="raw", src_path=None, pdf_format=False, **kwargs):
    """Generate a filename template snippet from the schema, based on specific filters.

    Parameters
    ----------
    pdf_format : bool, optional
        If True, the filename template will be compiled as a standard markdown code block,
        without any hyperlinks, so that the specification's PDF build will look right.
        If False, the filename template will use HTML and include hyperlinks.
        This works on the website.
        Default is False.

    Other Parameters
    ----------------
    **kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    codeblock : str
        A multiline string containing the filename templates for file types
        in the schema, after filtering.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    codeblock = render.make_filename_template(
        dstype,
        schema_obj,
        src_path=src_path,
        pdf_format=pdf_format,
        **kwargs,
    )
    return codeblock


def make_entity_table(src_path=None, **kwargs):
    """Generate an entity table from the schema, based on specific filters.

    Parameters
    ----------
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Other Parameters
    ----------------
    **kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding entity table for
        a subset of the schema.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_entity_table(schema_obj, src_path=src_path, **kwargs)
    return table


def make_entity_definitions(src_path=None):
    """Generate definitions and other relevant information for entities in the
    specification.

    Parameters
    ----------
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    text = render.make_entity_definitions(schema_obj, src_path=src_path)
    return text


def make_glossary(src_path=None):
    """Generate glossary.

    Parameters
    ----------
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    text : str
        A multiline string containing descriptions and some formatting
        information about the entities in the schema.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    text = render.make_glossary(schema_obj, src_path=src_path)
    return text


def make_suffix_table(suffixes, src_path=None):
    """Generate a markdown table of suffix information.

    Parameters
    ----------
    suffixes : list of str
        A list of the suffixes to include in the table.
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_suffix_table(schema_obj, suffixes, src_path=src_path)
    return table


def make_metadata_table(field_info, src_path=None):
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
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_metadata_table(schema_obj, field_info, src_path=src_path)
    return table


def make_sidecar_table(table_name, src_path=None):
    """Generate a markdown table of metadata field information.

    Parameters
    ----------
    table_name : str or list of str
        Qualified name(s) in schema.rules.sidecars
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_sidecar_table(schema_obj, table_name, src_path=src_path)
    return table


def make_subobject_table(object_name, src_path=None):
    """Generate a markdown table of a metadata object's field information.

    Parameters
    ----------
    object_tuple : tuple of string
        A tuple pointing to the object to render.
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested fields.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_subobject_table(
        schema_obj,
        object_name,
        src_path=src_path,
    )
    return table


def make_columns_table(table_name, src_path=None):
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
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    table : str
        A Markdown-format table containing the corresponding table for
        the requested columns.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    table = render.make_columns_table(schema_obj, table_name, src_path=src_path)
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


def define_common_principles(src_path=None):
    """Enumerate the common principles defined in the schema.

    Parameters
    ----------
    src_path : str or None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.

    Returns
    -------
    string : str
        The definitions of the common principles in a multiline string.
    """
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    string = render.define_common_principles(schema_obj, src_path=src_path)
    return string


def define_allowed_top_directories(src_path=None):
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    string = render.define_allowed_top_directories(schema_obj, src_path=src_path)
    return string


def render_text(key, src_path=None):
    if src_path is None:
        src_path = _get_source_path()

    schema_obj = schema.load_schema()
    string = render.render_text(schema_obj, key, src_path=src_path)
    return string
