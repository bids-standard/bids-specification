# Using MkDocs macros in the BIDS specification

We use [mkdocs-macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)
to standardize how some aspects of the BIDS specification are rendered in HTML.
Macros make it easy to achieve a consistent style throughout the specification,
and changing a given macro will automatically change all appropriate paragraphs
in the specification.

Below you will find answers to frequently asked questions regarding using macros
in the BIDS specification.

- [Using MkDocs macros in the BIDS specification](#using-mkdocs-macros-in-the-bids-specification)
   - [What are macros and why use them?](#what-are-macros-and-why-use-them)
   - [What kind of input information are required by macros?](#what-kind-of-input-information-are-required-by-macros)
   - [What macros are available?](#what-macros-are-available)
   - [When should I use a macro?](#when-should-i-use-a-macro)
   - [Do I need learn how to program to use those macros?](#do-i-need-learn-how-to-program-to-use-those-macros)
   - [Anything else I need to know if I need to insert a new macro call?](#anything-else-i-need-to-know-if-i-need-to-insert-a-new-macro-call)
   - [How-To and Examples](#how-to-and-examples)
      - [Writing directory content examples](#writing-directory-content-examples)
      - [Generating tables](#generating-tables)
         - [Modifying a term in the table](#modifying-a-term-in-the-table)
         - [Why would you NOT want to modify the content of the yml file directly ?](#why-would-you-not-want-to-modify-the-content-of-the-yml-file-directly-)
         - [Adding a new term to the table](#adding-a-new-term-to-the-table)
         - [Should I create a macro if I need a new kind of table?](#should-i-create-a-macro-if-i-need-a-new-kind-of-table)
   - [Why use macros at all?](#why-use-macros-at-all)
   - [Links and references](#links-and-references)

## What are macros and why use them?

A macro is a rule or pattern that specifies how an input should be mapped to
output. Macros are very useful for standardizing the output format for items
such as tables. You might already be familiar with using macros from other tools
such as Excel.

MkDocs (the tool we use to turn the markdown version of the BIDS specification
into HTML pages) supports macros. In the specification document, we use these
macros to standardize the format of items such as tables and examples.

The following is an example of a macro used to create consistent "file tree"
layouts in the documentation. The macro takes a single parameter, the directory
tree to be displayed in JSON format. If you insert the following in the BIDS
markdown document:

```python
{{ MACROS___make_filetree_example(

   {
   "sub-01": {
      "func": {
         "sub-control01_task-nback_bold.json": "",
         },
      }
   }

) }}
```

The result would be rendered in the specification document as:

```bash
└─ sub-01/
   └─ func/
      └─ sub-control01_task-nback_bold.json
```

## What kind of input information are required by macros?

Some macros only use the arguments you directly supply in the macro call.

Other macros use information (such as metadata terms) from external sources, and
you will need to provide links to this information as part of the call. For
example, parts of the BIDS specification are formalized into a "schema" so that
requirements in the specification can be automatically checked by validators.
Several of the macros incorporate information from this schema to assure
consistency.

## What macros are available?

All the macros we use are in listed in this
[python file](https://github.com/bids-standard/bids-specification/blob/master/tools/mkdocs_macros_bids/macros.py).

| Name                    | Purpose                                                                                | Uses schema | Example                                                                                                                                                                                     |
| ----------------------- | -------------------------------------------------------------------------------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| make_columns_table      | Generate a markdown table of TSV column information.                                   | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/03-modality-agnostic-files.md?plain=1#L202)                                    |
| make_entity_table       | Generate an entity table from the schema, based on specific filters.                   | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/99-appendices/04-entity-table.md?plain=1#L23)                                  |
| make_entity_definitions | Generate definitions and other relevant information for entities in the specification. | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/99-appendices/09-entities.md?plain=1#L16)                                      |
| make_filename_template  | Generate a filename template from the schema, based on specific filters.               | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/04-modality-specific-files/10-microscopy.md?plain=1#L21)                       |
| make_filetree_example   | Generate a filetree snippet from example content.                                      | No          | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/02-common-principles.md?plain=1#L268)                                          |
| make_glossary           |                                                                                        | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/99-appendices/14-glossary.md?plain=1#L9)                                       |
| make_metadata_table     | Generate a markdown table of metadata field information.                               | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/02-common-principles.md?plain=1#L462)                                          |
| make_suffix_table       | Generate a markdown table of suffix information.                                       | Yes         | [link](https://github.com/bids-standard/bids-specification/blob/9201b203ffaa72d83b2fa30d1c61f46f089f77de/src/04-modality-specific-files/01-magnetic-resonance-imaging-data.md?plain=1#L199) |

## When should I use a macro?

Most typo corrections and minor changes to the BIDS specification do not require
you to use macros. Even adding a table may not require you to use macros unless
the table falls into one of the categories listed in the macros table.

If you want to add content with a macro and need help, do not hesitate to
contact a member of the bids-maintainers for help. To do this, you can either
mention an individual maintainer by their GitHub username or mention the whole
team (`@bids-standard/maintainers`).

## Do I need learn how to program to use those macros?

Macros don't require programming knowledge to use. You do need to know what
arguments the macro expects. The examples linked in the above table provide
useful guidance in this respect.

Macros that extract information from the schema also require you to use the
correct terms in the schema. This process is illustrated in the next section.

Note that under the hood the macros themselves call python code that can be
found in the
[`tools` directory](https://github.com/bids-standard/bids-specification/tree/master/tools).
If you are interested in creating a new macro for users, this would be useful.

## Anything else I need to know if I need to insert a new macro call?

One nice thing for the people who will come after you (or yourself in 6 months
when you get back to the document you just edited) is to leave a comment before
the macro to quickly explain what it does and where to find more information
about it.

<!-- - [ ] TODO for maintainers: actually add those comments in the current
      specification. -->

It could for example look like this:

```markdown
<!--
This block generates a metadata table.
The definitions of these fields can be found in src/schema/...
and a guide for editing at <link>.
-->

{{ MACROS\_\_\_make_metadata_table( { "AcquisitionMode": "REQUIRED",
"MoonPhase": "OPTIONAL", "ImageDecayCorrected": "REQUIRED",
"ImageDecayCorrectionTime": "REQUIRED",

      ...

} ) }}
```

## How-To and Examples

### Writing directory content examples

One of the simplest macro we use helps us create consistent "file tree" examples
that would look like this in the final document:

```Text
└─ sub-01/
   └─ func/
      └─ sub-control01_task-nback_bold.json
```

To do this get this output, your macro call would look like this:

```
{{ MACROS___make_filetree_example(

   {
   "sub-01": {
      "func": {
         "sub-control01_task-nback_bold.json": "",
         },
      }
   }

) }}
```

When you have complex files and directory structure, we suggest you use this
[Jupyter notebook](tools/filetree_example.ipynb) for sandboxing your example
before you insert the macro call into the markdown document.

### Generating tables

Say you want to edit the content of table of the `Reconstruction` section for
the PET page.

The HTML version of the this section is here:

https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/09-positron-emission-tomography.html#reconstruction

In the markdown document, it is here:

https://github.com/bids-standard/bids-specification/blob/master/src/04-modality-specific-files/09-positron-emission-tomography.md#reconstruction

GitHub's way of directly rendering markdown documents makes it a bit harder to
read, so if you opened the markdown document in your code editor it would look
like this.

```markdown
#### Reconstruction

{{ MACROS___make_metadata_table(
   {
      "AcquisitionMode": "REQUIRED",
      "ImageDecayCorrected": "REQUIRED",
      "ImageDecayCorrectionTime": "REQUIRED",
      "ReconMethodName": "REQUIRED",
      "ReconMethodParameterLabels": "REQUIRED",
      "ReconMethodParameterUnits": "REQUIRED",
      "ReconMethodParameterValues": "REQUIRED",
      "ReconFilterType": "REQUIRED",
      "ReconFilterSize": "REQUIRED",
      "AttenuationCorrection": "REQUIRED",
      "ReconMethodImplementationVersion": "RECOMMENDED",
      "AttenuationCorrectionMethodReference": "RECOMMENDED",
      "ScaleFactor": "RECOMMENDED",
      "ScatterFraction": "RECOMMENDED",
      "DecayCorrectionFactor": "RECOMMENDED",
      "DoseCalibrationFactor": "RECOMMENDED",
      "PromptRate": "RECOMMENDED",
      "RandomRate": "RECOMMENDED",
      "SinglesRate": "RECOMMENDED",
   }
) }}
```

---

**HINT:** if you want to see the "raw" content of a file on Github you can
always press the `raw` button that is on the top right of the document you are
browsing on Github.

---

This section calls the macro `make_metadata_table` to create the table when
building the HTML version of that page.

The macro will create the different columns of the table:

- Key name
- Requirement level
- Data type
- Description

A general description of that macro call would look like this:

```python
{{ MACROS___make_metadata_table(
   {
      "TermToRender": "REQUIREMENT_LEVEL plus anything else after", "Extra content you want to append after the description of that term."
   }
) }}
```

To know what to put in the different columns, the macro will go and look into
the
[`metadata.yaml`](https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/metadata.yaml)
file in the BIDS schema and find the entry that correspond to the term you want
to add.

And in the above example, all the information about `AcquisitionMode` would be
read from
[that section](https://github.com/bids-standard/bids-specification/blob/master/src/schema/objects/metadata.yaml#L20).

If you had to write the markdown equivalent of the general example for the macro
call above it would give a table that would look like this:

| Key name     | Requirement level                          | Data type | Description                                  |
| ------------ | ------------------------------------------ | --------- | -------------------------------------------- |
| TermToRender | REQUIREMENT_LEVEL plus anything else after | string    | whatever description was in the metadata.yml |

#### Modifying a term in the table

So if you want to change the content of what will appear in the HTML table, you
need to edit this `metadata.yml` file.

If you wanted to add some extra content to that table, but without modifying the
definition in the schema, then you could just add some extra content into the
macro call.

```python
#### Reconstruction

{{ MACROS___make_metadata_table(
   {
      "AcquisitionMode": "REQUIRED", "But only when the acquisition was done on a full moon."

       ...
```

#### Why would you NOT want to modify the content of the yml file directly ?

Well the same term can be used in different parts of the BIDS specification and
some details that might apply to, say, PET might not apply to how the term is
used for MRI. So we can use the schema for the common part and add extra content
where necessary in the macro call.

So always better to check if that term is not used somewhere else before making
a change in the yml file. When in doubt add the change directly in the macro
call and ask the BIDS maintainers for help.

#### Adding a new term to the table

Say you wanted to add a new term `MoonPhase` to the table, on the second row.
You would do it like this. But this would only work if the `metadata.yml` file
contains an entry for `MoonPhase`. If this is the case because the term already
exists and is used somewhere in the BIDS specification, you are in luck and you
can just stop there.

```python
#### Reconstruction

{{ MACROS___make_metadata_table(
   {
      "AcquisitionMode": "REQUIRED",
      "MoonPhase": "OPTIONAL",
      "ImageDecayCorrected": "REQUIRED",
      "ImageDecayCorrectionTime": "REQUIRED",

      ...

   }
) }}
```

If the term does not exist, you need to add it. `YML` files have a fairly strict
syntax where spaces and indentation matter a lot. You can a mini intro to YML
files in the Turing way:
https://the-turing-way.netlify.app/reproducible-research/renv/renv-yaml.html

In practice, you should try to use a code editor that tells you when your syntax
is wrong.

#### Should I create a macro if I need a new kind of table?

As a rule of thumb, no, unless it is clear that this kind of table will reappear
many times in the future in the specification. But this is usually hard to
predict so better start with a table in Markdown.

If later we see that the same type of table keeps reoccuring the specification
we could create a macro to generate them.

## Why use macros at all?

> Seriously why did you have to make it so complicated just to have pretty
> tables? Are macros that necessary ? Couldn't we just have everything in
> Markdown?

In principle we could, and before we started working on the schema that's
exactly what we did. But there are several good reasons to use macros.

When a definition gets repeated in different places, we could just copy-paste
it. But when you start having several copies of that definition, if you have to
modify it, you then need to edit several files and never forget any of them. So
this becomes very error prone.

So it becomes better to have one central place for that definition and grab that
definition every time we need to reuse it.

In practice this applies the
[DRY principle ("Don't Repeat Yourself")](https://en.wikipedia.org/wiki/Don%27t_repeat_yourself)
to the specification:

> "Every piece of knowledge must have a single, unambiguous, authoritative
> representation within a system".

Having one centralized place where we put all our definitions can be useful when
we want other tools (the BIDS validator, bids-matlab...) to use the content of
the specification.

This is where the BIDS schema (those .yml files we talked about above) comes in
as it is meant to be a machine readable version of the specification.

And so to avoid having to maintain the SAME definition in both the schema and
specification, we started using macros to generate the specification from the
schema.

## Links and references

- [documentation for mkdocs](https://www.mkdocs.org) and how to install it
  locally,
- [documentation for the material theme](https://squidfunk.github.io/mkdocs-material/)
  we use.
- [documentation for the `macros` plugin](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)
