"""Utility functions for the bids-specification schema."""
import logging
import math
import os.path as op
from pprint import pprint


def get_schema_path():
    """Get the path to the schema directory.

    Returns
    -------
    str
        Absolute path to the directory containing schema-related files.
    """
    return op.abspath(op.join(op.dirname(__file__), "data", "schema"))


def _link_with_html(string, html_path=None, heading=None, pdf_format=False):
    """Wrap a string in an HTML hyperlink.

    Parameters
    ----------
    string : str
        The string to wrap a hyperlink around.
    html_path : None or str, optional
        Path to the HTML file that the string should link to.
    heading : None or str, optional
        The heading on the HTML page the string should link to.
    pdf_format : bool, optional
        If True, the string will be returned unmodified.
        If False, a hyperlink will be generated around the string,
        linking to the ``heading`` heading in the ``html_path`` page.
        Default is False.

    Returns
    -------
    string : str
        The modified (or unmodified) string.
    """
    if not pdf_format:
        string = string.replace("<", "&lt;").replace(">", "&gt;")
        string = f'<a href="{html_path}#{heading}">{string}</a>'

    return string


def combine_extensions(lst, html_path=None, heading_lst=None, pdf_format=True):
    """Combine extensions with their compressed versions in a list.

    Valid combinations are hardcoded in the function,
    since some extensions look like compressed versions of one another, but are not.

    Parameters
    ----------
    lst : list of str
        Raw list of extensions.
    html_path : None or str
        Path to the HTML file that each extension should link to.
        Only used if pdf_format is False.
        Default is None.
    heading_lst : None or list of str
        List of headings in the HTML page to link to.
        Should be one heading for each extension in lst.
        Only used if pdf_format is False.
        Default is None.
    pdf_format : bool, optional
        If True, the extensions will be compiled as markdown strings,
        without any hyperlinks, so that the specification's PDF build will look right.
        If False, the extensions will use HTML and include hyperlinks to the their
        associated glossary entries.
        This works on the website.
        Default is True.

    Returns
    -------
    new_lst : list of str
        List of extensions, with compressed and uncompressed versions of the same extension
        combined.
    """
    COMPRESSION_EXTENSIONS = [".gz"]
    if pdf_format and not heading_lst:
        heading_lst = lst[:]

    new_lst = []
    items_to_remove = []
    for i_item, item in enumerate(lst):
        for ext in COMPRESSION_EXTENSIONS:
            if item.endswith(ext) and item.replace(ext, "") in lst:
                base_item_idx = lst.index(item.replace(ext, ""))
                temp_item = _link_with_html(
                    lst[base_item_idx],
                    html_path=html_path,
                    heading=heading_lst[base_item_idx].lower(),
                    pdf_format=pdf_format,
                )
                ext_string = _link_with_html(
                    ext,
                    html_path=html_path,
                    heading=heading_lst[i_item].lower(),
                    pdf_format=pdf_format,
                )

                temp_item = temp_item + "[" + ext_string + "]"
                new_lst.append(temp_item)
                items_to_remove.append(item)
                items_to_remove.append(item.replace(ext, ""))
                continue

    heading_lst = [head for i, head in enumerate(heading_lst) if lst[i] not in items_to_remove]
    items_to_add = [item for item in lst if item not in items_to_remove]
    item_strings_to_add = []
    for i_item, item in enumerate(items_to_add):
        item_strings_to_add.append(
            _link_with_html(
                item,
                html_path=html_path,
                heading=heading_lst[i_item],
                pdf_format=pdf_format,
            )
        )

    new_lst += item_strings_to_add

    return new_lst


def get_logger(name=None):
    """Return a logger to use.

    Parameters
    ----------
    name : None or str, optional
        Name of the logger. Defaults to None.

    Returns
    -------
    logging.Logger
        logger object.
    """
    return logging.getLogger("bids-schema" + (".%s" % name if name else ""))


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
        lgr.warning("Do not know how to treat loglevel %s" % level)
        return
    lgr.setLevel(level)


def drop_unused_entities(df):
    """Remove columns from a dataframe where all values in the column are NaNs.

    For entity tables, this limits each table to only entities that are used
    within the modality.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing entities and datatypes/suffixes.
        Rows are datatype/suffix combinations and columns are entities.

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with columns associated with unused entities removed.
    """
    df = df.replace("", math.nan).dropna(axis=1, how="all").fillna("")
    return df


def flatten_multiindexed_columns(df):
    """Remove multi-indexing of multi-indexed column headers.

    The first layer is the "DataType", while the second layer is the "Format".
    This second layer will become a new row.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame with two header levels: "Datatype" and "Format".

    Returns
    -------
    df : pandas.DataFrame
        DataFrame with the second header level ("Format") converted to a
        normal row.
    """
    # Flatten multi-index
    vals = df.index.tolist()
    df.loc["Format"] = df.columns.get_level_values(1)
    df.columns = df.columns.get_level_values(0)
    df = df.loc[["Format"] + vals]
    df.index.name = "Entity"
    df = df.drop(columns=["DataType"])
    return df


def get_link(string):
    refs = {
        "array": "https://www.w3schools.com/js/js_json_arrays.asp",
        "string": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "number": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "object": "https://www.json.org/json-en.html",
        "integer": "https://www.w3schools.com/js/js_json_datatypes.asp",
        "boolean": "https://www.w3schools.com/js/js_json_datatypes.asp",
    }
    # Allow plurals (e.g., strings -> links to string)
    dtype = string[:-1] if string[-1] == "s" else string
    url = refs.get(dtype)
    if url:
        return f"[{string}]({url})"
    return string


def resolve_metadata_type(definition):
    """Generate string of metadata type from dictionary.

    Parameters
    ----------
    definition : :obj:`dict`
        A schema object definition for a metadata term.

    Returns
    -------
    string : :obj:`str`
        A string describing the valid value types for the metadata term.
    """
    if "type" in definition.keys():
        string = get_link(definition["type"])

        if definition.get("enum") == ["n/a"]:
            # Special string case of n/a
            string = '`"n/a"`'

        elif "type" in definition.get("items", {}):
            # Items within arrays
            string += " of " + get_link(definition["items"]["type"] + "s")

        elif "type" in definition.get("additionalProperties", {}):
            # Values within objects
            string += " of " + get_link(definition["additionalProperties"]["type"] + "s")

    elif "anyOf" in definition:
        # Use dictionary to get unique substrings while preserving insertion order
        substrings = {resolve_metadata_type(subdict): None for subdict in definition["anyOf"]}

        string = " or ".join(substrings)

    else:
        # A hack to deal with $ref in the current schema
        print(f"Type could not be inferred for {definition['name']}")
        pprint(definition)
        string = "unknown"

    return string


def describe_valid_values(definition):
    """Build a sentence describing valid values for an object from its definition.

    This only covers booleans, enums, integers, and numbers.
    Currently uncovered are anyOfs, arrays, and objects.

    Parameters
    ----------
    definition : :obj:`dict`
        An object definition, following the BIDS schema object rules.

    Returns
    -------
    :obj:`str`
        A sentence describing valid values for the object.
    """
    description = ""
    if "anyOf" in definition.keys():
        return description

    if definition["type"] == "boolean":
        description = 'Must be one of: `"true"`, `"false"`.'

    elif definition["type"] == "string":
        if "enum" in definition.keys():
            # Allow enums to be "objects" (dicts) or strings
            enum_values = [
                list(v.keys())[0] if isinstance(v, dict) else v for v in definition["enum"]
            ]
            enum_values = [f'`"{v}"`' for v in enum_values]
            description = f"Must be one of: {', '.join(enum_values)}."

    elif definition["type"] in ("integer", "number"):
        if "minimum" in definition.keys():
            minstr = f"greater than or equal to {definition['minimum']}"
        elif "exclusiveMinimum" in definition.keys():
            minstr = f"greater than {definition['exclusiveMinimum']}"
        else:
            minstr = ""

        if "maximum" in definition.keys():
            maxstr = f"less than or equal to {definition['maximum']}"
        elif "exclusiveMaximum" in definition.keys():
            maxstr = f"less than {definition['exclusiveMaximum']}"
        else:
            maxstr = ""

        if minstr and maxstr:
            minmaxstr = f"{minstr} and {maxstr}"
        elif minstr:
            minmaxstr = minstr
        elif maxstr:
            minmaxstr = maxstr
        else:
            minmaxstr = ""

        if minmaxstr:
            description = f"Must be a number {minmaxstr}."
        else:
            description = ""

    return description
