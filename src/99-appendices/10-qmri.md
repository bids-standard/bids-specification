### qMRI method-specific priority levels for grouping suffix

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

### qMRI applications that can be derived from an existing `grouping suffix`

Certain grouping suffixes may refer to a generic data collection regime such as
variable flip angle (VFA), rather than a more specific acquisition, e.g.,
magnetization prepared two gradient echoes (MP2RAGE). Such generic acquisitions
can serve as a basis to derive various qMRI applications by changes to
the acquisition sequence (e.g. readout) type or varying additional scan parameters.

If such inheritance relationship is applicable between an already existing
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

### Metadata of qMRI maps

Metadata fields listed in the sidecar JSON of a qMRI map depend on the method by
which it is obtained:
* If a qMRI map is generated at the scanner site through non-transparent vendor
implementation, JSON content is confined to the available metadata.
* If a qMRI map is generated using an open-source software, its sidecar JSON
file MUST inherit content from the JSON files of the constituent images of a
`grouped scan collection` by adhering to the following rules:
     * All the acquisition parameters that are unchanged across constituents of
     a `grouped scan collection` are added to the JSON file of the resultant
     qMRI map.
     * Relevant acquisition parameters that vary across constituents of a
     `grouped scan collection` are added to the JSON file of the resultant
     qMRI map **in array form**. To find out which varying scan parameters are
     relevant to a given `grouped scan collection`, please see the
    [method-specific priority levels for qMRI metadata](#prioritylevels) above.
     * The JSON file accompanying a qMRI map which is obtained by
     using an open-source software MUST include all the metadata fields listed
     in the following table for the sake of provenance.

| Field name                  | Definition                                                     |
| :-------------------------- | :------------------------------------------------------------- |
| BasedOn | List of files grouped by an `grouping suffix` to generate the map. The fieldmaps are also listed, if involved in the processing. |
| EstimationReference | Reference to the study/studies on which the implementation is based.|
| EstimationAlgorithm | Type of algoritm used to perform fitting (e.g. linear, non-linear, LM etc.)|
| EstimationSoftwareName | The name of the open-source tool used for fitting (e.g. qMRLab, QUIT, hMRI-Toolbox etc.)|
| EstimationSoftwareVer | Version of the open-source tool used for fitting (e.g. v2.3.0 etc.)|
| EstimationSoftwareLang | Language in which the software is natively developed (e.g. MATLAB R2018b, C++17, Python 3.6 etc.)|
| EstimationSoftwareEnv | Operation system on which the application was run (e.g. OSX 10.14.3, Ubuntu 18.04, Win10 etc.)|

Example:

```Text
sub-01_T1map.nii.gz
sub-01_T1map.json
```

```Text
sub-01_T1map.json
{

<<Parameter injected by the software for provenance recording>>

"BasedOn":["anat/sub-01_fa-1_VFA.nii.gz",
           "anat/sub-01_fa-2_VFA.nii.gz",
           "anat/sub-01_fa-3_VFA.nii.gz",
           "anat/sub-01_fa-4_VFA.nii.gz",
           "fmap/sub-01_B1plusmap.nii.gz"],

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
```\