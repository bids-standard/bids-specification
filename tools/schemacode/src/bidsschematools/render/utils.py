"""Utility functions for specification rendering tools."""

import math
import posixpath
import re
from functools import cache, wraps

import pandas as pd

from ..utils import in_context


def _pandas_3_0():
    """Silence pandas warnings and opt in to future behavior.

    This sets pandas behavior to 3.0+ defaults.
    Prior to pandas 3.0, the fillna() and replace() methods would convert
    object columns to float64 if the resulting series was all float64.
    In 3.0+, you need to use infer_objects() to do this.

    This also opts-in to copy-on-write, which previously required `copy=False`
    to be set.
    """
    if args := _pandas_3_0_options():
        return pd.option_context(*args)

    import contextlib

    return contextlib.nullcontext()


@cache
def _pandas_3_0_options():
    options = [
        ("future.no_silent_downcasting", True),
        ("mode.copy_on_write", True),
    ]

    args = []
    for option in options:
        try:
            pd.get_option(option[0])
        except KeyError:
            continue
        args.extend(option)
    return args


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


@in_context(_pandas_3_0())
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
    return df.replace("", math.nan).dropna(axis=1, how="all").fillna("")


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
    return df


def get_link(string):
    """Return a hyperlink to the JSON specification for a given JSON type.

    Parameters
    ----------
    string : str
        The JSON type to link to.

    Returns
    -------
    url : str
        The hyperlink to the JSON specification for the given JSON type.
    """
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
    string : str
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

    elif "definition" in definition:
        json_def = definition["definition"]

        if "Delimiter" in json_def:
            # Delimiter indicates the value must be parsed. For BIDS purposes,
            # this is a string, even if the parsed array is of numbers.
            string = "string"
        elif "Levels" in json_def:
            # JSON keys are always strings.
            string = "string"
        elif "Units" in json_def:
            # Values with units are always (any exceptions?) numbers.
            string = "number"
        else:
            string = "string or number"
    else:
        # This clause should only catch $refs.
        # The schema should be deferenced by this point, so $refs should not exist.
        raise ValueError(f"Type could not be inferred for {definition['name']}")

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
    str : A sentence describing valid values for the object.
    """
    description = ""
    if "anyOf" in definition:
        return description

    if "definition" in definition:
        levels = definition["definition"].get("Levels")
        if levels:
            description = (
                f"Unless redefined in a sidecar file, must be one of: {', '.join(levels)}."
            )
        return description

    if definition["type"] == "boolean":
        description = 'Must be one of: `"true"`, `"false"`.'

    elif definition["type"] == "string":
        if "enum" in definition.keys():
            # Allow enums to be "objects" (dicts) or strings
            enums = [list(v.keys())[0] if isinstance(v, dict) else v for v in definition["enum"]]
            enums = [f'`"{v}"`' for v in enums]
            description = f"Must be one of: {', '.join(enums)}."

    elif definition["type"] in ("integer", "number"):
        minstr = maxstr = minmaxstr = ""

        if "minimum" in definition.keys():
            minstr = f"greater than or equal to {definition['minimum']}"
        elif "exclusiveMinimum" in definition.keys():
            minstr = f"greater than {definition['exclusiveMinimum']}"

        if "maximum" in definition.keys():
            maxstr = f"less than or equal to {definition['maximum']}"
        elif "exclusiveMaximum" in definition.keys():
            maxstr = f"less than {definition['exclusiveMaximum']}"

        if minstr and maxstr:
            minmaxstr = f"{minstr} and {maxstr}"
        elif minstr or maxstr:
            minmaxstr = minstr + maxstr

        if minmaxstr:
            description = f"Must be a number {minmaxstr}."

    return description


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


def normalize_requirements(text):
    """Normalize requirements wording in a string.

    Parameters
    ----------
    text : str

    Returns
    -------
    text : str
    """
    return re.sub(
        r"\b(optional|recommended|required|deprecated)\b",
        lambda m: m.group(1).upper(),
        text,
        flags=re.IGNORECASE,
    )


def normalize_breaks(text):
    """Normalize line breaks in a string, for new lines, escaped new lines and double new lines.

    Parameters
    ----------
    text : str

    Returns
    -------
    text : str
    """
    # A backslash before a newline means continue a string
    text = text.replace("\\\n", "")
    # Two newlines should be respected
    text = text.replace("\n\n", "<br>")
    # Otherwise a newline corresponds to a space
    return text.replace("\n", " ")


def num2words(integer, to="ordinal"):
    """Convert integers to words.

    This is a very simplistic mapping of numbers to words,
    to avoid adding num2words to our requirements.
    It only works with the first few numbers.

    Parameters
    ----------
    integer : int
    to : {"ordinal", "cardinal"}, optional

    Returns
    -------
    word : str
    """
    if to == "ordinal":
        mapper = {
            1: "first",
            2: "second",
            3: "third",
            4: "fourth",
            5: "fifth",
            6: "sixth",
            7: "seventh",
            8: "eighth",
            9: "ninth",
            10: "tenth",
        }
    elif to == "cardinal":
        mapper = {
            1: "one",
            2: "two",
            3: "three",
            4: "four",
            5: "five",
            6: "six",
            7: "seven",
            8: "eight",
            9: "nine",
            10: "ten",
        }

    try:
        return mapper[integer]
    except KeyError:
        raise ValueError(f"Input {integer} is not supported.")


def propagate_fence_exception(func):
    """Decorator to prevent superfences from swallowing exceptions."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            from pymdownx.superfences import SuperFencesException

            raise SuperFencesException from e

    return wrapper
