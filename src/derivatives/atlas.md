# Templates and atlases

In the following, we describe how the outcomes of analyses that derive from or
produce [templates and atlases](../common-principles.md#definitions) are organized
as BIDS-Derivatives.
These outcomes typically involve quantitative maps, feature maps, parcellations,
segmentations, and other knowledge annotations such as landmarks defined with
respect to individual or template brains that are supported by spaces
such as surfaces and regular grids (images).

For derivatives with atlases in their provenance corresponding to individual subjects,
the organization follows the standards for BIDS raw and derivatives.
The following entities MAY be employed to specify template- and atlas-derived results:

-    [`space-<label>`](../glossary.md#space-entities) is REQUIRED to disambiguate derivatives defined with
     respect to different [coordinate systems](../appendices/coordinate-systems.md), following the general
     BIDS-Derivatives specifications.
-    [`cohort-<label>`](../glossary.md#cohort-entities) is REQUIRED to disambiguate derivatives defined with
     respect to different cohort instances of a single [space (coordinate system)](../appendices/coordinate-systems.md).
-    [`atlas-<label>`](../glossary.md#atlas-entities) is REQUIRED to encode files pertaining
     or derived from the atlas identified by the entity's label.
-    [`seg-<label>`](../glossary.md#segmentation-entities) is REQUIRED when a single atlas has several different
     realizations (for instance, segmentations and parcellations created with different criteria) that
     need disambiguation.
-    [`scale-<label>`](../glossary.md#scale-entities) is REQUIRED to disambiguate different atlas 'scales',
     when the atlas has more than one 'brain unit' resolutions, typically relating to the area covered
     by regions.

The general filename pattern for subject derivatives with templates and atlases in their provenance
follows the general BIDS-Derivatives pattern:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_cohort-<label>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

[`atlas-<label>`](../glossary.md#atlas-entities), [`seg-<label>`](../glossary.md#segmentation-entities),
and [`scale-<label>`](../glossary.md#scale-entities) are discussed later in section
[Filenames of derivatives with atlases in their provenance](#filenames-of-derivatives-with-atlases-in-their-provenance).

For derivatives of template- and altas-generating pipelines, which typically aggregate
several sessions and/or subjects, the derivatives-specific
[`tpl-<label>` entity](../glossary.md#template-entities) is dual in terms of usage to BIDS raw's
[`sub-<label>`](../glossary.md#subject-entities), and MAY be employed as follows:

```Text
<pipeline_name>/
    tpl-<label>/
        [cohort-<label>/]
           [<datatype>/]
               tpl-<label>_<source_entities>[_cohort-<label>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

where [`suffix`](../glossary.md#suffix-common_principles) will generally be existing BIDS raw modalities
(such as `T1w`) for templates, while it will normally take `dseg`, `probseg`, or `mask` to encode atlased
knowledge.
In terms of [`extension`](../glossary.md#extension-common_principles), `nii[.gz]`, `dscalar.nii[.gz]`,
`dlabel.nii[.gz]`, `label.gii[.gz]`, `tsv`, or `json`.
Please note that the [`<datatype>/` directory](../glossary.md#data_type-common_principles) is RECOMMENDED.
The [`<datatype>/` directory](../glossary.md#data_type-common_principles) MAY be omitted in the case
only one data type (such as `anat/`) is stored under the `tpl-<label>` directory.
The [`cohort-<label>` directory and entity](../glossary.md#cohort-entities) MUST be specified for templates
with several cohorts.
The [`cohort-<label>` directory and entity](../glossary.md#cohort-entities) are dual in terms of usage to BIDS raw's
[`session-<label>`](../glossary.md#session-entities).
Both subject-level and template-level results can coexist in a single pipeline directory:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_cohort-<label>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
    tpl-<label>/
        [cohort-<label>/]
           [<datatype>/]
               <source_entities>[_cohort-<label>][_space-<space>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

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
         "anat": {
            "sub-01_label-brain_mask.nii.gz": "",
            "sub-01_label-head_mask.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
            "sub-01_T1w.json": "",
         },
      },
   }
})
}}

In the presence of conflicting files, for example, when there are several resolutions,
additional entities MUST be specified:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "colin27-pipeline": {
      "sub-01": {
         "anat": {
            "sub-01_res-1_label-brain_mask.nii.gz": "",
            "sub-01_res-1_label-head_mask.nii.gz": "",
            "sub-01_res-1_T1w.nii.gz": "",
            "sub-01_res-1_T1w.json": "",
            "sub-01_res-2_T1w.nii.gz": "",
            "sub-01_res-2_T1w.json": "",
         },
      },
   }
})
}}

## Multi-subject template and atlases and deriving an existing template/atlas

Atlasing multiple individual brains is a higher-than-first-level analysis,
as it requires first generating derivatives for the individuals (for example,
a transformation to align them into a standardized space) and later aggregate
and distill the sample-pooled knowledge and feature maps.
Similarly, deriving from an existing template and atlases is also
a higher-than-first-level analysis as it builds on a previous analysis.

**Multi-subject templates**.
While at the subject level analysis it is the individual brain that establishes
stereotaxy.
At higher-than-first-level stereotaxy is supported by templates, which are
encoded through the [`tpl-<label>` entity](../glossary.md#template-entities).
For the pipeline that generated the MNI152NLin2009cAsym, the outputs would look
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

**Multi-cohort templates.**
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

**Storing spatial transforms.**
Since multi-subject templates and atlas involve the spatial normalization of
subjects by means of image registration processes, it is RECOMMENDED to store
the resulting transforms for each of the subjects employed to create the
output.
Please note that the specification for spatial transforms (BEP 014) is currently
under development, and therefore, the specification of transforms files may
change in the future.
As these are subject-wise results, they follow the standard derivatives conventions
with a `sub-<label>` directory to house these derivatives:

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

**Defining atlases referenced to a pre-existing template.**
Once a standard space is instantiated by a reference template,
atlasing knowledge MAY be specified employing the
[`atlas-<label>` entity](../glossary.md#atlas-entities).

The following example shows how 'Colin27' could have encoded the Automated Anatomical Labeling (AAL)
atlas ([Tzourio-Mazoyer et al., 2002](https://doi.org/10.1006/nimg.2001.0978)), which was originally
defined on the Colin27 space:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "colin27-pipeline": {
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

As [the authors of 'Colin27' indicate](https://www.mcgill.ca/bic/software/tools-data-analysis/anatomical-mri/atlases/colin-27),
it is aligned with MNI305:

> In 1998, a new atlas with much higher definition than MNI305s was created at the MNI.
> One individual (CJH) was scanned 27 times and the images linearly registered to create
> an average with high SNR and structure definition (Holmes et al., 1998).
> This average was linearly registered to the average 305.
> Ironically, this dataset was not originally intended for use as a stereotaxic template
> but as the sub-strate for an ROI parcellation scheme to be used with
> ANIMAL non-linear spatial normalization (Collins et al., 1995),
> i.e. it was intended for the purpose of segmentation, NOT stereotaxy.
> As a single brain atlas, it did not capture anatomical variability and was, to some degree,
> a reversion to the Talairach approach.
>
> However, the high definition proved too attractive to the community and,
> after non-linear mapping to fit the MNI305 space, it has been adopted
> by many groups as a stereotaxic template.

Therefore, this pipeline potentially could have produced outputs in the realigned T1w space
before alignment to the MNI305 template.
To disambiguate in this case, we employ the [`space-<label>` entity](../glossary.md#space-entities):

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "colin27-pipeline": {
      "sub-01": {
         "anat": {
            "sub-01_space-MNI305_atlas-AAL_dseg.json": "",
            "sub-01_space-MNI305_atlas-AAL_dseg.nii.gz": "",
            "sub-01_space-MNI305_atlas-AAL_dseg.tsv": "",
            "sub-01_space-MNI305_atlas-AAL_probseg.nii.gz": "",
            "sub-01_space-MNI305_label-brain_mask.nii.gz": "",
            "sub-01_space-MNI305_label-head_mask.nii.gz": "",
            "sub-01_space-MNI305_T1w.nii.gz": "",
            "sub-01_space-MNI305_T1w.json": "",
            "sub-01_space-T1w_label-brain_mask.nii.gz": "",
            "sub-01_space-T1w_label-head_mask.nii.gz": "",
            "sub-01_space-T1w_T1w.nii.gz": "",
            "sub-01_space-T1w_T1w.json": "",
         },
      },
   }
})
}}

For example, the [PS13 atlas](https://doi.org/10.18112/openneuro.ds004401.v1.3.0),
a molecular imaging brain atlas of Cyclooxygenase-1 (PET),
was generated in two standard spaces: `MNI152Lin` and `fsaverage`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "ps13-pipeline": {
      "tpl-fsaverage": {
         "pet": {
            "tpl-fsaverage_atlas-ps13_desc-nopvc_dseg.nii.gz": "",
            "tpl-fsaverage_atlas-ps13_desc-pvc_dseg.nii.gz": "",
            "tpl-fsaverage_atlas-ps13_dseg.json": "",
            "tpl-fsaverage_atlas-ps13_dseg.tsv": "",
            "tpl-fsaverage_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_desc-nopvc_mimap.nii.gz": "",
            "tpl-fsaverage_desc-pvc_mimap.json": "",
            "tpl-fsaverage_desc-pvc_mimap.nii.gz": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-nopvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-pvc_mimap.json": "",
            "tpl-fsaverage_hemi-L_den-164k_desc-pvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-nopvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-pvc_mimap.json": "",
            "tpl-fsaverage_hemi-L_den-164k_stat-std_desc-pvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-nopvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-pvc_mimap.json": "",
            "tpl-fsaverage_hemi-R_den-164k_desc-pvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-nopvc_mimap.shape.gii": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-pvc_mimap.json": "",
            "tpl-fsaverage_hemi-R_den-164k_stat-std_desc-pvc_mimap.shape.gii": "",
            "tpl-fsaverage_stat-std_desc-nopvc_mimap.json": "",
            "tpl-fsaverage_stat-std_desc-nopvc_mimap.nii.gz": "",
            "tpl-fsaverage_stat-std_desc-pvc_mimap.json": "",
            "tpl-fsaverage_stat-std_desc-pvc_mimap.nii.gz": "",
         },
      },
      "tpl-MNI152Lin": {
         "pet": {
            "tpl-MNI152Lin_atlas-ps13_desc-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_desc-pvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.json": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.tsv": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmNopvc_mimap.json": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmNopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmPvc_mimap.json": "",
            "tpl-MNI152Lin_res-1p5_desc-spmvbmPvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmNopvc_mimap.json": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmNopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmPvc_mimap.json": "",
            "tpl-MNI152Lin_res-1p5_stat-std_desc-spmvbmPvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-fnirtNopvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_desc-fnirtNopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-fnirtPvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_desc-fnirtPvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-nopvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_desc-nopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_desc-pvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_desc-pvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtNopvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtNopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtPvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-fnirtPvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-nopvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-nopvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-pvc_mimap.json": "",
            "tpl-MNI152Lin_res-2_stat-std_desc-pvc_mimap.nii.gz": "",
         },
      }
   }
})
}}

If the pipeline generates two different atlases for at least one template space
in the output, then [`atlas-<label>`](../glossary.md#atlas-entities) is REQUIRED
for the whole dataset.
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
      "tpl-fsaverage": {
         "pet": {
            "tpl-fsaverage_atlas-ps13_desc-nopvc_dseg.nii.gz": "",
            "tpl-fsaverage_atlas-ps13_desc-pvc_dseg.nii.gz": "",
            "tpl-fsaverage_atlas-ps13_dseg.json": "",
            "tpl-fsaverage_atlas-ps13_dseg.tsv": "",
            "tpl-fsaverage_atlas-ps13_hemi-L_den-164k_desc-nopvc_mimap.json": "",
            "...": "",
            "tpl-fsaverage_atlas-ps13_stat-std_desc-pvc_mimap.nii.gz": "",
         },
      },
      "tpl-MNI152Lin": {
         "pet": {
            "tpl-MNI152Lin_atlas-ps13_desc-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_desc-pvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.json": "",
            "tpl-MNI152Lin_atlas-ps13_dseg.tsv": "",
            "tpl-MNI152Lin_atlas-ps13_res-1p5_desc-spmvbmNopvc_mimap.json": "",
            "...": "",
            "tpl-MNI152Lin_atlas-ps13_res-2_stat-std_desc-pvc_mimap.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_desc-nopvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_desc-pvc_dseg.nii.gz": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_dseg.json": "",
            "tpl-MNI152Lin_atlas-ps13rev2034_dseg.tsv": "",
         },
      }
   }
})
}}

**Producing a new template AND atlas.**
Atlasing is often performed with reference to a *custom* standard space.
In this case, a feature template map is generated from all the participant(s)
in the study, and the atlas' artifacts are produced with reference to that
template.

Either by generating the template space with aligning to a pre-existing template,
or by estimating a transform between templates by means of image registration,
a new template definition MUST be employed if the new template generates
a new [*space*](../common-principles.md#definitions).
For example, let's imagine that PS13 first generated a template nuclear imaging
map and after that, a corresponding [*atlas*](../common-principles.md#definitions)
was defined.
In that case, the [`atlas-<label>`](../glossary.md#atlas-entities) SHOULD be omitted
except several atlases need specification:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "ps13-pipeline": {
      "tpl-PS13": {
         "pet": {
            "tpl-PS13_desc-nopvc_dseg.nii.gz": "",
            "tpl-PS13_desc-pvc_dseg.nii.gz": "",
            "tpl-PS13_dseg.json": "",
            "tpl-PS13_dseg.tsv": "",
            "tpl-PS13_stat-std_desc-fnirtNopvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-fnirtNopvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-fnirtPvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-fnirtPvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-nopvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-nopvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-pvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-pvc_mimap.nii.gz": "",
         },
      },
   }
})
}}

Let's complete the above example by adding two new atlases to the existing
template and (*default*) atlas:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "ps13-with-atlases-pipeline": {
      "tpl-PS13": {
         "pet": {
            "tpl-PS13_atlas-Economo1916_desc-nopvc_dseg.nii.gz": "",
            "tpl-PS13_atlas-Economo1916_desc-pvc_dseg.nii.gz": "",
            "tpl-PS13_atlas-Economo1916_dseg.json": "",
            "tpl-PS13_atlas-Economo1916_dseg.tsv": "",
            "tpl-PS13_atlas-RamonCajal1908_desc-nopvc_dseg.nii.gz": "",
            "tpl-PS13_atlas-RamonCajal1908_desc-pvc_dseg.nii.gz": "",
            "tpl-PS13_atlas-RamonCajal1908_dseg.json": "",
            "tpl-PS13_atlas-RamonCajal1908_dseg.tsv": "",
            "tpl-PS13_desc-nopvc_dseg.nii.gz": "",
            "tpl-PS13_desc-pvc_dseg.nii.gz": "",
            "tpl-PS13_dseg.json": "",
            "tpl-PS13_dseg.tsv": "",
            "tpl-PS13_stat-std_desc-fnirtNopvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-fnirtNopvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-fnirtPvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-fnirtPvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-nopvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-nopvc_mimap.nii.gz": "",
            "tpl-PS13_stat-std_desc-pvc_mimap.json": "",
            "tpl-PS13_stat-std_desc-pvc_mimap.nii.gz": "",
         },
      },
   }
})
}}

where the `atlas-RamonCajal1908` and `atlas-Economo1916` hypothetically define
two different atlases (please note that, often, atlases are named after
the first author and indicating a year of a reference communication).
The original *default* or *implicit* atlas' artifacts such as
the `tpl-PS13_desc-nopvc_dseg.nii.gz` segmentation,
which were originally generated with the PS13 template,
MAY take an [`atlas-<label>`](../glossary.md#atlas-entities) if they
need to be differentiated from the original template and atlas dataset.
However, it is RECOMMENDED that these *default* or *implicit* atlases employed
in the *custom* space they were generated only define
[`atlas-<label>`](../glossary.md#atlas-entities)
if it is necessary to disambiguate two or more atlases.

A further example of these template-and-atlas specifications
is the *Spatially Unbiased Infratentorial Template (SUIT)*
([Diedrichsen, 2006](https://doi.org/10.1016/j.neuroimage.2006.05.056)):

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "suit-pipeline": {
      "tpl-SUIT": {
         "anat": {
            "CHANGES": "",
            "LICENSE": "",
            "README.md": "",
            "dataset_description.json": "",
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

In this case, a new T1w template of the cerebellum was created, and two different
atlases (`Diedrichsen2009`, and `Buckner2011`) were generated with respect to
the T1w template.

**Deriving from an existing template/atlas**.
For example, the MIAL67ThalamicNuclei
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
            "sub-01_label-ThalamicNuclei_dseg.json": "",
            "sub-01_label-ThalamicNuclei_dseg.tsv": "",
            "sub-01_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_label-ThalamicNuclei_dseg.json": "",
            "sub-67_label-ThalamicNuclei_dseg.tsv": "",
            "sub-67_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.json": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
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
      "label-ThalamicNuclei_dseg.json": "",
      "label-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.json": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

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
      "label-ThalamicNuclei_dseg.json": "",
      "label-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
         },
      },
      "tpl-MNI152NLin6Asym": {
         "anat": {
            "tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

In the case the pipeline generated atlas-based segmentations of the original subjects in
their native T1w space (for example, to compare with the original segmentation given by
`label-ThalamicNuclei`), the above example translates into:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "mial67thalamicnuclei-pipeline": {
      "atlas-MIAL67ThalamicNuclei_dseg.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
      "label-ThalamicNuclei_dseg.json": "",
      "label-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_atlas-MIAL67ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-01_T1w.nii.gz": "",
         },
      },
      "...": "",
      "sub-67": {
         "anat": {
            "sub-67_atlas-MIAL67ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
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
      "atlas-MIAL67ThalamicNuclei_dseg.json": "",
      "atlas-MIAL67ThalamicNuclei_dseg.tsv": "",
      "label-ThalamicNuclei_dseg.json": "",
      "label-ThalamicNuclei_dseg.tsv": "",
      "sub-01": {
         "anat": {
            "sub-01_from-T1w_to-MNI152NLin2009cAsym_mode-image_xfm.h5": "",
            "sub-01_from-T1w_to-MNI152NLin6Asym_mode-image_xfm.h5": "",
            "sub-01_label-ThalamicNuclei_dseg.nii.gz": "",
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
            "sub-67_label-ThalamicNuclei_dseg.nii.gz": "",
            "sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz": "",
            "sub-67_space-MNI152NLin6Asym_T1w.nii.gz": "",
            "sub-67_T1w.nii.gz": "",
         },
      },
      "tpl-MNI152NLin2009cAsym": {
         "anat": {
            "tpl-MNI152NLin2009cAsym_from-MNI152NLin6Asym_mode-image_xfm.h5": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
         },
      },
      "tpl-MNI152NLin6Asym": {
         "anat": {
            "tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz": "",
            "tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz": "",
         },
      },
   }
})
}}

The next subsection describes this latter use-case in further depth.

## Filenames of derivatives with atlases in their provenance

Like for the [`space-<label>` entity](../glossary.md#space-entities),
outputs derived from atlases MUST employ
[`atlas-<label>`](../glossary.md#atlas-entities),
[`seg-<label>`](../glossary.md#segmentation-entities), and
[`scale-<label>`](../glossary.md#scale-entities) when necessary:

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
   }
})
}}

## Tabular data

The `[probseg|dseg|mask].tsv` file indexes and labels each node/parcel/region within the atlas.
This file resembles the typical Look Up Table (LUT) often shared with atlases.
This file will be essential for downstream workflows that generate matrices or other derived files within which node/parcel/region information is required,
as the index/label fields will be used to reference the original anatomy the index/labels are derived from.
Additional fields can be added with their respective definition/description in the sidecar json file.

This is described in the [imaging derivatives](./imaging.md#common-image-derived-labels) section of the BIDS specification

Example:
```Text
index	label	network_label	hemisphere
1	Heschl's Gyrus	Somatomotor	left
2	Heschl's Gyrus	Somatomotor	right
```

## Atlas metadata

The `atlas-<label>_description.json` file provides metadata to uniquely identify, describe and characterize the atlas, as well as give proper attribution to the creators.
Additionally, SpatialReference serves the important purpose of unambiguously identifying the space the atlas is labeled in.

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

Example:

```JSON
{
  "Name": "FSL's MNI ICBM 152 non-linear 6th Generation Asymmetric Average Brain Stereotaxic Registration Model",
  "Authors": [
    "David Kennedy",
    "Christian Haselgrove",
    "Bruce Fischl",
    "Janis Breeze",
    "Jean Frazie",
    "Larry Seidman",
    "Jill Goldstein"
  ],
  "BIDSVersion": "1.1.0",
  "Curators": "FSL team",
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
  "Resolution": "Matched with original template resolution (2x2x3 mm^3)",
  "License": "See LICENSE file",
  "RRID": "SCR_002823",
  "ReferencesAndLinks": [
    "https://doi.org/10.1016/j.neuroimage.2012.01.024",
    "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases"
  ],
  "Species": "Human"
}
```
