# Intracranial Electroencephalography

Support Intracranial Electroencephalography (iEEG) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Several [example iEEG datasets](https://github.com/bids-standard/bids-examples#ieeg-datasets)
have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

## iEEG recording data

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   datatypes=["ieeg"],
   suffixes=["ieeg", "events", "physio", "stim"])
}}

The iEEG community uses a variety of formats for storing raw data, and there is
no single standard that all researchers agree on. For BIDS, iEEG data MUST be
stored in one of the following formats:

| **Format**                                                                                   | **Extension(s)**         | **Description**                                                                                                                                                            |
| -------------------------------------------------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [European data format](https://www.edfplus.info/)                                            | `.edf`                   | Each recording consists of a `.edf` single file. [`edf+`](https://www.edfplus.info/specs/edfplus.html) files are permitted. The capital `.EDF` extension MUST NOT be used. |
| [BrainVision Core Data Format](https://www.brainproducts.com/productdetails.php?id=21&tab=5) | `.vhdr`, `.vmrk`, `.eeg` | Each recording consists of a  `.vhdr`, `.vmrk`, `.eeg` file triplet.                                                                                                       |
| [EEGLAB](https://sccn.ucsd.edu/eeglab)                                                       | `.set`, `.fdt`           | The format used by the MATLAB toolbox [EEGLAB](https://sccn.ucsd.edu/eeglab). Each recording consists of a `.set` file with an optional `.fdt` file.                       |
| [Neurodata Without Borders](https://nwb-schema.readthedocs.io)                               | `.nwb`                   | Each recording consists of a single `.nwb` file.                                                                                                                           |
| [MEF3](https://osf.io/e3sf9/)                                                                | `.mefd`                  | Each recording consists of a `.mefd` directory.                                                                                                                            |

It is RECOMMENDED to use the European data format, or the BrainVision data
format. It is furthermore discouraged to use the other accepted formats over
these RECOMMENDED formats, particularly because there are conversion scripts
available in most commonly used programming languages to convert data into the
RECOMMENDED formats.

Future versions of BIDS may extend this list of supported file formats. File
formats for future consideration MUST have open access documentation, MUST have
open source implementation for both reading and writing in at least two
programming languages and SHOULD be widely supported in multiple software
packages. Other formats that may be considered in the future should have a clear
added advantage over the existing formats and should have wide adoption in the
BIDS community.

The data format in which the data was originally stored is especially valuable
in case conversion elicits the loss of crucial metadata specific to
manufacturers and specific iEEG systems. We also encourage users to provide
additional meta information extracted from the manufacturer-specific data files
in the sidecar JSON file. Other relevant files MAY be included alongside the
original iEEG data in the [`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data).

Note the RecordingType, which depends on whether the data stream on disk is interrupted or not.
Continuous data is by definition 1 segment without interruption.
Epoched data consists of multiple segments that all have the same length
(for example, corresponding to trials) and that have gaps in between.
Discontinuous data consists of multiple segments of different length,
for example due to a pause in the acquisition.

### Terminology: Electrodes vs. Channels

For proper documentation of iEEG recording metadata it is important to
understand the difference between electrode and channel: an iEEG electrode
is placed on or in the brain, whereas a channel is the combination of the analog
differential amplifier and analog-to-digital converter that result in a
potential (voltage) difference that is stored in the iEEG dataset. We employ the
following short definitions:

-   Electrode = A single point of contact between the acquisition system and the
    recording site (for example, scalp, neural tissue, ...). Multiple electrodes can be
    organized as arrays, grids, leads, strips, probes, shafts, caps (for EEG),
    and so forth.

-   Channel = A single analog-to-digital converter in the recording system that
    regularly samples the value of a transducer, which results in the signal
    being represented as a time series in the digitized data. This can be
    connected to two electrodes (to measure the potential difference between
    them), a magnetic field or magnetic gradient sensor, temperature sensor,
    accelerometer, and so forth.

Although the _reference_ and _ground_ electrodes are often referred to as
channels, they are in most common iEEG systems not recorded by themselves.
Therefore they are not represented as channels in the data. The type of
referencing for all channels and optionally the location of the reference
electrode and the location of the ground electrode MAY be specified.

### Sidecar JSON (`*_ieeg.json`)

For consistency between studies and institutions, we encourage users to extract
the values of metadata fields from the actual raw data. Whenever possible,
please avoid using ad hoc wording.

Generic fields MUST be present:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "TaskName": ("REQUIRED", "A RECOMMENDED convention is to name resting state task using labels beginning with `rest`."),
   }
) }}

Note that the `TaskName` field does not have to be a "behavioral task" that subjects perform, but can reflect some information about the conditions present when the data was acquired (for example, `"rest"`, `"sleep"`, or `"seizure"`).

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "InstitutionName": "RECOMMENDED",
      "InstitutionAddress": "RECOMMENDED",
      "InstitutionalDepartmentName": "RECOMMENDED",
      "Manufacturer": ("RECOMMENDED", 'For example, `"TDT"`, `"Blackrock"`.'),
      "ManufacturersModelName": "RECOMMENDED",
      "SoftwareVersions": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "Instructions": ("RECOMMENDED", "This is especially important in context of resting state recordings and distinguishing between eyes open and eyes closed paradigms."),
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
   }
) }}

Specific iEEG fields MUST be present:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "iEEGReference": "REQUIRED",
      "SamplingFrequency": ("REQUIRED", "The sampling frequency of data channels that deviate from the main sampling frequency SHOULD be specified in the `channels.tsv` file."),
      "PowerLineFrequency": "REQUIRED",
      "SoftwareFilters": "REQUIRED",
   }
) }}

Specific iEEG fields SHOULD be present:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "DCOffsetCorrection": "DEPRECATED",
      "HardwareFilters": "RECOMMENDED",
      "ElectrodeManufacturer": "RECOMMENDED",
      "ElectrodeManufacturersModelName": "RECOMMENDED",
      "ECOGChannelCount": "RECOMMENDED",
      "SEEGChannelCount": "RECOMMENDED",
      "EEGChannelCount": "RECOMMENDED",
      "EOGChannelCount": "RECOMMENDED",
      "ECGChannelCount": "RECOMMENDED",
      "EMGChannelCount": "RECOMMENDED",
      "MiscChannelCount": "RECOMMENDED",
      "TriggerChannelCount": "RECOMMENDED",
      "RecordingDuration": "RECOMMENDED",
      "RecordingType": "RECOMMENDED",
      "EpochLength": "RECOMMENDED",
      "iEEGGround": "RECOMMENDED",
      "iEEGPlacementScheme": "RECOMMENDED",
      "iEEGElectrodeGroups": "RECOMMENDED",
      "SubjectArtefactDescription": "RECOMMENDED",
   }
) }}

Specific iEEG fields MAY be present:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "ElectricalStimulation": "OPTIONAL",
      "ElectricalStimulationParameters": "OPTIONAL",
   }
) }}

Example:

```JSON
{
  "TaskName":"visual",
  "InstitutionName":"Stanford Hospital and Clinics",
  "InstitutionAddress":"300 Pasteur Dr, Stanford, CA 94305",
  "Manufacturer":"Tucker Davis Technologies",
  "ManufacturersModelName":"n/a",
  "TaskDescription":"visual gratings and noise patterns",
  "Instructions":"look at the dot in the center of the screen and press the button when it changes color",
  "iEEGReference":"left mastoid",
  "SamplingFrequency":1000,
  "PowerLineFrequency":60,
  "SoftwareFilters":"n/a",
  "HardwareFilters":{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dBOctave"}},
  "ElectrodeManufacturer":"AdTech",
  "ECOGChannelCount":120,
  "SEEGChannelCount":0,
  "EEGChannelCount":0,
  "EOGChannelCount":0,
  "ECGChannelCount":0,
  "EMGChannelCount":0,
  "MiscChannelCount":0,
  "TriggerChannelCount":0,
  "RecordingDuration":233.639,
  "RecordingType":"continuous",
  "iEEGGround":"placed on the right mastoid",
  "iEEGPlacementScheme":"right occipital temporal surface",
  "ElectricalStimulation":false
}
```

Note that the date and time information SHOULD be stored in the Study key file
([`scans.tsv`](../03-modality-agnostic-files.md#scans-file)).
Date time information MUST be expressed as indicated in [Units](../02-common-principles.md#units)

## Channels description (`*_channels.tsv`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["ieeg"], suffixes=["channels"]) }}

A channel represents one time series recorded with the recording system
(for example, there can be a bipolar channel, recorded from two electrodes or contact points on the tissue).
Although this information can often be extracted from the iEEG recording,
listing it in a simple `.tsv` document makes it easy to browse or search
(for example, searching for recordings with a sampling frequency of >=1000 Hz).
Hence, the `channels.tsv` file is RECOMMENDED.
Channels SHOULD appear in the table in the same order they do in the iEEG data file.
Any number of additional columns MAY be provided to provide additional information about the channels.
Note that electrode positions SHOULD NOT be added to this file but to `*_electrodes.tsv`.

The columns of the channels description table stored in `*_channels.tsv` are:

MUST be present **in this specific order**:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "name__channels": ("REQUIRED", "When a corresponding electrode is specified in `_electrodes.tsv`, "
                         "the name of that electrode MAY be specified here and the reference electrode "
                         "name MAY be provided in the `reference` column."),
      "type__channels": "REQUIRED",
      "units": "REQUIRED",
      "low_cutoff": "REQUIRED",
      "high_cutoff": "REQUIRED",
   }
) }}

SHOULD be present:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "reference__ieeg": "OPTIONAL",
      "group": ("OPTIONAL", "Note that any groups specified in `_electrodes.tsv` must match those present here."),
      "sampling_frequency": "OPTIONAL",
      "description": "OPTIONAL",
      "notch": "OPTIONAL",
      "status": "OPTIONAL",
      "status_description": "OPTIONAL",
   }
) }}

**Example** `sub-01_channels.tsv`:

```Text
name  type  units low_cutoff  high_cutoff status  status_description
LT01  ECOG  uV    300         0.11        good    n/a
LT02  ECOG  uV    300         0.11        bad     broken
H01   SEEG  uV    300         0.11        bad     line_noise
ECG1  ECG   uV    n/a         0.11        good    n/a
TR1   TRIG  n/a   n/a         n/a         good    n/a
```

Restricted keyword list for field type in alphabetic order (shared with the MEG
and EEG modality; however, only types that are common in iEEG data are listed here).
Note that upper-case is REQUIRED:

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
| TRIG        | System Triggers                                                        |
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

Example of free-form text for field `description`:

-   intracranial, stimulus, response, vertical EOG, skin conductance

## Electrode description (`*_electrodes.tsv`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["ieeg"], suffixes=["electrodes"]) }}

File that gives the location, size and other properties of iEEG electrodes. Note
that coordinates are expected in cartesian coordinates according to the
`iEEGCoordinateSystem` and `iEEGCoordinateUnits` fields in
`*_coordsystem.json`. If an `*_electrodes.tsv` file is specified, a
`*_coordsystem.json` file MUST be specified as well.

The optional [`space-<label>`](../99-appendices/09-entities.md#space) entity (`*[_space-<label>]_electrodes.tsv`) can be used to
indicate the way in which electrode positions are interpreted.
The space `<label>` MUST be taken from one of the modality specific lists in
[Appendix VIII](../99-appendices/08-coordinate-systems.md).
For example for iEEG data, the restricted keywords listed under
[iEEG Specific Coordinate Systems](../99-appendices/08-coordinate-systems.md#ieeg-specific-coordinate-systems)
are acceptable for `<label>`.

For examples:

-   `_space-MNI152Lin` (electrodes are coregistred and scaled to a specific MNI
    template)

-   `_space-Talairach` (electrodes are coregistred and scaled to Talairach
    space)

When referring to the `*_electrodes.tsv` file in a certain _space_ as defined
above, the [`space-<label>`](../99-appendices/09-entities.md#space) of the accompanying `*_coordsystem.json` MUST
correspond.

For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "sub-01_space-Talairach_electrodes.tsv": "",
      "sub-01_space-Talairach_coordsystem.json": "",
      "...": "",
      },
   }
) }}

The order of the required columns in the `*_electrodes.tsv` file MUST be as listed below.
The `x`, `y`, and `z` columns indicate the positions of the center of each electrode in Cartesian coordinates.
Units are specified in `space-<label>_coordsystem.json`.

MUST be present **in this specific order**:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "name__electrodes": "REQUIRED",
      "x": "REQUIRED",
      "y": "REQUIRED",
      "z": ("REQUIRED", "If electrodes are in 2D space this should be a column of `n/a` values."),
      "size": "REQUIRED",
   }
) }}

SHOULD be present:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "material": "RECOMMENDED",
      "manufacturer": "RECOMMENDED",
      "group": ("RECOMMENDED", "Note that any group specified here should match a group specified in `_channels.tsv`."),
      "hemisphere": "RECOMMENDED",
   }
) }}

MAY be present:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "type__electrodes": "OPTIONAL",
      "impedance": "OPTIONAL",
      "dimension": "OPTIONAL",
   }
) }}

Example:

```Text
name  x   y    z    size   manufacturer
LT01  19  -39  -16  2.3    Integra
LT02  23  -40  -19  2.3    Integra
H01   27  -42  -21  5      AdTech
```

## Coordinate System JSON (`*_coordsystem.json`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["ieeg"], suffixes=["coordsystem"]) }}

This `_coordsystem.json` file contains the coordinate system in which electrode
positions are expressed. The associated MRI, CT, X-Ray, or operative photo can
also be specified.

General fields:

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
         "If only a surface reconstruction is available, this should point to "
         "the surface reconstruction file. "
         "Note that this file should have the same coordinate system "
         "specified in `iEEGCoordinateSystem`. "
         "For example, **T1**: `'sub-<label>/ses-<label>/anat/"
         "sub-01_T1w.nii.gz'`  "
         "**Surface**: `'/derivatives/surfaces/sub-<label>/ses-<label>/anat/"
         "sub-01_hemi-R_desc-T1w_pial.surf.gii'` "
         "**Operative photo**: `'/sub-<label>/ses-<label>/ieeg/"
         "sub-0001_ses-01_acq-photo1_photo.jpg'` "
         "**Talairach**: `'/derivatives/surfaces/sub-Talairach/ses-01/anat/"
         "sub-Talairach_hemi-R_pial.surf.gii'`",
      )
   }
) }}

Fields relating to the iEEG electrode positions:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "iEEGCoordinateSystem": "REQUIRED",
      "iEEGCoordinateUnits": "REQUIRED",
      "iEEGCoordinateSystemDescription": 'RECOMMENDED, but REQUIRED if `iEEGCoordinateSystem` is `"Other"`',
      "iEEGCoordinateProcessingDescription": "RECOMMENDED",
      "iEEGCoordinateProcessingReference": "RECOMMENDED",
   }
) }}

### Recommended 3D coordinate systems

It is preferred that electrodes are localized in a 3D coordinate system (with
respect to a pre- and/or post-operative anatomical MRI or CT scans or in a
standard space as specified in BIDS [Appendix VIII](../99-appendices/08-coordinate-systems.md)
about preferred names of coordinate systems, such as ACPC).

### Allowed 2D coordinate systems

If electrodes are localized in 2D space (only x and y are specified and z is `"n/a"`),
then the positions in this file MUST correspond to the locations expressed
in pixels on the photo/drawing/rendering of the electrodes on the brain.
In this case, `iEEGCoordinateSystem` MUST be defined as `"Pixels"`,
and `iEEGCoordinateUnits` MUST be defined as `"pixels"`
(note the difference in capitalization).
Furthermore, the coordinates MUST be (row,column) pairs,
with (0,0) corresponding to the upper left pixel and (N,0) corresponding to the lower left pixel.

### Multiple coordinate systems

If electrode positions are known in multiple coordinate systems (for example, MRI, CT
and MNI), these spaces can be distinguished by the optional [`space-<label>`](../99-appendices/09-entities.md#space)
field, see the [`*_electrodes.tsv`-section](#electrode-description-_electrodestsv)
for more information.
Note that the [`space-<label>`](../99-appendices/09-entities.md#space) fields must correspond
between `*_electrodes.tsv` and `*_coordsystem.json` if they refer to the same
data.

Example:

```json
{
    "IntendedFor": "/sub-01/ses-01/anat/sub-01_T1w.nii.gz",
    "iEEGCoordinateSystem": "ACPC",
    "iEEGCoordinateUnits": "mm",
    "iEEGCoordinateSystemDescription": "Coordinate system with the origin at anterior commissure (AC), negative y-axis going through the posterior commissure (PC), z-axis going to a mid-hemisperic point which lies superior to the AC-PC line, x-axis going to the right",
    "iEEGCoordinateProcessingDescription": "surface_projection",
    "iEEGCoordinateProcessingReference": "Hermes et al., 2010 JNeuroMeth"
}
```

## Photos of the electrode positions (`*_photo.jpg`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["ieeg"], suffixes=["photo"]) }}

These can include photos of the electrodes on the brain surface, photos of
anatomical features or landmarks (such as sulcal structure), and fiducials. Photos
can also include an X-ray picture, a flatbed scan of a schematic drawing made
during surgery, or screenshots of a brain rendering with electrode positions.
The photos may need to be cropped and/or blurred to conceal identifying features
or entirely omitted prior to sharing, depending on obtained consent.

If there are photos of the electrodes, the [`acq-<label>`](../99-appendices/09-entities.md#acq) entity should be specified
with:

-   `*_photo.jpg` in case of an operative photo

-   `*_acq-xray#_photo.jpg` in case of an x-ray picture

-   `*_acq-drawing#_photo.jpg` in case of a drawing or sketch of electrode
    placements

-   `*_acq-render#_photo.jpg` in case of a rendering

The [`ses-<label>`](../99-appendices/09-entities.md#ses) entity may be used to specify when the photo was taken.

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

Below is an example of a volume rendering of the cortical surface with a
superimposed subdural electrode implantation. This map is often provided by the

EEG technician and provided to the epileptologists (for example, see Burneo JG et al.
2014. [doi:10.1016/j.clineuro.2014.03.020](https://doi.org/10.1016/j.clineuro.2014.03.020)).

```Text
    sub-0002_ses-01_acq-render_photo.jpg
```

![volume rendering of the cortical surface](images/ieeg_electrodes2.png "volume rendering of the cortical surface")

## Electrical stimulation

In case of electrical stimulation of brain tissue by passing current through the
iEEG electrodes, and the electrical stimulation has an event structure (on-off,
onset, duration), the `_events.tsv` file can contain the electrical stimulation
parameters in addition to other events. Note that these can be intermixed with
other task events. Electrical stimulation parameters can be described in columns
called `electrical_stimulation_<label>`, with labels chosen by the researcher and
optionally defined in more detail in an accompanying `_events.json` file (as
per the main BIDS spec). Functions for complex stimulation patterns can, similar
as when a video is presented, be stored in a directory in the `/stimuli/` directory.
For example: `/stimuli/electrical_stimulation_functions/biphasic.tsv`

Example:

```Text
onset duration trial_type             electrical_stimulation_type electrical_stimulation_site electrical_stimulation_current
1.2   0.001    electrical_stimulation biphasic                    LT01-LT02                   0.005
1.3   0.001    electrical_stimulation biphasic                    LT01-LT02                   0.005
2.2   0.001    electrical_stimulation biphasic                    LT02-LT03                   0.005
4.2   1        electrical_stimulation complex                     LT02-LT03                   n/a
15.2  3        auditory_stimulus      n/a                         n/a                         n/a
```

<!-- Link Definitions -->
