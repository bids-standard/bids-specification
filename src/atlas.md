# Explanation

In the following we describe how an [atlas](schema/objects/entities.yaml#atlas) can be shared within BIDS.
Broadly we define an atlas as a reference quantity sampled to a template.
With this definition, an atlas can be a parcellation, a segmentation, or a quantitative map.

We aim to cover three main use cases with the given definition:
1. Generating/sharing atlas(es) to be published and used by others.
2. Using a shared atlas and transforming/resampling it into new template spaces or subject spaces.
3. Creating subject-specific atlases derived from the corresponding subject’s data.

These three use cases cover the majority of scenarios where atlases are used in neuroimaging research.

The first use case would comprise (publicly) available atlases, for example,
Destrieux et al. ([doi.org/10.1016/j.neuroimage.2010.06.010](https://doi.org/10.1016/j.neuroimage.2010.06.010)),
AAL ([doi.org/10.1006/nimg.2001.0978](https://doi.org/10.1006/nimg.2001.0978)),
Yeo ([doi.org/10.1152/jn.00338.2011](https://doi.org/10.1152/jn.00338.2011))
and JHU DTI-based white-matter atlases
([eBook ISBN: 9780080456164](https://shop.elsevier.com/books/mri-atlas-of-human-white-matter/mori/978-0-444-51741-8)
and [doi.org/10.1016/j.neuroimage.2007.07.053](https://doi.org/10.1016/j.neuroimage.2007.07.053)).
The second use case would comprise transforming/resampling the publicly available atlases into new template spaces or subject spaces for further analysis.
For example, resampling the AAL atlas from MNI152NLin6Asym space to a subject’s native T1w space.
The third use case would include atlases obtained through analyses within a dataset at hand,
for example, resting-state networks and functional localizers.

## Definitions and Terminology

Template - a canonical anatomical reference in a particular space; while two templates may be in the same space, the template matters for the association of coordinates with structures, so when something is said to be resampled into a space, the template used is the more useful name.

Space - A common coordinate frame with an origin, axis orientations and spatial units;
in practice this definition is too abstract to be directly usable.
Within the BIDS filename structure, the keyword `space-` is an application of a template onto a subject space.

Atlas - A reference quantity sampled to a template. In many contexts this is a parcellation, but it in some communities (notably PET) it is more common to publish absolute quantities and leave it to end-users to discretize the quantities into segmentations. It is also common to publish reference data sampled to one or more public templates, rather than publishing yet another atlas.

Segmentation - A partition of an image into multiple segments or regions based on certain criteria, such as intensity, texture, or anatomical features.
Both atlases and segmentations provide spatial information about the brain,
however, they serve distinct purposes: atlases provide a common spatial framework and
delineate predefined regions of interest, while segmentations partition brain images into distinct tissue types for quantitative analysis and anatomical characterization
for individual subjects or groups of subjects.
Within the BIDS filenaming structure, the keyword `seg` is used to indicate
an application of an atlas to a subject.

## File formats for the data

BIDS-Atlas aims to describe brain atlases via four REQUIRED files.
They entail the atlas itself (for example, in .nii, .nii.gz, .gii, or .tsv),
a file indexing/labeling each node in the atlas (in .tsv), a sidecar json file containing
spatial meta-data about the atlas, and an exhaustive meta-data `_description.json`
file containing information about how the atlas was generated.

{{ MACROS___make_filename_template("atlas", suffixes=["dseg", "probseg", "mask"]) }}

## Atlas file formats

The `[probseg|dseg|mask].[nii|dlabel.nii|label.gii][.gz]` file represents the location and extent of the nodes/parcels/regions within the atlas.
Different file types are supported based on the modality and atlas at hand.
In more detail, this encompasses the following three options:

1. [_dseg](schema/objects/suffixes.yaml#dseg): Each node is labeled with a unique integer corresponding to its row/index in the tsv sidecar.
1. [_probseg](schema/objects/suffixes.yaml#probseg): Each node is represented along an additional dimension of the file (for example, a 4D NIfTI file where each volume represents a node) and its position in that dimension corresponds to its row/index in the tsv sidecar.
1. [_mask](schema/objects/suffixes.yaml#mask): Either each voxel represents a node or the entire mask is a single node.
   How the mask should be interpreted is determined by other specifications.
   Based on these options, an atlas can take the following forms in the here proposed specification (non-exhaustive list):
     1.  A 3D NIfTI file with unique integers defining nodes
     1.  A 4D binary NIfTI file with spatially overlapping nodes in each volume (along the 4th dimension)
     1.  A 4D NIfTI file with overlapping nodes with continuous values for each voxel within a volume

Examples:
```Text
atlas-HarvardOxford_res-2_dseg.nii.gz
atlas-HarvardOxford_res-2_probseg.nii.gz
atlas-HarvardOxford_res-2_desc-HeschlGyrus_mask.nii.gz
```

General Recommendations: This specification relies on the inheritance principle whereby files deeper in the hierarchy inherit from the top-level files.
If you have atlas files that are transformed to subject-specific space for each subject,
then excluding the space entity at the top level is a good way to ensure the file inherits information about the original atlas.
Additionally, the [desc](schema/objects/entities.yaml#desc) label should be avoided as an inherited file.
One may need to use the [desc](schema/objects/entities.yaml#desc) label to contain information related or unrelated to the atlas.

## Directory Structure

An atlas can be conceptualized with three use cases in mind.
1. Generating/Sharing an atlas to be published and used by others.
2. Using a shared atlas and transforming it into new template spaces or subject spaces.
3. Creating subject-specific atlases derived from the corresponding subject’s data.

For all three use cases, a compatible directory structure is proposed that is modular
and extensible for representing atlases in BIDS derivative datasets.


# Reference

## Files

### atlas-\<label>_description.json

The `atlas-<label>_description.json` file provides metadata to uniquely identify, describe and characterize the atlas, as well as give proper attribution to the creators.


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

#### Example:

```JSON
{
  "Name": "HarvardOxford cort maxprob thr25 2mm",
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
  "License": "See LICENSE file",
  "RRID": "SCR_002823",
  "ReferencesAndLinks": [
    "https://doi.org/10.1016/j.neuroimage.2012.01.024",
    "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases"
  ],
  "Species": "Human"
}
```

### atlas-\<label>_[dseg|probseg|mask].json

This sidecar json file contains the spatial meta-data about the atlas, including the spatial reference and resolution of the atlas projected onto a template space.


|       Name       | Description                                                                                                         |
|:----------------:|---------------------------------------------------------------------------------------------------------------------|
| SpatialReference | RECOMMENDED. Point to an existing atlas in a template space (url or bids URI where file is located). |
| Resolution       | RECOMMENDED. Resolution atlas is provided in.                                                                       |

#### Example:
```JSON
{
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
  "Resolution": "Matched with original template resolution (2x2x3 mm^3)"
}
```

### atlas-\<label>_[dseg|probseg|mask].tsv

The `[probseg|dseg|mask|channels].tsv` file indexes and labels each node/parcel/region within the atlas.
This file resembles the typical Look Up Table (LUT) often shared with atlases.
This file will be essential for downstream workflows that generate matrices or other derived files within which node/parcel/region information is required,
as the index/label fields will be used to reference the original anatomy the index/labels are derived from.
Additional fields can be added with their respective definition/description in the sidecar json file.
This file is not applicable for quantitative maps.

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
   <td>OPTIONAL. The x-coordinate of the node in the spatial reference space (See SpatialReference in the sidecar json file)
   </td>
  </tr>
  <tr>
   <td>y
   </td>
   <td>OPTIONAL. The y-coordinate of the node in the spatial reference space (See SpatialReference in the sidecar json file)
   </td>
  </tr>
  <tr>
   <td>z
   </td>
   <td>OPTIONAL. The z-coordinate of the node in the spatial reference space (See SpatialReference in the sidecar json file)
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

#### Example:
```Text
index	label	network_label	hemisphere
1	Heschl's Gyrus	Somatomotor	left
2	Heschl's Gyrus	Somatomotor	right
```

## Directory Structure

```Text
<dataset>/derivatives/atlas-<label>
  atlas-<label>_description.json
  atlas-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
  atlas-<label>_[dseg|probseg|mask].tsv
  atlas-<label>_[dseg|probseg|mask].json
  sub-<label>/...
    sub-<label>_space-<label>_seg-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
    sub-<label>_space-<label>_seg-<label>_[dseg|probseg|mask].tsv
    sub-<label>_space-<label>_seg-<label>_[dseg|probseg|mask].json
```

# How to use BIDS-Atlas

Below are a collection of exemplary use cases that illustrate how to use the BIDS-Atlas extension.

## Sharing an atlas

The example below illustrates how a single existing atlas in template space is represented as a dataset according to the atlas BEP.
Specifically, the example refers to the Harvard-Oxford atlas in MN152NLin6Asym space with a resolution of 2 mm3,
used without modifications (for example, transformations, subsetting, etc.)
for all subjects to which the pipeline was applied.

```Text
my_dataset/derivatives/atlas-HarvardOxford/
  atlas-HarvardOxford_description.json
  atlas-HarvardOxford_res-2_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-2_dseg.tsv
```

The content of each file is further outlined in the following,
starting with the .json sidecar file containing meta-data about the atlas at hand.

Example content of the `atlas-HarvardOxford_description.json` file:

```JSON
{
  "Name": "HarvardOxford cort maxprob thr25 2mm",,
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
  "License": "See LICENSE file",
  "RRID": "SCR_002823",
  "ReferencesAndLinks": [
    "https://doi.org/10.1016/j.neuroimage.2012.01.024",
    "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases"
  ],
  "Species": "Human"
}
```

Example content of the `atlas-HarvardOxford_res-2_dseg.json` file:

```JSON
{
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
  "Resolution": "Matched with original template resolution (2x2x3 mm^3)"
}
```

Next, the content of the tsv files describing the indices and corresponding labels present in the atlas at hand.

Example content of the `atlas-HarvardOxford_res-2_dseg.tsv` file:

```Text
index	label	hemisphere
0	Background	bilateral
1	Frontal Pole	bilateral
2 Insular Cortex	bilateral
3	Superior Frontal Gyrus	bilateral
4	Middle Frontal Gyrus	bilateral
5	Inferior Frontal Gyrus, pars triangularis	bilateral
6	Inferior Frontal Gyrus, pars opercularis	bilateral
```

If the atlas was projected into multiple resolutions, for example, 1 mm3, 2 mm3, and 3 mm3, this could be described with a sidecar and nifti file for each resolution.


```Text
my_dataset/derivatives/atlas-HarvardOxford/
  atlas-HarvardOxford_description.json
  atlas-HarvardOxford_dseg.tsv
  atlas-HarvardOxford_res-1_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-2_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-3_dseg.json
  atlas-HarvardOxford_res-3_dseg.nii.gz
```

Here the tsv file would be applicable to all resolutions, while the json and nii.gz files would be specific to each resolution.
For certain atlases, the resolution may be coarse enough such that certain nodes are not present in the atlas.
In such cases, a unique tsv could be defined for each resolution, removing the rows
that are not present in the atlas at that resolution.

```Text
my_dataset/derivatives/atlas-HarvardOxford/
  atlas-HarvardOxford_description.json
  atlas-HarvardOxford_res-1_dseg.tsv
  atlas-HarvardOxford_res-1_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-1_dseg.tsv
  atlas-HarvardOxford_res-2_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-1_dseg.tsv
  atlas-HarvardOxford_res-3_dseg.json
  atlas-HarvardOxford_res-3_dseg.nii.gz
```

### Same Atlas projected into multiple Template spaces

```Text
bids/
  derivatives/
    atlas-AAL/
      dataset_description.json
      atlas-AAL_description.json
      atlas-AAL_dseg.tsv
      atlas-AAL_space-MNI152NLin6Asym_dseg.json
      atlas-AAL_space-MNI152NLin6Asym_dseg.nii.gz
      atlas-AAL_space-MNI305Lin_dseg.json
      atlas-AAL_space-MNI305Lin_dseg.nii.gz
```

## Transforming an Atlas to subject space

The example below illustrates how a single existing atlas transformed into a subject’s native space space is represented according to the atlas BEP.
Specifically, the example refers to the Harvard-Oxford atlas with a resolution of 2 mm3 that was transformed from the MN152NLin6Asym template space to a given subject’s native T1w space.
While the original atlas-related files remain as outlined in the use case in template space,
the spatially transformed version of the nii.gz atlas file will be placed within a given subjects directory.
The precise location within the latter depends on the modality space to which the atlas was transformed to,
for example, anat, func or dwi.
The same location furthermore entails a corresponding json file outlining further information on the source atlas and applied transformation(s).


```Text
bids/derivatives/pipeline-test/
  atlas-HarvardOxfordThr50_description.json
  atlas-HarvardOxfordThr50_dseg.json
  atlas-HarvardOxfordThr50_dseg.tsv
  atlas-HavardOxfordThr50_dseg.nii.gz
  sub-01/
    anat/
      sub-01_T1w.nii.gz
      sub-01_space-T1w_res-1_seg-HarvardOxfordThr50_dseg.nii.gz
      sub-01_space-T1w_res-1_seg-HarvardOxfordThr50_dseg.json
      sub-01_space-T1w_res-1_seg-HarvardOxfordThr50_dseg.tsv
```

The json file accompanying the transformed atlas should include the following information.

Example content of the `sub-01_space-T1w_res-1_seg-HarvardOxford_dseg.json` file:

```JSON
{
  "SpatialReference": "sub-01/anat/sub-01_T1w.nii.gz",
  "Resolution": "Matched with original resolution in subject T1w space (1x1x1 mm^3)",
}
```

## Multiple Atlases in the same space

The example below illustrates how multiple existing atlases in the same template space are represented according to the atlas BEP.
Specifically, the example refers to the Harvard-Oxford, Schaefer, Yeo and MSDL atlases,
all in MN152NLin6Asym space and with a resolution of 2 mm3, and this information
is represented in the sidecar `_dseg.json` file.
Importantly, all atlas-related information is indicated via the value of the atlas- key and not via desc- to help prevent inheritance problems in subsequent steps.
Here, the `atlas` entity was used to indicate that the Harvard-Oxford atlas in its version with a maximum probability of 50,
the Schaefer atlas in its 400 parcel version and the Yeo atlas in its 17 networks version were used.
Below, each of the atlases are given their own derivative dataset.

```Text
bids/derivatives/
  atlas-HarvardOxford50thr/
    atlas-HarvardOxford50thr_description.json
    atlas-HarvardOxford50thr_dseg.nii.gz
    atlas-HarvardOxford50thr_dseg.json
    atlas-HarvardOxford50thr_dseg.tsv
  atlas-Schaefer400/
    atlas-Schaefer400_description.json
    atlas-Schaefer400_dseg.nii.gz
    atlas-Schaefer400_dseg.json
    atlas-Schaefer400_dseg.tsv
  atlas-Yeo17/
    atlas-Yeo17_description.json
    atlas-Yeo17_dseg.nii.gz
    atlas-Yeo17_dseg.json
    atlas-Yeo17_dseg.tsv
  atlas-msdl/
    atlas-msdl_description.json
    atlas-msdl_probseg.nii.gz
    atlas-msdl_probseg.json
    atlas-msdl_probseg.tsv
```

Or they could all be represented in the same directory:

```Text
bids/derivatives/
  atlas-HarvardOxford50thr_description.json
  atlas-HarvardOxford50thr_dseg.nii.gz
  atlas-HarvardOxford50thr_dseg.json
  atlas-HarvardOxford50thr_dseg.tsv
  atlas-Schaefer400_description.json
  atlas-Schaefer400_dseg.nii.gz
  atlas-Schaefer400_dseg.json
  atlas-Schaefer400_dseg.tsv
  atlas-Yeo17_description.json
  atlas-Yeo17_dseg.nii.gz
  atlas-Yeo17_dseg.json
  atlas-Yeo17_dseg.tsv
  atlas-msdl_description.json
  atlas-msdl_probseg.nii.gz
  atlas-msdl_probseg.json
  atlas-msdl_probseg.tsv
```

##  MyConnectome example

The example below illustrates how two atlases,
an individual surface-based cortical parcellation in FS_lr space (called Russome),
and the subcortical regions from a volumetric segmentation provided by the FreeSurfer aseg,
are represented according to the atlas BEP.
While the FreeSurfer atlas-related files have two instances,
one as outlined in the use case in template space and one as outlined in the use case covering subject spaces,
the individual parcellation in FS_lr space will be placed only within a given subjects directory.
The same location furthermore entails a corresponding json file outlining further information on the atlas and applied analysis to obtain it.

```Text
bids/
  sub-01/
    anat/
      sub-01_T1w.nii.gz

bids/derivatives/pipeline-<name>/
  atlas-Russome_description.json
  atlas-FreeSurferASEG_description.json
  sub-01/
    anat/
      sub-01_T1w.nii.gz
      sub-01_space-T1w_res-2_seg-FreeSurferASEG_dseg.nii.gz
      sub-01_space-T1w_res-2_seg-FreeSurferASEG_dseg.json
      sub-01_space-T1w_res-2_seg-FreeSurferASEG_dseg.tsv
    func/
      sub-01_space-FSLr_res-2_seg-Russome_dseg.nii.gz
      sub-01_space-FSLr_res-2_seg-Russome_dseg.json
      sub-01_space-FSLr_res-2_seg-Russome_dseg.tsv
```

The json file accompanying the functionally derived atlas should include the following information.

Example content of the `atlas-FreeSurferASEG_description.json` file contains top-level metadata about the atlas:

```JSON

{
  "Name": "FreeSurferASEG",,
  "Authors": [
    "Bruce Fischl",
    "David H. Salat",
    "Evelina Busa",
    "Marilyn Albert",
    "Megan Dieterich",
    "Christian Haselgrove",
    "Andre van der Kouwe",
    "Ron Killiany",
    "David Kennedy",
    "Shuna Klaveness",
    "Albert Montillo",
    "Nikos Makris",
    "Bruce Rosen",
    "Anders M. Dale",
  ],
  "BIDSVersion": "1.1.0",
  "License": "See LICENSE file",
  "ReferencesAndLinks": [
    "https://surfer.nmr.mgh.harvard.edu/fswiki/FreeSurferVersion3",
    "https://surfer.nmr.mgh.harvard.edu/ftp/articles/fischl02-labeling.pdf",
  ],
  "Species": "Human"
}
```

This is what is contained in the `sub-01_space-T1w_res-2_seg-FreeSurferASEG_dseg.json` file:

```JSON
{
  "SpatialReference": "bids:sub-01/anat/sub-01_T1w.nii.gz",
  "Resolution": "Matched with original template resolution (2x2x3 mm^3)",
}
```

## Quantitative atlas examples

The example below is for PET imaging, but this applies to any quantitative mapping (PET or qMRI).
Compared to anatomical atlases, quantitative atlases give reference values to be compared with.
Such values can be derived voxel/vertex wise (see case 1) or per region of interest (ROI) (see case 2).
In the latter case, ROIs are generally derived from an anatomical atlas.

We created a Molecular Imaging Brain Atlases (MIBA) from 16 subjects who underwent a [11C]PS13 PET scan,
a radioligand that quantifies cyclooxygenase-1 (see [source data](https://openneuro.org/datasets/ds004332/versions/1.0.2)).
Our atlas consists of mean and standard deviations of PS13 target distribution volumes (VT) computed across the 16 subjects at each voxel, in standard MRI spaces.
We also project these distribution volumes onto the FreeSurfer cortical surfaces and include these as well.
The goal is to allow researchers with MRI-only data to correlate their results to the distribution volume of PS13.
The dataset can be found [here](https://openneuro.org/datasets/ds004401/versions/1.1.0).

### Case 1: voxel/vertex wise analysis

Example directory content for a quantitative atlas that provides values at all voxels and/or vertices:

```Text
bids/derivatives/atlas-ps13/
    atlas-ps13_description.json
    atlas-ps13_space-fsaverage_hemi-L_stat-mean_meas-VT_mimap.json
    atlas-ps13_space-fsaverage_hemi-L_stat-mean_meas-VT_mimap.nii.gz
    atlas-ps13_space-fsaverage_hemi-R_stat-mean_meas-VT_mimap.json
    atlas-ps13_space-fsaverage_hemi-R_stat-mean_meas-VT_mimap.nii.gz
    atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_mimap.json
    atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_mimap.nii.gz
    atlas-ps13_space-fsaverage_hemi-L_stat-std_meas-VT_mimap.json
    atlas-ps13_space-fsaverage_hemi-L_stat-std_meas-VT_mimap.nii.gz
    atlas-ps13_space-fsaverage_hemi-R_stat-std_meas-VT_mimap.json
    atlas-ps13_space-fsaverage_hemi-R_stat-std_meas-VT_mimap.nii.gz
    atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_mimap.json
    atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_mimap.nii.gz
```

### Case 2: regional analysis (voxels/vertices are averaged per regions from dseg/probseg)

Example directory content for a quantitative atlas that provides values for certain ROIs only,
in this case defined by the AAL atlas:

```Text
bids/derivatives/atlas/
  atlas-aparc.DKTatlas+aseg.mgz  # need to figure out how to represent this
  atlas-aparc.DKTatlas+aseg.tsv   # need to figure out how to represent this
  atlas-RB_all_2008-03-26.probseg.gca   # need to figure out how to represent this
  atlas-RB_all_2008-03-26.probseg.tsv   # need to figure out how to represent this
  atlas-ps13_description.json
  atlas-ps13_space-fsaverage_hemi-L_stat-mean_meas-VT_seg-AAL_mimap.json # should not have seg and atlas in the same filename
  atlas-ps13_space-fsaverage-hemi-L_stat-mean_meas-VT_seg-AAL_mimap.tsv
  atlas-ps13_space-fsaverage-hemi-L_stat-std_meas-VT_seg-AAL_mimap.json
  atlas-ps13_space-fsaverage-hemi-L_stat-std_meas-VT_seg-AAL_mimap.tsv
  atlas-ps13_space-fsaverage-hemi-R_stat-mean_meas-VT_seg-AAL_mimap.json
  atlas-ps13_space-fsaverage-hemi-R_stat-mean_meas-VT_seg-AAL_mimap.tsv
  atlas-ps13_space-fsaverage-hemi-R_stat-std_meas-VT_seg-AAL_mimap.json
  atlas-ps13_space-fsaverage-hemi-R_stat-std_meas-VT_seg-AAL_mimap.tsv
  atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_seg-AAL_mimap.json
  atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_seg-AAL_mimap.tsv
  atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_seg-AAL_mimap.json
  atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_seg-AAL_mimap.tsv
```

Note that there is no image file present in a regional quantitative atlas.
The `atlas-<label>_description.json` file accompanying the quantitative atlas should include the information as in [Single existing atlas in template space](#_Single_existing_atlas_in_template_space).


## FAQ

### How should I use the _desc- entity?

The usage of [_desc-](schema/objects/entities.yaml#desc) is generally discouraged but should be evaluated on a case by case basis in order to keep this identifier available for necessary cases.
Specifically, this refers to the atlas at hand and potential different versions thereof.
As a rule of thumb, BIDS-Atlas proposed to evaluate and consider how many versions across how many levels of versions an atlas is (commonly) provided and used in.
If there is only one version, as in "release", of an atlas
and no sub-versions, as in "different parcel numbers" (or comparable),
[_desc-](schema/objects/entities.yaml#desc) is most likely not expected and/or required.
An example for [_desc-](schema/objects/entities.yaml#desc) in such a use case would be
to indicate a subset of parcels and would entail the addition of
the [_mask-](schema/objects/entities.yaml#mask) extension,
for example, providing/using the "postcentral gyrus" region of the [Destrieux atlas](doi:10.1093/cercor/bhg087.) would result in the following file name:
`atlas-Destrieux_space-MNI152NLin6Asym_res-2_desc-PostCentralGyrus_mask.nii.gz`.
Similar to the above case, if there are multiple versions, as in "release",
of an atlas and no sub-versions, as in "different parcel numbers" (or comparable),
[_desc-](schema/objects/entities.yaml#desc) is also most likely not expected and/or required,
as the version(s) (release(s)) should be indicated via `atlas-`.
For example, the different versions of the [AAL parcellation](http://www.gin.cnrs.fr/AAL-217?lang=en)
would result in the following file names:
`atlas-AAL1_space-MNI152NLin6Asym_res-2.nii.gz`, `atlas-AAL2_space-MNI152NLin6Asym_res-2.nii.gz` and `atlas-AAL3_space-MNI152NLin6Asym_res-2.nii.gz`.
Given an atlas has only one version, as in "release", and multiple sub-versions
as in "different parcel numbers" (or comparable)
[_desc-](schema/objects/entities.yaml#desc) is considered appropriate.
For example, when indicating information pertaining to the probabilistic nature of an atlas
such as the [_probseg](schema/objects/entities.yaml#probseg) version of
the [Harvard-Oxford parcellation](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases):
`atlas-HarvardOxford_res-2_desc-th25_probseg.nii.gz`.
In cases where an atlas has multiple versions, as in "release", and sub-versions,
as in "different parcel numbers" (or comparable),
the version(s) (release(s)) should be indicated via `atlas-` as outlined above and the sub-versions should be indicated via [_desc-](schema/objects/entities.yaml#desc).
For example, different versions and sub-versions of the [Schaefer parcellation](https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/Updates/Update_20190916_README.md) would be denoted as follows:
`atlas-Schaefer2018_space-MNI152NLin6Asym_res-2_desc-400Parcels7Networks.nii.gz`,
`atlas-Schaefer2018_space-MNI152NLin6Asym_res-2_desc-400Parcels17Networks.nii.gz`,
`atlas-Schaefer2022_space-MNI152NLin6Asym_res-2_desc-800Parcels7Networks.nii.gz`
and `atlas-Schaefer2022_space-MNI152NLin6Asym_res-2_desc-800Parcels17Networks.nii.gz`.

Importantly, already existing BIDS entities should be used to indicate certain aspects of an atlas,
instead of [_desc-](schema/objects/entities.yaml#desc), for example,
[hemi](schema/objects/entities.yaml#hemi) to denote a given hemisphere
and [_dseg](schema/objects/entities.yaml#dseg)/[_probseg](schema/objects/entities.yaml#probseg)
to denote deterministic and probabilistic atlases respectively.

However, as mentioned above, these are general guidelines and the exact implementation should be evaluated on a case by case basis, with deviations following common BIDS principles being permitted.


# TO BE DELETED

### Each atlas gets its own derivative directory
```Text
bids/
  derivatives/
    atlas-AAL/
      dataset_description.json
      atlas-AAL_description.json
      atlas-AAL_dseg.tsv
      atlas-AAL_dseg.json
      atlas-AAL_dseg.nii.gz
    atlas-Destrieux/
      dataset_description.json
      atlas-Destrieux_description.json
      atlas-Destrieux_dseg.tsv
      atlas-Destrieux_dseg.json
      atlas-Destrieux_dseg.nii.gz
```

### Multiple atlases in the same directory

```Text
bids/
  derivatives/
    atlasRepository/
      dataset_description.json
      atlas-AAL_description.json
      atlas-AAL_dseg.tsv
      atlas-AAL_dseg.json
      atlas-AAL_dseg.nii.gz
      atlas-Destrieux_description.json
      atlas-Destrieux_dseg.tsv
      atlas-Destrieux_dseg.json
      atlas-Destrieux_dseg.nii.gz
```

### Multiple atlases in subdirectories in the same derivative dataset

```Text
bids/
  derivatives/
    AtlasRepository/
      dataset_description.json
      atlas-AAL/
        atlas-AAL_description.json
        atlas-AAL_dseg.tsv
        atlas-AAL_dseg.json
        atlas-AAL_dseg.nii.gz
      atlas-Destrieux/
        atlas-Destrieux_description.json
        atlas-Destrieux_dseg.tsv
        atlas-Destrieux_dseg.json
        atlas-Destrieux_dseg.nii.gz
```


## I want to transform/resample a public atlas onto subject specific space(s)

This is a use case where a publicly available/previously generated atlas is transformed/resampled into subject spaces.
In this example, the referenced atlas is also in derivatives, but it could
also be an external link.

### Filesystem

```Text
bids/
  sub-01/
    anat/
      sub-01_T1w.nii.gz
  derivatives/
    atlas-MyNewAtlas/
      atlas-MyNewAtlas_description.json
      atlas-MyNewAtlas_dseg.tsv
      atlas-MyNewAtlas_dseg.json
      atlas-MyNewAtlas_dseg.nii.gz
    resampleAtlasToSubjects/
      seg-MyNewAtlas_dseg.json  # recommended
      seg-MyNewAtlas_dseg.tsv  # optional
      sub-01/
        func/
          sub-01_space-T1w_seg-MyNewAtlas_dseg.nii.gz
          sub-01_space-T1w_seg-MyNewAtlas_dseg.tsv  # optional
          sub-01_space-T1w_seg-MyNewAtlas_dseg.json  # optional
```

### atlas-MyNewAtlas/atlas-MyNewAtlas_description.json (Required)

```JSON
{
  "Name": "MyNewAtlas",
  "Authors": [
    "John Doe",
    "Jane Doe"
  ]
}
```

### atlas-MyNewAtlas/atlas-MyNewAtlas_dseg.tsv (Required)

In the original atlas, the index/label information is stored in a tsv file.

| Index | Label       |
|:-----:|-------------|
| 1     | amygdala    |
| 2     | hippocampus |

### atlas-MyNewAtlas/atlas-MyNewAtlas_dseg.json (Required)

```JSON
{
  "SpatialReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
  "Resolution": "Matched with original template resolution (2x2x2 mm^3)"
}
```

### atlas-MyNewAtlas/atlas-MyNewAtlas_dseg.nii.gz (Required)

The actual atlas that contains the value 1 for voxels
in the amygdala and 2 for voxel in the hippocampus.

### resampleAtlasToSubjects/seg-MyNewAtlas_dseg.json (Recommended)

Having sources here helps to keep track of the original atlas used to generate the subject-specific atlases.
This could be defined in the subject directories, but it is more efficient to define it at the top level.

```JSON
{
  "Sources": [
     "atlas-MyNewAtlas:atlas-MyNewAtlas_dseg.nii.gz",
  ]
}
```

### resampleAtlasToSubjects/seg-MyNewAtlas_dseg.tsv (Optional)

In the applied the index/label information is stored in a tsv file,
this could differ from the original atlas, but will generally be the same.

| Index | Label       |
|:-----:|-------------|
| 1     | amygdala    |
| 2     | hippocampus |

### resampleAtlasToSubjects/sub-01/func/sub-01_space-T1w_seg-MyNewAtlas_dseg.tsv (Optional)

For this subject, the resampling/transformation result in the elimination of the
hippocampus, either because of a lesion or from the resolution of the space
being resampled into.

| Index | Label       |
|:-----:|-------------|
| 1     | amygdala    |


### resampleAtlasToSubjects/sub-01/func/sub-01_space-T1w_seg-MyNewAtlas_dseg.json (Recommended)

This defines the spatial reference of the atlas in subject space.
This is important for understanding the spatial relationship between the atlas and the subject data.

```JSON
  {
    "SpatialReference": "bids:sub-01/anat/sub-01_T1w.nii.gz",
    "Resolution": "Matched with original anat resolution (1x1x1 mm^3)"
  }
```
## Case N/A: Using a public atlas with my subject data resampled into the atlas template space

The same file from the public atlas can already be applied to the subject data, no need to transform/resample the atlas into subject specific directories.

## I want to transform/resample a shared/public atlas into new template space

When you are extending an atlas to include other spaces and you are not the
owner/curator of the atlas and cannot modify the original atlas,
you will likely copy the `.tsv` and `_description.json` files
from the original atlas for re-use.

### FileSystem

```Text
  derivatives/
    atlas-ExtendedAtlas/
      atlas-ExtendedAtlas_description.json
      atlas-ExtendedAtlas_dseg.tsv
      atlas-ExtendedAtlas_space-Tal_dseg.json
      atlas-ExtendedAtlas_space-Tal_dseg.nii.gz
      atlas-ExtendedAtlas_space-MNINew_dseg.json
      atlas-ExtendedAtlas_space-MNINew_dseg.nii.gz
```

### atlas-ExtendedAtlas/atlas-ExtendedAtlas_description.json (Required)

```JSON
{
  "Name": "ExtendedAtlas",
  "Authors": [
    "John Doe",
    "Jane Doe"
  ]
}
```

### atlas-ExtendedAtlas_dseg.tsv (Required)

| Index | Label       |
|:-----:|-------------|
| 1     | amygdala    |
| 2     | hippocampus |

### atlas-ExtendedAtlas_space-Tal_dseg.json (Required)

```JSON
{
  "SpatialReference": "URI/URL to Talairach space",
  "Resolution": "Matched with original template resolution (2x2x2 mm^3)",
  "Sources": [
    "URI/URL to original atlas in original space"
  ]
}
```

### atlas-ExtendedAtlas_space-Tal_dseg.nii.gz (Required)

The actual atlas transformed into Talairach space.


### atlas-ExtendedAtlas_space-MNINew_dseg.json (Required)

```JSON
{
  "SpatialReference": "URI to MNI1New space",
  "Resolution": "Matched with original template resolution (2x2x2 mm^3)",
  "Sources": [
    "URI/URL to original atlas in original space"
  ]
}
```

### atlas-ExtendedAtlas_space-MNINew_dseg.nii.gz (Required)

The actual atlas transformed into MNINew space.

## I want to create subject specific atlases derived from subject specific data

The `seg-individualConnectome.json` will typically be the same for all subjects if the
process for generating the atlas is the same for all subjects.

```Text
bids/
  derivatives/
    subjectAtlases/
      seg-individualConnectome_dseg.json # recommended
      seg-individualConnectome_dseg.tsv
  sub-01/
    func/
      sub-01_space-orig_seg-individualConnectome_dseg.nii.gz
      sub-01_space-orig_seg-individualConnectome_dseg.tsv
      sub-01_space-orig_seg-individualConnectome_dseg.json
  sub-02/
    func/
      sub-02_space-orig_seg-individualConnectome_dseg.nii.gz
      sub-02_space-orig_seg-individualConnectome_dseg.tsv
      sub-02_space-orig_seg-individualConnectome_dseg.json

```

### Case 1: sharing atlas(es) to be used by others

In the simplest case, there are four files for each atlas.
`atlas-<label>_description.json` contains metadata about the atlas, `atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv` contains the index/label information for the atlas, and `atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json` contains spatial information about the atlas file
projected/transformed into a template space.
If the atlas is projected/transformed into multiple spaces, generally the same `atlas-<label>_description.json` file is used for all spaces, but the sidecar
.json files are specific to each space.
If there are a number of atlases to share that cannot be differentiated by the available entities (`space`, `res`, `desc`, etc.) and suffixes/extensions then
each atlas may have its own directory, or be represented in a single directory with a unique identifier for each atlas.

#### Each atlas gets its own derivative directory
```Text
<dataset>/
  derivatives/
    <pipeline1>/
      atlas-<label>_description.json
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
    <pipeline2>/
      atlas-<label>_description.json
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
```

#### Multiple atlases in the same directory
```Text
<dataset>/
  derivatives/
    <pipeline1>/
      atlas-<label1>_description.json
      atlas-<label1>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label1>_space-<label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label1>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
      atlas-<label2>_description.json
      atlas-<label2>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label2>_space-<label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label2>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
```

#### Multiple atlases in subdirectories in the same derivative dataset

```Text
<dataset>/
  derivatives/
    <pipeline1>/
      atlas-<label1>/
        atlas-<label1>_description.json
        atlas-<label1>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
        atlas-<label1>_space-<label>_desc-<label>_[dseg|probseg|mask].json
        atlas-<label1>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
      atlas-<label2>/
        atlas-<label2>_description.json
        atlas-<label2>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
        atlas-<label2>_space-<label>_desc-<label>_[dseg|probseg|mask].json
        atlas-<label2>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
```

#### Same atlas projected into multiple template spaces

```Text
<dataset>/
  derivatives/
    <pipeline1>/
      atlas-<label>_description.json
      atlas-<label>_space-<space1label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label>_space-<space1label1>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label>_space-<space1label1>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
      atlas-<label>_space-<space2label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label>_space-<space2label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label>_space-<space2label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
```

### Case 2: using a shared atlas to transform/resample into subject spaces

This is a typical use case where a publicly available/previously generated atlas is transformed/resampled into subject spaces.


```Text
<dataset>/
  derivatives/
    <pipeline1>/
      atlas-<label>_description.json
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
      atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
      atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
    <pipeline2>/
      seg-<label>_[dseg|probseg|mask].json # {"Sources": ["derivatives/pipeline1:atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]"]}
      seg-<label>_[dseg|probseg|mask].tsv
      sub-01/
        func/
          sub-01_space-<label>_seg-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz]
          sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].tsv
          sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].json
```

With this structure, the atlas is projected into subject space and/or resampled into
subject space.
As with use case 1, the top level directory contains the four atlas files.
Then the atlas is resampled/transformed into each individual subject space.

## Case 3: using a shared atlas to transform/resample it into new template space

## Case 4: representing subject-specific atlases derived from the corresponding subject’s data

```Text
<dataset>/derivatives/<pipleline>
  atlas-<label>_description.json
  sub-01/
    anat/
      sub-01_atlas-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz][.ome-tiff|.png]
      sub-01_atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
      sub-01_atlas-<label>_desc-<label>_[dseg|probseg|mask].json
      sub-01_atlas-<label>_desc-<label>_coordsystem.json
```

The `atlas-<label>_description.json` will typically be the same for all subjects if the
process for generating the atlas is the same for all subjects.
