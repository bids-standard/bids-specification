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
[`tpl-<label>` entity](../glossary.md#template-entities) indicates that the
spatial frame of analysis is not defined by a single brain image but an
aggregation thereof.
On that sense, the [`tpl-<label>` entity](../glossary.md#template-entities)
would be dual in terms of usage to BIDS raw's [`sub-<label>`](../glossary.md#subject-entities).

!!! tip "Recommendation"

    The selected `<label>` in the [`tpl-<label>` entity](../glossary.md#template-entities)
    is RECOMMENDED for the [`space-<label>` entity](../appendices/entities.md#space-entities)
    in downstream derivatives from this particular template (see previous section
    [Derivatives from atlases](imaging.md#derivatives-from-atlases)).

Template:

```Text
<pipeline_name>/
    tpl-<label>/
        [cohort-<label>/]
           [<datatype>/]
               tpl-<label>_[cohort-<label>][_space-<label>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

where [`suffix`](../glossary.md#suffix-common_principles) SHOULD be an existing BIDS modality
such as `T1w` or `PET`.
[`extension`](../glossary.md#extension-common_principles), MAY take values such as `nii[.gz]`, `dscalar.nii[.gz]`,
`dlabel.nii[.gz]`, `label.gii[.gz]`, `tsv`, or `json`.

Please note that the [`<datatype>/` directory](../glossary.md#data_type-common_principles) is RECOMMENDED.
The [`<datatype>/` directory](../glossary.md#data_type-common_principles) MAY be omitted in the case
only one data type (such as `anat/`) is stored under the `tpl-<label>` directory.

The [`cohort-<label>` directory and entity](../glossary.md#cohort-entities) MUST be specified for templates
with several cohorts.
The [`cohort-<label>` directory and entity](../glossary.md#cohort-entities) are dual in terms of usage to BIDS raw's
[`session-<label>`](../glossary.md#session-entities).

**Example: the `MNI152NLin2009cAsym` template**.
For the pipeline that generated the MNI152NLin2009cAsym, the outputs could look
like the following example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mni152nlin2009casym-pipeline": {
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-eye_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-face_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-head_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-CSF_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-GM_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_label-WM_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_T1w.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_T1w.json": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-brain_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-eye_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-face_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-head_mask.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-CSF_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-GM_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_label-WM_probseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_T1w.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-2_T1w.json": "",
         },
      },
   }
})
}}

**Example: multi-cohort templates.**
In the case that the template-generating pipeline derives
several cohorts, the file structure must employ the
[`cohort-<label>` directory and entity](../glossary.md#cohort-entities).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mnipediatricasym-pipeline": {
      "tpl-MNIPediatricAsym": {
         "cohort-1": {
            "anat": {
               "tpl-MNIPediatricAsym_cohort-1_res-1_PD.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_T1w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_T2w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_desc-brain_mask.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_label-CSF_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_label-GM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-1_label-WM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_PD.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_T1w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_T2w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_desc-brain_mask.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_label-CSF_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_label-GM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-1_res-2_label-WM_probseg.nii.gz": "",
            },
         },
         "...": "",
         "cohort-6": {
            "anat": {
               "tpl-MNIPediatricAsym_cohort-6_res-1_PD.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_T1w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_T2w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_desc-brain_mask.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_label-CSF_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_label-GM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-1_label-WM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_PD.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_T1w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_T2w.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_desc-brain_mask.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_label-CSF_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_label-GM_probseg.nii.gz": "",
               "tpl-MNIPediatricAsym_cohort-6_res-2_label-WM_probseg.nii.gz": "",
            },
         },
      },
   }
})
}}

**Subject-level and template derivatives**.
Both subject-level and template-level results MAY coexist in a single pipeline directory.
If the subject-level results based on which a template was generated are to be
shared with the template, it is RECOMMENDED to store both families of results within the
pipeline directory:

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
         "anat": {
            "tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.nii.gz": "",
            "...": "",
            "tpl-MNI152NLin2009cAsym_res-2_T1w.json": "",
         },
      },
   }
})
}}

!!! warning "Warning"

    Please note that the specification for spatial transforms (BEP 014) is currently
    under development, and therefore, the specification of transforms files may
    change in the future.

## Derived atlases

### Atlas identification and metadata

The `atlas-<label>_description.json` file provides metadata to uniquely identify,
describe and characterize the atlas, as well as give proper attribution to the creators.
Atlases MUST include `atlas-<label>_description.json` files
corresponding to the atlas or atlases in the structure.

!!! tip "Recommendation"

    The selected `<label>` in the `atlas-<label>_description.json` file is RECOMMENDED
    for the [`atlas-<label>` entity](../appendices/entities.md#atlas-entities)
    in downstream derivatives from this particular atlas (see previous section
    [Derivatives from atlases](imaging.md#derivatives-from-atlases)).

Template:

```Text
<pipeline_name>/
    tpl-<label>/
        atlas-<label>_description.json
        [cohort-<label>/]
           [<datatype>/]
               tpl-<label>_[cohort-<label>][_space-<label>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

Atlas metadata fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "derivatives.common_derivatives.AtlasDescription",
   ]) }}

Additionally, `SpatialReference` serves the important purpose of unambiguously identifying
the space the atlas is labeled in.

Example `atlas-MyAtlas2025_description.json`:

```JSON
{
  "Name": "A new atlas of the human brain",
  "Authors": [
    "Jane Doe",
    "John Doe"
  ],
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
  "License": "CC0",
  "RRID": "SCR_002823",
  "Species": "Human"
}
```

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
            "tpl-SUIT_flat.surf.gii": "",
            "tpl-SUIT_sulc.shape.gii": "",
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
      "tpl-SUIT": {
         "anat": {
            "atlas-Dietrich2009_description.json": "",
            "tpl-SUIT_T1w.nii.gz": "",
            "tpl-SUIT_dseg.json": "",
            "tpl-SUIT_dseg.label.gii": "",
            "tpl-SUIT_dseg.nii.gz": "",
            "tpl-SUIT_dseg.tsv": "",
            "tpl-SUIT_probseg.nii.gz": "",
            "tpl-SUIT_flat.surf.gii": "",
            "tpl-SUIT_sulc.shape.gii": "",
         },
      },
   }
})
}}

where `atlas-Dietrich2009_description.json` could contain:

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
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152Lin_res-01_T1w.nii.gz",
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
the [`atlas-<label>` entity](../appendices/entities.md#atlas-entities) MUST be used:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "suit-pipeline": {
      "tpl-SUIT": {
         "anat": {
            "atlas-Buckner2011_description.json": "",
            "atlas-Dietrich2009_description.json": "",
            "tpl-SUIT_T1w.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_dseg.json": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_dseg.label.gii": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_dseg.tsv": "",
            "tpl-SUIT_atlas-Buckner2011_seg-17n_stat-confidence_probseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_dseg.label.gii": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_dseg.tsv": "",
            "tpl-SUIT_atlas-Buckner2011_seg-7n_stat-confidence_probseg.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.json": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.label.gii": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.nii.gz": "",
            "tpl-SUIT_atlas-Diedrichsen2009_dseg.tsv": "",
            "tpl-SUIT_atlas-Diedrichsen2009_probseg.nii.gz": "",
            "tpl-SUIT_flat.surf.gii": "",
            "tpl-SUIT_sulc.shape.gii": "",
         },
      },
   }
})
}}

### Deriving an atlas from an existing template

For example, the `MIAL67ThalamicNuclei`
([Najdenovska et al., 2018](https://doi.org/10.1038/sdata.2018.270))
atlas-generation pipeline could display the following structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
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
            "atlas-MIAL67ThalamicNuclei_description.json": "",
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
            "atlas-MIAL67ThalamicNuclei_description.json": "",
            "tpl-MNI152NLin2009cAsym_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_res-1_probseg.nii.gz": "",
         },
      },
      "tpl-MNI152NLin6Asym": {
         "anat": {
            "atlas-MIAL67ThalamicNuclei_description.json": "",
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

**A more comprehensive example.**
For example, the [PS13 atlas](https://doi.org/10.18112/openneuro.ds004401.v1.3.0),
a molecular imaging brain atlas of Cyclooxygenase-1 (PET),
was generated in two standard spaces: `MNI152Lin` and `fsaverage`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "ps13-pipeline": {
      "atlas-ps13_description.json": "",
      "tpl-fsaverage": {
         "pet": {
            "tpl-fsaverage_desc-nopvc_pet.json": "",
            "tpl-fsaverage_desc-nopvc_pet.nii.gz": "",
            "tpl-fsaverage_desc-pvc_pet.json": "",
            "tpl-fsaverage_desc-pvc_pet.nii.gz": "",
            "tpl-fsaverage_dseg.json": "",
            "tpl-fsaverage_dseg.tsv": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-nopvc_pet.json": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-nopvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-pvc_pet.json": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-pvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-nopvc_pet.json": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-nopvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-pvc_pet.json": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-pvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-nopvc_pet.json": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-nopvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-pvc_pet.json": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-pvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-nopvc_pet.json": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-nopvc_pet.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-pvc_pet.json": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-pvc_pet.shape.gii": "",
            "tpl-fsaverage_seg-nopvc_dseg.nii.gz": "",
            "tpl-fsaverage_seg-pvc_dseg.nii.gz": "",
            "tpl-fsaverage_stat-std_desc-nopvc_pet.json": "",
            "tpl-fsaverage_stat-std_desc-nopvc_pet.nii.gz": "",
            "tpl-fsaverage_stat-std_desc-pvc_pet.json": "",
            "tpl-fsaverage_stat-std_desc-pvc_pet.nii.gz": "",
         },
      },
      "tpl-MNI152Lin": {
         "pet": {
            "tpl-MNI152Lin_dseg.json": "",
            "tpl-MNI152Lin_dseg.tsv": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmNopvc_pet.json": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmNopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmPvc_pet.json": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmPvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmNopvc_pet.json": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmNopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmPvc_pet.json": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmPvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-fnirtNopvc_pet.json": "",
            "tpl-MNI152Lin_res-2_desc-fnirtNopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-fnirtPvc_pet.json": "",
            "tpl-MNI152Lin_res-2_desc-fnirtPvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-nopvc_pet.json": "",
            "tpl-MNI152Lin_res-2_desc-nopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-pvc_pet.json": "",
            "tpl-MNI152Lin_res-2_desc-pvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtNopvc_pet.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtNopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtPvc_pet.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtPvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-nopvc_pet.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-nopvc_pet.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-pvc_pet.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-pvc_pet.nii.gz": "",
            "tpl-MNI152Lin_seg-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_seg-pvc_dseg.nii.gz": "",
         },
      }
   }
})
}}

If the pipeline generates two different atlases for at least one template space
in the output, then [`atlas-<label>`](../glossary.md#atlas-entities) is REQUIRED
for disambiguation.
For example, let's imagine the PS13 atlas is revised in 2034, and based on the
original pipeline and data, it generates now a new manual segmentation
in the `MNI152Lin` space with some new regions defined.
The new atlas can be structured as follows:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "ps13rev2034-pipeline": {
      "atlas-ps13_description.json": "",
      "tpl-fsaverage": {
         "pet": {
            "tpl-fsaverage_seg-nopvc_dseg.nii.gz": "",
            "tpl-fsaverage_seg-pvc_dseg.nii.gz": "",
            "tpl-fsaverage_dseg.json": "",
            "tpl-fsaverage_dseg.tsv": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-nopvc_pet.json": "",
            "...": "",
            "tpl-fsaverage_stat-std_desc-pvc_pet.nii.gz": "",
         },
      },
      "tpl-MNI152Lin": {
         "pet": {
            "atlas-ps13rev2034_description.json": "",
            "tpl-MNI152Lin_atlas-ps13_seg-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_seg-pvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.json": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.tsv": "",
            "tpl-MNI152Lin_atlas-ps13_res-1p5_desc-spmvbmNopvc_pet.json": "",
            "...": "",
            "tpl-MNI152Lin_atlas-ps13_res-2_stat-std_desc-pvc_pet.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_seg-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_seg-pvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_dseg.json": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_dseg.tsv": "",
         },
      }
   }
})
}}

## Single-subject templates and atlases

Early digital templates and atlases such as MNI's
'[Colin 27 Average Brain, Stereotaxic Registration Model](https://www.mcgill.ca/bic/software/tools-data-analysis/anatomical-mri/atlases/colin-27)'
([Holmes et al., 1998](https://doi.org/10.1097/00004728-199803000-00032)) were built by examining single individuals.
For example, the outputs of the pipeline that generated 'Colin27' would have been organized as follows:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "colin27-pipeline": {
      "sub-01": {
         "ses-01": {
            "anat": {
               "sub-01_ses-01_label-brain_mask.nii.gz": "",
               "sub-01_ses-01_label-head_mask.nii.gz": "",
               "sub-01_ses-01_T1w.nii.gz": "",
               "sub-01_ses-01_T1w.json": "",
            },
         },
         "ses-02": {
            "anat": {
               "sub-01_ses-02_label-brain_mask.nii.gz": "",
               "sub-01_ses-02_label-head_mask.nii.gz": "",
               "sub-01_ses-02_T1w.nii.gz": "",
               "sub-01_ses-02_T1w.json": "",
            },
         },
         "...": "",
         "ses-27": {
            "anat": {
               "sub-01_ses-27_label-brain_mask.nii.gz": "",
               "sub-01_ses-27_label-head_mask.nii.gz": "",
               "sub-01_ses-27_T1w.nii.gz": "",
               "sub-01_ses-27_T1w.json": "",
            },
         },
      },
      "tpl-Colin27": {
         "anat": {
            "atlas-AAL_description.json": "",
            "tpl-Colin27_atlas-AAL_dseg.json": "",
            "tpl-Colin27_atlas-AAL_dseg.nii.gz": "",
            "tpl-Colin27_atlas-AAL_dseg.tsv": "",
            "tpl-Colin27_atlas-AAL_probseg.nii.gz": "",
            "tpl-Colin27_label-brain_mask.nii.gz": "",
            "tpl-Colin27_label-head_mask.nii.gz": "",
            "tpl-Colin27_T1w.nii.gz": "",
            "tpl-Colin27_T1w.json": "",
         },
      },
   }
})
}}

where the atlas *AAL* has been added to the structure.
Note that names contain `atlas-AAL` even though no other atlases
are present to disambiguate the two brain and head masks that
are not derived from *AAL*.
