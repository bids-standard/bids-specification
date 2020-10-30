"""Functions used by the macros mkdocs plugin.
"""
from . import schema, utils


def make_filename_template(**kwargs):
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    codeblock = schema.make_filename_template(schema_obj, **kwargs)
    return codeblock


def make_entity_table(**kwargs):
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    table = schema.make_entity_table(schema_obj, **kwargs)
    return table


def make_entity_definitions():
    schemapath = utils.get_schema_path()
    schema_obj = schema.load_schema(schemapath)
    text = schema.make_entity_definitions(schema_obj)
    return text
