"""
This package is used to build elements in the bids-specification schema into
MarkDown format for the specification text.

Functions decorated in "define_env()" are callable throughout the
specification and are run/rendered with the mkdocs plugin "macros".
"""
import sys
sys.path.append("tools/")
from schemacode import macros


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """
    env.macro(macros.make_filename_template, 'make_filename_template')
    env.macro(macros.make_entity_table, 'make_entity_table')
    env.macro(macros.make_entity_definitions, 'make_entity_definitions')

    @env.macro
    def make_metadata_table():
        return None

    @env.macro
    def make_suffix_table(suffixes):
        return None
