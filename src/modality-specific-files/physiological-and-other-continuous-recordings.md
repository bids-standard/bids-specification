# Physiological and other continuous recordings

Physiological recordings such as cardiac and respiratory signals and other
continuous measures (such as parameters of a film or audio stimuli) MAY be
specified using two files:

1.  a [gzip](https://datatracker.ietf.org/doc/html/rfc1952)
    compressed TSV file with data (without header line)

1.  a JSON file for storing metadata fields (see below)

[Example datasets](https://bids-standard.github.io/bids-examples/#dataset-index)
with physiological data have been formatted using this specification
and can be used for practical guidance when curating a new dataset:

-   [`7t_trt`](https://github.com/bids-standard/bids-examples/tree/master/7t_trt)
-   [`ds210`](https://github.com/bids-standard/bids-examples/tree/master/ds210)

Template:

```Text
sub-<label>/[ses-<label>/]
    <datatype>/
        <matches>[_recording-<label>]_physio.tsv.gz
        <matches>[_recording-<label>]_physio.json
        <matches>[_recording-<label>]_stim.tsv.gz
        <matches>[_recording-<label>]_stim.json
```

Continuous physiological recordings SHOULD use `_physio.<tsv.gz|json>`
pairs, for example:

- pulse measurement,
- electrocardiogram,
- respiratory movement measured with a respiration belt,
- gas concentration,
- eye tracking,
- head-motion parameters estimated by the MRI scanner.

Continuous signals related to the stimulus SHOULD use the `_stim` suffix.

For the template directory name, `<datatype>` can correspond to any data
recording modality, for example `func`, `anat`, `dwi`, `meg`, `eeg`, `ieeg`,
or `beh`.

In the template filenames, the `<matches>` part corresponds to task filename
before the suffix.
For example for the file `sub-01_task-nback_run-1_bold.nii.gz`,
`<matches>` would correspond to `sub-01_task-nback_run-1`.

Note that when supplying a `<matches>_<physio|stim>.tsv.gz` file,
an accompanying `<matches>_<physio|stim>.json` MUST be supplied as well.

The [`recording-<label>`](../appendices/entities.md#recording)
entity MAY be used to distinguish between several recording files.
For example, `sub-01_task-bart_recording-cardio_physio.tsv.gz` to contain
electrocardiography recordings in a certain sampling frequency, and
`sub-01_task-bart_recording-breathing_physio.tsv.gz` to contain respiratory

The following table specifies metadata fields for the
`<matches>_<physio|stim>.json` file.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["continuous.Continuous", "continuous.Physio", "continuous.PhysioTypeRecommended"]) }}

Additional metadata may be included as in
[any TSV file](../common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series.
Please note that, in contrast to other TSV files in BIDS, the TSV files specified
for physiological and other continuous recordings MUST NOT include a header
line.
Instead, the name of columns MUST be specified in the JSON file (see `Columns` field).
This is to improve compatibility with existing software (for example, FSL, PNM)
as well as to make support for other file formats possible in the future.
As in any TSV file, column names MUST NOT be blank (that is, an empty string),
and MUST NOT be duplicated within a single JSON file describing a headerless
TSV file.

Example `<matches>_physio.tsv.gz`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-nback_physio.tsv.gz": "",
         },
      },
   }
) }}

(after decompression)

```Text
34    110    0
44    112    0
23    100    1
```

Example of `<matches>_physio.json` including cardiac and respiratory
recordings at a sampling frequency of 100 Hz, with a column including the
scanner's trigger signal:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-nback_physio.json": "",
         },
      },
   }
) }}

```JSON
{
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "Columns": ["cardiac", "respiratory", "trigger"],
    "Manufacturer": "Brain Research Equipment ltd.",
    "cardiac": {
        "Description": "continuous pulse measurement",
        "Units": "mV"
        },
    "respiratory": {
        "Description": "continuous measurements by respiration belt",
        "Units": "mV"
        },
    "trigger": {
        "Description": "continuous measurement of the scanner trigger signal"
        }
}
```

General metadata fields include `SamplingFrequency`, `StartTime`, `Columns`,
and `Manufacturer`, in addition to individual column descriptions.
Each individual column in the TSV file MAY be documented as its own field in the JSON file
(identical to the practice in other TSV+JSON file pairs).
Here, only the `Description` and `Units` fields are shown, but any other of the
[defined fields](../common-principles.md#tabular-files) such as `TermURL`, `LongName`,
and so on, MAY be included.
In this example, the `"cardiac"` and `"respiratory"` time series are produced by devices from
the same manufacturer and follow the same sampling frequency.
To specify different sampling frequencies, starting times, manufacturers,
or any other nonuniform metadata value, the time series MUST be split into
separate files like `<matches>_recording-cardiac_physio.<tsv.gz|json>`
and `<matches>_recording-respiratory_physio.<tsv.gz|json>`.
In such cases, the [`recording-<label>`](../appendices/entities.md#recording)
entity MUST be used to distinguish these files.

If the same continuous recording has been used for all subjects (for example in
the case where they all watched the same movie), one file placed in the
root directory (for example, `<root>/task-movie_stim.<tsv.gz|json>`) MAY be used.

For multi-echo data, a single `_physio.<tsv.gz|json>` file without the
[`echo-<index>`](../appendices/entities.md#echo) entity applies to all echos of
a particular run.
For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
        "sub-01_task-cuedSGT_run-1_physio.tsv.gz": "",
        "sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz": "",
        "sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz": "",
        "sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz": "",
         },
      },
   }
) }}

**General column naming recommendation**.
To store pulse or breathing measurements, or the scanner trigger signal, the
following naming conventions MAY be used for the column names:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("physio.PhysioColumns") }}

Metadata sidecar files (`<matches>_physio.json`) MAY define the field
`PhysioType` to indicate a specific type of recording.
The default value of `PhysioType` is `"generic"`, and MUST be assumed
if the `PhysioType` metadata is not defined.
The allowed physiological recording types encoded by `PhysioType` and
their corresponding metadata specifications are in subsection
[Specific physiological signal types](#specific-physiological-signal-types)
below.

For example, the following metadata file:

```JSON
{
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "Columns": ["cardiac"],
    "cardiac": {
        "Description": "continuous pulse measurement",
        "Units": "mV"
    }
}
```

is equivalent to:

```JSON
{
    "PhysioType": "generic",
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "Columns": ["cardiac"],
    "cardiac": {
        "Description": "continuous pulse measurement",
        "Units": "mV"
    }
}
```

## Discontinuous data

Discontinuous data associated with continuous recordings
stored in `<matches>_physio.tsv.gz` files MAY be specified
with two files:

1.  a [gzip](https://datatracker.ietf.org/doc/html/rfc1952)
    compressed TSV file with data (without header line)

1.  a JSON file for storing metadata fields (see below)

Template:

```Text
sub-<label>/[ses-<label>/]
    <datatype>/
        <matches>[_recording-<label>]_physioevents.tsv.gz
        <matches>[_recording-<label>]_physioevents.json
```

Placeholders such as `<datatype>` and `<matches>` are defined
as above for the template of continous recordings.
The [`recording-<label>`](../appendices/entities.md#recording)
entity is OPTIONAL, but MUST be matched with an existing
`<matches>[_recording-<label>]_physio.tsv.gz` file.

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

The `ForeignIndexColumn` metadata specifies whether
`<matches>[_recording-<label>]_physio.tsv.gz` files are
implicitly or explicitly indexed.

**Implicit indexing of `<matches>_physioevents.tsv.gz` files**.
When `ForeignIndexColumn` is not provided, a column with
name `"foreign_index"` SHOULD be defined.
The `"foreign_index"` column corresponds to the zero-based row number
of the associated `<matches>_physio.tsv.gz` file.
The `"foreign_index"` column accepts negative values to register
events occurred before the recording(s) in the corresponding
`<matches>_physio.tsv.gz` file started.

For example, considering the following structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-nback_physio.json": "",
         "sub-01_task-nback_physio.tsv.gz": "",
         "sub-01_task-nback_physioevents.json": "",
         "sub-01_task-nback_physioevents.tsv.gz": "",
         },
      },
   }
) }}

where the decompressed contents of `sub-01_task-nback_physio.tsv.gz`
are:

```TSV linenums=1
10.1
10.0
9.5
9.2
9.0
10.2
10.3
10.1
```

and the `ForeignIndexColumn` is not defined in the
`sub-01_task-nback_physioevents.json` file:

```JSON
{
    "Columns": ["foreign_index", "message"],
    "Description": "Messages logged by the measurement device"
}
```

then, the decompressed contents of the corresponding
TSV file, `sub-01_task-nback_physioevents.tsv.gz` may be:

```TSV
-4   "Ready"
2    "Synchronous recalibration triggered"
5    "External message received: new block"
```

In this case, the first column lists the indexes (zero-based row index)
in the `sub-01_task-nback_physio.tsv.gz`.
The first entry, with `foreign_index` set to 2 maps to the third line of the
`sub-01_task-nback_physio.tsv.gz`, indicating that the message
*Synchronous recalibration triggered* was logged at the same time the recording
registered the value `9.5`.
Likewise, the second message was logged when the recording later registered a
value of `10.2`.
As negative indexes are allowed, the first *Ready* message ocurred four sampling
cycles before the first recorded measurement.
For example, if `SamplingFrequency` in `sub-01_task-nback_physio.json`
is set to 100 Hz and `StartTime` is -22.345 s, then the *Ready* message was recorded
0.04 s before the first sample, therefore at -22.305 s of experiment time.

**Explicit indexing of `<matches>_physioevents.tsv.gz` files (RECOMMENDED)**.
When the `ForeignIndexColumn` defines a value such as `"timestamp"`,
that specific column name MUST be present in both
the `<matches>_physioevents.tsv.gz` and its corresponding
`<matches>_physio.tsv.gz`.
In that case, all values of the `"timestamp"` column of the
`<matches>_physioevents.tsv.gz` file MUST exist within the
`"timestamp"` column of the corresponding
`<matches>_physio.tsv.gz` file.

For example, let us consider the previous structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
         "sub-01_task-nback_physio.json": "",
         "sub-01_task-nback_physio.tsv.gz": "",
         "sub-01_task-nback_physioevents.json": "",
         "sub-01_task-nback_physioevents.tsv.gz": "",
         },
      },
   }
) }}

However, the `sub-01_task-nback_physio.json` will define now an extra
column called `"timestamp"`:

```JSON
{
    "SamplingFrequency": 100.0,
    "StartTime": -22.345,
    "Columns": ["cardiac", "timestamp"],
    "cardiac": {
        "Description": "continuous pulse measurement",
        "Units": "mV"
    },
    "timestamp": {
        "Description": "a continously increasing identifier of the sampling time registered by the device"
    }
}
```

The decompressed contents of `sub-01_task-nback_physio.tsv.gz`
are now:

```TSV linenums=1
10.1    13894432329
10.0    13894432330
9.5    13894432331
9.2    13894432332
9.0    13894432333
10.2    13894432334
10.3    13894432335
10.1    13894432336
```

Then, the `sub-01_task-nback_physioevents.json` MAY define
the `ForeignIndexColumn` for indexing:

```JSON
{
    "Columns": ["timestamp", "message"],
    "Description": "Messages logged by the measurement device",
    "ForeignIndexColumn": "timestamp"
}
```

The decompressed contents of the corresponding TSV file,
`sub-01_task-nback_physioevents.tsv.gz` could read now:

```TSV
13894432325    "Ready"
13894432331    "Synchronous recalibration triggered"
13894432334    "External message received: new block"
```

## Specific physiological signal types

### Eye-tracking

Setting `PhysioType` to the keyword `"eyetrack"` specifies that
the physiological recordings in the `<matches>_physio.tsv.gz` have
been acquired with an *eye-tracker*.
In the following, *eye-tracker* refers to the apparatus allowing
the recording of gaze position and/or pupil size.

Eye-tracking data MUST be stored following the general specifications
for `"generic"` physiological recordings.
However, it is REQUIRED that recordings corresponding to each eye
(and *merged* signals for binocular eye-trackers providing a third
recording) are split into files with different
[`recording-<label>`](../appendices/entities.md#recording).
Therefore, the [`recording-<label>`](../appendices/entities.md#recording)
is REQUIRED with eye-tracking data.

For example, for a binocular eye-tracker producing three signals
(left and right eyes, plus a *merged* recording), the file structure
is:
<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
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
   }
) }}

The labels `"eye1"`, `"eye2"`, and `"eye3"` for the
[`recording-<label>`](../appendices/entities.md#recording) entity
are RECOMMENDED.

The above example is simplified for a monocular eye-tracker as follows:
<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
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
    "continuous.Physio",
    "continuous.PhysioTypeRequired",
    "continuous.EyeTrack"
]) }}

We highly RECOMMEND to document the calibration metadata carefully.
Note that the following fields from `*_events.json` files
are REQUIRED as they are considered essential in eye-tracking data analysis:

-   `StimulusPresentation.ScreenSize`,
-   `StimulusPresentation.ScreenResolution`,
-   `StimulusPresentation.ScreenDistance`.

**Example metadata sidecar**.
Given the above example file structures, a corresponding
`sub-01_task-visualSearch_recording-eye1_physio.json` sidecar
could read:

```JSON
{
    "Manufacturer": "SR-Research",
    "ManufacturersModelName": "EYELINK II CL v4.56 Aug 18 2010",
    "DeviceSerialNumber": "17535483",
    "SoftwareVersion": "SREB1.10.1630 WIN32 LID:F2AE011 Mod:2017.04.21 15:19 CEST",
    "SamplingFrequency": 1000,
    "SampleCoordinateUnits": "pixel",
    "SampleCoordinateSystem": "gaze-on-screen",
    "EnvironmentCoordinates": "top-left",
    "RecordedEye": "both",
    "ScreenAOIDefinition": ["square",
                            [100, 150, 300, 350]]
}
```

Content of `sub-01_task-VisualSearch_events.json`:

```JSON
{
   "TaskName": "Visual Search",
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "StimulusPresentation": {
       "ScreenDistance": 60,
       "ScreenRefreshRate": 60,
       "ScreenResolution": [1024, 768],
       "ScreenSize": [0.386, 0.29]
   }
}
```
