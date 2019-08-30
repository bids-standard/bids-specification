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
    processing. Each pipeline has a dedicated directory under which it stores
    all of its outputs. There are few restriction on the directory name; it is
    RECOMMENDED to use the format `<pipeline>-<variant>` in cases where it is
    anticipated that the same pipeline will output more than one variant (e.g.,
    `AFNI-blurring`, `AFNI-noblurring`, etc.). For the sake of consistency, the
    subfolder name MUST be the `PipelineDescription.Name` field in
    `data_description.json`, optionally followed by a hyphen and a suffix (see
    below).

    For example:

    ```Plain
    <dataset>/derivatives/fmriprep-v1.4.1/sub-0001
    <dataset>/derivatives/spm/sub-0001
    <dataset>/derivatives/vbm/sub-0001
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

In addition to raw BIDS datasets, derived BIDS datasets include the following
required or recommended `dataset_description.json` keys (a dot in the Key name
denotes a key in a subdictionary):

| **Key name**                  | **Description**                                                                                                                                                                                                                              |
| ----------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PipelineDescription.Name      | REQUIRED. Name of the pipeline that generated the outputs. In case the derived dataset is stored as a subfolder of the raw dataset this field MUST be a substring of the derived dataset folder name (a.k.a. `<pipeline_name>` - see above). |
| PipelineDescription.Version   | OPTIONAL. Version of the pipeline.                                                                                                                                                                                                           |
| PipelineDescription.CodeURL   | OPTIONAL. URL where the code for the analysis can be found.                                                                                                                                                                                  |
| PipelineDescription.Container | OPTIONAL. Object specifying the location and relevant attributes of software container image used to produce the derivative. Valid fields in this object include `Type`, `Tag` and `URI`.                                                    |
| SourceDatasets                | OPTIONAL. A list of objects specifying the locations and relevant attributes of all source datasets. Valid fields in each object include `URL`, `DOI`, and `Version`.                                                                        |

Example:

```JSON
{
    "Name": "FMRIPREP Outputs",
    "BIDSVersion": "TODO (depends when this PR will be merged)",
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

The coordinate system (a.k.a. space) a particular derivative is in SHOULD be
denoted using a filename keyword `space` whenever such keyword is present in
the filename template of a given derivative type. The allowed values for this
keyword depend on the file format:

| File format                  | Description             | Allowed `CoordinateSystem` values                                                                                                                                                                                                                     |
| ---------------------------- | ----------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIfTI (`.nii` and `.nii.gz`) | Volume data             | Coordinate systems listed in [Template Based Coordinate Systems: Volume](../99-appendices/08-coordinate-systems.md#volume). If `individual` or `custom` is used then setting [`SpatialReference`](#spatialreference-key-allowed-values) is REQUIRED   |
| GIFTI (`.gii`)               | Surface data            | Coordinate systems listed in [Template Based Coordinate Systems: Surface](../99-appendices/08-coordinate-systems.md#surface). If `individual` or `custom` is used then setting [`SpatialReference`](#spatialreference-key-allowed-values) is REQUIRED |
| CIFTI (`.nii`)               | Volume and surface data | Coordinate systems listed in [Template Based Coordinate Systems: Hybrid (Volume/Surface) aliases](../99-appendices/08-coordinate-systems.md#hybrid-volumesurface-aliases)                                                                             |

Examples:

```Text
sub-01/func/sub-01_task-rest_space-MNI305_bold.nii.gz
sub-01/func/sub-01_task-rest_space-individual_bold.nii.gz
sub-01/anat/sub-01_hemi-L_space-fsaverage5_thickness.shape.gii
sub-01/anat/sub-01_hemi-R_space-fsaverage5_thickness.shape.gii
sub-01/anat/sub-01_hemi-L_space-individual_thickness.shape.gii
sub-01/anat/sub-01_hemi-R_space-individual_thickness.shape.gii
sub-01/func/sub-01_task-rest_space-HCPMNIfsLR32k_bold.nii
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
| RawSources       | OPTIONAL. A list of paths relative to dataset root pointing to the BIDS-Raw file(s) that were used in the creation of this derivative.                                                                                                                                                                                                                |
| SpatialReference | REQUIRED when a custom template or file is used. A path to a file that was used as, or can be used as, a reference image for determining the coordinate space of this file. The path should start with a `/` and should be relative to the root of the dataset.                                                                                       |
| ReferenceIndex   | REQUIRED when an index into a 4D (SpatialReference) file is used. Used to index into a 4D spatial-reference file.                                                                                                                                                                                                                                     |

### SpatialReference key allowed values

| **Value name** | **Description**                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| orig           | A (potentially unique) per-image space. Useful for describing the source of transforms from an input image to a target space. |
| uri or path    | This can be used to point to a specific file.                                                                                 |

### Examples

Preprocessed `bold` NIfTI file in `individual` coordinate space. Please mind
that in this case `SpatialReference` key is REQUIRED.

```Text
sub-01/func/sub-01_task-rest_space-individual_bold.nii.gz
sub-01/func/sub-01_task-rest_space-individual_bold.json
```

```JSON
{
    "SpatialReference": "/sub-01/anat/sub-01_desc-combined_T1w.nii.gz"
}
```

Participant cortical thickness GIFTI file in `individual` coordinate space.
Please mind that in this case `SpatialReference` key is REQUIRED.

```Text
sub-01/anat/sub-01_hemi-L_space-individual_thickness.shape.gii
sub-01/anat/sub-01_hemi-L_space-individual_thickness.json
```

```JSON
{
    "SpatialReference": "/sub-01/anat/sub-01_hemi-L_pial.surf.gii"
}
```

## Metadata conventions

-   Unless specified otherwise, individual sidecar JSON files and all metadata
    fields within are optional. However, the appropriate use of these files and
    pertinent fields is very valuable and thus encouraged. Moreover, for some
    types of files, there may be one or more required metadata fields, in which
    case at least one metadata file containing that field must be located
    somewhere within the file’s hierarchy (per [the Inheritance
    Principle](../02-common-principles.md#the-inheritance-principle)).

-   When chaining derivative pipelines, any JSON fields that were specified as
    mandatory in the input files should be propagated forward in the output
    file’s JSON provided they remain valid. Non-required JSON fields can be
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
