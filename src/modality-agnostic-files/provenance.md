# Provenance

Support for provenance was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension when referring to it in the
context of the academic literature.

!!! example "Example datasets"

    Several [example BIDS-Prov datasets](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#provenance) have been formatted using this specification and can be used for practical guidance when curating a new dataset.

This part of the BIDS specification is aimed at describing the provenance of a BIDS dataset. This description is retrospective: it describes a set of steps that were executed in order to obtain the dataset. Note: This is different from prospective provenance that focuses describing workflows that may be run on a dataset. This description is based on the [W3C Prov](https://www.w3.org/TR/2013/REC-prov-o-20130430/) standard (see the [Provenance from an RDF perspective](#provenance-from-a-rdf-perspective) section for more information).

Provenance information SHOULD be included in a BIDS dataset when possible. If provenance information is included, it MUST be described using the conventions detailed by this specification. Provenance information reflects the provenance of a full dataset and/or of specific files at any level of the BIDS hierarchy. Provenance information SHOULD not include human subject identifying data.

## Provenance of a BIDS file

Provenance of a BIDS file SHOULD be stored inside its sidecar JSON.

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

Provenance of a BIDS dataset (raw, derivative, or study) SHOULD be stored inside its `dataset_description.json` file. This metadata describes the provenance of the whole dataset.

The `dataset_description.json` file of a **BIDS raw dataset** or **BIDS study dataset** MAY include the `GeneratedBy` key to describe provenance.

The `dataset_description.json` file of a **BIDS derivative dataset** MUST include the `GeneratedBy` key to describe provenance.

The `GeneratedBy` field MAY contain either of the following values:

-   Identifier(s) of the activity/activities responsible for the creation of the dataset (see the [Description using provenance objects](#description-using-provenance-objects) section).
-   A description of pipelines or processes responsible for the creation of the dataset (see the [Description of pipelines or processes](#description-of-pipelines-or-processes) section).

### Description using provenance objects

This section details the way to describe provenance of a dataset in the `GeneratedBy` field, using provenance objects.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedById": "RECOMMENDED for BIDS raw datasets and BIDS study datasets, REQUIRED for BIDS derivative datasets"
   }
) }}

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

When not inside sidecar JSONs or `dataset_description.json`, provenance information MUST be stored inside provenance files.

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
    The [`prov entity`](../appendices/entities.md#prov) allows to group related provenance files, using an arbitrary value for `<label>`. A subdirectory MAY be used to group provenance files sharing the same `prov entity`.

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

### Activities

Activities are JSON objects representing the transformations that have been applied to data.

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
                "Id": "bids::prov#conversion-00f3a18f",
                "Label": "Dicom to Nifti conversion",
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
    This snippet is similar to Activities described in the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix).

### ProvEntities

ProvEntities are JSON objects representing input or output data for activities (Note: this corresponds to Entities in [W3C Prov](https://www.w3.org/TR/2013/REC-prov-o-20130430/), the prefix "Prov" is used here to disambiguate with [BIDS entities](../appendices/entities.md)).

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
                "Id": "bids::prov#provEntity-9rfe8szz",
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

Software are JSON objects representing software packages used to compute the [activities](#activities).

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
                "Id": "bids::prov#dcm2niix-khhkm7u1",
                "AltIdentifier": "RRID:SCR_023517",
                "Label": "dcm2niix",
                "Version": "v1.0.20220720"
            }
        ]
    }
    ```
    This is a snippet from the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

### Environments

Environments are JSON objects representing software environments in which activities were performed.

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
                "Id": "bids::prov#fedora-uldfv058",
                "Label": "Fedora release 36 (Thirty Six)",
                "OperatingSystem": "GNU/Linux 6.2.15-100.fc36.x86_64"
            }
        ]
    }
    ```
    This is a snippet from the [DICOM to Nifti conversion with `dcm2niix` example](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix)

### Provenance description file

Template:

```text
prov/
    provenance.tsv
    provenance.json
```

The purpose of this RECOMMENDED file is to describe properties of provenance files. It MUST contain the column `provenance_label`, which MUST consist of `prov-<label>` values identifying one row for each [`prov entity`](../appendices/entities.md#prov) in the dataset, followed by an optional column containing a description for the entity. Each entity MUST be described by one and only one row.

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
provenance_label    description
prov-preprocspm Provenance of preprocessing performed with SPM.
prov-preprocfsl Provenance of preprocessing performed with FSL.
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

## Consistency and uniqueness of identifiers

The following rules and conventions are provided in order to have consistent, human readable, and explicit [IRIs](https://www.w3.org/TR/json-ld11/#iris) as identifiers for provenance objects.

!!! note
    The `Id` field contains the identifier of a provenance objects.

### Identifiers for provEntities

The identifier of a provEntity describing a BIDS file available in the dataset MUST be a [BIDS URI](../common-principles.md#bids-uri).
The identifier of a provEntity describing a BIDS file not available in the dataset SHOULD be a [BIDS URI](../common-principles.md#bids-uri) with a fragment part.

!!! warning
    The use of BIDS URIs may require to define the `DatasetLinks` object in [`dataset_description.json`](dataset-description.md#dataset_descriptionjson).

In other cases, the identifier of a provEntity described in a BIDS dataset `<dataset-name>` MAY have the following form, where `<label>` is an arbitrary value for identifying the provEntity.

```text
bids:[<dataset-name>]:prov#provEntity-<label>
```

!!! example "Examples of identifiers for provEntities"
    - `bids:ds001734:sub-002/anat/sub-02_T1w.nii` - a provEntity describing a T1w file for subject `sub-002` in the `ds001734` dataset;
    - `bids::sub-014/func/sub-014_task-MGT_run-01_events.tsv` - a provEntity describing an events file for subject `sub-014` in the current dataset;
    - `bids:fmriprep:sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz` - a provEntity describing a bold file for subject `sub-001` in the `fmriprep` dataset;
    - `bids::prov#provEntity-acea8093` - a provEntity describing a file that is not available in the dataset.

### Identifiers for other provenance objects

The identifier of an activity, software, or environment described in a BIDS dataset `<dataset-name>` SHOULD have the following form, where `<label>` is a human readable name for coherently identifying the provenance object and `<uid>` is a unique group of chars.

```text
bids:[<dataset-name>]:prov#<label>-<uid>
```

The uniqueness of this identifier MUST be used to distinguish any activity, software, or environment that are different in any of their attributes.

!!! example "Examples of identifiers for activities, environments and software"
    - `bids:ds001734:prov#conversion-xfMMbHK1` - a conversion activity described inside the `ds001734` dataset;
    - `bids::prov#fedora-uldfv058` - a Fedora based environment described inside the current dataset.
    - `bids:preprocessing:prov#fmriprep-r4kzzMt8` - the fMRIPrep software described inside the `preprocessing` dataset.

## Provenance from an RDF perspective

!!! note
    The [Resource Description Framework (RDF)](https://www.w3.org/RDF/) is a method to describe and exchange graph data.

Provenance objects as defined in this specification can be aggregated into [JSON-LD](https://www.w3.org/TR/json-ld11/) files ; which allows to represent provenance as an RDF graph.

!!! example "Minimal provenance graph"

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

Moreover, the terms defined in this specification to describe provenance objects are based on the [W3C Prov](https://www.w3.org/TR/2013/REC-prov-o-20130430/) standard. They can be resolved to [IRIs](https://www.w3.org/TR/json-ld11/#iris) using the JSON-LD context file [`provenance-context.json`](../../provenance-context.json) provided with this specification.

All BIDS examples related to provenance (see. [bids-examples, provenance section](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#provenance)) show the aggregated version of the provenance metadata they contain. This comes as a JSON-LD file and a visualization of the graph.

## Minimal examples

### Provenance of a BIDS raw dataset

!!! example
    This section shows a snippet from the [Provenance of DICOM to Nifti conversion with `dcm2niix`](https://github.com/bclenet/bids-examples/tree/BEP028_dcm2niix/provenance_dcm2niix) example.

In this example, we explain provenance metadata of a DICOM to Nifti conversion with `dcm2niix`. Consider the following BIDS raw dataset:

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

The `prov/prov-dcm2niix_soft.json` file describes `dcm2niix`, the software package used for the DICOM conversion. As per the [Consistency and uniqueness of identifiers](#consistency-and-uniqueness-of-identifiers) section, the identifier for the associated software provenance object SHOULD start with `bids:<dataset>:prov#` (`bids::` refers to the current dataset).

```JSON
{
  "Software": [
    {
      "Id": "bids::prov#dcm2niix-khhkm7u1",
      "Label": "dcm2niix",
      ...
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
            "AssociatedWith": "bids::prov#dcm2niix-khhkm7u1",
            ...
        }
    ]
}
```

Inside the `sub-001/anat/sub-001_T1w.json` file, the metadata field `GeneratedBy` indicates that the `sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described activity.

```JSON
{
    ...
    "GeneratedBy": "bids::prov#conversion-00f3a18f",
    ...
}
```

### Provenance of a BIDS derivative dataset

!!! example
    This section shows a snippet from the [Provenance of fMRI preprocessing with `SPM`](https://github.com/bclenet/bids-examples/tree/BEP028_spm/provenance_spm) example.

In this example, we explain provenance metadata of fMRI preprocessing steps performed with `SPM`. Consider the following BIDS derivative dataset:

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

The `prov/prov-spm_act.json` file describes the preprocessing steps as activities provenance objects. Among them:

-   the `bids::prov#movefile-bac3f385` activity needed a T1w file from the ds000011 dataset identified by `bids:ds000011:sub-01/anat/sub-01_T1w.nii.gz`;
-   the `bids::prov#segment-7d5d4ac5` brain segmentation activity needed two files listed as provEntities inside the `Used` array.

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#movefile-bac3f385",
            "Label": "Move file",
            "Used": [
                "bids:ds000011:sub-01/anat/sub-01_T1w.nii.gz"
            ],
            ...
        },
        ...
        {
            "Id": "bids::prov#segment-7d5d4ac5",
            "Label": "Segment",
            "Used": [
                "urn:c1d082a5-34ee-4282-99df-28c0ba289210",
                "bids::sub-01/anat/sub-01_T1w.nii"
            ],
            ...
        },
        ...
    ]
}
```

The BIDS file described by provEntity `bids::sub-01/anat/sub-01_T1w.nii` is available in the current dataset. The file described by provEntity `urn:c1d082a5-34ee-4282-99df-28c0ba289210` is not inside the dataset ; the provEntity is stored inside `prov/prov-spm_ent.json`:

```JSON
{
    "ProvEntities": [
        ...
        {
          "Id": "urn:c1d082a5-34ee-4282-99df-28c0ba289210",
          "Label": "TPM.nii",
          "AtLocation": "spm12/tpm/TPM.nii",
          ...
        },
        ...
    ]
}
```

Inside the `sub-001/anat/c1sub-001_T1w.json` file, the metadata field `GeneratedBy` indicates that the `c1sub-001/anat/sub-001_T1w.nii.gz` file was generated by the previously described brain segmentation activity.

```JSON
{
    "GeneratedBy": "bids::prov#segment-7d5d4ac5",
    ...
}
```

### Provenance of a BIDS study dataset

!!! example
    This section shows a snippet from the [Provenance of manual annotations](https://github.com/bclenet/bids-examples/tree/BEP028_manual/provenance_manual) example.

In this example, we explain provenance metadata of brain segmentation performed by two experts on the same T1w file. Consider the following BIDS study dataset:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "dataset_description.json": "",
        "derivatives": {
            "seg": {
                "dataset_description.json": "",
                "descriptions.tsv": "",
                "...": "",
                "prov": {
                    "provenance.tsv": "",
                    "prov-seg_desc-exp1_act.json": "",
                    "prov-seg_desc-exp1_soft.json": "",
                    "prov-seg_desc-exp2_act.json": "",
                    "prov-seg_desc-exp2_soft.json": "",
                    "prov-seg_ent.json": "",
                },
                "sub-001": {
                    "sub-001_space-orig_desc-exp1_dseg.json": "",
                    "sub-001_space-orig_desc-exp1_dseg.nii.gz": "",
                    "sub-001_space-orig_desc-exp2_dseg.json": "",
                    "sub-001_space-orig_desc-exp2_dseg.nii.gz": ""
                }
            }
        },
        "...": "",
        "sourcedata": {
            "raw": {
                "dataset_description.json": "",
                "sub-001": {
                    "sub-001_T1w.json": "",
                    "sub-001_T1w.nii.gz": ""
                }
            }
        },
        "...": ""
    }
) }}

Inside the `dataset_description.json` file of the `seg` derivative dataset, the `DatasetLinks` metadata field defines an alias that is needed to refer to the raw dataset using BIDS URIs.

```JSON
{
    ...
    "DatasetLinks": {
        "raw": "../../sourcedata/raw"
    }
}
```

The `prov/prov-seg_desc-exp1_act.json` file describes the activity during which expert #1 generated the brain segmentation.

```JSON
{
    "Activities": [
        {
            "Id": "bids::prov#segmentation-nO5RGsrb",
            "Label": "Semi-automatic brain segmentation",
            "Command": "itk-snap sourcedata/raw/sub-001/anat/sub-001_T1w.nii.gz",
            "AssociatedWith": [
                "bids::prov#itksnap-Lfs6FRMn"
            ],
            "Used": [
                "bids:raw:sub-001/anat/sub-001_T1w.nii.gz"
            ]
        }
    ]
}
```

Note that a description of the `sub-001/anat/sub-001_T1w.nii.gz` file is needed inside `derivatives/seg/prov/prov-seg_ent.json` because this data file is not in the `derivative/seg` dataset.

Under the `derivatives/seg` dataset, the `sub-001_space-orig_desc-exp1_dseg.json` file describes that this activity generated the `sub-001_space-orig_desc-exp1_dseg.nii.gz` file.

```JSON
{
    "GeneratedBy": "bids::prov#segmentation-nO5RGsrb"
}
```

The `derivatives/seg/prov/provenance.tsv` gives a description of the `prov-seg`.

```TXT
provenance_label    description
prov-seg   Manual brain segmentation performed by two experts
```

The `descriptions.tsv` gives descriptions of the `desc` entities used both for provenance files and datafiles.

```TXT
desc_id    description
desc-seg1   Files generated by expert #1
desc-seg2   Files generated by expert #2
```
