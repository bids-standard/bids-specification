# Provenance

Support for provenance was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension when referring to it in the
context of the academic literature.

!!! bug
    Change example links below once they are merged to bids-examples

!!! example "Example datasets"

    The following examples have been formatted using this specification
    and can be used for practical guidance when curating a new dataset.

    - [Provenance of DICOM to Nifti conversion with `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix) - [Associated Pull Request #494](https://github.com/bids-standard/bids-examples/pull/494)
    - [Provenance of DICOM to Nifti conversion with `heudiconv`](https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv) - [Associated Pull Request #496](https://github.com/bids-standard/bids-examples/pull/496)
    - [Provenance of fMRI preprocessing with `SPM`](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm) - [Associated Pull Request #497](https://github.com/bids-standard/bids-examples/pull/497)
    - [Provenance of fMRI preprocessing with `fMRIPrep`](https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep) - [Associated Pull Request#502](https://github.com/bids-standard/bids-examples/pull/502)

    Further datasets are available from
    the [BIDS examples repository](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#provenance).

## Overview

This part of the BIDS specification is aimed at describing the provenance of a BIDS dataset.

This description is retrospective: it describes a set of steps that were executed in order to obtain the dataset.

!!! note
    This is different from prospective provenance that focuses describing workflows that may be run on a dataset.

This description is based on the [W3C Prov](https://www.w3.org/TR/2013/REC-prov-o-20130430/) standard.

### General principles

Provenance information SHOULD be included in a BIDS dataset when possible.

If provenance information is included, it MUST be described using the conventions detailed by this specification.

Provenance information reflects the provenance of a full dataset and/or of specific files at any level of the BIDS hierarchy.

Provenance information SHOULD not include human subject identifying data.

### Key concepts

Provenance information is encoded using metadata fields.

For the most part, this metadata consists of **provenance objects** of 4 types:

-   **Activities**: transformations that have been applied to data.
-   **ProvEntities**: input or output data for activities.
-   **Software**: software packages used to compute the activities.
-   **Environments**: software environments in which activities were performed.

!!! example "Minimal provenance example"

    ```mermaid
    flowchart BT
        B[Brain extraction] -->|wasAssociatedWith| S{FSL<br>}
        B -->|used| T1([sub-001_T1w.nii])
        B -->|used| L((Linux))
        T1p([sub-001_T1w_preproc.nii]) -->|wasGeneratedBy| B
    ```

    In this example, a brain extraction algorithm was applied on a T1-weighted image:

    - *sub-001_T1w.nii* is the original T1-weighted image;
    - *sub-001_T1w_preproc.nii* is the skull striped image;
    - the *"Brain extraction"* activity was performed using the *FSL* software within a *Linux* software environment.

Provenance objects are described as JSON objects in BIDS. They are stored inside **provenance files** (see [Provenance files](#provenance-files)). Additionally, metadata of provEntities can be stored as BIDS metadata inside sidecar JSON files (see [Provenance of a BIDS file](#provenance-of-a-bids-file)) as well as in `dataset_description.json` files (see [Provenance of a BIDS dataset](#provenance-of-a-bids-dataset)).

## Provenance files

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
   suffixes=["act", "ent", "env", "soft"])
}}

!!! note
    The `prov` BIDS entity allows to group related provenance files, using an arbitrary value for `<label>`. A subdirectory MAY be used to group provenance files sharing the same `prov` entity.

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
    │  ├─ prov-preprocspm_desc-v1_act.json
    │  ├─ prov-preprocspm_desc-v1_ent.json
    │  ├─ prov-preprocspm_desc-v2_act.json
    │  └─ prov-preprocspm_desc-v2_ent.json
    ├─ prov-preprocfsl_act.json
    ├─ prov-preprocfsl_ent.json
    ├─ prov-preprocfsl_env.json
    ├─ prov-preprocfsl_soft.json
    └─ ...
    ```

### Provenance description file

Template:

```
prov/
	provenance.tsv
	provenance.json
```

The purpose of this RECOMMENDED file is to describe properties of provenance files. It MUST contain the column `provenance_label`, which MUST consist of `prov-<label>` values identifying one row for each `prov` entity in the dataset, followed by an optional column containing a description for the entity. Each entity MUST be described by one and only one row.

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
provenance_label	description
prov-preprocspm	Provenance of preprocessing performed with SPM.
prov-preprocfsl	Provenance of preprocessing performed with FSL.
```

It is RECOMMENDED to accompany each `provenance.tsv` file with a sidecar
`provenance.json` file to describe the TSV column names and properties of their values
(see also the [section on tabular files](../common-principles.md#tabular-files)).

`provenance.json` example:

```JSON
{
    "description": {
        "Description": "Description of the provenance file(s)."
    }
}
```

### Activities

Each file with a `act` suffix is a JSON file describing activities.

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

!!! example "Example: a provenance object in a `prov/[<subdir>/]prov-<label>_act.json` file"
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
    This snippet is similar to Activities described in the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

### ProvEntities

Each file with a `ent` suffix is a JSON file describing provEntities.

!!! warning
    These files SHOULD not contain provEntities describing data files that are available in the dataset. Use sidecar JSON files instead for this purpose (see [Provenance of a BIDS file](#provenance-of-a-bids-file)).

    These files SHOULD not contain provEntities describing the current dataset. Use `dataset_description.json` files instead for this purpose (see [Provenance of a BIDS dataset](#provenance-of-a-bids-dataset)).

Each file MUST include the following key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "ProvEntities": "REQUIRED"
   }
) }}

Each object in the `ProvEntities` array includes the following keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.ProvEntities.items") }}

!!! example "Example: a provenance object in a `prov/[<subdir>/]prov-<label>_ent.json` file"
    ```JSON
    {
        "ProvEntities": [
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
    This is a snippet from the [fMRI preprocessing with `SPM` example](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm)

### Software

Each file with a `soft` suffix is a JSON file describing software.

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

!!! example "Example: a provenance object in a `prov/[<subdir>/]prov-<label>_soft.json` file"
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
    This is a snippet from the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

### Environments

Each file with a `env` suffix is a JSON file describing environments.

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

!!! example "Example: a provenance object in a `prov/[<subdir>/]prov-<label>_env.json` file"
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
    This is a snippet from the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

## Provenance of a BIDS file

Metadata of a provEntity describing a BIDS file MAY be stored inside its sidecar JSON.

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
      "ProvEntityType": "OPTIONAL"
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
    This snippet is similar to fields described in [DICOM to Nifti conversion with `heudiconv` example](https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv).

## Provenance of a BIDS dataset

Metadata of a provEntity describing a BIDS dataset (raw, derivative, or study) MAY be stored inside its `dataset_description.json` file. This metadata describes the provenance of the whole dataset.

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

-   Identifier(s) of the activity (one or more) responsible for the creation of the dataset (see the [Description using provenance objects](#description-using-provenance-objects) section).
-   A description of pipelines or processes responsible for the creation of the dataset (see the [Description of pipelines or processes](#description-of-pipelines-or-processes) section).

### Description using provenance objects

This section details a way to describe the provenance of a dataset using provenance objects, providing `GeneratedBy` with the identifier(s) of the activity (one or more) responsible for the creation of the dataset.

Related activities MUST be described inside the dataset (see the [Activities](#activities) section).

!!! example "Example of `GeneratedBy` contents in a `dataset_description.json`"
    ```JSON
    {
        "GeneratedBy": "bids::prov#preprocessing-xMpFqB5q"
    }
    ```
    This is a snippet from the [fMRI preprocessing with `fMRIPrep` example](https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

### Description of processes or pipelines

This section details a way to describe the provenance of a dataset, providing `GeneratedBy` with an array of objects representing pipelines or processes that generated the dataset.

!!! note
    This description can be equivalently represented using the previous section. This modeling is kept for backward-compatibility but might be removed in future BIDS releases (see BIDS 2.0).

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

The following rules and conventions are provided in order to have consistent, human readable, and explicit [IRIs](https://www.w3.org/TR/json-ld11/#iris) as identifiers for provenance objects.

!!! note
    The `Id` field contains the identifier of a provenance objects.

### Identifiers for provEntities

The identifier of a provEntity describing a BIDS file inside a BIDS dataset MUST be a [BIDS URI](../common-principles.md#bids-uri).

!!! warning
    The use of BIDS URIs may require to define the `DatasetLinks` object in [`dataset_description.json`](dataset-description.md#dataset_descriptionjson).

For other cases listed in the [ProvEntities](#proventities) section, the identifier of a provEntity described in a BIDS dataset `<dataset-name>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the provEntity and `<uid>` is a unique group of chars.

```text
bids:[<dataset-name>]:prov#<label>-<uid>
```

!!! example "Examples of identifiers for provEntities"
    - `bids:ds001734:sub-002/anat/sub-02_T1w.nii` - a provEntity describing a T1w file for subject `sub-002` in the `ds001734` dataset;
    - `bids::sub-014/func/sub-014_task-MGT_run-01_events.tsv` - a provEntity describing an events file for subject `sub-014` in the current dataset;
    - `bids:fmriprep:sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz` - a provEntity describing a bold file for subject `sub-001` in the `fmriprep` dataset;
    - `bids::prov#provEntity-acea8093` - a provEntity describing a file that is not available in the dataset.

### Identifiers for other provenance objects

The identifier of an activity, software, or environment described in a BIDS dataset `<dataset-name>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the provenance objects and `<uid>` is a unique group of chars.

```text
bids:[<dataset-name>]:prov#<label>-<uid>
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

The `prov/prov-dcm2niix_soft.json` file describes the software package used for the DICOM conversion. As per the [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers) section, the identifier SHOULD start with `bids:<dataset>:prov#` (here, `bids::` refers to the current dataset).

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

This `prov/prov-dcm2niix_act.json` file describes the conversion activity. Note that the identifier of the previously described software package is used here to describe that the software package was used to compute this activity.

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

Inside the `sub-001/anat/sub-001_T1w.json` file, the metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described activity.

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```

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

The `prov/prov-dcm2niix_soft.json` file describes the software package used. As per [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers) section, the identifier SHOULD start with `bids:<dataset>:prov#` (here, `bids::` refers to the current dataset).

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

The `prov/prov-dcm2niix_act.json` file describes the conversion activity. Note that the identifier of the previously described software package is used here to describe that the software package was used to compute this activity.

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

Inside the `sub-001/anat/sub-001_T1w.json` file, the metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described activity.

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```

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

Inside the `dataset_description.json` file of the study dataset, dataset names are defined in order to refer to two nested datasets using BIDS URIs.

```JSON
{
    ...
    "DatasetLinks": {
        "raw": "sourcedata/raw",
        "fmriprep": "derivatives/fmriprep"
    }
}
```

The `prov/prov-fmriprep_ent.json` file describes two provEntities: one per nested dataset.

```JSON
{
    "ProvEntities": [
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

The `prov/prov-fmriprep_act.json` file describes the activity that generated the derivative dataset using the raw dataset.

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
