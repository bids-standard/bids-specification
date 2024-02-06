# BIDS-Atlas

In the following we describe how an [atlas](schema/objects/entities.yaml#atlas) can be shared within BIDS. We describe a broad set of atlases and use cases thereof.

More specifically, this entails providing and referring to existing atlas datasets, describing atlases that were newly derived within an analysis, and providing information for derivatives that were obtained through them. The first would comprise (publicly) available atlases, for example, Destrieux et al. ([doi.org/10.1016/j.neuroimage.2010.06.010](https://doi.org/10.1016/j.neuroimage.2010.06.010)), AAL ([doi.org/10.1006/nimg.2001.0978](https://doi.org/10.1006/nimg.2001.0978)), Yeo ([doi.org/10.1152/jn.00338.2011](https://doi.org/10.1152/jn.00338.2011)) and JHU DTI-based white-matter atlases ([eBook ISBN: 9780080456164](https://shop.elsevier.com/books/mri-atlas-of-human-white-matter/mori/978-0-444-51741-8) and [doi.org/10.1016/j.neuroimage.2007.07.053](https://doi.org/10.1016/j.neuroimage.2007.07.053)), while the second would include atlases obtained through analyses within a dataset at hand, for example, resting-state networks and functional localizers. Importantly, the latter can also be utilized as existing atlases if made available. The third would entail referencing an atlas and its properties used to derive e.g. parcellated time series or a connectivity matrix.

## Atlas as new DatasetType
Here we introduce an additional value to the `DatasetType field` of `dataset_description.json`. If a dataset declares its DatasetType to be [atlas](schema/objects/entities.yaml#atlas), the top-level directories MUST be `atlas-` instead of `sub-`. This will allow sharing existing atlases as stand-alone datasets, validating them via the [BIDS validator](https://github.com/bids-standard/bids-validator) and enabling their integration as sub-datasets of other BIDS datasets.

## File formats for the raw data
BIDS-Atlas aims to describe brain atlases via three REQUIRED files. They entail the atlas itself (e.g. in .nii, .nii.gz, .gii, or .tsv), a file indexing/labeling each node in the atlas (in .tsv) and a file containing exhaustive meta-data about the atlas (in .json).

The usage of [_desc-](schema/objects/entities.yaml#desc) is generally discouraged but should be evaluated on a case by case basis in order to keep this identifier available for necessary cases. Specifically, this refers to the atlas at hand and potential different versions thereof. As a rule of thumb, BIDS-Atlas proposed to evaluate and consider how many versions across how many levels of versions an atlas is (commonly) provided and used in.
If there is only one version, as in "release", of an atlas and no sub-versions, as in "different parcel numbers" (or comparable), [_desc-](schema/objects/entities.yaml#desc) is most likely not expected and/or required. An example for [_desc-](schema/objects/entities.yaml#desc) in such a use case would be to indicate a subset of parcels and would entail the addition of the [_mask-](schema/objects/entities.yaml#mask) extension, e.g. providing/using the "postcentral gyrus" region of the [Destrieux atlas](doi:10.1093/cercor/bhg087.) would result in the following file name: `atlas-Destrieux_space-MNI152NLin6Asym_res-2_desc-PostCentralGyrus_mask.nii.gz`.
Similar to the above case, if there are multiple versions, as in "release", of an atlas and no sub-versions, as in "different parcel numbers" (or comparable), [_desc-](schema/objects/entities.yaml#desc) is also most likely not expected and/or required, as the version(s) (release(s)) should be indicated via `atlas-`. For example, the different versions of the [AAL parcellation](http://www.gin.cnrs.fr/AAL-217?lang=en) would result in the following file names: `atlas-AAL1_space-MNI152NLin6Asym_res-2.nii.gz`, `atlas-AAL2_space-MNI152NLin6Asym_res-2.nii.gz` and `atlas-AAL3_space-MNI152NLin6Asym_res-2.nii.gz`.
Given an atlas has only one version, as in "release", and multiple sub-versions, as in "different parcel numbers" (or comparable), [_desc-](schema/objects/entities.yaml#desc) is considered appropriate. For example, when indicating information pertaining to the probabilistic nature of an atlas such as the [_probseg](schema/objects/entities.yaml#probseg) version of the [Harvard-Oxford parcellation](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases): `atlas-HarvardOxford_res-2_desc-th25_probseg.nii.gz`.
In cases where an atlas has multiple versions, as in "release", and sub-versions, as in "different parcel numbers" (or comparable), the version(s) (release(s)) should be indicated via `atlas-` as outlined above and the sub-versions should be indicated via [_desc-](schema/objects/entities.yaml#desc). For example, different versions and sub-versions of the [Schaefer parcellation](https://github.com/ThomasYeoLab/CBIG/blob/master/stable_projects/brain_parcellation/Schaefer2018_LocalGlobal/Parcellations/Updates/Update_20190916_README.md) would be denoted as follows: `atlas-Schaefer2018_space-MNI152NLin6Asym_res-2_desc-400Parcels7Networks.nii.gz`, `atlas-Schaefer2018_space-MNI152NLin6Asym_res-2_desc-400Parcels17Networks.nii.gz`, `atlas-Schaefer2022_space-MNI152NLin6Asym_res-2_desc-800Parcels7Networks.nii.gz` and `atlas-Schaefer2022_space-MNI152NLin6Asym_res-2_desc-800Parcels17Networks.nii.gz`.

Importantly, already existing BIDS entities should be used to indicate certain aspects of an atlas, instead of [_desc-](schema/objects/entities.yaml#desc), e.g. [hemi](schema/objects/entities.yaml#hemi) to denote a given hemisphere and [_dseg](schema/objects/entities.yaml#dseg)/[_probseg](schema/objects/entities.yaml#probseg) to denote deterministic and probabilistic atlases respectively.

However, as mentioned above, these are general guidelines and the exact implementation should be evaluated on a case by case basis, with deviations following common BIDS principles being permitted.

## Directory Structure
BIDS-Atlas focuses on the utilization of atlases while also allowing their sharing. Thus, atlases are either stored within a dedicated `atlas` directory at the BIDS root directory (comparable to the `code` directory), such files are the non-altered/original atlases or within a given directory under `derivatives`. In the second case, atlases are altered, derived or applied and thus multiple use cases have to be distinguished as indicated further below.

### Representing an atlas as a dataset

The first option refers to atlases that were not altered, e.g. via spatial transformations and/or resampling or applied to data and thus their initial inclusion/utilization in a given dataset. If there is only this form of atlases (i.e., the tool used), they are always shared at the root directory and everything else is under derivatives. This allows validating any

```Text
<dataset>/atlas/
```

using the  [BIDS validator](https://github.com/bids-standard/bids-validator). Importantly, only this case follows the same directory structure as [sub](schema/objects/entities.yaml#sub), i.e., one dedicated directory for each atlas within a given dataset.
The default way of storage of the non-altered atlas at the root directory looks like this:

```Text
<dataset>/atlas/atlas-<label>/
  atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
  atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
  atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
```

### Representing an atlas within a dataset

Besides this default and required storage of the non-altered atlas at the root directory, the second use case provides three sub-cases to store atlases that were either altered, applied, or derived within a given dataset. While case 1 uses the [atlas](schema/objects/entities.yaml#atlas) identifier, case 2 and 3 use the [seg](schema/objects/entities.yaml#seg) identifier. The difference between the use of [atlas](schema/objects/entities.yaml#atlas) and [seg](schema/objects/entities.yaml#seg) identifier is that in the first case an existing atlas is changed, e.g. transformed, but still remains an atlas. In the other case, the atlas is used to define a segmentation, e.g. the AAL atlas is used to define a cortical parcellation, that then is applied to a subjects other content, e.g. a cortical thickness or binding potential map.

#### Case 1

First, a given atlas underwent modifications before its utilization, specifically spatial transformations to a template space and is used in this form within a given pipeline. In this case, the respective BIDS-Atlas files will be stored at both the BIDS root level and the given pipeline directory under `derivatives`. Files stored at the BIDS root level will follow the structure outlined in option 1, while files stored at the pipeline level will follow the respective naming conventions. For example, if an atlas was spatially transformed to a certain MNI template, then the BIDS-Atlas files will be stored within the respective pipeline directory and the corresponding [space](schema/objects/entities.yaml#space)-<label> identifier will be adapted accordingly.

```Text
<dataset>/atlas/atlas-<label>/
  atlas-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
  atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
  atlas-<label>_desc-<label>_[dseg|probseg|mask].json

<dataset>/derivatives/<pipeline>/
  atlas-<label>_space-<label>_res-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|.tsv][.gz]
  atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
  atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
```

#### Case 2

Second, a given atlas underwent modifications before its utilization, specifically spatial transformations to an individual subject space and is used in this form. In this case, the respective BIDS-Atlas files will be stored at both the BIDS root level and at the given subject level under `derivatives`. Files stored at the BIDS root level will follow the structure outlined in option 1. Files stored at the subject level now use the [seg](schema/objects/entities.yaml#seg) entity with it's value referring to the atlas use on a given file.

```Text
<dataset>/atlas/atlas-<label>/
  atlas-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
  atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
  atlas-<label>_desc-<label>_[dseg|probseg|mask].json

<dataset>/derivatives/
  sub-01/
    func/
      sub-01_space-<label>_seg-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz]
      sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].tsv
      sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].json
```

#### Case 3

Third, a given atlas was derived from the corresponding subject’s data and thus is subject-specific. In this case, the `atlas` directory at the root of the dataset does not exist. The subject specific atlas filenames are the same as in case 2 at the subject level within the modality directory of the data the atlas was derived from. Optionally, a `*_coordsystem.json` file that specifies the [Image-based Coordinate System](/appendices/coordinate-systems.md) of the subject-specific atlas can be used for e.g. an histological atlas/segmentation. Unlike as in the prior use case, the [atlas](schema/objects/entities.yaml#atlas) identifier will be replaced with the [seg](schema/objects/entities.yaml#seg) identifier.

```Text
<dataset>/derivatives/
  sub-01/
    anat/
      sub-01_atlas-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz][.ome-tiff|.png]
      sub-01_atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
      sub-01_atlas-<label>_desc-<label>_[dseg|probseg|mask].json
      sub-01_atlas-<label>_desc-<label>_coordsystem.json
```

### Representing locations in an atlas file

The `[probseg|dseg|mask].[nii|dlabel.nii|label.gii][.gz]` file represents the location and extent of the nodes/parcels/regions within the atlas. Different file types are supported based on the modality and atlas at hand. In more detail, this encompasses the following three options:

1. [_dseg](schema/objects/suffixes.yaml#dseg): Each node is labeled with a unique integer corresponding to its row/index in the tsv sidecar.
2. [_probseg](schema/objects/suffixes.yaml#probseg): Each node is represented along an additional dimension of the file (e.g., a 4D NIfTI file where each volume represents a node) and its position in that dimension corresponds to its row/index in the tsv sidecar.
3. [_mask](schema/objects/suffixes.yaml#mask): Either each voxel represents a node or the entire mask is a single node. How the mask should be interpreted is determined by other specifications. Based on these options, an atlas can take the following forms in the here proposed specification (non-exhaustive list):
a.  A 3D NIfTI file with unique integers defining nodes
b.  A 4D binary NIfTI file with spatially overlapping nodes in each volume (along the 4th dimension)
c.  A 4D NIfTI file with overlapping nodes with continuous values for each voxel within a volume

Examples:
```Text
atlas-HarvardOxford_res-2_dseg.nii.gz
atlas-HarvardOxford_res-2_probseg.nii.gz
atlas-HarvardOxford_res-2_desc-HeschlGyrus_mask.nii.gz
```

General Recommendations: This specification relies on the inheritance principle whereby files deeper in the hierarchy inherit from the top-level files. If you have atlas files that are transformed to subject-specific space for each subject, then excluding the space entity at the top level is a good way to ensure the file inherits information about the original atlas. Additionally, the [desc](schema/objects/entities.yaml#desc) label should be avoided as an inherited file. One may need to use the [desc](schema/objects/entities.yaml#desc) label to contain information related or unrelated to the atlas.

The `[probseg|dseg|mask|channels].tsv` file indexes and labels each node/parcel/region within the atlas. This file resembles the typical Look Up Table (LUT) often shared with atlases. This file will be essential for downstream workflows that generate matrices or other derived files within which node/parcel/region information is required, as the index/label fields will be used to reference the original anatomy the index/labels are derived from. Additional fields can be added with their respective definition/description in the sidecar json file.

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
   <td>OPTIONAL. Label of Network (e.g. Dorsal Attention Network)
   </td>
  </tr>
  <tr>
   <td>coordinate_report_strategy
   </td>
   <td>OPTIONAL (RECOMMENDED if x, y, z keys are specified).  The strategy used to assess and report x, y and z coordinates of a given node/parcel/region. For example, “CenterOfMass”.
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
   <td>OPTIONAL. MUST BE ONE OF: “left”, “right”, “bilateral”. Indicate whether the node/parcel/region is in the left or right hemispheres, or is available bilaterally.
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
   <td>OPTIONAL. “XY”, where X can be L:left, R:right, B:bilateral, and Y can be F:frontal, T:temporal, P:parietal, O:occipital
   </td>
  </tr>
</table>

Example:
```Text
index	label	network_label	hemisphere
1	Heschl's Gyrus	Somatomotor	left
2	Heschl's Gyrus	Somatomotor	right
```

The `[probseg|dseg|mask].json` file provides metadata to uniquely identify, describe and characterize the atlas, as well as give proper attribution to the creators. Additionally, SpatialReference serves the important purpose of unambiguously identifying the space the atlas is labeled in.

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
   <td>OPTIONAL. RECOMMENDED if probabilistic atlas. Should indicate what the 4th dimension entails/refers to. MUST be “Indices” or   .
   </td>
  </tr>
  <tr>
   <td>CoordinateReportStrategy
   </td>
   <td>OPTIONAL. MUST BE ONE OF: “peak”, “center_of_mass”, “other”. Indicate the method of coordinate reporting in statistically significant clusters. Could be the “peak” statistical coordinate in the cluster or the “center_of_mass” of the cluster. RECOMMENDED if x, y ,z values are set in the .tsv file.
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
   <td>RECOMMENDED. Indicate what data modality the atlas was derived from, e.g. "cytoarchitecture", "resting-state", "task".
   </td>
  </tr>
  <tr>
   <td>LevelType
   </td>
   <td>RECOMMENDED. Indicate what analysis level the atlas was derived from, e.g. "group", "individual".
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

# BIDS-Atlas Example datasets
Within the following, multiple examples showcasing the proposed extension are provided. They include BEP-specific as well as other/general BIDS files.

## Atlas as dataset - single existing atlas in template space

The example below illustrates how a single existing atlas in template space is represented as a dataset according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford atlas in MN152NLin6Asym space with a resolution of 2 mm3, used without modifications (e.g. transformations, subsetting, etc.) for all subjects to which the pipeline was applied.

```Text
my_dataset/atlas-HarvardOxford/
  atlas-HarvardOxford_res-2_dseg.json
  atlas-HarvardOxford_res-2_dseg.nii.gz
  atlas-HarvardOxford_res-2_dseg.tsv
```

The content of each file is further outlined in the following, starting with the .json sidecar file containing meta-data about the atlas at hand.

Example content of the `atlas-HarvardOxford_res-2_dseg.json` file:

```JSON
{
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
    "Name": "FSL's MNI ICBM 152 non-linear 6th Generation Asymmetric Average Brain Stereotaxic Registration Model",
  "RRID": "SCR_002823",
  "ReferencesAndLinks": [
    "https://doi.org/10.1016/j.neuroimage.2012.01.024",
    "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases"
  ],
  "Species": "Human"
}
```

Next, the content of the tsv files describing the indices and corresponding labels present in the atlas at hand.

Example content of the `atlas-HarvardOxford_res-2_dseg.tsv` file:

```Text
index	label	hemisphere
0	Background	bilateral
1	Frontal Pole	bilateral
2
Insular Cortex	bilateral
3	Superior Frontal Gyrus	bilateral
4	Middle Frontal Gyrus	bilateral
5	Inferior Frontal Gyrus, pars triangularis	bilateral
6	Inferior Frontal Gyrus, pars opercularis	bilateral
```

## Multiple existing atlases in template space
The example below illustrates how multiple existing atlases in the same template space are represented according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford, Schaefer, Yeo and MSDL atlases, all in MN152NLin6Asym space and with a resolution of 2 mm3, were utilized without modifications (e.g. transformations, subsetting, etc.) for all subjects to which the pipeline was applied. Importantly, all atlas-related information is indicated via the value of the atlas- key and not via desc- to help prevent inheritance problems in subsequent steps. Here, this was used to indicate that the Harvard-Oxford atlas in its version with a maximum probability of 50, the Schaefer atlas in its 400 parcel version and the Yeo atlas in its 17 networks version were used. The respective information found in each file follows the example outlined in 4.1 as atlases were used independently from one another.


```Text
bids/atlases/
  atlas-HarvardOxford/
    atlas-HarvardOxford_dseg.nii.gz
    atlas-HarvardOxford_dseg.json
    atlas-HarvardOxford_dseg.tsv
  atlas-Schaefer400/
    atlas-Schaefer400_dseg.nii.gz
    atlas-Schaefer400_dseg.json
    atlas-Schaefer400_dseg.tsv
  atlas-Yeo17/
    atlas-Yeo17_dseg.nii.gz
    atlas-Yeo17_dseg.json
    atlas-Yeo17_dseg.tsv
  atlas-msdl/
    atlas-msdl_probseg.nii.gz
    atlas-msdl_probseg.json
    atlas-msdl_probseg.tsv
```
 
## Single existing atlas transformed to subject space
The example below illustrates how a single existing atlas transformed into a subject’s native space space is represented according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford atlas with a resolution of 2 mm3 that was transformed from the MN152NLin6Asym template space to a given subject’s native T1w space. While the original atlas-related files remain as outlined in the use case in template space, the spatially transformed version of the nii.gz atlas file will be placed within a given subjects directory. The precise location within the latter depends on the modality space to which the atlas was transformed to, e.g. anat, func or dwi. The same location furthermore entails a corresponding json file outlining further information on the source atlas and applied transformation(s).


```Text
bids/atlases/atlas-HarvardOxford/
  atlas-HarvardOxford_dseg.json
  atlas-HarvardOxford_dseg.tsv
  atlas-HavardOxford2_dseg.nii.gz
bids/derivatives/pipeline-<name>/
  sub-01/
    anat/
      sub-01_T1w.nii.gz
      sub-01_space-T1w_seg-HarvardOxfordThr50_res-2_dseg.nii.gz
      sub-01_space-T1w_seg-HarvardOxfordThr50_res-2_dseg.json
      sub-01_space-T1w_seg-HarvardOxfordThr50_res-2_dseg.tsv
```

The json file accompanying the transformed atlas should include the following information.

Example content of the `sub-01_space-T1w_seg-HarvardOxford_res-2_dseg.json` file:

```JSON
{
  "BIDSVersion": "1.1.0",
  "SpatialReference": "sub-01/anat/sub-01_T1w.nii.gz",
  "Space": "T1w",
  "Resolution": "Matched with original resolution in subject T1w space (1x1x1 mm^3)",
  "Sources": [],
  "transformation":
}
```

##  MyConnectome example

The example below illustrates how two atlases, an individual surface-based cortical parcellation in FS_lr space (called Russome), and the subcortical regions from a volumetric segmentation provided by the FreeSurfer aseg, are represented according to the atlas BEP. While the FreeSurfer atlas-related files have two instances, one as outlined in the use case in template space and one as outlined in the use case covering subject spaces, the individual parcellation in FS_lr space will be placed only within a given subjects directory. The same location furthermore entails a corresponding json file outlining further information on the atlas and applied analysis to obtain it.

```Text
bids/atlases/atlas-FreeSurferASEG/
  atlas-FreeSurferASEG_dseg.json
  atlas-FreeSurferASEG_dseg.tsv
  atlas-FreeSurferASEG_dseg.nii.gz

bids/derivatives/pipeline-<name>/
  sub-01/
    anat/
      sub-01_space-T1w_seg-FreeSurferASEG_res-2_dseg.nii.gz
      sub-01_space-T1w_seg-FreeSurferASEG_res-2_dseg.json
      sub-01_space-T1w_seg-FreeSurferASEG_res-2_dseg.tsv
    func/
      sub-01_space-FSlr_seg-Russome_res-2_dseg.nii.gz
      sub-01_space-FSlr_seg-Russome_res-2_dseg.json
      sub-01_space-FSlr_seg-Russome_res-2_dseg.tsv
```

The json file accompanying the functionally derived atlas should include the following information.

Example content of the `sub-01_task-rest_atlas.json` file contains top-level metadata about the atlas:

```JSON

"Atlas":
{
  "Russome":
  {
    "Atlasfile": "/link/to/russome/file",
    "Extra": "individualized surface parcellation"
  },
  "FS_aseg": {
    "Atlasfile": "/link/to/aseg/file",
    "Extra": "freesurfer aseg"
  }
}

```

## Quantitative atlas examples

The example below is for PET imaging, but this applies to any quantitative mapping (PET or qMRI). Compared to anatomical atlases, quantitative atlases give reference values to be compared with. Such values can be derived voxel/vertex wise (see case 1) or per region of interest (ROI) (see case 2). In the latter case, ROIs are generally derived from an anatomical atlas.

We created a Molecular Imaging Brain Atlases (MIBA) from 16 subjects who underwent a [11C]PS13 PET scan, a radioligand that quantifies cyclooxygenase-1 (see [source data](https://openneuro.org/datasets/ds004332/versions/1.0.2)). Our atlas consists of mean and standard deviations of PS13 target distribution volumes (VT) computed across the 16 subjects at each voxel, in standard MRI spaces. We also project these distribution volumes onto the FreeSurfer cortical surfaces and include these as well.  The goal is to allow researchers with MRI-only data to correlate their results to the distribution volume of PS13. The dataset can be found [here](https://openneuro.org/datasets/ds004401/versions/1.1.0).

### Case 1: voxel/vertex wise analysis

Example directory content for a quantitative atlas that provides values at all voxels and/or vertices:

```Text
bids/atlas/atlas-ps13/
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

Example directory content for a quantitative atlas that provides values for certain ROIs only, in this case defined by the AAL atlas:

```Text
bids/atlas/
  atlas-mni305/
    atlas-aparc.DKTatlas+aseg.mgz
    atlas-aparc.DKTatlas+aseg.tsv
    atlas-RB_all_2008-03-26.probseg.gca
    atlas-RB_all_2008-03-26.probseg.tsv
  atlas-ps13/
    atlas-ps13_space-fsaverage_hemi-L_stat-mean_meas-VT_seg-AAL_mimap.json
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

Note that there is no image file present in a regional quantitative atlas. The json file accompanying the quantitative atlas should include the information as in [Single existing atlas in template space](#_Single_existing_atlas_in_template_space).
