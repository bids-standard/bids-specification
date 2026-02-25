We would like to rework our metaschema (src/metaschema.json) into linkml.  That metaschema describes our "BIDS schema" which is arranged through yaml files under src/schema. src/schema/README.md provides more description about schema organization etc.

Note that some constructs such as objects.metadata and objects.columns have types described in jsonschema.
Compiled schema (could be done via `uv run bst export` which outputs to stdout) should be validated with the converted metaschema.

We would like to make it more "classy" as to define classes with linkml which would nicely translate into OOP e.g. in Python.
So then we could generate Python dataclasses to be used by `tools/schemacode/` python packages.
From linkml we would like also to generate TypeScript classes, for which an experimental branch (jsr-dist) was developed so check it out as well (e.g. in a worktree under .worktrees)

We still want to use new metaschema in linkml to validate our BIDS schema located under src/schema which is compiled into src/schema.json.
If you need "sources" of linkml, its git repos are also available locally under /home/yoh/proj/misc/linkml .
