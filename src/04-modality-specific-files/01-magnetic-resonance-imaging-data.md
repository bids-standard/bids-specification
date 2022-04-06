# Magnetic Resonance Imaging

## Common metadata fields

MR Data described in the following sections share the following RECOMMENDED metadata
fields (stored in sidecar JSON files).
MRI acquisition parameters are divided into several categories based on
"A checklist for fMRI acquisition methods reporting in the literature"
([article](https://winnower-production.s3.amazonaws.com/papers/977/v4/pdf/977-a-checklist-for-fmri-acquisition-methods-reporting-in-the-literature.pdf),
[checklist](https://winnower-production.s3.amazonaws.com/papers/977/assets/993e199d-6bc3-4418-be3a-f620af1188b7-Parameter_Reporting_V1p3.pdf))
by Ben Inglis.

### Scanner Hardware

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Manufacturer": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 0070 `Manufacturer`."),
      "ManufacturersModelName": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 1090 `Manufacturers Model Name`."),
      "DeviceSerialNumber": ("RECOMMENDED", "Corresponds to DICOM Tag 0018, 1000 `DeviceSerialNumber`."),
      "StationName": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 1010 `Station Name`."),
      "SoftwareVersions": ("RECOMMENDED", "Corresponds to DICOM Tag 0018, 1020 `Software Versions`."),
      "HardcopyDeviceSoftwareVersion": "DEPRECATED",
      "MagneticFieldStrength": "RECOMMENDED, but REQUIRED for Arterial Spin Labeling",
      "ReceiveCoilName": "RECOMMENDED",
      "ReceiveCoilActiveElements": (
         "RECOMMENDED",
         "See an example below the table.",
      ),
      "GradientSetType": "RECOMMENDED",
      "MRTransmitCoilSequence": "RECOMMENDED",
      "MatrixCoilMode": "RECOMMENDED",
      "CoilCombinationMethod": "RECOMMENDED",
   }
) }}

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

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "PulseSequenceType": "RECOMMENDED",
      "ScanningSequence": "RECOMMENDED",
      "SequenceVariant": "RECOMMENDED",
      "ScanOptions": "RECOMMENDED",
      "SequenceName": "RECOMMENDED",
      "PulseSequenceDetails": "RECOMMENDED",
      "NonlinearGradientCorrection": "RECOMMENDED, but REQUIRED if [PET](./09-positron-emission-tomography.md) data are present",
      "MRAcquisitionType": "RECOMMENDED, but REQUIRED for Arterial Spin Labeling",
      "MTState": "RECOMMENDED",
      "MTOffsetFrequency": "RECOMMENDED if the MTstate is `True`.",
      "MTPulseBandwidth": "RECOMMENDED if the MTstate is `True`.",
      "MTNumberOfPulses": "RECOMMENDED if the MTstate is `True`.",
      "MTPulseShape": "RECOMMENDED if the MTstate is `True`.",
      "MTPulseDuration": "RECOMMENDED if the MTstate is `True`.",
      "SpoilingState": "RECOMMENDED",
      "SpoilingType": "RECOMMENDED if the SpoilingState is `True`.",
      "SpoilingRFPhaseIncrement": 'RECOMMENDED if the SpoilingType is `"RF"` or `"COMBINED"`.',
      "SpoilingGradientMoment": 'RECOMMENDED if the SpoilingType is `"GRADIENT"` or `"COMBINED"`.',
      "SpoilingGradientDuration": 'RECOMMENDED if the SpoilingType is `"GRADIENT"` or `"COMBINED"`.',
   }
) }}

### In-Plane Spatial Encoding

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "NumberShots": "RECOMMENDED",
      "ParallelReductionFactorInPlane": "RECOMMENDED",
      "ParallelAcquisitionTechnique": "RECOMMENDED",
      "PartialFourier": "RECOMMENDED",
      "PartialFourierDirection": "RECOMMENDED",
      "PhaseEncodingDirection": (
         "RECOMMENDED",
         "This parameter is REQUIRED if corresponding fieldmap data is present "
         "or when using multiple runs with different phase encoding directions "
         "(which can be later used for field inhomogeneity correction).",
      ),
      "EffectiveEchoSpacing": (
         "RECOMMENDED",
         "<sup>2</sup> This parameter is REQUIRED if corresponding fieldmap data is present.",
      ),
      "TotalReadoutTime": (
         "RECOMMENDED",
         "<sup>3</sup> This parameter is REQUIRED if corresponding 'field/distortion' maps "
         "acquired with opposing phase encoding directions are present "
         "(see [Case 4: Multiple phase encoded "
         "directions](#case-4-multiple-phase-encoded-directions-pepolar)).",
      ),
      "MixingTime": "RECOMMENDED",
   }
) }}

<sup>2</sup>Conveniently, for Siemens data, this value is easily obtained as
`1 / (BWPPPE * ReconMatrixPE)`, where BWPPPE is the
"BandwidthPerPixelPhaseEncode" in DICOM Tag 0019, 1028 and ReconMatrixPE is
the size of the actual reconstructed data in the phase direction (which is NOT
reflected in a single DICOM Tag for all possible aforementioned scan
manipulations). See [here](https://lcni.uoregon.edu/kb-articles/kb-0003) and
[here](https://github.com/neurolabusc/dcm_qa/tree/master/In/TotalReadoutTime)

<sup>3</sup>We use the time between the center of the first "effective" echo
and the center of the last "effective" echo, sometimes called the "FSL definition".

### Timing Parameters

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "EchoTime": "RECOMMENDED, but REQUIRED if corresponding fieldmap data is present, or the data comes from a multi echo sequence or Arterial Spin Labeling",
      "InversionTime": "RECOMMENDED",
      "SliceTiming": "RECOMMENDED, but REQUIRED for sparse sequences that do not have the `DelayTime` field set, and Arterial Spin Labeling with `MRAcquisitionType` set on `2D`.",
      "SliceEncodingDirection": "RECOMMENDED",
      "DwellTime": "RECOMMENDED",
   }
) }}

### RF & Contrast

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "FlipAngle": "RECOMMENDED, but REQUIRED if `LookLocker` is set `true`",
      "NegativeContrast": "OPTIONAL",
   }
) }}

### Slice Acceleration

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "MultibandAccelerationFactor": "RECOMMENDED",
   }
) }}

### Anatomical landmarks

Useful for multimodal co-registration with MEG, (S)EEG, TMS, and so on.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "AnatomicalLandmarkCoordinates__mri": "RECOMMENDED",
   }
) }}

### Echo-Planar Imaging and *B<sub>0</sub>* mapping

Echo-Planar Imaging (EPI) schemes typically used in the acquisition of
diffusion and functional MRI may also be *intended for* estimating the
*B<sub>0</sub>* field nonuniformity inside the scanner (in other words,
*mapping the field*) without the acquisition of additional MRI schemes
such as gradient-recalled echo (GRE) sequences that are stored under the
`fmap/` directory of the BIDS structure.

The modality labels `dwi` (under `dwi/`), `bold` (under `func/`),
`asl` (under `perf/`), `sbref` (under `dwi/`, `func/` or `perf/`), and
any modality under `fmap/` are allowed to encode the MR protocol intent for
fieldmap estimation using the following metadata:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "B0FieldIdentifier": "RECOMMENDED",
      "B0FieldSource": "RECOMMENDED",
   }
) }}

### Institution information

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "InstitutionName": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 0080 `InstitutionName`."),
      "InstitutionAddress": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 0081 `InstitutionAddress`."),
      "InstitutionalDepartmentName": ("RECOMMENDED", "Corresponds to DICOM Tag 0008, 1040 `Institutional Department Name`.")
   }
) }}

When adding additional metadata please use the CamelCase version of
[DICOM ontology terms](https://scicrunch.org/scicrunch/interlex/dashboard)
whenever possible. See also
[recommendations on JSON files](../02-common-principles.md#keyvalue-files-dictionaries).

## Anatomy imaging data

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["anat"]) }}

Currently supported non-parametric structural MR images include:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "T1w",
         "T2w",
         "PDw",
         "T2starw",
         "FLAIR",
         "inplaneT1",
         "inplaneT2",
         "PDT2",
         "UNIT1",
         "angio",
      ]
   )
}}

If the structural images included in the dataset were defaced (to protect
identity of participants) one MAY provide the binary mask that was used to
remove facial features in the form of `_defacemask` files.
In such cases,  the OPTIONAL [`mod-<label>`](../99-appendices/09-entities.md#mod)
key/value pair corresponds to modality suffix,
such as T1w or inplaneT1, referenced by the defacemask image.
For example, `sub-01_mod-T1w_defacemask.nii.gz`.

If several scans with the same acquisition parameters are acquired in the same session,
they MUST be indexed with the [`run-<index>`](../99-appendices/09-entities.md#run) entity:
`_run-1`, `_run-2`, `_run-3`, and so on (only nonnegative integers are allowed as
run labels).

If different entities apply,
such as a different session indicated by [`ses-<label>`](../99-appendices/09-entities.md#ses),
or different acquisition parameters indicated by
[`acq-<label>`](../99-appendices/09-entities.md#acq),
then `run` is not needed to distinguish the scans and MAY be omitted.

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq)
key/value pair corresponds to a custom label the user
MAY use to distinguish a different set of parameters used for acquiring the same
modality. For example this should be used when a study includes two T1w images -
one full brain low resolution and one restricted field of view but high
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

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "ContrastBolusIngredient": "OPTIONAL",
      "RepetitionTimeExcitation": "OPTIONAL",
      "RepetitionTimePreparation": "OPTIONAL",
   }
) }}

The [`part-<label>`](../99-appendices/09-entities.md#part) key/value pair is
used to indicate which component of the complex representation of the MRI
signal is represented in voxel data.
This entity is associated with the DICOM Tag `0008, 9208`.
Allowed label values for this entity are `phase`, `mag`, `real` and `imag`,
which are typically used in `part-mag`/`part-phase` or `part-real`/`part-imag`
pairs of files.
For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "anat": {
         "sub-01_part-mag_T1w.nii.gz": "",
         "sub-01_part-mag_T1w.json": "",
         "sub-01_part-phase_T1w.nii.gz": "",
         "sub-01_part-phase_T1w.json": "",
         },
      }
   }
) }}

Phase images MAY be in radians or in arbitrary units.
The sidecar JSON file MUST include the units of the `phase` image.
The possible options are `rad` or `arbitrary`.

For example, for `sub-01_part-phase_T1w.json`:

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

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "T1map",
         "R1map",
         "T2map",
         "R2map",
         "T2starmap",
         "R2starmap",
         "PDmap",
         "MTRmap",
         "MTsat",
         "T1rho",
         "MWFmap",
         "MTVmap",
         "PDT2map",
         "Chimap",
         "TB1map",
         "RB1map",
         "S0map",
         "M0map",
      ]
   )
}}

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

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "T2star",
         "FLASH",
         "PD",
      ]
   )
}}

## Task (including resting state) imaging data

Currently supported image contrasts include:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "bold",
         "cbv",
         "phase",
      ]
   )
}}

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["func"]) }}

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

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz": "",
         "sub-01_task-cuedSGT_run-1_echo-1_bold.json": "",
         "sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz": "",
         "sub-01_task-cuedSGT_run-1_echo-2_bold.json": "",
         "sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz": "",
         "sub-01_task-cuedSGT_run-1_echo-3_bold.json": "",
         },
      }
   }
) }}

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

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-cuedSGT_part-mag_bold.nii.gz": "",
         "sub-01_task-cuedSGT_part-mag_bold.json": "",
         "sub-01_task-cuedSGT_part-phase_bold.nii.gz": "",
         "sub-01_task-cuedSGT_part-phase_bold.json": "",
         "sub-01_task-cuedSGT_part-mag_sbref.nii.gz": "",
         "sub-01_task-cuedSGT_part-mag_sbref.json": "",
         "sub-01_task-cuedSGT_part-phase_sbref.nii.gz": "",
         "sub-01_task-cuedSGT_part-phase_sbref.json": "",
         },
      },
   }
) }}

Some meta information about the acquisition MUST be provided in an additional
JSON file.

### Required fields

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "RepetitionTime": "REQUIRED",
      "VolumeTiming": "REQUIRED",
      "TaskName": ("REQUIRED", "A RECOMMENDED convention is to name resting state task using labels beginning with `rest`.")
   }
) }}

For the fields described above and in the following section, the term "Volume"
refers to a reconstruction of the object being imaged (for example, brain or part of a
brain). In case of multiple channels in a coil, the term "Volume" refers to a
combined image rather than an image from each coil.

### Other RECOMMENDED metadata

#### Timing Parameters

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "NumberOfVolumesDiscardedByScanner": "RECOMMENDED",
      "NumberOfVolumesDiscardedByUser": "RECOMMENDED",
      "DelayTime": "RECOMMENDED",
      "AcquisitionDuration": 'RECOMMENDED, but REQUIRED for sequences that are described with the `VolumeTiming` field and that do not have the `SliceTiming` field set to allow for accurate calculation of "acquisition time"',
      "DelayAfterTrigger": "RECOMMENDED",
   }
) }}

The following table recapitulates the different ways that specific fields have
to be populated for functional sequences. Note that all these options can be
used for non sparse sequences but that only options B, D and E are valid for
sparse sequences.

|          | **`RepetitionTime`** | **`SliceTiming`** | **`AcquisitionDuration`** | **`DelayTime`** | **`VolumeTiming`** |
| -------- | -------------------- | ----------------- | ------------------------- | --------------- | ------------------ |
| option A |     \[ X ]           |                   |         \[ ]              |                 |     \[ ]           |
| option B |      \[ ]            |    \[ X ]         |                           |    \[ ]         |    \[ X ]          |
| option C |      \[ ]            |                   |        \[ X ]             |    \[ ]         |    \[ X ]          |
| option D |     \[ X ]           |    \[ X ]         |         \[ ]              |                 |     \[ ]           |
| option E |     \[ X ]           |                   |         \[ ]              |   \[ X ]        |     \[ ]           |

**Legend**

-   \[ X ] --> MUST be defined
-   \[  \] --> MUST NOT be defined
-   empty cell --> MAY be specified

#### fMRI task information

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Instructions": ("RECOMMENDED", "This is especially important in context of resting state recordings and distinguishing between eyes open and eyes closed paradigms."),
      "TaskDescription": "RECOMMENDED",
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
   }
) }}

See [Common metadata fields](#common-metadata-fields) for a list of
additional terms and their definitions.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-control01_task-nback_bold.json": "",
         },
      }
   }
) }}

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
   "DeviceSerialNumber": "11035",
   "B0FieldSource": ["phasediff_fmap0", "pepolar_fmap0"]
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

Several [example datasets](https://github.com/bids-standard/bids-examples)
contain diffusion imaging data formatted using this specification
and that can be used for practical guidance when curating a new dataset:

-   [`genetics_ukbb`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)
-   [`eeg_rest_fmri`](https://github.com/bids-standard/bids-examples/tree/master/eeg_rest_fmri)
-   [`ds114`](https://github.com/bids-standard/bids-examples/tree/master/ds114)
-   [`ds000117`](https://github.com/bids-standard/bids-examples/tree/master/ds000117)

Diffusion-weighted imaging data acquired for a participant.
Currently supported image types include:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "dwi",
         "sbref",
      ]
   )
}}

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["dwi"]) }}

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
The most relevant limitation imposed by this choice is that the gradient information cannot
be directly stored in this format if the scanner generates *b*-vectors in *scanner coordinates*.

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

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "MultipartID": "REQUIRED",
   }
) }}

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

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-1": {
      "dwi                               # MultipartID": {
         "sub-1_dir-AP_run-1_dwi.nii.gz": " # dwi_1",
         "sub-1_dir-AP_run-2_dwi.nii.gz": " # dwi_1",
         "sub-1_dir-PA_run-1_dwi.nii.gz": " # dwi_1",
         "sub-1_dir-PA_run-2_dwi.nii.gz": " # dwi_1",
         }
      }
   }
) }}

If, conversely, the researcher wanted to store two multipart scans, one possibility
is to combine matching phase-encoding directions:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-1": {
      "dwi                               # MultipartID":{
            "sub-1_dir-AP_run-1_dwi.nii.gz": " # dwi_1",
            "sub-1_dir-AP_run-2_dwi.nii.gz": " # dwi_1",
            "sub-1_dir-PA_run-1_dwi.nii.gz": " # dwi_2",
            "sub-1_dir-PA_run-2_dwi.nii.gz": " # dwi_2",
      },
      }
   }
) }}

Alternatively, the researcher's intent could be combining opposed phase-encoding
runs instead:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-1": {
      "dwi                               # MultipartID":{
            "sub-1_dir-AP_run-1_dwi.nii.gz": " # dwi_1",
            "sub-1_dir-AP_run-2_dwi.nii.gz": " # dwi_2",
            "sub-1_dir-PA_run-1_dwi.nii.gz": " # dwi_1",
            "sub-1_dir-PA_run-2_dwi.nii.gz": " # dwi_2",
      },
      }
   }
) }}

The `MultipartID` metadata MAY be used with the
[`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair, for example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-1": {
      "dwi                                   # MultipartID":{
         "sub-1_acq-shell1_run-1_dwi.nii.gz": " # dwi_1",
         "sub-1_acq-shell1_run-2_dwi.nii.gz": " # dwi_2",
         "sub-1_acq-shell2_run-1_dwi.nii.gz": " # dwi_1",
         "sub-1_acq-shell2_run-2_dwi.nii.gz": " # dwi_2",
         },
      }
   }
) }}

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
  "TotalReadoutTime": 0.095,
  "B0FieldSource": ["phasediff_fmap0", "pepolar_fmap0"]
}
```

## Arterial Spin Labeling perfusion data

Several [example ASL datasets](https://github.com/bids-standard/bids-examples#asl-datasets)
have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["perf"]) }}

The complete ASL time series should be stored as a 4D NIfTI file in the original acquisition order,
accompanied by two ancillary files: `*_asl.json` and `*_aslcontext.tsv`.

### `*_aslcontext.tsv`

The `*_aslcontext.tsv` table consists of a single column of labels identifying the
`volume_type` of each volume in the corresponding `*_asl.nii[.gz]` file.
Volume types are defined in the following table, based on DICOM Tag 0018, 9257 `ASL Context`.
Note that the volume_types `control` and  `label` within BIDS only serve
to specify the magnetization state of the blood and thus the ASL subtraction order.
See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#which-image-is-control-and-which-is-label) for more information on `control` and  `label`.

| **volume_type** | **Definition**                                                                                                                                                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
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

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "ArterialSpinLabelingType": "REQUIRED",
      "PostLabelingDelay": "REQUIRED",
      "BackgroundSuppression": "REQUIRED",
      "M0Type": "REQUIRED",
      "TotalAcquiredPairs": "REQUIRED",
      "VascularCrushing": "RECOMMENDED",
      "AcquisitionVoxelSize": "RECOMMENDED",
      "M0Estimate": "OPTIONAL, but REQUIRED when `M0Type` is defined as `Estimate`",
      "BackgroundSuppressionNumberPulses": "OPTIONAL, RECOMMENDED if `BackgroundSuppression` is `true`",
      "BackgroundSuppressionPulseTime": "OPTIONAL, RECOMMENDED if `BackgroundSuppression` is `true`",
      "VascularCrushingVENC": "OPTIONAL, RECOMMENDED if `VascularCrushing` is `true`",
      "LabelingOrientation": "RECOMMENDED",
      "LabelingDistance": "RECOMMENDED",
      "LabelingLocationDescription": "RECOMMENDED",
      "LookLocker": "OPTIONAL",
      "LabelingEfficiency": "OPTIONAL",
   }
) }}

#### (P)CASL-specific metadata fields

These fields can only be used when `ArterialSpinLabelingType` is `"CASL"` or `"PCASL"`. See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#pcasl-sequence) for more information on the (P)CASL sequence and the Labeling Pulse fields.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "LabelingDuration": "REQUIRED",
      "PCASLType": 'RECOMMENDED if `ArterialSpinLabelingType` is `"PCASL"`',
      "CASLType": 'RECOMMENDED if `ArterialSpinLabelingType` is `"CASL"`',
      "LabelingPulseAverageGradient": "RECOMMENDED",
      "LabelingPulseMaximumGradient": "RECOMMENDED",
      "LabelingPulseAverageB1": "RECOMMENDED",
      "LabelingPulseDuration": "RECOMMENDED",
      "LabelingPulseFlipAngle": "RECOMMENDED",
      "LabelingPulseInterval": "RECOMMENDED",
   }
) }}

#### PASL-specific metadata fields

These fields can only be used when `ArterialSpinLabelingType` is `PASL`. See [Appendix XII - ASL](../99-appendices/12-arterial-spin-labeling.md#pasl-sequence) for more information on the PASL sequence and the BolusCutOff fields.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "BolusCutOffFlag": "REQUIRED",
      "PASLType": "RECOMMENDED",
      "LabelingSlabThickness": "RECOMMENDED",
      "BolusCutOffDelayTime": "OPTIONAL, REQUIRED if `BolusCutOffFlag` is `true`",
      "BolusCutOffTechnique": "OPTIONAL, REQUIRED if `BolusCutOffFlag` is `true`",
   }
) }}

### `m0scan` metadata fields

Some common metadata fields are REQUIRED for the `*_m0scan.json`: `EchoTime`, `RepetitionTimePreparation`, and `FlipAngle` in case `LookLocker` is `true`.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "IntendedFor": (
         "REQUIRED",
         "This is used to refer to the ASL time series for which the `*_m0scan.nii[.gz]` is intended."
      ),
      "AcquisitionVoxelSize": "RECOMMENDED",
   }
) }}

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

1.  [Phase-difference map](#case-1-phase-difference-map-and-at-least-one-magnitude-image)
1.  [Two phase maps](#case-2-two-phase-maps-and-two-magnitude-images)
1.  [Direct *field mapping*](#case-3-direct-field-mapping)
1.  ["*PEpolar*" fieldmaps](#case-4-multiple-phase-encoded-directions-pepolar)

These four different types of field mapping strategies can be encoded
using the following image types:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "magnitude",
         "magnitude1",
         "magnitude2",
         "phase1",
         "phase2",
         "phasediff",
         "fieldmap",
         "epi",
      ]
   )
}}

Two OPTIONAL entities, following more general rules of the specification,
are allowed across all the four scenarios:

-   The OPTIONAL [`run-<index>`](../99-appendices/09-entities.md#run) key/value pair corresponds to a one-based index
    to distinguish multiple fieldmaps with the same parameters.

-   The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair corresponds to a custom label
    the user may use to distinguish different set of parameters.

### Expressing the MR protocol intent for fieldmaps

Fieldmaps are typically acquired with the purpose of correcting one or more EPI
scans under `dwi/`, `func/`, or `perf/` for distortions derived from *B<sub>0</sub>*
nonuniformity.

#### Using `B0FieldIdentifier` metadata

The general purpose [`B0FieldIdentifier` MRI metadata](#echo-planar-imaging-and-b0-mapping)
is RECOMMENDED for the prescription of the *B<sub>0</sub>* field estimation intent of the
original acquisition protocol.
`B0FieldIdentifier` and `B0FieldSource` duplicate the capabilities of
the original `IntendedFor` approach (see below), while permitting more
complex use cases.
It is RECOMMENDED to use both approaches to maintain compatibility with
tools that support older datasets.

#### Using `IntendedFor` metadata

Fieldmap data MAY be linked to the specific scan(s) it was acquired for by
filling the `IntendedFor` field in the corresponding JSON file.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "IntendedFor": (
         "OPTIONAL",
         "This field is OPTIONAL, and in case the fieldmaps do not correspond "
         "to any particular scans, it does not have to be filled.",
      ),
   }
) }}

For example:

```JSON
{
   "IntendedFor": [
        "ses-pre/func/sub-01_ses-pre_task-motor_run-1_bold.nii.gz",
        "ses-pre/func/sub-01_ses-pre_task-motor_run-2_bold.nii.gz"
    ]
}
```

### Types of fieldmaps

#### Case 1: Phase-difference map and at least one magnitude image

[Example datasets](https://github.com/bids-standard/bids-examples)
containing that type of fieldmap can be found here:

-   [`7t_trt`](https://github.com/bids-standard/bids-examples/tree/master/7t_trt)
-   [`genetics_ukbb`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)
-   [`ds000117`](https://github.com/bids-standard/bids-examples/tree/master/ds000117)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["fmap"], suffixes=["phasediff", "magnitude1", "magnitude2"]) }}

where
the REQUIRED `_phasediff` image corresponds to the phase-drift map between echo times,
the REQUIRED `_magnitude1` image corresponds to the shorter echo time, and
the OPTIONAL `_magnitude2` image to the longer echo time.

Required fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "EchoTime1": "REQUIRED",
      "EchoTime2": "REQUIRED",
   }
) }}

In this particular case, the sidecar JSON file
`sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phasediff.json`
MUST define the time of two echos used to map the phase and finally calculate
the phase-difference map.
For example:

```JSON
{
   "EchoTime1": 0.00600,
   "EchoTime2": 0.00746,
   "B0FieldIdentifier": "phasediff_fmap0"
}
```

#### Case 2: Two phase maps and two magnitude images

Similar to case 1, but instead of a precomputed phase-difference map, two
separate phase images and two magnitude images corresponding to first and
second echos are available.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["fmap"], suffixes=["phase1", "phase2", "magnitude1", "magnitude2"]) }}

Required fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "EchoTime__fmap": "REQUIRED",
   }
) }}

Each phase map has a corresponding sidecar JSON file to specify its corresponding `EchoTime`.
For example, `sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_phase2.json` may read:

```JSON
{
   "EchoTime": 0.00746,
   "B0FieldIdentifier": "phases_fmap0"
}
```

#### Case 3: Direct *field mapping*
In some cases (for example GE), the scanner software will directly reconstruct a
*B<sub>0</sub>* field map along with a magnitude image used for anatomical reference.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["fmap"], suffixes=["fieldmap", "magnitude"]) }}

Required fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Units": (
         "REQUIRED",
         'Fieldmaps must be in units of Hertz (`"Hz"`), '
         'radians per second (`"rad/s"`), or Tesla (`"T"`).',
      ),
   }
) }}

For example:

```JSON
{
   "Units": "rad/s",
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz",
   "B0FieldIdentifier": "b0map_fmap0"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

#### Case 4: Multiple phase encoded directions ("pepolar")

An [example dataset](https://github.com/bids-standard/bids-examples)
containing that type of fieldmap can be found here:

-   [`ieeg_visual_multimodal`](https://github.com/bids-standard/bids-examples/tree/master/ieeg_visual_multimodal)

The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo
EPI scans with different phase encoding directions to estimate the distortion
map corresponding to the nonuniformities of the *B<sub>0</sub>* field.
These `*_epi.nii[.gz]` - or `*_m0scan.nii[.gz]` for arterial spin labeling perfusion data - files can be 3D or 4D --
in the latter case, all timepoints share the same scanning parameters.
Examples of software tools using these kinds of images are FSL TOPUP,
AFNI `3dqwarp`, and SPM.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["fmap"], suffixes=["epi"]) }}

The [`dir-<label>`](../99-appendices/09-entities.md#dir) entity is REQUIRED
for these files.
This key-value pair MUST be used in addition to
the REQUIRED `PhaseEncodingDirection` metadata field
(see [File name structure](../02-common-principles.md#file-name-structure)).

Required fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "PhaseEncodingDirection": "REQUIRED",
      "TotalReadoutTime": "REQUIRED",
   }
) }}

For example:

```JSON
{
   "PhaseEncodingDirection": "j-",
   "TotalReadoutTime": 0.095,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz",
   "B0FieldIdentifier": "pepolar_fmap0"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

As for other EPI sequences, these field mapping sequences may have any of the
[in-plane spatial encoding](#in-plane-spatial-encoding) metadata keys.
However, please note that `PhaseEncodingDirection` and `TotalReadoutTime` keys
are REQUIRED for these field mapping sequences.

<!-- Link Definitions -->
