# Templates and atlases

In the following, we describe how the outcomes of analyses that produce
[templates and atlases](../common-principles.md#definitions) are organized
as BIDS-Derivatives.

!!! note "Important"

    For outcomes of analyses corresponding to individual subjects
    that derive from atlases and may refer to spaces other than the original
    subject's space, please refer to the
    [Derivatives from atlases](imaging.md#derivatives-from-atlases) subsection.

## Derived templates

Many analyses include spatial standardization to pull individuals' data
into a common spatial frame.
For example, creating an atlas will most likely require the creation of a new template
or the integration of existing ones to define a stereotactic space.

For derivatives of template-generating pipelines, which typically aggregate
several sessions and/or subjects, the derivatives-specific
[`tpl-<label>` entity](../appendices/entities.md#tpl) indicates that the
spatial frame of analysis is not defined by a single brain image but an
aggregation thereof.

!!! tip "Recommendation"

    The selected `<label>` in the [`tpl-<label>` entity](../appendices/entities.md#tpl)
    is RECOMMENDED for the [`space-<label>` entity](../appendices/entities.md#space)
    in downstream derivatives from this particular template (see previous section
    [Derivatives from atlases](imaging.md#derivatives-from-atlases)).

Template:

```Text
<pipeline_name>/
    tpl-<label>/
        [cohort-<label>/]
           [<datatype>/]
               tpl-<label>[_cohort-<label>][_<entities>]_<suffix>.<extension>
```

where [`suffix`](../glossary.md#suffix-common_principles) is any valid BIDS suffix
such as `T1w` or `PET`; and
[`extension`](../glossary.md#extension-common_principles) is a valid BIDS extension
such as `nii[.gz]`, `dscalar.nii[.gz]`, `dlabel.nii[.gz]`, `label.gii`, `tsv`, or `json`.
Templates and atlases do not establish new suffixes or extensions,
but any valid BIDS/BIDS Derivatives filename is permitted in a template directory,
substituting `tpl` for `sub` and `cohort` for `ses`.

The [`<datatype>/` directory](../glossary.md#data_type-common_principles) MAY be omitted in the case
only one data type (such as `anat/`) is stored under the `tpl-<label>/` directory.

The [`cohort-<label>` directory and entity](../appendices/entities.md#cohort) MUST be specified for templates
with several cohorts.

!!! note "Dataset structure"

    In templates/atlases the [`tpl-<label>`](../appendices/entities.md#tpl) and
    [`cohort-<label>`](../appendices/entities.md#cohort) entities are structurally
    analogous to the [`sub-<label>`](../appendices/entities.md#sub)
    and [`ses-<label>`](../appendices/entities.md#ses) entities,
    appearing as both directories and entities.
    The [`cohort-<label>`](../appendices/entities.md#cohort) entity is used
    to track mappings of arbitrary subject/session pairs.

In BIDS, a template is considered *any* aggregation of data and the `tpl-` entity
replaces the subject-level `sub-` entity when aggregating data across subjects.
The `tpl-` entity and `sub-` entity are mutually exclusive in a given file.
When the `tpl-` entity is used without the `atlas-` entity, as in the following examples,
the imaging data serves as an instantiation of a space.
When the `tpl-` entity is used in conjunction with the `atlas-` entity,
the intention is to describe aggregations of data in a particular space,
as described in the [Derived atlases](#derived-atlases) section, below.
For uses of the `atlas-` entity without the `tpl-` entity,
see [Imaging derivatives - Derivatives from atlases](imaging.md#derivatives-from-atlases).

### Example: Single-cohort template

For the pipeline that generated [`MNI152NLin2009cAsym`](../appendices/coordinate-systems.md#standard-template-identifiers),
the outputs could look like the following example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mni152nlin2009casym-pipeline": {
      "tpl-MNI152NLin2009cAsym": {
         "tpl-MNI152NLin2009cAsym_res-1_T1w.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-1_T1w.json": "",
         "tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.json": "",
         "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-1_probseg.json": "",
         "tpl-MNI152NLin2009cAsym_res-2_T1w.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-2_T1w.json": "",
         "tpl-MNI152NLin2009cAsym_res-2_label-brain_mask.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-2_label-brain_mask.json": "",
         "tpl-MNI152NLin2009cAsym_res-2_probseg.nii.gz": "",
         "tpl-MNI152NLin2009cAsym_res-2_probseg.json": "",
      },
   }
})
}}

### Example: Multi-cohort template

In the case that the template-generating pipeline derives
several cohorts, the file structure must employ the
[`cohort-<label>` directory and entity](../appendices/entities.md#cohort).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mnipediatricasym-pipeline": {
      "tpl-MNIPediatricAsym": {
         "cohort-1": {
            "tpl-MNIPediatricAsym_cohort-1_T1w.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-1_T2w.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-1_PDw.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-1_desc-brain_mask.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-1_probseg.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-1_probseg.json": "",
         },
         "...": "",
         "cohort-6": {
            "tpl-MNIPediatricAsym_cohort-6_T1w.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-6_T2w.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-6_PDw.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-6_desc-brain_mask.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-6_probseg.nii.gz": "",
            "tpl-MNIPediatricAsym_cohort-6_probseg.json": "",
         },
      },
   }
})
}}

### Example: Subject-level and template derivatives

Both subject-level and template-level results MAY coexist in a single derivatives dataset.
For example, it is possible to share the subject-level results used to generate the template
alongside the template:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mni152nlin2009casym-pipeline": {
      "sub-001": {
         "anat": {
            "sub-001_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5": "",
            "sub-001_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-001_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-152": {
         "anat": {
            "sub-152_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5": "",
            "sub-152_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-152_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.nii.gz": "",
         "...": "",
         "tpl-MNI152NLin2009cAsym_res-2_T1w.json": "",
      },
   }
})
}}

!!! warning "Warning"

    Please note that the specification for spatial transforms (BEP 014) is currently
    under development, and therefore, the specification of transforms files (`xfm` suffix above)
    may change in the future.

## Derived atlases

{{ MACROS___render_text('objects.common_principles.atlas.description') }}

### Atlas identification and metadata

The `atlas-<label>_description.json` file provides metadata to uniquely identify,
describe and characterize the atlas, as well as give proper attribution to the creators.
Atlases MUST include `atlas-<label>_description.json` files
corresponding to the atlas or atlases in the structure.

!!! tip "Recommendation"

    The selected `<label>` in the `atlas-<label>_description.json` file is RECOMMENDED
    for the [`atlas-<label>` entity](../appendices/entities.md#atlas)
    in downstream derivatives from this particular atlas (see previous section
    [Derivatives from atlases](imaging.md#derivatives-from-atlases)).

Template:

```Text
<pipeline_name>/
    atlas-<label>_description.json
    tpl-<label>/
        [cohort-<label>/]
           [<datatype>/]
               tpl-<label>[_cohort-<label>][_space-<label>][_atlas-<label>][_seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

Atlas metadata fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table('json.atlas.AtlasDescription') }}

Example `atlas-MyAtlas2025_description.json`:

```JSON
{
  "Name": "A new atlas of the human brain",
  "Authors": [
    "Jane Doe",
    "John Doe"
  ],
  "License": "CC0",
  "RRID": "SCR_002823",
  "Species": "Human"
}
```

Atlases are often aligned to a common spatial reference
to allow for the ready application of atlas data.
A file may indicate the spatial reference to which it has been aligned using the
[`tpl` entity](../appendices/entities.md#template) and/or the `SpatialReference` metadata.

The [`tpl` entity](../appendices/entities.md#template) may take any value in
[Image-Based Coordinate Systems][coordsys].

If the [`tpl` entity](../appendices/entities.md#template) is not in the
[Standard template identifiers][templates] table,
then the `SpatialReference` metadata is REQUIRED.

### Deriving templates and atlases

A common use-case of brain templates is establishing stereotaxy for the creation
of atlases.
For example, the *Spatially Unbiased Infratentorial Template* (*SUIT*;
[Diedrichsen, 2006](https://doi.org/10.1016/j.neuroimage.2006.05.056)),
presents an *atlas template* of the human cerebellum and brainstem based
on the anatomy of 20 young healthy individuals.

The authors first developed a template of the cerebellum and brainstem,
which is spatially standardized *in MNI space*.
This could be the organization of the template part:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "suit-pipeline": {
      "tpl-SUIT": {
         "anat": {
            "tpl-SUIT_T1w.nii.gz": "",
         },
      },
   }
})
}}

Once the standard space of analysis was prepared, a first atlas was
developed in 2009, integrating some segmentations and parcellations:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "suit-pipeline": {
      "atlas-Diedrichsen2009_description.json": "",
      "tpl-SUIT": {
         "anat": {
            "tpl-SUIT_T1w.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.json": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.tsv": "",
            "tpl-SUIT_atlas-Diedrichsen2009_probseg.nii.gz": "",
         },
      },
   }
})
}}

where `atlas-Diedrichsen2009_description.json` could contain:

```JSON
{
  "Name": "A probabilistic MR atlas of the human cerebellum",
  "Authors": [
     "Jörn Diedrichsen",
     "Joshua H Balsters",
     "Jonathan Flavell",
     "Emma Cussans",
     "Narender Ramnani"
  ],
  "Sample Size": 20,
  "License": "LICENSE file",
  "ReferencesAndLinks": [
     "https://doi.org/10.1016/j.neuroimage.2009.01.045",
     "https://github.com/jdiedrichsen/suit"
  ],
  "Species": "Human"
}
```

Finally, in 2011 a second atlas was developed integrating new segmentations.
Now, to disambiguate between the two atlases,
the [`atlas-<label>` entity](../appendices/entities.md#atlas) MUST be used:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "suit-pipeline": {
      "atlas-Buckner2011_description.json": "",
      "atlas-Diedrichsen2009_description.json": "",
      "tpl-SUIT": {
         "anat": {
            "tpl-SUIT_T1w.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_dseg.json": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_dseg.tsv": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_stat-confidence_probseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_dseg.tsv": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_stat-confidence_probseg.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.json": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.tsv": "",
            "tpl-SUIT_atlas-Diedrichsen2009_probseg.nii.gz": "",
         },
      },
   }
})
}}

where `atlas-Diedrichsen2009_description.json` remains as above,
and `atlas-Buckner2011_description.json` could contain:

```JSON
{
  "Name": "Atlas of the human cerebellum estimated by intrinsic functional connectivity",
  "Authors": [
     "Randy L Buckner",
     "Fenna M Krienen",
     "Angela Castellanos",
     "Julio C Diaz",
     "B T Thomas Yeo"
  ],
  "Sample Size": 1000,
  "License": "LICENSE file",
  "ReferencesAndLinks": [
     "https://doi.org/10.1152/jn.00339.2011",
     "https://github.com/jdiedrichsen/suit"
  ],
  "Species": "Human"
}
```

### Deriving a new atlas referenced in an existing template

For example, the `MIAL67ThalamicNuclei`
([Najdenovska et al., 2018](https://doi.org/10.1038/sdata.2018.270))
atlas-generation pipeline could display the following structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "atlas-MIAL67ThalamicNuclei_description.json": "",
      "sub-01": {
         "anat": {
            "sub-01_seg-ThalamicNuclei_dseg.json": "",
            "sub-01_seg-ThalamicNuclei_dseg.tsv": "",
            "sub-01_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_seg-ThalamicNuclei_dseg.json": "",
            "sub-67_seg-ThalamicNuclei_dseg.tsv": "",
            "sub-67_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_dseg.json": "",
            "tpl-MNI152NLin2009cAsym_dseg.tsv": "",
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

where the derivatives of anatomical processing of the 67 subjects that were
employed to generate the atlas coexist with the template structure.

The inheritance principle applies uniformly, allowing the segmentation
metadata be stored only once at the root of the pipeline directory and
apply to all the individual subject segmentations:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "seg-ThalamicNuclei_dseg.json": "",
      "seg-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "atlas-MIAL67ThalamicNuclei_description.json": "",
            "tpl-MNI152NLin2009cAsym_dseg.json": "",
            "tpl-MNI152NLin2009cAsym_dseg.tsv": "",
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

In the case the pipeline generated atlas-based segmentations of the original subjects in
their native T1w space (for example, to compare with the original segmentation given by
`seg-ThalamicNuclei`), the above example translates into:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "atlas-MIAL67ThalamicNuclei_description.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
      "seg-ThalamicNuclei_dseg.json": "",
      "seg-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_atlas-MIAL67ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_atlas-MIAL67ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

### Deriving one atlas from two or more existing templates

This directory structure can be generally applied when the atlas is derived into several
template spaces, for example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "atlas-MIAL67ThalamicNuclei_description.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
      "seg-ThalamicNuclei_dseg.json": "",
      "seg-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
      "tpl-MNI152NLin6Asym": {
         "anat": {
            "tpl-MNI152NLin6Asym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin6Asym_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

Without any loss in generality, we can store subjects' spatially normalizing
transforms, as well as transforms between template spaces:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "atlas-MIAL67ThalamicNuclei_description.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
      "seg-ThalamicNuclei_dseg.json": "",
      "seg-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5": "",
            "sub-01_from-T1w_to-MNI152NLin6Asym_mode-image_xfm.h5": "",
            "sub-01_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5": "",
            "sub-67_from-T1w_to-MNI152NLin6Asym_mode-image_xfm.h5": "",
            "sub-67_seg-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5": "",
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
      "tpl-MNI152NLin6Asym": {
         "anat": {
            "tpl-MNI152NLin6Asym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin6Asym_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}
