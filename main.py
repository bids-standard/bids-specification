import sys


def define_env(env):
    """
    This is the hook for defining variables, macros and filters

    - variables: the dictionary that contains the environment variables
    - macro: a decorator function, to declare a macro.
    """

    @env.macro
    def make_filenames(datatype):
        sys.path.append("tools/")
        from bids_schema import build_filename_format, load_schema
        schema = load_schema("src/schema/")
        codeblock = build_filename_format(schema, datatype=datatype)
        return codeblock
