"""Functions for rendering portions of the schema as text."""
import logging
import os

import yaml
from markdown_it import MarkdownIt

from bidsschematools.render import utils
from bidsschematools.schema import Namespace, filter_schema, load_schema
from bidsschematools.utils import get_logger, set_logger_level

lgr = get_logger()
# Basic settings for output, for now just basic
set_logger_level(lgr, os.environ.get("BIDS_SCHEMA_LOG_LEVEL", logging.INFO))
logging.basicConfig(format="%(asctime)-15s [%(levelname)8s] %(message)s")

# Remember to add extension (.html or .md) to the paths when using them.
ENTITIES_PATH = "SPEC_ROOT/appendices/entities"
GLOSSARY_PATH = "SPEC_ROOT/glossary"
TYPE_CONVERTER = {
    "associated_data": "associated data",
    "columns": "column",
    "common_principles": "common principle",
    "datatypes": "datatype",
    "entities": "entity",
    "extensions": "extension",
    "formats": "format",
    "metadata": "metadata",
    "top_level_files": "top level file",
    "suffixes": "suffix",
}


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
        entity_text = _make_entity_definition(entity, entity_info)
        text += "\n" + entity_text

    text = text.replace("SPEC_ROOT", utils.get_relpath(src_path))
    return text


def _make_entity_definition(entity, entity_info):
    """Describe an entity."""
    entity_shorthand = entity_info["name"]
    text = ""
    text += "## {}".format(entity_shorthand)
    text += "\n\n"
    text += f"**Full name**: {entity_info['display_name']}"
    text += "\n\n"
    text += f"**Format**: `{entity_info['name']}-<{entity_info.get('format', 'label')}>`"
    text += "\n\n"
    if "enum" in entity_info.keys():
        text += f"**Allowed values**: `{'`, `'.join(entity_info['enum'])}`"
        text += "\n\n"

    description = entity_info["description"]
    text += f"**Definition**: {description}"
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
    schema = schema.to_dict()

    for group, group_objects in schema["objects"].items():
        group_obj_keys = list(group_objects.keys())

        # Do not include private objects in the glossary
        group_obj_keys = [k for k in group_obj_keys if not k.startswith("_")]

        # Identify multi-sense objects (multiple entries, indicated by __ in key)
        multi_sense_objects = []
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
            all_objects[new_name]["type"] = TYPE_CONVERTER.get(group, group)
            all_objects[new_name]["definition"] = group_objects[key]

    text = ""
    for obj_key in sorted(all_objects.keys()):
        obj = all_objects[obj_key]
        obj_marker = obj["key"]
        obj_def = obj["definition"]

        # Clean up the text description
        obj_desc = obj_def["description"]
        # A backslash before a newline means continue a string
        obj_desc = obj_desc.replace("\\\n", "")
        # Two newlines should be respected
        obj_desc = obj_desc.replace("\n\n", "<br>")
        # Otherwise a newline corresponds to a space
        obj_desc = obj_desc.replace("\n", " ")

        text += f'\n<a name="{obj_marker}"></a>'
        text += f"\n## {obj_key}\n\n"
        text += f"**Name**: {obj_def['display_name']}\n\n"
        text += f"**Type**: {obj['type'].title()}\n\n"

        if obj["type"] == "suffix":
            text += f"**Format**: `<entities>_{obj_def['value']}.<extension>`\n\n"
        elif obj["type"] == "extension":
            text += f"**Format**: `<entities>_<suffix>{obj_def['value']}`\n\n"
        elif obj["type"] == "format":
            text += f"**Regular expression**: `{obj_def['pattern']}`\n\n"

        if "enum" in obj_def.keys():
            allowed_vals = [f"`{enum}`" for enum in obj_def["enum"]]
            text += f"**Allowed values**: {', '.join(allowed_vals)}\n\n"

        text += f"**Description**:\n{obj_desc}\n\n"

        temp_obj_def = {
            k: v
            for k, v in obj_def.items()
            if k not in ("description", "display_name", "name", "value", "enum", "pattern")
        }

        if temp_obj_def:
            temp_obj_def = yaml.dump(temp_obj_def)
            text += f"**Schema information**:\n```yaml\n{temp_obj_def}\n```"

    # Spec internal links need to be replaced
    text = text.replace("SPEC_ROOT", utils.get_relpath(src_path))

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


def make_filename_template(
    schema=None,
    src_path=None,
    n_dupes_to_combine=6,
    pdf_format=False,
    **kwargs,
):
    """Create codeblocks containing example filename patterns for a given datatype.

    By default, this function uses HTML, instead of direct Markdown codeblocks,
    so that it can embed hyperlinks within the filenames.

    Parameters
    ----------
    schema : dict
        The schema object, which is a dictionary with nested dictionaries and
        lists stored within it.
    src_path : str | None
        The file where this macro is called, which may be explicitly provided
        by the "page.file.src_path" variable.
    n_dupes_to_combine : int
        The minimum number of suffixes/extensions to combine in the template as
        <suffix>/<extension>.
    pdf_format : bool, optional
        If True, the filename template will be compiled as a standard markdown code block,
        without any hyperlinks, so that the specification's PDF build will look right.
        If False, the filename template will use HTML and include hyperlinks.
        This works on the website.
        Default is False.
    kwargs : dict
        Keyword arguments used to filter the schema.
        Example kwargs that may be used include: "suffixes", "datatypes",
        "extensions".

    Returns
    -------
    codeblock : str
        A multiline string containing the filename templates for file types
        in the schema, after filtering.

    Notes
    -----
    This function links to HTML files, rather than markdown files.
    """
    if not schema:
        schema = load_schema()

    schema = Namespace(filter_schema(schema.to_dict(), **kwargs))
    entity_order = schema["rules"]["entities"]

    paragraph = ""
    # Parent directories
    sub_string = (
        f'{schema["objects"]["entities"]["subject"]["name"]}-'
        f'<{schema["objects"]["entities"]["subject"]["format"]}>'
    )
    paragraph += utils._link_with_html(
        sub_string,
        html_path=ENTITIES_PATH + ".html",
        heading="sub",
        pdf_format=pdf_format,
    )
    paragraph += "/\n\t["
    ses_string = (
        f'{schema["objects"]["entities"]["session"]["name"]}-'
        f'<{schema["objects"]["entities"]["session"]["format"]}>'
    )
    paragraph += utils._link_with_html(
        ses_string,
        html_path=ENTITIES_PATH + ".html",
        heading="ses",
        pdf_format=pdf_format,
    )
    paragraph += "/]\n"

    datatypes = schema.rules.datatypes

    for datatype in datatypes:
        # NOTE: We should have a full rethink of the schema hierarchy
        # so that derivatives aren't treated like a "datatype"
        if datatype == "derivatives":
            continue

        paragraph += "\t\t"
        paragraph += utils._link_with_html(
            datatype,
            html_path=GLOSSARY_PATH + ".html",
            heading=f"{datatype.lower()}-datatypes",
            pdf_format=pdf_format,
        )
        paragraph += "/\n"

        # Unique filename patterns
        for group in datatypes[datatype].values():
            string = "\t\t\t"
            for ent in entity_order:
                if "enum" in schema["objects"]["entities"][ent].keys():
                    # Entity key-value pattern with specific allowed values
                    ent_format = (
                        f'{schema["objects"]["entities"][ent]["name"]}-'
                        f'<{"|".join(schema["objects"]["entities"][ent]["enum"])}>'
                    )
                    ent_format = utils._link_with_html(
                        ent_format,
                        html_path=ENTITIES_PATH + ".html",
                        heading=schema["objects"]["entities"][ent]["name"],
                        pdf_format=pdf_format,
                    )
                else:
                    # Standard entity key-value pattern with simple label/index
                    ent_format = utils._link_with_html(
                        schema["objects"]["entities"][ent]["name"],
                        html_path=ENTITIES_PATH + ".html",
                        heading=schema["objects"]["entities"][ent]["name"],
                        pdf_format=pdf_format,
                    )
                    ent_format += "-"
                    ent_format += "<" if pdf_format else "&lt;"
                    ent_format += utils._link_with_html(
                        schema["objects"]["entities"][ent].get("format", "label"),
                        html_path=GLOSSARY_PATH + ".html",
                        heading=(
                            f'{schema["objects"]["entities"][ent].get("format", "label")}-formats'
                        ),
                        pdf_format=pdf_format,
                    )
                    ent_format += ">" if pdf_format else "&gt;"

                if ent in group["entities"]:
                    if isinstance(group["entities"][ent], dict):
                        if "enum" in group["entities"][ent].keys():
                            # Overwrite the filename pattern using valid values
                            ent_format = "{}-&lt;{}&gt;".format(
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
                string += "_"
                string += "<" if pdf_format else "&lt;"
                string += utils._link_with_html(
                    "suffix",
                    html_path=GLOSSARY_PATH + ".html",
                    heading="suffix-common_principles",
                    pdf_format=pdf_format,
                )
                string += ">" if pdf_format else "&gt;"
                strings = [string]
            else:
                strings = []
                for suffix in group["suffixes"]:
                    # The glossary indexes by the suffix identifier (TwoPE instead of 2PE),
                    # but the rules reference the actual suffix string (2PE instead of TwoPE),
                    # so we need to look it up.
                    suffix_id = [
                        k for k, v in schema["objects"]["suffixes"].items() if v["value"] == suffix
                    ][0]

                    suffix_string = utils._link_with_html(
                        suffix,
                        html_path=GLOSSARY_PATH + ".html",
                        heading=f"{suffix_id.lower()}-suffixes",
                        pdf_format=pdf_format,
                    )
                    strings.append(f"{string}_{suffix_string}")

            # Add extensions
            full_strings = []
            extensions = group["extensions"]
            extensions = [ext if ext != "*" else ".<extension>" for ext in extensions]
            if len(extensions) >= n_dupes_to_combine:
                # Combine exts when there are many, but keep JSON separate
                if ".json" in extensions:
                    extensions = [".<extension>", ".json"]
                else:
                    extensions = [".<extension>"]

            ext_headings = []
            for extension in extensions:
                # The glossary indexes by the extension identifier (niigz instead of .nii.gz),
                # but the rules reference the actual suffix string (.nii.gz instead of niigz),
                # so we need to look it up.
                ext_id = [
                    k
                    for k, v in schema["objects"]["extensions"].items()
                    if v["value"] == extension
                ]
                if ext_id:
                    ext_id = ext_id[0]
                    ext_headings.append(f"{ext_id.lower()}-extensions")
                else:
                    ext_headings.append("extension-common_principles")

            extensions = utils.combine_extensions(
                extensions,
                html_path=GLOSSARY_PATH + ".html",
                heading_lst=ext_headings,
                pdf_format=pdf_format,
            )

            for extension in extensions:
                for string in strings:
                    new_string = f"{string}{extension}"
                    full_strings.append(new_string)

            full_strings = sorted(full_strings)
            if full_strings:
                paragraph += "\n".join(full_strings) + "\n"

    paragraph = paragraph.rstrip()
    if pdf_format:
        codeblock = f"Template:\n```Text\n{paragraph}\n```"
    else:
        codeblock = (
            f'Template:\n<div class="highlight"><pre><code>{paragraph}\n</code></pre></div>'
        )

    codeblock = codeblock.expandtabs(4)
    codeblock = append_filename_template_legend(codeblock, pdf_format)
    codeblock = codeblock.replace("SPEC_ROOT", utils.get_relpath(src_path))

    return codeblock


def append_filename_template_legend(text, pdf_format=False):
    """Append a legend to filename templates."""
    if pdf_format:
        info_str = ""
    else:
        info_str = """
- For more information about filename elements (for example, entities, suffixes, extensions),
  follow the links embedded in the filename template.
  """

    legend = f"""{info_str}
- Filename entities or folders between square brackets
  (for example, `[_ses-<label>]`) are OPTIONAL.
- Some entities may only allow specific values,
  in which case those values are listed in `<>`, separated by `|`.
- `_<suffix>` means that there are several (>6) valid suffixes for this filename pattern.
- `.<extension>` means that there are several (>6) valid extensions for this file type.
- `[.gz]` means that both the unzipped and gzipped versions of the extension are valid.
"""

    if pdf_format:
        text += f"""

**Legend**:

{legend}

"""
    else:
        md = MarkdownIt()
        text += f"""
<details>
<summary><strong>Legend:</strong></summary>
{md.render(legend)}
</details>
"""

    return text


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
        substring = (
            f"{i_prin + 1}. **{principle_name}** - {common_principles[principle]['description']}"
        )
        string += substring
        if i_prin < len(order) - 1:
            string += "\n\n"

    string = string.replace("SPEC_ROOT", utils.get_relpath(src_path))

    return string
