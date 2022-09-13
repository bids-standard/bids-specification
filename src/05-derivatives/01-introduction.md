# BIDS Derivatives

Derivatives are outputs of common processing pipelines, capturing data and
meta-data sufficient for a researcher to understand and (critically) reuse those
outputs in subsequent processing.
Standardizing derivatives is motivated by use cases where formalized
machine-readable access to processed data enables higher level processing.

The following sections cover additions to and divergences from "raw" BIDS.
Placement and naming conventions for derived datasets are addressed in
[Storage of derived datasets][storage], and dataset-level metadata is included
in [Derived dataset and pipeline description][derived-dataset-description].

## Metadata conventions

-   Unless specified otherwise, individual sidecar JSON files and all metadata
    fields within are OPTIONAL. However, the appropriate use of these files and
    pertinent fields is very valuable and thus encouraged. Moreover, for some
    types of files, there may be one or more required metadata fields, in which
    case at least one metadata file containing that field must be located
    somewhere within the file’s hierarchy (per the
    [Inheritance Principle](../02-common-principles.md#the-inheritance-principle)).

-   When chaining derivative pipelines, any JSON fields that were specified as
    mandatory in the input files SHOULD be propagated forward in the output
    file’s JSON provided they remain valid. Non-required JSON fields MAY be
    propagated, and are highly useful, but it is the pipeline’s responsibility
    to ensure that the values are still relevant and appropriate to the type of
    output data.

## Model-based grouping of derivatives

Here, a *model* is defined as a process via which parameters that describe
the data are fit/derived. This could include, but is not limited to things
like:

1.  The beta weights for different kinds of events in an event-related design
    in fMRI.

1.  The six components of the diffusion tensor in DTI.

1.  Etc.

Model-based derivatives SHOULD be saved in a directory named `model-<model_id>`
that is placed under the datatype from which the model was derived.

{{ MACROS___make_filetree_example(

   {
   "<pipeline_name>": {
      "sub-<label>": {
         "<datatype>": {
            "model-<label>": {
                "<model files>": ""
            }
         }
      }
   }
   }

) }}

The specification of `<model files>` is [introduced below](#file-naming-conventions).

### Models file

Template:

{{ MACROS___make_filetree_example(

   {
   "<pipeline_name>": {
      "sub-<label>": {
         "<datatype>": {
            "model-<label>": {
                "<model files>": ""
            },
            "models.tsv": "",
            "models.json": ""
         }
      }
   }
   }

) }}

A metadata file, `models.tsv` is OPTIONAL, accompanied by
a `models.json` file that is REQUIRED, if and only if `models.tsv` is present.
The purpose of the RECOMMENDED `models.tsv` file is to index the available
`<model_id>` labels and describe properties of the models such as the datatype
from which they are derived and a human-readable description of each model.

If this file exists, it MUST contain the column `model_id`,
which MUST consist of `model-<label>` values identifying one row for each model,
followed by a list of optional columns describing models.
Each model MUST be described by one and only one row.

The RECOMMENDED `datatype` column SHOULD be one of the available
[data type identifiers](../02-common-principles.md#definitions).

The RECOMMENDED `description` column SHOULD be string containing a short description
of the model. It is RECOMMENDED that the description is a single line of no more than
50 words. It is also RECOMMENDED to avoid special characters (e.g., new lines, tabs).

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "model_id": ("REQUIRED", "There MUST be exactly one row for each model."),
      "datatype": "RECOMMENDED",
      "description__models": "RECOMMENDED",
   }
) }}

In this case, the `models.tsv` file could contain the following content:

```Text
model_id    datatype    description
model-DTI dwi Diffusion tensor model.
model-VGG16   func    A VGG convolutional neural network.
```

It is RECOMMENDED to accompany each `models.tsv` file with a sidecar
`models.json` file to describe the TSV column names and properties of their values (see also
the [section on tabular files](../02-common-principles.md#tabular-files)).
Such sidecar files are needed to interpret the data, especially so when
custom columns are defined beyond `model_id`, `datatypes`, `description`.

`models.json` example for a `models.tsv` file that has an extra column with name `runtime`:

```JSON
{
    "runtime": {
        "Description": "elapsed time for the execution of the model",
        "Units": "seconds"
    }
}
```

### Example

The contents of the `model-<model_id>/` folders can differ widely between models
and modalities and are described in the relevant modality-specific derivative
specifications. For a more concrete example, consider the following
derivative dataset:

{{ MACROS___make_filetree_example(

   {
   "my_pipeline-v2002a": {
      "models.tsv": "",
      "models.json": "",
      "sub-01": {
         "dwi": {
            "model-DTI": {
                "sub-01_model-DTI_param-tensor_model.nii.gz": "",
                "sub-01_model-DTI_param-tensor_model.json": "",
                "sub-01_model-DTI_param-S0_model.nii.gz": "",
                "sub-01_model-DTI_param-S0_model.json": ""
            },
            "model-DTI_model.tsv": ""
         },
         "func": {
            "model-VGG16": {
                "sub-01_model-VGG16_param-all_model.h5": "",
                "sub-01_model-VGG16_param-all_model.json": ""
            },
            "model-VGG16_model.tsv": ""
         }
      }
   }
   }

) }}

Please note that this example is fictional, and the `_model` suffix here has been
used to only illustrate file names according to their particular convention (see below).

## File naming conventions

-   Filenames that are permissible for a raw BIDS data type have a privileged
    status. Any modification of raw files must use a modified filename that does
    not conflict with the raw filename. Further, any files created as part of a
    derivative dataset must not match a permissible filename of a valid raw
    dataset. Stated equivalently, if any filename in a derivative dataset has a
    name permissible for a raw BIDS data, then that file must be an identical
    copy of that raw file.

-   Each Derivatives filename MUST be of the form:
    `<source_entities>[_keyword-<value>]_<suffix>.<ext>`
    (where `<value>` could either be an `<index>` or a `<label>` depending on
    the keyword; see [Definitions][definitions])

-   When the derivatives chain involves outputs derived from a single raw input,
    `source_entities` MUST be the entire source filename, with the omission of
    the source suffix and extension. One exception to this rule is filename
    entities that are no longer relevant. Depending on the nature of the
    derivative file, the suffix can either be the same as the source file if
    that suffix is still appropriate, or a new appropriate value selected from
    the controlled list.

-   There is no prohibition against identical filenames in different derived
    datasets, although users should be aware of the potential ambiguity this can
    create and use the sidecar JSON files to detail the specifics of individual
    files.

-   When necessary to distinguish two files that do not otherwise have a
    distinguishing entity, the [`_desc-<label>`](../appendices/entities.md#desc)
    entity SHOULD be used.
    This includes the cases of needing to distinguish both differing inputs and
    differing outputs (for example, `_desc-T1w` and `_desc-T2w` to distinguish
    brain mask files derived from T1w and T2w images;
    or `_desc-sm4` and `_desc-sm8` to distinguish between outputs generated with
    two different levels of smoothing).

-   When naming files that are not yet standardized, it is RECOMMENDED to use
    names consistent with BIDS conventions where those conventions apply.
    For example, if a summary statistic is derived from a given task, the file
    name SHOULD contain [`_task-<label>`](../appendices/entities.md#task).

<!-- Link Definitions -->

[definitions]: ../02-common-principles.md#definitions

[storage]: ../02-common-principles.md#storage-of-derived-datasets

[derived-dataset-description]: ../03-modality-agnostic-files.md#derived-dataset-and-pipeline-description
