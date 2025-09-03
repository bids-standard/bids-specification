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

### Goals

This part of the BIDS specification is aimed at describing the provenance of a BIDS dataset. This description is retrospective: it describes a set of steps that were executed in order to obtain the dataset (this is different from prospective descriptions of workflows that could for instance list all sets of steps that can be run on this dataset).

### Principles for encoding provenance in BIDS

-   Provenance information SHOULD be included in a BIDS dataset when possible.
-   If provenance records are included, these MUST be described using the conventions detailed by this specification.
-   Provenance records MAY be used to reflect the provenance of a full dataset and/or of specific files at any level of the BIDS hierarchy.
-   Provenance information SHOULD be de-identified as necessary.

### Definitions

**Provenance record**: provenance metadata consists of records of 4 types:

-   `Activity`: a transformation that has been applied to data.
-   `Entity`: input or output data for an Activity.
-   `Software`: a software package an Activity is associated with.
-   `Environment`: a software environment in which the Activity was performed.

Provenance records are described as JSON objects in BIDS. This is detailed in the [Provenance files section](#provenance-files).

!!! example
    The following graph represents examples of links between provenance records. In this example, `Entities` *sub-001_brainmask.nii* and *sub-001_T1w.nii* represent files used by `Activity` *Brain extraction* to generate another file represented by `Entity` *sub-001_T1w_preproc.nii*. `Activities` *Brain extraction* and *Move to MNI* were associated with the `Software` *FSL* and used `Environment` *Linux* as a software environment.
    ![](../images/provenance_definitions_graph.png)

**Provenance group**: refers to a collection of provenance records corresponding to a consistent set of processings. Defining multiple provenance groups is appropriate when separate sets of processings have been performed on data, and that they differ in purpose or chronology.

## Provenance in sidecar JSON files

Provenance metadata MAY be stored inside the sidecar JSON of any BIDS file it applies to.
This metadata only describes the provenance of the BIDS file.

!!! example
    Provenance metadata in a sidecar JSON file:
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
    This snippet is derived from the following comprehensive example: [Provenance records for DICOM to Nifti conversion using `heudiconv`](https://github.com/bclenet/bids-examples/tree/BEP028_heudiconv/provenance_heudiconv).

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

!!! note
    Not defining the `SidecarGeneratedBy` field means that the sidecar JSON was generated by the same `Activity` as the data file itself and described in the `GenearatedBy` field.

## Provenance at dataset level

Provenance metadata MAY be stored inside the `dataset_description.json` of any BIDS dataset (or BIDS-Derivatives dataset) it applies to.
This metadata describes the provenance of the whole dataset.

!!! example
    `GeneratedBy` contents in a `dataset_description.json`:
    ```JSON
    {
        "GeneratedBy": [
            {
                "Name": "fmriprep",
                "Id": "bids::prov#preprocessing-xMpFqB5q"
            }
        ]
    }
    ```
    This snippet is an extract of the following comprehensive example: [Provenance records for fMRI preprocessing using `fMRIPrep`](https://github.com/bclenet/bids-examples/tree/BEP028_fmriprep/provenance_fmriprep).

The `dataset_description.json` file of a BIDS dataset MAY include the following key to describe provenance:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "RECOMMENDED"
   }
) }}

The `dataset_description.json` file of a BIDS-Derivatives dataset MUST include the following key to describe provenance:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "REQUIRED"
   }
) }}

Each object in the `GeneratedBy` array includes the following REQUIRED, RECOMMENDED
and OPTIONAL keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.GeneratedBy.items") }}

## Provenance files

Template:

```text
prov/
    [<label>/]
        prov-<label>_act.json
        prov-<label>_ent.json
        prov-<label>_env.json
        prov-<label>_soft.json
```

!!! Note
    Files sharing the same `prov` BIDS entity contain provenance records that belong to the same provenance group.

!!! example
    In this example, two separated sets of processings (`preprocspm` and `preprocfsl`) were performed on the data, resulting in two groups of provenance records.
    ```
    prov/
    ├─ preprocspm/
    │  ├─ prov-preprocspm_act.json
    │  └─ prov-preprocspm_ent.json
    ├─ prov-preprocfsl_act.json
    ├─ prov-preprocfsl_ent.json
    ├─ prov-preprocfsl_env.json
    ├─ prov-preprocfsl_soft.json
    └─ ...
    ```

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

### `Activity` records

Each `prov/[<label>/]prov-<label>_act.json` file is a JSON file describing `Activity` records for a provenance group.

!!! example
    Provenance metadata in a `prov/[<label>/]prov-<label>_act.json` file:
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
    This snippet is derived from the following comprehensive example: [Provenance records for DICOM to Nifti conversion using `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

Each file MUST include an `Activities` key:

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

### `Entity` records

Each `prov/[<label>/]prov-<label>_ent.json` file is a JSON file describing `Entity` records for a provenance group.

!!! Caution
    These files MUST not contain `Entity` records describing data files that are available in the dataset. Use sidecar JSON files instead for this purpose (see [Provenance in sidecar JSON files](#provenance-in-sidecar-json-files)).
    These files MUST not contain `Entity` records describing the current dataset. The provenance of a dataset MAY be described in the `dataset_description.json` files instead (see [Provenance at dataset level](#provenance-at-dataset-level)).

!!! example
    Provenance metadata in a `prov/[<label>/]prov-<label>_ent.json` file:
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
    This snippet is an extract of the following comprehensive example: [Provenance records for fMRI preprocessing using `SPM`](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm)

`Entity` records in these files MAY describe:

-   files or data that are located in another dataset ;
-   files or data that were deleted during the creation of the dataset ;
-   different versions of the same files or data that were modified during the creation of the dataset ;
-   files or data that are part of software pieces or environments ;
-   any other files or data that do not match the previously listed cases, as long as the `Entity` record cannot be described in a sidecar JSON or in `dataset_description.json`.

Each file MUST include an `Entities` key:

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

### `Software` records

Each `prov/[<label>/]prov-<label>_soft.json` file is a JSON file describing `Software` records for a provenance group.

!!! example
    Provenance metadata in a `prov/[<label>/]prov-<label>_soft.json` file:
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
    This snippet is an extract of the following comprehensive example: [Provenance records for DICOM to Nifti conversion using `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

Each file MUST include a `Software` key:

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

### `Environment` records

Each `prov/[<label>/]prov-<label>_env.json` file is a JSON file describing `Environment` records for a provenance group.

!!! example
    Provenance metadata in a `prov/[<label>/]prov-<label>_ent.json` file:
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
    This snippet is an extract of the following comprehensive example: [Provenance records for DICOM to Nifti conversion using `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

Each file MUST include a `Environments` key:

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

!!! bug
    TODO: Environment not currently defined in the context

## Consistency and uniqueness of Ids

The following rules and conventions are provided in order to have consistent, human readable, and explicit [IRIs](https://www.w3.org/TR/json-ld11/#iris) as `Id` for `Entity` provenance records.

!!! example "`Activity`, `Environment`, `Software` naming examples"
    - `bids:ds001734:prov#conversion-xfMMbHK1`: a conversion `Activity` described inside the `ds001734` dataset;
    - `bids::prov#fedora-uldfv058`: a Fedora based `Environment` described inside the current dataset.
    - `bids:derivatives:prov#fmriprep-r4kzzMt8`: the fMRIPrep `Software` described inside the `derivatives` dataset.

An `Id` identifying an `Entity` record corresponding to a file of a BIDS dataset MUST be a [BIDS URI](../common-principles.md#bids-uri).

!!! Warning
    The use of BIDS URIs may require to define the `DatasetLinks` object in [`dataset_description.json`](dataset-description.md#dataset_descriptionjson).

!!! example "`Entity` naming examples"
    - `bids:ds001734:sub-002/anat/sub-02_T1w.nii`: the `Id` of an `Entity` describing a T1w file for subject `sub-002` in the `ds001734` dataset ;
    - `bids::sub-014/func/sub-014_task-MGT_run-01_events.tsv`: the `Id` of an `Entity` describing an events file for subject `sub-014` in the current dataset ;
    - `bids:derivatives:fmriprep/sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz`:  the `Id` of an `Entity` describing a bold file for subject `sub-001` in the `derivatives` dataset.

An `Id` identifying `Activity`, `Software`, and `Environment` provenance records described in a BIDS dataset `<dataset>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the record and `<uid>` is a unique group of chars.

```text
bids:<dataset>:prov#<label>-<uid>
```

The uniqueness of this `Id` MUST be used to distinguish any `Activity`, `Software`, or `Environment` that are different in any of their attributes.

## Minimal example

Here is a comprehensive example that considers the following dataset:

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

The following provenance record is defined in `prov/prov-dcm2niix_soft.json`. As mentioned in the [Consistency and uniqueness of Ids](#consistency-and-uniqueness-of-ids) section, its `Id` SHOULD start with `bids:<dataset>:prov#` (here, `bids::` refers to the current dataset).

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

The previously described `Software` is referred to in the `prov/prov-dcm2niix_act.json` file:

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

The previously described `Activity`  is referred to in the `sub-001/anat/sub-001_T1w.json` sidecar JSON file:

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f"
}
```
