# Method-specific priority levels for grouping suffix

Although there is not an upper limit to the amount of metadata
for images collected by a `grouping suffix`, some of the metadata entries become
REQUIRED when considered within the context of a specific qMRI
application.

<a name="prioritylevels">Table of method-specific priority levels for qMRI metadata</a>

| Grouping suffix | REQUIRED metadata                                                                                    | OPTIONAL metadata          |
|-----------------|------------------------------------------------------------------------------------------------------|----------------------------|
| VFA             | `FlipAngle`, `PulseSequenceType`, `RepetitionTimeExcitation`                                         | `SpoilingRFPhaseIncrement` |
| IRT1            | `InversionTime`                                                                                      |                           |
| MP2RAGE         | `FlipAngle`, `InversionTime`, `RepetitionTimeExcitation`, `RepetitionTimePreperation`, `NumberShots` | `EchoTime`                 |
| MESE            | `EchoTime`                                                                                           |                           |
| MEGRE           | `EchoTime`                                                                                           |                           |
| MTR             | `MTState`                                                                                            |                           |
| MTS             | `FlipAngle`, `MTState`, `RepetitionTimeExcitation`                                                   |                           |
| MPM             | `FlipAngle`, `MTState`, `RepetitionTimeExcitation`                                                   | `EchoTime`                 |
| B1DAM           | `FlipAngle`                                                                                          |                          |

Explanation of the table:

* The metadata fields listed in the REQUIRED column are needed to perform a
minimum viable qMRI application for the corresponding `grouping suffix`.
* Note that some of the metadata fields may be unaltered across different members
of a given `grouped scan collection`, yet still needed as an input to a qMRI
model for parameter fitting (e.g. `RepetitionTimeExcitation` of `VFA`). 
* The metadata fields listed in the OPTIONAL column can be used to derive
various qMRI applications from an existing `grouping suffix`. The following section expands on the set of rules to derive qMRI applications from an existing `grouping suffix`.

# qMRI applications that can be derived from an existing `grouping suffix`

Certain grouping suffixes may refer to a generic data collection regime such as
variable flip angle (VFA), rather than a more specific acquisition, e.g.,
magnetization prepared two gradient echoes (MP2RAGE). Such generic acquisitions
can serve as a basis to derive various qMRI applications by changes to
the acquisition sequence (e.g. readout) type or varying additional scan parameters.

If such an inheritance relationship is applicable between an already existing
`grouping suffix` and a new qMRI application to be included in the specification,
the inheritor qMRI method MUST be listed in the table below instead of
introducing a new `grouping suffix`. This approach:

* prevents the list of available suffixes from over-proliferation
* provides qMRI-focused BIDS applications with a set of meta-data driven rules
to infer possible fitting options
* keep an inheritance track of the qMRI methods described within the
specification.

<a name="varianttable">Table of qMRI applications that can be derived from an existing grouping suffix</a>

| Grouping suffix | If REQUIRED metadata == Value | OPTIONAL metadata [`var`/`fix`]<sup>[*](#footnotederive)</sup>      | Derived application |
|-----------------|-------------------------------|----------------------------------|---------------------|
| VFA             | `PulseSequenceType` == `SPGR` |                                  | DESPOT1             |
| VFA             | `PulseSequenceType` == `SSFP` | `SpoilingRFPhaseIncrement` [`fix`] | DESPOT2             |
| VFA             | `PulseSequenceType` == `SSFP` | `SpoilingRFPhaseIncrement` [`var`] | DESPOT2-FM          |
| MP2RAGE         |                               | `EchoTime` [`var`]                 | MP2RAGE-ME          |
| MPM             |                               | `EchoTime` [`var`]                 | MPM-ME              |

<a name="footnotederive">*</a> `var` denotes that the listed OPTIONAL metadata value changes across
 constituent images of the respective `grouping suffix`, fixed otherwise (`fix`). 
 If the OPTIONAL metadata type is `var`, respective naming entities can be found in the 
 OPTIONAL entities column of [`grouping suffix` table](#grouping-suffix). 
*** 

A derived qMRI application becomes avaiable if all the OPTIONAL metadata fields
listed for a `grouping suffix` is provided in the data. In addition, conditional
rules based on the value of a given REQUIRED metada field can be set
for the description of a derived qMRI application. Note that the value of this
REQUIRED metadata is fixed across constituent images of a `grouping suffix`. 

For example, if the REQUIRED metadata field of `PulseSequenceType` is SPGR
for a collection of anatomical images listed by the `VFA` suffix, the data
qualifies for `DESPOT1` T1 fitting. For the same suffix, if the `PulseSequenceType`
metadata field has the value of `SSFP`, and the `SpoilingRFPhaseIncrement` is 
provided as a metadata field, then the dataset becomes eligible for `DESPOT2`
T2 fitting application. Finally, if the `DESPOT2` data has more than one
`SpoilingRFPhaseIncrement` field as a metadata field, then the dataset is valid
for `DESPOT2-FM`. In this case, `rfphase` entity can be used to distinguish inputs. 

Please note that OPTIONAL metadata fields listed in the [qMRI applications that can be derived from an existing suffix table](#varianttable) MUST be also included in the [method sprecific priority levels for qMRI metadata table](#prioritylevels)  for the sake of completeness.

Please also note that the rules concerning the presence/value of certain metadata
fields within the context of `grouping suffix` is not a part of the BIDS
validation process. Such rules rather constitute a centralized guideline for
creating interoperable qMRI datasets.

For a dataset with a `grouping suffix`, the BIDS validation is successful if:

* provided NIfTI and JSON file names respect the anatomy imaging dataset template
* provided suffixes are present in the list of available suffixes
* sidecar JSON files follow the hierarchy defined for `grouping suffix`.

# Introducing a new qMRI grouping suffix

In the future, novel qMRI applications will be introduced that are not yet
described by the BIDS. If such applications can not be interpreted as a 
subset of a pre-existing `grouping suffix`,
a new grouping suffix can be introduced, but should adhere to the following
principles:

* All grouping suffixes MUST be capitalized.
* Grouping suffixes MUST attain a clear description of the qMRI application
that they relate to. Hyperlinks to example applications and/or more detailed
descriptions are encouraged whenever possible.
* Unless the pulse sequence is exclusively associated with a specific qMRI
application (e.g. `MP2RAGE`), sequence names are NOT used as grouping suffixes.
* If it is possible to derive a qMRI application from an already existing
grouping suffix by defining a set of logical conditions over the metadata
fields, the [table of method-specific priority levels](#prioritylevels) and the
[table of qMRI applications that can be derived from an existing grouping suffix](#varianttable)
 MUST be expanded instead of introducing a new grouping suffix.
 Please visit the [JSON content for grouping suffixes](#whichmetadata) 
 for further details.
* Please note that if a structural data has the type of grouped scan collection,
the use of `_suffix` alone cannot distinguish its members from each other,
failing to identify their roles as inputs to the calculation of qMRI maps.
Although such images are REQUIRED to be grouped by a proper grouping suffix,
they are also RECOMMENDED to include at least one of the `acq`, `part`, `echo`,
`met`, `inv`-key/value-pairs (please visit corresponding sections for details).


# Management of the qMRI maps

All qMRI maps are generated following a set of calculations. Unlike conventional 
MR images, they are not products of an MRI image reconstruction (from k-space data 
to structural images). There are two possible options in the way a qMRI map is obtained: 

1. Pre-generated qMRI maps: The qMRI maps are generated immediately after the 
reconstruction of the multi-contrast input images and made available to the user
at the scanner console. The acquisition scenarios may include (a) vendor pipelines 
or (b) open-source pipelines deployed on the scanner site.
2. Post-generated qMRI maps: The qMRI maps are generated from the multi-contrast
input images after they are exported outside the scanner site.

## Where to place qMRI maps? 

**If the provenance record of the qMRI map generation is NOT accessible:**

Although qMRI maps are derivatives by definition, we cannot relate them to their 
multi-contrast input images in this case. Therefore, qMRI maps lacking provenance
are directly placed at the `/sub-#/anat` directory.

**If the provenance record of the qMRI map generation is available:**

In this case, qMRI maps SHOULD be stored in the `derivatives` folder, but MAY
be symbolic linked to the corresponding raw data directory to facilitate the
easy use of these images as inputs to the processing workflows implemented as
BIDS-apps. For example:

```diff
 ds-example/
 ├── derivatives/
 |   └── qMRI-software/
 |       └── sub-01/
 |           └── anat/
 |               ├── sub-01_T1map.nii.gz ─────────┐ S
 |               ├── sub-01_T1map.json   ───────┐ | Y
 |               ├── sub-01_MTsat.nii.gz ─────┐ | | M
 |               └── sub-01_MTsat.json   ───┐ | | | L 
 └── sub-01/                                | | | | I
     └── anat/                              | | | | N
         ├── sub-01_T1w.nii.gz              | | | | K
         ├── sub-01_T1w.json                | | | | 
         ├── sub-01_fa-1_mt-on_MTS.nii.gz   | | | | T
         ├── sub-01_fa-1_mt-on_MTS.json     | | | | O 
         ├── sub-01_fa-1_mt-off_MTS.nii.gz  | | | | 
         ├── sub-01_fa-1_mt-off_MTS.json    | | | | A
         ├── sub-01_fa-2_mt-off_MTS.nii.gz  | | | | N
         ├── sub-01_fa-2_mt-off_MTS.json    | | | | A
         ├── sub-01_T1map.nii.gz ◀──────────├─├─├─┘ T
         ├── sub-01_T1map.json   ◀──────────├─├─┘   
         ├── sub-01_MTsat.nii.gz ◀──────────├─┘
         └── sub-01_MTsat.json   ◀──────────┘ 
```

In the example above, outputs of the `MTS` that are placed under the `derivatives`
folder are symbolic linked to the respective `anat` folder. This way, an
application can easily pick up a qMRI map along with other anatomical images.

## <a name="whichmetadata">Which metadata fields should a qMRI map contain?</a>

**If the provenance record of the qMRI map generation is NOT accessible:**

JSON content is confined to the metadata made available for the pre-generated
qMRI map.

**If the provenance record of the qMRI map generation is available:**

JSON file of the qMRI map MUST inherit metadata from its parent images (typically a grouped scan 
collection) by adhering to the following rules:
* All the acquisition parameters that are unchanged across constituents of
a `grouped scan collection` are added to the JSON file of the resultant
qMRI map.
* Relevant acquisition parameters that vary across constituents of a
`grouped scan collection` are added to the JSON file of the resultant
qMRI map **`in array form`**. 
 > To find out which varying scan parameters are
 relevant to a given `grouped scan collection`, please see the
[method-specific priority levels for qMRI metadata](#prioritylevels) above.
* The JSON file accompanying a qMRI map which is obtained by
using open-source software MUST include all the metadata fields listed
in the following table for the sake of provenance.

| Field name                  | Definition                                                     |
| :-------------------------- | :------------------------------------------------------------- |
| BasedOn | List of files grouped by an `grouping suffix` to generate the map. The fieldmaps are also listed, if involved in the processing. |
| EstimationReference | Reference to the study/studies on which the implementation is based.|
| EstimationAlgorithm | Type of algoritm used to perform fitting (e.g. linear, non-linear, LM etc.)|
| EstimationSoftwareName | The name of the open-source tool used for fitting (e.g. [qMRLab](https://qmrlab.org), [QUIT](https://github.com/spinicist/QUIT), [hMRI-Toolbox](https://hmri-group.github.io/hMRI-toolbox/) etc.)|
| EstimationSoftwareVer | Version of the open-source tool used for fitting (e.g. v2.3.0 etc.)|
| EstimationSoftwareLang | Language in which the software is natively developed (e.g. MATLAB R2018b, C++17, Python 3.6 etc.)|
| EstimationSoftwareEnv | Operation system on which the application was run (e.g. OSX 10.14.3, Ubuntu 18.04, Win10 etc.)|

Example:

```Text
sub-01_T1map.nii.gz
sub-01_T1map.json
```

```
sub-01_T1map.json
{

<<Parameter injected by the software for provenance recording>>

"BasedOn":["anat/sub-01_fa-1_VFA.nii.gz",
           "anat/sub-01_fa-2_VFA.nii.gz",
           "anat/sub-01_fa-3_VFA.nii.gz",
           "anat/sub-01_fa-4_VFA.nii.gz",
           "fmap/sub-01_TB1map.nii.gz"],

<<Parameters that are constant across members of VFA grouping suffix>>

“MagneticFieldStrength”: “3”,
“Manufacturer”: “Siemens”,
“ManufacturerModelName”: “TrioTim”,
“InstitutionName”: “xxx”,
“PulseSequenceType”: “SPGR”,
“PulseSequenceDetails”: “Information beyond the sequence type that identifies
 specific pulse sequence used (VB version, if not standard, Siemens WIP XXX
 ersion ### sequence written by xx using a version compiled on mm/dd/yyyy/)”,
"RepetitionTimeExcitation": "35",
"EchoTime": "2.86",
"SliceThickness": "5",

<<Relevant parameters that vary across members of VFA grouping suffix>>

"FlipAngle": ["5","10","15","20"],

<<Additional parameters injected by the software for provenance recording>>

"EstimationPaper":"Deoni et. al.MRM, 2015",
"EstimationAlgorithm":"Linear",
“EstimationSoftwareName”: “qMRLab”,
“EstimationSoftwareLanguage”: “Octave”,
“EstimationSoftwareVersion”: “2.3.0”,
“EstimationSoftwareEnv”: “Ubuntu 16.04”
}
```

# Radiofrequency (RF) field mapping 

Most qMRI methods are susceptible to the nonuniformities in the transmit (B1<sup>+</sup>) and/or receive (B1<sup>-</sup>) radiofrequency (RF) fields. Various (acquisition based)
methods are available to derive maps of spatial variations in the B1<sup>+</sup> and B1<sup>-</sup> 
fields. These maps are commonly used for the correction of qMRI estimation errors 
arising from the imperfections in the respective RF field.

An approach similar to that used in anatomical MR images to group a set of input images intended
for qMRI application (`grouping suffix`) is applied for the inputs of B1<sup>+</sup> and B1<sup>-</sup> RF field mapping. Note that these images do not convey substantial
structural information by design. Therefore, both inputs and outputs of RF field
maps are stored in the `fmap` folder.

## Grouping suffixes for RF field mapping 

| Name                                       | Suffix  | Type     | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
|--------------------------------------------|---------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Double-angle B1<sup>+</sup> mapping                    | TB1DAM   | RF Grouping | Groups images for B1<sup>+</sup> field mapping ([Insko and Bolinger 1993](https://www.sciencedirect.com/science/article/abs/pii/S1064185883711332)). Double angle method is based on the calculation of the actual angles from signal ratios, collected by two acquisitions at different nominal excitation flip angles. Common sequence types for this application include spin echo and echo planar imaging. _Associated output suffixes_: `TB1map`                                                                                                                                                      |
| B1<sup>+</sup> mapping with 3D EPI            | TB1EPI   | RF Grouping | Groups images for B1<sup>+</sup> field mapping ([Jiru and Klose 2006](https://dx.doi.org/10.1002/mrm.21083)). This method is based on two EPI readouts to acquire spin echo (SE) and stimulated echo (STE) images at multiple flip angles in one sequence, used in the calculation of deviations from the nominal flip angle. _Associated output suffixes_: `TB1map`                                                                                                                                                      |
| Actual Flip Ange Imaging (AFI)             | TB1AFI   | RF Grouping | Groups images for B1<sup>+</sup> field mapping ([Yarnykh 2007](https://dx.doi.org/10.1002/mrm.21120)). This method calculates a B1<sup>+</sup> map from two images acquired at interleaved (two) TRs with identical RF pulses using a steady-state sequence. _Associated output suffixes_: `TB1map`                                                                                                                                                      |
| Siemens `tfl_b1_map`             | TB1TFL   | RF Grouping | Groups images acquired using `tfl_b1_map` product sequence by Siemens based on the method by [Chung et al. (2010)](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.22423). The sequence generates one ~anatomical image and one scaled flip angle map._Associated output suffixes_: `TB1map`                                                                                                                                                      |
| Siemens `rf_map`             | TB1RFM   | RF Grouping | Groups images acquired using `rf_map` product sequence by Siemens, using a method combining SE and STE images with EPI readout similar to that by ([Jiru and Klose 2006](https://dx.doi.org/10.1002/mrm.21083)). The sequence generates one ~anatomical image and one scaled flip angle map. _Associated output suffixes_: `TB1map`                                                                                                                                                      |
|Saturation‐prepared with 2 rapid Gradient Echoes (SA2RAGE) B1<sup>+</sup> mapping | TB1SRGE | RF Grouping |Groups images for  B1+ field mapping ([Eggenschwiler et al. 2011](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.23145)). SA2RAGE uses a ratio of two saturation recovery images with different time delays, and a simulated look-up table to estimate B1+. This sequence can also be used in conjunction with MP2RAGE T1 mapping to iteratively improve B1+ and T1 map estimation ([Marques & Gruetter 2013](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0069294)). Associated output suffixes: TB1map                                                                                                                                                     |
| B1<sup>-</sup> field correction          | RB1COR   | RF Grouping | Groups low resolution images acquired by the body coil (in the gantry of the scanner) and the head coil using identical acquisition parameters to generate a combined sensitivity map as described in [Papp et al. (2016)](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.26058). _Associated output suffixes_: `RB1map`                                                                                                                                                      |


## Entity specifications for RF field mapping grouping suffixes

### `TB1DAM` 

The `fa` entity MUST be used to distinguish images with this suffix: 

```
└── sub-01/
     └── fmap/
         ├── sub-01_fa-1_TB1DAM.nii.gz
         ├── sub-01_fa-1_TB1DAM.json
         ├── sub-01_fa-2_TB1DAM.nii.gz
         └── sub-01_fa-2_TB1DAM.json
```

### `TB1EPI`

The `fa` and `echo` entities MUST be used to distinguish images with this suffix.
The use of `fa` follows the default convention. However, this suffix defines a
specific use case for the `echo` entity:

|`echo-1`|`echo-2`|
|:--|:----|
|Lower `EchoTime` | Higher `EchoTime`                  |
|Spin Echo (SE) image|Stimulated Echo (STE) image|

At each `FlipAngle`, the `TB1EPI` suffix lists two images acquired at two echo times.
The first echo is a spin echo (SE) formed by the pulses alpha-2alpha. However, the 
second echo in this method is generated in a different fashion compared to a typical
MESE acquisition. The second echo is a stimulated echo (STE) that is formed by an 
additional alpha pulse (i.e., alpha-2alpha-alpha).

The `FlipAngle` value corresponds to the nominal flip angle value of the STE pulse. 
The nominal FA value of the SE pulse is twice this value.

Note that the following metadata fields MUST be defined in the accompanying JSON 
files:

| Field name         | Definition |
| :----------------- | :--------- |
| `TotalReadoutTime` |   The effective readout length defined as `EffectiveEchoSpacing * PEReconMatrix`, with `EffectiveEchoSpacing = TrueEchoSpacing / PEacceleration`         |
| `MixingTime`       |  Time interval between the SE and STE pulses          |

To properly identify constituents of this particular method, values of the `echo`
entity MUST index the images as follows:  

```
└── sub-01/
     └── fmap/
         ├── sub-01_fa-1_echo-1_TB1EPI.nii.gz (SE)
         ├── sub-01_fa-1_echo-1_TB1EPI.json
         ├── sub-01_fa-1_echo-2_TB1EPI.nii.gz (STE)
         ├── sub-01_fa-1_echo-2_TB1EPI.json
         ├── sub-01_fa-2_echo-1_TB1EPI.nii.gz (SE)
         ├── sub-01_fa-2_echo-1_TB1EPI.json
         ├── sub-01_fa-2_echo-2_TB1EPI.nii.gz (STE)
         └── sub-01_fa-2_echo-2_TB1EPI.json
```

### `TB1AFI`

This method calculates a B1<sup>+</sup> map from two images acquired at two
interleaved excitation repetition times (TR). Note that there is not an entity 
for the TR and its definition depends on the modality (`functional` or `anatomical`)
in the specification. 

Therefore, to properly identify constituents of this particular method, values of 
the `acq` entity SHOULD begin with either `tr1` (lower TR) or `tr2` (higher TR) 
and MAY be followed by freeform entries:  

|First `TR`|Second `TR`|Use case|
|:--|:----| :----| 
|`_acq-tr1`|`_acq-tr2`|Single acquisition|
|`_acq-tr1Test`|`_acq-tr2Test`|Acquisition `Test`|
|`_acq-tr1Retest`|`_acq-tr2Retest`|Acquisition `Retest`|

```
└── sub-01/
     └── fmap/
         ├── sub-01_acq-tr1_TB1AFI.nii.gz
         ├── sub-01_acq-tr1_TB1AFI.json
         ├── sub-01_acq-tr2_TB1AFI.nii.gz
         └── sub-01_acq-tr2_TB1AFI.json
```

### `TB1TFL` and `TB1RMF`

These suffixes describe two outputs generated by Siemens `tfl_b1_map` and `rf_map`
product sequences, respectively. Both sequences output two images. The first image
appears like an anatomical images and the second output is a scaled flip angle map.

To properly identify constituents of this particular method, values of 
the `acq` entity SHOULD begin with either `anat` or `famp` and MAY be followed 
by freeform entries:

|Anatomical (like) image|Scaled FA map|Use case|
|:--|:----| :----| 
|`_acq-anat`|`_acq-famp`|Single acquisition|
|`_acq-anatTest`|`_acq-fampTest`|Acquisition `Test`|
|`_acq-anatRetest`|`_acq-fampRetest`|Acquisition `Retest`|

```
└── sub-01/
     └── fmap/
         ├── sub-01_acq-anat_TB1TFL.nii.gz 
         ├── sub-01_acq-anat_TB1TFL.json
         ├── sub-01_acq-famp_TB1TFL.nii.gz
         └── sub-01_acq-famp_TB1TFL.json
```

The example above applies to the `TB1RFM` suffix as well. 

### `RB1COR`

This method generates a sensitivity map by combining two low resolution images
collected by two transmit coils (the body and the head coil) upon subsequent scans
with identical acquisition parameters.

To properly identify constituents of this particular method, values of the `acq`
entity SHOULD begin with either `body` or `head` and MAY be followed by freeform
entries:  

|Body coil|Head coil|Use case|
|:--|:----| :----| 
|`_acq-body`|`_acq-head`|Single acquisition|
|`_acq-bodyMTw`|`_acq-headMTw`|`MTw` for `MPM`|
|`_acq-bodyPDw`|`_acq-headPDw`|`PDw` for `MPM`|
|`_acq-bodyT1w`|`_acq-headT1w`|`T1w` for `MPM`|

```
└── sub-01/
     └── fmap/
         ├── sub-01_acq-body_RB1COR.nii.gz (Body coil)
         ├── sub-01_acq-body_RB1COR.json
         ├── sub-01_acq-head_RB1COR.nii.gz (Head coil)
         └── sub-01_acq-head_RB1COR.json
```

## Where to place RF field maps? 

**If the provenance record of the RF field map generation is NOT accessible:**

RF field maps lacking provenance are directly placed at the `/sub-#/fmap` directory.

**If the provenance record of the RF rield map generation is available:**

RF field maps SHOULD be stored in the `derivatives` folder, but MAY
be symbolic linked to the corresponding raw data directory to facilitate the
easy use of these images as input to processing workflows implemented as
BIDS-apps. For example:

```diff
 ds-example/
 ├── derivatives/
 |   └── qMRI-software/
 |       └── sub-01/
 |           └── fmap/
 |               ├── sub-01_acq-PDw_RB1map.nii.gz        ─────────┐ 
 |               ├── sub-01_acq-PDw_RB1map.json          ───────┐ | 
 |               ├── sub-01_TB1map.nii.gz                ─────┐ | | 
 |               └── sub-01_TB1map.json                  ───┐ | | | 
 └── sub-01/                                                | | | | S
     └── fmap/                                              | | | | Y
         ├── sub-01_acq-bodyPDw_RB1COR.nii.gz               | | | | M
         ├── sub-01_acq-bodyPDw_RB1COR.json                 | | | | L
         ├── sub-01_acq-headPDw_RB1COR.nii.gz               | | | | I
         ├── sub-01_acq-headPDw_RB1COR.json                 | | | | N
         ├── sub-01_fa-1_TB1DAM.nii.gz                      | | | | K
         ├── sub-01_fa-1_TB1DAM.json                        | | | | 
         ├── sub-01_fa-2_TB1DAM.nii.gz                      | | | | T
         ├── sub-01_fa-2_TB1DAM.json                        | | | | O
         ├── sub-01_acq-PDw_RB1map.nii.gz      ◀────────────├─├─├─┘
         ├── sub-01_acq-PDw_RB1map.json        ◀────────────├─├─┘
         ├── sub-01_TB1map.nii.gz              ◀────────────├─┘
         └── sub-01_TB1map.json                ◀────────────┘

```
