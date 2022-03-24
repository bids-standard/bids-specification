"""Generate the Glossary appendix file."""
import os.path as op

import mkdocs_gen_files

from schemacode import render, schema, utils

out_file = op.abspath("src/99-appendices/14-glossary.md")

output = """# Appendix XIV: Glossary of schema objects

This section compiles the object definitions in the schema.

"""

schemapath = utils.get_schema_path()
schema_obj = schema.load_schema(schemapath)
text = render.make_glossary(schema_obj)
output += text

with mkdocs_gen_files.open(out_file, "w") as fobj:
    fobj.write(output)

mkdocs_gen_files.set_edit_path(out_file, "tools/generate_glossary.py")
