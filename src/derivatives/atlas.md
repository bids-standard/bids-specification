# Templates and atlases

In the following we describe how the outcomes of analyses that produce new
templates and [atlases](../glossary.md#atlas-entities) are organized
as BIDS-Derivatives.
These outcomes typically involve quantitative maps, feature maps, parcellations,
segmentations, and other knowledge annotations such as landmarks defined with
respect to individual or template brains that are supported by spaces
such as surfaces and regular grids (images).
Templates and atlases follow BIDS raw and derivatives specifications to store
these outcomes:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_atlas-<label>][seg-<label>][_scale-<label>][_res-<label>][_den-<label>][_desc-<label>]_<suffix>.<extension>
```

Template's [`suffix`](../glossary.md#suffix-common_principles) will generally be existing BIDS raw modalities
such as `T1w`, while it will normally take `dseg`, `probseg`, or `mask` to encode atlased knowledge.
In terms of [`extension`](../glossary.md#extension-common_principles), `nii[.gz]`, `dscalar.nii[.gz]`,
`dlabel.nii[.gz]`, `label.gii[.gz]`, `tsv`, or `json`.

The [`atlas-<label>` entity](../glossary.md#atlas-entities) is REQUIRED to encode files belonging in
the atlas identified by the label.
Two entities MAY be employed along with `atlas-` to disentangle different realizations and scales
of a single atlas:

-    [`seg-<label>`](../glossary.md#segmentation-entities) is REQUIRED when a single atlas has several different
     realizations (for instance, segmentations and parcellations created with different criteria) that
     need disambiguation.
-    [`scale-<label>`](../glossary.md#scale-entities) is REQUIRED to disambiguate different atlas 'scales',
     when the atlas has more than one 'brain unit' resolutions, typically relating to the area covered
     by regions.

These three atlas-related entities are discussed later in section [#atlas-filenames-specifications].

## Single-subject templates and atlases

Early digital templates and atlases such as MNI's
'[Colin 27 Average Brain, Stereotaxic Registration Model](https://www.mcgill.ca/bic/software/tools-data-analysis/anatomical-mri/atlases/colin-27)'
([Holmes et al., 1998](https://doi.org/10.1097/00004728-199803000-00032)) were built by examining single individuals.
For example, the outputs of the pipeline that generated 'Colin27' would have been organized as follows:

```Text
colin27-pipeline/
└─ sub-01/
   └─ anat/
      ├─ sub-01_label-brain_mask.nii.gz
      ├─ sub-01_label-head_mask.nii.gz
      ├─ sub-01_T1w.nii.gz
      └─ sub-01_T1w.json
```

In the presence of conflicting files, for example, when there are several resolutions,
additional entities MUST be specified:

```Text
colin27-pipeline/
└─ sub-01/
   └─ anat/
      ├─ sub-01_res-1_label-brain_mask.nii.gz
      ├─ sub-01_res-1_label-head_mask.nii.gz
      ├─ sub-01_res-1_T1w.nii.gz
      ├─ sub-01_res-1_T1w.json
      ├─ sub-01_res-2_T1w.nii.gz
      └─ sub-01_res-2_T1w.json
```

Often, templates are necessary to bring or project information from/to an atlas.
Derivatives provenant from an atlas MUST be encoded with the
[`atlas-<label>` entity](../glossary.md#atlas-entities).
The following example shows how 'Colin27' could have encoded the Automated Anatomical Labeling (AAL)
atlas ([Tzourio-Mazoyer et al., 2002](https://doi.org/10.1006/nimg.2001.0978)), which was originally
defined on the Colin27 space:

```Text
colin27-pipeline/
└─ sub-01/
   └─ anat/
      ├─ sub-01_atlas-AAL_dseg.json
      ├─ sub-01_atlas-AAL_dseg.nii.gz
      ├─ sub-01_atlas-AAL_dseg.tsv
      ├─ sub-01_atlas-AAL_probseg.nii.gz
      ├─ sub-01_label-brain_mask.nii.gz
      ├─ sub-01_label-head_mask.nii.gz
      ├─ sub-01_T1w.nii.gz
      └─ sub-01_T1w.json
```

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

```Text
colin27-pipeline/
└─ sub-01/
   └─ anat/
      ├─ sub-01_space-MNI305_atlas-AAL_dseg.json
      ├─ sub-01_space-MNI305_atlas-AAL_dseg.nii.gz
      ├─ sub-01_space-MNI305_atlas-AAL_dseg.tsv
      ├─ sub-01_space-MNI305_atlas-AAL_probseg.nii.gz
      ├─ sub-01_space-MNI305_label-brain_mask.nii.gz
      ├─ sub-01_space-MNI305_label-head_mask.nii.gz
      ├─ sub-01_space-MNI305_T1w.nii.gz
      ├─ sub-01_space-MNI305_T1w.json
      ├─ sub-01_space-T1w_label-brain_mask.nii.gz
      ├─ sub-01_space-T1w_label-head_mask.nii.gz
      ├─ sub-01_space-T1w_T1w.nii.gz
      └─ sub-01_space-T1w_T1w.json
```

## Multi-subject template and atlases and deriving an existing template/atlas

Atlasing multiple individual brains is a higher-than-first-level analysis,
as it requires first generating derivatives for the individuals (for example,
a transformation to align them into a standardized space) and later aggregate
and distill the sample-pooled knowledge and feature maps.
Similarly, deriving from an existing template and atlases is also
a higher-than-first-level analysis as it builds on a previous analysis.

**Multi-subject templates and atlases**.
While at the subject level analysis it is the individual brain that establishes
stereotaxy.
At higher-than-first-level stereotaxy is supported by templates, which are
encoded through the [`tpl-<label>` entity](../glossary.md#template-entities).
For the pipeline that generated the MNI152NLin2009cAsym, the outputs would look
like the following example:

```Text
mni152nlin2009casym-pipeline/
└─ tpl-MNI152NLin2009cAsym/
   └─ anat/
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-brain_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-eye_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-face_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-head_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-CSF_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-GM_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_label-WM_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_T1w.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-1_T1w.json
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-brain_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-eye_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-face_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-head_mask.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-CSF_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-GM_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_label-WM_probseg.nii.gz
      ├─ tpl-MNI152NLin2009cAsym_res-2_T1w.nii.gz
      └─ tpl-MNI152NLin2009cAsym_res-2_T1w.json
```

**Deriving from an existing template/atlas**.
For example, the MIAL67ThalamicNuclei
([Najdenovska et al., 2018](https://doi.org/10.1038/sdata.2018.270))
atlas-generation pipeline could display the following structure:

```Text
MIAL67ThalamicNuclei-pipeline/
├─ tpl-MNI152NLin2009cAsym/
│  └─ anat/
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.json
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.tsv
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ sub-01
│  └─ anat/
│     ├─ sub-01_label-ThalamicNuclei_dseg.json
│     ├─ sub-01_label-ThalamicNuclei_dseg.tsv
│     ├─ sub-01_label-ThalamicNuclei_dseg.nii.gz
│     ├─ sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz
│     └─ sub-01_T1w.nii.gz
┇
└─ sub-67
   └─ anat/
      ├─ sub-67_label-ThalamicNuclei_dseg.json
      ├─ sub-67_label-ThalamicNuclei_dseg.tsv
      ├─ sub-67_label-ThalamicNuclei_dseg.nii.gz
      ├─ sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz
      └─ sub-67_T1w.nii.gz
```

where the derivatives of anatomical processing of the 67 subjects that were
employed to generate the atlas co-exist with the template structure.

The inheritance principle applies uniformly, allowing the segmentation
metadata be stored only once at the root of the pipeline directory and
apply to all the individual subject segmentations:

```Text
MIAL67ThalamicNuclei-pipeline/
├─ label-ThalamicNuclei_dseg.json
├─ label-ThalamicNuclei_dseg.tsv
├─ tpl-MNI152NLin2009cAsym/
│  └─ anat/
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.json
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_dseg.tsv
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ sub-01
│  └─ anat/
│     ├─ sub-01_label-ThalamicNuclei_dseg.nii.gz
│     ├─ sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz
│     └─ sub-01_T1w.nii.gz
┇
└─ sub-67
   └─ anat/
      ├─ sub-67_label-ThalamicNuclei_dseg.nii.gz
      ├─ sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz
      └─ sub-67_T1w.nii.gz
```

This directory structure can be generally applied when the atlas is derived into several
template spaces, for example:

```Text
MIAL67ThalamicNuclei-pipeline/
├─ atlas-MIAL67ThalamicNuclei_dseg.json
├─ atlas-MIAL67ThalamicNuclei_dseg.tsv
├─ label-ThalamicNuclei_dseg.json
├─ label-ThalamicNuclei_dseg.tsv
├─ tpl-MNI152NLin6Asym/
│  └─ anat/
│     ├─ tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ tpl-MNI152NLin2009cAsym/
│  └─ anat/
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ sub-01
│  └─ anat/
│     ├─ sub-01_label-ThalamicNuclei_dseg.nii.gz
│     ├─ sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz
│     └─ sub-01_T1w.nii.gz
┇
└─ sub-67
   └─ anat/
      ├─ sub-67_label-ThalamicNuclei_dseg.nii.gz
      ├─ sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz
      └─ sub-67_T1w.nii.gz
```

In the case the pipeline generated atlas-based segmentations of the original subjects in
their native T1w space (for example, to compare with the original segmentation given by
`label-ThalamicNuclei`), the above example translates into:

```Text
MIAL67ThalamicNuclei-pipeline/
├─ atlas-MIAL67ThalamicNuclei_dseg.json
├─ atlas-MIAL67ThalamicNuclei_dseg.tsv
├─ label-ThalamicNuclei_dseg.json
├─ label-ThalamicNuclei_dseg.tsv
├─ tpl-MNI152NLin6Asym/
│  └─ anat/
│     ├─ tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin6Asym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ tpl-MNI152NLin2009cAsym/
│  └─ anat/
│     ├─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_dseg.nii.gz
│     └─ tpl-MNI152NLin2009cAsym_atlas-MIAL67ThalamicNuclei_res-1_probseg.nii.gz
├─ sub-01
│  └─ anat/
│     ├─ sub-01_atlas-MIAL67ThalamicNuclei_dseg.nii.gz
│     ├─ sub-01_label-ThalamicNuclei_dseg.nii.gz
│     ├─ sub-01_space-MNI152NLin2009cAsym_T1w.nii.gz
│     └─ sub-01_T1w.nii.gz
┇
└─ sub-67
   └─ anat/
      ├─ sub-67_atlas-MIAL67ThalamicNuclei_dseg.nii.gz
      ├─ sub-67_label-ThalamicNuclei_dseg.nii.gz
      ├─ sub-67_space-MNI152NLin2009cAsym_T1w.nii.gz
      └─ sub-67_T1w.nii.gz
```

The next subsection describes this latter use-case in further depth.

## Filenames of derivatives with atlases in their provenance

Like for the [`space-` entity](../glossary.md#space-entities), outputs derived from atlases
MUST employ `atlas-`, `seg-`, and `scale-` when necessary:

```Text
bold-pipeline/
├─ atlas-Schaefer2018_dseg.json
├─ atlas-Schaefer2018_seg-7n_scale-100_dseg.tsv
├─ atlas-Schaefer2018_seg-7n_scale-200_dseg.tsv
├─ atlas-Schaefer2018_seg-7n_scale-300_dseg.tsv
├─ atlas-Schaefer2018_seg-17n_scale-100_dseg.tsv
├─ atlas-Schaefer2018_seg-17n_scale-200_dseg.tsv
├─ atlas-Schaefer2018_seg-17n_scale-300_dseg.tsv
├─ atlas-Schaefer2018_seg-kong17n_scale-100_dseg.tsv
├─ atlas-Schaefer2018_seg-kong17n_scale-200_dseg.tsv
├─ atlas-Schaefer2018_seg-kong17n_scale-300_dseg.tsv
└─ sub-01/
   ├─ anat/
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-100_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-200_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-7n_scale-300_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-100_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-200_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-17n_scale-300_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-100_den-164k_dseg.label.gii
   │  ├─ sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-200_den-164k_dseg.label.gii
   │  └─ sub-01_hemi-L_atlas-Schaefer2018_seg-kong17n_scale-300_den-164k_dseg.label.gii
   └─ func/
      └─ sub-01_task-rest_hemi-L_den-164k_bold.func.gii
```

## Tabular data

The `[probseg|dseg|mask|channels].tsv` file indexes and labels each node/parcel/region within the atlas.
This file resembles the typical Look Up Table (LUT) often shared with atlases.
This file will be essential for downstream workflows that generate matrices or other derived files within which node/parcel/region information is required,
as the index/label fields will be used to reference the original anatomy the index/labels are derived from.
Additional fields can be added with their respective definition/description in the sidecar json file.

<table>
  <tr>
   <td>index (or placeholder in fragment in reference)
   </td>
   <td>REQUIRED. (Integer) The number associated with the node/parcel/region (right/left hemispheres may be different).
   </td>
  </tr>
  <tr>
   <td>label
   </td>
   <td>RECOMMENDED. The node name
   </td>
  </tr>
  <tr>
   <td>network_id
   </td>
   <td>OPTIONAL. Network ID the node/parcel belongs to
   </td>
  </tr>
  <tr>
   <td>network_label
   </td>
   <td>OPTIONAL. Label of Network (for example, Dorsal Attention Network)
   </td>
  </tr>
  <tr>
   <td>coordinate_report_strategy
   </td>
   <td>OPTIONAL (RECOMMENDED if x, y, z keys are specified).  The strategy used to assess and report x, y and z coordinates of a given node/parcel/region. For example, "CenterOfMass".
   </td>
  </tr>
  <tr>
   <td>x
   </td>
   <td>OPTIONAL. The x-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
   </td>
  </tr>
  <tr>
   <td>y
   </td>
   <td>OPTIONAL. The y-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
   </td>
  </tr>
  <tr>
   <td>z
   </td>
   <td>OPTIONAL. The z-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
   </td>
  </tr>
  <tr>
   <td>hemisphere
   </td>
   <td>OPTIONAL. MUST BE ONE OF: "left", "right", "bilateral". Indicate whether the node/parcel/region is in the left or right hemispheres, or is available bilaterally.
   </td>
  </tr>
  <tr>
   <td>color
   </td>
   <td>OPTIONAL. RGB color to use for the node.
   </td>
  </tr>
  <tr>
   <td>seed
   </td>
   <td>OPTIONAL. Seed vertex/channel of the node/region
   </td>
  </tr>
  <tr>
   <td>region
   </td>
   <td>OPTIONAL. "XY", where X can be L:left, R:right, B:bilateral, and Y can be F:frontal, T:temporal, P:parietal, O:occipital
   </td>
  </tr>
</table>

Example:
```Text
index	label	network_label	hemisphere
1	Heschl's Gyrus	Somatomotor	left
2	Heschl's Gyrus	Somatomotor	right
```

## Atlas metadata

The `[probseg|dseg|mask].json` file provides metadata to uniquely identify, describe and characterize the atlas, as well as give proper attribution to the creators.
Additionally, SpatialReference serves the important purpose of unambiguously identifying the space the atlas is labeled in.

<table>
  <tr>
   <td>Name
   </td>
   <td>REQUIRED. Name of the atlas
   </td>
  </tr>
  <tr>
   <td>Description
   </td>
   <td>RECOMMENDED. Longform description of the atlas
   </td>
  </tr>
  <tr>
   <td>SpatialReference
   </td>
   <td>RECOMMENDED. Point to an existing atlas in a template space (URL or relative file path where this file is located).
   </td>
  </tr>
  <tr>
   <td>Resolution
   </td>
   <td>RECOMMENDED. Resolution atlas is provided in.
   </td>
  </tr>
  <tr>
   <td>Dimensions
   </td>
   <td>RECOMMENDED. Dimensions of the atlas, MUST be 3 (for deterministic atlases) or 4 (for probabilistic atlases).
   </td>
  </tr>
  <tr>
   <td>4thDimension
   </td>
   <td>OPTIONAL. RECOMMENDED if probabilistic atlas. Should indicate what the 4th dimension entails/refers to. MUST be "Indices" or   .
   </td>
  </tr>
  <tr>
   <td>CoordinateReportStrategy
   </td>
   <td>OPTIONAL. MUST BE ONE OF: "peak", "center_of_mass", "other". Indicate the method of coordinate reporting in statistically significant clusters. Could be the "peak" statistical coordinate in the cluster or the "center_of_mass" of the cluster. RECOMMENDED if x, y ,z values are set in the .tsv file.
   </td>
  </tr>
  <tr>
   <td>Authors
   </td>
   <td>RECOMMENDED. List of the authors involved in the creation of the atlas
   </td>
  </tr>
  <tr>
   <td>Curators
   </td>
   <td>RECOMMENDED. List of curators who helped make the atlas accessible in a database or dataset
   </td>
  </tr>
  <tr>
   <td>Funding
   </td>
   <td>RECOMMENDED. The funding source(s) involved in the atlas creation
   </td>
  </tr>
  <tr>
   <td>License
   </td>
   <td>RECOMMENDED. The license agreement for using the atlas.
   </td>
  </tr>
  <tr>
   <td>ReferencesAndLinks
   </td>
   <td>RECOMMENDED. A list of relevant references and links pertaining to the atlas.
   </td>
  </tr>
  <tr>
   <td>Species
   </td>
   <td>RECOMMENDED. The species the atlas was derived from. For example, could be Human, Macaque, Rat, Mouse, etc.
   </td>
  </tr>
  <tr>
   <td>DerivedFrom
   </td>
   <td>RECOMMENDED. Indicate what data modality the atlas was derived from, for example, "cytoarchitecture", "resting-state", "task".
   </td>
  </tr>
  <tr>
   <td>LevelType
   </td>
   <td>RECOMMENDED. Indicate what analysis level the atlas was derived from, for example, "group", "individual".
   </td>
  </tr>
</table>

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
  "Space": "MNI152NLin6Asym",
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
