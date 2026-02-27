We would like to rework our metaschema (src/metaschema.json) into linkml.  That metaschema describes our "BIDS schema" which is arranged through yaml files under src/schema. src/schema/README.md provides more description about schema organization etc.

Note that some constructs such as objects.metadata and objects.columns have types described in jsonschema.
Compiled schema (could be done via `uv run bst export` which outputs to stdout) should be validated with the converted metaschema.

We would like to make it more "classy" as to define classes with linkml which would nicely translate into OOP e.g. in Python.
So then we could generate Python dataclasses to be used by `tools/schemacode/` python packages.
From linkml we would like also to generate TypeScript classes, for which an experimental branch (jsr-dist) was developed so check it out as well (e.g. in a worktree under .worktrees)

We still want to use new metaschema in linkml to validate our BIDS schema located under src/schema which is compiled into src/schema.json.
If you need "sources" of linkml, its git repos are also available locally under /home/yoh/proj/misc/linkml .

# Discoveries after round 1

Looking at state at v1.11.1-18-g1320e864f and diagram at http://127.0.0.1:8000/en/stable/schema/class_diagram.html

(We will use D{round}.{index} for identifiers)

### D1.1 DataProperties

It feels that we need a construct (class?) to define smth like "DataProperties"  (propose better name) to define

   - minimum: float
   - maximum: float
   - unit: str

  which defined at metaschema level and in principle can be used to hardcode in scheme associating with some suffixes e.g

    ❯ show-paths -e unit: -f full-lines src/schema/objects/suffixes.yaml
    18  Chimap:
    28:   unit: ppm
    ...

    ❯ show-paths -e 'max' -f full-lines src/schema/objects/suffixes.yaml
    144  MTRmap:
    155:   maxValue: 100
    ...

  to describe associated data file (e.g. nii.gz) properties and then could be hardcoded for some .tsv columns

    ❯ show-paths -e '(unit|max.*):' -f full-lines src/schema/objects/columns.yaml
    ...
    311  low_cutoff:
    318:   unit: Hz
    ...
    353  metabolite_polar_fraction:
    360:   maximum: 1
    418:   unit: s
    ...

  and then could be provided in the actual datasets for columns in corresponding .json for .tsv files; and for data in data sidecar .json files:

    ❯ show-paths -e 'maxim' -f full-lines src/schema/objects/metadata.yaml
    ...
    2214  LabelingPulseFlipAngle:
    2222:   maximum: 360

