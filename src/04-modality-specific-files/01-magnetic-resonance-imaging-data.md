# Magnetic Resonance Imaging

## Common metadata fields

MR Data described in the following sections share the following RECOMMENDED metadata
fields (stored in sidecar JSON files). MRI acquisition parameters are divided
into several categories based on
["A checklist for fMRI acquisition methods reporting in the literature"](https://thewinnower.com/papers/977-a-checklist-for-fmri-acquisition-methods-reporting-in-the-literature)
by Ben Inglis:

### Scanner Hardware

| **Key name**                  | **Requirement level**                                | **Data type** | **Description**                                                                                                                                                                                                                                                           |
|-------------------------------|------------------------------------------------------|---------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Manufacturer                  | RECOMMENDED                                          | [string][]    | Manufacturer of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0070 `Manufacturer`                                                                                                                                                   |
| ManufacturersModelName        | RECOMMENDED                                          | [string][]    | Manufacturer's model name of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1090 `Manufacturers Model Name`                                                                                                                          |
| DeviceSerialNumber            | RECOMMENDED                                          | [string][]    | The serial number of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1000 `DeviceSerialNumber`. A pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset |
| StationName                   | RECOMMENDED                                          | [string][]    | Institution defined name of the machine that produced the composite instances. Corresponds to DICOM Tag 0008, 1010 `Station Name`                                                                                                                                         |
| SoftwareVersions              | RECOMMENDED                                          | [string][]    | Manufacturer's designation of software version of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1020 `Software Versions`                                                                                                            |
| HardcopyDeviceSoftwareVersion | [DEPRECATED][]                                       | [string][]    | Manufacturer's designation of the software of the device that created this Hardcopy Image (the printer). Corresponds to DICOM Tag 0018, 101A `Hardcopy Device Software Version`                                                                                           |
| MagneticFieldStrength         | RECOMMENDED, but REQUIRED for Arterial Spin Labeling | [number][]    | Nominal field strength of MR magnet in Tesla. Corresponds to DICOM Tag 0018,0087 `Magnetic Field Strength`                                                                                                                                                                |
| ReceiveCoilName               | RECOMMENDED                                          | [string][]    | Information describing the receiver coil. Corresponds to DICOM Tag 0018, 1250 `Receive Coil Name`, although not all vendors populate that DICOM Tag, in which case this field can be derived from an appropriate private DICOM field                                      |
| ReceiveCoilActiveElements     | RECOMMENDED                                          | [string][]    | Information describing the active/selected elements of the receiver coil. This doesn't correspond to a tag in the DICOM ontology. The vendor-defined terminology for active coil elements can go in this field. See an example below the table.                           |
| GradientSetType               | RECOMMENDED                                          | [string][]    | It should be possible to infer the gradient coil from the scanner model. If not, for example because of a custom upgrade or use of a gradient insert set, then the specifications of the actual gradient coil should be reported independently                            |
| MRTransmitCoilSequence        | RECOMMENDED                                          | [string][]    | This is a relevant field if a non-standard transmit coil is used. Corresponds to DICOM Tag 0018, 9049 `MR Transmit Coil Sequence`                                                                                                                                         |
| MatrixCoilMode                | RECOMMENDED                                          | [string][]    | (If used) A method for reducing the number of independent channels by combining in analog the signals from multiple coil elements. There are typically different default modes when using un-accelerated or accelerated (for example, GRAPPA, SENSE) imaging              |
| CoilCombinationMethod         | RECOMMENDED                                          | [string][]    | Almost all fMRI studies using phased-array coils use root-sum-of-squares (rSOS) combination, but other methods exist. The image reconstruction is changed by the coil combination method (as for the matrix coil mode above), so anything non-standard should be reported |

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

| **Key name**                | **Requirement level**                                                                     | **Data type**                          | **Description**                                                                                                                                                                                                                                                           |
|-----------------------------|-------------------------------------------------------------------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PulseSequenceType           | RECOMMENDED                                                                               | [string][]                             | A general description of the pulse sequence used for the scan (for example, MPRAGE, Gradient Echo EPI, Spin Echo EPI, Multiband gradient echo EPI).                                                                                                                       |
| ScanningSequence            | RECOMMENDED                                                                               | [string][] or [array][] of [strings][] | Description of the type of data acquired. Corresponds to DICOM Tag 0018, 0020 `Scanning Sequence`.                                                                                                                                                                        |
| SequenceVariant             | RECOMMENDED                                                                               | [string][] or [array][] of [strings][] | Variant of the ScanningSequence. Corresponds to DICOM Tag 0018, 0021 `Sequence Variant`.                                                                                                                                                                                  |
| ScanOptions                 | RECOMMENDED                                                                               | [string][] or [array][] of [strings][] | Parameters of ScanningSequence. Corresponds to DICOM Tag 0018, 0022 `Scan Options`.                                                                                                                                                                                       |
| SequenceName                | RECOMMENDED                                                                               | [string][]                             | Manufacturer's designation of the sequence name. Corresponds to DICOM Tag 0018, 0024 `Sequence Name`.                                                                                                                                                                     |
| PulseSequenceDetails        | RECOMMENDED                                                                               | [string][]                             | Information beyond pulse sequence type that identifies the specific pulse sequence used (for example, "Standard Siemens Sequence distributed with the VB17 software," "Siemens WIP ### version #.##," or "Sequence written by X using a version compiled on MM/DD/YYYY"). |
| NonlinearGradientCorrection | RECOMMENDED, but REQUIRED if [PET](./09-positron-emission-tomography.md) data are present | [boolean][]                            | Boolean stating if the image saved has been corrected for gradient nonlinearities by the scanner sequence.                                                                                                                                                                |
| MRAcquisitionType           | RECOMMENDED, but REQUIRED for Arterial Spin Labeling                                      | [string][]                             | Possible values: `2D` or `3D`. Type of sequence readout. Corresponds to DICOM Tag 0018,0023 `MR Acquisition Type`.                                                                                                                                                        |
| MTState                     | RECOMMENDED                                                                               | [boolean][]                            | Boolean stating whether the magnetization transfer pulse is applied. Corresponds to DICOM tag (0018, 9020) `Magnetization Transfer`.                                                                                                                                      |
| MTOffsetFrequency           | RECOMMENDED if the MTstate is `True`.                                                     | [number][]                             | The frequency offset of the magnetization transfer pulse with respect to the central H1 Larmor frequency in Hertz (Hz).                                                                                                                                                   |
| MTPulseBandwidth            | RECOMMENDED if the MTstate is `True`.                                                     | [number][]                             | The excitation bandwidth of the magnetization transfer pulse in Hertz (Hz).                                                                                                                                                                                               |
| MTNumberOfPulses            | RECOMMENDED if the MTstate is `True`.                                                     | [number][]                             | The number of magnetization transfer RF pulses applied before the readout.                                                                                                                                                                                                |
| MTPulseShape                | RECOMMENDED if the MTstate is `True`.                                                     | [string][]                             | Shape of the magnetization transfer RF pulse waveform. Accepted values: `HARD`, `GAUSSIAN`, `GAUSSHANN` (gaussian pulse with Hanning window), `SINC`, `SINCHANN` (sinc pulse with Hanning window), `SINCGAUSS` (sinc pulse with Gaussian window), `FERMI`.                |
| MTPulseDuration             | RECOMMENDED if the MTstate is `True`.                                                     | [number][]                             | Duration of the magnetization transfer RF pulse in seconds.                                                                                                                                                                                                               |
| SpoilingState               | RECOMMENDED                                                                               | [boolean][]                            | Boolean stating whether the pulse sequence uses any type of spoiling strategy to suppress residual transverse magnetization.                                                                                                                                              |
| SpoilingType                | RECOMMENDED if the SpoilingState is `True`.                                               | [string][]                             | Specifies which spoiling method(s) are used by a spoiled sequence. Accepted values: `RF`, `GRADIENT` or `COMBINED`.                                                                                                                                                       |
| SpoilingRFPhaseIncrement    | RECOMMENDED if the SpoilingType is `RF` or `COMBINED`.                                    | [number][]                             | The amount of incrementation described in degrees, which is applied to the phase of the excitation pulse at each TR period for achieving RF spoiling.                                                                                                                     |
| SpoilingGradientMoment      | RECOMMENDED if the SpoilingType is `GRADIENT` or `COMBINED`.                              | [number][]                             | Zeroth moment of the spoiler gradient lobe in millitesla times second per meter (mT.s/m).                                                                                                                                                                                 |
| SpoilingGradientDuration    | RECOMMENDED if the SpoilingType is `GRADIENT` or `COMBINED`.                              | [number][]                             | The duration of the spoiler gradient lobe in seconds. The duration of a trapezoidal lobe is defined as the summation of ramp-up and plateau times.                                                                                                                        |

### In-Plane Spatial Encoding
| **Key name**                   | **Requirement level** | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|--------------------------------|-----------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| NumberShots                    | RECOMMENDED           | [number][] or [array][] of [numbers][] | The number of RF excitations needed to reconstruct a slice or volume (may be referred to as partition). Please mind that this is not the same as Echo Train Length which denotes the number of k-space lines collected after excitation in a multi-echo readout. The data type array is applicable for specifying this parameter before and after the k-space center is sampled. Plase see [`NumberShots` metadata field](../99-appendices/11-qmri.md#numbershots-metadata-field) in the qMRI appendix for corresponding calculations.                                                                                                                                                                                                                                                                                    |
| ParallelReductionFactorInPlane | RECOMMENDED           | [number][]                             | The parallel imaging (for instance, GRAPPA) factor. Use the denominator of the fraction of k-space encoded for each slice. For example, 2 means half of k-space is encoded. Corresponds to DICOM Tag 0018, 9069 `Parallel Reduction Factor In-plane`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| ParallelAcquisitionTechnique   | RECOMMENDED           | [string][]                             | The type of parallel imaging used (for example GRAPPA, SENSE). Corresponds to DICOM Tag 0018, 9078 `Parallel Acquisition Technique`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| PartialFourier                 | RECOMMENDED           | [number][]                             | The fraction of partial Fourier information collected. Corresponds to DICOM Tag 0018, 9081 `Partial Fourier`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| PartialFourierDirection        | RECOMMENDED           | [string][]                             | The direction where only partial Fourier information was collected. Corresponds to DICOM Tag 0018, 9036 `Partial Fourier Direction`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| PhaseEncodingDirection         | RECOMMENDED           | [string][]                             | Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-`. The letters `i`, `j`, `k` correspond to the first, second and third axis of the data in the NIFTI file. The polarity of the phase encoding is assumed to go from zero index to maximum index unless `-` sign is present (then the order is reversed - starting from the highest index instead of zero). `PhaseEncodingDirection` is defined as the direction along which phase is was modulated which may result in visible distortions. Note that this is not the same as the DICOM term `InPlanePhaseEncodingDirection` which can have `ROW` or `COL` values. This parameter is REQUIRED if corresponding fieldmap data is present or when using multiple runs with different phase encoding directions (which can be later used for field inhomogeneity correction). |
| EffectiveEchoSpacing           | RECOMMENDED           | [number][]                             | The "effective" sampling interval, specified in seconds, between lines in the phase-encoding direction, defined based on the size of the reconstructed image in the phase direction. It is frequently, but incorrectly, referred to as "dwell time" (see `DwellTime` parameter below for actual dwell time). It is required for unwarping distortions using field maps. Note that beyond just in-plane acceleration, a variety of other manipulations to the phase encoding need to be accounted for properly, including partial fourier, phase oversampling, phase resolution, phase field-of-view and interpolation.<sup>2</sup> This parameter is REQUIRED if corresponding fieldmap data is present.                                                                                                                  |
| TotalReadoutTime               | RECOMMENDED           | [number][]                             | This is actually the "effective" total readout time , defined as the readout duration, specified in seconds, that would have generated data with the given level of distortion. It is NOT the actual, physical duration of the readout train. If `EffectiveEchoSpacing` has been properly computed, it is just `EffectiveEchoSpacing * (ReconMatrixPE - 1)`.<sup>3</sup> . This parameter is REQUIRED if corresponding "field/distortion" maps acquired with opposing phase encoding directions are present (see 8.9.4).                                                                                                                                                                                                                                                                                                  |
| MixingTime                     | RECOMMENDED           | [number][]                             | In the context of a stimulated- and spin-echo 3D EPI sequence for B1+ mapping, corresponds to the interval between spin- and stimulated-echo pulses. In the context of a diffusion-weighted double spin-echo sequence, corresponds to the interval between two successive diffusion sensitizing gradients, specified in seconds.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |

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

| **Key name**           | **Requirement level**                                                                                                                                       | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|----------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| EchoTime               | RECOMMENDED, but REQUIRED if corresponding fieldmap data is present, or the data comes from a multi echo sequence or Arterial Spin Labeling                 | [number][] or [array][] of [numbers][] | The echo time (TE) for the acquisition, specified in seconds. Corresponds to DICOM Tag 0018, 0081 Echo Time (please note that the DICOM term is in milliseconds not seconds). The data type number may apply to files from any MRI modality concerned with a single value for this field, or to the files in a [file collection](../99-appendices/10-file-collections.md) where the value of this field is iterated using the [echo entity](../99-appendices/09-entities.md#echo). The data type array provides a value for each volume in a 4D dataset and should only be used when the volume timing is critical for interpretation of the data, such as in [ASL](#arterial-spin-labeling-perfusion-data) or variable echo time fMRI sequences.                                                                                               |
| InversionTime          | RECOMMENDED                                                                                                                                                 | [number][]                             | The inversion time (TI) for the acquisition, specified in seconds. Inversion time is the time after the middle of inverting RF pulse to middle of excitation pulse to detect the amount of longitudinal magnetization. Corresponds to DICOM Tag 0018, 0082 `Inversion Time` (please note that the DICOM term is in milliseconds not seconds).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| SliceTiming            | RECOMMENDED, but REQUIRED for sparse sequences that do not have the `DelayTime` field set, and Arterial Spin Labeling with `MRAcquisitionType` set on `2D`. | [array][] of [numbers][]               | The time at which each slice was acquired within each volume (frame) of the acquisition. Slice timing is not slice order -- rather, it is a list of times containing the time (in seconds) of each slice acquisition in relation to the beginning of volume acquisition. The list goes through the slices along the slice axis in the slice encoding dimension (see below). Note that to ensure the proper interpretation of the `SliceTiming` field, it is important to check if the OPTIONAL `SliceEncodingDirection` exists. In particular, if `SliceEncodingDirection` is negative, the entries in `SliceTiming` are defined in reverse order with respect to the slice axis, such that the final entry in the `SliceTiming` list is the time of acquisition of slice 0. Without this parameter slice time correction will not be possible. |
| SliceEncodingDirection | RECOMMENDED                                                                                                                                                 | [string][]                             | Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-` (the axis of the NIfTI data along which slices were acquired, and the direction in which `SliceTiming` is defined with respect to). `i`, `j`, `k` identifiers correspond to the first, second and third axis of the data in the NIfTI file. A `-` sign indicates that the contents of `SliceTiming` are defined in reverse order - that is, the first entry corresponds to the slice with the largest index, and the final entry corresponds to slice index zero. When present, the axis defined by `SliceEncodingDirection` needs to be consistent with the ‘slice_dim' field in the NIfTI header. When absent, the entries in `SliceTiming` must be in the order of increasing slice index as defined by the NIfTI header.                                                                   |
| DwellTime              | RECOMMENDED                                                                                                                                                 | [number][]                             | Actual dwell time (in seconds) of the receiver per point in the readout direction, including any oversampling. For Siemens, this corresponds to DICOM field (0019,1018) (in ns). This value is necessary for the optional readout distortion correction of anatomicals in the HCP Pipelines. It also usefully provides a handle on the readout bandwidth, which isn't captured in the other metadata tags. Not to be confused with `EffectiveEchoSpacing`, and the frequent mislabeling of echo spacing (which is spacing in the phase encoding direction) as "dwell time" (which is spacing in the readout direction).                                                                                                                                                                                                                         |

### RF & Contrast

| **Key name**     | **Requirement level**                                   | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
|------------------|---------------------------------------------------------|----------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| FlipAngle        | RECOMMENDED, but REQUIRED if `LookLocker` is set `true` | [number][] or [array][] of [numbers][] | Flip angle (FA) for the acquisition, specified in degrees. Corresponds to: DICOM Tag 0018, 1314 `Flip Angle`. The data type number may apply to files from any MRI modality concerned with a single value for this field, or to the files in a [file collection](../99-appendices/10-file-collections.md) where the value of this field is iterated using the [flip entity](../99-appendices/09-entities.md#flip). The data type array provides a value for each volume in a 4D dataset and should only be used when the volume timing is critical for interpretation of the data, such as in [ASL](#arterial-spin-labeling-perfusion-data) or variable flip angle fMRI sequences. |
| NegativeContrast | OPTIONAL                                                | [boolean][]                            | `true` or `false` value specifying whether increasing voxel intensity (within sample voxels) denotes a decreased value with respect to the contrast suffix. This is commonly the case when Cerebral Blood Volume is estimated via usage of a contrast agent in conjunction with a T2\* weighted acquisition protocol.                                                                                                                                                                                                                                                                                                                                                              |

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
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_part-<label>]_<suffix>.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_defacemask.nii[.gz]
```

Anatomical (structural) data acquired for that participant. Currently supported
non-parametric structural MR images include:

| **Name**                                     | `suffix`         | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| -------------------------------------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| T1 weighted images                           | T1w              | In arbitrary units (arbitrary). The contrast of these images is mainly determined by spatial variations in the longitudinal relaxation time of the imaged specimen. In spin-echo sequences this contrast is achieved at relatively short repetition and echo times. To achieve this weighting in gradient-echo images, again, short repetition and echo times are selected; however, at relatively large flip angles. Another common approach to increase T1 weighting in gradient-echo images is to add an inversion preparation block to the beginning of the imaging sequence (for example, `TurboFLASH` or `MP-RAGE`). |
| T2 weighted images                           | T2w              | In arbitrary units (arbitrary). The contrast of these images is mainly determined by spatial variations in the (true) transverse relaxation time of the imaged specimen. In spin-echo sequences this contrast is achieved at relatively long repetition and echo times. Generally, gradient echo sequences are not the most suitable option for achieving T2 weighting, as their contrast natively depends on T2-star rather than on T2.                                                                                                                                                                                   |
| Proton density (PD) weighted images          | PDw              | In arbitrary units (arbitrary). The contrast of these images is mainly determined by spatial variations in the spin density (1H) of the imaged specimen. In spin-echo sequences this contrast is achieved at short repetition and long echo times. In a gradient-echo acquisition, PD weighting dominates the contrast at long repetition and short echo times, and at small flip angles.                                                                                                                                                                                                                                  |
| T2star weighted images                       | T2starw          | In arbitrary units (arbitrary). The contrast of these images is mainly determined by spatial variations in the (observed) transverse relaxation time of the imaged specimen. In spin-echo sequences, this effect is negated as the excitation is followed by an inversion pulse. The contrast of gradient-echo images natively depends on T2-star effects. However, for T2-star variation to dominate the image contrast, gradient-echo acquisitions are carried out at long repetition and echo times, and at small flip angles.                                                                                          |
| Fluid attenuated inversion recovery images   | FLAIR            | In arbitrary units (arbitrary). Structural images with predominant T2 contribution (a.k.a T2-FLAIR), in which signal from fluids (for example, CSF) is nulled out by adjusting inversion time, coupled with notably long repetition and echo times.                                                                                                                                                                                                                                                                                                                                                                        |
| Inplane T1                                   | inplaneT1        | In arbitrary units (arbitrary). T1 weighted structural image matched to a functional (task) image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| Inplane T2                                   | inplaneT2        | In arbitrary units (arbitrary). T2 weighted structural image matched to a functional (task) image.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| PD and T2 weighted images                    | PDT2             | In arbitrary units (arbitrary). PDw and T2w images acquired using a dual echo FSE sequence through view sharing process ([Johnson et al. 1994](https://pubmed.ncbi.nlm.nih.gov/8010268/)).                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Homogeneous (flat) T1-weighted MP2RAGE image | UNIT1            | In arbitrary units (arbitrary). UNIT1 images are REQUIRED to use this suffix regardless of the method used to generate them. Note that although this image is T1-weighted, regions without MR signal will contain white salt-and-pepper noise that most segmentation algorithms will fail on. Therefore, it is important to dissociate it from from `T1w`. Plase see [`MP2RAGE` specific notes](../99-appendices/11-qmri.md#unit1-images) in the qMRI appendix for further information.                                                                                                                                    |

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

| **Key name**              | **Requirement level** | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ------------------------- | --------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ContrastBolusIngredient   | OPTIONAL              | [string][]                             | Active ingredient of agent. Values MUST be one of: IODINE, GADOLINIUM, CARBON DIOXIDE, BARIUM, XENON Corresponds to DICOM Tag 0018,1048.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| RepetitionTimeExcitation  | OPTIONAL              | [number][]                             | The interval, in seconds, between two successive excitations. The DICOM tag that best refers to this parameter is [(0018, 0080)](http://dicomlookup.com/lookup.asp?sw=Tnumber&q=(0018,0080)). This field may be used together with the `RepetitionTimePreparation` for certain use cases, such as [MP2RAGE](https://doi.org/10.1016/j.neuroimage.2009.10.002). Use `RepetitionTimeExcitation` (in combination with `RepetitionTimePreparation` if needed) for anatomy imaging data rather than `RepetitionTime` as it is already defined as the amount of time that it takes to acquire a single volume in the [task imaging data](#task-including-resting-state-imaging-data) section. |
| RepetitionTimePreparation | OPTIONAL              | [number][] or [array][] of [numbers][] | The interval, in seconds, that it takes a preparation pulse block to re-appear at the beginning of the succeeding (essentially identical) pulse sequence block. The data type number may apply to files from any MRI modality concerned with a single value for this field. The data type array provides a value for each volume in a 4D dataset and should only be used when the volume timing is critical for interpretation of the data, such as in [ASL](#arterial-spin-labeling-perfusion-data).                                                                                                                                                                                   |

The [`part-<label>`](../99-appendices/09-entities.md#part) key/value pair is
used to indicate which component of the complex representation of the MRI
signal is represented in voxel data.
This entity is associated with the DICOM tag `0008,9208`.
Allowed label values for this entity are `phase`, `mag`, `real` and `imag`,
which are typically used in `part-mag`/`part-phase` or `part-real`/`part-imag`
pairs of files.
For example:

```Text
sub-01_part-mag_T1w.nii.gz
sub-01_part-mag_T1w.json
sub-01_part-phase_T1w.nii.gz
sub-01_part-phase_T1w.json
```

Phase images MAY be in radians or in arbitrary units.
The sidecar JSON file MUST include the units of the `phase` image.
The possible options are `rad` or `arbitrary`.
For example:

sub-01_part-phase_T1w.json

```Text
{
   "Units": "rad"
}
```

When there is only a magnitude image of a given type, the `part` key MAY be omitted.

Similarly, the OPTIONAL [`rec-<label>`](../99-appendices/09-entities.md#rec)
key/value can be used to distinguish
different reconstruction algorithms (for example ones using motion correction).

Structural MR images whose intensity is represented in a non-arbitrary scale
constitute parametric maps. Currently supported parametric maps include:

| **Name**                                     | `suffix`  | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|----------------------------------------------|-----------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Longitudinal relaxation time map             | T1map     | In seconds (s). T1 maps are REQUIRED to use this suffix regardless of the method used to generate them. See [this interactive book on T1 mapping](https://qmrlab.org/t1_book/intro) for further reading on T1-mapping.                                                                                                                                                                                                                                                                                            |
| Longitudinal relaxation rate map             | R1map     | In seconds<sup>-1</sup> (1/s). R1 maps (R1 = 1/T1) are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                |
| True transverse relaxation time map          | T2map     | In seconds (s). T2 maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                                           |
| True transverse relaxation rate map          | R2map     | In seconds<sup>-1</sup> (1/s). R2 maps (R2 = 1/T2) are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                |
| Observed transverse relaxation time map      | T2starmap | In seconds (s). T2-star maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                                      |
| Observed transverse relaxation rate map      | R2starmap | In seconds<sup>-1</sup> (1/s). R2-star maps (R2star = 1/T2star) are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                   |
| Proton density map                           | PDmap     | In arbitrary units (arbitrary). PD maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                           |
| Magnetization transfer ratio map             | MTRmap    | In arbitrary units (arbitrary). MTR maps are REQUIRED to use this suffix regardless of the method used to generate them. MTRmap intensity values are RECOMMENDED to be represented in percentage in the range of 0-100%.                                                                                                                                                                                                                                                                                          |
| Magnetization transfer saturation map        | MTsat     | In arbitrary units (arbitrary). MTsat maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                        |
| T1 in rotating frame (T1 rho) map            | T1rho     | In seconds (s). T1-rho maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                                       |
| Myelin water fraction map                    | MWFmap    | In arbitrary units (arbitrary). MWF maps are REQUIRED to use this suffix regardless of the method used to generate them. MWF intensity values are RECOMMENDED to be represented in percentage in the range of 0-100%.                                                                                                                                                                                                                                                                                             |
| Macromolecular tissue volume (MTV) map       | MTVmap    | In arbitrary units (arbitrary). MTV maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                                          |
| Combined PD/T2 map                           | PDT2map   | In arbitrary units (arbitrary). Combined PD/T2 maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                                                                                                                                                                               |
| Quantitative susceptibility map (QSM)        | Chimap    | In parts per million (ppm). QSM allows for determining the underlying magnetic susceptibility of tissue (Chi) ([Wang & Liu, 2014](https://onlinelibrary.wiley.com/doi/10.1002/mrm.25358)). Chi maps are REQUIRED to use this suffix regardless of the method used to generate them.                                                                                                                                                                                                                               |
| RF transmit field map                        | TB1map    | In arbitrary units (arbitrary). Radio frequency (RF) transmit (B1+) field maps are REQUIRED to use this suffix regardless of the method used to generate them. TB1map intensity values are RECOMMENDED to be represented as percent multiplicative factors such that FlipAngle<sub>effective</sub> = B1+<sub>intensity</sub>\*FlipAngle<sub>nominal</sub> .                                                                                                                                                       |
| RF receive sensitivity map                   | RB1map    | In arbitrary units (arbitrary). Radio frequency (RF) receive (B1-) sensitivity maps are REQUIRED to use this suffix regardless of the method used to generate them. RB1map intensity values are RECOMMENDED to be represented as percent multiplicative factors such that Amplitude<sub>effective</sub> = B1-<sub>intensity</sub>\*Amplitude<sub>ideal</sub>.                                                                                                                                                     |
| Observed signal amplitude (S0) map           | S0map     | In arbitrary units (arbitrary). For a multi-echo (typically fMRI) sequence, S0 maps index the baseline signal before exponential (T2-star) signal decay. In other words: the exponential of the intercept for a linear decay model across log-transformed echos. For more information, please see, for example, [the tedana documentation](https://tedana.readthedocs.io/en/latest/approach.html#monoexponential-decay-model-fit). S0 maps are RECOMMENDED to use this suffix if derived from an ME-FMRI dataset. |
| Equilibrium magnetization (M0) map           | M0map     | In arbitrary units (arbitrary). A common quantitative MRI (qMRI) fitting variable that represents the amount of magnetization at thermal equilibrium. M0 maps are RECOMMENDED to use this suffix if generated by qMRI applications (for example, variable flip angle T1 mapping).                                                                                                                                                                                                                                 |

Parametric images listed in the table above are typically generated by
processing a [file collection](../02-common-principles.md#entity-linked-file-collections).
Please visit the [file collections appendix](../99-appendices/10-file-collections.md) to see the
list of suffixes available for quantitative MRI (qMRI) applications associated
with these maps.
For any other details on the organization of parametric maps, their
recommended metadata fields, and the application specific entity or
metadata requirement levels of [file collections](../99-appendices/10-file-collections.md) that can generate
them, visit the [qMRI appendix](../99-appendices/11-qmri.md).

### Deprecated suffixes

Some suffixes that were available in versions of the specification prior to
1.5.0 have been deprecated.
These suffixes are ambiguous and have been superseded by more precise conventions.
Therefore, they are not recommended for use in new datasets.
They are, however, still valid suffixes, to maintain backwards compatibility.

The following suffixes are valid, but SHOULD NOT be used for new BIDS compatible
datasets (created after version 1.5.0.):

| **Name**           | `suffix`         | **Reason to deprecate**                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ------------------ | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| T2\*               | T2star           | Ambiguous, may refer to a parametric image or to a conventional image. **Change:** Replaced by `T2starw` or `T2starmap`.                                                                                                                                                                                                                                                                                                                   |
| FLASH              | FLASH            | FLASH (Fast-Low-Angle-Shot) is a vendor specific implementation for spoiled gradient echo acquisition. It is commonly used for rapid anatomical imaging and also for many different qMRI applications. When used for a single file, it does not convey any information about the image contrast. When used in a file collection, it may result in conflicts across filenames of different applications. **Change:** Removed from suffixes. |
| Proton density     | PD               | Ambiguous, may refer to a parametric image or to a conventional image. **Change:** Replaced by `PDw` or `PDmap`.                                                                                                                                                                                                                                                                                                                           |

## Task (including resting state) imaging data

Currently supported image contrasts include:

| **Name**  | `suffix` | **Description**                                                                                                                                                                                                                                                          |
|---------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| BOLD      | bold     | Blood-Oxygen-Level Dependent contrast (specialized T2\* weighting)                                                                                                                                                                                                       |
| CBV       | cbv      | Cerebral Blood Volume contrast (specialized T2\* weighting or difference between T1 weighted images)                                                                                                                                                                     |
| Phase     | phase    | [DEPRECATED](../02-common-principles.md#definitions). Phase information associated with magnitude information stored in BOLD contrast. This suffix should be replaced by the [`part-phase`](../99-appendices/09-entities.md#part) in conjunction with the `bold` suffix. |

Template:

```Text
sub-<label>/[ses-<label>/]
    func/
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_echo-<index>][_part-<label>]_bold.nii[.gz]
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_echo-<index>][_part-<label>]_cbv.nii[.gz]
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_ce-<label>][_dir-<label>][_rec-<label>][_run-<index>][_echo-<index>][_part-<label>]_sbref.nii[.gz]
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

Complex-valued data MUST be split into one file for each data type.
For BOLD data, there are separate suffixes for magnitude (`_bold`) and phase
(`_phase`) data, but the `_phase` suffix is [deprecated](../02-common-principles.md#definitions).
Newly generated datasets SHOULD NOT use the `_phase` suffix, and the suffix will be removed
from the specification in the next major release.
For backwards compatibility, `_phase` is considered equivalent to `_part-phase_bold`.
When the `_phase` suffix is not used, each file shares the same
name with the exception of the `part-<mag|phase>` or `part-<real|imag>` key/value.
For example:

```Text
sub-01/
   func/
      sub-01_task-cuedSGT_part-mag_bold.nii.gz
      sub-01_task-cuedSGT_part-mag_bold.json
      sub-01_task-cuedSGT_part-phase_bold.nii.gz
      sub-01_task-cuedSGT_part-phase_bold.json
      sub-01_task-cuedSGT_part-mag_sbref.nii.gz
      sub-01_task-cuedSGT_part-mag_sbref.json
      sub-01_task-cuedSGT_part-phase_sbref.nii.gz
      sub-01_task-cuedSGT_part-phase_sbref.json
```

Some meta information about the acquisition MUST be provided in an additional
JSON file.

### Required fields

| **Key name**   | **Requirement level** | **Data type**            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| -------------- | --------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| RepetitionTime | REQUIRED              | [number][]               | The time in seconds between the beginning of an acquisition of one volume and the beginning of acquisition of the volume following it (TR). When used in the context of functional acquisitions this parameter best corresponds to [DICOM Tag 0020,0110](http://dicomlookup.com/lookup.asp?sw=Tnumber&q=(0020,0110)): the "time delta between images in a dynamic of functional set of images" but may also be found in [DICOM Tag 0018, 0080](http://dicomlookup.com/lookup.asp?sw=Tnumber&q=(0018,0080)): "the period of time in msec between the beginning of a pulse sequence and the beginning of the succeeding (essentially identical) pulse sequence". This definition includes time between scans (when no data has been acquired) in case of sparse acquisition schemes. This value MUST be consistent with the '`pixdim[4]`' field (after accounting for units stored in '`xyzt_units`' field) in the NIfTI header. This field is mutually exclusive with `VolumeTiming`. |
| VolumeTiming   | REQUIRED              | [array][] of [numbers][] | The time at which each volume was acquired during the acquisition. It is described using a list of times referring to the onset of each volume in the BOLD series. The list must have the same length as the BOLD series, and the values must be non-negative and monotonically increasing. This field is mutually exclusive with `RepetitionTime` and `DelayTime`. If defined, this requires acquisition time (TA) be defined via either `SliceTiming` or `AcquisitionDuration` be defined.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| TaskName       | REQUIRED              | [string][]               | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric (`[a-zA-Z0-9]`) characters. For example TaskName `faces n-back` will correspond to task label `facesnback`. A RECOMMENDED convention is to name resting state task using labels beginning with `rest`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |

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

-   \[ X ] --> MUST be defined
-   \[  \] --> MUST NOT be defined
-   empty cell --> MAY be specified

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

Diffusion-weighted imaging data acquired for a participant.
Currently supported image types include:

| **Name**              | `suffix` | **Description**                                                   |
|---------------------- | -------- | ----------------------------------------------------------------- |
| DWI                   | dwi      | Diffusion-weighted imaging contrast (specialized T2\* weighting). |
| Single-Band Reference | sbref    | Single-band reference for one or more multi-band `dwi` images.    |

Template:

```Text
sub-<label>/[ses-<label>/]
    dwi/
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_dwi.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_dwi.bval
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_dwi.bvec
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_dwi.json
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_sbref.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_dir-<label>][_run-<index>][_part-<label>]_sbref.json
```

If more than one run of the same acquisition and direction has been acquired, the
[`run-<index>`](../99-appendices/09-entities.md#run) key/value pair MUST be used:
`_run-1`, `_run-2`, `_run-3` (and so forth.)
When there is only one scan of a given acquisition and direction, the run key MAY be
omitted.
The [`run-<index>`](../99-appendices/09-entities.md#run) key/value pair is RECOMMENDED
to encode the splits of multipart DWI scans (see [below](#multipart-split-dwi-schemes).)

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label the user may use to
distinguish different sets of parameters.

The OPTIONAL [`dir-<label>`](../99-appendices/09-entities.md#dir)
key/value pair corresponds to a custom label the user may use to
distinguish different sets of phase-encoding directions.

**Combining multi- and single-band acquisitions**.
The single-band reference image MAY be stored with suffix `sbref` (for example,
`dwi/sub-control01_sbref.nii[.gz]`) as long as the image has no corresponding
[gradient information (`[*_]dwi.bval` and `[*_]dwi.bvec` sidecar files)](#required-gradient-orientation-information)
to be stored.

Otherwise, if some gradient information is associated to the single-band diffusion
image and a multi-band diffusion image also exists, the `acq-<label>` key/value pair
MUST be used to distinguish both images.
In such a case, two files could have the following names:
`sub-01_acq-singleband_dwi.nii.gz` and `sub-01_acq-multiband_dwi.nii.gz`.
The user is free to choose any other label than `singleband` and
`multiband`, as long as they are consistent across subjects and sessions.

### REQUIRED gradient orientation information

The REQUIRED gradient orientation information corresponding to a DWI acquisition
MUST be stored using `[*_]dwi.bval` and `[*_]dwi.bvec` pairs of files.
The `[*_]dwi.bval` and `[*_]dwi.bvec` files MAY be saved on any level of the directory structure
and thus define those values for all sessions and/or subjects in one place (see
[the inheritance principle](../02-common-principles.md#the-inheritance-principle)).

As an exception to the [common principles](../02-common-principles.md#definitions)
that parameters are constant across runs, the gradient table information (stored
within the `[*_]dwi.bval` and `[*_]dwi.bvec` files) MAY change across DWI runs.

**Gradient orientation file formats**.
The `[*_]dwi.bval` and `[*_]dwi.bvec` files MUST follow the
[FSL format](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT/UserGuide#DTIFIT):
The `[*_]dwi.bvec` file contains 3 rows with *N* space-delimited floating-point numbers
(corresponding to the *N* volumes in the corresponding NIfTI file.)
The first row contains the *x* elements, the second row contains the *y* elements and
the third row contains the *z* elements of a unit vector in the direction of the applied
diffusion gradient, where the *i*-th elements in each row correspond together to
the *i*-th volume, with `[0,0,0]` for *non-diffusion-weighted* (also called *b*=0 or *low-b*)
volumes.
Following the FSL format for the `[*_]dwi.bvec` specification, the coordinate system of
the *b* vectors MUST be defined with respect to the coordinate system defined by
the header of the corresponding `_dwi` NIfTI file and not the scanner's device
coordinate system (see [Coordinate systems](../99-appendices/08-coordinate-systems.md)).
The most relevant implication for this choice is that any rotations applied to the DWI data
also need to be applied to the *b* vectors in the `[*_]dwi.bvec` file.

Example of `[*_]dwi.bvec` file, with *N*=6, with two *b*=0 volumes in the beginning:

```Text
0 0 0.021828 -0.015425 -0.70918 -0.2465
0 0 0.80242 0.22098 -0.00063106 0.1043
0 0 -0.59636 0.97516 -0.70503 -0.96351
```

The `[*_]dwi.bval` file contains the *b*-values (in s/mm<sup>2</sup>) corresponding to the
volumes in the relevant NIfTI file), with 0 designating *b*=0 volumes, space-delimited.

Example of `[*_]dwi.bval` file, corresponding to the previous `[*_]dwi.bvec` example:

```Text
0 0 2000 2000 1000 1000
```

### Multipart (split) DWI schemes

Some MR schemes cannot be acquired directly by some scanner devices,
requiring to generate several DWI runs that were originally meant to belong
in a single one.
For instance, some GE scanners cannot collect more than &asymp;160 volumes
in a single run under fast-changing gradients, so acquiring *HCP-style*
diffusion images will require splitting the DWI scheme in several runs.
Because researchers will generally optimize the data splits, these will likely
not be able to be directly concatenated.
BIDS permits defining arbitrary groupings of these multipart scans with the
following metadata:

| **Key name**    | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                      |
| --------------- | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MultipartID     | REQUIRED              | [string][]    | A unique (per participant) label tagging DWI runs that are part of a multipart scan.                                                                                                                                 |

JSON example:

```JSON
{
  "MultipartID": "dwi_1"
}
```

For instance, if there are two phase-encoding directions (`AP`, `PA`), and
two runs each, and the intent of the researcher is that all of them are
part of a unique multipart scan, then they will tag all four runs with the
same `MultipartID` (shown at the right-hand side of the file listing):

```Text
sub-<label>/[ses-<label>/]         # MultipartID
  dwi/
    sub-1_dir-AP_run-1_dwi.nii.gz  # dwi_1
    sub-1_dir-AP_run-2_dwi.nii.gz  # dwi_1
    sub-1_dir-PA_run-1_dwi.nii.gz  # dwi_1
    sub-1_dir-PA_run-2_dwi.nii.gz  # dwi_1
```

If, conversely, the researcher wanted to store two multipart scans, one possibility
is to combine matching phase-encoding directions:

```Text
sub-<label>/[ses-<label>/]         # MultipartID
  dwi/
    sub-1_dir-AP_run-1_dwi.nii.gz  # dwi_1
    sub-1_dir-AP_run-2_dwi.nii.gz  # dwi_1
    sub-1_dir-PA_run-1_dwi.nii.gz  # dwi_2
    sub-1_dir-PA_run-2_dwi.nii.gz  # dwi_2
```

Alternatively, the researcher's intent could be combining opposed phase-encoding
runs instead:

```Text
sub-<label>/[ses-<label>/]         # MultipartID
  dwi/
    sub-1_dir-AP_run-1_dwi.nii.gz  # dwi_1
    sub-1_dir-AP_run-2_dwi.nii.gz  # dwi_2
    sub-1_dir-PA_run-1_dwi.nii.gz  # dwi_1
    sub-1_dir-PA_run-2_dwi.nii.gz  # dwi_2
```

The `MultipartID` metadata MAY be used with the
[`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair, for example:

```Text
sub-<label>/[ses-<label>/]             # MultipartID
  dwi/
    sub-1_acq-shell1_run-1_dwi.nii.gz  # dwi_1
    sub-1_acq-shell1_run-2_dwi.nii.gz  # dwi_2
    sub-1_acq-shell2_run-1_dwi.nii.gz  # dwi_1
    sub-1_acq-shell2_run-2_dwi.nii.gz  # dwi_2
```

### Other RECOMMENDED metadata

The `PhaseEncodingDirection` and `TotalReadoutTime` metadata
fields are RECOMMENDED to enable the correction of geometrical distortions
with [fieldmap information](#fieldmap-data).
See [Common metadata fields](#common-metadata-fields) for a list of
additional terms that can be included in the corresponding JSON file.

JSON example:

```JSON
{
  "PhaseEncodingDirection": "j-",
  "TotalReadoutTime": 0.095
}
```

## Arterial Spin Labeling perfusion data

Template:

```Text
sub-<label>/[ses-<label>/]
    perf/
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_asl.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_asl.json
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_aslcontext.tsv
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_dir-<label>][_run-<index>]_m0scan.json
       sub-<label>[_ses-<label>][_acq-<label>][_rec-<label>][_run-<index>]_asllabeling.jpg
```

The complete ASL time series should be stored as a 4D NIfTI file in the original acquisition order,
accompanied by two ancillary files: `*_asl.json` and `*_aslcontext.tsv`.

### `*_aslcontext.tsv`
The `*_aslcontext.tsv` table consists of a single column of labels identifying the
`volume_type` of each volume in the corresponding `*_asl.nii[.gz]` file.
Volume types are defined in the following table, based on DICOM Tag (0018,9257) `ASL Context`.
Note that the volume_types `control` and  `label` within BIDS only serve
to specify the magnetization state of the blood and thus the ASL subtraction order.
See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#which-image-is-control-and-which-is-label) for more information on `control` and  `label`.

| **volume_type** | **Definition**                                                                                                                                                                         |
|-----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| control         | The control image is acquired in the exact same way as the label image, except that the magnetization of the blood flowing into the imaging region has not been inverted.              |
| label           | The label image is acquired in the exact same way as the control image, except that the blood magnetization flowing into the imaging region has been inverted.                         |
| m0scan          | The M0 image is a calibration image, used to estimate the equilibrium magnetization of blood.                                                                                          |
| deltam          | The deltaM image is a perfusion-weighted image, obtained by the subtraction of `control` - `label`.                                                                                    |
| cbf             | The cerebral blood flow (CBF) image is produced by dividing the deltaM by the M0, quantified into `mL/100g/min` (See also [doi:10.1002/mrm.25197](https://doi.org/10.1002/mrm.25197)). |

If the `control` and `label` images are not available,
their derivative `deltam` should be stored within the `*_asl.nii[.gz]`
and specified in the `*_aslcontext.tsv` instead.
If the `deltam` is not available,
`cbf` should be stored within the `*_asl.nii[.gz]` and specified in the `*_aslcontext.tsv`.
When `cbf` is stored within the `*_asl.nii[.gz]`,
its units need to be specified in the `*_asl.json` as well.
Note that the raw images, including the `m0scan`, may also be used for quality control.
See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#_aslcontexttsv-three-possible-cases) for examples of the three possible cases, in order of decreasing preference.

### Scaling
The `*_asl.nii.gz` and `*_m0scan.nii.gz` should contain appropriately scaled data, and no additional scaling factors are allowed other than the scale slope in the respective
NIfTI headers.

### M0
The `m0scan` can either be stored inside the 4D ASL time-series NIfTI file
or as a separate NIfTI file,
depending on whether it was acquired within the ASL time-series or as a separate scan.
These and other M0 options are specified in the REQUIRED `M0Type` field of the `*_asl.json` file.
It can also be stored under `fmap/sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_m0scan.nii[.gz]`,
when the [pepolar approach](#case-4-multiple-phase-encoded-directions-pepolar) is used.

### `*_asl.json` file

Depending on the method used for ASL acquisition ((P)CASL or PASL)
different metadata fields are applicable.
Additionally, some common metadata fields are REQUIRED for the `*_asl.json`:
`MagneticFieldStrength`, `MRAcquisitionType`, `EchoTime`,
`SliceTiming` in case `MRAcquisitionType` is defined as 2D,
`RepetitionTimePreparation`, and `FlipAngle` in case `LookLocker` is `true`.
See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#summary-image-of-the-most-common-asl-sequences) for more information on the most common ASL sequences.

#### Common metadata fields applicable to both (P)CASL and PASL
| **Key name**                      | **Requirement level**                                                         | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-----------------------------------|-------------------------------------------------------------------------------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ArterialSpinLabelingType          | REQUIRED                                                                      | [string][]                             | `CASL`, `PCASL`, `PASL`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| PostLabelingDelay                 | REQUIRED                                                                      | [number][] or [array][] of [numbers][] | This is the postlabeling delay (PLD) time, in seconds, after the end of the labeling (for `(P)CASL`) or middle of the labeling pulse (for `PASL`) until the middle of the excitation pulse applied to the imaging slab (for 3D acquisition) or first slice (for 2D acquisition).  Can be a number (for a single-PLD time series) or an array of numbers (for multi-PLD and Look-Locker). In the latter case, the array of numbers contains the PLD of each volume, namely each `control` and `label`, in the acquisition order. Any image within the time-series without a PLD, for example an `m0scan`, is indicated by a zero. Based on DICOM Tags 0018,9079 `Inversion Times` and 0018,0082 `InversionTime`. |
| BackgroundSuppression             | REQUIRED                                                                      | [boolean][]                            | Boolean indicating if background suppression is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| M0Type                            | REQUIRED                                                                      | [string][]                             | Describes the presence of M0 information, as either: `Separate` when a separate `*_m0scan.nii[.gz]` is present, `Included` when an m0scan volume is contained within the current `*_asl.nii[.gz]`, `Estimate` when a single whole-brain M0 value is provided, or `Absent` when no specific M0 information is present.                                                                                                                                                                                                                                                                                                                                                                                           |
| VascularCrushing                  | RECOMMENDED                                                                   | [boolean][]                            | Boolean indicating if Vascular Crushing is used. Corresponds to DICOM Tag 0018,9259 `ASL Crusher Flag`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| AcquisitionVoxelSize              | RECOMMENDED                                                                   | [array][] of [numbers][]               | An array of numbers with a length of 3, in millimeters. This parameter denotes the original acquisition voxel size, excluding any inter-slice gaps and before any interpolation or resampling within reconstruction or image processing. Any point spread function effects, for example due to T2-blurring, that would decrease the effective resolution are not considered here.                                                                                                                                                                                                                                                                                                                               |
| M0Estimate                        | OPTIONAL, but REQUIRED when `M0Type` is defined as `Estimate`                 | [number][]                             | A single numerical whole-brain M0 value (referring to the M0 of blood), only if obtained externally (for example retrieved from CSF in a separate measurement).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| TotalAcquiredVolumes              | OPTIONAL, but RECOMMENDED when not all 3D volumes are provided by the scanner | [array][] of [numbers][]               | The original number of 3D volumes acquired for each volume defined in the `*_aslcontext.tsv`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| BackgroundSuppressionNumberPulses | OPTIONAL, RECOMMENDED if `BackgroundSuppression` is `true`                    | [number][]                             | The number of background suppression pulses used. Note that this excludes any effect of background suppression pulses applied before the labeling.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| BackgroundSuppressionPulseTime    | OPTIONAL, RECOMMENDED if `BackgroundSuppression` is `true`                    | [array][] of [numbers][]               | Array of numbers containing timing, in seconds, of the background suppression pulses with respect to the start of the labeling. In case of multi-PLD with different background suppression pulse times, only the pulse time of the first PLD should be defined.                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| VascularCrushingVENC              | OPTIONAL, RECOMMENDED if `VascularCrushing` is `true`                         | [number][] or [array][] of [numbers][] | The crusher gradient strength, in centimeters per second. Specify either one number for the total time-series, or provide an array of numbers, for example when using QUASAR, using the value zero to identify volumes for which `VascularCrushing` was turned off. Corresponds to DICOM Tag 0018,925A `ASL Crusher Flow Limit`.                                                                                                                                                                                                                                                                                                                                                                                |
| LabelingOrientation               | RECOMMENDED                                                                   | [array][] of [numbers][]               | Orientation of the labeling plane (`(P)CASL`) or slab (`PASL`). The direction cosines of a normal vector perpendicular to the ASL labeling slab or plane with respect to the patient. Corresponds to DICOM Tag 0018,9255 `ASL Slab Orientation`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| LabelingDistance                  | RECOMMENDED                                                                   | [number][]                             | Distance from the center of the imaging slab to the center of the labeling plane (`(P)CASL`) or the leading edge of the labeling slab (`PASL`), in millimeters. If the labeling is performed inferior to the isocenter, this number should be negative. Based on DICOM macro C.8.13.5.14.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| LabelingLocationDescription       | RECOMMENDED                                                                   | [string][]                             | Description of the location of the labeling plane (`(P)CASL`) or the labeling slab (`PASL`) that cannot be captured by fields ‘LabelingOrientation’ or ‘LabelingDistance’. May include a link to an anonymized screenshot of the planning of the labeling slab/plane with respect to the imaging slab or slices `*_asllabeling.jpg`. Based on DICOM macro C.8.13.5.14.                                                                                                                                                                                                                                                                                                                                          |
| LookLocker                        | OPTIONAL                                                                      | [boolean][]                            | Boolean indicating if a Look-Locker readout is used.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| LabelingEfficiency                | OPTIONAL                                                                      | [number][]                             | Labeling efficiency, specified as a number between zero and one, only if obtained externally (for example phase-contrast based).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

#### (P)CASL-specific metadata fields
These fields can only be used when `ArterialSpinLabelingType` is `CASL` or `PCASL`. See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#pcasl-sequence) for more information on the (P)CASL sequence and the Labeling Pulse fields.

| **Key name**                 | **Requirement level**                            | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
|------------------------------|--------------------------------------------------|----------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| LabelingDuration             | REQUIRED                                         | [number][] or [array][] of [numbers][] | Total duration of the labeling pulse train, in seconds, corresponding to the temporal width of the labeling bolus for `(P)CASL`. In case all control-label volumes (or deltam or CBF) have the same `LabelingDuration`, a scalar must be specified. In case the control-label volumes (or deltam or cbf) have a different `LabelingDuration`, an array of numbers must be specified, for which any `m0scan` in the timeseries has a `LabelingDuration` of zero. In case an array of numbers is provided, its length should be equal to the number of volumes specified in `*_aslcontext.tsv`. Corresponds to DICOM Tag 0018,9258 `ASL Pulse Train Duration`. |
| PCASLType                    | RECOMMENDED if ArterialSpinLabelingType is PCASL | [string][]                             | Type the gradient pulses used in the `control` condition: `balanced` or `unbalanced`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| CASLType                     | RECOMMENDED if ArterialSpinLabelingType is CASL  | [string][]                             | Describes if a separate coil is used for labeling: `single-coil` or `double-coil`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| LabelingPulseAverageGradient | RECOMMENDED                                      | [number][]                             | The average labeling gradient, in milliteslas per meter.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| LabelingPulseMaximumGradient | RECOMMENDED                                      | [number][]                             | The maximum amplitude of the gradient switched on during the application of the labeling RF pulse(s), in milliteslas per meter.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| LabelingPulseAverageB1       | RECOMMENDED                                      | [number][]                             | The average B1-field strength of the RF labeling pulses, in microteslas. As an alternative, `LabelingPulseFlipAngle` can be provided.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| LabelingPulseDuration        | RECOMMENDED                                      | [number][]                             | Duration of the individual labeling pulses, in milliseconds.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| LabelingPulseFlipAngle       | RECOMMENDED                                      | [number][]                             | The flip angle of a single labeling pulse, in degrees, which can be given as an alternative to `LabelingPulseAverageB1`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| LabelingPulseInterval        | RECOMMENDED                                      | [number][]                             | Delay between the peaks of the individual labeling pulses, in milliseconds.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |

#### PASL-specific metadata fields
These fields can only be used when `ArterialSpinLabelingType` is `PASL`. See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#pasl-sequence) for more information on the PASL sequence and the BolusCutOff fields.

| **Key name**          | **Requirement level**                             | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|-----------------------|---------------------------------------------------|----------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| BolusCutOffFlag       | REQUIRED                                          | [boolean][]                            | Boolean indicating if a bolus cut-off technique is used. Corresponds to DICOM Tag 0018,925C `ASL Bolus Cut-off Flag`.                                                                                                                                                                                                                                                                                                                                   |
| PASLType              | RECOMMENDED                                       | [string][]                             | Type of the labeling pulse of the `PASL` labeling, for example FAIR, EPISTAR, or PICORE.                                                                                                                                                                                                                                                                                                                                                                |
| LabelingSlabThickness | RECOMMENDED                                       | [number][]                             | Thickness of the labeling slab in millimeters. For non-selective FAIR a zero is entered. Corresponds to DICOM Tag 0018,9254 `ASL Slab Thickness`.                                                                                                                                                                                                                                                                                                       |
| BolusCutOffDelayTime  | OPTIONAL, REQUIRED if `BolusCutOffFlag` is `true` | [number][] or [array][] of [numbers][] | Duration between the end of the labeling and the start of the bolus cut-off saturation pulse(s), in seconds. This can be a number or array of numbers, of which the values must be non-negative and monotonically increasing, depending on the number of bolus cut-off saturation pulses. For Q2TIPS, only the values for the first and last bolus cut-off saturation pulses are provided. Based on DICOM Tag 0018,925F `ASL Bolus Cut-off Delay Time`. |
| BolusCutOffTechnique  | OPTIONAL, REQUIRED if `BolusCutOffFlag` is `true` | [string][]                             | Name of the technique used, for example Q2TIPS, QUIPSS, QUIPSSII. Corresponds to DICOM Tag 0018,925E `ASL Bolus Cut-off Technique`.                                                                                                                                                                                                                                                                                                                     |

### `m0scan` metadata fields

Some common metadata fields are REQUIRED for the `*_m0scan.json`: `EchoTime`, `RepetitionTimePreparation`, and `FlipAngle` in case `LookLocker` is `true`.

| **Key name**         | **Requirement level** | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                   |
|----------------------|-----------------------|----------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| IntendedFor          | REQUIRED              | [string][] or [array][] of [strings][] | One or more filenames with paths relative to the subject subfolder, with forward slashes, referring to ASL time series for which the `*_m0scan.nii[.gz]` is intended.                                                                                                                                                                                                             |
| AcquisitionVoxelSize | RECOMMENDED           | [array][] of [numbers][]               | An array of numbers with a length of 3, in millimeters. This parameter denotes the original acquisition voxel size, excluding any inter-slice gaps and before any interpolation or resampling within reconstruction or image processing. Any point spread function effects, for example due to T2-blurring, that would decrease the effective resolution are not considered here. |

The following table recapitulates the ASL field dependencies. If Source field (column 1) contains the Value specified in column 2, then the Requirements in column 4 are
imposed on the Dependent fields in column 3. See [Appendix XII](../99-appendices/12-arterial-spin-labeling.md#flowchart-based-on-dependency-table) for this information in the
form of flowcharts.

| **Source field**         | **Value**    | **Dependent field**  | **Requirements**                                 |
|--------------------------|--------------|----------------------|--------------------------------------------------|
| MRAcquisitionType        | 2D / 3D      | SliceTiming          | \[X\] / \[\]                                     |
| LookLocker               | true         | FlipAngle            | \[X\]                                            |
| ArterialSpinLabelingType | PCASL        | LabelingDuration     | \[X\]                                            |
| ArterialSpinLabelingType | PASL         | BolusCutOffFlag      | \[X\]                                            |
| BolusCutOffFlag          | true / false | BolusCutOffDelayTime | \[X\] / \[\]                                     |
| BolusCutOffFlag          | true / false | BolusCutOffTechnique | \[X\] / \[\]                                     |
| M0Type                   | Separate     | */perf/              | contains `*_m0scan.nii[.gz]` and `*_m0scan.json` |
| M0Type                   | Included     | *_aslcontext.tsv     | contains m0scan                                  |
| M0Type                   | Estimate     | M0Estimate           | \[X\]                                            |
| `*_aslcontext.tsv`       | cbf          | Units                | \[X\]                                            |

**Legend**

-   \[ X ] --> MUST be defined
-   \[   \] --> MUST NOT be defined

## Fieldmap data

Data acquired to correct for *B<sub>0</sub>* inhomogeneities can come in different forms.
The current version of this standard considers four different scenarios:

 1. [Phase-difference map](#case-1-phase-difference-map-and-at-least-one-magnitude-image)
 1. [Two phase maps](#case-2-two-phase-maps-and-two-magnitude-images)
 1. [Direct *field mapping*](#case-3-direct-field-mapping)
 1. ["*PEpolar*" fieldmaps](#case-4-multiple-phase-encoded-directions-pepolar)

These four different types of field mapping strategies can be encoded
using the following image types:

| **Name**         | `suffix`         | **Description**                                                                                                                                                                                                      |
| ---------------- | ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Magnitude        | magnitude\[1,2\] | Field-mapping MR schemes such as gradient-recalled echo (GRE) generate a Magnitude image to be used for anatomical reference. Requires the existence of Phase, Phase-difference or Fieldmap maps.                    |
| Phase            | phase{1,2}       | Phase map generated by GRE or similar schemes, each associated with the first (`phase1`) or second (`phase2`) echoes in the sequence.                                                                                |
| Phase-difference | phasediff        | Some scanners subtract the `phase1` from the `phase2` map and generate a unique `phasediff` file. For instance, this is a common output for the built-in fieldmap sequence of Siemens scanners.                      |
| Fieldmap         | fieldmap         | Some MR schemes such as spiral-echo (SE) sequences are able to directly provide maps of the *B<sub>0</sub>* field inhomogeneity.                                                                                     |
| EPI              | epi              | The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo EPI scans with different phase encoding directions to estimate the underlying inhomogeneity/deformation map.                          |

Two OPTIONAL entities, following more general rules of the specification,
are allowed across all the four scenarios:

  - The OPTIONAL [`run-<index>`](../99-appendices/09-entities.md#run) key/value pair corresponds to a one-based index
    to distinguish multiple fieldmaps with the same parameters.

  - The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair corresponds to a custom label
    the user may use to distinguish different set of parameters.

### Types of fieldmaps

#### Case 1: Phase-difference map and at least one magnitude image

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.json
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude1.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude2.nii[.gz]  # OPTIONAL
```

where
the REQUIRED `_phasediff` image corresponds to the phase-drift map between echo times,
the REQUIRED `_magnitude1` image corresponds to the shorter echo time, and
the OPTIONAL `_magnitude2` image to the longer echo time.

Required fields:

| **Key name**   | **Requirement level** | **Data type**            | **Description**                                             |
| -------------- | --------------------- | ------------------------ | ----------------------------------------------------------- |
| EchoTime1      | REQUIRED              | [number][]               | The time (in seconds) when the first (shorter) echo occurs. |
| EchoTime2      | REQUIRED              | [number][]               | The time (in seconds) when the second (longer) echo occurs. |

In this particular case, the sidecar JSON file
`sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.json`
MUST define the time of two echos used to map the phase and finally calculate
the phase-difference map.
For example:

```JSON
{
   "EchoTime1": 0.00600,
   "EchoTime2": 0.00746
}
```

#### Case 2: Two phase maps and two magnitude images
Similar to case 1, but instead of a precomputed phase-difference map, two
separate phase images and two magnitude images corresponding to first and
second echos are available.

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

Required fields:

| **Key name**   | **Requirement level** | **Data type**            | **Description**                                                                   |
| -------------- | --------------------- | ------------------------ | --------------------------------------------------------------------------------- |
| EchoTime       | REQUIRED              | [number][]               | The time (in seconds) when the echo corresponding to this phase map was acquired. |

Each phase map has a corresponding sidecar JSON file to specify its corresponding `EchoTime`.
For example, `sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase2.json` may read:

```JSON
{
   "EchoTime": 0.00746
}
```

#### Case 3: Direct *field mapping*
In some cases (for example GE), the scanner software will directly reconstruct a
*B<sub>0</sub>* field map along with a magnitude image used for anatomical reference.

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_magnitude.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_fieldmap.nii[.gz]
       sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_fieldmap.json
```

Required fields:

| **Key name**   | **Requirement level** | **Data type**            | **Description**                                                                    |
| -------------- | --------------------- | ------------------------ | ---------------------------------------------------------------------------------- |
| Units          | REQUIRED              | [string][]               | Units of the fieldmap: Hertz (`Hz`), Radians per second (`rad/s`), or Tesla (`T`). |

For example:

```JSON
{
   "Units": "rad/s",
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

#### Case 4: Multiple phase encoded directions ("pepolar")
The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo
EPI scans with different phase encoding directions to estimate the distortion
map corresponding to the nonuniformities of the *B<sub>0</sub>* field.
These `*_epi.nii[.gz]` - or `*_m0scan.nii[.gz]` for arterial spin labeling perfusion data - files can be 3D or 4D --
in the latter case, all timepoints share the same scanning parameters.
Examples of software tools using these kinds of images are FSL TOPUP,
AFNI `3dqwarp`, and SPM.

Template:

```Text
sub-<label>/[ses-<label>/]
    fmap/
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_epi.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_epi.json
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_m0scan.nii[.gz]
        sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_m0scan.json
```

The [`dir-<label>`](../99-appendices/09-entities.md#dir) entity is REQUIRED
for these files.
This key-value pair MUST be used in addition to
the REQUIRED `PhaseEncodingDirection` metadata field
(see [File name structure](../02-common-principles.md#file-name-structure)).

Required fields:

| **Key name**           | **Requirement level** | **Data type** | **Description**                                                                    |
| ---------------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------- |
| PhaseEncodingDirection | REQUIRED              | [string][]    | See [in-plane spatial encoding](#in-plane-spatial-encoding) table of fields.       |
| TotalReadoutTime       | REQUIRED              | [number][]    | See [in-plane spatial encoding](#in-plane-spatial-encoding) table of fields.       |

For example:

```JSON
{
   "PhaseEncodingDirection": "j-",
   "TotalReadoutTime": 0.095,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

As for other EPI sequences, these field mapping sequences may have any of the
[in-plane spatial encoding](#in-plane-spatial-encoding) metadata keys.
However, please note that `PhaseEncodingDirection` and `TotalReadoutTime` keys
are REQUIRED for these field mapping sequences.

### Expressing the MR protocol intent for fieldmaps

Fieldmaps are typically acquired with the purpose of correcting one or more EPI
scans under `func/` or `dwi/` for distortions derived from *B<sub>0</sub>*
nonuniformity.
This linking between fieldmaps and their targetted data MAY be encoded with the
`IntendedFor` metadata.

#### Using `IntendedFor` metadata

Fieldmap data MAY be linked to the specific scan(s) it was acquired for by
filling the `IntendedFor` field in the corresponding JSON file.

| **Key name** | **Requirement level** | **Data type**                         | **Description**                                                                                                                                                                                                                                                                 |
| ------------ | --------------------- | ------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IntendedFor  | RECOMMENDED           | [string][] or [array][] of [string][] | Contains one or more filenames with paths relative to the participant subfolder. The path needs to use forward slashes instead of backward slashes. This field is OPTIONAL, and in case the fieldmaps do not correspond to any particular scans, it does not have to be filled. |

For example:

```JSON
{
   "IntendedFor": [
        "ses-pre/func/sub-01_ses-pre_task-motor_run-1_bold.nii.gz",
        "ses-pre/func/sub-01_ses-pre_task-motor_run-2_bold.nii.gz"
    ]
}
```

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
