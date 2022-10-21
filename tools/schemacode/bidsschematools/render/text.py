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
    "columns": "column",
    "common_principles": "common principle",
    "datatypes": "datatype",
    "entities": "entity",
    "extensions": "extension",
    "files": "files and directories",
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
    # Skip underscore on first entity
    if filename_template:
        entity_pattern = f"_{entity_pattern}"
    if requirement_level != "required":
        entity_pattern = f"[{entity_pattern}]"
    return filename_template + entity_pattern


def _format_entity(entity, lt, gt):
    fmt = entity.get("format")
    if "enum" in entity:
        fmt = "|".join(entity["enum"])
    if fmt is None:
        raise ValueError(f"entity missing format or enum fields: {entity}")
    return f"{entity['name']}-{lt}{fmt}{gt}"


def value_key_table(namespace):
    return {struct.value: key for key, struct in namespace.items()}


def make_filename_template(
    dstype,
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
    dstype : "raw" or "deriv"
        The type of files being rendered; determines if rules are found in rules.files.raw
        or rules.files.deriv
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

    if pdf_format:
        lt, gt = "<", ">"
    else:
        lt, gt = "&lt;", "&gt;"

    schema = Namespace(filter_schema(schema.to_dict(), **kwargs))
    suffix_key_table = value_key_table(schema.objects.suffixes)
    ext_key_table = value_key_table(schema.objects.extensions)

    # Parent directories
    sub_string = utils._link_with_html(
        _format_entity(schema.objects.entities.subject, lt, gt),
        html_path=ENTITIES_PATH + ".html",
        heading="sub",
        pdf_format=pdf_format,
    )
    ses_string = utils._link_with_html(
        _format_entity(schema.objects.entities.session, lt, gt),
        html_path=ENTITIES_PATH + ".html",
        heading="ses",
        pdf_format=pdf_format,
    )
    lines = [f"{sub_string}/", f"\t[{ses_string}/]"]

    file_rules = schema.rules.files[dstype]
    file_groups = {}
    for rule in file_rules.values(level=2):
        for datatype in rule.datatypes:
            file_groups.setdefault(datatype, []).append(rule)

    for datatype in sorted(file_groups):
        datatype_string = utils._link_with_html(
            datatype,
            html_path=GLOSSARY_PATH + ".html",
            heading=f"{datatype.lower()}-datatypes",
            pdf_format=pdf_format,
        )
        lines.append(f"\t\t{datatype_string}/")

        # Unique filename patterns
        for group in file_groups[datatype]:
            ent_string = ""
            for ent in schema.rules.entities:
                if ent not in group.entities:
                    continue

                # Add level and any overrides to entity
                ent_obj = group.entities[ent]
                if isinstance(ent_obj, str):
                    ent_obj = {"level": ent_obj}
                entity = {**schema.objects.entities[ent], **ent_obj}

                if "enum" in entity:
                    # Link full entity
                    pattern = utils._link_with_html(
                        _format_entity(entity, lt, gt),
                        html_path=f"{ENTITIES_PATH}.html",
                        heading=entity["name"],
                        pdf_format=pdf_format,
                    )
                else:
                    # Link entity and format separately
                    entity["name"] = utils._link_with_html(
                        entity["name"],
                        html_path=f"{ENTITIES_PATH}.html",
                        heading=entity["name"],
                        pdf_format=pdf_format,
                    )
                    entity["format"] = utils._link_with_html(
                        entity.get("format", "label"),
                        html_path=f"{ENTITIES_PATH}.html",
                        heading=entity.get("format", "label"),
                        pdf_format=pdf_format,
                    )
                    pattern = _format_entity(entity, lt, gt)

                ent_string = _add_entity(ent_string, pattern, entity["level"])

            # In cases of large numbers of suffixes,
            # we use the "suffix" variable and expect a table later in the spec
            if len(group["suffixes"]) >= n_dupes_to_combine:
                suffixes = [
                    lt
                    + utils._link_with_html(
                        "suffix",
                        html_path=GLOSSARY_PATH + ".html",
                        heading="suffix-common_principles",
                        pdf_format=pdf_format,
                    )
                    + gt
                ]
            else:
                suffixes = [
                    utils._link_with_html(
                        suffix,
                        html_path=GLOSSARY_PATH + ".html",
                        heading=f"{suffix_key_table[suffix].lower()}-suffixes",
                        pdf_format=pdf_format,
                    )
                    for suffix in group.suffixes
                ]

            # Add extensions
            extensions = [ext if ext != "*" else ".<extension>" for ext in group.extensions]
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
                key = ext_key_table.get(extension)
                if key:
                    ext_headings.append(f"{key.lower()}-extensions")
                else:
                    ext_headings.append("extension-common_principles")

            extensions = utils.combine_extensions(
                extensions,
                html_path=GLOSSARY_PATH + ".html",
                heading_lst=ext_headings,
                pdf_format=pdf_format,
            )

            lines.extend(
                f"\t\t\t{ent_string}_{suffix}{extension}"
                for suffix in sorted(suffixes)
                for extension in sorted(extensions)
            )

    paragraph = "\n".join(lines)
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
- Filename entities or directories between square brackets
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


def define_allowed_top_directories(schema, src_path=None) -> str:
    """Create a list of allowed top-level directories with their descriptions.

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
        Unordered list describing top level directories.
    """

    string = ""

    for dirname, definition in schema.objects.files.items():
        if definition.file_type == "directory":
            string += f"- `{dirname}`: {definition.description}"

    return string.replace("SPEC_ROOT", utils.get_relpath(src_path))
