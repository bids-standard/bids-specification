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
suffixes=["emg", "events"])
}}

EMG device manufacturers use a variety of formats for storing raw data, and there is
no single standard that all researchers agree on. For BIDS, EMG data MUST be
stored in one of the following formats:

| **Format**                                                         | **Extension(s)**         | **Description**                                                                                                                                                                                      |
| ------------------------------------------------------------------ | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Biosemi data format](https://www.biosemi.com/faq/file_format.htm) | `.bdf`                   | Each recording consists of a single `.bdf` file. [`bdf+`](https://www.teuniz.net/edfbrowser/bdfplus%20format%20description.html) files are permitted. The capital `.BDF` extension MUST NOT be used. |
| [European data format](https://www.edfplus.info/)                  | `.edf`                   | Each recording consists of a single `.edf` file. [`edf+`](https://www.edfplus.info/specs/edfplus.html) files are permitted. The capital `.EDF` extension MUST NOT be used.                           |

EDF, EDF+, BDF, and BDF+ are all open data formats with broad support in various programming languages for reading and writing the files. BDF and BDF+ formats store data samples using 3 bytes instead of 2 bytes as in EDF and EDF+ formats, allowing for greater resolution. EDF+/BDF+ accommodate more header metadata than EDF/BDF, and support storing event or annotation information in the file. Thus it is RECOMMENDED to use the BDF+ data format.

The [`recording-<label>`](../appendices/entities.md#recording) entity MAY be used to indicate
simultaneous acquisition of data from multiple EMG devices, in cases where the devices
store data in separate data files.
If separate devices are being used with separate sampling rates, start times, or other
acquisition parameters, the `recording-<label>` entity MUST be used to distinguish between them.
The synchronization of data from multiple devices SHOULD be described in the
[Scans](../modality-agnostic-files/data-summary-files.md#scans-file) (`scans.tsv`) file, using the
`acq_time` entity.

In cases where the allowed formats do not encode all relevant metadata present in the
device manufacturer's native file format, we encourage users to provide the additional
metadata in the sidecar JSON file.

### Terminology: Electrodes vs. Channels

For proper documentation of EMG recording metadata it is important to understand the
difference between an electrode and a channel: an EMG electrode is a single point of
electrical contact with the body, whereas a channel is the combination of the analog
differential amplifier (which combines signals from two electrode sources) and the
analog-to-digital converter, which results in a potential difference (voltage) that forms
the actual data stored in the EMG dataset. We employ the following short definitions:

-   **Electrode:** A single point of contact between the acquisition system and
    the recording site (whether on the skin surface or intramuscular).
    Multiple electrodes can be organized as arrays, grids, leads, strips, probes,
    shafts, and so on.

-   **Channel:** A single analog-to-digital converter in the recording system that
    regularly samples the value of a transducer, which results in the signal being
    represented as a time series in the digitized data.
    This can be connected to two electrodes (to measure the potential difference between
    them), a magnetic field or magnetic gradient sensor, temperature sensor,
    accelerometer, and so forth.

This distinction is especially important for EMG because a common type of EMG device
(often erroneously called a "bipolar electrode") comprises two electrodes at a fixed distance,
wired such that the electrode pair is necessarily converted to a single channel by the amplifier
(in other words, one of the electrodes necessarily acts as the _reference_ for the other).
In other kinds of devices, researchers may have control over which electrode(s) to use as
the reference for each channel.

Note also that although the _reference_ and _ground_ electrodes are often referred to as
channels, in most common EMG systems they are not recorded by themselves.
Therefore they are usually not represented as channels in the data.
<!-- The type of referencing for all channels and optionally the location of the reference
electrode and the location of the ground electrode MAY be specified. -->

### Describing sensor locations

Each EMG-BIDS dataset SHOULD include sensor location information that is as accurate as
possible given the measurement means available to the researcher(s).
Below are examples ranging from most accurate to least accurate, which can serve as a
guide to where sensor placement information should be stored in the dataset.

1.  Electrode locations and anatomical landmarks are digitized with a 3D localizer device
    such as Polhemus FasTrak or a 3D scanner.
    3D coordinates for each electrode are given in `x,y,z` columns of `*_electrodes.tsv`,
    and the coordinate system definition is given in `*_coordsystem.json`.

1.  Electrode locations are measured relative to nearby anatomical landmarks using a flexible
    measuring tape.
    2D or 3D coordinates for each electrode are given in `x`, `y`, and (optionally) `z`
    columns of `*_electrodes.tsv`, and the coordinate system definition in
    `*_coordsystem.json` specifies the axis directions with reference to those anatomical
    landmarks.

1.  The arrangement of electrodes in a group or grid is measured (or known from the device
    manufacturer), and is provided in `x`, `y`, and (optionally) `z` columns of `*_electrodes.tsv`,
    with a device-internal "child" coordinate system defined in a `*_coordsystem.json` file.
    An anatomically-defined "parent" coordinate system is also defined in a different
    `*_coordsystem.json` file, and the name and coordinates of one electrode (the "anchor"
    electrode) from each "child" group or grid is provided in the "parent" coordinate system.
    This allows the approximate anatomical locations of all electrodes to be calculated
    by treating the device-internal coordinates as offsets from the anchor coordinate.
    The two `*_coordsystem.json` files are distinguished by the `space` entity in their filenames;
    the labels used for that entity may be arbitrary (for example, `*_space-grid_coordsystem.json`
    for the child coordinate system, and `*_space-forearm_coordsystem.json` for the parent
    coordinate system).

1.  Individual electrode locations are chosen by visual inspection, palpation, or
    functional localizers.
    No measured coordinates are provided; placement information is given either in the
    `EMGPlacementSchemeDescription` field of `*_emg.json` (when the placement approach is
    the same for all sensors), or in the `placement_description` column of `*_channels.tsv`
    (when the placement approach varied across sensors).

More details on each of these scenarios is given below in the
[Channels description](#channels-description-_channelstsv),
[Electrodes description](#electrodes-description-_electrodestsv), and
[Coordinate system](#coordinate-system-json-_coordsystemjson) sections.

A fifth scenario unique to EMG involves location information that is fairly accurate
(as in scenarios (1) and (2) above) but it locates _bipolar sensor devices_ rather than
_electrodes_.
In this case, researchers SHOULD provide `*_electrodes.tsv` even though information about
the individual electrode contacts is not available.
Rather, each entry from `*_channels.tsv` should have a corresponding row in `*_electrodes.tsv`
where the location information is given, and `*_coordsystem.json` should also be provided
(as in scenarios (1) or (2) above).

### EMG in combination with other modalities

When EMG is recorded alongside other BIDS modalities (such as EEG or motion),
researchers SHOULD define how recordings are synchronized. Options include:

-   Recording time stamps from a common clock source on the LATENCY channel of
    each modality’s acquisition device.

-   Recording experimental events (usually as TTL pulses) on dedicated channels of
    each modality’s acquisition devices.

-   Storing the acquisition time (relative to a common clock source) of the first data point
    of each modality’s recording in the acq_time column of the *_scans.tsv file.
    Note that the BIDS date time format allows optional fractional seconds,
    which SHOULD be used to maximize the precision of the synchronization.

-   Record the start- and stop-time of one modality’s recording (relative to
    the other modality’s clock) in the *_events.tsv file for the other modality.

It is up to the user to decide which approach is most appropriate given their experimental setup,
and to identify which modality will serve as the 'main' clock source for synchronization purposes
(or whether a separate external clock source is used).

### Sidecar JSON (`*_emg.json`)

For consistency between studies and institutions,
we encourage users to extract the values of metadata fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

These fields MUST be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGRequired") }}

These fields SHOULD be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("emg.EMGRecommended") }}

Note the `RecordingType`, which depends on whether the data stream on disk is interrupted or not.
Continuous data is by definition 1 segment without interruption.
Epoched data consists of multiple segments that all have the same length
(for example, corresponding to trials) and that have gaps in between.
Discontinuous data consists of multiple segments of different length,
for example due to a pause in the acquisition.

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
([`scans.tsv`](../modality-agnostic-files/data-summary-files.md#scans-file)).
Date time information MUST be expressed as indicated in [Units](../common-principles.md#units).

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
<!-- TODO check if hardware filters are plausible for an EMG system -->
```JSON
{
  "EMGChannelCount":4,
  "EMGGround":"n/a",
  "EMGPlacementScheme":"Other",
  "EMGPlacementSchemeDescription":"midpoint between cubital fossa and radial styloid process",
  "EMGReference":"4 reference electrodes built-in to device, placed near the midpoint between radial and ulnar styloid processes on the volar surface",
  "HardwareFilters":{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dBOctave"}},
  "InstitutionAddress":"9500 Gilman Drive 0559, La Jolla, CA 92093",
  "InstitutionalDepartmentName":"Swartz Center for Computational Neuroscience",
  "InstitutionName":"University of California San Diego",
  "Instructions":"Jump straight upward as high as you can, while keeping your arms at your sides.",
  "Manufacturer":"Delsys",
  "ManufacturersModelName":"Trigno® Galileo",
  "PowerLineFrequency":60,
  "RecordingDuration":123.456,
  "RecordingType":"continuous",
  "SamplingFrequency":1000,
  "SoftwareFilters":"n/a",
  "TaskDescription":"jumping with stationary arms",
  "TaskName":"jumping"
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

A channel is represented by one time series recorded with the recording system.
Although this information can often be extracted from the EMG recording,
listing it in a simple `.tsv` document makes it easy to browse or search
(for example, searching for recordings with a sampling frequency of >=1000 Hz).
Hence, the `*_channels.tsv` file is RECOMMENDED.
Channels SHOULD appear in the table in the same order they do in the EMG data file.
Additional columns MAY be included to provide additional information about the channels.
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

| **Keyword** | **Description**                                                                                                                                                                                                                                                                   |
| ----------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| VEOG        | Vertical EOG (electrooculogram)                                                                                                                                                                                                                                                   |
| HEOG        | Horizontal EOG                                                                                                                                                                                                                                                                    |
| EOG         | Generic EOG channel if HEOG or VEOG information not available                                                                                                                                                                                                                     |
| ECG         | ElectroCardioGram (heart)                                                                                                                                                                                                                                                         |
| EMG         | ElectroMyoGram (muscle)                                                                                                                                                                                                                                                           |
| TRIG        | Analog (TTL in Volt) or digital (binary TTL) trigger channel                                                                                                                                                                                                                      |
| MISC        | Miscellaneous                                                                                                                                                                                                                                                                     |
| SYSCLOCK    | Elapsed time since trial/recording start, as provided by the recording device.                                                                                                                                                                                                    |
| LATENCY     | Latency of sample, in seconds from recording onset, typically from an _external_ clock source. See `acq_time` column of the respective `*_scans.tsv` file. MUST be in form of `s[.000000]`, where `s` reflects whole seconds, and `.000000` reflects OPTIONAL fractional seconds. |
| REF         | Reference channel                                                                                                                                                                                                                                                                 |

Examples of common free-form text for the `description` column (these should occur _without enclosing quotation marks_):

-   n/a
-   stimulus
-   response
-   skin conductance
-   battery status

### Example `*_channels.tsv`

See also the corresponding [`electrodes.tsv` example](#example-electrodestsv).
```Text
name  type  units  signal_electrode  reference  target_muscle
emg1  EMG   V      E1                E2         anterior belly of the digastric
emg2  EMG   V      E3                E4         levator angulis oris, zygomaticus major
emg3  EMG   V      E5                E6         platysma
emg4  EMG   V      E7                E8         obicularis oris
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

Electrode locations may be specified in one of four ways:

1.  **Coordinates and landmarks digitized in situ.**
    When 3D electrode locations are digitized in situ, the origin, orientation, and measurement
    unit of the coordinate system MUST be recorded in Cartesian coordinates according to the
    `EMGCoordinateSystem` and `EMGCoordinateUnits` fields in `*_coordsystem.json`,
    as described in the [Coordinate Systems Appendix](../appendices/coordinate-systems.md).
    In such cases, `EMGCoordinateSystem` SHOULD be specified as `Other`, the
    `EMGCoordinateSystemDescription` SHOULD contain a description of the origin and axis
    orientations of the 3D coordinate system, and the `coordinate_system` column in
    `*_electrodes.tsv` may be omitted.

1.  **Measured coordinates in a single coordinate system defined by anatomical landmarks.**
    This approach is suitable for individual electrodes placed close together on a single
    body part.
    In this case the `*_coordsystem.json` file MUST contain fields `EMGCoordinateSystem`,
    `EMGCoordinateUnits`, and `EMGCoordinateSystemDescription` as described in (1) above.
    For example, 4 electrodes all placed on the forearm (2 on the volar surface and 2 on
    the dorsal surface) could be located with coordinates in the following coordinate system:

    -   `x`: radial styloid process (RSP) → ulnar styloid process (USP);
    -   `y`: oleacranon process → cubital fossa;
    -   `z`: RSP-USP → lateral humerus epicondyle

    It may be possible to omit the `z` column when all electrodes are on the same surface
    (in the above example, if all electrodes were on the volar surface and none were on
    the dorsal surface).
    Though it would be possible to omit both `z` and `y` if all electrodes are colinear
    along the anatomically defined `x` axis, the `y` column is required and thus researchers
    SHOULD enter `0` for all entries in column `y` in such cases.
    In this case (of a single coordinate system for all electrodes) the
    `coordinate_system` column in `*_electrodes.tsv` may be omitted as in (1) above.

1.  **Measured coordinates in multiple anatomically-defined coordinate systems.**
    This approach is suitable for individual electrodes placed on multiple body parts.
    In this case there MUST be multiple `*_coordsystem.json` files (distinguished by the
    `space` entity) for each coordinate system, each of which MUST contain the fields
    `EMGCoordinateSystem`, `EMGCoordinateUnits`, and `EMGCoordinateSystemDescription` as
    described in (1) above.
    Additionally, the `coordinate_system` column in `*_electrodes.tsv` MUST indicate which
    named coordinate system the coordinate values in that row reflect, by referencing the
    label of the `space` entity for the corresponding `*_coordsystem.json` file.
    For example, `*_space-lowerLeg_coordsystem.json` may specify a coordinate system defined
    by lower leg landmarks for electrodes below the knee, and another called
    `*_space-thigh_coordsystem.json` defined by upper-leg landmarks for electrodes above the knee.
    In such a case, entries in the `coordinate_system` column of `*_electrodes.tsv` MUST
    specify either `"lowerLeg"` or `"thigh"`.
    As in (2) above, enter `0` for the `y` column values if all electrodes are colinear
    along the defined `x` axis.

1.  **Measured coordinates in "nested" coordinate systems.**
    This approach is suitable for large electrode grids or similar devices.
    In this case, measured 2D locations in the `x` and `y` columns define the geometry
    of an electrode grid or group, relative to an arbitrary device-internal origin and
    axes (this is the "child" coordinate system, defined for example in a file
    `*_space-dorsalGrid_coordsystem.json`).
    The group's placement on the body is then described by selecting an "anchor"
    electrode and providing its coordinates within a "parent" coordinate system defined
    in reference to subject anatomy (as in (2) above), in a separate file such as
    `*_space-forearm_coordsystem.json`.
    Each coordinate system file MUST contain the fields `EMGCoordinateSystem`,
    `EMGCoordinateUnits`, and `EMGCoordinateSystemDescription` as described in (1) above.
    Additionally, each child coordinate system file MUST contain an entry `ParentCoordinateSystem`
    giving the value of the `space` entity for the file that defines the parent (anatomical) coordinate system,
    and entries `AnchorElectrode` and `AnchorCoordinates` that name an electrode and provide
    its coordinates in the parent coordinate system (respectively).
    For example, a coordinate system called "forearm" defined by forearm anatomical landmarks
    (as in (2) above) could be the parent coordinate system for two electrode grids placed on
    the volar and dorsal surfaces of the forearm.
    Each grid would have its own coordinate system file (named, for example,
    `*_space-dorsalGrid_coordsystem.json` and `*_space-volarGrid_coordsystem.json`)
    in which coordinates of each electrode are relative to a device-internal
    origin, such as the lower-leftmost electrode when the device is in a specified orientation.
    In such a scenario, entries in the `coordinate_system` column of `*_electrodes.tsv`
    MUST specify either `"volarGrid"` or `"dorsalGrid"` for electrodes within each grid
    (electrodes external to the grid, such as separate reference or ground electrodes, MAY
    specify a different value in the `coordinate_system` column: typically this will be the parent
    coordinate system or a different anatomically defined coordinate system as in (2) above).
    Note that the parent coordinate system may be defined in different units than the child
    coordinate system; for example, if an anchor electrode was placed 50% of the distance
    between the ulnar styloid process and cubital fossa, the unit of the parent coordinate
    system is `"percent"` and `AnchorCoordinates` would have a value of `50` for the `x`
    coordinate in `*_space-volarGrid_coordsystem.json`.
    Meanwhile, the `x` column of `*_electrodes.tsv` gives the device-internal coordinates
    of the grid electrodes, which may be in a different unit such as `"mm"`.
    See the [`coordsystem.json` section](#example-coordsystemjson) for further details.

For details of how to specify the coordinate systems in each of these cases, see the
[`coordsystem.json` section](#example-coordsystemjson).

### Required columns

The order of the required columns in the `*_electrodes.tsv` file MUST be as listed below.

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("emg.EMGElectrodes") }}

The [`recording-<label>`](../appendices/entities.md#recording) entity MUST be used to indicate
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
         "emg": {
            "sub-01_ses-01_recording-RectusFemoris_electrodes.tsv": "",
            "sub-01_ses-01_recording-VastusLateralis_electrodes.tsv": "",
            "sub-01_ses-01_recording-VastusMedialis_electrodes.tsv": ""
            },
         },
      }
   }
) }}

Above, acquisitions are labeled with the target muscle, but other naming schemes are also
appropriate. For example, if bipolar and grid EMG devices are used simultaneously,
acquisitions may be labeled "bipolar" and "grid", or use the device manufacturer names.
For cases of multiple devices recording simultaneously into _the same data file_,
the `group` column MUST be used to distinguish which electrodes belong to which device.

Except in cases of simultaneous acquisitions from different devices into different data
files (as mentioned above), `*_electrodes.tsv` files SHOULD NOT be duplicated for each data file,
for example, during multiple runs of a task.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate electrode positions for a given data file.
If electrodes are repositioned, it is RECOMMENDED to use multiple sessions to indicate this.

### Example `*_electrodes.tsv`

Example `*_electrodes.tsv` for a 2 by 2 grid of EMG electrodes with 2.5 mm electrode diameter
and 10 mm inter-electrode distance.

```Text
name  x     y     coordinate_system  group  diameter
001   0.0   0.0   VolarForearm       grid1  2.5
002   10.0  0.0   VolarForearm       grid1  2.5
003   0.0   10.0  VolarForearm       grid1  2.5
004   10.0  10.0  VolarForearm       grid1  2.5
001   0.0   0.0   DorsalForearm      grid2  2.5
002   10.0  0.0   DorsalForearm      grid2  2.5
003   0.0   10.0  DorsalForearm      grid2  2.5
004   10.0  10.0  DorsalForearm      grid2  2.5
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

This `*_coordsystem.json` file contains the coordinate system in which electrode positions
are expressed.
Associated photos can also be provided.
**The `*_coordsystem.json` is REQUIRED if the optional `*_electrodes.tsv` is specified**;
please see the [electrodes description section](#electrodes-description-electrodestsv) for
important guidance regarding how to specify electrode location.

Fields relating to the EMG coordinate system(s):

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table("json.emg.EMGCoordsystemPositions") }}

The [`recording-<label>`](../appendices/entities.md#recording) entity MUST be used to indicate
simultaneous acquisition of data from multiple EMG devices, in cases where the devices
store data in separate data files.
Except in cases of simultaneous acquisitions from different devices into different data
files (as just mentioned), `*_coordsystem.json` files SHOULD NOT be duplicated for each data file,
for example, during multiple runs of a task.
However, multiple `*_coordsystem.json` files distinguished by the `space` entity MUST be
used to describe separate anatomically-defined coordinate systems (for example, to situate
devices in reference to landmarks on different limbs).
Multiple `*_coordsystem.json` files distinguished by the `space` entity MUST also be used to describe
_nested coordinate systems_ that give the relative positions of groups or grids of electrodes
mounted to a single device and situate that "child" coordinate system within an anatomically-defined
"parent" coordinate system that situates the placement multi-electrode device on the body.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate coordinate system description for a given data file.

### Example 1: `*_coordsystem.json` for digitized electrode positions

Here, a coordinate system is defined based on digitized cranial landmarks, and is suitable
for EMG electrodes on the face whose locations are digitized with the same equipment as the
cranial landmarks:

```json
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x: left helix-tragus junction (LHJ) → right helix-tragus junction (RHJ); y: inion → nasion; z: midpoint between mastoid processes → vertex",
    "EMGCoordinateSystemUnits": "m"
}
```

### Example 2: `*_coordsystem.json` for measured electrode positions in a single coordinate system defined by anatomical landmarks

Here, a coordinate system is defined based on percentage of distances between anatomical
landmarks of the forearm, and is suitable for localizing individual electrodes on the
same body part:

```json
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x: radial styloid process (RSP) → ulnar styloid process (USP); y: oleacranon process → cubital fossa; z: RSP-USP → lateral humerus epicondyle",
    "EMGCoordinateSystemUnits": "percent"
}
```

### Example 3: multiple `*_coordsystem.json` files for measured electrode positions in multiple anatomically-defined coordinate systems

Here, separate anatomically-based coordinate systems are defined for electrodes above and
below the elbow joint, and each is given a unique name ("Forearm" or "Humerus") which can
be referenced in the `coordinate_system` column of `*_electrodes.tsv`:

```json title="*_space-Forearm_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x: radial styloid process (RSP) → ulnar styloid process (USP); y: oleacranon process → cubital fossa; z: RSP-USP → lateral humerus epicondyle",
    "EMGCoordinateSystemUnits": "percent"
}
```

```json title="*_space-Humerus_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x: medial humerus epicondyle (MHE) → lateral humerus epicondyle (LHE), y: oleacranon process → cubital fossa, z: MHE-LHE → greater humerus tubercule",
    "EMGCoordinateSystemUnits": "percent"
}
```

### Example 4: multiple `*_coordsystem.json` files for nested/anchored coordinate systems

Here, coordinate systems for the _relative_ locations of electrodes in grids or groups are
given in "child" coordinate systems ("BicepGrid", "VolarForearmGrid", "DorsalForearmGrid"),
each of which is anchored to a "parent" coordinate system that is defined anatomically:

```json title="*_space-BicepGrid_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x-axis left → right, y-axis bottom → top, when grid is oriented with leads at the bottom",
    "EMGCoordinateSystemUnits": "mm",
    "ParentCoordinateSystem": "Humerus",
    "AnchorCoordinates": [40, 70, 0],
    "AnchorElectrode": "E1"
}
```

```json title="*_space-VolarForearmGrid_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x-axis left → right, y-axis bottom → top, when grid is oriented with leads at the bottom",
    "EMGCoordinateSystemUnits": "mm",
    "ParentCoordinateSystem": "Forearm",
    "AnchorCoordinates": [25, 50, 10],
    "AnchorElectrode": "E1"
}
```

```json title="*_space-DorsalForearmGrid_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x-axis left → right, y-axis bottom → top, when grid is oriented with leads at the bottom",
    "EMGCoordinateSystemUnits": "mm",
    "ParentCoordinateSystem": "Forearm",
    "AnchorCoordinates": [75, 0, 90],
    "AnchorElectrode": "E1",
}
```

```json title="*_space-Forearm_coordsystem.json"
{
    "EMGCoordinateSystem": "Other",
    "EMGCoordinateSystemDescription": "x: radial styloid process (RSP) → ulnar styloid process (USP); y: oleacranon process → cubital fossa; z: RSP-USP → lateral humerus epicondyle",
    "EMGCoordinateSystemUnits": "percent"
}
```

```json title="*_space-Humerus_coordsystem.json"
{
        "EMGCoordinateSystem": "Other",
        "EMGCoordinateSystemDescription": "x: medial humerus epicondyle (MHE) → lateral humerus epicondyle (LHE), y: oleacranon process → cubital fossa, z: MHE-LHE → greater humerus tubercule",
        "EMGCoordinateSystemUnits": "percent"
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

If there are photos of the electrodes, the [`recording-<label>`](../appendices/entities.md#recording) entity
MAY be specified, if separate photos are provided of each EMG device and the devices recorded
into separate data files.
The [`ses-<label>`](../appendices/entities.md#ses) entity may be used to specify when the photo was taken.

### Example `*_photo.<extension>`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "ses-01":{
         "sub-01_ses-01_recording-DorsalForearmGrid_photo.jpg": "",
         "...": "",
         },
      }
   }
) }}

![photo of EMG electrodes](images/emg_electrodes1.png "photo of an EMG electrode grid on a subject's forearm")
