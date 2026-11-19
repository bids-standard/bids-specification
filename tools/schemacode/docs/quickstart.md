---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

# BIDS Schema Tools Quick Start

The `bidsschematools` package is a Python package that is bundled with the [BIDS specification](https://github.com/bids-standard/bids-specification/) in order to render the components of the specification document from the BIDS schema.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
import bidsschematools as bst
import bidsschematools.schema
```

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: skip
tags: [hide-cell, remove-input]
---
# Hidden cell to import useful tools
import os
from upath import UPath
from pprint import pprint
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

## Schema loading

Schemas are loaded with the `load_schema()` function. The default schema is the one that is bundled as part of the package:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
schema = bst.schema.load_schema()
```

+++ {"editable": true, "slideshow": {"slide_type": "subslide"}}

In the BIDS repository, the schema source is a subdirectory of YAML documents that need to be compiled before they can be used. Passing such a directory into `load_schema()` will perform the compilation:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
# Build from local repository, or else set `BIDS_SPEC_REPO` environment variable
spec = UPath(os.getenv('BIDS_SPEC_REPO', UPath(os.getcwd()).parent.parent.parent))
schema_from_directory = bst.schema.load_schema(spec / 'src' / 'schema')
```

+++ {"editable": true, "slideshow": {"slide_type": "subslide"}}

`load_schema()` can also load a precompiled JSON schema document, such as can be found at <https://bids-specification.readthedocs.io/en/latest/schema.json>.

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
schema_path = UPath('https://bids-specification.readthedocs.io/en/latest/schema.json')
schema_from_json = bst.schema.load_schema(schema_path)
```

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

## Schema organization

The schema has three top-level subdivisions (`objects`, `rules`, and `meta`) and also contains its own version and the version of the BIDS standard that it encodes:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
print(list(schema.keys()))
print(f'BIDS-Schema version: {schema.schema_version}')
print(f'BIDS version: {schema.bids_version}')
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

Note that the schema provided by `load_schema()` is a [Namespace](#bidsschematools.types.namespace.Namespace) object, which is able to access fields with dot notation (`schema.bids_version`) as well as index notation (`schema['bids_version'])`.

+++ {"editable": true, "slideshow": {"slide_type": "subslide"}}

We can see the general structure of the schema by listing keys at the second level:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
list(schema.keys(level=2))
```

```{code-cell} ipython3
schema['meta.associations']
```

+++ {"editable": true, "slideshow": {"slide_type": "fragment"}}

The `objects` subschema contains definitions of data and metadata used throughout BIDS, while the `rules` subschema contains definitions of constraints that may be validated. `meta` contains definitions that are essential for validation.

+++ {"editable": true, "slideshow": {"slide_type": "subslide"}}

To see how these sections interact, consider `rules.files.raw.func.func`, which contains the valid entities, datatypes, extensions and suffixes for functional neuroimaging files:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
pprint(schema.rules.files.raw.func.func.to_dict())
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

We can look up the suffix definitions in `objects.suffixes`:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
pprint({
    suffix: schema.objects.suffixes[suffix].to_dict()
    for suffix in schema.rules.files.raw.func.func.suffixes
})
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

Note that suffixes are duplicated in the `value` field. Because suffixes are valid identifiers, this generally does not cause problems, and `objects.suffixes[suffix]` is a shorthand lookup.

+++ {"editable": true, "slideshow": {"slide_type": "subslide"}}

This isn't true in all fields, for example, in extensions:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
schema.objects.extensions.nii_gz
```

+++ {"editable": true, "slideshow": {"slide_type": ""}}

In this case, a lookup table needs to be built on the fly:

```{code-cell} ipython3
---
editable: true
slideshow:
  slide_type: ''
---
ext_lookup = {ext.value: ext for ext in schema.objects.extensions.values()}
pprint({
    ext: ext_lookup[ext].to_dict()
    for ext in schema.rules.files.raw.func.func.extensions
})
```
