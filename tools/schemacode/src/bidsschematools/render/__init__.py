"""Functions for rendering elements of the schema in the specification text."""

from bidsschematools.render.tables import (
    make_columns_table,
    make_entity_table,
    make_json_table,
    make_metadata_table,
    make_sidecar_table,
    make_subobject_table,
    make_suffix_table,
)
from bidsschematools.render.text import (
    define_allowed_top_directories,
    define_common_principles,
    make_entity_definitions,
    make_filename_template,
    make_glossary,
    render_text,
)

__all__ = [
    "make_entity_table",
    "make_suffix_table",
    "make_json_table",
    "make_sidecar_table",
    "make_metadata_table",
    "make_subobject_table",
    "make_columns_table",
    "make_entity_definitions",
    "make_glossary",
    "make_filename_template",
    "define_common_principles",
    "define_allowed_top_directories",
    "render_text",
]
