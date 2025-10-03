# Provenance

Support for provenance was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension when referring to it in the
context of the academic literature.

!!! bug
    Change example links below once they are merged to bids-examples

!!! example "Example datasets"

    The following examples have been formatted using this specification
    and can be used for practical guidance when curating a new dataset.

    - [Provenance records for DICOM to Nifti conversion using `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix) - [Associated Pull Request #494](https://github.com/bids-standard/bids-examples/pull/494)
    - [Provenance records for DICOM to Nifti conversion using `heudiconv`](https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv) - [Associated Pull Request #496](https://github.com/bids-standard/bids-examples/pull/496)
    - [Provenance records for fMRI preprocessing using `SPM`](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm) - [Associated Pull Request #497](https://github.com/bids-standard/bids-examples/pull/497)
    - [Provenance records for fMRI preprocessing using `fMRIPrep`](https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep) - [Associated Pull Request#502](https://github.com/bids-standard/bids-examples/pull/502)

    Further datasets are available from
    the [BIDS examples repository](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#provenance).

## Overview

This part of the BIDS specification is aimed at describing the provenance of a BIDS dataset.

This description is retrospective, it describes a set of steps that were executed in order to obtain the dataset (this is different from prospective descriptions of workflows that could for instance list all sets of steps that can be run on this dataset).

This description is based on the [W3C Prov](https://www.w3.org/TR/2013/REC-prov-o-20130430/) standard.

### General principles

Provenance information SHOULD be included in a BIDS dataset when possible.

If provenance information is included, it MUST be described using the conventions detailed by this specification.

Provenance information reflects the provenance of a full dataset and/or of specific files at any level of the BIDS hierarchy.

Provenance information SHOULD not include human subject identifying data.

### Key concepts

Provenance information is encoded using metadata fields.

For the most part, this metadata consists of **provenance records** of 4 types:

-   **Activities**: transformations that have been applied to data.
-   **Entities**: input or output data for activities.
-   **Software**: software packages activities are associated with.
-   **Environments**: software environments in which activities were performed.

!!! example "Relations between provenance records"

    The following graph presents examples of relations between provenance records.

    ```mermaid
    flowchart BT
        B[Brain extraction] -->|wasAssociatedWith| S{FSL<br>}
        B -->|used| T1([sub-001_T1w.nii])
        B -->|used| L((Linux))
        T1p([sub-001_T1w_preproc.nii]) -->|wasGeneratedBy| B
    ```

    In this example:

    - *sub-001_T1w.nii* is an entity representing a file used by the *Brain extraction* activity;
    - this activity generated another file represented by the *sub-001_T1w_preproc.nii* entity;
    - this activity was associated with the *FSL* software and used *Linux* as a software environment.

Provenance records are described as JSON objects in BIDS. They are stored inside **provenance files** (see [Provenance files](#provenance-files)).

Additionally, metadata of entities can be stored as regular BIDS metadata inside:

-   sidecar JSON files (see [Provenance of a BIDS file](#provenance-of-a-bids-file));
-   `dataset_description.json` files (see [Provenance of a BIDS dataset](#provenance-of-a-bids-dataset)).

## Provenance files

Template:

```text
prov/
    [<subdir>/]
        prov-<label>_act.json
        prov-<label>_ent.json
        prov-<label>_env.json
        prov-<label>_soft.json
```

!!! note
    The `prov` BIDS entity allows to group related provenance files, using an arbitrary value for `<label>`. A subdirectory MAY be used to organize provenance files, using an arbitrary value for `<subdir>`.

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
    ├─ preprocspm/
    │  ├─ prov-preprocspm1_act.json
    │  ├─ prov-preprocspm1_ent.json
    │  ├─ prov-preprocspm2_act.json
    │  └─ prov-preprocspm2_ent.json
    ├─ prov-preprocfsl_act.json
    ├─ prov-preprocfsl_ent.json
    ├─ prov-preprocfsl_env.json
    ├─ prov-preprocfsl_soft.json
    └─ ...
    ```

### Activities

Each `prov/[<subdir>/]prov-<label>_act.json` file is a JSON file describing activities.

Each file MUST include the following key:

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

!!! example "Example of provenance record in a `prov/[<subdir>/]prov-<label>_act.json` file"
    ```JSON
    {
        "Activities": [
            {
                "Id": "bids::prov/#conversion-00f3a18f",
                "Label": "Dicom to Nifti conversion",
                "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
                "AssociatedWith": "bids::prov/#dcm2niix-khhkm7u1",
                "Used": [
                    "bids::prov/#fedora-uldfv058",
                    "bids::sourcedata/dicoms"
                ],
                "StartedAtTime": "2025-03-13T10:26:00",
                "EndedAtTime": "2025-03-13T10:26:05"
            }
        ]
    }
    ```
    This snippet is derived from the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

### Entities

Each `prov/[<subdir>/]prov-<label>_ent.json` file is a JSON file describing entities.

!!! warning
    These files MUST not contain entity records describing data files that are available in the dataset. Use sidecar JSON files instead for this purpose (see [Provenance of a BIDS file](#provenance-of-a-bids-file)).

!!! warning
    These files MUST not contain entity records describing the current dataset. Use `dataset_description.json` files instead for this purpose (see [Provenance of a BIDS dataset](#provenance-of-a-bids-dataset)).

Entity records in these files MAY describe:

-   files or data that are located in another dataset;
-   files or data that were deleted during the creation of the dataset;
-   different versions of the same files or data that were modified during the creation of the dataset;
-   files or data that are part of software pieces or environments;
-   any other files or data that do not match the previously listed cases, as long as the entity record cannot be described in a sidecar JSON or in `dataset_description.json`.

Each file MUST include the following key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Entities": "REQUIRED"
   }
) }}

Each object in the `Entities` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Entities.items") }}

!!! example "Example of provenance record in a `prov/[<subdir>/]prov-<label>_ent.json` file"
    ```JSON
    {
        "Entities": [
            {
                "Id": "bids::sub-01/func/sub-01_task-tonecounting_bold.nii",
                "Label": "sub-01_task-tonecounting_bold.nii",
                "AtLocation": "sub-01/func/sub-01_task-tonecounting_bold.nii",
                "GeneratedBy": "bids::prov#realign-acea8093",
                "Digest": {
                    "sha256": "a4e801438b9c36df010309c94fc4ef8b07d95e7d9cb2edb8c212a5e5efc78d90"
                }
            }
        ]
    }
    ```
    This snippet is an extract of the [fMRI preprocessing with `SPM` example](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm)

### Software

Each `prov/[<subdir>/]prov-<label>_soft.json` file is a JSON file describing software.

Each file MUST include the following key:

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

!!! example "Example of provenance record in a `prov/[<subdir>/]prov-<label>_soft.json` file"
    ```JSON
    {
        "Software": [
            {
                "Id": "bids::prov/#dcm2niix-khhkm7u1",
                "AltIdentifier": "RRID:SCR_023517",
                "Label": "dcm2niix",
                "Version": "v1.0.20220720"
            }
        ]
    }
    ```
    This snippet is an extract of the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

### Environments

Each `prov/[<subdir>/]prov-<label>_env.json` file is a JSON file describing environments.

Each file MUST include the following key:

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

!!! example "Example of provenance record in a `prov/[<subdir>/]prov-<label>_env.json` file"
    ```JSON
    {
        "Environments": [
            {
                "Id": "bids::prov/#fedora-uldfv058",
                "Label": "Fedora release 36 (Thirty Six)",
                "OperatingSystem": "GNU/Linux 6.2.15-100.fc36.x86_64"
            }
        ]
    }
    ```
    This snippet is an extract of the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

## Provenance of a BIDS file

Metadata of an entity describing a BIDS file MAY be stored inside its sidecar JSON.

Any sidecar JSON file MAY include the following keys:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedById": "OPTIONAL",
      "SidecarGeneratedBy": "OPTIONAL",
      "Digest": "OPTIONAL",
      "EntityType": "OPTIONAL"
   }
) }}

!!! example "Example of metadata in a sidecar JSON file"
    ```JSON
    {
        "GeneratedBy": "bids::prov#conversion-00f3a18f",
        "SidecarGeneratedBy": [
            "bids::prov#preparation-conversion-1xkhm1ft",
            "bids::prov#conversion-00f3a18f"
        ],
        "Digest": {
            "sha256": "66eeafb465559148e0222d4079558a8354eb09b9efabcc47cd5b8af6eed51907"
        }
    }
    ```
    This snippet is derived from the [DICOM to Nifti conversion with `heudiconv` example](https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv).

## Provenance of a BIDS dataset

Metadata of an entity describing a BIDS dataset (raw, derivative, or study) MAY be stored inside its `dataset_description.json` file.

This metadata describes the provenance of the whole dataset.

The `dataset_description.json` file of a **BIDS raw dataset** or **BIDS study dataset** MAY include the following key to describe provenance.

The `dataset_description.json` file of a **BIDS derivative dataset** MUST include the following key to describe provenance.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "RECOMMENDED for BIDS raw datasets and BIDS study datasets, REQUIRED for BIDS derivative datasets"
   }
) }}

The `GeneratedBy` field MAY contain either of the following values:

-   Identifier (respectively set of identifiers) of the activity (resp. activities) responsible for the creation of the dataset (see the [Description using provenance records](#description-using-provenance-records) section).
-   A description of pipelines or processes responsible for the creation of the dataset (see the [Description of pipelines or processes](#description-of-pipelines-or-processes) section).

### Description using provenance records

This section details a way to describe the provenance of a dataset using provenance records, providing `GeneratedBy` with the identifier (respectively a set of identifiers) of the activity (resp. activities) responsible for the creation of the dataset.

Related `Activities` MUST be described inside the dataset (see the [`Activities`](#activities) section).

!!! example "Example of `GeneratedBy` contents in a `dataset_description.json`"
    ```JSON
    {
        "GeneratedBy": "bids::prov#preprocessing-xMpFqB5q"
    }
    ```
    This snippet is an extract of the [fMRI preprocessing with `fMRIPrep` example](https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

### Description of processes or pipelines

This section details a way to describe the provenance of a dataset, providing `GeneratedBy` with an array of objects representing pipelines or processes that generated the dataset.

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

## Consistency and uniqueness of identifiers

The following rules and conventions are provided in order to have consistent, human readable, and explicit [IRIs](https://www.w3.org/TR/json-ld11/#iris) as identifiers for provenance records.

!!! note
    The `Id` field contains the identifier of a provenance records.

### Identifiers for entities

The identifier of an entity describing a BIDS file inside a BIDS dataset MUST be a [BIDS URI](../common-principles.md#bids-uri).

!!! note
    The use of BIDS URIs may require to define the `DatasetLinks` object in [`dataset_description.json`](dataset-description.md#dataset_descriptionjson).

For other cases listed in the [Entities](#entities) section, the identifier of an entity described in a BIDS dataset `<dataset>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the record and `<uid>` is a unique group of chars.

```text
bids:<dataset>:prov#<label>-<uid>
```

!!! example "Examples of identifiers for entities"
    - `bids:ds001734:sub-002/anat/sub-02_T1w.nii` - an entity describing a T1w file for subject `sub-002` in the `ds001734` dataset;
    - `bids::sub-014/func/sub-014_task-MGT_run-01_events.tsv` - an entity describing an events file for subject `sub-014` in the current dataset;
    - `bids:fmriprep:sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz` - an entity describing a bold file for subject `sub-001` in the `fmriprep` dataset;
    - `bids::prov#entity-acea8093` - an entity describing a file that is not available in the dataset.

### Identifiers for other provenance records

The identifier of an activity, software, or environment described in a BIDS dataset `<dataset>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the record and `<uid>` is a unique group of chars.

```text
bids:<dataset>:prov#<label>-<uid>
```

The uniqueness of this identifier MUST be used to distinguish any activity, software, or environment that are different in any of their attributes.

!!! example "Examples of identifiers for activities, environments and software"
    - `bids:ds001734:prov#conversion-xfMMbHK1` - a conversion activity described inside the `ds001734` dataset;
    - `bids::prov#fedora-uldfv058` - a Fedora based environment described inside the current dataset.
    - `bids:preprocessing:prov#fmriprep-r4kzzMt8` - the fMRIPrep software described inside the `preprocessing` dataset.

## Minimal examples

### Provenance of a BIDS raw dataset

Consider the following BIDS raw dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "sourcedata": {
            "dicoms": {
                "...": "",
            },
        },
        "sub-001": {
            "anat": {
                "sub-001_T1w.nii.gz": "",
                "sub-001_T1w.json": ""
            },
        },
        "prov": {
            "prov-dcm2niix_act.json": "",
            "prov-dcm2niix_soft.json": ""
        }
    }
) }}

Here are the contents of the `prov/prov-dcm2niix_soft.json` file:

```JSON
{
    "Software": [
        {
            "Id": "bids::prov#dcm2niix-70ug8pl5",
            "Label": "dcm2niix",
            "Version": "v1.1.3"
        }
    ]
}
```

A software package is described using a provenance record inside the `Software` array. As mentioned in the [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers) section, its identifier SHOULD start with `bids:<dataset>:prov#` (here, `bids::` refers to the current dataset).

Here are the contents of the `prov/prov-dcm2niix_act.json` file:

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#conversion-00f3a18f",
            "Label": "Conversion",
            "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
            "AssociatedWith": "bids::prov#dcm2niix-70ug8pl5"
        }
    ]
}
```

An activity is described using a provenance record inside the `Activities` array. Note that the identifier of the previously described software package is used here to describe that the software package was associated with this activity.

Here are the contents of the `sub-001/anat/sub-001_T1w.json` file:

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```

The metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described activity.

### Provenance of a BIDS derivative dataset

Consider the following BIDS derivative dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "sourcedata": {
            "dicoms": {
                "...": "",
            },
        },
        "sub-001": {
            "anat": {
                "sub-001_T1w.nii.gz": "",
                "sub-001_T1w.json": ""
            },
        },
        "prov": {
            "prov-dcm2niix_act.json": "",
            "prov-dcm2niix_soft.json": ""
        }
    }
) }}

Here are the contents of the `prov/prov-dcm2niix_soft.json` file:

```JSON
{
    "Software": [
        {
            "Id": "bids::prov#dcm2niix-70ug8pl5",
            "Label": "dcm2niix",
            "Version": "v1.1.3"
        }
    ]
}
```

A software package is described using a provenance record inside the `Software` array. As mentioned in the [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers) section, its identifier SHOULD start with `bids:<dataset>:prov#` (here, `bids::` refers to the current dataset).

Here are the contents of the `prov/prov-dcm2niix_act.json` file:

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#conversion-00f3a18f",
            "Label": "Conversion",
            "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
            "AssociatedWith": "bids::prov#dcm2niix-70ug8pl5"
        }
    ]
}
```

An activity is described using a provenance record inside the `Activities` array. Note that the identifier of the previously described software package is used here to describe that the software package was associated with this activity.

Here are the contents of the `sub-001/anat/sub-001_T1w.json` file:

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```

The metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described activity.

### Provenance of a BIDS study dataset

Consider the following BIDS study dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "study-1": {
        "sourcedata": {
            "raw": {
                "sub-01": {},
                "sub-02": {},
                "...": ""
            }
        },
        "derivatives": {
            "fmriprep": {}
        },
        "prov": {
            "prov-fmriprep_act.json": "",
            "prov-fmriprep_ent.json": ""
        },
        "dataset_description.json": "",
        "...": ""
    }
   }
) }}

Here are the contents of the `dataset_description.json` file for the study dataset:

```JSON
{
    ...
    "DatasetLinks": {
        "raw": "sourcedata/raw",
        "fmriprep": "derivatives/fmriprep"
    }
}
```

Dataset names are defined in order to refer to two nested datasets using BIDS URIs.

Here are the contents of the `prov/prov-fmriprep_ent.json` file:

```JSON
{
    "Entities": [
        {
            "Id": "bids:raw",
            "Label": "Raw data"
        },
        {
            "Id": "bids:fmriprep",
            "Label": "Preprocessed data",
            "GeneratedBy": "bids::prov#preprocessing-00f3a18f"
        },
    ]
}
```

Two entities are described inside the `Entities` array, using one provenance record per nested dataset.

Here are the contents of the `prov/prov-fmriprep_act.json` file:

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#preprocessing-00f3a18f",
            "Label": "Preprocessing with fMRIprep",
            "Command": "docker run  -v sourcedata/raw:/data:ro -v derivatives/fmriprep:/out poldracklab/fmriprep:1.1.4 /data /out",
            "Used": "bids:raw"
        }
    ]
}
```

An activity is described using a provenance record inside the `Activities` array.
