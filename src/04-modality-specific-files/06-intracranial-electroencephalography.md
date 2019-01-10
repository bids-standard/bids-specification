# intracranial Electroencephalography (iEEG)

## Citation

Support for iEEG was developed as a
[BIDS Extension Proposal](../06-extensions.md#bids-extension-proposals). Please
cite the following paper when referring to this part of the standard in context
of the academic literature:

> TODO: citation

## iEEG recording data

Template:

```Text
sub-<label>/
  [ses-<label>]/
    ieeg/
      sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>]_ieeg.<manufacturer_specific_extension>
      sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>]_ieeg.json
```

The iEEG community uses a variety of formats for storing raw data, and there is
no single standard that all researchers agree on. The allowed file formats for
iEEG data in BIDS are divided into two groups: _recommended_ formats that are
open, well-defined standards, and _accepted_ formats that are common in the
community. In general, it is discouraged to use _accepted_ formats over
_recommended_ formats, particularly because there are conversion scripts
available in most analytics languages to convert data into _recommended_
formats. Below are lists of each group of allowed data formats in BIDS-iEEG.

**Recommended Formats**

-   European Data Format (.edf) (https://www.edfplus.info/)
-   Brainvision (.vhdr/.eeg/.vmrk)
    [BrainVision data format](https://www.brainproducts.com/productdetails.php?id=21&tab=5)
    by Brain Products GmbH.

**Accepted Formats**

-   [Neurodata Without Borders](<(https://github.com/NeurodataWithoutBorders/pynwb)>)
    (.nwb)
-   [EEGLAB](https://sccn.ucsd.edu/eeglab) (`.set` and `.fdt` files)
-   [MEF3](https://github.com/msel-source) (`.mef`)
    ([paper](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4956586/),
    [specification and links](http://msel.mayo.edu/codes.html),
    [Python reader](https://www.google.com/url?q=https://github.com/ICRC-BME/PySigView&sa=D&ust=1540234072960000&usg=AFQjCNEBg8ua_qEc7U3OsK0lh-iXn94mWQ))

Future versions of BIDS may extend this list of supported file formats. File
formats for future consideration MUST have open access documentation, MUST have
open source implementation for both reading and writing in at least two
programming languages and SHOULD be widely supported in multiple software
packages. Other formats that may be considered in the future should have a clear
added advantage over the existing formats and should have wide adoption in the
BIDS-iEEG community.

The data format in which the data was originally stored is especially valuable in case conversion elicits the
loss of crucial metadata specific to manufacturers and specific iEEG systems. We
also encourage users to provide additional meta information extracted from the
manufacturer-specific data files in the sidecar JSON file. Other relevant files
MAY be included alongside the original EEG data in the
[`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data).


### Terminology: Electrodes vs. Channels

For proper documentation of iEEG recording metadata it is important to
understand the difference between electrode and channel: An EEG electrode is
attached to the skin, whereas a channel is the combination of the analog
differential amplifier and analog-to-digital converter that result in a
potential (voltage) difference that is stored in the EEG dataset. We employ the
following short definitions:

-   Electrode = A single point of contact between the acquisition system and the
    recording site (e.g., scalp, neural tissue, ...). Multiple electrodes can be
    organized as arrays, grids, leads, strips, probes, shafts, caps (for EEG),
    etc.

-   Channel = A single analog-to-digital converter in the recording system that
    regularly samples the value of a transducer, which results in the signal
    being represented as a time series in the digitized data. This can be
    connected to two electrodes (to measure the potential difference between
    them), a magnetic field or magnetic gradient sensor, temperature sensor,
    accelerometer, etc.

Although the _reference_ and _ground_ electrodes are often referred to as
channels, they are in most common iEEG systems not recorded by themselves.
Therefore they are not represented as channels in the data. The type of
referencing for all channels and optionally the location of the reference
electrode and the location of the ground electrode MAY be specified.
### Sidecar JSON document (`*_ieeg.json`)

For consistency between studies and institutions, we encourage users to extract
the values of metadata fields from the actual raw data. Whenever possible,
please avoid using ad hoc wording.

Generic fields MUST be present:

| Field name         | Definition                                                                                                                                                                                                                                                                                                                                                                                                              |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TaskName           | REQUIRED. Name of the task (for resting state use the “rest” prefix). No two tasks should have the same name. Task label is derived from this field by removing all non alphanumeric ([a-zA-Z0-9]) characters. Note this does not have to be a “behavioral task” that subjects perform, but can reflect some information about the conditions present when the data was acquired (e.g., “rest”, “sleep”, or "seizure"). |
| SamplingFrequency  | REQUIRED. Sampling frequency (in Hz) of all the iEEG channels in the recording (e.g., 2400). All other channels should have frequency specified as well in the `channels.tsv` file.                                                                                                                                                                                                                                     |
| PowerLineFrequency | REQUIRED. Frequency (in Hz) of the power grid where the iEEG recording was done (i.e., 50 or 60).                                                                                                                                                                                                                                                                                                                       |
| SoftwareFilters    | REQUIRED. List of temporal software filters applied or ideally key:value pairs of pre-applied filters and their parameter values. (n/a if none). E.g., “{'HighPass': {'HalfAmplitudeCutOffHz': 1, 'RollOff: '6dB/Octave'}}”.                                                                                                                                                                                            |

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

| Field name             | Definition                                                                                                                                                                                                                    |
| :--------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manufacturer           | RECOMMENDED. Manufacturer of the amplifier system (e.g., "TDT, Blackrock").                                                                                                                                                   |
| ManufacturersModelName | RECOMMENDED. Manufacturer’s designation of the iEEG amplifier model.                                                                                                                                                          |
| TaskDescription        | RECOMMENDED. Longer description of the task.                                                                                                                                                                                  |
| Instructions           | RECOMMENDED. Text of the instructions given to participants before the recording. This is especially important in context of resting state and distinguishing between eyes open and eyes closed paradigms.                    |
| CogAtlasID             | RECOMMENDED. URL of the corresponding [Cognitive Atlas Task](http://www.cognitiveatlas.org/) term.                                                                                                                            |
| CogPOID                | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term.                                                                                                                                                    |
| InstitutionName        | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                    |
| InstitutionAddress     | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                 |
| DeviceSerialNumber     | RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset. |

Specific iEEG fields MUST be present:

| Field name    | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| :------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| iEEGReference | REQUIRED. General description of the reference scheme used and (when applicable) of location of the reference electrode in the raw recordings (e.g., "left mastoid”, “bipolar”, “T01” for electrode with name T01, “intracranial electrode on top of a grid, not included with data”, “upside down electrode”). If different channels have a different reference, this field should have a general description and the channel specific reference should be defined in the \_channels.tsv file. |

Specific iEEG fields SHOULD be present:

| Field name                      | Definition                                                                                                                                                                                                                                                                               |
| :------------------------------ | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DCOffsetCorrection              | RECOMMENDED. A description of the method (if any) used to correct for a DC offset. If the method used was subtracting the mean value for each channel, use “mean”.                                                                                                                       |
| HardwareFilters                 | RECOMMENDED. List of hardware (amplifier) filters applied with key:value pairs of filter parameters and their values.                                                                                                                                                                    |
| ElectrodeManufacturer           | RECOMMENDED. can be used if all electrodes are of the same manufacturer (e.g., AD-TECH, DIXI). If electrodes of different manufacturers are used, please use the corresponding table in the \_electrodes.tsv file.                                                                       |
| ElectrodeManufacturersModelName | RECOMMENDED. If different electrode types are used, please use the corresponding table in the \_electrodes.tsv file.                                                                                                                                                                     |
| ECOGChannelCount                | RECOMMENDED. Number of iEEG surface channels included in the recording (e.g., 120).                                                                                                                                                                                                      |
| SEEGChannelCount                | RECOMMENDED. Number of iEEG depth channels included in the recording (e.g., 8).                                                                                                                                                                                                          |
| EEGChannelCount                 | RECOMMENDED. Number of scalp EEG channels recorded simultaneously (e.g., 21).                                                                                                                                                                                                            |
| EOGChannelCount                 | RECOMMENDED. Number of EOG channels.                                                                                                                                                                                                                                                     |
| ECGChannelCount                 | RECOMMENDED. Number of ECG channels.                                                                                                                                                                                                                                                     |
| EMGChannelCount                 | RECOMMENDED. Number of EMG channels.                                                                                                                                                                                                                                                     |
| MiscChannelCount                | RECOMMENDED. Number of miscellaneous analog channels for auxiliary signals.                                                                                                                                                                                                              |
| TriggerChannelCount             | RECOMMENDED. Number of channels for digital (TTL bit level) triggers.                                                                                                                                                                                                                    |
| RecordingDuration               | RECOMMENDED. Length of the recording in seconds (e.g., 3600).                                                                                                                                                                                                                            |
| RecordingType                   | RECOMMENDED. Defines whether the recording is “continuous” or “epoched”; this latter limited to time windows about events of interest (e.g., stimulus presentations, subject responses etc.)                                                                                             |
| EpochLength                     | RECOMMENDED. Duration of individual epochs in seconds (e.g., 1) in case of epoched data. If recording was continuous, leave out the field.                                                                                                                                               |
| SubjectArtefactDescription      | RECOMMENDED. Freeform description of the observed subject artefact and its possible cause (e.g., “door open”, ”nurse walked into room at 2 min”, ”seizure at 10 min”). If this field is left empty, it will be interpreted as absence of artifacts.                                      |
| SoftwareVersions                | RECOMMENDED. Manufacturer’s designation of the acquisition software.                                                                                                                                                                                                                     |
| iEEGGround                      | RECOMMENDED. Description of the location of the ground electrode (“placed on right mastoid (M2)”).                                                                                                                                                                                       |
| iEEGPlacementScheme             | RECOMMENDED. Freeform description of the placement of the iEEG electrodes. Left/right/bilateral/depth/surface (e.g., “left frontal grid and bilateral hippocampal depth” or “surface strip and STN depth” or “clinical indication bitemporal, bilateral temporal strips and left grid”). |
| iEEGElectrodeGroups             | RECOMMENDED. Field to describe the way electrodes are grouped into strips, grids or depth probes e.g., {'grid1': "10x8 grid on left temporal pole", 'strip2': "1x8 electrode strip on xxx"}.                                                                                             |

Specific iEEG fields MAY be present:

| Field name                      | Definition                                                                                                                                                                                                                          |
| :------------------------------ | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ElectricalStimulation           | OPTIONAL. Boolean field to specify if electrical stimulation was done during the recording (options are “true” or “false”). Parameters for event-like stimulation should be specified in the \_events.tsv file (see example below). |
| ElectricalStimulationParameters | OPTIONAL. Free form description of stimulation parameters, such as frequency, shape etc. Specific onsets can be specified in the \_events.tsv file. Specific shapes can be described here in freeform text.                         |

Example:

```JSON
{
  "TaskName":"visual",
  "Manufacturer":"Tucker Davis Technologies",
  "ManufacturersModelName":"n/a",
  "TaskDescription":"visual gratings and noise patterns",
  "Instructions":"look at the dot in the center of the screen and press the button when it changes color",
  "CogAtlasID":"n/a",
  "CogPOID":"n/a",
  "InstitutionName":"Stanford Hospital and Clinics",
  "InstitutionAddress":"300 Pasteur Dr, Stanford, CA 94305",
  "DeviceSerialNumber":"n/a",
  "EEGChannelCount":0,
  "EOGChannelCount":0,
  "ECGChannelCount":0,
  "EMGChannelCount":0,
  "MiscChannelCount":0,
  "TriggerChannelCount":0,
  "PowerLineFrequency":60,
  "RecordingDuration":233.639,
  "RecordingType":"continuous",
  "SubjectArtefactDescription":"",
  "ECOGChannelCount":118,
  "SEEGChannelCount":0,
  "iEEGPlacementScheme":"right occipital temporal surface",
  "iEEGReference":"left mastoid",
  "Stimulation":false
}
```

Note that the date and time information SHOULD be stored in the Study key file
([`scans.tsv`](../03-modality-agnostic-files.md#scans-file)). As it is indicated
there, date time information MUST be expressed in the following format
`YYYY-MM-DDThh:mm:ss`
([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For
example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending
on local REB/IRB ethics board policy.

## Channels description table (`*_channels.tsv`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      ieeg/
        [sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_channels.tsv]
```

A channel represents one time series recorded with the recording system (for
example, there can be a bipolar channel, recorded from two electrodes or contact
points on the tissue). Although this information can often be extracted from the
iEEG recording, listing it in a simple `.tsv` document makes it easy to browse
or search (e.g., searching for recordings with a sampling frequency of >=1000
Hz). The two required columns are channel name and type. Channels should appear
in the table in the same order they do in the iEEG data file. Any number of
additional columns may be provided to provide additional information about the
channels. Note that electrode positions should not be added to this file but to
`*_electrodes.tsv`.

The columns of the Channels description table stored in \*\_channels.tsv are:

MUST be present:

| Field name  | Definition                                                                                                                                                                                                                                                                                                                                                   |
| :---------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name        | REQUIRED. Label of the channel, only contains letters and numbers. The label must correspond to \_electrodes.tsv name and all ieeg type channels are required to have a position. The reference channel name MUST be provided in the reference column.                                                                                                       |
| type        | REQUIRED. Type of channel, see below for adequate keywords in this field.                                                                                                                                                                                                                                                                                    |
| units       | REQUIRED. Physical unit of the value represented in this channel, e.g., V for Volt, specified according to the [SI unit symbol](https://en.wikipedia.org/wiki/International_System_of_Units#Base_units) and possibly prefix symbol (e.g., mV, μV), see [TODO: bids link] the BIDS spec (section 15 Appendix V: Units) for guidelines for Units and Prefixes. |
| low_cutoff  | REQUIRED. Frequencies used for the low pass filter applied to the channel in Hz. If no low pass filter was applied, use `n/a`. Note that anti-alias is a low pass filter, specify its frequencies here if applicable.                                                                                                                                        |
| high_cutoff | REQUIRED. Frequencies used for the high pass filter applied to the channel in Hz. If no high pass filter applied, use `n/a`.                                                                                                                                                                                                                                 |

SHOULD be present:

| Field name         | Definition                                                                                                                                                                                                                                                                           |
| :----------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| reference          | OPTIONAL. Specification of the reference (e.g., ‘mastoid’, ’ElectrodeName01’, ‘intracranial’, ’CAR’, ’other’, ‘n/a’). If the channel is not an electrode channel (e.g., a microphone channel) use `n/a`.                                                                             |
| group              | OPTIONAL. Which group of channels (grid/strip/seeg/depth) this channel belongs to. This is relevant because one group has one cable-bundle and noise can be shared. This can be a name or number. Note that any groups specified in `_electrodes.tsv` must match those present here. |
| sampling_frequency | OPTIONAL. Sampling rate of the channel in Hz.                                                                                                                                                                                                                                        |
| description        | OPTIONAL. Brief free-text description of the channel, or other information of interest (e.g., position (e.g., “left lateral temporal surface”, etc.).                                                                                                                                |
| notch              | OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use n/a.                                                                                                                                                                  |
| status             | OPTIONAL. Data quality observed on the channel (good/bad). A channel is considered bad if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in `[status_description]`.                                                                |
| status_description | OPTIONAL. Freeform text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in [status].                                                                                                                 |

**Example** `sub-01_channels.tsv`:

```Text
name  type  units sampling_frequency low_cutoff high_cutoff notch group reference description              status status_description
LT01  ECOG  μV    10000             3000       0.11        n/a   LTG   mastoid   lateral_temporal_surface good   n/a
LT02  ECOG  μV    10000              3000       0.11        n/a   LTG   mastod   lateral_temporal_surface bad    brokenn
H01   SEEG  μV    10000              3000       0.11        n/a   HST   mastoid   hippocampal_depthh       bad    line noisee
ECG1  ECG   μV    10000              n/aa       0.11        60    4     ECG2      ecg_channell             good   na
TR1   TRIG  n/a   1000               n/a        n/a         n/a   5     n/a       ana_trigger              good   n/a
```
Restricted keyword list for field type in alphabetic order (shared with the MEG
and EEG modality; however, only iEEG specific types are listed here):

| Keyword  | Description                                                       |
| :------- | :---------------------------------------------------------------- |
| EEG      | Electrode channel from electroencephalogram                       |
| ECOG     | Electrode channel from electrocorticogram (intracranial)          |
| SEEG     | Electrode channel from stereo-electroencephalogram (intracranial) |
| DBS      | Electrode channel from deep brain stimulation (intracranial)      |
| VEOG     | Vertical EOG (electrooculogram)                                   |
| HEOG     | Horizontal EOG                                                    |
| EOG      | Generic EOG channel if HEOG or VEOG information not available     |
| ECG      | ElectroCardioGram (heart)                                         |
| EMG      | ElectroMyoGram (muscle)                                           |
| TRIG     | System Triggers                                                   |
| AUDIO    | Audio signal                                                      |
| PD       | Photodiode                                                        |
| EYEGAZE  | Eye Tracker gaze                                                  |
| PUPIL    | Eye Tracker pupil diameter                                        |
| MISC     | Miscellaneous                                                     |
| SYSCLOCK | System time showing elapsed time since trial started              |
| ADC      | Analog to Digital input                                           |
| DAC      | Digital to Analog output                                          |
| REF      | Reference channel                                                 |
| OTHER    | Any other type of channel                                         |

The free text field for the channel description can for example be specified as
intracranial, stimulus, response, vertical EOG, horizontal EOG, skin
conductance, eyetracker, etc.

## Electrode description table (`*[_space-<label>]_electrodes.tsv`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      ieeg/
         sub-<label>[_ses-<label>][_space-<label>]_electrodes.tsv
```

File that gives the location, size and other properties of iEEG electrodes. Note
that coordinates are expected in cartesian coordinates according to the
`iEEGCoordinateSystem` and `iEEGCoordinateSystemUnits` fields in
`*_coordsystem.json`. **If an `*_electrodes.tsv` file is specified, a
`*_coordsystem.json` file MUST be specified as well**. The order of the required
columns in the `*_electrodes.tsv` file MUST be as listed below.

MUST be present:
| Field name | Definition                                                                                                                                                                   |
| :--------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name       | REQUIRED. Name of the electrode contact point.                                                                                                                               |
| x          | REQUIRED. X position. The positions of the center of each electrode in xyz space. Units are in millimeters or pixels and are specified in \_\*space-<label>\_electrode.json. |
| y          | REQUIRED. Y position.                                                                                                                                                        |
| z          | REQUIRED. Z position. If electrodes are in 2D space this should be a column of n/a values.                                                                                   |
| size       | REQUIRED. Surface area of the electrode, in mm^2.                                                                                                                            |

SHOULD be present:

| Field name   | Definition                                                                                                                                                           |
| :----------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| material     | OPTIONAL. Material of the electrodes.                                                                                                                                |
| manufacturer | OPTIONAL. Recommended field to specify the manufacturer for each electrode. Can be used if electrodes were manufactured by more than one company.                    |
| group        | OPTIONAL. Optional field to specify the group that the electrode is a part of. Note that any group specified here should match a group specified in `_channels.tsv`. |
| hemisphere   | OPTIONAL. Optional field to specify the hemisphere in which the electrode is placed, one of [‘L’ or ‘R’] (use capital).                                              |

MAY be present:

| Field name | Definition                                                                                                                                   |
| :--------- | :------------------------------------------------------------------------------------------------------------------------------------------- |
| type       | OPTIONAL. Optional type of the electrode, e.g., cup, ring, clip-on, wire, needle, ...                                                        |
| impedance  | OPTIONAL. Impedance of the electrode in kOhm.                                                                                                |
| dimension  | OPTIONAL. Size of the grid/strip/probe that this electrode belongs to. Must be of form [AxB] with the smallest dimension first (e.g. [1x8]). |

Example:

```Text
name  x   y    z    type     size   material    manufacturer
LT01  19  -39  -16  surface  2.3    platinum    Integra
LT02  23  -40  -19  surface  2.3    platinum    Integra
H01   27  -42  -21  depth    5      platinum    AdTech
```

## Coordinate System JSON document (`*[_space-<label>]\_coordsystem.json`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      ieeg/
         sub-<label>[_ses-<label>][_space-<label>]_coordsystem.json
```

This `_coordsystem.json` file contains the coordinate system in which electrode
positions are expressed. The associated MRI, CT, X-Ray, or operative photo can
also be specified. It may also be a geometric description of the
anatomy/electrodes such as a surface description in a `.gii` file (_?_).

General fields:

| Field name  | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| :---------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IntendedFor | RECOMMENDED. This can be an MRI/CT or a file containing the operative photo, x-ray or drawing with path relative to the project folder. If only a surface reconstruction is available, this should point to the surface reconstruction file. Note that this file should have the same coordinate system specified in `iEEGCoordinateSystem`. <br /><br /> For example, <br /><br /> **T1**: `sub-<label>/ses-<label>/anat/sub-01_T1w.nii.gz` <br /><br /> **Surface**: `/derivatives/surfaces/sub-<label>/ses-<label>/anat/sub-01_T1w_pial.R.surf.gii` <br /><br /> **Operative photo**: `/sub-<label>/ses-<label>/ieeg/sub-0001_ses-01_acq-photo1_photo.jpg` <br /><br /> **Talairach**: `/derivatives/surfaces/sub-Talairach/ses-01/anat/sub-Talairach_T1w_pial.R.surf.gii` |

Fields relating to the iEEG electrode positions:

| Field name                          | Definition                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| :---------------------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| iEEGCoordinateSystem                | REQUIRED. Defines the coordinate system for the iEEG electrodes. For example, “ACPC”. See Appendix VIII: preferred names of Coordinate systems. If "Other" (e.g., individual subject MRI), provide definition of the coordinate system in `[iEEGCoordinateSystemDescription]`. If positions correspond to pixel indices in a 2D image (of either a volume-rendering, surface-rendering, operative photo, or operative drawing), this must be “pixels”. See section 3.4.1: Electrode locations for more information on electrode locations. |
| iEEGCoordinateUnits                 | REQUIRED. Units of the \_electrodes.tsv, MUST be “m”, “mm”, “cm” or “pixels”.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| iEEGCoordinateSystemDescription     | RECOMMENDED. Freeform text description or link to document describing the iEEG coordinate system system in detail (e.g., “Coordinate system with the origin at anterior commissure (AC), negative y-axis going through the posterior commissure (PC), z-axis going to a mid-hemisperic point which lies superior to the AC-PC line, x-axis going to the right”).                                                                                                                                                                           |
| iEEGCoordinateProcessingDescription | RECOMMENDED. Has any projection been done on the electrode positions (e.g., “surface_projection”, “none”).                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| iEEGCoordinateProcessingReference   | RECOMMENDED. A reference to a paper that defines in more detail the method used to project or localize the electrodes.                                                                                                                                                                                                                                                                                                                                                                                                                     |

### Recommended 3D coordinate systems

It is preferred that electrodes are localized in a 3D coordinate system (with
respect to a pre- and/or post-operative anatomical MRI or CT scans or in a
standard space as specified in BIDS Appendix VIII: preferred names of Coordinate
systems, such as ACPC).

### Allowed 2D coordinate systems

If electrodes are localized in 2D space (only x and y are specified and z is
n/a), then the positions in this file must correspond to the locations expressed
in pixels on the photo/drawing/rendering of the electrodes on the brain. In this
case, coordinates must be (row,column) pairs, with (0,0) corresponding to the
upper left pixel and (N,0) corresponding to the lower left pixel.
### Multiple coordinate systems

If electrode positions are known in multiple coordinate systems (e.g., MRI, CT
and MNI), these spaces can be distinguished by the optional `[_space-<label>]`
and `[_proc-<label>]` fields.

The optional space label (`[_space-<label>]_electrodes.tsv`) indicates the way
in which electrode positions are interpreted, see [BEP003 - Common
Derivatives](../06-extensions). Examples include:

-   `_space-orig` (electrodes are in the space originally extracted from the
    image, such as a T1 weighted MRI, CT, XRay or 2D operative photo).
-   `_space-MNI152Lin` (electrodes are coregistred and scaled to a specific MNI
    template)
-   `_space-Talairach` (electrodes are coregistred and scaled to Talairach
    space)

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

Template:

```Text
sub-<label>/
    [ses-<label>]/
      ieeg/
         sub-<label>[_ses-<label>][_acq-<label]_photo.json
```

These can include photos of the electrodes on the brain surface, photos of
anatomical features or landmarks (such as sulcal structure), and fiducials. Photos
can also include an X-ray picture, a flatbed scan of a schematic drawing made
during surgery, or screenshots of a brain rendering with electrode positions.
The photos may need to be cropped and/or blurred to conceal identifying features
or entirely omitted prior to sharing, depending on obtained consent.

If there are photos of the electrodes, the acquisition field should be specified
with:

-   `*_photo.jpg` in case of an operative photo
-   `*_acq-xray#_photo.jpg` in case of an x-ray picture
-   `*_acq-drawing#_photo.jpg` in case of a drawing or sketch of electrode
    placements
-   `*_acq-render#_photo.jpg` in case of a rendering

The session label may be used to specify when the photo was taken.

Example of the operative photo of ECoG electrodes (here is an annotated example in
which electrodes and vasculature are marked, taken from Hermes et al.,
JNeuroMeth 2010).

```
    sub-0001_ses-01_acq-photo1_photo.jpg
    sub-0001_ses-01_acq-photo2_photo.jpg
```

[TODO: brain picture]

Below is an example of a volume rendering of the cortical surface with a
superimposed subdural electrode implantation. This map is often provided by the
EEG technician and provided to the epileptologists (e.g., see Burneo JG et al.
2014 http://dx.doi.org/10.1016/j.clineuro.2014.03.020).

```
    sub-0002_ses-001_acq-render_photo.jpg (for volume rendering)
```

[TODO: brain picture 2]

## Electrical stimulation

In case of electrical stimulation of brain tissue by passing current through the
iEEG electrodes, and the electrical stimulation has an event structure (on-off,
onset, duration), the `_events.tsv` file can contain the electrical stimulation
parameters in addition to other events. Note that these can be intermixed with
other task events. Electrical stimulation parameters can be described in columns
called electrical*stimulation*<label>, with labels chosen by the researcher and
optionally defined in more detail in an accompanying `_electrodes.json` file (as
per the main BIDS spec). Functions for complex stimulation patterns can, similar
as when a video is presented, be stored in a folder in the `/stimuli/` folder.
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


========================================================================
THE REMAINING TEXT SHOULD BE SCANNED FOR RELEVANT ITEMS THAT ARE
STILL TO BE INCLUDED IN THE IEEG SPECIFICATION. I (=ROBERT) THINK THAT
THE REMAINDER CAN BE REMOVED.
========================================================================

### Complete template including iEEG data

The following section describes the structure of files, folders, and their naming conventions for the BIDS-iEEG specification.

```Text
# required: essential to be BIDS compliant (i.e., MUST as per RFC2199)
# recommended: gives a warning if not present (i.e., SHOULD as per RFC2199)
# [] indicates optional: no warning if missing (i.e., MAY as per RFC2199)

sub-<label>/
  [ses-<label>]/
    [sub-<label>_scans.tsv]                                         # optional
    anat/
      sub-<label>[_ses-<label>]_T1w.nii[.gz]                        # recommend
      ...
  [ses-<label>]/
    [sub-<label>_scans.tsv]                                         # optional
    anat/
      sub-<label>[_ses-<label>]_T1w.nii[.gz]                        # recommend
      [sub-<label>[_ses-<label>]_CT.nii[.gz]]                       # optional
      ...
    ieeg/
      sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>]
        [_run-<index>][_space-<label>]_ieeg.<allowed_extension>     # required
      sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>]
        [_run-<index>][_space-<label>]_ieeg.json                    # required
      sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>]
        [_run-<index>][_space-<label>]_channels.tsv                 # required
      [sub-<label>[_ses-<label>]_task-<task_label>[_acq-<label>]
        [_run-<index>][_space-<label>]_events.tsv]                  # optional

# electrode metadata
sub-<label>[_ses-<label>][_space-<label>]_electrodes.tsv            # required
sub-<label>[_ses-<label>][_space-<label>]_coordsystem.json          # required
[sub-<label>[_ses-<label>][_space-<label>]_photo.jpg]               # optional
```

The iEEG template can include iEEG data of any kind, including but not limited to task-based, resting state, sleep and cortico-cortical evoked potentials (CCEP) recordings.

The `_proc` (processed) label can be added for processing on a recording device, such as e.g., real-time processing for a closed loop DBS device.

### RUN specific files

A number of files may be included alongside each iEEG recording data file (i.e., for every run of data collection). These files contain information that can often be partially extracted from the raw data files. By having this information in the json/tsv files as well, it facilitates querying large collections of iEEG datasets. These include:

1. `*_ieeg.json`:  A JSON document containing metadata about the iEEG recording data file.
2. `*_channels.tsv`: A `.tsv` file listing amplifier metadata such as channel names, types, sampling frequency, and other information. Note that this may include non-electrode channels such as trigger channels.
3. `*_events.tsv`: A `.tsv` file listing the event latency and description.

For behavioral data acquired independently or alongside the iEEG, MEG, or MRI recording, see section “8.7 Behavioral experiments (with no MRI)” of the The Brain Imaging Data Structure (BIDS) Specification.[TODO: BIDS link]




#### Task events (`*_events.tsv`)
Task events are part of the general BIDS (see section 8.5 from [TODO LINK] The Brain Imaging Data Structure (BIDS) Specification). We add some examples here about storing data recorded during electrical stimulation of the electrodes.

Template:
```Text
sub-<label>/[ses-<_label>]/
   ieeg/
      <matches>_events.tsv
```
Where `<matches>` corresponds to task file name. For example: sub-control01_task-nback

**Required Fields**

| Field name | Definition |
| :--- | :---
| onset | REQUIRED. Onset in seconds.
| duration | REQUIRED. Duration in seconds.
| trial_type | REQUIRED. Examples:  “electrical_stimulation” for trials with electrical stimulation on the intracranial electrodes, “passive listening” for trials where a subject passively hears a stimulus.

**Optional fields**

| Field name | Definition |
| :--- | :---
| sample | OPTIONAL. Onset of the event with respect to the digitization of the signal.
| value | OPTIONAL. Corresponds to the value of a marker of the event, for example the value of a TTL trigger as incorporated in a TRIG channel.

#### Physiological and other continuous recordings
Auxiliary continuous recordings such as an audio or video are part of the general
[TODO: link]Brain Imaging Data Structure (BIDS) Specification (see section 8.6).

### SESSION specific files

These are files unique to each session of recording. For example, across multiple experiments run in the same day for one patient. Channels are defined as the entities of the amplifier, electrodes are the single metallic contacts to the tissue.

**Required Files:**

1. Electrode locations table: `*[_space-<label>]_electrodes.tsv`
2. Electrode coordinates JSON document (`*[_space-<label>]_coordsystem.json`)

The optional element space-<label> should  be used to distinguish the files in case electrodes are expressed in multiple coordinate systems (e.g., in pixels in a photo, and in mm relative to a CT) and/or in relation to different templates or atlases (e.g., in the “individual'’ coordinates, as well as after piecewise re-scaling relative to the Talairach-Tournoux atlas)

**Optional Files:**
A number of optional files may be included once for a given iEEG session. These are listed below and described in the following sections.

1. `*_photo.jpg`
2. `*_scans.tsv`

#### Multiple recordings in one session  (`scans.tsv`)

See section “8.10 Scans key file” of  The Brain Imaging Data Structure (BIDS) Specification for a detailed description.
Optional: Yes

This file is called scans, but is used to describe timing and other properties of any ieeg recording sequence or imaging acquisition sequence (each run (.nii[.gz] or ieeg) file) within one session. Each  data file file should be described by at most one row. Relative paths to files should be used under a compulsory “filename” header. If acquisition time is included it should be under “acq_time” header.

Clinical EEG or iEEG recordings  can be very long. If this results in multiple recordings, either because the recording software automatically breaks it up in separate files, or because some intervention was needed after which recording was resumed, the recordings should be represented as separate runs (using `_run-<number>_` in the file name). During clinical long-term monitoring of iEEG it happens that patients participate as volunteers in experiments (including tasks). Since long recordings that are split over multiple runs are represented separately in the scans.tsv file, the `acq_time` column should be used to determine whether they are part of a long continuous recording or whether there was a gap in between.         

Datetime should be expressed in the following format `2009-06-15T13:45:30` (year, month, day, hour (24h), minute, second; this is equivalent to the RFC3339 “date-time” format, time zone is always assumed as local time). For anonymization purposes all dates within one subject should be shifted by a randomly chosen (but common across all runs etc.) number of days. This way relative timing would be preserved, but chances of identifying a person based on the date and time of their scan would be decreased. Dates that are shifted for anonymization purposes should be set to a year `1900` or earlier to clearly distinguish them from unmodified data. Shifting dates is recommended, but not required. Additional fields can include external behavioral measures relevant to the scan. For example vigilance questionnaire score administered after a resting state scan.

Template:

```
sub-<label>/[ses-<session_label>/]
  sub-<label>_scans.tsv
```

**Example**


| filename | acq_time |
| :--- | :--- |
| anat/sub-control01_T1w.nii.gz | 1876-06-09T00:07:10
| ieeg/sub-control01_task-rest_ieeg.edf | 1877-06-15T13:45:30
| ieeg/sub-control01_task-motor_ieeg.edf | 1889-06-15T13:55:33

### SUBJECT keyfiles

#### Sessions file (`*_sessions.tsv`)
See section “9.1 Sessions file” of  The Brain Imaging Data Structure (BIDS) Specification for a detailed description.
Optional: Yes

### STUDY keyfiles

#### `participants.tsv`

See section “8.11 Participant key file” of  The Brain Imaging Data Structure (BIDS) Specification for a detailed description.
Optional: Yes

Template: (single session case)

```
participants.tsv
participants.json
```

**Example**


| participant_id | age | sex | group
| :---: | :---: | :---: | :---: |
| sub-control01 | 34 | M | control
| sub-control02 | 12 | F | control
| sub-patient01 | 33 | F | patient

## Appendix I: Example iEEG cases

This section contains examples that demonstrate the structure of files for BIDS-iEEG.
Examples are included that use several different methods to determine electrode coordinates:

- From pre- and/or post-operative anatomical MRI or CT scans.
- From a photo taken during surgery, or a drawing made during surgery (scanned to an image afterward).
- Localizing in Talairach space using X-ray images.

### Visual dataset

This dataset is an example of a `.mat` file containing a single data matrix. All metadata and header file information is contained in the `.json` and `.tsv` files. The electrode locations are in millimeter and match the surface rendering of the associated gifti (.gii) file.  A link to this dataset can be found here: https://github.com/bids-standard/bids-examples/tree/bep010_ieeg/ieeg_visual

```
ieeg_visual/
├── dataset_description.json
├── derivatives
│   └── surfaces
│       └── sub-01
│           └── ses-01
│               └── anat
│                   └── sub-01_ses-01_T1w_pial.R.surf.gii
├── participants.tsv
├── stimuli
│   ├── stim_100.png
├───├── ...
│   └── stim_9.png
└── sub-01
    └── ses-01
        ├── anat
        │   ├── sub-01_ses-01_T1w.json
        │   └── sub-01_ses-01_T1w.nii.gz
        └── ieeg
            ├── sub-01_ses-01_coordsystem.json
            ├── sub-01_ses-01_electrodes.tsv
            ├── sub-01_ses-01_task-visual_run-01_channels.tsv
            ├── sub-01_ses-01_task-visual_run-01_events.tsv
            ├── sub-01_ses-01_task-visual_run-01_ieeg.gdf
            └── sub-01_ses-01_task-visual_run-01_ieeg.json
```

### Auditory dataset

This dataset was collected during a passive listening task in which subjects listened to filtered and unfiltered versions of natural speech. In this case, there is no surface reconstruction of the patient’s cortex, only an operative photo with 2-D electrode locations in a corresponding TSV file. A link to the dataset can be found here: https://github.com/bids/bids-examples/tree/bep010_ieeg/ieeg_filtered_speech

```
ieeg_filtered_speech/
├── dataset_description.json
├── participants.tsv
├── stimuli
│   └── cm4_audio.wav
├── sub-cm4
│   ├── anat
│   │   └── sub-cm4_photo.jpg
│   └── ieeg
│       ├── sub-cm4_ieeg.json
│       ├── sub-cm4_space-2DImage_coordsystem.json
│       ├── sub-cm4_task-FilteredSpeech_channels.tsv
│       ├── sub-cm4_task-FilteredSpeech_electrodes.tsv
│       ├── sub-cm4_task-FilteredSpeech_events.tsv
│       └── sub-cm4_task-FilteredSpeech_ieeg.fif
```

### Hand and tongue movement dataset

This link has an example dataset (with an empty datamatrix to reduce space):
https://github.com/bids-standard/bids-examples/tree/bep010_ieeg/ieeg_motorMiller2007

If a surgical photo or drawing is used, 2-D electrode positions should be specified in pixels, where the upper left corner is (0,0), the first dimension moves across rows, and the second dimension moves across columns.  If an X-Ray is used, it is possible to e.g., use the “Matlab LOC package” to coregister the X-Ray with the Talairach-Tournoux atlas Miller et al., 2007, Journal of Neuroscience Methods doi:10.1016/j.jneumeth.2007.01.019) and to determine the electrodes in TT coordinates. If the “Matlab LOC package” is not used, it is also possible to specify the position of the electrodes in pixels on the X-ray, just like for photos or for drawings that have digitally scanned. If a pre- and/or post-operative anatomical MRI or CT is available, the position of the electrodes can be specified in the coordinate system that is specified by that 3-D anatomical data.

### Visual multimodal dataset

This example set demonstrates how complex datasets containing multimodal recordings can be organized using BIDS. This dataset contains both ECoG and fMRI recordings from a single patient. The patient viewed a variety of visual stimuli, separated across three different tasks (spatialobject, spatialpattern, and temporalpattern), which were each repeated four times (run 01-04). The same tasks were run in both modalities: one ECoG session (somecog01) and one fMRI session (nyu3t01). The electrode positions (detailed in electrodes.tsv) are specified in the coordinate system of a pre-operative T1 scan that was collected in a third, separate MRI session (som3t01). A link to the full dataset structure can be found here: https://github.com/irisgroen/bids-examples

```
ieeg_visual_multimodal/
├── dataset_description.json
├── participants.tsv
└── stimuli
    ├── stim_107.png
    ├── stim_108.png
    ├── ...
    └── stim_133.png  
└── sub-som682
    └── ses-nyu3t01
        └── anat
            ├── sub-som682_ses-nyu3t01_T1w.nii.gz
            ├── sub-som682_ses-nyu3t01_T1w.json
 └── fmap
            ├── sub-som682_ses-nyu3t01_dir-LR_epi.json
            ├── sub-som682_ses-nyu3t01_dir-LR_epi.nii.gz
            ├── sub-som682_ses-nyu3t01_dir-RL_epi.json
            ├── sub-som682_ses-nyu3t01_dir-RL_epi.nii.gz
        └── func
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-01_bold.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-01_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-01_events.tsv
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-01_sbref.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-01_sbref.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-02_bold.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-02_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-02_events.tsv
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-02_sbref.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-02_sbref.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-03_bold.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-03_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-03_events.tsv
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-03_sbref.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-03_sbref.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-04_bold.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-04_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-04_events.tsv
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-04_sbref.json
            ├── sub-som682_ses-nyu3t01_task-spatialobject_run-04_sbref.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialpattern_run-01_bold.json
            ├── sub-som682_ses-nyu3t01_task-spatialpattern_run-01_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-spatialpattern_run-01_events.tsv
            ├── sub-som682_ses-nyu3t01_task-spatialpattern_run-01_sbref.json
            ├── sub-som682_ses-nyu3t01_task-spatialpattern_run-01_sbref.nii.gz
            ├── ...
            ├── sub-som682_ses-nyu3t01_task-temporalpattern_run-04_bold.json
            ├── sub-som682_ses-nyu3t01_task-temporalpattern_run-04_bold.nii.gz
            ├── sub-som682_ses-nyu3t01_task-temporalpattern_run-04_events.tsv
            ├── sub-som682_ses-nyu3t01_task-temporalpattern_run-04_sbref.json
            └── sub-som682_ses-nyu3t01_task-temporalpattern_run-04_sbref.nii.gz   
    └── ses-som3t01
        └── anat
            ├── sub-som682_ses-som3t01_T1w.nii.gz
    └── ses-somecog01
        └── ieeg
            ├── sub-som682_ses-somecog01_coordsystem.json
            ├── sub-som682_ses-somecog01_electrodes.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_channels.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_events.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_ieeg.json
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_ieeg.vhdr
            ├── sub-som682_ses-somecog01_task-spatialobject_run-01_ieeg.vmrk
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_channels.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_events.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_ieeg.json
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_ieeg.vhdr
            ├── sub-som682_ses-somecog01_task-spatialobject_run-02_ieeg.vmrk
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_channels.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_events.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_ieeg.json
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_ieeg.vhdr
            ├── sub-som682_ses-somecog01_task-spatialobject_run-03_ieeg.vmrk
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_channels.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_events.tsv
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_ieeg.json
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_ieeg.vhdr
            ├── sub-som682_ses-somecog01_task-spatialobject_run-04_ieeg.vmrk
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_channels.tsv
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_events.tsv
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_ieeg.json
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_ieeg.vhdr
            ├── sub-som682_ses-somecog01_task-spatialpattern_run-01_ieeg.vmrk
            ├── ...
            ├── sub-som682_ses-somecog01_task-temporalpattern_run-04_channels.tsv
            ├── sub-som682_ses-somecog01_task-temporalpattern_run-04_events.tsv
            ├── sub-som682_ses-somecog01_task-temporalpattern_run-04_ieeg.eeg
            ├── sub-som682_ses-somecog01_task-temporalpattern_run-04_ieeg.json
            ├── sub-som682_ses-somecog01_task-temporalpattern_run-04_ieeg.vhdr
            └── sub-som682_ses-somecog01_task-temporalpattern_run-04_ieeg.vmrk
```         

## Appendix II: Preferred names of Coordinate systems

**See the main BIDS specification document appendix on preferred names of coordinate systems for information on coordinate system naming. The language in that section will be copied here just before finalizing the BIDS-iEEG specification.**

## Appendix III: Simultaneous recordings of different data types

**Definitions**
Synchronous = specifies that two or more data types include an explicit link between data points.
Simultaneous = specifies that the recording was done at approximately the same time with an implicit link between data points.

[TODO: figure out this table]

## Change-log

Here is a list of dates and changes made to the specs:

* TODO: first commit
