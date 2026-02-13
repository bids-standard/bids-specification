# Provenance

Support for provenance was developed as
a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit
this extension when referring to it in the context of the academic literature.

!!! example "Example datasets"

    Several [example datasets](https://bids.neuroimaging.io/datasets/examples.html#provenance)
    have been formatted using this specification and can be used
    for practical guidance when curating a new dataset.

This part of the BIDS specification is aimed at describing the provenance of a BIDS dataset.
This description is retrospective: it describes a set of steps that were executed in order to
establish the dataset and is based on [W3C PROV](https://www.w3.org/TR/2013/REC-prov-o-20130430/)
(see [Provenance from an RDF perspective](#provenance-from-a-rdf-perspective)).

Provenance information SHOULD be included in a BIDS dataset when possible.
If provenance information is included,
it MUST be described using the conventions detailed hereafter.
Provenance information reflects the provenance of a full dataset
and/or of specific files at any level of the BIDS hierarchy.
Provenance information SHOULD not include human subject identifying data.

## Provenance of a BIDS file

Provenance of a BIDS data file SHOULD be stored inside its sidecar JSON.

For that purpose, any sidecar JSON file MAY include the following keys:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table('prov.CommonProvenanceFields') }}

!!! example "Example of metadata in a sidecar JSON file"

    ```JSON
    {
        "GeneratedBy": "bids::prov#conversion-00f3a18f",
        "SidecarGeneratedBy": [
            "bids::prov#preparation-conversion-1xkhm1ft",
            "bids::prov#conversion-00f3a18f"
        ],
        "Digest": {
            "SHA-256": "66eeafb465559148e0222d4079558a8354eb09b9efabcc47cd5b8af6eed51907"
        }
    }
    ```
    For a complete example see
    [Provenance of DICOM to NIfTI conversion with `heudiconv`](
    https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv).

## Provenance of a BIDS dataset

Provenance of a BIDS dataset (raw, derivative, or study) SHOULD be stored
inside its `dataset_description.json` file.
The `dataset_description.json` file of a **BIDS raw dataset** or **BIDS study dataset** MAY
include the `GeneratedBy` key to describe provenance.
The `dataset_description.json` file of a **BIDS derivative dataset** MUST
include the `GeneratedBy` key to describe provenance.

The `GeneratedBy` field MAY contain either of the following values:

-   Identifier(s) of the activity/activities responsible for the creation of the dataset
(see [Description using identifiers](#description-using-identifiers)).

-   A description of pipelines or processes responsible for the creation of the dataset
(see [Description of pipelines or processes](#description-of-pipelines-or-processes)).

### Description using identifiers

This section details how to describe provenance of a dataset using identifiers.
The following field is intended for use in `dataset_description.json` to provide
provenance information that applies to the entire dataset.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy__Id__Dataset": "RECOMMENDED for BIDS raw datasets and BIDS study datasets,\
      REQUIRED for BIDS derivative datasets"
   }
) }}

!!! example "Example of `GeneratedBy` contents in a `dataset_description.json`"

    ```JSON
    {
        "GeneratedBy": "bids::prov#preprocessing-xMpFqB5q"
    }
    ```
    For a complete example see [Provenance of fMRI preprocessing with `fMRIPrep`](
    https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

### Description of processes or pipelines

This section details how to describe the provenance of a dataset using an array of objects
representing pipelines or processes that generated the dataset.

!!! warning

    This description can be equivalently represented using the previous section.
    This modeling is kept for backward-compatibility but might be removed
    in future BIDS releases (see BIDS 2.0).

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "RECOMMENDED for BIDS raw datasets and BIDS study datasets,\
      REQUIRED for BIDS derivative datasets"
   }
) }}

Each object in the `GeneratedBy` array includes the following REQUIRED, RECOMMENDED
and OPTIONAL keys:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Name__GeneratedBy": "REQUIRED",
      "Version__GeneratedBy": "RECOMMENDED",
      "Description__GeneratedBy": 'RECOMMENDED if `Name` is `"Manual"`, OPTIONAL otherwise',
      "CodeURL": "OPTIONAL",
      "Container": "OPTIONAL"
   }
) }}

!!! example "Example of `GeneratedBy` contents in a `dataset_description.json`"

    ```JSON
    {
        "GeneratedBy": [
            {
              "Name": "reproin",
              "Version": "0.6.0",
              "Container": {
                "Type": "docker",
                "Tag": "repronim/reproin:0.6.0"
              }
            }
        ]
    }
    ```

## Provenance files

Any provenance information that can't be stored in either sidecar JSON files
(see [Provenance of BIDS file](#provenance-of-a-bids-file)) or in `dataset_description.json`
(see [Provenance of BIDS dataset](#provenance-of-a-bids-dataset)) MUST be stored in
provenance files under the `/prov/` directory.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/common
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "common",
   datatypes=["prov"],
   suffixes=["act", "soft", "env", "ent"])
}}

!!! note

    The [`prov entity`](../appendices/entities.md#prov) allows to group related provenance files,
    using an arbitrary value for `<label>`.
    A subdirectory MAY be used to group provenance files sharing the same `prov entity`.

The following suffixes specify the contents of provenance files.

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/objects/suffixes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      ["act", "ent", "env", "soft"]
   )
}}

!!! example "Example of organization for provenance files"

    ```
    prov/
    ├─ prov-preprocspm/
    │  ├─ prov-preprocspm_act.json
    │  └─ prov-preprocspm_ent.json
    ├─ prov-preprocfsl_act.json
    ├─ prov-preprocfsl_ent.json
    ├─ prov-preprocfsl_env.json
    ├─ prov-preprocfsl_soft.json
    └─ ...
    ```

### Activities

Activities are transformations that have been applied to data.

Each file with an `act` suffix is a JSON file describing activities.
It MUST include the following key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Activities": "REQUIRED"
   }
) }}

Each object in the `Activities` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Activities.items") }}

!!! example "Example: description of an activity in a `prov/[<subdir>/]prov-<label>_act.json` file"

    ```JSON
    {
        "Activities": [
            {
                "Id": "bids::prov#conversion-00f3a18f",
                "Label": "Dicom to NIfTI conversion",
                "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
                "AssociatedWith": "bids::prov#dcm2niix-khhkm7u1",
                "Used": [
                    "bids::prov#fedora-uldfv058",
                    "bids::sourcedata/dicoms"
                ],
                "StartedAtTime": "2025-03-13T10:26:00",
                "EndedAtTime": "2025-03-13T10:26:05"
            }
        ]
    }
    ```
    For a complete example, see
    [Provenance of DICOM to NIfTI conversion with `dcm2niix`](
    https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

### Software

This section specifies how to describe software packages
that computed the [activities](#activities).

Each file with a `soft` suffix is a JSON file describing software.
It MUST include the following key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Software": "REQUIRED"
   }
) }}

Each object in the `Software` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Software.items") }}

!!! example "Example: description of a software package in a `prov/[<subdir>/]prov-<label>_soft.json` file"

    ```JSON
    {
        "Software": [
            {
                "Id": "bids::prov#dcm2niix-khhkm7u1",
                "AlternativeIdentifier": ["RRID:SCR_023517"],
                "Label": "dcm2niix",
                "Version": "v1.0.20220720"
            }
        ]
    }
    ```
    For a complete example, see [Provenance of DICOM to NIfTI conversion with `dcm2niix`](
    https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

### Input and output data

This section specifies how to describe input and output data for [activities](#activities).
This data corresponds to the W3C PROV
[prov:Entity](https://www.w3.org/TR/2013/REC-prov-o-20130430/#Entity)
class that includes files, datasets and other types of data.

Each file with a `ent` suffix is a JSON file describing input and output data.

!!! note

    The `ent` suffix stands for prov:Entity.

!!! warning

    These files SHOULD not describe files that are available in the dataset.
    See [Provenance of a BIDS file](#provenance-of-a-bids-file) for this purpose.

    These files SHOULD not describe the current dataset.
    See [Provenance of a BIDS dataset](#provenance-of-a-bids-dataset) for this purpose.

Each file MUST include one or more of the following keys:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table('json.prov.EntitiesProvenanceFile') }}

Each object in the `Files` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Files.items") }}

Each object in the `Datasets` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Datasets.items") }}

Each object in the `prov:Entity` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.ProvEntity.items") }}

!!! example "Example: description of a file in a `prov/[<subdir>/]prov-<label>_ent.json` file"

    ```JSON
    {
        "Files": [
            {
                "Id": "bids::sub-01/anat/sub-01_T1w.nii#97a89211",
                "Label": "sub-01_T1w.nii",
                "AtLocation": "sub-01/anat/sub-01_T1w.nii",
                "GeneratedBy": "bids::prov#gunzip-e9264918",
                "Digest": {
                    "SHA-256": "45485541db5734f565b7cac3e009f8b02907245fc6db435c700e84d1037773b5"
                }
            }
        ]
    }
    ```
    For a complete example, see [Provenance of fMRI preprocessing with `SPM`](
    https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm)

!!! example "Example: description of a dataset in a `prov/[<subdir>/]prov-<label>_ent.json` file"

    ```JSON
    {
        "Datasets": [
            {
                "Id": "bids:ds001734:.",
                "Label": "NARPS"
            }
        ]
    }
    ```
    For a complete example, see [Provenance of fMRI preprocessing with `fMRIPrep`](
    https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

### Environments

This section specifies how to describe software environments
in which [activities](#activities) were performed.

Each file with a `env` suffix is a JSON file describing environments.
It MUST include the following key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Environments": "REQUIRED"
   }
) }}

Each object in the `Environments` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Environments.items") }}

!!! example "Example: description of an environment (docker container) in a `prov/[<subdir>/]prov-<label>_env.json` file"

    ```JSON
    {
        "Environments": [
            {
                "Id": "bids::prov#poldracklab/fmriprep-mHl7Dqa0",
                "Label": "poldracklab/fmriprep:1.1.4",
                "AlternativeIdentifier": [
                    "https://hub.docker.com/layers/poldracklab/fmriprep/1.1.4"
                ]
            }
        ]
    }
    ```
    For a complete example, see [Provenance of fMRI preprocessing with `fMRIPrep`](
    https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

### Provenance label file

Template:

```text
prov/
    provenance.tsv
    provenance.json
```

The purpose of this RECOMMENDED file is to describe properties of
[`prov-`](../appendices/entities.md#prov) entities used in the names of provenance files.
It MUST contain the column `provenance_id`,
which MUST consist of `prov-<label>` values identifying one row for each
[`prov entity`](../appendices/entities.md#prov) in the dataset,
followed by an optional column containing a description for the entity.
Each entity MUST be described by one and only one row.

We RECOMMEND to make use of these columns, and
in case that you do use them, we RECOMMEND to use the following values
for them:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Provenance") }}

Throughout BIDS you can indicate missing values with `n/a` (for "not
available").

`provenance.tsv` example:

```tsv
provenance_id	description
prov-preprocspm	Provenance of preprocessing performed with SPM.
prov-preprocfsl	Provenance of preprocessing performed with FSL.
```

Additional columns may be added to `provenance.tsv` but MUST be accompanied with a
`provenance.json` sidecar file to describe the TSV column names and properties of their values
as outlined in [common principles for tabular files](../common-principles.md#tabular-files).

## Consistency and uniqueness of identifiers

Identifiers for JSON objects related to provenance must be
[IRIs](https://www.w3.org/TR/json-ld11/#iris).
The following rules and conventions are provided in order to have consistent,
human readable, and explicit IRIs as identifiers.

### Identifiers for input and output data

The identifier for a BIDS file or a BIDS dataset MUST be
a [BIDS URI](../common-principles.md#bids-uri).
The identifier for a no-longer-existing BIDS file or BIDS dataset SHOULD be
a [BIDS URI](../common-principles.md#bids-uri) with a fragment part.

!!! warning

    The use of BIDS URIs may require to define the `DatasetLinks` object
    in [`dataset_description.json`](dataset-description.md#dataset_descriptionjson).

Apart from BIDS files and BIDS datasets, identifiers for a prov:Entity
(see [Input and output data](#input-and-output-data))
in a BIDS dataset `<dataset-name>` MAY have the following form,
where `<label>` is an arbitrary value for identifying the prov:Entity.

```text
bids:[<dataset-name>]:prov#entity-<label>
```

!!! example "Examples of identifiers for input and output data"

    BIDS files and datasets

    - `bids:ds000011:sub-01/anat/sub-01_T1w.nii.gz` -
    identifier for a T1w file for subject `sub-01` in the `ds000011` dataset;
    - `bids::sub-014/func/sub-014_task-MGT_run-01_events.tsv` -
    identifier for an events file for subject `sub-014` in the current dataset;
    - `bids:fmriprep:sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz` -
    identifier for a bold file for subject `sub-001` in the `fmriprep` dataset;
    - `bids:ds001734:.` - identifier for the `ds001734` dataset;

    Other prov:Entity

    - `bids::prov#entity-28c0ba28` -
    identifier for a prov:Entity that is described in the current dataset.

### Identifiers for other objects

The identifier for an activity, software, or environment described
in a BIDS dataset `<dataset-name>` SHOULD have the following form,
where `<label>` is a human readable name for coherently identifying
the object and `<uid>` is a unique group of chars.

```text
bids:[<dataset-name>]:prov#<label>-<uid>
```

The `<uid>` part of this identifier MUST be used to generate unique identifiers
that distinguish any activity, software, or environment that are different in any of their attributes.

!!! example "Examples of identifiers for activities, environments and software"

    - `bids::prov#conversion-00f3a18f` - a conversion activity described inside the current dataset;
    - `bids::prov#fedora-uldfv058` - a Fedora based environment described inside the current dataset;
    - `bids::prov#fmriprep-awf6cvk6` - the fMRIPrep software described inside the current dataset.

## Provenance from an RDF perspective

Objects describing provenance as defined in this specification
can be aggregated into [JSON-LD](https://www.w3.org/TR/json-ld11/) files ;
which allows to represent provenance as
an RDF graph (see [Resource Description Framework (RDF)](https://www.w3.org/RDF/)).

!!! example "Minimal provenance graph"

    ```mermaid
    flowchart BT
        B[Brain extraction] -->|wasAssociatedWith| S{FSL<br>}
        B -->|used| T1([sub-001_T1w.nii])
        B -->|used| L((Linux))
        T1p([sub-001_space-orig_dseg.nii]) -->|wasGeneratedBy| B
    ```

    In this example, a brain extraction algorithm was applied on a T1-weighted image:

    - *sub-001_T1w.nii* is the original T1-weighted image;
    - *sub-001_space-orig_dseg.nii* is the skull striped image;
    - the *Brain extraction* activity was performed using the *FSL*
    software within a *Linux* software environment.

The terms defined in this specification to describe provenance
are based on the [RDF](https://www.w3.org/RDF/), the [RDF Schema](https://www.w3.org/TR/rdf-schema/),
[JSON-LD](https://www.w3.org/TR/json-ld11/), and [W3C PROV](https://www.w3.org/TR/2013/REC-prov-o-20130430/).
The corresponding [IRIs](https://www.w3.org/TR/json-ld11/#iris) are described
in the JSON-LD context file [`provenance-context.json`](../provenance-context.json)
provided with this specification.

Furthermore, this specification allows to describe provenance with terms from other vocaularies.
This can be done using the `Type` fields for [Activities](#activities),
[Files](#input-and-output-data) or [prov:Entity](#input-and-output-data).

All BIDS examples related to provenance (see. [bids-examples, provenance section](
https://bids-website.readthedocs.io/en/latest/datasets/examples.html#provenance))
show the aggregated version of the provenance metadata they contain.
This comes as a JSON-LD file and a visualization of the graph.
The JSON-LD file consists of an aggregation of the [`Activities`](../glossary.md#objects.metadata.Activities),
[`Software`](../glossary.md#objects.metadata.Software), [`Files`](../glossary.md#objects.metadata.Files),
[`Datasets`](../glossary.md#objects.metadata.Datasets), [`prov:Entity`](../glossary.md#objects.metadata.ProvEntity)
and [`Environments`](../glossary.md#objects.metadata.Environments) objects inside a `Records` object,
as well as a reference to the [`provenance-context.json`](../provenance-context.json) file as
[JSON-LD `@context`](https://www.w3.org/TR/json-ld11/#syntax-tokens-and-keywords).

## Minimal examples

### Provenance of a BIDS raw dataset

!!! example

    For a complete example, see [Provenance of DICOM to NIfTI conversion with `dcm2niix`](
    https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

In this example, we explain provenance metadata of a DICOM to NIfTI conversion with `dcm2niix`.
Consider the following BIDS raw dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "prov": {
            "prov-dcm2niix_act.json": "",
            "prov-dcm2niix_soft.json": "",
            "...": ""
        },
        "sourcedata": {
            "dicoms": {
                "...": "",
            },
        },
        "sub-001": {
            "anat": {
                "sub-001_T1w.json": "",
                "sub-001_T1w.nii.gz": ""
            },
        },
        "...": ""
    }
) }}

The `prov/prov-dcm2niix_soft.json` file describes `dcm2niix`,
the software package used for the DICOM conversion.
As per the [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers)
section, the identifier for the associated software object SHOULD
start with `bids:<dataset>:prov#` (`bids::` refers to the current dataset).

```JSON
{
    "Software": [
        {
            "Id": "bids::prov#dcm2niix-khhkm7u1",
            "Label": "dcm2niix"
        }
    ]
}
```

The `prov/prov-dcm2niix_act.json` file describes the conversion activity.
Note that the identifier for the previously described software package is used here
to describe that the software package was used to compute this activity.

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#conversion-00f3a18f",
            "Label": "Conversion",
            "AssociatedWith": "bids::prov#dcm2niix-khhkm7u1"
        }
    ]
}
```

Inside the `sub-001/anat/sub-001_T1w.json` file,
the metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file
was generated by the previously described activity.

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```

### Provenance of a BIDS derivative dataset

!!! example

    For a complete example, see [Provenance of fMRI preprocessing with `SPM`](
    https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm).

In this example, we explain provenance metadata of fMRI preprocessing steps performed with `SPM`.
Consider the following BIDS derivative dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "prov": {
            "prov-spm_act.json": "",
            "prov-spm_ent.json": "",
            "...": ""
        },
        "sub-01": {
            "anat": {
                "c1sub-001_T1w.json": "",
                "c1sub-001_T1w.nii": "",
                "...": "",
                "sub-001_T1w.json": "",
                "sub-001_T1w.nii": "",
                "...": ""
            },
            "func": {
                "...": ""
            }
        },
        "...": ""
    }
) }}

The `prov/prov-spm_act.json` file describes the preprocessing steps (activities) as JSON objects.
Among them:

-   the `bids::prov#movefile-bac3f385` activity needed a T1w file from the ds000011
dataset identified by `bids:ds000011:sub-01/anat/sub-01_T1w.nii.gz`;

-   the `bids::prov#segment-7d5d4ac5` brain segmentation activity needed the two files
listed inside the `Used` array.

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#movefile-bac3f385",
            "Label": "Move file",
            "Used": [
                "bids:ds000011:sub-01/anat/sub-01_T1w.nii.gz"
            ]
        },
        {
            "Id": "bids::prov#segment-7d5d4ac5",
            "Label": "Segment",
            "Used": [
                "bids::prov#entity-28c0ba28",
                "bids::sub-01/anat/sub-01_T1w.nii"
            ]
        }
    ]
}
```

`bids::sub-01/anat/sub-01_T1w.nii` is a BIDS file available in the current dataset.
The `spm12/tpm/TPM.nii` file is not inside the dataset ;
hence its description is stored inside `prov/prov-spm_ent.json` and
its identifier is not a BIDS URI:

```JSON
{
    "Files": [
        {
            "Id": "bids::prov#entity-28c0ba28",
            "Label": "TPM.nii",
            "AtLocation": "spm12/tpm/TPM.nii"
        }
    ]
}
```

Inside the `sub-001/anat/c1sub-001_T1w.json` file,
the metadata field `GeneratedBy` indicates that the `c1sub-001/anat/sub-001_T1w.nii.gz` file
was generated by the previously described brain segmentation activity.

```JSON
{
    "GeneratedBy": "bids::prov#segment-7d5d4ac5"
}
```

### Provenance of a BIDS study dataset

!!! example

    For a complete example, see [Provenance of manual segmentations](
    https://github.com/bclenet/bids-examples/tree/BEP028_manual/provenance_manual).

In this example, we explain provenance metadata of manual segmentations performed by
two experts on the same T1w file.
Consider the following BIDS study dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "dataset_description.json": "",
        "derivatives": {
            "seg-brain": {
                "dataset_description.json": "",
                "descriptions.tsv": "",
                "...": "",
                "prov": {
                    "provenance.tsv": "",
                    "prov-seg_act.json": "",
                    "prov-seg_soft.json": "",
                    "prov-seg_ent.json": "",
                },
                "sub-001": {
                    "sub-001_space-orig_desc-exp1_dseg.json": "",
                    "sub-001_space-orig_desc-exp1_dseg.nii.gz": "",
                    "sub-001_space-orig_desc-exp2_dseg.json": "",
                    "sub-001_space-orig_desc-exp2_dseg.nii.gz": ""
                }
            },
            "seg-lesions": {
                "...": ""
            }
        },
        "...": "",
        "sourcedata": {
            "raw": {
                "dataset_description.json": "",
                "prov": {
                    "prov-raw_ent.json": "",
                },
                "sub-001": {
                    "sub-001_T1w.json": "",
                    "sub-001_T1w.nii.gz": ""
                }
            }
        },
        "...": ""
    }
) }}

Inside the `dataset_description.json` file of the `seg-brain` derivative dataset,
the `DatasetLinks` metadata field defines an alias that is needed
to refer to the raw dataset using BIDS URIs.

```JSON
{
    "DatasetLinks": {
        "raw": "../../sourcedata/raw"
    }
}
```

The `prov/prov-seg_act.json` file describes activities during which
the experts generated segmentations.

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#segmentation-nO5RGsrb",
            "Label": "Manual brain segmentation",
            "Command": null,
            "Used": [
                "bids:raw:sub-001/anat/sub-001_T1w.nii.gz"
            ]
        },
        {
            "Id": "bids::prov#segmentation-mOOypIYB",
            "Label": "Manual brain segmentation",
            "Command": null,
            "Used": [
                "bids:raw:sub-001/anat/sub-001_T1w.nii.gz"
            ]
        }
    ]
}
```

Note that a description of the `sub-001/anat/sub-001_T1w.nii.gz` file is needed because
this data file is related to the activities.
Here we rely on the `sourcedata/raw` dataset to provide a description of the data file.

Under the `derivatives/seg-brain` dataset,
the `sub-001_space-orig_desc-exp1_dseg.json` file describes which activity generated
the `sub-001_space-orig_desc-exp1_dseg.nii.gz` file.

```JSON
{
    "GeneratedBy": "bids::prov#segmentation-nO5RGsrb"
}
```

The `derivatives/seg-brain/prov/provenance.tsv` gives a description of the `prov-seg` entity.

```tsv
provenance_id	description
prov-seg	Manual brain segmentation performed by two experts
```

The `descriptions.tsv` gives descriptions of the `desc-` entities used for datafiles.

```tsv
desc_id	description
desc-exp1	Files generated by expert #1
desc-exp2	Files generated by expert #2
```
