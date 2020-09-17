"""
This package is used to build elements in the bids-specification schema into
MarkDown format for the specification text.

Functions decorated in "define_env()" are callable throughout the
specification and are run/rendered with the mkdocs plugin "macros".
"""
import sys
sys.path.append(".")
from schemacode import schema, utils


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    env.variables['schemapath'] = utils.get_schema_path()

    def make_filename_template(datatypes):
        schema_path = utils.get_schema_path()
        schema_obj = schema.load_schema(schema_path)
        codeblock = schema.build_filename_format(
            schema_obj,
            datatypes=datatypes
        )
        return codeblock
    env.macro(make_filename_template)

    def make_entity_table(datatypes):
        schema_path = utils.get_schema_path()
        schema_obj = schema.load_schema(schema_path)
        table = schema.make_entity_table(schema_obj, datatypes=datatypes)
        return table
    env.macro(make_entity_table)

    def make_metadata_table():
        return None
    env.macro(make_metadata_table)

    def make_suffix_table(suffixes):
        return None
    env.macro(make_suffix_table)
