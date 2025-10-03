# Physiological recordings

!!! example "Example datasets"

      [Example datasets](https://bids-standard.github.io/bids-examples/#dataset-index)
      with physiological data have been formatted using this specification
      and can be used for practical guidance when curating a new dataset:

      -   [`7t_trt`](https://github.com/bids-standard/bids-examples/tree/master/7t_trt)
      -   [`ds210`](https://github.com/bids-standard/bids-examples/tree/master/ds210)

## General specifications

Continuous (that is, regularly sampled over time at a fixed frequency)
physiological recordings such as cardiac and respiratory signals, and
asynchronous events corresponding to those signals MAY be specified using
[compressed tabular files](../common-principles.md#compressed-tabular-files)
([TSV.GZ file](../glossary.md#tsvgz-extensions)).
TSV.GZ files MUST be accompanied by a JSON file with the same name as their
corresponding tabular file but with a `.json` extension.

{{ MACROS___make_filename_template(
       "raw",
       placeholders=True,
       show_entities=["recording"],
       suffixes=["physio", "physioevents"]
   )
}}

The [`recording-<label>`](../appendices/entities.md#recording)
entity is OPTIONAL, and is [described below](#continuous-physiological-recordings).

!!! warning "Caution"

    Columns of TSV.GZ files MUST be defined in the corresponding JSON sidecar
    and the tabular content MUST NOT include a header line.

    As a consequence, when supplying a `<matches>_<physio|physioevents>.tsv.gz` file,
    an accompanying `<matches>_<physio|physioevents>.json` MUST be supplied as well.

For multi-echo data, a single `_physio.<tsv.gz|json>` file without the
[`echo-<index>`](../appendices/entities.md#echo) entity applies to all echos of
a particular run.
For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-nback_run-1_echo-1_bold.nii.gz": "",
      "sub-01_task-nback_run-1_echo-2_bold.nii.gz": "",
      "sub-01_task-nback_run-1_echo-3_bold.nii.gz": "",
      "sub-01_task-nback_run-1_physio.tsv.gz": "",
    },
  },
}) }}

This specification section first describes the organization of
[continuous physiological recordings](#continuous-physiological-recordings), and
then [events corresponding to the physiological recordings](#physiology-events).
Finally, the remainder of the document describes
[specific types of continuous recordings](#specific-physiological-signal-types)
such as [eye-tracking](#eye-tracking).

## Continuous physiological recordings

Continuous physiological recordings, such as pulse monitoring,
electrocardiogram, respiratory movement measured with a respiration belt,
gas concentration, or eye-tracking, MUST use `_physio.<tsv.gz|json>` pairs.

### Storing different recordings
The [`recording-<label>`](../appendices/entities.md#recording)
entity MAY be used to distinguish between several recording files.
Recordings with different metadata such as sampling frequencies
or recording device MUST be stored in separate files with different
[`recording-<label>`](../appendices/entities.md#recording) entities.
For example, given a BOLD acquisition of a breath-holding task (`task-bht`)
for which pulse and respiratory movement were sampled at different frequencies,
recordings are separated as follows:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-bht_bold.nii.gz": "",
      "sub-01_task-bht_recording-cardiac_physio.json": "",
      "sub-01_task-bht_recording-cardiac_physio.tsv.gz": "",
      "sub-01_task-bht_recording-respiratory_physio.json": "",
      "sub-01_task-bht_recording-respiratory_physio.tsv.gz": "",
    },
  },
}) }}

**Metadata fields for `<matches>_physio.json` files**.
General metadata fields include `SamplingFrequency`, `StartTime`, `Columns`,
and `Manufacturer`, in addition to individual column descriptions.
Each individual column in the TSV file MAY be documented as its own field in the JSON file
(identical to the practice in other TSV+JSON file pairs).

!!! warning "Caution"

    Recordings with different key metadata MUST be split into separate files.

When key metadata such as sampling frequencies, manufacturers varies between recordings,
tabular data MUST be split into separate files.
In such cases, the [`recording-<label>`](../appendices/entities.md#recording)
entity MUST be used to distinguish these files.

Metadata sidecar files (`<matches>_physio.json`) MAY define the field
`PhysioType` to indicate a specific type of recording.
The default value of `PhysioType` is `"generic"`, and MUST be assumed
if the `PhysioType` metadata is not defined.
Specific recording types (that is, when `PhysioType` takes a valid value other than `"generic"`)
have separate prescriptions for columns in the TSV.GZ files and corresponding metadata
specifications.

!!! tip "RECOMMENDED"

    Using specific recording types is RECOMMENDED when available in the
    specification.

    The allowed physiological recording types encoded by `PhysioType` and
    their corresponding metadata specifications are described in subsection
    [Specific physiological signal types](#specific-physiological-signal-types)
    below, and its subsections:

    -   eye-tracking ([subsection Eye-tracking](#eye-tracking)).

The following table specifies metadata fields for `"generic"` recordings:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["continuous.Continuous", "continuous.PhysioTypeRecommended"]) }}

**Hardware information**.
Details about the hardware MAY be stored with the following metadata fields.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["continuous.PhysioHardware"]) }}

Additional metadata may be included as in
[any TSV file](../common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series.

**Column naming recommendations for `"generic"` recordings.**
To store pulse or breathing measurements, or the scanner trigger signal,
the following naming conventions SHOULD be used for the column names:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("physio.PhysioColumns") }}

Please note that the specification of columns such as `cardiac`, `respiratory`, and `trigger` above
follow the general specifications for [tabular files](../common-principles.md#tabular-files):

<!-- This table should be the same as that in the common-principles.md file,
	   unless the specification wants to specifically deviate for physio at some point.
-->
{{ MACROS___make_metadata_table(
   {
        "LongName": "OPTIONAL",
        "Description": (
            "RECOMMENDED",
            "The description of the column.",
        ),
        "Levels": "RECOMMENDED",
        "Units": "RECOMMENDED",
        "Delimiter": "OPTIONAL",
        "TermURL": "RECOMMENDED",
        "HED": "OPTIONAL",
   }
) }}

**Examples**.
Let's encode cardiac and respiratory recordings, as well as a trigger signal,
the three of them sampled at 100.0 Hz by the same device during a behavioral task:
<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-nback_physio.json": "",
      "sub-01_task-nback_physio.tsv.gz": "",
    },
  },
}) }}

In this example, the contents of `sub-01_task-nback_physio.tsv.gz`
after decompression are:

```tsvgz {linenums="1"}
34	110	0
44	112	0
23	100	1
```

and the header-less TSV.GZ contents are described with the following
metadata `sub-01_task-nback_physio.json` where the `Columns` field defines
the names corresponding to the three columns above:

```JSON
{
    "Columns": ["cardiac", "respiratory", "trigger"],
    "Manufacturer": "Brain Research Equipment ltd.",
    "PhysioType": "generic",
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "cardiac": {
      "Description": "continuous pulse measurement",
      "Units": "mV"
    },
    "respiratory": {
      "Description": "continuous measurements by respiration belt",
      "Units": "mV"
    },
    "trigger": {
      "Description": "continuous measurement of the scanner trigger signal",
      "Units": "V"
    }
}
```

The example shows the three REQUIRED metadata entries `Columns`, `SamplingFrequency`,
and `StartTime`.
Columns are further described following the specifications for
[tabular files](../common-principles.md#tabular-files),
indicating `Description` and `Units` fields.
Other fields, such as `TermURL`, `LongName`, MAY be included.

Because a missing `PhysioType` is assumed to be `"generic"`, the following sidecar is equivalent:

```JSON
{
    "Columns": ["cardiac", "respiratory", "trigger"],
    "Manufacturer": "Brain Research Equipment ltd.",
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "cardiac": {
      "Description": "continuous pulse measurement",
      "Units": "mV"
    },
    "respiratory": {
      "Description": "continuous measurements by respiration belt",
      "Units": "mV"
    },
    "trigger": {
      "Description": "continuous measurement of the scanner trigger signal",
      "Units": "V"
    }
}
```

If the `"cardiac"` and `"respiratory"` signals above were acquired at different
sampling frequencies, then the recordings MUST be separated into two files
disambiguated by the [`recording-<label>`](../appendices/entities.md#recording)
entity:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-nback_recording-cardiac_physio.json": "",
      "sub-01_task-nback_recording-cardiac_physio.tsv.gz": "",
      "sub-01_task-nback_recording-respiratory_physio.json": "",
      "sub-01_task-nback_recording-respiratory_physio.tsv.gz": "",
    },
  },
}) }}

## Physiology "events"

Discontinuous data associated with continuous recordings
stored in `<matches>_physio.tsv.gz` files MAY be specified
following the summary template pattern above.

Physiology "events" files `<matches>_recording-<label>_physioevents.tsv.gz`
MUST follow specific column specifications:

<!--
This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/physio.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("physio.PhysioEventsColumns") }}

The following table specifies metadata fields for the
`<matches>[_recording-<label>]_physioevents.json` file.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["continuous.PhysioEvents"]) }}

The REQUIRED `OnsetSource` metadata specifies the interpretation of
the values of the `onset` column.
If `OnsetSource` is the name of a column in the associated
`<matches>[_recording-<label>]_physio.tsv.gz` file, the values have the same interpretation
as values in the named column.

For example, considering the following structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-nback_physio.json": "",
      "sub-01_task-nback_physio.tsv.gz": "",
      "sub-01_task-nback_physioevents.json": "",
      "sub-01_task-nback_physioevents.tsv.gz": "",
    },
  },
}) }}

The decompressed contents of `sub-01_task-nback_physio.tsv.gz` are:

```{.text noheader="1" linenums="1"}
13894432329	10.1
13894432330	10.0
13894432331     9.5
13894432332     9.2
13894432333     9.0
13894432334	10.2
13894432335	10.3
13894432336	10.1
```

And `sub-01_task-nback_physio.json` defines `timestamp` column:

```JSON
{
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "Columns": ["timestamp", "cardiac"],
    "cardiac": {
        "Description": "continuous pulse measurement",
        "Units": "mV"
    },
    "timestamp": {
        "Description": "a continuously increasing identifier of the sampling time registered by the device",
        "Units": "ms",
        "Origin": "System startup"
    }
}
```

The decompressed contents of the corresponding `sub-01_task-nback_physioevents.tsv.gz` are:

```{.text noheader="1" linenums="1"}
13894432325	Ready
13894432331	Synchronous recalibration triggered
13894432334	External message received: new block
```

To indicate that the first column (`onset`) is to be interpreted as a timestamp,
the `OnsetSource` MUST be set to `"timestamp"` in `sub-01_task-nback_physioevents.json`:

```JSON
{
    "Columns": ["onset", "message"],
    "Description": "Messages logged by the measurement device",
    "OnsetSource": "timestamp"
}
```

If there is no appropriate source column in
`<matches>[_recording-<label>]_physio.tsv.gz`, `OnsetSource` MAY be set to `"n/a"`.
In this case, the values of `onset` MUST be interpreted as row indices
into the `physio` file, with the first row having index zero (`0`).
Negative onsets are possible, and such events are interpreted as occurring prior
to the start of the recording, at the same sampling rate.

For example, the above `sub-01_task-nback_physioevents.tsv.gz` could be equivalently
written:

```{.text noheader="1"}
-3	Ready
3	Synchronous recalibration triggered
6	External message received: new block
```

To indicate that the first column (`onset`) is to be interpreted as an index,
the `OnsetSource` is set to `"n/a"` in `sub-01_task-nback_physioevents.json`:

```JSON
{
    "Columns": ["onset", "message"],
    "Description": "Messages logged by the measurement device",
    "OnsetSource": "n/a"
}
```

## Specific physiological signal types

### Eye-tracking

<!--
1. Datasets will be updated later to adapt to the agreed format.
2. We aim at adding a last example converting published dataset from openeuro.
-->
!!! example "Example datasets"

    [Example datasets](https://bids-standard.github.io/bids-examples/#dataset-index)
    with eye-tracking data have been formatted using this specification
    and can be used for practical guidance when curating a new dataset:

    -   Combined fMRI and eye-tracking data in a resting-state task, measured with
        an Eyelink (SR research). Human participant kept their gaze steady at the
        screen center.

        [BIDS dataset](https://openneuro.org/datasets/ds004158)

    -   Combined behavioral and eye-tracking data, measured with and Eyelink
        (SR Research). Human participants freely viewed as set of natural images.
        Published paper: https://doi.org/10.1523/ENEURO.0287-23.2023

        [BIDS dataset](https://github.com/julia-pfarr/natImSac_BIDSexample)

Setting `PhysioType` to the keyword `"eyetrack"` specifies that
the physiological recordings in the `<matches>_physio.tsv.gz` have
been acquired with an *eye-tracker*.
In the following, *eye-tracker* refers to the apparatus allowing
the recording of gaze position, and, optionally, pupil size.

Eye-tracking data MUST be stored following the general specifications
for `"generic"` physiological recordings.
However, it is REQUIRED that recordings corresponding to each eye
(and/or *cyclopean* or averaged signals for binocular eye-trackers providing
a third recording) are split into files with different
[`recording-<label>`](../appendices/entities.md#recording).
Therefore, the use of [`recording-<label>`](../appendices/entities.md#recording)
is REQUIRED with eye-tracking data.
The values `"eye1"`, `"eye2"`, and `"eye3"` are RECOMMENDED as the respective labels
for the [`recording-<label>`](../appendices/entities.md#recording) entity.

!!! danger "MANDATORY metadata"

    The correspondence of labels and the recorded eye MUST be encoded
    by the MANDATORY `RecordedEye` metadata.

    The [`recording-<label>`](../appendices/entities.md#recording) entity
    MAY take other values such as `"left"`, `"cyclopean"`, or `"right"` corresponding
    to the `RecordedEye` metadata.
    However, it is RECOMMENDED that metadata is not encoded in the file names to avoid
    conflicts between filenames and metadata.
    For example, if [`recording-<label>`](../appendices/entities.md#recording) takes
    the value `"left"` but the corresponding sidecar JSON file contains a definition of
    `RecordedEye` being `"right"`.

Eye-tracking files `<matches>_recording-<label>_physio.tsv.gz` MUST follow
specific column prescriptions:

<!--
This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/eyetrack.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("physio.PhysioEyeTracking") }}

Please note that the specification of columns such as `timestamp`, `x_coordinate`, `y_coordinate`, and `pupil_size`
follow the general specifications for [tabular files](../common-principles.md#tabular-files) and MAY define
metadata fields such as [`LongName`](../glossary.md#objects.metadata.LongName),
[`Description`](../glossary.md#objects.metadata.Description),
[`Levels`](../glossary.md#objects.metadata.Levels), or
[`TermURL`](../glossary.md#objects.metadata.TermURL).
However, in the case of eye-tracking, the metadata entry [`Units`](../glossary.md#objects.metadata.Units),
becomes REQUIRED for the columns `x_coordinate` and `y_coordinate`:

{{ MACROS___make_metadata_table(
   {
        "Units": "REQUIRED",
   }
) }}

The following table specifies metadata fields for the
`<matches>_recording-<label>_physio.json` file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table([
    "continuous.Continuous",
    "continuous.PhysioHardware",
    "continuous.PhysioTypeRequired",
    "continuous.EyeTrack"
]) }}

Comprehensively documenting the calibration metadata is RECOMMENDED.

Eye-tracking files `<matches>_recording-<label>_physio.tsv.gz` MAY be annotated
with a corresponding `<matches>_recording-<label>_physioevents.tsv.gz` file.
The `<matches>_recording-<label>_physioevents.tsv.gz` file MAY be employed to
record discontinuous model parameters generated by the eye-tracker, for example,
those derived from the saccade and blinks model some eye-trackers produce.

!!! warning "Important"

    The following fields pertaining to `<matches>_events.json` of tasks that were acquired
    with the simultaneous recording of eye-tracking escalate to REQUIRED as they are considered
    essential in eye-tracking data analysis:

    -   `StimulusPresentation.ScreenDistance`,
    -   `StimulusPresentation.ScreenOrigin`,
    -   `StimulusPresentation.ScreenResolution`,
    -   `StimulusPresentation.ScreenSize`.

**Examples**.
The recordings produced by a monocular eye-tracker during a
visual search task may display the following structure:
<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-visualSearch_bold.json": "",
      "sub-01_task-visualSearch_bold.nii.gz": "",
      "sub-01_task-visualSearch_events.json": "",
      "sub-01_task-visualSearch_events.tsv": "",
      "sub-01_task-visualSearch_recording-eye1_physio.json": "",
      "sub-01_task-visualSearch_recording-eye1_physio.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye1_physioevents.json": "",
      "sub-01_task-visualSearch_recording-eye1_physioevents.tsv.gz": ""
    },
  },
}) }}

The above example is extended to a binocular eye-tracker producing three signals
(left and right eyes, plus a *cyclopean* recording), as follows:
<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-visualSearch_bold.json": "",
      "sub-01_task-visualSearch_bold.nii.gz": "",
      "sub-01_task-visualSearch_events.json": "",
      "sub-01_task-visualSearch_events.tsv": "",
      "sub-01_task-visualSearch_recording-eye1_physio.json": "",
      "sub-01_task-visualSearch_recording-eye1_physio.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye1_physioevents.json": "",
      "sub-01_task-visualSearch_recording-eye1_physioevents.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye2_physio.json": "",
      "sub-01_task-visualSearch_recording-eye2_physio.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye2_physioevents.json": "",
      "sub-01_task-visualSearch_recording-eye2_physioevents.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye3_physio.json": "",
      "sub-01_task-visualSearch_recording-eye3_physio.tsv.gz": "",
      "sub-01_task-visualSearch_recording-eye3_physioevents.json": "",
      "sub-01_task-visualSearch_recording-eye3_physioevents.tsv.gz": ""
    },
  },
}) }}

Given the above example file structures, a corresponding
`sub-01_task-visualSearch_recording-eye1_physio.json` sidecar
could read:

```JSON
{
    "DeviceSerialNumber": "17535483",
    "Columns": ["timestamp", "x_coordinate", "y_coordinate", "pupil_size"],
    "Manufacturer": "SR-Research",
    "ManufacturersModelName": "EYELINK II CL v4.56 Aug 18 2010",
    "PhysioType": "eyetrack",
    "RecordedEye": "right",
    "SampleCoordinateSystem": "gaze-on-screen",
    "SamplingFrequency": 1000,
    "SoftwareVersion": "SREB1.10.1630 WIN32 LID:F2AE011 Mod:2017.04.21 15:19 CEST",
    "ScreenAOIDefinition": [
        "square",
        [100, 150, 300, 350]
    ],
    "timestamp": {
        "Description": "a continuously increasing identifier of the sampling time registered by the device",
        "Units": "ms",
        "Origin": "System startup"
    },
    "x_coordinate": {
      "LongName": "Gaze position (x)",
      "Description": "Gaze position x-coordinate of the recorded eye, in the coordinate units specified in the corresponding metadata sidecar.",
      "Units": "pixel"
    },
    "y_coordinate": {
      "LongName": "Gaze position (y)",
      "Description": "Gaze position y-coordinate of the recorded eye, in the coordinate units specified in the corresponding metadata sidecar.",
      "Units": "pixel"
    },
    "pupil_size": {
        "Description": "Pupil area of the recorded eye as calculated by the eye-tracker in arbitrary units (see EyeLink's documentation for conversion).",
        "Units": "arbitrary"
    }
}
```

Content of `sub-01_task-VisualSearch_events.json`:

```JSON
{
   "TaskName": "Visual Search",
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "StimulusPresentation": {
       "ScreenDistance": 0.6,
       "ScreenOrigin": ["top", "left"],
       "ScreenRefreshRate": 60,
       "ScreenResolution": [1024, 768],
       "ScreenSize": [0.386, 0.29]
   }
}
```

**Example eye-tracking recording**.
Given the above `sub-01_task-visualSearch_recording-eye1_physio.json` metadata
specification, the decompressed content of the
`sub-01_task-visualSearch_recording-eye1_physio.tsv.gz` can be:

```TSV
7186799    416.29    267.39    4612.0
7186800    416.29    268.10    4623.0
7186801    416.20    269.00    4623.0
7186802    415.89    269.60    4613.0
7186803    415.70    269.20    4603.0
7186804    415.60    266.79    4591.0
7186805    415.79    264.60    4589.0
7186806    416.10    263.89    4587.0
7186807    416.29    265.20    4587.0
7186808    416.39    266.50    4588.0
7186809    416.50    266.79    4594.0
7186810    416.50    267.20    4599.0
7186811    416.10    268.00    4609.0
7186812    415.70    268.29    4612.0
7186813    416.00    268.60    4605.0
```

Example `sub-01_task-visualSearch_recording-eye1_physioevents.tsv.gz` corresponding
to the above eye-tracking recording, after decompressing:

```TSV
7184392    n/a    n/a         n/a    "NO Reply is disabled for function eyelink_cal_result"
7184392    n/a    n/a         n/a    "RECCFG CR 1000 2 0 R"
7184392    n/a    n/a         n/a    "ELCLCFG TOWER"
7186771    n/a    n/a         n/a    "First task trigger"
7186806    72     fixation    0      n/a
7186879    231    saccade     1      n/a
7187111    6186   fixation    0      n/a
7193298    216    saccade     1      n/a
7193515    1286   fixation    0      n/a
7194802    24     saccade     0      n/a
7194827    2403   fixation    0      n/a
7197231    17     saccade     0      n/a
7197249    1640   fixation    0      n/a
7198890    6      saccade     0      n/a
7198897    1105   fixation    0      n/a
7200003    233    saccade     1      n/a
7200237    184    fixation    0      n/a
7200422    15     saccade     0      n/a
7200438    264    fixation    0      n/a
```

where the first three rows are logged by the eye-tracker and the fourth row shows
a *message* asynchronously received by the eye-tracker.
The remainder of the rows contain a subset of parameters registered by the device,
derived from applying a model to identify saccades and blinks.
The corresponding `sub-01_task-visualSearch_recording-eye1_physioevents.json` sidecar
would read:

```JSON
{
    "Columns": ["onset", "duration", "trial_type", "blink", "message"],
    "Description": "Messages logged by the measurement device",
    "OnsetSource": "timestamp",
    "blink": {
      "Description": "Gives status of the eye.",
      "Levels": {
          "0": "Indicates if the eye was open.",
          "1": "Indicates if the eye was closed.",
      },
    },
    "message": {
      "Description": "String messages logged by the eye-tracker."
    },
    "trial_type": {
      "Description": "Event type as identified by the eye-tracker's model.",
      "Levels": {
          "fixation": "Indicates a fixation.",
          "saccade": "Indicates a saccade.",
      },
    }
}
```
