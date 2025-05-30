# Imaging data types

This section pertains to imaging data, which characteristically have spatial
extent and resolution.

## Preprocessed, coregistered and/or resampled volumes

Template:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

Volumetric preprocessing does not modify the number of dimensions, and so
the specifications in [Preprocessed or cleaned data][common_preproc]
apply.
The use of surface meshes and volumetric measures sampled to those meshes is
sufficiently similar in practice to treat them equivalently.

When two or more instances of a given derivative are provided with resolution
or surface sampling density being the only difference between them, then the
[`res`](../appendices/entities.md#res) (for *resolution* of regularly sampled N-D data) and/or
[`den`](../appendices/entities.md#den) (for *density* of non-parametric surfaces)
entities SHOULD be used to avoid name conflicts.
Note that only files combining both regularly sampled (for example, gridded)
and surface sampled data (and their downstream derivatives) are allowed
to present both [`res`](../appendices/entities.md#res) and
[`den`](../appendices/entities.md#den) entities simultaneously.

Examples:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline1": {
        "sub-001": {
            "func": {
                "sub-001_task-rest_run-1_space-MNI305_res-lo_bold.nii.gz": "",
                "sub-001_task-rest_run-1_space-MNI305_res-hi_bold.nii.gz": "",
                "sub-001_task-rest_run-1_space-MNI305_bold.json": "",
                },
            },
        }
   }
) }}

The following metadata JSON fields are defined for preprocessed images:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "derivatives.common_derivatives.ImageDerivatives",
       "derivatives.common_derivatives.ImageDerivativeResEntity",
       "derivatives.common_derivatives.ImageDerivativeDenEntity",
   ]) }}

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

```JSON
{
  "SkullStripped": true,
  "Resolution": "Matched with high-resolution T1w (0.7mm, isotropic)"
}
```

Example of CIFTI-2 files (a format that combines regularly sampled data
and non-parametric surfaces) having both [`res`](../appendices/entities.md#res)
and [`den`](../appendices/entities.md#den) entities:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline1": {
        "sub-001": {
            "func": {
                "sub-001_task-rest_run-1_space-fsLR_res-1_den-10k_bold.dtseries.nii": "",
                "sub-001_task-rest_run-1_space-fsLR_res-1_den-41k_bold.dtseries.nii": "",
                "sub-001_task-rest_run-1_space-fsLR_res-2_den-10k_bold.dtseries.nii": "",
                "sub-001_task-rest_run-1_space-fsLR_res-2_den-41k_bold.dtseries.nii": "",
                "sub-001_task-rest_run-1_space-fsLR_bold.json": "",
                },
            },
        }
   }
) }}

And the corresponding `sub-001_task-rest_run-1_space-fsLR_bold.json` file:

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
    sub-<label>/
        anat|func|dwi/
            <source_entities>[_space-<space>][_res-<label>][_den-<label>][_label-<label>][_desc-<label>]_mask.nii.gz
```

A binary (1 - inside, 0 - outside) mask in the space defined by the [`space` entity](../appendices/entities.md#space).
If no transformation has taken place, the value of `space` SHOULD be set to `orig`.
If the mask is an ROI mask derived from a discrete or probabilistic segmentation,
then the [`label` entity](../appendices/entities.md#label) SHOULD be used to specify the masked structure
(see [Common image-derived labels](#common-image-derived-labels)).

JSON metadata fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "derivatives.common_derivatives.MaskDerivatives",
       "derivatives.common_derivatives.ImageDerivativeResEntity",
       "derivatives.common_derivatives.ImageDerivativeDenEntity",
   ]) }}

Examples:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "func_loc": {
        "sub-001": {
            "func": {
                "sub-001_task-rest_run-1_space-MNI305_label-PFC_mask.nii.gz": "",
                "sub-001_task-rest_run-1_space-MNI305_label-PFC_mask.json": "",
                },
            },
        }
   }
) }}

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "manual_masks": {
        "sub-001": {
            "anat": {
                "sub-001_label-tumor_mask.nii.gz": "",
                "sub-001_label-tumor_mask.json": "",
                },
            },
        }
   }
) }}

## Segmentations

A *segmentation* is a spatial partition of images and surfaces,
such that each location (for example, a voxel or a surface vertex)
is identified with one label (discrete) or a combination of labels (probabilistic).
Labeled regions may include anatomical structures (for example, tissue classes,
white matter tracts, Thalamic nuclei, cortical areas),
functionally-defined networks, tumors or lesions.

A *discrete segmentation* represents each region with a unique integer
label.
A *probabilistic segmentation* represents each region as values between
0 and 1 (inclusive) at each location in the image, and one volume/frame per
structure may be concatenated in a single file.

Segmentations may be defined in a volume (labeled voxels), a surface (labeled
vertices) or a combined volume/surface space.

If different segmentations coexist within the same directory of the BIDS
structure (for example, if they were generated with two alternative tools),
the [`seg-<label>` entity](../appendices/entities.md#segmentation)
SHOULD be used for disambiguation.

The [`seg-<label>` entity](../appendices/entities.md#segmentation) MAY be used in combination
with the [`atlas-<label>` entity](../appendices/entities.md#segmentation)
as indicated by the [Templates and Atlases section](atlas.md).

The following section describes discrete and probabilistic segmentations of
volumes, followed by discrete segmentations of surface/combined spaces.
Probabilistic segmentations of surfaces are currently [unspecified][].

The following metadata fields apply to all segmentation files:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "derivatives.common_derivatives.SegmentationCommon",
       "derivatives.common_derivatives.ImageDerivativeResEntity",
       "derivatives.common_derivatives.ImageDerivativeDenEntity",
   ]) }}

### Discrete Segmentations

Discrete segmentations of brain tissue represent regions with unique integer labels.
See [Common image-derived labels](#common-image-derived-labels) for a description
of how integer values map to anatomical structures.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        <data_type>/
            <source_entities>[_space-<space>][_seg-<label>][_res-<label>][_den-<label>]_dseg.nii.gz
```

For example, we can specify the results of a classic brain tissue segmentation algorithm
of a T1w image based on a Gaussian mixture model as:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_dseg.nii.gz": "",
                "sub-001_dseg.json": "",
                },
            },
        }
   }
) }}

When several segmentations coexist at the same BIDS hierarchy point,
[`seg-<label>` entity](../appendices/entities.md#segmentation) SHOULD
be used for disambiguation.
For example, if the brain tissue segmentation above will be stored next
to segmentations of the eyes:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_seg-braintissues_dseg.nii.gz": "",
                "sub-001_seg-braintissues_dseg.json": "",
                "sub-001_seg-eyes_dseg.nii.gz": "",
                "sub-001_seg-eyes_dseg.json": "",
                },
            },
        }
   }
) }}

### Probabilistic Segmentations

Probabilistic segmentations of brain tissue represent a single anatomical
structure with values ranging from 0 to 1 in individual 3D volumes or across
multiple frames.
If a single structure is included,
the [`label` entity](../appendices/entities.md#label) SHOULD be used to specify
the structure.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        func|anat|dwi/
            <source_entities>[_space-<space>][_seg-<label>][_res-<label>][_den-<label>][_label-<label>]_probseg.nii.gz
```

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_space-orig_label-BG_probseg.nii.gz": "",
                "sub-001_space-orig_label-WM_probseg.nii.gz": "",
                },
            },
        }
   }
) }}

See [Common image-derived labels](#common-image-derived-labels)
for reserved values for the [`label`](../appendices/entities.md#label) entity.

A 4D probabilistic segmentation, in which each frame corresponds to a different
tissue class, must provide a label mapping in its JSON sidecar. For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
		        "sub-001_space-orig_probseg.nii.gz": "",
		        "sub-001_space-orig_probseg.json": "",
                },
            },
        }
   }
) }}

The JSON sidecar MUST include the label-map key that specifies a tissue label
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

Values of `label` SHOULD correspond to abbreviations defined in
[Common image-derived labels](#common-image-derived-labels).

### Discrete surface segmentations

Discrete surface segmentations (sometimes called *parcellations*) of cortical
structures MUST be stored as GIFTI label files, with the extension `.label.gii`.
For combined volume/surface spaces, discrete segmentations MUST be stored as
CIFTI-2 dense label files, with the extension `.dlabel.nii`.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        anat/
            <source_entities>[_hemi-{L|R}][_space-<space>][_seg-<label>][_res-<label>][_den-<label>]_dseg.{label.gii|dlabel.nii}
```

The [`hemi-<label>`](../appendices/entities.md#hemi) entity is REQUIRED for GIFTI files storing information about
a structure that is restricted to a hemibrain.
For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_hemi-L_dseg.label.gii": "",
                "sub-001_hemi-R_dseg.label.gii": "",
                },
            },
        }
   }
) }}

The REQUIRED extension for CIFTI parcellations is `.dlabel.nii`. For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_dseg.dlabel.nii": "",
                "sub-001_dseg.dlabel.nii": "",
                },
            },
        }
   }
) }}

### Common image-derived labels

BIDS supplies a standard, generic label-index mapping, defined in the table
below, that contains common image-derived segmentations and can be used to map segmentations
(and parcellations) between lookup tables.

| **Integer value** | **Description**         | **Abbreviation (label)** |
| ----------------- | ----------------------- | ------------------------ |
| 0                 | Background              | BG                       |
| 1                 | Gray Matter             | GM                       |
| 2                 | White Matter            | WM                       |
| 3                 | Cerebrospinal Fluid     | CSF                      |
| 4                 | Bone                    | B                        |
| 5                 | Soft Tissue             | ST                       |
| 6                 | Non-brain               | NB                       |
| 7                 | Lesion                  | L                        |
| 8                 | Cortical Gray Matter    | CGM                      |
| 9                 | Subcortical Gray Matter | SGM                      |
| 10                | Brainstem               | BS                       |
| 11                | Cerebellum              | CBM                      |

These definitions can be overridden (or added to) by providing custom labels in
a sidecar `<matches>.tsv` file, in which `<matches>` corresponds to segmentation
filename.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_space-orig_dseg.nii.gz": "",
                "sub-001_space-orig_dseg.tsv": "",
                },
            },
        }
   }
) }}

Definitions can also be specified with a top-level `dseg.tsv`, which propagates to
segmentations in relative subdirectories.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "dseg.tsv": "",
        "sub-001": {
            "anat": {
                "sub-001_space-orig_dseg.nii.gz": "",
                },
            },
        }
   }
) }}

These TSV lookup tables contain the following columns:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("derivatives.common_derivatives.SegmentationLookup") }}

An example, custom `dseg.tsv` that defines three labels:

```tsv
index	name	abbreviation	color	mapping
100	Gray Matter	GM	#ff53bb	1
101	White Matter	WM	#2f8bbe	2
102	Brainstem	BS	#36de72	11
```

The following example `dseg.tsv` defines regions that are not part of the
standard BIDS labels:

```tsv
index	name	abbreviation
137	pars	opercularis	IFGop
138	pars	triangularis	IFGtr
139	pars	orbitalis	IFGor
```

## Derivatives from atlases

Often, derivatives are *atlas-based*, meaning, a particular result has been
derived from prior knowledge in the form of an [atlas](../common-principles.md).
These derivatives follow the specifications above, with the addition of
a set of entities that MAY be used to disambiguate the outputs.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

-   [`space-<label>`](../appendices/entities.md#space) is REQUIRED to disambiguate derivatives defined with
    respect to different [coordinate systems](../appendices/coordinate-systems.md), following the general
    BIDS-Derivatives specifications.

-   [`atlas-<label>`](../appendices/entities.md#atlas) is REQUIRED to encode files derived
    from the atlas identified by the entity's label.

-   [`seg-<label>`](../appendices/entities.md#seg) is REQUIRED when a single atlas has several different
    realizations (for instance, segmentations and parcellations created with different criteria) that
    need disambiguation.

-   [`scale-<label>`](../appendices/entities.md#scale) is REQUIRED to disambiguate different atlas 'scales',
    when the atlas has more than one 'brain unit' or 'areal resolution', typically relating to the
    number of regions defined and the area they cover.

For example, derivatives from a single subject segmented with the Automated Anatomical Labeling (AAL)
atlas ([Tzourio-Mazoyer et al., 2002](https://doi.org/10.1006/nimg.2001.0978)).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "aals-pipeline": {
      "sub-01": {
         "anat": {
            "sub-01_atlas-AAL_dseg.json": "",
            "sub-01_atlas-AAL_dseg.nii.gz": "",
            "sub-01_atlas-AAL_dseg.tsv": "",
            "sub-01_atlas-AAL_probseg.nii.gz": "",
            "sub-01_label-brain_mask.nii.gz": "",
            "sub-01_label-head_mask.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
            "sub-01_T1w.json": "",
         },
      },
   }
})
}}

Because the AAL atlas was originally defined in the standardized space of MNI305,
it would be unsurprising to find the anatomical reference resampled into the standard
space for validation, as well as the spatial transformation file:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "aals-pipeline": {
      "sub-001": {
         "anat": {
            "sub-001_atlas-AAL_dseg.json": "",
            "sub-001_atlas-AAL_dseg.nii.gz": "",
            "sub-001_atlas-AAL_dseg.tsv": "",
            "sub-001_atlas-AAL_probseg.nii.gz": "",
            "sub-001_from-T1w_to-MNI305_mode-image_xfm.h5": "",
            "sub-001_label-brain_mask.nii.gz": "",
            "sub-001_label-head_mask.nii.gz": "",
            "sub-001_space-MNI305_T1w.nii.gz": "",
            "sub-001_space-MNI305_T1w.json": "",
            "sub-001_T1w.nii.gz": "",
            "sub-001_T1w.json": "",
         },
      },
   }
})
}}

!!! warning "Warning"

    Please note that the specification for spatial transforms (BEP 014) is currently under development,
    and therefore, the specification of transforms files (`sub-01_from-T1w_to-MNI305_mode-image_xfm.h5`
    in the example above) may change in the future.

In the common case of multiple segmentations and parcellations derived from an atlas,
[`seg-<label>`](../appendices/entities.md#segmentation) SHOULD be used in combination
with the [`atlas-<label>` entity](../appendices/entities.md#atlas-entities).
Extending on our previous example, when the brain tissue and the eye
segmentations are stored next to the results of *FreeSurfer*'s automatic subcortical
segmentation ("aseg") using the `Destrieux2009` atlas:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline": {
        "sub-001": {
            "anat": {
                "sub-001_atlas-Destrieux2009_seg-aseg_dseg.nii.gz": "",
                "sub-001_atlas-Destrieux2009_seg-aseg_dseg.json": "",
                "sub-001_atlas-Destrieux2009_seg-aseg+aparc_dseg.nii.gz": "",
                "sub-001_atlas-Destrieux2009_seg-aseg+aparc_dseg.json": "",
                "sub-001_seg-braintissues_dseg.nii.gz": "",
                "sub-001_seg-braintissues_dseg.json": "",
                "sub-001_seg-eyes_dseg.nii.gz": "",
                "sub-001_seg-eyes_dseg.json": "",
                },
            },
        }
   }
) }}

Derivatives from several atlases can coexist in a single directory:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "aals-pipeline": {
      "sub-001": {
         "anat": {
            "sub-001_atlas-AAL_dseg.json": "",
            "sub-001_atlas-AAL_dseg.nii.gz": "",
            "sub-001_atlas-AAL_dseg.tsv": "",
            "sub-001_atlas-AAL_probseg.nii.gz": "",
            "sub-001_atlas-Destrieux2009_seg-aseg+aparc_dseg.json": "",
            "sub-001_atlas-Destrieux2009_seg-aseg+aparc_dseg.nii.gz": "",
            "sub-001_atlas-Destrieux2009_seg-aseg_dseg.json": "",
            "sub-001_atlas-Destrieux2009_seg-aseg_dseg.nii.gz": "",
            "sub-001_from-T1w_to-MNI305_mode-image_xfm.h5": "",
            "sub-001_label-brain_mask.nii.gz": "",
            "sub-001_label-head_mask.nii.gz": "",
            "sub-001_seg-braintissues_dseg.json": "",
            "sub-001_seg-braintissues_dseg.nii.gz": "",
            "sub-001_seg-eyes_dseg.json": "",
            "sub-001_seg-eyes_dseg.nii.gz": "",
            "sub-001_space-MNI305_T1w.json": "",
            "sub-001_space-MNI305_T1w.nii.gz": "",
            "sub-001_T1w.json": "",
            "sub-001_T1w.nii.gz": "",
         },
      },
   }
})
}}

### Atlas tabular data

Atlases are often distributed with a Look Up Table (LUT) that indexes and labels each
node/parcel/region within the atlas.
This file will be essential for downstream workflows that generate matrices or other derived files within
which node/parcel/region information is required, as the index/label fields will be used to reference
the original anatomy the index/labels are derived from.
Atlas-derived results SHOULD encode this information with the `[probseg|dseg|mask].tsv` files following
the prescriptions of the [Common image-derived labels](#common-image-derived-labels) section above.
Additional fields can be added with their respective definition/description in the sidecar JSON file.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_atlas-<label>][seg-<label>][_scale-<label>][_desc-<label>]_<suffix>.tsv
```

For example, the participant-level results using the Schaefer 2018 atlas
could be structured as follows.
Please note that, the `dseg.tsv` files have been moved to the root of the
hierarchy following the common principles.

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "bold-pipeline": {
      "atlas-Schaefer2018_dseg.json": "",
      "atlas-Schaefer2018_seg-7n_scale-100_dseg.tsv": "",
      "atlas-Schaefer2018_seg-7n_scale-200_dseg.tsv": "",
      "atlas-Schaefer2018_seg-7n_scale-300_dseg.tsv": "",
      "atlas-Schaefer2018_seg-17n_scale-100_dseg.tsv": "",
      "atlas-Schaefer2018_seg-17n_scale-200_dseg.tsv": "",
      "atlas-Schaefer2018_seg-17n_scale-300_dseg.tsv": "",
      "atlas-Schaefer2018_seg-kong17n_scale-100_dseg.tsv": "",
      "atlas-Schaefer2018_seg-kong17n_scale-200_dseg.tsv": "",
      "atlas-Schaefer2018_seg-kong17n_scale-300_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-100_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-200_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-300_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-100_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-200_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-300_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-100_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-200_den-164k_dseg.label.gii": "",
            "sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-300_den-164k_dseg.label.gii": "",
            "...": "",
            "sub-01_hemi-R_atlas-Schaefer2018_seg-kong17n_scale-300_den-164k_dseg.label.gii": "",
         },
         "bold": {
            "sub-01_task-rest_hemi-L_den-164k_bold.func.gii": "",
            "sub-01_task-rest_hemi-R_den-164k_bold.func.gii": "",
         }
      },
      "sub-02": {
         "anat": {
            "sub-02_hemi-L_atlas-Schaefer2018_seg-7n_scale-100_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-7n_scale-200_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-7n_scale-300_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-17n_scale-100_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-17n_scale-200_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-17n_scale-300_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-100_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-200_den-164k_dseg.label.gii": "",
            "sub-02_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-300_den-164k_dseg.label.gii": "",
            "...": "",
            "sub-02_hemi-R_atlas-Schaefer2018_seg-kong17n_scale-300_den-164k_dseg.label.gii": "",
         },
         "bold": {
            "sub-02_task-rest_hemi-L_den-164k_bold.func.gii": "",
            "sub-02_task-rest_hemi-R_den-164k_bold.func.gii": "",
         }
      },
   }
})
}}

**Example of contents**.
For example, the file `atlas-Schaefer2018_seg-7n_scale-100_dseg.tsv` could look like:

```tsv
index   name    color
1   17Networks_LH_VisCent_ExStr_1   #781180
2   17Networks_LH_VisCent_ExStr_2   #781181
3   17Networks_LH_VisCent_ExStr_3   #781182
4   17Networks_LH_VisCent_ExStr_4   #781183
5   17Networks_LH_VisCent_ExStr_5   #781184

...

998 17Networks_RH_TempPar_20    #0d2afb
999 17Networks_RH_TempPar_21    #0d2afc
1000    17Networks_RH_TempPar_22    #0d2afd
```

<!-- Link Definitions -->

[common_preproc]: common-data-types.md#preprocessed-or-cleaned-data

[unspecified]: ../common-principles.md#unspecified-data
