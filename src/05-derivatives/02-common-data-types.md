# Common data types and metadata

## Common file level metadata fields

Each derivative data file SHOULD be described by a JSON file provided as a sidecar
or higher up in the hierarchy of the derived dataset (according to the
[Inheritance Principle](../02-common-principles.md#the-inheritance-principle))
unless a particular derivative includes REQUIRED metadata fields, in which case a
JSON file is also REQUIRED.
Each derivative type defines their own set of fields, but all of them
share the following (non-required) ones:

| **Key name** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Description  | RECOMMENDED. Free-form natural language description of the nature of the file.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| Sources      | OPTIONAL. A list of files with the paths specified relative to dataset root; these files were directly used in the creation of this derivative data file. For example, if a derivative A is used in the creation of another derivative B, which is in turn used to generate C in a chain of A->B->C, C should only list B in `Sources`, and B should only list A in `Sources`. However, in case both X and Y are directly used in the creation of Z, then Z should list X and Y in `Sources`, regardless of whether X was used to generate Y. |
| RawSources   | OPTIONAL. A list of paths relative to dataset root pointing to the BIDS-Raw file(s) that were used in the creation of this derivative.                                                                                                                                                                                                                                                                                                                                                                                                        |

### Examples

Preprocessed `bold` NIfTI file in the original coordinate space of the original run.
The location of the file in the original datasets is encoded in the `RawSources`
metadata, and `desc-<label>` is used to prevent clashing with the original file name.

```Text
sub-01/func/sub-01_task-rest_desc-preproc_bold.nii.gz
sub-01/func/sub-01_task-rest_desc-preproc_bold.json
```

```JSON
{
    "RawSources": ["sub-01/func/sub-01_task-rest_bold.nii.gz"]
}
```

If this file was generated with prior knowledge from additional sources, such as
the same subject's `T1w`, then both files MAY be included in `RawSources`.

```JSON
{
    "RawSources": [
        "sub-01/func/sub-01_task-rest_bold.nii.gz",
        "sub-01/anat/sub-01_T1w.nii.gz"
    ]
}
```

On the other hand, if a preprocessed version of the T1w image was used, and it also
occurs in the derivatives, `Sources` and `RawSources` can both be specified.

```JSON
{
    "Sources": [
        "sub-01/anat/sub-01_desc-preproc_T1w.nii.gz"
    ],
    "RawSources": [
        "sub-01/func/sub-01_task-rest_bold.nii.gz"
    ]
}
```

## Spatial references

Derivatives are often aligned to a common spatial reference to allow for the
comparison of acquired data across runs, sessions, subjects or datasets.
A file may indicate the spatial reference to which it has been aligned using the
`space` entity and/or the `SpatialReference` metadata.

The `space` entity may take any value in [Image-Based Coordinate Systems][coordsys].

If the `space` entity is omitted, or the space is not in the [Standard template
identifiers][templates] table, then the `SpatialReference` metadata is REQUIRED.

| **Key name**     | **Description**                                                                                                                                                                                                                                                                                                          |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SpatialReference | RECOMMENDED if the derivative is aligned to a standard template listed in [Standard template identifiers][templates]. REQUIRED otherwise. For images with a single reference, the value MUST be a single string. For images with multiple references, such as surface and volume references, a JSON object MUST be used. |

### SpatialReference key allowed values

| **Value**      | **Description**                                                                                                               |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| `orig`         | A (potentially unique) per-image space. Useful for describing the source of transforms from an input image to a target space. |
| URI or path    | This can be used to point to a specific file. Paths are written relative to the root of the derivative dataset.               |

In the case of images with multiple references, an [object][] must link the relevant structures to reference files.
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

## Preprocessed or cleaned data

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        <datatype>/
            <source_entities>[_space-<space>][_desc-<label>]_<suffix>.<ext>
```

Data is considered to be *preprocessed* or *cleaned* if the data type of the input,
as expressed by the BIDS `suffix`, is unchanged.
By contrast, processing steps that change the number of dimensions are likely to disrupt
the propagation of the input's `suffix` and generally, the outcomes of such transformation
cannot be considered preprocessed or cleaned data.

Examples of preprocessing:

 -  Motion-corrected, temporally denoised, and transformed to MNI space BOLD series
 -  Inhomogeneity corrected and skull stripped T1w files
 -  Motion-corrected DWI files
 -  Time-domain filtered EEG data
 -  MaxFilter (for example, SSS) cleaned MEG data

The `space` keyword is recomended to distinguish files with different underlying
coordinate systems or registered to different reference maps.
See [Spatial references](#spatial-references) for details.
The `desc` (description) keyword is a general purpose field with freeform values,
which SHOULD be used to distinguish between multiple different versions of
processing for the same input data.

Examples of preprocessed data:

```Text
pipeline1/
    sub-001/
        anat/
            sub-001_space-MNI305_T1w.nii.gz
            sub-001_space-MNI305_T1w.json
        func/
            sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.nii.gz
            sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.json
```

```Text
pipeline2/
    sub-001/
        eeg/
            sub-001_task-listening_run-1_desc-autoannotation_events.tsv
            sub-001_task-listening_run-1_desc-autoannotation_events.json
            sub-001_task-listening_run-1_desc-filtered_eeg.edf
            sub-001_task-listening_run-1_desc-filtered_eeg.json
```

All REQUIRED metadata fields coming from a derivative file’s source file(s) MUST
be propagated to the JSON description of the derivative unless the processing
makes them invalid (e.g., if a source 4D image is averaged to create a single
static volume, a `RepetitionTime` property would no longer be relevant).

[]: <> (################)
[]: <> (Link definitions)
[]: <> (################)

[coordsys]: ../99-appendices/08-coordinate-systems.md#image-based-coordinate-systems
[templates]: ../99-appendices/08-coordinate-systems.md#standard-template-identifiers
[object]: https://www.json.org/json-en.html
