# Common data types

## Processed, coregistered and/or resampled volumes

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        anat|func|dwi|meg|eeg|ieeg|beh/
        <source_keywords>[_space-<space>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<ext>
```

Processing in this context means transformations of data that does not change
the number of dimensions of the input and are not explicitly covered by other
data types in the specification. Examples:

 -  Motion-corrected, temporally denoised, and transformed to MNI space bold files.
 -  Inhomogeneity corrected and skull stripped T1w files.
 -  Motion-corrected DWI files.
 -  Time-domain filtered and ICA cleaned EEG data

The `space` keyword is recomended to distinguish files with different underlying
coordinate systems or registered to different reference maps. The
`desc` keyword is a general purpose field with freeform values. To distinguish
between multiple different versions of processing for the same input data the
`desc` keyword should be used.

Note that even though `space` and `desc` are
optional at least one of them needs to be defined to avoid name conflict with
the raw file.

**Sampling**. When two or more instances of a given derivative are provided
with resolution (or surface sampling density) being the only difference
between them, then the `res` (for *resolution* of regularly sampled N-D data)
and/or `den` (for *density* of non-parametric surfaces) SHOULD be used to avoid
name conflicts.
Note that only files combining both regularly sampled (e.g., gridded) and surface
sampled data (and their downstream derivatives) are allowed to present both `res`
and `den` keywords simultaneously.

!!! tip "Recommendation"
    Although the `res` entity accepts any BIDS-valid `<label>`, it is
    recommended to use one-based, consecutive indexes as label to preempt
    inconsistencies between the value of `res` and the metadata embedded
    within the actual file.

Examples:

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_space-MNI305_res-lo_bold.nii.gz
            sub-001_task-rest_run-1_space-MNI305_res-hi_bold.nii.gz
            sub-001_task-rest_run-1_space-MNI305_bold.json
```

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_desc-MC_bold.nii.gz
            sub-001_task-rest_run-1_desc-MC_bold.json
```

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_desc-fmriprep_bold.nii.gz
            sub-001_task-rest_run-1_desc-fmriprep_bold.json
```

All REQUIRED metadata fields coming from a derivative file’s source file(s) MUST
be propagated to the JSON description of the derivative unless the processing
makes them invalid (e.g., if a source 4D image is averaged to create a single
static volume, a SamplingFrequency property would no longer be relevant). In
addition, all processed files include the following metadata JSON fields:

| **Key name**  | **Description**                                                                                                              |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------- |
| SkullStripped | REQUIRED. Boolean. Whether the volume was skull stripped (non-brain voxels set to zero) or not.                              |
| Resolution    | REQUIRED if `res` keyword present. Dictionary of Strings to Strings. Specifies the interpretation of the resolution keyword. |
| Density       | REQUIRED if `den` keyword present. Dictionary of Strings to Strings. Specifies the interpretation of the density keyword.    |

Example JSON file corresponding to
`pipeline1/sub-001/func/sub-001_task-rest_run-1_space-MNI305_bold.json` above:

```JSON
{
  "SkullStripped": true,
  "Resolution": {
    "hi": "Matched with high-resolution T1w (0.7mm, isotropic)",
    "lo": "Matched with original BOLD resolution (2x2x3 mm^3)"
  }
}
```

This would be equivalent to having two JSON metadata files, one
corresponding to `res-lo`
(`pipeline1/sub-001/func/sub-001_task-rest_run-1_space-MNI305_res-lo_bold.json`):

```JSON
{
  "SkullStripped": true,
  "Resolution": "Matched with original BOLD resolution (2x2x3 mm^3)"
}
```

And one corresponding to `res-hi`
(`pipeline1/sub-001/func/sub-001_task-rest_run-1_space-MNI305_res-hi_bold.json`):

```JSON "pipeline1/sub-001/func/sub-001_task-rest_run-1_space-MNI305_res-hi_bold.json"
{
  "SkullStripped": true,
  "Resolution": "Matched with high-resolution T1w (0.7mm, isotropic)"
}
```

Example of CIFTI files (i.e., a file that combines regularly sampled data
and non-parametric surfaces) having both `res` and `den` keywords:

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_res-1_den-10k_bold.dtseries.nii
            sub-001_task-rest_run-1_res-1_den-41k_bold.dtseries.nii
            sub-001_task-rest_run-1_res-2_den-10k_bold.dtseries.nii
            sub-001_task-rest_run-1_res-2_den-41k_bold.dtseries.nii
            sub-001_task-rest_run-1_bold.dtseries.json
```

And the corresponding `sub-001_task-rest_run-1_bold.dtseries.json` file:

```JSON
{
    "SkullStripped": true,
    "Resolution": {
        "1": "Matched with MNI152NLin6Asym 1.6mm isotropic",
        "2": "Matched with MNI152NLin6Asym 2.0mm isotropic"
    },
    "Density": {
        "10k": "10242 vertices per hemisphere (5th order icosahedron)",
        "41k": "40962 vertices per hemisphere (6th order icosahedron)"
    }
}
```

## Masks

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        anat|func|dwi/
        <source_keywords>[_space-<space>][_desc-<label>]_mask.nii.gz
```

A binary (1 - inside, 0 - outside) mask in the space defined by `<space>`. By
default (i.e., if no transformation has taken place) the value of `space` should
be set to `orig`.

JSON metadata fields:

| **Key name** | **Description**                                                                                                                                |
| ------------ |----------------------------------------------------------------------------------------------------------------------------------------------- |
| RawSources   | Same as defined in [Introduction](01-introduction.md), but elevated from OPTIONAL to REQUIRED                                                  |
| Type         | RECOMMENDED. Short identifier of the mask. Reserved values: `Brain` - brain mask, `Lesion` - lesion mask, `Face` - face mask, `ROI` - ROI mask |

Examples:

```Text
func_loc/
    sub-001/
        func/
           sub-001_task-rest_run-1_space-MNI305_desc-PFC_mask.nii.gz
           sub-001_task-rest_run-1_space-MNI305_desc-PFC_mask.json
```

```Text
manual_masks/
    sub-001/
        anat/
            sub-001_desc-tumor_mask.nii.gz
            sub-001_desc-tumor_mask.json
```

## Segmentations and parcellations

Common JSON metadata fields:

| **Key name** | **Description**                                                                                    |
| ------------ | -------------------------------------------------------------------------------------------------- |
| Manual       | OPTIONAL. Boolean. Indicates if the segmenation was performed manually or via an automated process |
| Atlas        | OPTIONAL. Which atlas (if any) was used to derive the segmentation.                                |

### Discrete Segmentations

Discrete segmentations of brain tissue represent each tissue class with a unique
integer label in a 3D volume. See [Anatomical Labels](#anatomical-labels) for
interpretation how integer values map to tissue classes.

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        anat|func|dwi/
            <source_keywords>[_space-<space>]_dseg.nii.gz
```

Example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_space-orig_dseg.nii.gz
            sub-001_space-orig_dseg.json
```

A segmentation could be a binary mask that functions as a discrete `label` for a
single structure. In this case, the label key must be used to specify the
corresponding structure. For example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_space-orig_label-GM_dseg.nii.gz
```

See [Anatomical Labels](#anatomical-labels) for reserved key values for `label`.

### Probabilistic Segmentations

Probabilistic segmentations of brain tissue represent a single tissue class with
values ranging from 0 to 1 in individual 3D volumes or across multiple frames.
Similarly to a discrete, binary segmentation, the label key can be used to
specify the corresponding structure.

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func|anat|dwi/
            <source_keywords>[space-<space>][_label-<label>]_probseg.nii.gz
```

Example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_space-orig_label-BG_probseg.nii.gz
            sub-001_space-orig_label-WM_probseg.nii.gz
```

See [Anatomical labels](#anatomical-labels) for reserved key values for `label`.

A 4D probabilistic segmentation, in which each frame corresponds to a different
tissue class, must provide a label mapping in its JSON sidecar. For example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_space-orig_probseg.nii.gz
            sub-001_space-orig_probseg.json
```

The JSON sidecar must include the label-map key that specifies a tissue label
for each volume:

```JSON
{
    "LabelMap": [
        "BG",
        "WM",
        "GM"
        ]
}
```

Values of `label` need to map to Abbreviations defined in [Anatomical Labels](#anatomical-labels).

### Surface Parcellations

Discrete parcellations (surface segmentations) of cortical structures should be
stored as GIFTI or CIFTI file.

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        anat/
            <source_keywords>[_hemi-{L|R}][_space-<space>]_dseg.{label.gii|dlabel.nii}
```

The REQUIRED extension for GIFTI parcellations is `.label.gii`. The `hemi` tag is
REQUIRED for GIFTI files. For example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_hemi-L_dparc.label.gii
            sub-001_hemi-R_dparc.label.gii
```

The REQUIRED extension for CIFTI parcellations is `.dlabel.nii`. For example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_dparc.dlabel.nii
            sub-001_dparc.dlabel.nii
```

### Anatomical Labels

BIDS supplies a standard, generic label-index dictionary, defined in the table
below, that contains common tissue classes and can be used to map segmentations
(and parcellations) between lookup tables.

| Integer value | Description             | Abbreviation (label) |
| ------------- | ----------------------- | -------------------- |
| 0             | Background              | BG                   |
| 1             | Grey Matter             | GM                   |
| 2             | White Matter            | WM                   |
| 3             | Cerebrospinal Fluid     | CSF                  |
| 4             | Grey and White Matter   | GWM                  |
| 5             | Bone                    | B                    |
| 6             | Soft Tissue             | ST                   |
| 7             | Non-brain               | NB                   |
| 8             | Lesion                  | L                    |
| 9             | Cortical Grey Matter    | CGM                  |
| 10            | Subcortical Grey Matter | SCGM                 |
| 11            | Brainstem               | BS                   |
| 12            | Cerebellum              | CBM                  |

These definitions can be overridden (or added to) by providing custom labels in
a sidecar `<matches>.tsv` file, in which `<matches>` corresponds to segmentation
filename.

Example:

```Text
pipeline/
    sub-001/
        anat/
            sub-001_space-orig_dseg.nii.gz
            sub-001_space-orig_dseg.tsv
```

Definitions can also be specified with a top-level dseg.tsv, which propagates to
segmentations in relative subdirectories.

Example:

```Text
pipeline/
    dseg.tsv
    sub-001/
        anat/
            sub-001_space-orig_dseg.nii.gz
```

These tsv lookup tables should contain the following columns:

| Column name | Description                                                             |
| ----------- | ----------------------------------------------------------------------- |
| index       | REQUIRED. The label integer index                                       |
| name        | REQUIRED. The unique label name                                         |
| abbr        | OPTIONAL. The unique label abbreviation                                 |
| mapping     | OPTIONAL. Corresponding integer label in the standard BIDS label lookup |
| color       | OPTIONAL. Hexadecimal. Label color for visualization                    |

An example, custom dseg.tsv that defines three labels:

```Text
index   name            abbr    color       mapping
100     "Grey Matter"   GM      #ff53bb     1
101     "White Matter"  WM      #2f8bbe     2
102     "Brainstem"     BS      #36de72     11
```
