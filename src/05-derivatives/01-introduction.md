# Goals and scope

Derivatives are outputs of common processing pipelines, capturing data and
meta-data sufficient for a researcher to understand and (critically) reuse those
outputs in subsequent processing. Standardizing derivatives is motivated by use
cases where formalized machine-readable access to processed data enables higher
level processing.

## Storage of derived datasets

Derivatives can be stored/distributed in two ways:

1.  Under a `derivatives/` subfolder in the root of the source BIDS dataset
    folder to make a clear distinction between raw data and results of data
    processing. A data processing pipeline will typically have a dedicated directory
    under which it stores all of its outputs. Different components of a pipeline can,
    however, also be stored under different subfolders. There are few restrictions on
    the directory names; it is RECOMMENDED to use the format `<pipeline>-<variant>` in
    cases where it is anticipated that the same pipeline will output more than one variant (e.g.,
    `AFNI-blurring`, `AFNI-noblurring`, etc.). For the sake of consistency, the
    subfolder name SHOULD be the `PipelineDescription.Name` field in
    `data_description.json`, optionally followed by a hyphen and a suffix (see
    [Derived dataset and pipeline description](#derived-dataset-and-pipeline-description).

    Example of derivatives with one directory per pipeline:

    ```Plain
    <dataset>/derivatives/fmriprep-v1.4.1/sub-0001
    <dataset>/derivatives/spm/sub-0001
    <dataset>/derivatives/vbm/sub-0001
    ```

    Example of a pipeline with split derivative directories:

    ```Plain
    <dataset>/derivatives/spm-preproc/sub-0001
    <dataset>/derivatives/spm-stats/sub-0001
    ```

    Example of a pipeline with nested derivative directories:

    ```Plain
    <dataset>/derivatives/spm-preproc/sub-0001
    <dataset>/derivatives/spm-preproc/derivatives/spm-stats/sub-0001
    ```


1.  As a standalone dataset independent of the source (raw or derived) BIDS
    dataset. This way of specifying derivatives is particularly useful when the
    source dataset is provided with read-only access, and for publishing
    derivatives as independent bodies of work, or for describing derivatives
    that were created from more than one source dataset. The `sourcedata/`
    subdirectory MAY be used to include the source dataset(s) that were used
    to generate the derivatives.
    Likewise, any code used to generate the derivatives from the source data
    MAY be included in the `code/` subdirectory.

The rest of the Derivatives specification assumes Case 1, but Case 2 applies
after removing `/derivatives/<pipeline_name>` from template names. In both cases
every derivatives dataset is considered a BIDS dataset and must include a
`dataset_description.json` file at the root level. Consequently, files should be
organized to comply with BIDS to the full extent possible (i.e., unless
explicitly contradicted below). Any subject-specific derivatives should be
housed within each subject’s directory; if session-specific derivatives are
generated, they should be deposited under a session subdirectory within the
corresponding subject directory; and so on.

## Derived dataset and pipeline description

As for any BIDS dataset a `dataset_description.json` file MUST be found at the
top level of the particular pipeline:
`<dataset>/derivatives/<pipeline_name>/dataset_description.json`

In addition to the keys for raw BIDS datasets,
derived BIDS datasets include the following REQUIRED, RECOMMENDED or OPTIONAL
`dataset_description.json` keys
(a dot in the Key name denotes a key in a subdictionary):

| **Key name**                  | **Description**                                                                                                                                                                                                                              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PipelineDescription.Name      | REQUIRED. Name of the pipeline that generated the outputs. In case the derived dataset is stored as a subfolder of the raw dataset this field MUST be a substring of the derived dataset folder name (a.k.a. `<pipeline_name>` - see above). |
| PipelineDescription.Version   | RECOMMENDED. Version of the pipeline.                                                                                                                                                                                                        |
| PipelineDescription.CodeURL   | OPTIONAL. URL where the code for the analysis can be found.                                                                                                                                                                                  |
| PipelineDescription.Container | OPTIONAL. Object specifying the location and relevant attributes of software container image used to produce the derivative. Valid fields in this object include `Type`, `Tag` and `URI`.                                                    |
| SourceDatasets                | RECOMMENDED. A list of objects specifying the locations and relevant attributes of all source datasets. Valid fields in each object include `URL`, `DOI`, and `Version`.                                                                     |

Example:

```JSON
{
    "Name": "FMRIPREP Outputs",
    "BIDSVersion": "1.4.0",
    "PipelineDescription": {
        "Name": "FMRIPREP",
        "Version": "1.2.5",
        "Container": {
            "Type": "docker",
            "Tag": "poldracklab/fmriprep:1.2.5"
            }
        },
    "SourceDatasets": [
        {
            "DOI": "10.18112/openneuro.ds000114.v1.0.1",
            "URL": "https://openneuro.org/datasets/ds000114/versions/1.0.1",
            "Version": "1.0.1"
        }
    ]
}
```

## Coordinate systems

The spatial reference (_space_ in the following) to which a particular derivative
is aligned SHOULD be denoted using a filename keyword `space` whenever such keyword
is present in the filename template of a given derivative type.
The allowed values for this keyword depend are identifiers given in section
[Image-Based Coordinate Systems][coordsys].

| File format                  | Description             |
| ---------------------------- | ----------------------- |
| NIfTI (`.nii` and `.nii.gz`) | Volume data             |
| GIFTI (`.gii`)               | Surface data            |
| CIFTI (`.nii`)               | Volume and surface data |

Examples:

```Text
sub-01/func/sub-01_task-rest_space-MNI305_bold.nii.gz
sub-01/func/sub-01_task-rest_space-individual_bold.nii.gz
sub-01/anat/sub-01_hemi-L_space-fsaverage5_thickness.shape.gii
sub-01/anat/sub-01_hemi-R_space-fsaverage5_thickness.shape.gii
sub-01/anat/sub-01_hemi-L_space-individual_thickness.shape.gii
sub-01/anat/sub-01_hemi-R_space-individual_thickness.shape.gii
sub-01/func/sub-01_task-rest_space-fsLR_bold.dtseries.nii
```

## Common file level metadata fields

Each derivative file SHOULD be described by a JSON file provided as a sidecar or
higher up in the hierarchy of the derived dataset (according to
[The Inheritance Principle](../02-common-principles.md#the-inheritance-principle))
unless a particular derivative includes REQUIRED metadata fields in which case a
JSON file is also REQUIRED.
Each derivative type defines their own set of fields, but all of them
share the following (non-required) ones:

| **Key name**     | **Description**                                                                                                                                                                                                                                                                                                                                       |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description      | RECOMMENDED. Free-form natural language description of the nature of the file.                                                                                                                                                                                                                                                                        |
| Sources          | OPTIONAL. A list of paths relative to dataset root pointing to the file(s) that were directly used in the creation of this derivative. For example in a chain of A->B->C, “C” should only list “B” as Sources, and “B” should only list “A” as Sources. However in case X and Y jointly contribute to Z, then “Z” should list “X” and “Y” as Sources. |
| RawSources       | OPTIONAL. A list of paths relative to dataset root pointing to the BIDS-Raw file(s) that were used in the creation of this derivative. When the derivative filename does not define a `space` keyword, the first entry of `RawSources` MUST be defined and it will define the `scanner` coordinate system that applies.                               |
| SpatialReference | REQUIRED in case a custom reference image was used. OPTIONAL if a coordinate system listed in [Image-Based Coordinate Systems][coordsys] is used. For images with a single reference, the value MUST be a single string. For images with multiple references, such as surface and volume references, a data dictionary MUST be used.                  |

### SpatialReference key allowed values

| **Value**      | **Description**                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `orig`         | A (potentially unique) per-image space. Useful for describing the source of transforms from an input image to a target space. |
| URI or path    | This can be used to point to a specific file. Paths are written relative to the root of the derivative dataset.               |

In the case of images with multiple references, a data dictionary must link the relevant structures to reference files.
If a single volumetric reference is used for multiple structures, the `VolumeReference` key MAY be used to reduce duplication.
For CIFTI-2 images, the relevant structures are BrainStructure values defined in the BrainModel elements found in the CIFTI-2 header.

### Examples

Preprocessed `bold` NIfTI file in `individual` coordinate space. Please mind
that in this case `SpatialReference` key is REQUIRED.

```Text
sub-01/func/sub-01_task-rest_space-individual_bold.nii.gz
sub-01/func/sub-01_task-rest_space-individual_bold.json
```

```JSON
{
    "SpatialReference": "sub-01/anat/sub-01_desc-combined_T1w.nii.gz"
}
```

Preprocessed `bold` CIFTI-2 files that have been sampled to the fsLR surface
meshes defined in the Conte69 atlas along with the MNI152NLin6Asym template.
In this example, because all volumetric structures are sampled to the same
reference, the `VolumeReference` key is used as a default, and only the
surface references need to be specified by BrainStructure names.

```Text
sub-01/func/sub-01_task-rest_space-fsLR_den-91k_bold.dtseries.nii
sub-01/func/sub-01_task-rest_space-fsLR_den-91k_bold.json
```

```JSON
{
    "SpatialReference": {
        "VolumeReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
        "CIFTI_STRUCTURE_CORTEX_LEFT": "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/Conte69.L.midthickness.32k_fs_LR.surf.gii",
        "CIFTI_STRUCTURE_CORTEX_RIGHT": "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/Conte69.R.midthickness.32k_fs_LR.surf.gii"
    }
}
```

Preprocessed `bold` NIfTI file in the original coordinate space of the
original run. Please mind that in this case `RawSources` key is REQUIRED
(and also `desc-<label>` so that the name does not overlap with the
original filename).

```Text
sub-01/func/sub-01_task-rest_desc-preproc_bold.nii.gz
sub-01/func/sub-01_task-rest_desc-preproc_bold.json
```

```JSON
{
    "RawSources": ["sub-01/func/sub-01_task-rest_bold.nii.gz"]
}
```

If this file was generated with prior knowledge from additional sources
(e.g., say the same subject's `T1w`), then the first item of `RawSources`
should be the original `bold` file that defined the coordinate system:

```JSON
{
    "RawSources": [
        "sub-01/func/sub-01_task-rest_bold.nii.gz",
        "sub-01/anat/sub-01_T1w.nii.gz"
    ]
}
```

## Metadata conventions

-   Unless specified otherwise, individual sidecar JSON files and all metadata
    fields within are OPTIONAL. However, the appropriate use of these files and
    pertinent fields is very valuable and thus encouraged. Moreover, for some
    types of files, there may be one or more required metadata fields, in which
    case at least one metadata file containing that field must be located
    somewhere within the file’s hierarchy (per [the Inheritance
    Principle](../02-common-principles.md#the-inheritance-principle)).

-   When chaining derivative pipelines, any JSON fields that were specified as
    mandatory in the input files SHOULD be propagated forward in the output
    file’s JSON provided they remain valid. Non-required JSON fields MAY be
    propagated, and are highly useful, but it is the pipeline’s responsibility
    to ensure that the values are still relevant and appropriate to the type of
    output data.

## File naming conventions

-   Filenames that are permissible for a raw BIDS data type have a privileged
    status. Any modification of raw files must use a modified filename that does
    not conflict with the raw filename. Further, any files created as part of a
    derivative dataset must not match a permissible filename of a valid raw
    dataset. Stated equivalently, if any filename in a derivative dataset has a
    name permissible for a raw BIDS data, then that file must be an identical
    copy of that raw file.

-   Each Derivatives filename MUST be of the form:
    `<source_keywords>[_keyword-<value>]_<suffix>.<ext>`
    (where `<value>` could either be an `<index>` or a `<label>` depending on
    the keyword)

-   When the derivatives chain involves outputs derived from a single raw input,
    `source_keywords` MUST be the entire source filename, with the omission of
    the source suffix and extension. One exception to this rule is filename
    keywords that are no longer relevant. Depending on the nature of the
    derivative file, the suffix can either be the same as the source file if
    that suffix is still appropriate, or a new appropriate value selected from
    the controlled list.

-   There is no prohibition against identical filenames in different derived
    datasets, although users should be aware of the potential ambiguity this can
    create and use the sidecar JSON files to detail the specifics of individual
    files.

-   When necessary to distinguish two files, the `_desc-<label>` keyword-value
    should be used. This includes the cases of needing to distinguish both
    differing inputs and differing outputs (e.g., `_desc-T1w` and `_desc-T2w` to
    distinguish brain mask files derived from T1w and T2w images; or `_desc-sm4`
    and `_desc-sm8` to distinguish between outputs generated with two different
    levels of smoothing).

-   When naming files that are not yet standardized, it is RECOMMENDED to use
    names consistent with BIDS conventions where those conventions apply.
    For example, if a summary statistic is derived from a given task, the file
    name SHOULD contain `_task-<label>`.

## Non-compliant datasets

Nothing in this specification should be interpreted to disallow the
storage/distribution non-compliant derivatives of BIDS datasets.
In particular, if a BIDS dataset contains a `derivatives/` sub-directory,
the contents of that directory may be a heterogeneous mix of BIDS Derivatives
datasets and non-compliant derivatives.

[coordsys]: ../99-appendices/08-coordinate-systems.md#image-based-coordinate-systems
