# Magnetic Resonance Imaging

## Common metadata fields

MR Data described in the following sections share the following RECOMMENDED metadata
fields (stored in sidecar JSON files).
MRI acquisition parameters are divided into several categories based on
"A checklist for fMRI acquisition methods reporting in the literature"
([article](https://doi.org/10.15200/winn.143191.17127)) by Ben Inglis.

When adding additional metadata please use the CamelCase version of
[DICOM ontology terms](https://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_d.html)
whenever possible. See also
[recommendations on JSON files](../common-principles.md#key-value-files-dictionaries).

### Hardware information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRIHardware") }}

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
that a given scan was collected with the intended coil elements selected.

### Institution information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRIInstitutionInformation") }}

### Sequence Specifics

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRISequenceSpecifics") }}

### In- and Out-of-Plane Spatial Encoding

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["mri.MRISpatialEncoding", "mri.PhaseEncodingDirectionRec"]) }}

<sup>2</sup>Conveniently, for Siemens data, this value is easily obtained as
`1 / (BWPPPE * ReconMatrixPE)`, where BWPPPE is the
"BandwidthPerPixelPhaseEncode" in [DICOM Tag 0019, 1028](https://dicomlookup.com/dicomtags/(0019,1028)) and ReconMatrixPE is
the size of the actual reconstructed data in the phase direction (which is NOT
reflected in a single DICOM Tag for all possible aforementioned scan
manipulations). See
[Acquiring and using field maps - LCNI](https://lcni.uoregon.edu/wiki/acquiring-and-using-field-maps/)
and [TotalReadoutTime - dcm\_qa](https://github.com/neurolabusc/dcm_qa/tree/master/In/TotalReadoutTime).

<sup>3</sup>We use the time between the center of the first "effective" echo
and the center of the last "effective" echo, sometimes called the "FSL definition".

### Timing Parameters

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["mri.MRITimingParameters", "mri.SliceTimingMRI"]) }}

### RF & Contrast

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["mri.MRIFlipAngleLookLockerFalse", "mri.MRIRFandContrast" ]) }}

### Slice Acceleration

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRISliceAcceleration") }}

### Anatomical landmarks

Useful for multimodal co-registration with MEG, (S)EEG, TMS, and so on.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRIAnatomicalLandmarks") }}

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
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
     "mri.MRIB0FieldIdentifier",
     "mri.MRIEchoPlanarImagingAndB0FieldSource",
   ])
}}

### Tissue description

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRISample") }}

### Deidentification information

Describes the mechanism or method used to modify or remove metadata
and/or pixel data to protect the patient or participant's identity.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.DeidentificationMethod") }}

Each object in the `DeidentificationMethodCodeSequence` array includes the following RECOMMENDED keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.DeidentificationMethodCodeSequence.items") }}

## Anatomy imaging data

Anatomy MRI sequences measure static, structural features of the brain.

This datatype is divided into two groups:
non-parametric and parametric.

Non-parametric structural images have an arbitrary scale.
For example, T1w data are T1-weighted,
but the values do not correspond to actual T1 value estimates.

Parametric structural imaging, on the other hand, use a non-arbitrary scale.
For example, a T1map file contains T1 value estimates, in seconds.

### Non-parametric structural MR images

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["anat"], suffixes=[
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
      ])
}}

Currently supported non-parametric structural MR images include the following:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
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

The [`part-<label>`](../appendices/entities.md#part) entity is
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
)
}}

Phase images MAY be in radians or in arbitrary units.
The sidecar JSON file MUST include the units of the `phase` image.
The possible options are `rad` or `arbitrary`.

For example, for `sub-01_part-phase_T1w.json`:

```Text
{
   "Units": "rad"
}
```

When there is only a magnitude image of a given type, the `part` entity MAY be omitted.

### Parametric structural MR images

Structural MR images whose intensity is represented in a non-arbitrary scale
constitute parametric maps.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["anat"], suffixes=[
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
         "Chimap",
         "TB1map",
         "RB1map",
         "S0map",
         "M0map",
      ])
}}

Parametric images listed in the table below are typically generated by
processing a [file collection](../common-principles.md#entity-linked-file-collections).
Please visit the [file collections appendix](../appendices/file-collections.md) to see the
list of suffixes available for quantitative MRI (qMRI) applications associated
with these maps
(for example, [MPM](../glossary.md#mpm-suffixes),
[MP2RAGE](../glossary.md#mp2rage-suffixes),
and [MTR](../glossary.md#mtransfer-entities)).

Currently supported parametric maps include:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
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
         "Chimap",
         "TB1map",
         "RB1map",
         "S0map",
         "M0map",
      ]
   )
}}

For any other details on the organization of parametric maps, their
recommended metadata fields, and the application specific entity or
metadata requirement levels of [file collections](../appendices/file-collections.md) that can generate
them, visit the [qMRI appendix](../appendices/qmri.md).

### Defacing masks

If the structural images included in the dataset were defaced (to protect
identity of participants) one MAY provide the binary mask that was used to
remove facial features in the form of `_defacemask` files.
In such cases, the OPTIONAL [`mod-<label>`](../appendices/entities.md#mod)
entity corresponds to modality suffix,
such as `T1w` or `inplaneT1`, referenced by the defacemask image.
For example, `sub-01_mod-T1w_defacemask.nii.gz`.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["anat"], suffixes=[
         "defacemask",
      ])
}}

### Task metadata for anatomical scans

The OPTIONAL [`task-<label>`](../appendices/entities.md#task) entity can be used
in order to allow tasks during structural MR acquisitions,
for example pre-described motion paradigms such as nodding, to be described.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("anat.TaskMetadata") }}

Some meta information about the acquisition MAY be provided in an additional
JSON file. See [Common metadata fields](#common-metadata-fields) for a
list of terms and their definitions. There are also some OPTIONAL JSON
fields specific to anatomical scans:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("anat.MRIAnatomyCommonMetadataFields") }}

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
  src/schema/rules/files/raw
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
  src/schema/rules/files/raw
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
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["func"]) }}

Functional imaging consists of techniques that support rapid temporal repetition.
This includes, but is not limited to, task based fMRI, as well as resting state fMRI, which is treated like any other task.
For task based fMRI, a corresponding task events file (see below) MUST be provided
(please note that this file is not necessary for resting state scans).
For multiband acquisitions, one MAY also save the single-band reference image with the `sbref` suffix
(for example, `sub-control01_task-nback_sbref.nii.gz`).

Multi-echo data MUST be split into one file per echo using the
[`echo-<index>`](../appendices/entities.md#echo) entity. For example:

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
(`_phase`) data, but the `_phase` suffix is [deprecated](../common-principles.md#definitions).
Newly generated datasets SHOULD NOT use the `_phase` suffix, and the suffix will be removed
from the specification in the next major release.
For backwards compatibility, `_phase` is considered equivalent to `_part-phase_bold`.
When the `_phase` suffix is not used, each file shares the same
name with the exception of the `part-<mag|phase>` or `part-<real|imag>` entity.

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

Some meta information about the acquisition MUST be provided in an additional JSON file.

### Required fields

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "func.MRIFuncRepetitionTime",
       "func.MRIFuncVolumeTiming",
       "func.MRIFuncRequired",
   ])
}}

For the fields described above and in the following section, the term "Volume"
refers to a reconstruction of the object being imaged (for example, brain or part of a
brain). In case of multiple channels in a coil, the term "Volume" refers to a
combined image rather than an image from each coil.

### Other RECOMMENDED metadata

#### Timing Parameters

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("func.MRIFuncTimingParameters") }}

The following table recapitulates the different ways that specific fields have
to be populated for functional sequences. Note that all these options can be
used for non sparse sequences but that only options B, D and E are valid for
sparse sequences.

|          | **`RepetitionTime`** | **`SliceTiming`** | **`AcquisitionDuration`** | **`DelayTime`** | **`VolumeTiming`** |
| -------- | -------------------- | ----------------- | ------------------------- | --------------- | ------------------ |
| option A | \[ X ]               |                   | \[ ]                      |                 | \[ ]               |
| option B | \[ ]                 | \[ X ]            |                           | \[ ]            | \[ X ]             |
| option C | \[ ]                 |                   | \[ X ]                    | \[ ]            | \[ X ]             |
| option D | \[ X ]               | \[ X ]            | \[ ]                      |                 | \[ ]               |
| option E | \[ X ]               |                   | \[ ]                      | \[ X ]          | \[ ]               |

**Legend**

-   \[ X ] --> MUST be defined
-   \[  \] --> MUST NOT be defined
-   empty cell --> MAY be specified

#### fMRI task information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("func.MRIFuncTaskInformation") }}

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
         "sub-01_task-nback_bold.json": "",
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

## Diffusion imaging data

!!! example "Example datasets"

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
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(["dwi", "sbref"]) }}

Additionally, the following suffixes are used for scanner-generated images:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(["ADC", "expADC", "trace", "FA", "colFA", "S0map"]) }}

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["dwi"]) }}

The [`run-<index>`](../appendices/entities.md#run) entity is RECOMMENDED
to encode the splits of multipart DWI scans
(see [below](#multipart-split-dwi-schemes) for more information on multipart DWI schemes).

**Combining multi- and single-band acquisitions**.
The single-band reference image MAY be stored with suffix `sbref` (for example,
`dwi/sub-control01_sbref.nii[.gz]`) as long as the image has no corresponding
[gradient information (`[*_]dwi.bval` and `[*_]dwi.bvec` sidecar files)](#required-gradient-orientation-information)
to be stored.

Otherwise, if some gradient information is associated to the single-band diffusion
image and a multi-band diffusion image also exists, the `acq-<label>` entity
MUST be used to distinguish both images.
In such a case, two files could have the following names:
`sub-01_acq-singleband_dwi.nii.gz` and `sub-01_acq-multiband_dwi.nii.gz`.
The user is free to choose any other label than `singleband` and
`multiband`, as long as they are consistent across subjects and sessions.

Scanner-generated derivative images,
such as trace-weighted, ADC, exponentiated ADC,
fractional anisotropy (FA and colFA), and estimated unweighted signal intensity,
MAY be included using the `trace`, `ADC`, `expADC`, `FA`, `colFA` and `S0map` suffixes, respectively.
If trace, ADC, expADC, FA, colFA, or S0 volume filenames match a diffusion series with all applicable entities,
such volumes SHOULD have been computed from that series.
Otherwise, some entity, such as [`acq-<label>`](../appendices/entities.md#acq),
SHOULD be used to indicate that the files are unrelated.

### REQUIRED gradient orientation information

The REQUIRED gradient orientation information corresponding to a DWI acquisition
MUST be stored using `[*_]dwi.bval` and `[*_]dwi.bvec` pairs of files.
The `[*_]dwi.bval` and `[*_]dwi.bvec` files MAY be saved on any level of the directory structure
and thus define those values for all sessions and/or subjects in one place (see
[the inheritance principle](../common-principles.md#the-inheritance-principle)).

As an exception to the [common principles](../common-principles.md#definitions)
that parameters are constant across runs, the gradient table information (stored
within the `[*_]dwi.bval` and `[*_]dwi.bvec` files) MAY change across DWI runs.

**Gradient orientation file formats**.
The `[*_]dwi.bval` and `[*_]dwi.bvec` files MUST follow the
[FSL format](https://fsl.fmrib.ox.ac.uk/fsl/docs/#/diffusion/index?id=diffusion-data-in-fsl).

The `[*_]dwi.bvec` file contains 3 rows with *N* space-delimited floating-point numbers,
corresponding to the *N* volumes in the corresponding NIfTI file.
Across these three rows,
each column encodes three elements of a 3-vector for the corresponding image volume;
each vector MUST be either of unit norm,
or optionally the vector `[0.0,0.0,0.0]`
for *non-diffusion-weighted* (also called *b*=0 or *low-b*) volumes.
These values are to be interpreted as cosine values with respect to the image axis orientations
as defined by the corresponding NIfTI image header transformation;
*unless* the image axes defined in the corresponding NIfTI image header
form a right-handed coordinate system
(that is, the 3x3 matrix of direction cosines has a positive determinant),
in which case the sign of the first element of each 3-vector must be inverted
for this interpretation to be valid.
Note that this definition of orientations with respect to the NIfTI image axes
is *not* equivalent to the DICOM convention,
where orientations are instead defined with respect to the scanner device's coordinate system
(see [Coordinate systems](../appendices/coordinate-systems.md)).

The `[*_]dwi.bval` file contains the *b*-values (in s/mm<sup>2</sup>)
corresponding to the volumes in the relevant NIfTI file,
with 0 designating *b*=0 volumes; space-delimited.

Examples of `[*_]dwi.bvec` and `[*_]dwi.bval` files,
corresponding to a NIfTI image with 6 volumes
with the first two volumes having no diffusion sensitization:

-   `[*_]dwi.bvec`:
    ```Text
    0 0 0.021828 -0.015425 -0.70918 -0.2465
    0 0 0.80242 0.22098 -0.00063106 0.1043
    0 0 -0.59636 0.97516 -0.70503 -0.96351
    ```

-   `[_]dwi.bval`:
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
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("dwi.MRIDiffusionMultipart") }}

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
[`acq-<label>`](../appendices/entities.md#acq) entity, for example:

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

!!! example "Example datasets"

    Several [example ASL datasets](https://bids-standard.github.io/bids-examples/#asl)
    have been formatted using this specification
    and can be used for practical guidance when curating a new dataset.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["perf"]) }}

The complete ASL time series should be stored as a 4D NIfTI file in the original acquisition order,
accompanied by two ancillary files: `*_asl.json` and `*_aslcontext.tsv`.

### `*_aslcontext.tsv`

The `*_aslcontext.tsv` table consists of a single column of labels identifying the
`volume_type` of each volume in the corresponding `*_asl.nii[.gz]` file.
Volume types are defined in the following table, based on [DICOM Tag 0018, 9257](https://dicomlookup.com/dicomtags/(0018,9257)) `ASL Context`.
Note that the volume_types `control` and  `label` within BIDS only serve
to specify the magnetization state of the blood and thus the ASL subtraction order.
See the [ASL Appendix](../appendices/arterial-spin-labeling.md#which-image-is-control-and-which-is-label)
for more information on `control` and  `label`.

| **volume_type** | **Definition**                                                                                                                                                                         |
| --------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `control`       | The control image is acquired in the exact same way as the label image, except that the magnetization of the blood flowing into the imaging region has not been inverted.              |
| `label`         | The label image is acquired in the exact same way as the control image, except that the blood magnetization flowing into the imaging region has been inverted.                         |
| `m0scan`        | The M0 image is a calibration image, used to estimate the equilibrium magnetization of blood.                                                                                          |
| `deltam`        | The deltaM image is a perfusion-weighted image, obtained by the subtraction of `control` - `label`.                                                                                    |
| `cbf`           | The cerebral blood flow (CBF) image is produced by dividing the deltaM by the M0, quantified into `mL/100g/min` (See also [doi:10.1002/mrm.25197](https://doi.org/10.1002/mrm.25197)). |
| `noRF`          | No radio frequency excitation (noRF) images are produced by disabling the radio frequency excitation, while maintaining all other parameters from the associated scan.                 |
| `n/a`           | In some cases, there may be volume types that are not yet supported by BIDS, or which cannot be used by tools.                                                                         |

If the `control` and `label` images are not available,
their derivative `deltam` should be stored within the `*_asl.nii[.gz]`
and specified in the `*_aslcontext.tsv` instead.
If the `deltam` is not available,
`cbf` should be stored within the `*_asl.nii[.gz]` and specified in the `*_aslcontext.tsv`.
When `cbf` is stored within the `*_asl.nii[.gz]`,
its units need to be specified in the `*_asl.json` as well.
Note that the raw images, including the `m0scan`, may also be used for quality control.
See the [ASL Appendix](../appendices/arterial-spin-labeling.md#_aslcontexttsv-three-possible-cases)
for examples of the three possible cases, in order of decreasing preference.

### Scaling

The `*_asl.nii.gz` and `*_m0scan.nii.gz` should contain appropriately scaled data,
and no additional scaling factors are allowed other than the scale slope in the respective
NIfTI headers.

### `*_asllabeling.*`

A deidentified screenshot of the planning of the labeling slab/plane
with respect to the imaging slab or slices.
This screenshot is based on DICOM macro C.8.13.5.14.

See [`LabelingLocationDescription`](../glossary.md#labelinglocationdescription-metadata) for more details.

### M0

The `m0scan` can either be stored inside the 4D ASL time-series NIfTI file
or as a separate NIfTI file,
depending on whether it was acquired within the ASL time-series or as a separate scan.
These and other M0 options are specified in the REQUIRED `M0Type` field of the `*_asl.json` file.
It can also be stored under
`fmap/sub-<label>[_ses-<label>][_acq-<label>][_ce-<label>]_dir-<label>[_run-<index>]_m0scan.nii[.gz]`,
when the [pepolar approach](#case-4-multiple-phase-encoded-directions-pepolar) is used.

### `*_asl.json` file

Depending on the method used for ASL acquisition ((P)CASL or PASL)
different metadata fields are applicable.
Additionally, some common metadata fields are REQUIRED for the `*_asl.json`:
`MagneticFieldStrength`, `MRAcquisitionType`, `EchoTime`,
`SliceTiming` in case `MRAcquisitionType` is defined as 2D,
`RepetitionTimePreparation`, and `FlipAngle` in case `LookLocker` is `true`.
See the [ASL Appendix](../appendices/arterial-spin-labeling.md#summary-image-of-the-most-common-asl-sequences)
for more information on the most common ASL sequences.

#### Common metadata fields applicable to both (P)CASL and PASL

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["asl.MRIASLCommonMetadataFields", "asl.MRIASLCommonMetadataFieldsM0TypeRec", "asl.MRIASLCommonMetadataFieldsBackgroundSuppressionOpt", "asl.MRIASLCommonMetadataFieldsVascularCrushingOpt", ]) }}

#### (P)CASL-specific metadata fields

These fields can only be used when `ArterialSpinLabelingType` is `"CASL"` or `"PCASL"`. See the [ASL Appendix](../appendices/arterial-spin-labeling.md#pcasl-sequence) for more information on the (P)CASL sequence and the Labeling Pulse fields.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
       "asl.MRIASLPcaslSpecific",
       "asl.MRIASLCaslSpecific",
       "asl.MRIASLCaslPcaslSpecific",
   ]) }}

#### PASL-specific metadata fields

These fields can only be used when `ArterialSpinLabelingType` is `PASL`.
See the [ASL Appendix](../appendices/arterial-spin-labeling.md#pasl-sequence)
for more information on the PASL sequence and the BolusCutOff fields.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["asl.MRIASLPaslSpecific", "asl.MRIASLPASLSpecificBolusCutOffFlagFalse"]) }}

### `m0scan` metadata fields

Some common metadata fields are REQUIRED for the `*_m0scan.json`: `EchoTime`, `RepetitionTimePreparation`, and `FlipAngle` in case `LookLocker` is `true`.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("asl.MRIASLM0Scan") }}

The following table recapitulates the ASL field dependencies. If Source field (column 1) contains the Value specified in column 2, then the Requirements in column 4 are
imposed on the Dependent fields in column 3. See the [ASL Appendix](../appendices/arterial-spin-labeling.md#flowchart-based-on-dependency-table) for this information in the
form of flowcharts.

| **Source field**         | **Value**    | **Dependent field**  | **Requirements**                                 |
| ------------------------ | ------------ | -------------------- | ------------------------------------------------ |
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
  src/schema/rules/files/raw
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
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.MRIFieldmapIntendedFor") }}

For example:

```JSON
{
   "IntendedFor": [
        "bids::sub-01/ses-pre/func/sub-01_ses-pre_task-motor_run-1_bold.nii.gz",
        "bids::sub-01/ses-pre/func/sub-01_ses-pre_task-motor_run-2_bold.nii.gz"
    ]
}
```

### Types of fieldmaps

#### Case 1: Phase-difference map and at least one magnitude image

!!! example "Example datasets"

    [Example datasets](https://bids-standard.github.io/bids-examples/#dataset-index)
    containing that type of fieldmap can be found here:

    -   [`7t_trt`](https://github.com/bids-standard/bids-examples/tree/master/7t_trt)
    -   [`genetics_ukbb`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)
    -   [`ds000117`](https://github.com/bids-standard/bids-examples/tree/master/ds000117)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["fmap"], suffixes=["phasediff", "magnitude1", "magnitude2"]) }}

where
the REQUIRED `_phasediff` image corresponds to the phase-drift map between echo times,
the REQUIRED `_magnitude1` image corresponds to the shorter echo time, and
the OPTIONAL `_magnitude2` image to the longer echo time.

Required fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.MRIFieldmapPhaseDifferencePhasediff") }}

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
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["fmap"], suffixes=["phase1", "phase2", "magnitude1", "magnitude2"]) }}

Required fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.MRIFieldmapTwoPhase") }}

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
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["fmap"], suffixes=["fieldmap", "magnitude"]) }}

Required fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.MRIFieldmapDirectFieldMapping") }}

For example:

```JSON
{
   "Units": "rad/s",
   "IntendedFor": "bids::sub-01/func/sub-01_task-motor_bold.nii.gz",
   "B0FieldIdentifier": "b0map_fmap0"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

#### Case 4: Multiple phase encoded directions ("pepolar")

!!! example "Example datasets"

    An [example dataset](https://github.com/bids-standard/bids-examples)
    containing that type of fieldmap can be found here:

    -   [`ieeg_visual_multimodal`](https://github.com/bids-standard/bids-examples/tree/master/ieeg_visual_multimodal)

The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo
EPI scans with different phase encoding directions to estimate the distortion
map corresponding to the nonuniformities of the *B<sub>0</sub>* field.
These `*_epi.nii[.gz]` - or `*_m0scan.nii[.gz]` for arterial spin labeling perfusion data - files can be 3D or 4D --
in the latter case, all timepoints share the same scanning parameters.
Some 4D scans intended for correcting DWIs may have accompanying `*_epi.bval` and `*_epi.bvec` files.
Examples of software tools using these kinds of images are FSL TOPUP and
AFNI `3dqwarp`.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["fmap"], suffixes=["epi"]) }}

The [`dir-<label>`](../appendices/entities.md#dir) entity is REQUIRED
for these files.
This entity MUST be used in addition to
the REQUIRED `PhaseEncodingDirection` metadata field
(see [Filename structure](../common-principles.md#filenames)).

Required fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.MRIFieldmapPepolar") }}

For example:

```JSON
{
   "PhaseEncodingDirection": "j-",
   "TotalReadoutTime": 0.095,
   "IntendedFor": "bids::sub-01/func/sub-01_task-motor_bold.nii.gz",
   "B0FieldIdentifier": "pepolar_fmap0"
}
```

See [Using `IntendedFor` metadata](#using-intendedfor-metadata)
for details on the `IntendedFor` field.

As for other EPI sequences, these field mapping sequences may have any of the
[in-plane spatial encoding](#in-and-out-of-plane-spatial-encoding) metadata keys.
However, please note that `PhaseEncodingDirection` and `TotalReadoutTime` keys
are REQUIRED for these field mapping sequences.
