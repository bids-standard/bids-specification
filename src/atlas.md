# BIDS-Atlas

## Atlas as new DatasetType
Here we introduce an additional value to the DatasetType field of dataset_description.json. If a dataset declares its DatasetType to be "atlas", the top-level directories MUST be `atlas-` instead of `sub-`. This will allow sharing existing atlases as stand-alone datasets, validating them via the BIDS validator and enabling their integration as sub-datasets of other BIDS datasets.

## File formats for the raw data
BIDS-Atlas aims to describe brain atlases via three REQUIRED files. They entail the atlas itself (e.g. in .nii, .nii.gz, .gii, or .tsv), a file indexing/labeling each node in the atlas (in .tsv) and a file containing exhaustive meta-data about the atlas (in .json). 

The usage of _desc- is currently discouraged in order to keep this identifier available for necessary cases. Phrased differently, instead of using the _desc- identifier to refer to a specific version of a given atlas (e.g. atlas-Schaefer_res-2_desc-400.nii.gz), the respective information should be captured in the atlas- identifier (e.g. atlas-Schaefer400_res-2.nii.gz)  and the _desc- used for e.g. referring to subsets of a given atlas (e.g. atlas-Schaefer400_res-2_desc-label01_mask.nii.gz). Common identifiers (e.g., hemi) currently exist and should not be used in lieu of the _desc- identifier, whereas information pertaining to the probabilistic nature of an atlas threshold is appropriate for the _desc- identifier (e.g. atlas-HarvardOxford_res-2_desc-th25_probseg.nii.gz)

## Directory Structure
Importantly, BIDS-Atlas focuses on the utilization of atlases while also allowing their sharing. Thus, atlases are either stored within a dedicated atlas directory at the BIDS root directory (comparable to the “code” directory) or within the directory of a given subject’s derivatives. Given the manifold use cases of atlases, the files mentioned above are utilized in BIDS-Atlas in two general ways: non-altered/original required at BIDS root and altered/derived/applied atlases stored under derivatives. The first option refers to atlases that were not altered, e.g. via spatial transformations and/or resampling or applied to data and thus their initial inclusion/utilization in a given dataset. If there is only this form of atlases (i.e., the tool used), they are always shared at the root folder and everything else is under derivatives. This allows validating any  <dataset>/atlas/ using the  BIDS validator. Importantly, only this case uses the “atlas-” identifier, following the same directory structure as “sub”, i.e., one dedicated directory for each atlas within a given dataset. 

Representing the atlas at the dataset level, 
<dataset>/atlases/atlas-<label>/
atlas-<label>_space-<label>[_desc-<label>]_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json

Besides this default and required storage of the non-altered atlas at the root directory, the second use case provides three options to store atlases that were either altered, applied, or derived within a given dataset. While option 1 also uses the “atlas” identifier, options 2 and 3 use the “seg” identifier, as outlined in the next paragraphs.

First: a given atlas underwent modifications before its utilization, specifically spatial transformations to a template space and is used in this form within a given pipeline. In this case, the respective BIDS-Atlas files will be stored at both the BIDS root level and the given pipeline directory under “derivatives”. Files stored at the BIDS root level will follow the structure outlined in option 1, while files stored at the pipeline level will follow the respective naming conventions. For example, if an atlas was spatially transformed to a certain MNI template, then the BIDS-Atlas files will be stored within the respective pipeline directory and the corresponding space-<label> identifier will be adapted accordingly. 

<dataset>/atlases/atlas-<label>/
atlas-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
atlas-<label>_desc-<label>_[dseg|probseg|mask].json
<dataset>/derivatives/<pipeline>/
atlas-<label>_space-<label>_res-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|.tsv][.gz]
atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].tsv
atlas-<label>_space-<label>_desc-<label>_[dseg|probseg|mask].json
atlas-<label>_space-<label>_desc-<label>_edges.[tck|<eeg,meg>]

Second: a given atlas underwent modifications before its utilization, specifically spatial transformations to an individual subject space and is used in this form. In this case, the respective BIDS-Atlas files will be stored at both the BIDS root level and at the given subject level within the pipeline directory under “derivatives”. Files stored at the BIDS root level will follow the structure outlined in option 1, while files stored at the subject level will be placed within the modality directory of the space the atlas was spatially transformed to and follow the subject-related naming conventions. For example, if an atlas was spatially transformed to the anatomical space of a given subject, then the BIDS-Atlas files will be stored within the respective subject’s anat directory and their file names will be prepended with the subject identifier. Additionally, instead of “atlas”, the “seg” identifier will be used to support a broader scope and more data modalities.  

<dataset>/atlases/atlas-<label>/
atlas-<label>_desc-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii][.gz]
atlas-<label>_desc-<label>_[dseg|probseg|mask].tsv
atlas-<label>_desc-<label>_[dseg|probseg|mask].json
<dataset>/derivatives/<pipeline>/
	anat/		sub-01_space-<label>_seg-<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz]
sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].tsv
sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].json
sub-01_space-<label>_seg-<label>_desc-<label>_edges.[tck|<eeg,meg>]


Third: a given atlas was derived from the corresponding subject’s data and thus is subject-specific. In this case, the respective BIDS-Atlas files are only stored at the subject level within the modality directory of the data the atlas was derived from. If a subject-specific atlas was spatially transformed from the space of the modality it was derived into the space of a different modality, then the BIDS-Atlas files would be stored in both respective modality directories. For example, if an atlas was derived from data in anat and shared/utilized as is, then the BIDS-Atlas files would only be stored in the anat directory. If the atlas was spatially transformed to the functional space of the respective subject, then the BIDS-Atlas files would be stored in both directories, anat and func. As in the prior use case, the “atlas” identifier will be replaced with “seg”.   

<dataset>/derivatives/<pipeline_name>/
sub-01/
	anat/		sub-01_space-<label>_seg_<label>_[dseg|probseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tsv][.gz]
sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].tsv
sub-01_space-<label>_seg-<label>_desc-<label>_[dseg|probseg|mask].json
sub-01_space-<label>_seg-<label>_desc-<label>_edges.[tck|<eeg,meg>]

 
### [probseg|dseg|mask].[nii|dscalar.nii|dlabel.nii|label.gii|tracts.trx/tck/trk][.gz]

This file represents the location and extent of the nodes/parcels/regions within the atlas. Different file types are supported based on the modality and atlas at hand. In more detail, this encompasses the following three options:

1.	_dseg: Each node is labeled with a unique integer corresponding to its row/index in the tsv sidecar.
2.	_probseg: Each node is represented along an additional dimension of the file (e.g., a 4D nifti file where each volume represents a node) and its position in that dimension corresponds to its row/index in the tsv sidecar.
3.	_mask: Either each voxel represents a node or the entire mask is a single node. How the mask should be interpreted is determined by other specifications. Based on these options, an atlas can take the following forms in the here proposed specification (non-exhaustive list):
a.	A 3D nifti file with unique integers defining nodes
b.	A 4D binary nifti file with spatially overlapping nodes in each volume (along the 4th dimension)
c.	A 4D nifti file with overlapping nodes with continuous values for each voxel within a volume

Examples
atlas-HarvardOxford_res-2_dseg.nii.gz
atlas-HarvardOxford_res-2_probseg.nii.gz
atlas-HarvardOxford_res-2_desc-HeschlGyrus_mask.nii.gz

General Recommendations: This specification relies on the inheritance principle whereby files deeper in the hierarchy inherit from the top-level files. If you have atlas files that are transformed to subject-specific space for each subject, then excluding the space entity at the top level is a good way to ensure the file inherits information about the original atlas. Additionally, the “desc” label should be avoided as an inherited file may need to use the desc label to contain information related or unrelated to the atlas.

 
### [probseg|dseg|mask|channels].tsv

This file indexes and labels each node/parcel/region within the atlas. This file resembles the typical Look Up Table (LUT) often shared with atlases. This file will be essential for downstream workflows that generate matrices, as the index/label fields will be used to reference the original anatomy the index/labels are derived from. Additional fields can be added with their respective definition/description in the sidecar json file.

index (or placeholder in fragment in reference)	REQUIRED. (Integer) The number associated with the node/parcel/region (right/left hemispheres may be different).
label	RECOMMENDED. The node name
network_id	OPTIONAL. Network ID the node/parcel belongs to
network_label
	OPTIONAL. Label of Network (e.g. Dorsal Attention Network)

CoordinateReportStrategy	OPTIONAL (RECOMMENDED if x, y, z keys are specified).  The strategy used to assess and report x, y and z coordinates of a given node/parcel/region. For example, “CenterOfMass”. 
x	OPTIONAL. The x-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
y	OPTIONAL. The y-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
z	OPTIONAL. The z-coordinate of the node in the spatial reference space (See SpatialReference in the .json file)
hemisphere	OPTIONAL. MUST BE ONE OF: “left”, “right”, “bilateral”. Indicate whether the node/parcel/region is in the left or right hemispheres, or is available bilaterally.
color
OPTIONAL. RGB color to use for the node.
seed
OPTIONAL. Seed vertex/channel of the node/region
region
OPTIONAL. “XY”, where X can be L:left, R:right, B:bilateral, and Y can be F:frontal, T:temporal, P:parietal, O:occipital






Example

index	label	network_label	hemisphere	…
1	Heschl’ Gyrus	Somatomotor	left	…
2	Heschl’ Gyrus	Somatomotor	right	…
…	…	…	…	…

### [probseg|dseg|mask].json

This file provides metadata to uniquely identify, describe and characterize the atlas, as well as give proper attribution to the creators. Additionally, SpatialReference serves the important purpose of unambiguously identifying the space the atlas is labeled in.


Name	REQUIRED. Name of the atlas
Description	RECOMMENDED. Longform description of the atlas
SpatialReference	RECOMMENDED. Point to an existing atlas in a template space (url or relative file path where this file is located).
CoordinateReportStrategy	OPTIONAL. MUST BE ONE OF: “peak”, “center_of_mass”, “other”. Indicate the method of coordinate reporting in statistically significant clusters. Could be the “peak” statistical coordinate in the cluster or the “center_of_mass” of the cluster. RECOMMENDED if x, y ,z values are set in the .tsv file. 
Authors	RECOMMENDED. List of the authors involved in the creation of the atlas
Curators	RECOMMENDED. List of curators who helped make the atlas accessible in a database or dataset
Funding	RECOMMENDED. The funding source(s) involved in the atlas creation
License	RECOMMENDED. The license agreement for using the atlas.
ReferencesAndLinks	RECOMMENDED. A list of relevant references and links pertaining to the atlas.
Species	RECOMMENDED. The species the atlas was derived from. For example, could be Human, Macaque, Rat, Mouse, etc.
DerivedFrom	RECOMMENDED. Indicate what data modality the atlas was derived from, e.g. "cytoarchitecture", "resting-state", "task".
LevelType	RECOMMENDED. Indicate what analysis level the atlas was derived from, e.g. "group", "individual".
Additional Columns	RECOMMENDED. Describe the respective column in the tsv







Example 

{
  	"Name": "FSL's MNI ICBM 152 non-linear 6th Generation Asymmetric Average 
   Brain Stereotaxic Registration Model",
 	"Authors": [
 “David Kennedy”,
 “Christian Haselgrove”,
 “Bruce Fischl”,
 “Janis Breeze”,
 “Jean Frazie”, 
 “Larry Seidman”,
 “Jill Goldstein”
 		],
 	"BIDSVersion": "1.1.0",
 	"Curators": "FSL team",
“SpatialReference”:   
“https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz”,
 	"Space": "MNI152NLin6Asym",
“Resolution”: “Matched with original template resolution (2x2x3 mm^3)”, 
 	"License": "See LICENSE file",
"RRID": "SCR_002823",
  	"ReferencesAndLinks": [
  "https://doi.org/10.1016/j.neuroimage.2012.01.024",
  "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases”
     ],
  	"Species": "Human"
}







 
# BIDS-Atlas Example datasets
Within the following, multiple examples showcasing the proposed extension are provided. They include BEP-specific as well as other/general BIDS files.

## Single existing atlas in template space

The example below illustrates how a single existing atlas in template space is represented according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford atlas in MN152NLin6Asym space with a resolution of 2 mm3, used without modifications (e.g. transformations, subsetting, etc.) for all subjects to which the pipeline was applied.  

my_dataset/atlases/atlas-HarvardOxford/
	atlas-HarvardOxford_res-2_dseg.json
	atlas-HarvardOxford_res-2_dseg.nii.gz
	atlas-HarvardOxford_res-2_dseg.tsv

The content of each file is further outlined in the following, starting with the .json sidecar file containing meta-data about the atlas at hand.

atlas-HarvardOxford_res-2_dseg.json

{
 	"Authors": [
 “David Kennedy”,
 “Christian Haselgrove”,
 “Bruce Fischl”,
 “Janis Breeze”,
 “Jean Frazie”, 
 “Larry Seidman”,
 “Jill Goldstein”
 		],
 	"BIDSVersion": "1.1.0",
 	"Curators": "FSL team",
“SpatialReference”:   
“https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz”,
 	"Space": "MNI152NLin6Asym",
“Resolution”: “Matched with original template resolution (2x2x3 mm^3)”, 
 	"License": "See LICENSE file",
  	"Name": "FSL's MNI ICBM 152 non-linear 6th Generation Asymmetric Average 
   Brain Stereotaxic Registration Model",
"RRID": "SCR_002823",
  	"ReferencesAndLinks": [
  "https://doi.org/10.1016/j.neuroimage.2012.01.024",
  "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/Atlases”
     ],
  	"Species": "Human"
}

Next, the content of the tsv files describing the indices and corresponding labels present in the atlas at hand. 

atlas-HarvardOxford_res-2_dseg.tsv

index	label	hemisphere
0	Background	bilateral
1	Frontal Pole	bilateral
2
Insular Cortex	bilateral
3	Superior Frontal Gyrus	bilateral
4	Middle Frontal Gyrus	bilateral
5	Inferior Frontal Gyrus, pars triangularis	bilateral
6	Inferior Frontal Gyrus, pars opercularis	bilateral
…		



 
## Multiple existing atlases in template space
The example below illustrates how multiple existing atlases in the same template space are represented according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford, Schaefer, Yeo and MSDL atlases, all in MN152NLin6Asym space and with a resolution of 2 mm3, were utilized without modifications (e.g. transformations, subsetting, etc.) for all subjects to which the pipeline was applied. Importantly, all atlas-related information is indicated via the value of the atlas- key and not via desc- to help prevent inheritance problems in subsequent steps. Here, this was used to indicate that the Harvard-Oxford atlas in its version with a maximum probability of 50, the Schaefer atlas in its 400 parcel version and the Yeo atlas in its 17 networks version were used. The respective information found in each file follows the example outlined in 4.1 as atlases were used independently from one another.

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



 
## Single existing atlas transformed to subject space
The example below illustrates how a single existing atlas transformed into a subject’s native space space is represented according to the atlas BEP. Specifically, the example refers to the Harvard-Oxford atlas with a resolution of 2 mm3 that was transformed from the MN152NLin6Asym template space to a given subject’s native T1w space. While the original atlas-related files remain as outlined in the use case in template space, the spatially transformed version of the nii.gz atlas file will be placed within a given subjects directory. The precise location within the latter depends on the modality space to which the atlas was transformed to, e.g. anat, func or dwi. The same location furthermore entails a corresponding json file outlining further information on the source atlas and applied transformation(s).


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


The json file accompanying the transformed atlas should include the following information.

sub-01_space-T1w_seg-HarvardOxford_res-2_dseg.json

{
 	"BIDSVersion": "1.1.0",
“SpatialReference”: “sub-01/anat/sub-01_T1w.nii.gz”,
 	"Space": "T1w",
“Resolution”: “Matched with original resolution in subject T1w space 
  (1x1x1 mm^3)”, 
	“Sources”: [],
“transformation”:
}


##  MyConnectome example

The example below illustrates how two atlases, an individual surface-based cortical parcellation in FS_lr space (called Russome), and the subcortical regions from a volumetric segmentation provided by the FreeSurfer aseg, are represented according to the atlas BEP. While the FreeSurfer atlas-related files have two instances, one as outlined in the use case in template space and one as outlined in the use case covering subject spaces, the individual parcellation in FS_lr space will be placed only within a given subjects directory. The same location furthermore entails a corresponding json file outlining further information on the atlas and applied analysis to obtain it.

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


The json file accompanying the functionally derived atlas should include the following information.

sub-01_task-rest_atlas.json: contains top-level metadata about atlas

{
  "Atlas": {
    "Russome": {
“Atlasfile”: “/link/to/russome/file”, 
“Extra”: “individualized surface parcellation”
},
    “FS_aseg”: {
“Atlasfile”: “/link/to/aseg/file”, 
“Extra”: “freesurfer aseg”
}
}

## Atlas utilization in electrophysiology data

Some atlases in development include the Open MNI iEEG Atlas (https://mni-open-ieegatlas.research.mcgill.ca/) led by Birgit Frauscher and Jean Gotman of at McGill University with technical implementation led by Alan Evans’ group led by Christine Rogers [citation].  106 subjects’s signal data from 17__ channels in non-epileptogenic areas of (“normal”) tissue was mapped to a MICCAI 2012 standardized atlas template [citation]. 
-> what would an atlas directory look like given the data is coming from multi-subjects? (example 4.7 quantitative atlas example) 
-> Is BIDS coverage currently sufficient to describe this, what more metadata would be helpful, e.g. reference space.  (spatial reference is defined in 4.4 json sidecar)
-> what they can be used for.  Looks like eeg but x y z can’t be run without abc 


Additional intracranial EEG atlas development is in progress across 10 sites in 6 countries.   
Co-registration on MRI templates is performed with …. 

Example might look something like this, just to verify that the above could be extended with a timeseries file in which the ‘channels’ correspond to the _dseg.tsv, and the json file might need an indicator that there is a time series file. This example is only here to decide whether this is out of scope, can be removed.
bids/atlases/atlas-FreeSurferASEG/
	atlas-FreeSurferASEG_dseg.json
	atlas-FreeSurferASEG_dseg.tsv
	atlas-FreeSurferASEG_dseg.nii.gz
atlas-FreeSurferASEG_dseg.edf
 
## Quantitative atlas examples 

The example below is for PET imaging, but this applies to any quantitative mapping (PET or QMRI). Compared to anatomical atlases, quantitative atlases give reference values to be compared with. Such values can be derived voxel/vertex wise or per region of interest (ROI), in the later case deriving ROIs generally from an anatomical atlas. 

We created a Molecular Imaging Brain Atlases (MIBA) from 16 subjects who underwent a [11C]PS13 PET scan, a radioligand that quantifies cyclooxygenase-1 (source data: https://openneuro.org/datasets/ds004332/versions/1.0.2). Our atlas consists of mean and standard deviations of PS13 target distribution volumes (VT) computed across the 16 subjects at each voxel, in standard MRI spaces. We also project these distribution volumes onto the freesurfer cortical surfaces and include these as well.  The goal is to allow researchers with MRI-only data to correlate their results to the distribution volume of PS13. The dataset can be found at https://openneuro.org/datasets/ds004401/versions/1.1.0 (to be changed following this spec). 

Case 1: voxel/vertex wise analysis

Missing is the measure -- what was computed, BPND?

bids/atlases/atlas-ps13/
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


 
Case 2: regional analysis (voxels/vertices are averaged per regions from dseg/probseg)

bids/atlases/
atlas-mni305/
atlas-aparc.DKTatlas+aseg.mgz
atlas-aparc.DKTatlas+aseg.tsv
atlas-RB_all_2008-03-26.probseg.gca
atlas-RB_all_2008-03-26.probseg.tsv
atlas-ps13/
	  atlas-ps13_space-fsaverage_hemi-L_stat-mean_meas-VT_mimap.json
        atlas-ps13_space-fsaverage-hemi-L_stat-mean_meas-VT_mimap.tsv
        atlas-ps13_space-fsaverage-hemi-L_stat-std_meas-VT_mimap.json
       atlas-ps13_space-fsaverage-hemi-L_stat-std_meas-VT_mimap.tsv
       atlas-ps13_space-fsaverage-hemi-R_stat-mean_meas-VT_mimap.json
       atlas-ps13_space-fsaverage-hemi-R_stat-mean_meas-VT_mimap.tsv
  atlas-ps13_space-fsaverage-hemi-R_stat-std_meas-VT_mimap.json
  atlas-ps13_space-fsaverage-hemi-R_stat-std_meas-VT_mimap.tsv
  atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_mimap.json
  atlas-ps13_space-MNI305Lin_res-2_stat-mean_meas-VT_mimap.tsv
  atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_mimap.json
  atlas-ps13_space-MNI305Lin_res-2_stat-std_meas-VT_mimap.tsv

(note that there is no image -- we should provide instruction how to load such tsv in freesurfer for surface viewing (and save as?) in a readme and also do the same as matlab/python code for generating volumes from the tsv at the desired resolution)


The json file accompanying the quantitative atlas should include the information as in 4.1.