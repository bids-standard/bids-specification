# Structural (anatomical) derivatives

## Reconstructed cortical surfaces

Reconstructed cortical surfaces should be stored as GIFTI files, and each
hemisphere should be stored separately.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        anat/
            <source-entities>_hemi-{L|R}[_space-<label>][_den-<label>][_desc-<label>]_<surftype>.surf.gii
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
                    "sub-001_hemi-L_pial.surf.gii": "",
                    "sub-001_hemi-R_pial.surf.gii": "",
                },
            },
        }
    }
) }}

The supported surface types (`<surftype>` suffix) are:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "white",
         "smoothwm",
         "pial",
         "midthickness",
         "inflated",
         "vinflated",
         "sphere",
         "flat",
      ]
   )
}}

-   [`space-<label>`](../appendices/entities.md#space) is REQUIRED to disambiguate derivatives defined with
    respect to different [coordinate systems](../appendices/coordinate-systems.md), following the general
    BIDS-Derivatives specifications.

-   [`den-<label>`](../appendices/entities.md#den) is REQUIRED to disambiguate different surface sampling densities.

## Surface-Mapped Anatomical Scalar Derivatives

Surface-mapped scalar overlays should be stored as either GIFTI or CIFTI files
(which allow for the combination of left and right hemispheres).

Template:

```Text
<pipeline_name>/
    sub-<label>/
        anat/
            <source-entities>[_hemi-{L|R}][_space-<label>][_den-<label>][_desc-<label>]_<suffix>.{shape.gii|dscalar.nii}
```

The REQUIRED extension for scalar GIFTI files is `.shape.gii`.
The `hemi` key is required for GIFTI files. For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "pipeline": {
            "sub-001": {
                "anat": {
                    "sub-001_hemi-L_curv.shape.gii": "",
                    "sub-001_hemi-R_curv.shape.gii": "",
                },
            },
        }
    }
) }}

The REQUIRED extension for scalar CIFTI files is `.dscalar.nii`. For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
        "pipeline": {
            "sub-001": {
                "anat": {
                    "sub-001_curv.dscalar.nii": "",
                },
            },
        }
    }
) }}

The file `<suffix>` MUST be one of the following values:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "curv",
         "thickness",
         "area",
         "dist",
         "defects",
         "sulc",
         "T1wT2wratio",
         "distortion",
      ]
   )
}}

## Morphometrics

Structural statistics produced by segmentation routines should be stored within
tsv files, which could contain common parameters specified in the table below.

Template:

```Text
<pipeline_name>/
    sub-<label>/
        func|anat|dwi/
            <source-entities>[_desc-<label>]_morph.tsv
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
                    "sub-001_desc-volumetric_morph.tsv": "",
                },
            }
        }
    }
) }}

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("deriv.structural_mri.Morphometrics") }}

Some parameters might require unit specification or have multiple associated
statistics (such as avg, std, min, max, range). The suggested syntax for such
columns is `<parameter>[-<stat>][-<units>]`. An example volumetric stats file
might look something like this:

```Text
index  name               volume-mm3  intensity-avg  intensity-std
11     Brainstem          23415.9     80.11          3.40
32     Left-Hippocampus   5349.7      75.23          2.27
32     Right-Hippocampus  4112.1      76.98          4.01
```
