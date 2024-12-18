# Electromyography

Support for Electromyography (EMG) was developed as a
[BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit
this extension when referring to it in the context of the academic literature.

!!! example "Example datasets"

    Electromyography datasets formatted according to this specification are available on
    the [BIDS examples repository](https://github.com/bids-standard/bids-examples#emg)
    and can be emulated when curating new datasets.

## EMG data

{{ MACROS___make_filename_template(
"raw",
datatypes=["emg"],
suffixes=["motion", "channels", "events"])
}}

The EMG community uses a variety of formats for storing raw data, and there is
no single standard that all researchers agree on. For BIDS, EMG data MUST be
stored in one of the following formats:

| **Format**                                        | **Extension(s)**         | **Description**                                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [European data format](https://www.edfplus.info/) | `.edf`                   | Each recording consists of a single `.edf` file. [`edf+`](https://www.edfplus.info/specs/edfplus.html) files are permitted. The capital `.EDF` extension MUST NOT be used.                           |
| TODO OTHER ALLOWED (VENDOR-SPECIFIC?) FORMAT(S)?  | `.TODO`                  | TODO.                                                                                                                                                                                                |

It is RECOMMENDED to use the European data format.
It is furthermore discouraged to use the other accepted formats over this RECOMMENDED format,
particularly because there are conversion scripts available in most commonly used
programming languages to convert data into the RECOMMENDED format.

Future versions of BIDS may extend this list of supported file formats.
File formats for future consideration MUST have open access documentation, MUST have
open source implementation for both reading and writing in at least two programming
languages and SHOULD be widely supported in multiple software packages.
Other formats that may be considered in the future should have a clear added advantage
over the existing formats and should have wide adoption in the BIDS community.

We encourage users to provide additional metadata extracted from the
manufacturer-specific data files in the sidecar JSON file.

Note the RecordingType, which depends on whether the data stream on disk is interrupted or not.
Continuous data is by definition 1 segment without interruption.

Epoched data consists of multiple segments that all have the same length
(for example, corresponding to trials) and that have gaps in between.
Discontinuous data consists of multiple segments of different length,
for example due to a pause in the acquisition.

### Terminology: Electrodes vs. Channels

For proper documentation of EMG recording metadata it is important to understand the
difference between electrode and channel: an EMG electrode is a sensor placed on the
skin, whereas a channel is the combination of the analog differential amplifier and
analog-to-digital converter that result in a potential (voltage) difference that is
stored in the EMG dataset.
We employ the following short definitions:

-   Electrode = A single point of contact between the acquisition system and the
    recording site (for example, scalp, neural tissue, ...).
    Multiple electrodes can be organized as arrays, grids, leads, strips, probes,
    shafts, caps (for EEG), and so forth.

-   Channel = A single analog-to-digital converter in the recording system that
    regularly samples the value of a transducer, which results in the signal being
    represented as a time series in the digitized data.
    This can be connected to two electrodes (to measure the potential difference between
    them), a magnetic field or magnetic gradient sensor, temperature sensor,
    accelerometer, and so forth.

Although the _reference_ and _ground_ electrodes are often referred to as channels,
they are in most common EMG systems not recorded by themselves.
Therefore they are not represented as channels in the data.
The type of referencing for all channels and optionally the location of the reference
electrode and the location of the ground electrode MAY be specified.

### Sidecar JSON (`*_emg.json`)

For consistency between studies and institutions,
we encourage users to extract the values of metadata fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

Those fields MUST be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGRequired") }}

Those fields SHOULD be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGRecommended") }}

These fields MAY be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGOptional") }}

Note that the date and time information SHOULD be stored in the study key file
([`scans.tsv`](../modality-agnostic-files.md#scans-file)).
Date time information MUST be expressed as indicated in [Units](../common-principles.md#units)

#### Hardware information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGHardware") }}

#### Task information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGTaskInformation") }}

Note that the `TaskName` field does not have to be a "behavioral task" that subjects perform,
but can reflect some information about the conditions present when the data was acquired
(for example, `"treatment"`, `"control"`, or `"sleep"`).

#### Institution information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGInstitutionInformation") }}

#### Example `*_emg.json`

<!-- TODO do we need separate ElectrodeManufacturer and Manufacturer fields like iEEG? -->
<!-- TODO put in plausible hardware filters for an EMG system -->
<!-- TODO do we need TriggerChannelCount / MiscChannelCount / etc? -->
```JSON
{
  "EMGChannelCount":4,
  "EMGGround":"TODO",
  "EMGPlacementScheme":"TODO",
  "EMGReference":"TODO",
  "HardwareFilters":{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dBOctave"}},
  "InstitutionAddress":"300 Pasteur Dr, Stanford, CA 94305",
  "InstitutionName":"Stanford Hospital and Clinics",
  "Instructions":"Jump straight upward as high as you can, while keeping your arms at your sides.",
  "Manufacturer":"Delsys",
  "ManufacturersModelName":"Trigno® Galileo",
  "MiscChannelCount":0,
  "PowerLineFrequency":60,
  "RecordingDuration":123.456,
  "RecordingType":"continuous",
  "SamplingFrequency":1000,
  "SoftwareFilters":"n/a",
  "TaskDescription":"jumping with stiff arms",
  "TaskName":"jumping",
}
```

## Channels description (`*_channels.tsv`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["emg"], suffixes=["channels"]) }}

A channel represents one time series recorded with the recording system
(for example, there can be a bipolar channel, recorded from two electrodes or contact points on the tissue).
Although this information can often be extracted from the EMG recording,
listing it in a simple `.tsv` document makes it easy to browse or search
(for example, searching for recordings with a sampling frequency of >=1000 Hz).
Hence, the `channels.tsv` file is RECOMMENDED.
Channels SHOULD appear in the table in the same order they do in the EMG data file.
Any number of additional columns MAY be provided to provide additional information about the channels.
Note that electrode positions SHOULD NOT be added to this file but to `*_electrodes.tsv`.

The columns of the channels description table stored in `*_channels.tsv` are:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("emg.EMGChannels") }}

Restricted keyword list for field type in alphabetic order (shared with the MEG
and EEG modality; however, only types that are common in EMG data are listed here).
Note that upper-case is REQUIRED:
<!-- TODO what should be removed from this table? seems like EEG, ECOG, SEEG, DBS could be removed,
     and maybe PD, EYEGAZE, PUPIL too?
-->

| **Keyword** | **Description**                                                        |
| ----------- | ---------------------------------------------------------------------- |
| EEG         | Electrode channel from electroencephalogram                            |
| ECOG        | Electrode channel from electrocorticogram (intracranial)               |
| SEEG        | Electrode channel from stereo-electroencephalogram (intracranial)      |
| DBS         | Electrode channel from deep brain stimulation electrode (intracranial) |
| VEOG        | Vertical EOG (electrooculogram)                                        |
| HEOG        | Horizontal EOG                                                         |
| EOG         | Generic EOG channel if HEOG or VEOG information not available          |
| ECG         | ElectroCardioGram (heart)                                              |
| EMG         | ElectroMyoGram (muscle)                                                |
| TRIG        | Analog (TTL in Volt) or digital (binary TTL) trigger channel           |
| AUDIO       | Audio signal                                                           |
| PD          | Photodiode                                                             |
| EYEGAZE     | Eye Tracker gaze                                                       |
| PUPIL       | Eye Tracker pupil diameter                                             |
| MISC        | Miscellaneous                                                          |
| SYSCLOCK    | System time showing elapsed time since trial started                   |
| ADC         | Analog to Digital input                                                |
| DAC         | Digital to Analog output                                               |
| REF         | Reference channel                                                      |
| OTHER       | Any other type of channel                                              |

Examples of free-form text for field `description`:

-   n/a
-   stimulus
-   response
-   skin conductance
-   battery status

### Example `*_channels.tsv`

See also the corresponding [`electrodes.tsv` example](#example-electrodestsv).
<!-- TODO not yet updated after copy/paste from EEG -->
```Text
name     type  units  description                     reference     status  status_description
VEOG     VEOG  uV     left eye                        VEOG-, VEOG+  good    n/a
FDI      EMG   uV     left first dorsal interosseous  FDI-, FDI+    good    n/a
Cz       EEG   uV     n/a                             REF           bad     high frequency noise
UADC001  MISC  n/a    envelope of audio signal        n/a           good    n/a
```

## Electrodes description (`*_electrodes.tsv`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["emg"], suffixes=["electrodes"]) }}

File that gives the measured location, size, and other properties of EMG electrodes.
If an `*_electrodes.tsv` file is specified, a `*_coordsystem.json` file MUST be specified
as well.

When 3D electrode locations are digitized in situ, the origin, orientation, and measurement
unit of the coordinate system MUST be recorded in cartesian coordinates according to the
`EMGCoordinateSystem` and `EMGCoordinateUnits` fields in `*_coordsystem.json`,
as described in the [Coordinate Systems Appendix](../appendices/coordinate-systems.md).
In such cases, `EMGCoordinateSystem` SHOULD be specified as `Other` and the
`EMGCoordinateSystemDescription` SHOULD contain a description of the origin of the 3D
coordinate system.

When accurate 3D locations are unavailable, 2D locations may be provided to define the
geometry of an electrode grid or group, prior to anatomical placement.
See the [`electrodes.tsv` example](#example-electrodestsv) section for an example.
In such cases, `EMGCoordinateSystem` SHOULD be specified as `Other` and the
`EMGCoordinateSystemDescription` SHOULD contain a description of the origin of the 2D
coordinate system (for example, "origin at the center of the grid" or "origin at the
center of the electrode in the lower-left corner of the grid, when oriented with the
leads downward").
In such cases, the description in the `EMGPlacementScheme` field of `*_emg.json` MAY
refer to the origin of that 2D coordinate system in describing the placement of the grid.

The order of the required columns in the `*_electrodes.tsv` file MUST be as listed below.

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("emg.EMGElectrodes") }}

The [`acq-<label>`](../appendices/entities.md#acq) entity MUST be used to indicate
simultaneous acquisition of data from multiple EMG devices, in cases where the devices
store data in separate data files.
For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "ses-01":{
         "sub-01_ses-01_acq-RectusFemoris_electrodes.tsv": "",
         "sub-01_ses-01_acq-VastusLateralis_electrodes.tsv": "",
         "sub-01_ses-01_acq-VastusMedialis_electrodes.tsv": "",
         },
      }
   }
) }}

Above, acquisitions are labeled with the target muscle, but other schemes are also appropriate.
For example, if bipolar and grid EMG devices are used simultaneously,
acquisitions may be labeled "bipolar" and "grid", or use the device manufacturer names.

Except in cases of simultaneous acquisitions from different devices (as mentioned above),
`*_electrodes.tsv` files SHOULD NOT be duplicated for each data file, for example,
during multiple runs of a task.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate electrode positions for a given data file.
If electrodes are repositioned, it is RECOMMENDED to use multiple sessions to indicate this.

### Example `*_electrodes.tsv`

Example `*_electrodes.tsv` for a 2 by 2 grid of EMG electrodes with 2.5 mm electrode diameter
and 10 mm inter-electrode distance.

<!-- TODO should we demo other columns here too? Should we add ground/ref electrodes? -->
```Text
name  x     y     diameter
001   0.0   0.0   2.5
002   10.0  0.0   2.5
003   0.0   10.0  2.5
004   10.0  10.0  2.5
```

## Coordinate System JSON (`*_coordsystem.json`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["emg"], suffixes=["coordsystem"]) }}

This `*_coordsystem.json` file contains the coordinate system in which electrode
positions are expressed. The associated photo can also be specified.

General fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table("json.emg.EMGCoordsystemGeneral") }}

Fields relating to the EMG electrode positions:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table("json.emg.EMGCoordsystemPositions") }}

The [`acq-<label>`](../appendices/entities.md#acq) entity SHOULD be used to indicate
coordinate systems for simultaneous acquisition of data from multiple EMG devices,
in cases where the devices store data in separate data files.
Except in cases of simultaneous acquisitions from different devices (as mentioned above),
`*_coordsystem.json` files SHOULD NOT be duplicated for each data file,
for example, across multiple tasks.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate coordinate system description for a given data file.
If electrodes are repositioned, it is RECOMMENDED to use multiple sessions to indicate this.

### Recommended coordinate systems

TODO

### Multiple coordinate systems

TODO. relevant if multiple devices all run through same amplifier / end up in same data file,
but are on different sides of a joint (and thus located with respect to different skeletal landmarks).

### Example `*_coordsystem.json`

<!-- TODO not yet updated after copy/pasting from iEEG -->
```json
{
    "IntendedFor": "bids::sub-01/ses-01/anat/sub-01_T1w.nii.gz",
    "iEEGCoordinateSystem": "ACPC",
    "iEEGCoordinateUnits": "mm",
    "iEEGCoordinateSystemDescription": "Coordinate system with the origin at anterior commissure (AC), negative y-axis going through the posterior commissure (PC), z-axis going to a mid-hemisperic point which lies superior to the AC-PC line, x-axis going to the right",
    "iEEGCoordinateProcessingDescription": "surface_projection",
    "iEEGCoordinateProcessingReference": "Hermes et al., 2010 JNeuroMeth"
}
```

## Photos of the electrode positions (`*_photo.<extension>`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["emg"], suffixes=["photo"]) }}

Photos of the electrode locations are OPTIONAL.
Photos SHOULD include sufficient surrounding context to distinguish anatomical location.
For example, photographs of electrodes on the limbs should include at least one adjacent joint.
Photos may need to be cropped and/or blurred to conceal identifying features
or entirely omitted prior to dataset distribution, depending on obtained consent.

If there are photos of the electrodes, the [`acq-<label>`](../appendices/entities.md#acq) entity
MAY be specified, if separate photos are provided of each EMG device.
The [`ses-<label>`](../appendices/entities.md#ses) entity may be used to specify when the photo was taken.

### Example `*_photo.<extension>`

<!-- TODO not yet updated after copy/paste from iEEG -->
Example of the operative photo of ECoG electrodes (here is an annotated example in
which electrodes and vasculature are marked, taken from Hermes et al.,
JNeuroMeth 2010).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "ses-0001": {
         "sub-0001_ses-01_acq-photo1_photo.jpg": "",
         "sub-0001_ses-01_acq-photo2_photo.jpg": "",
         "...": "",
         },
      },
   }
) }}

![operative photo of ECoG electrodes](images/ieeg_electrodes1.png "operative photo of ECoG electrodes")
