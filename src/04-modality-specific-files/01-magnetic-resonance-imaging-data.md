# Magnetic Resonance Imaging

## Common metadata fields

MR Data described in the following sections share the following RECOMMENDED metadata
fields (stored in sidecar JSON files). MRI acquisition parameters are divided
into several categories based on
["A checklist for fMRI acquisition methods reporting in the literature"](https://thewinnower.com/papers/977-a-checklist-for-fmri-acquisition-methods-reporting-in-the-literature)
by Ben Inglis:

### Scanner Hardware

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                           |
|-------------------------------|-----------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Manufacturer                  | RECOMMENDED           | [string][]    | Manufacturer of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0070 `Manufacturer`                                                                                                                                                   |
| ManufacturersModelName        | RECOMMENDED           | [string][]    | Manufacturer's model name of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1090 `Manufacturers Model Name`                                                                                                                          |
| DeviceSerialNumber            | RECOMMENDED           | [string][]    | The serial number of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1000 `DeviceSerialNumber`. A pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset |
| StationName                   | RECOMMENDED           | [string][]    | Institution defined name of the machine that produced the composite instances. Corresponds to DICOM Tag 0008, 1010 `Station Name`                                                                                                                                         |
| SoftwareVersions              | RECOMMENDED           | [string][]    | Manufacturer's designation of software version of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1020 `Software Versions`                                                                                                            |
| HardcopyDeviceSoftwareVersion | [DEPRECATED][]        | [string][]    | Manufacturer's designation of the software of the device that created this Hardcopy Image (the printer). Corresponds to DICOM Tag 0018, 101A `Hardcopy Device Software Version`                                                                                           |
| MagneticFieldStrength         | RECOMMENDED           | [number][]    | Nominal field strength of MR magnet in Tesla. Corresponds to DICOM Tag 0018,0087 `Magnetic Field Strength`                                                                                                                                                                |
| ReceiveCoilName               | RECOMMENDED           | [string][]    | Information describing the receiver coil. Corresponds to DICOM Tag 0018, 1250 `Receive Coil Name`, although not all vendors populate that DICOM Tag, in which case this field can be derived from an appropriate private DICOM field                                      |
| ReceiveCoilActiveElements     | RECOMMENDED           | [string][]    | Information describing the active/selected elements of the receiver coil. This doesn't correspond to a tag in the DICOM ontology. The vendor-defined terminology for active coil elements can go in this field. See an example below the table.                           |
| GradientSetType               | RECOMMENDED           | [string][]    | It should be possible to infer the gradient coil from the scanner model. If not, for example because of a custom upgrade or use of a gradient insert set, then the specifications of the actual gradient coil should be reported independently                            |
| MRTransmitCoilSequence        | RECOMMENDED           | [string][]    | This is a relevant field if a non-standard transmit coil is used. Corresponds to DICOM Tag 0018, 9049 `MR Transmit Coil Sequence`                                                                                                                                         |
| MatrixCoilMode                | RECOMMENDED           | [string][]    | (If used) A method for reducing the number of independent channels by combining in analog the signals from multiple coil elements. There are typically different default modes when using un-accelerated or accelerated (for example, GRAPPA, SENSE) imaging              |
| CoilCombinationMethod         | RECOMMENDED           | [string][]    | Almost all fMRI studies using phased-array coils use root-sum-of-squares (rSOS) combination, but other methods exist. The image reconstruction is changed by the coil combination method (as for the matrix coil mode above), so anything non-standard should be reported |

Example for `ReceiveCoilActiveElements`:

For Siemens, coil channels are typically not activated/selected individually,
but rather in pre-defined selectable "groups" of individual channels,
and the list of the "groups" of elements that are active/selected in any
given scan populates the `Coil String` entry in Siemens' private DICOM fields
(for example, `HEA;HEP` for the Siemens standard 32 ch coil
when both the anterior and posterior groups are activated).
This is a flexible field that can be used as most appropriate for a given
vendor and coil to define the "active" coil elements.
Since individual scans can sometimes not have the intended coil elements selected,
it is preferable for this field to be populated directly from the DICOM
for each individual scan, so that it can be used as a mechanism for checking
that a given scan was collected with the intended coil elements selected

### Sequence Specifics

| **Key name**                | **Requirement level** | **Data type**                          | **Description**                                                                                                                                                                                                                                                           |
|-----------------------------|-----------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PulseSequenceType           | RECOMMENDED           | [string][]                             | A general description of the pulse sequence used for the scan (for example, MPRAGE, Gradient Echo EPI, Spin Echo EPI, Multiband gradient echo EPI).                                                                                                                       |
| ScanningSequence            | RECOMMENDED           | [string][] or [array][] of [strings][] | Description of the type of data acquired. Corresponds to DICOM Tag 0018, 0020 `Scanning Sequence`.                                                                                                                                                                        |
| SequenceVariant             | RECOMMENDED           | [string][] or [array][] of [strings][] | Variant of the ScanningSequence. Corresponds to DICOM Tag 0018, 0021 `Sequence Variant`.                                                                                                                                                                                  |
| ScanOptions                 | RECOMMENDED           | [string][] or [array][] of [strings][] | Parameters of ScanningSequence. Corresponds to DICOM Tag 0018, 0022 `Scan Options`.                                                                                                                                                                                       |
| SequenceName                | RECOMMENDED           | [string][]                             | Manufacturer's designation of the sequence name. Corresponds to DICOM Tag 0018, 0024 `Sequence Name`.                                                                                                                                                                     |
| PulseSequenceDetails        | RECOMMENDED           | [string][]                             | Information beyond pulse sequence type that identifies the specific pulse sequence used (for example, "Standard Siemens Sequence distributed with the VB17 software," "Siemens WIP ### version #.##," or "Sequence written by X using a version compiled on MM/DD/YYYY"). |
| NonlinearGradientCorrection | RECOMMENDED           | [boolean][]                            | Boolean stating if the image saved has been corrected for gradient nonlinearities by the scanner sequence.                                                                                                                                                                |

### In-Plane Spatial Encoding
| **Key name**                   | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------------------------------|-----------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NumberShots                    | RECOMMENDED           | [number][]    | The number of RF excitations need to reconstruct a slice or volume. Please mind that this is not the same as Echo Train Length which denotes the number of lines of k-space collected after an excitation.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| ParallelReductionFactorInPlane | RECOMMENDED           | [number][]    | The parallel imaging (e.g, GRAPPA) factor. Use the denominator of the fraction of k-space encoded for each slice. For example, 2 means half of k-space is encoded. Corresponds to DICOM Tag 0018, 9069 `Parallel Reduction Factor In-plane`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ParallelAcquisitionTechnique   | RECOMMENDED           | [string][]    | The type of parallel imaging used (for example GRAPPA, SENSE). Corresponds to DICOM Tag 0018, 9078 `Parallel Acquisition Technique`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| PartialFourier                 | RECOMMENDED           | [number][]    | The fraction of partial Fourier information collected. Corresponds to DICOM Tag 0018, 9081 `Partial Fourier`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| PartialFourierDirection        | RECOMMENDED           | [string][]    | The direction where only partial Fourier information was collected. Corresponds to DICOM Tag 0018, 9036 `Partial Fourier Direction`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| PhaseEncodingDirection         | RECOMMENDED           | [string][]    | Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-`. The letters `i`, `j`, `k` correspond to the first, second and third axis of the data in the NIFTI file. The polarity of the phase encoding is assumed to go from zero index to maximum index unless `-` sign is present (then the order is reversed - starting from the highest index instead of zero). `PhaseEncodingDirection` is defined as the direction along which phase is was modulated which may result in visible distortions. Note that this is not the same as the DICOM term `InPlanePhaseEncodingDirection` which can have `ROW` or `COL` values. This parameter is REQUIRED if corresponding fieldmap data is present or when using multiple runs with different phase encoding directions (which can be later used for field inhomogeneity correction). |
| EffectiveEchoSpacing           | RECOMMENDED           | [number][]    | The "effective" sampling interval, specified in seconds, between lines in the phase-encoding direction, defined based on the size of the reconstructed image in the phase direction. It is frequently, but incorrectly, referred to as "dwell time" (see `DwellTime` parameter below for actual dwell time). It is required for unwarping distortions using field maps. Note that beyond just in-plane acceleration, a variety of other manipulations to the phase encoding need to be accounted for properly, including partial fourier, phase oversampling, phase resolution, phase field-of-view and interpolation.<sup>2</sup> This parameter is REQUIRED if corresponding fieldmap data is present.                                                                                                                  |
| TotalReadoutTime               | RECOMMENDED           | [number][]    | This is actually the "effective" total readout time , defined as the readout duration, specified in seconds, that would have generated data with the given level of distortion. It is NOT the actual, physical duration of the readout train. If `EffectiveEchoSpacing` has been properly computed, it is just `EffectiveEchoSpacing * (ReconMatrixPE - 1)`.<sup>3</sup> . This parameter is REQUIRED if corresponding "field/distortion" maps acquired with opposing phase encoding directions are present (see 8.9.4).                                                                                                                                                                                                                                                                                                  |

<sup>2</sup>Conveniently, for Siemens data, this value is easily obtained as
`1 / (BWPPPE * ReconMatrixPE)`, where BWPPPE is the
"BandwidthPerPixelPhaseEncode" in DICOM tag (0019,1028) and ReconMatrixPE is
the size of the actual reconstructed data in the phase direction (which is NOT
reflected in a single DICOM tag for all possible aforementioned scan
manipulations). See [here](https://lcni.uoregon.edu/kb-articles/kb-0003) and
[here](https://github.com/neurolabusc/dcm_qa/tree/master/In/TotalReadoutTime)

<sup>3</sup>We use the time between the center of the first "effective" echo
and the center of the last "effective" echo, sometimes called the "FSL definition".

### Timing Parameters

| **Key name**           | **Requirement level**                                                                                            | **Data type**            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|------------------------|------------------------------------------------------------------------------------------------------------------|--------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EchoTime               | RECOMMENDED, but REQUIRED if corresponding fieldmap data is present or the data comes from a multi echo sequence | [number][]               | The echo time (TE) for the acquisition, specified in seconds. Corresponds to DICOM Tag 0018, 0081 `Echo Time` (please note that the DICOM term is in milliseconds not seconds).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| InversionTime          | RECOMMENDED                                                                                                      | [number][]               | The inversion time (TI) for the acquisition, specified in seconds. Inversion time is the time after the middle of inverting RF pulse to middle of excitation pulse to detect the amount of longitudinal magnetization. Corresponds to DICOM Tag 0018, 0082 `Inversion Time` (please note that the DICOM term is in milliseconds not seconds).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| SliceTiming            | RECOMMENDED, but REQUIRED for sparse sequences that do not have the `DelayTime` field set                        | [array][] of [numbers][] | The time at which each slice was acquired within each volume (frame) of the acquisition. Slice timing is not slice order -- rather, it is a list of times containing the time (in seconds) of each slice acquisition in relation to the beginning of volume acquisition. The list goes through the slices along the slice axis in the slice encoding dimension (see below). Note that to ensure the proper interpretation of the `SliceTiming` field, it is important to check if the OPTIONAL `SliceEncodingDirection` exists. In particular, if `SliceEncodingDirection` is negative, the entries in `SliceTiming` are defined in reverse order with respect to the slice axis, such that the final entry in the `SliceTiming` list is the time of acquisition of slice 0. Without this parameter slice time correction will not be possible. |
| SliceEncodingDirection | RECOMMENDED                                                                                                      | [string][]               | Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-` (the axis of the NIfTI data along which slices were acquired, and the direction in which `SliceTiming` is defined with respect to). `i`, `j`, `k` identifiers correspond to the first, second and third axis of the data in the NIfTI file. A `-` sign indicates that the contents of `SliceTiming` are defined in reverse order - that is, the first entry corresponds to the slice with the largest index, and the final entry corresponds to slice index zero. When present, the axis defined by `SliceEncodingDirection` needs to be consistent with the ‘slice_dim' field in the NIfTI header. When absent, the entries in `SliceTiming` must be in the order of increasing slice index as defined by the NIfTI header.                                                                   |
| DwellTime              | RECOMMENDED                                                                                                      | [number][]               | Actual dwell time (in seconds) of the receiver per point in the readout direction, including any oversampling. For Siemens, this corresponds to DICOM field (0019,1018) (in ns). This value is necessary for the optional readout distortion correction of anatomicals in the HCP Pipelines. It also usefully provides a handle on the readout bandwidth, which isn't captured in the other metadata tags. Not to be confused with `EffectiveEchoSpacing`, and the frequent mislabeling of echo spacing (which is spacing in the phase encoding direction) as "dwell time" (which is spacing in the readout direction).                                                                                                                                                                                                                         |

### RF & Contrast

| **Key name**                | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                       |
| --------------------------- | --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FlipAngle                   | RECOMMENDED           | [number][]    | Flip angle for the acquisition, specified in degrees. Corresponds to: DICOM Tag 0018, 1314 `Flip Angle`.                                                                                                                                                                                                              |
| NegativeContrast            | OPTIONAL              | [boolean][]   | `true` or `false` value specifying whether increasing voxel intensity (within sample voxels) denotes a decreased value with respect to the contrast suffix. This is commonly the case when Cerebral Blood Volume is estimated via usage of a contrast agent in conjunction with a T2\* weighted acquisition protocol. |

### Slice Acceleration

| **Key name**                | **Requirement level** | **Data type** | **Description**                                   |
| --------------------------- | --------------------- | ------------- | ------------------------------------------------- |
| MultibandAccelerationFactor | RECOMMENDED           | [number][]    | The multiband factor, for multiband acquisitions. |

### Anatomical landmarks

Useful for multimodal co-registration with MEG, (S)EEG, TMS, and so on.

| **Key name**                  | **Requirement level** | **Data type**            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ----------------------------- | --------------------- | ------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnatomicalLandmarkCoordinates | RECOMMENDED           | [object][] of [arrays][] | Key:value pairs of any number of additional anatomical landmarks and their coordinates in voxel units (where first voxel has index 0,0,0) relative to the associated anatomical MRI (for example, `{"AC": [127,119,149], "PC": [128,93,141], "IH": [131,114,206]}`, or `{"NAS": [127,213,139], "LPA": [52,113,96], "RPA": [202,113,91]}`). Each array MUST contain three numeric values corresponding to x, y, and z axis of the coordinate system in that exact order. |

### Institution information

| **Key name**                | **Requirement level** | **Data type** | **Description**                                                                                                                                                          |
| --------------------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| InstitutionName             | RECOMMENDED           | [string][]    | The name of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0080 `InstitutionName`.                     |
| InstitutionAddress          | RECOMMENDED           | [string][]    | The address of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0081 `InstitutionAddress`.               |
| InstitutionalDepartmentName | RECOMMENDED           | [string][]    | The department in the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1040 `Institutional Department Name`. |

When adding additional metadata please use the CamelCase version of
[DICOM ontology terms](https://scicrunch.org/scicrunch/interlex/dashboard)
whenever possible. See also
[recommendations on JSON files](../02-common-principles.md#keyvalue-files-dictionaries).

## Anatomy imaging data

Template:

```Text
sub-<label>/[ses-<label>/]
    anat/
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>]_<modality_label>.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_defacemask.nii[.gz]
```

Anatomical (structural) data acquired for that participant. Currently supported
modalities include:

| **Name**           | `modality_label` | **Description**                                                                                                                                   |
| ------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| T1 weighted        | T1w              |                                                                                                                                                   |
| T2 weighted        | T2w              |                                                                                                                                                   |
| T1 Rho map         | T1rho            | Quantitative T1rho brain imaging <br> <https://www.ncbi.nlm.nih.gov/pubmed/24474423> <br> <https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4346383/> |
| T1 map             | T1map            | quantitative T1 map                                                                                                                               |
| T2 map             | T2map            | quantitative T2 map                                                                                                                               |
| T2\*               | T2star           | High resolution T2\* image                                                                                                                        |
| FLAIR              | FLAIR            |                                                                                                                                                   |
| FLASH              | FLASH            |                                                                                                                                                   |
| Proton density     | PD               |                                                                                                                                                   |
| Proton density map | PDmap            |                                                                                                                                                   |
| Combined PD/T2     | PDT2             |                                                                                                                                                   |
| Inplane T1         | inplaneT1        | T1-weighted anatomical image matched to functional acquisition                                                                                    |
| Inplane T2         | inplaneT2        | T2-weighted anatomical image matched to functional acquisition                                                                                    |
| Angiography        | angio            |                                                                                                                                                   |

If the structural images included in the dataset were defaced (to protect
identity of participants) one MAY provide the binary mask that was used to
remove facial features in the form of `_defacemask` files.
In such cases,  the OPTIONAL [`mod-<label>`](../99-appendices/09-entities.md#mod)
key/value pair corresponds to modality suffix,
such as T1w or inplaneT1, referenced by the defacemask image.
For example, `sub-01_mod-T1w_defacemask.nii.gz`.

If several scans of the same modality are acquired they MUST be indexed with the
[`run-<index>`](../99-appendices/09-entities.md#run) key-value pair:
`_run-1`, `_run-2`, `_run-3`, and so on (only nonnegative integers are allowed as
run labels). When there is only one scan of a given type the run key MAY be
omitted. Please note that diffusion imaging data is stored elsewhere (see
below).

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label the user
MAY use to distinguish a different set of parameters used for acquiring the same
modality. For example this should be used when a study includes two T1w images -
one full brain low resolution and and one restricted field of view but high
resolution. In such case two files could have the following names:
`sub-01_acq-highres_T1w.nii.gz` and `sub-01_acq-lowres_T1w.nii.gz`, however the
user is free to choose any other label than `highres` and `lowres` as long as
they are consistent across subjects and sessions. In case different sequences
are used to record the same modality (for example, RARE and FLASH for T1w) this field
can also be used to make that distinction. At what level of detail to make the
distinction (for example, just between RARE and FLASH, or between RARE, FLASH, and
FLASHsubsampled) remains at the discretion of the researcher.

Similarly the OPTIONAL [`ce-<label>`](../99-appendices/09-entities.md#ce)
key/value can be used to distinguish
sequences using different contrast enhanced images. The label is the name of the
contrast agent. The key `ContrastBolusIngredient` MAY be also be added in the
JSON file, with the same label.

Some meta information about the acquisition MAY be provided in an additional
JSON file. See [Common metadata fields](#common-metadata-fields) for a
list of terms and their definitions. There are also some OPTIONAL JSON
fields specific to anatomical scans:

| **Key name**            | **Requirement level** | **Data type** | **Description**                                                                                                                          |
| ----------------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------- |
| ContrastBolusIngredient | OPTIONAL              | [string][]    | Active ingredient of agent. Values MUST be one of: IODINE, GADOLINIUM, CARBON DIOXIDE, BARIUM, XENON Corresponds to DICOM Tag 0018,1048. |

Similarly, the OPTIONAL [`rec-<label>`](../99-appendices/09-entities.md#rec)
key/value can be used to distinguish
different reconstruction algorithms (for example ones using motion correction).

## Task (including resting state) imaging data

Currently supported image contrasts include:

| **Name**  | `contrast_label` | **Description**                                                                                      |
|---------- | ---------------- | ---------------------------------------------------------------------------------------------------- |
| BOLD      | bold             | Blood-Oxygen-Level Dependent contrast (specialized T2\* weighting)                                   |
| CBV       | cbv              | Cerebral Blood Volume contrast (specialized T2\* weighting or difference between T1 weighted images) |
| Phase     | phase            | Phase information associated with magnitude information stored in BOLD contrast                      |

Template:

```Text
sub-<label>/[ses-<label>/]
    func/
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_echo-<index>]_<contrast_label>.nii[.gz]
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_echo-<index>]_sbref.nii[.gz]
```

Functional imaging consists of techniques that support rapid temporal repetition.
This includes but is not limited to task based fMRI
as well as resting state fMRI, which is treated like any other task. For task
based fMRI a corresponding task events file (see below) MUST be provided
(please note that this file is not necessary for resting state scans). For
multiband acquisitions, one MAY also save the single-band reference image as
type `sbref` (for example, `sub-control01_task-nback_sbref.nii.gz`).

Each task has a unique label that MUST only consist of letters and/or numbers
(other characters, including spaces and underscores, are not allowed) with the
[`task-<label>`](../99-appendices/09-entities.md#task) key/value pair.
Those labels MUST be consistent across subjects and sessions.

If more than one run of the same task has been acquired the
[`run-<index>`](../99-appendices/09-entities.md#run) key/value pair MUST be used:
`_run-1`, `_run-2`, `_run-3`, and so on. If only one run was acquired the
`run-<index>` can be omitted. In the context of functional imaging a run is
defined as the same task, but in some cases it can mean different set of stimuli
(for example randomized order) and participant responses.

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label one may
use to distinguish different set of parameters used for acquiring the same task.
For example this should be used when a study includes two resting state images -
one single band and one multiband. In such case two files could have the
following names: `sub-01_task-rest_acq-singleband_bold.nii.gz` and
`sub-01_task-rest_acq-multiband_bold.nii.gz`, however the user is MAY choose any
other label than `singleband` and `multiband` as long as they are consistent
across subjects and sessions and consist only of the legal label characters.

Similarly the OPTIONAL [`ce-<label>`](../99-appendices/09-entities.md#ce)
key/value can be used to distinguish
sequences using different contrast enhanced images. The label is the name of the
contrast agent. The key ContrastBolusIngredient MAY be also be added in the JSON
file, with the same label.

Similarly the OPTIONAL [`rec-<label>`](../99-appendices/09-entities.md#rec)
key/value can be used to distinguish
different reconstruction algorithms (for example ones using motion correction).

Similarly the OPTIONAL [`dir-<label>`](../99-appendices/09-entities.md#dir)
and [`rec-<label>`](../99-appendices/09-entities.md#rec) key/values
can be used to distinguish different phase-encoding directions and
reconstruction algorithms (for example ones using motion correction).
See [`fmap` Case 4](01-magnetic-resonance-imaging-data.md#case-4-multiple-phase-encoded-directions-pepolar)
for more information on `dir` field specification.

Multi-echo data MUST be split into one file per echo using the
[`echo-<index>`](../99-appendices/09-entities.md#echo) key-value pair. For example:

```Text
sub-01/
   func/
      sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-1_bold.json
      sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-2_bold.json
      sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-3_bold.json
```

Please note that the `<index>` denotes the number/index (in the form of a
nonnegative integer) of the echo not the echo time value which needs to be stored in the
field EchoTime of the separate JSON file.

Some meta information about the acquisition MUST be provided in an additional
JSON file.

### Required fields

| **Key name**   | **Requirement level** | **Data type**            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------- | --------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| RepetitionTime | REQUIRED              | [number][]               | The time in seconds between the beginning of an acquisition of one volume and the beginning of acquisition of the volume following it (TR). Please note that this definition includes time between scans (when no data has been acquired) in case of sparse acquisition schemes. This value needs to be consistent with the `pixdim[4]` field (after accounting for units stored in `xyzt_units` field) in the NIfTI header. This field is mutually exclusive with `VolumeTiming` and is derived from DICOM Tag 0018, 0080 and converted to seconds. |
| VolumeTiming   | REQUIRED              | [array][] of [numbers][] | The time at which each volume was acquired during the acquisition. It is described using a list of times referring to the onset of each volume in the BOLD series. The list must have the same length as the BOLD series, and the values must be non-negative and monotonically increasing. This field is mutually exclusive with `RepetitionTime` and `DelayTime`. If defined, this requires acquisition time (TA) be defined via either `SliceTiming` or `AcquisitionDuration` be defined.                                                         |
| TaskName       | REQUIRED              | [string][]               | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric (`[a-zA-Z0-9]`) characters. For example TaskName `faces n-back` will correspond to task label `facesnback`. A RECOMMENDED convention is to name resting state task using labels beginning with `rest`.                                                                                                                                                                       |

For the fields described above and in the following section, the term "Volume"
refers to a reconstruction of the object being imaged (for example, brain or part of a
brain). In case of multiple channels in a coil, the term "Volume" refers to a
combined image rather than an image from each coil.

### Other RECOMMENDED metadata

#### Timing Parameters

| **Key name**                      | **Requirement level**                                                                                                                                                                              | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NumberOfVolumesDiscardedByScanner | RECOMMENDED                                                                                                                                                                                        | [integer][]   | Number of volumes ("dummy scans") discarded by the scanner (as opposed to those discarded by the user post hoc) before saving the imaging file. For example, a sequence that automatically discards the first 4 volumes before saving would have this field as 4. A sequence that doesn't discard dummy scans would have this set to 0. Please note that the onsets recorded in the \_event.tsv file should always refer to the beginning of the acquisition of the first volume in the corresponding imaging file - independent of the value of `NumberOfVolumesDiscardedByScanner` field. |
| NumberOfVolumesDiscardedByUser    | RECOMMENDED                                                                                                                                                                                        | [integer][]   | Number of volumes ("dummy scans") discarded by the user before including the file in the dataset. If possible, including all of the volumes is strongly recommended. Please note that the onsets recorded in the \_event.tsv file should always refer to the beginning of the acquisition of the first volume in the corresponding imaging file - independent of the value of `NumberOfVolumesDiscardedByUser` field.                                                                                                                                                                       |
| DelayTime                         | RECOMMENDED                                                                                                                                                                                        | [number][]    | User specified time (in seconds) to delay the acquisition of data for the following volume. If the field is not present it is assumed to be set to zero. Corresponds to Siemens CSA header field `lDelayTimeInTR`. This field is REQUIRED for sparse sequences using the `RepetitionTime` field that do not have the `SliceTiming` field set to allowed for accurate calculation of "acquisition time". This field is mutually exclusive with `VolumeTiming`.                                                                                                                               |
| AcquisitionDuration               | RECOMMENDED, but REQUIRED for sequences that are described with the `VolumeTiming` field and that do not have the `SliceTiming` field set to allow for accurate calculation of "acquisition time"  | [number][]    | Duration (in seconds) of volume acquisition. Corresponds to DICOM Tag 0018,9073 `Acquisition Duration`. This field is mutually exclusive with `RepetitionTime`.                                                                                                                                                                                                                                                                                                                                                                                                                             |
| DelayAfterTrigger                 | RECOMMENDED                                                                                                                                                                                        | [number][]    | Duration (in seconds) from trigger delivery to scan onset. This delay is commonly caused by adjustments and loading times. This specification is entirely independent of `NumberOfVolumesDiscardedByScanner` or `NumberOfVolumesDiscardedByUser`, as the delay precedes the acquisition.                                                                                                                                                                                                                                                                                                    |

The following table recapitulates the different ways that specific fields have
to be populated for functional sequences. Note that all these options can be
used for non sparse sequences but that only options B, D and E are valid for
sparse sequences.

|          | RepetitionTime | SliceTiming | AcquisitionDuration | DelayTime | VolumeTiming |
| -------- | :------------: | :---------: | :-----------------: | :-------: | :----------: |
| option A |     \[ X ]     |             |         \[ ]        |           |     \[ ]     |
| option B |      \[ ]      |    \[ X ]   |                     |    \[ ]   |    \[ X ]    |
| option C |      \[ ]      |             |        \[ X ]       |    \[ ]   |    \[ X ]    |
| option D |     \[ X ]     |    \[ X ]   |         \[ ]        |           |     \[ ]     |
| option E |     \[ X ]     |             |         \[ ]        |   \[ X ]  |     \[ ]     |

**Legend**

-   \[ X ] --> has to be filled
-   \[   \] --> has to be left empty
-   empty cell --> can be specified but not required

#### fMRI task information

| **Key name**    | **Requirement level** | **Data type** | **Description**                                                                                                                                                                               |
|-----------------|-----------------------|---------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Instructions    | RECOMMENDED           | [string][]    | Text of the instructions given to participants before the scan. This is especially important in context of resting state fMRI and distinguishing between eyes open and eyes closed paradigms. |
| TaskDescription | RECOMMENDED           | [string][]    | Longer description of the task.                                                                                                                                                               |
| CogAtlasID      | RECOMMENDED           | [string][]    | [URI][uri] of the corresponding [Cognitive Atlas](https://www.cognitiveatlas.org/) Task term.                                                                                                 |
| CogPOID         | RECOMMENDED           | [string][]    | [URI][uri] of the corresponding [CogPO](http://www.cogpo.org/) term.                                                                                                                          |

See [Common metadata fields](#common-metadata-fields) for a list of
additional terms and their definitions.

Example:

```Text
sub-control01/
    func/
        sub-control01_task-nback_bold.json
```

```JSON
{
   "TaskName": "N Back",
   "RepetitionTime": 0.8,
   "EchoTime": 0.03,
   "FlipAngle": 78,
   "SliceTiming": [0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6],
   "MultibandAccelerationFactor": 4,
   "ParallelReductionFactorInPlane": 2,
   "PhaseEncodingDirection": "j",
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "DeviceSerialNumber": "11035"
}
```

If this information is the same for all participants, sessions and runs it can
be provided in `task-<label>_bold.json` (in the root directory of the
dataset). However, if the information differs between subjects/runs it can be
specified in the
`sub-<label>/func/sub-<label>_task-<label>[_acq-<label>][_run-<index>]_bold.json` file.
If both files are specified fields from the file corresponding to a particular
participant, task and run takes precedence.

## Diffusion imaging data

Template:

```Text
sub-<label>/[ses-<label>/]
    dwi/
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_dwi.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_dwi.bval
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_dwi.bvec
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_dwi.json
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_sbref.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>]_sbref.json
```

Diffusion-weighted imaging data acquired for that participant. The OPTIONAL
[`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label the user may use to
distinguish different set of parameters. For example this should be used when a
study includes two diffusion images - one single band and one multiband. In such
case two files could have the following names:
`sub-01_acq-singleband_dwi.nii.gz` and `sub-01_acq-multiband_dwi.nii.gz`,
however the user is free to choose any other label than `singleband` and
`multiband` as long as they are consistent across subjects and sessions. For
multiband acquisitions, one can also save the single-band reference image as
type `sbref` (for example, `dwi/sub-control01_sbref.nii[.gz]`) The bvec and bval files
are in the [FSL format](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/UserGuide#DTIFIT):
The bvec files contain 3 rows with n space-delimited floating-point numbers
(corresponding to the n volumes in the relevant NIfTI file). The first row
contains the x elements, the second row contains the y elements and third row
contains the z elements of a unit vector in the direction of the applied
diffusion gradient, where the i-th elements in each row correspond together to
the i-th volume with `[0,0,0]` for non-diffusion-weighted volumes. Inherent to
the FSL format for bvec specification is the fact that the coordinate system of
the bvecs is with respect to the participant, defined by the axes of the
corresponding `dwi.nii` file, and not the magnet's coordinate system.
Thus, any rotations applied to `dwi.nii` also need to be applied to the
corresponding bvec file.

bvec example:

```Text
0 0 0.021828 -0.015425 -0.70918 -0.2465
0 0 0.80242 0.22098 -0.00063106 0.1043
0 0 -0.59636 0.97516 -0.70503 -0.96351
```

The bval file contains the b-values (in s/mm<sup>2</sup>) corresponding to the
volumes in the relevant NIfTI file), with 0 designating non-diffusion-weighted
volumes, space-delimited.

bval example:

```Text
0 0 2000 2000 1000 1000
```

`.bval` and `.bvec` files can be saved on any level of the directory structure
and thus define those values for all sessions and/or subjects in one place (see
Inheritance principle).

See [Common metadata fields](#common-metadata-fields) for a list of
additional terms that can be included in the corresponding JSON file.

JSON example:

```JSON
{
  "PhaseEncodingDirection": "j-",
  "TotalReadoutTime": 0.095
}
```

## Arterial Spin Labeling data

Template:

```Text
sub-<label>/[ses-<label>/]
    perf/
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.json
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv
       [sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.nii[.gz]]
       [sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.json]
       [sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_labeling.[jpeg|png]]
```

The current ASL extension defaults to single-post labeling delay (PLD) ASL-data, for the quantification of brain perfusion, and multi-PLD data, for both Pulsed ASL (PASL), 
Pseudocontinuous ASL (PCASL) and Continuous ASL (CASL) approaches. Upon the conversion of DICOM to BIDS, all separate ASL timeseries should be stored as a separate 4D NIfTI file 
in the original acquisition order, and be joined by two ancillary files: `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.json` and `sub-<label>[_ses-
<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv`. Beware that the DICOM images exported from the scanner may be sorted in a different order than the 
acquisition order. In this case, they should be sorted in the acquisition order.

The responsibility of applying any scale slope defined in the DICOM header lies within the DCM2BIDS conversion, not in the image processing stage. Any conversion of DICOM data 
to NIfTI, both for ASL as M0, should apply the scale-slope information provided by the vendor, without any residual scale factors. Thus, the raw BIDS NIfTIs should not contain 
any scaled data, and no scaling factors should be stored in the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.json`,`sub-<label>[_ses-<label>][_acq-
<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.json` or NIfTI header. 

Multi-PLD sequences consist of time-series, for which the acquisition parameters can differ. Therefore, some parameters can either only be allowed as a scalar (e.g. 
`Manufacturer`), or both as a scalar and a vector with the same length as the number of volumes (e.g. `PostLabelingDelay` and `BackgroundSuppressionPulseTime`), described in 
`sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv`. Vectors of different lengths are never allowed to avoid confusion.

Generally, five types of volumes might be acquired: `control`, `label`, `m0scan`, `deltam` and `cbf`, based on DICOM Tag ASL Context (0018,9257) `ASL Context`. It should be 
noted that there are different ways to acquire `control` and `label` volumes, and thus the naming of `control` and `label` within BIDS only serves to specify the subtraction 
order.

| asl volume name                    | Definition    |
|---------------------------------- | -----------------------------------------------------|
| control                  | A control image is acquired in the exact same way as the label image, except for the modification in the ASL-preparation pulse. In the control images, this pulse effectively leads to no labeling of blood, i.e. the blood and tissue having identically aligned magnetization. It is important for both control and label images to be scaled identically. If no background suppression or pre-saturation pulses were applied, this image can be used as M0. Note that for FAIR PASL, the control volume is referred to as slice selective volume (see [https://www.ncbi.nlm.nih.gov/pubmed/7500865](https://www.ncbi.nlm.nih.gov/pubmed/7500865)).   |
| label                  | A label image is produced with proximal labeling of inflowing arterial blood, i.e. blood has inverted magnetization when compared to tissue. Note that for FAIR PASL, the label volume is referred to as non-selective (see [https://www.ncbi.nlm.nih.gov/pubmed/7500865](https://www.ncbi.nlm.nih.gov/pubmed/7500865)).    |
| m0scan                  | A M0 image is a calibration or reference image, used to estimate the M0 of blood. It is usually weighted toward the M0 of tissue, and is required especially when ASL is acquired with background suppression and/or pre-saturation pulses.    |
| deltam                  | The deltaM image is a perfusion-weighted image, which is formed by the subtraction of label from control images (`control` - `label`). These subtractions are averaged over multiple repeats, but can also be kept as individual subtractions, if perfusion time-courses are of interest. This is a derivative that can be regarded as raw data, when the raw data needed to derive deltaM is not available.     |
| cbf                  | The quantified cerebral blood flow (CBF) image is produced by dividing the deltaM by the M0 image or the M0 scalar value, which is then scaled into physiological units (`mL/100g/min`). This is a derivative that can be regarded as raw data when the raw data needed to derive CBF is not available.       |

Formally, `deltam` and `cbf` are derivatives (images calculated from raw data), and should therefore be stored in the `derivatives` folder. However, for some ASL sequences (e.g. 
the GE product sequence or the Philips product sequence with ‘ASLSourceImage’ set to off), these images are provided as raw data, instead of the `control` and `label` images. 
Therefore, those derivatives are included in the current BIDS extension, but should only be stored as ASL data in the `rawdata` folder in case the raw images are not available. 
It is always required to store the raw images when available (i.e. unsubtracted `control` and `label` images). The storage of the volumes follows the hierarchy in order of 
preference: 1) `control`/`label`/`m0scan`, 2) `deltam`/`m0scan`, 3) `cbf`[/`m0scan`]. Additionally, when `cbf` is stored as raw data, the units need to be specified in the `sub-
<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.json`.

The `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv` lists the original acquisition order of the `sub-<label>[_ses-<label>][_acq-<label>]
[_rec-<label>][_run-<index>]_asl.nii[.gz]`, containing one or more of the five ASL volumes. In contrast, the acquisition order for all other separately acquired images, e.g. M0 
acquired separately, with or without phase encoding direction, or a labeling plane image should not be specified in this `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>]
[_run-<index>]_aslcontext.tsv`.

`sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv` example 1:

```Text
volume_type
m0scan
control
label
control
label
control
label
```

`sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv` example 2, in case no raw data (`control` and `label`) is available:

```Text
volume_type
deltam
m0scan
```

The `m0scan`, used as a calibration image, should be converted in the original acquisition order. Currently both the acquisition of the `m0scan` within the asl time series, as 
well as acquiring it separately is equally valid. In the first case, the `m0scan` should be included in the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-
<index>]_asl.nii[.gz]`, its position within the time series should be specified in the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv`. When 
the `m0scan` is acquired separately, or when acquired with reversed phase encoding (fieldmap: pepolar), a separate `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-
<label>][_run-<index>]_m0scan.nii[.gz]` and `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.json` should be provided, including the M0-
specific JSON fields. In this case, the `m0scan` should not be included in the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv`. 
Alternatively, the average `control` image or a fixed value can be used for calibration. In any case, the calibration approach utilised should be specified in the M0 field of 
the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asl.json`.

It is recommended to specify as much labeling information as possible for quality control, such as: a description of the location of the labeling slab, the labeling slab 
orientation, labeling slab distance and labeling slab thickness, and the labeling efficiency. An anonymized screenshot of the planning of the labeling plane for each session, 
saved as `[sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_labeling.[jpeg|png]]`, can clarify exact positioning and is recommended.

### Required fields

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                   |
|-------------------------------|-----------------------|---------------|------------------------------------------------------------------------------------------|
|  LabelingType                | REQUIRED            | [string][]    | `PASL` (pulsed ASL), `CASL` (continuous ASL), `PCASL` (pseudo-continuous ASL). Note that `PCASL` is a modification of `CASL`, and uses the same quantification                                                                                    |
|  PostLabelingDelay                 | REQUIRED            | [number][] or [array][] of [numbers][]   | This is the time, in seconds, after the middle of the labeling pulse (for `PASL`) or the end of labeling (for `(P)CASL`) until the middle of the excitation pulse applied to the imaging slab. More specifically, in case of 2D multi-slice, this is the time, in seconds, to the excitation of the first slice. In the case of 3D, this is the time, in seconds, to the excitation of the 3D volume. For a single-PLD time series, this is a single scalar value which has been used for all volumes, whereas in case of multi-PLD and Look-Locker, this is a vector of PLDs for which the PLD of each volume (i.e. each `control` and `label`), or of the first slice in case of 2D, is given separately, in the order of acquisition. Any image within the time-series without a PLD is indicated by a zero (e.g. a `m0scan`). Based on DICOM Tag 0018,9079 `Inversion Times` and 0018,0082 `InversionTime` |
|  BackgroundSuppression                | REQUIRED            | [boolean][]           | Boolean indicating if background suppression has been used                           |
|  M0               | REQUIRED            | [string][] or [number][] or [boolean][]           | Location of `m0scan`, or information on M0 approach used, which can be either (depending on the data-type): Numerical: a single numerical whole-brain M0 value (e.g. obtained from the CSF in another sequence); SeparateFile: `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.nii[.gz]`; WithinASL: Boolean (`true` or `false`) value: `true` referring to a `m0scan` within the time series and defined within the `sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_aslcontext.tsv`; `false` referring to the use of the (average) `control` image for M0 calibration, in case background suppression or pre-saturation pulses were not applied       |

### (P)CASL-specific fields

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                   |
|-------------------------------|-----------------------|---------------|------------------------------------------------------------------------------------------|
|  LabelingDuration                 | REQUIRED            | [number][] or [array][] of [numbers][]         | Total duration, in seconds, of the labeling pulse train. This corresponds to the temporal width of the labeling bolus for (P)CASL. Specify either one value for total time-series or provide a vector of different values for each volume in case of sequential acquisitions with varying labeling duration. For PASL, the parameters of bolus saturation timing and bolus width are given in `BolusCutOff fields`, and the `LabelingDuration` field is set to zero or not provided. Note that in case a vector is provided and a `m0scan` is acquired within the ASL series, `LabelingDuration` also needs to be provided for the `m0scan` (preferably zero), to keep the length of the vector equal to the number of volumes. Corresponds to DICOM Tag 0018,9258 `ASL Pulse Train Duration` |
|  PCASLType                 | RECOMMENDED             | [string][]         | For `PCASL`, this contains the type of the `control` pulse: `balanced` or `unbalanced`  |
|  CASLType                  | RECOMMENDED             | [string][]         |  For `CASL`. It describes if a separate coil is used for labeling: `single-coil` or `double-coil`  |
|  LabelingPulseAverageGradient                   | RECOMMENDED             | [number][]         |  For `PCASL`, the average labeling gradient, in millitesla per meter. Based on COBIDAS |
|  LabelingPulseMaximumGradient                  | RECOMMENDED             | [number][]         | For `(P)CASL`, the maximum amplitude of the labeling gradient, in millitesla per meter. Based on COBIDAS  |
|  LabelingPulseAverageB1                   | RECOMMENDED             | [number][]         | For `(P)CASL`, the average B1-field strength of the RF labeling pulses, in microtesla. As an alternative, `LabelingPulseFlipAngle` can be provided. Based on COBIDAS  |
|  LabelingPulseDuration                    | RECOMMENDED             | [number][]         | For `PCASL`, duration, in seconds, of the individual labeling pulses  |

### PASL-specific fields

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                   |
|-------------------------------|-----------------------|---------------|------------------------------------------------------------------------------------------|

### Other recommended asl-related fields

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                   |
|-------------------------------|-----------------------|---------------|------------------------------------------------------------------------------------------|

### m0scan-specific fields

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                   |
|-------------------------------|-----------------------|---------------|------------------------------------------------------------------------------------------|

## Fieldmap data

Data acquired to correct for B0 inhomogeneities can come in different forms. The
current version of this standard considers four different scenarios. Please note
that in all cases fieldmap data can be linked to a specific scan(s) it was
acquired for by filling the IntendedFor field in the corresponding JSON file.
For example:

```JSON
{
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

The IntendedFor field may contain one or more filenames with paths relative to
the subject subfolder. The path needs to use forward slashes instead of backward
slashes. Here's an example with multiple target scans:

```JSON
{
   "IntendedFor": ["ses-pre/func/sub-01_ses-pre_task-motor_run-1_bold.nii.gz",
                   "ses-post/func/sub-01_ses-post_task-motor_run-1_bold.nii.gz"]
}
```

The IntendedFor field is OPTIONAL and in case the fieldmaps do not correspond to
any particular scans it does not have to be filled.

Multiple fieldmaps can be stored.
In such case the [`run-<index>`](../99-appendices/09-entities.md#run) key/value pair should be
used. The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label
the user may use to distinguish different set of parameters.

### Case 1: Phase difference image and at least one magnitude image

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.json
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude1.nii[.gz]
```

OPTIONAL

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude2.nii[.gz]
```

This is a common output for build in fieldmap sequence on Siemens scanners. In
this particular case the sidecar JSON file has to define the Echo Times of the
two phase images used to create the difference image. `EchoTime1` corresponds to
the shorter echo time and `EchoTime2` to the longer echo time. Similarly
`_magnitude1` image corresponds to the shorter echo time and the OPTIONAL
`_magnitude2` image to the longer echo time. For example:

```JSON
{
   "EchoTime1": 0.00600,
   "EchoTime2": 0.00746,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

### Case 2: Two phase images and two magnitude images

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase1.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase1.json
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase2.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase2.json
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude1.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude2.nii[.gz]
```

Similar to the case above, but instead of a precomputed phase difference map two
separate phase images are presented. The two sidecar JSON files need to specify
corresponding `EchoTime` values. For example:

```JSON
{
   "EchoTime": 0.00746,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

### Case 3: A real fieldmap image

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_fieldmap.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_fieldmap.json
```

In some cases (for example GE) the scanner software will output a precomputed
fieldmap denoting the B0 inhomogeneities along with a magnitude image used for
coregistration.
In this case the sidecar JSON file needs to include the units of the fieldmap.
The possible options are: Hertz (`Hz`), Radians per second (`rad/s`), or Tesla
(`T`).
For example:

```JSON
{
   "Units": "rad/s",
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

### Case 4: Multiple phase encoded directions ("pepolar")

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_epi.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_epi.json
```

The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo
EPI scans with different phase encoding directions to estimate the underlying
inhomogeneity/deformation map. Examples of tools using this kind of images are
FSL TOPUP, AFNI 3dqwarp and SPM. In such a case, the phase encoding direction is
specified in the corresponding JSON file as one of: `i`, `j`, `k`, `i-`, `j-`,
`k-`. For these differentially phase encoded sequences, one also needs to
specify the Total Readout Time defined as the time (in seconds) from the center
of the first echo to the center of the last echo (aka "FSL definition" - see
[here](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup/Faq#How_do_I_know_what_phase-encode_vectors_to_put_into_my_--datain_text_file.3F) and
[here](https://lcni.uoregon.edu/kb-articles/kb-0003) how to calculate it). For
example

```JSON
{
   "PhaseEncodingDirection": "j-",
   "TotalReadoutTime": 0.095,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

The `label` value of the [`dir-<label>`](../99-appendices/09-entities.md#dir) key/value pair
can be set to arbitrary alphanumeric label (`[a-zA-Z0-9]+` for
example `LR` or `AP`) that can help users to distinguish between different
files, but should not be used to infer any scanning parameters (such as phase
encoding directions) of the corresponding sequence. Please rely only on the JSON
file to obtain scanning parameters. \_epi files can be a 3D or 4D - in the
latter case all timepoints share the same scanning parameters. To indicate which
run is intended to be used with which functional or diffusion scan the
IntendedFor field in the JSON file should be used.

<!-- Link Definitions -->

[deprecated]: ../02-common-principles.md#definitions
[string]: https://www.w3schools.com/js/js_json_datatypes.asp
[strings]: https://www.w3schools.com/js/js_json_datatypes.asp
[integer]: https://www.w3schools.com/js/js_json_datatypes.asp
[number]: https://www.w3schools.com/js/js_json_datatypes.asp
[numbers]: https://www.w3schools.com/js/js_json_datatypes.asp
[boolean]: https://www.w3schools.com/js/js_json_datatypes.asp
[array]: https://www.w3schools.com/js/js_json_arrays.asp
[arrays]: https://www.w3schools.com/js/js_json_arrays.asp
[object]: https://www.json.org/json-en.html
[uri]: ../02-common-principles.md#uniform-resource-indicator
