# Physiological and other continuous recordings

Template:

```Text
sub-<label>/[ses-<label>/]
    func/
        <matches>[_recording-<label>]_physio.tsv.gz
        <matches>[_recording-<label>]_physio.json
        <matches>[_recording-<label>]_stim.tsv.gz
        <matches>[_recording-<label>]_stim.json
```

Optional: Yes

Where `<matches>` corresponds to task file name without the `_bold.nii[.gz]`
suffix. For example: `sub-control01_task-nback_run-1`. If the same continuous
recording has been used for all subjects (for example in the case where they
all watched the same movie) one file can be used and placed in the root
directory. For example:`task-movie_stim.tsv.gz`

Physiological recordings such as cardiac and respiratory signals and other
continuous measures (such as parameters of a film or audio stimuli) can be
specified using two files: a gzip compressed TSV file with data (without header
line) and a JSON for storing the following metadata fields:

| Field name        | Definition                                                                                                                                                          |
| :---------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SamplingFrequency | REQUIRED. Sampling frequency in Hz of all columns in the file.                                                                                                      |
| StartTime         | REQUIRED. Start time in seconds in relation to the start of acquisition of the first data sample in the corresponding neural dataset (negative values are allowed). |
| Columns           | REQUIRED. Names of columns in file.                                                                                                                                 |

Additional metadata may be included as in
[any TSV file](../02-common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series.
Please note that in contrast to other TSV files this one does not include a
header line. Instead the name of columns are specified in the JSON file.
This is to improve compatibility with existing software (FSL PNM) as
well as make support for other file formats possible in the future.
Recordings with different sampling frequencies and/or starting times should be
stored in separate files.
The following naming conventions should be used for column names:

| Column name | Definition                                           |
| :---------- | :--------------------------------------------------- |
| cardiac     | continuous pulse measurement                         |
| respiratory | continuous breathing measurement                     |
| trigger     | continuous measurement of the scanner trigger signal |

Any combination of those three can be included as well as any other stimuli
related continuous variables (such as low level image properties in a video
watching paradigm).

Physiological recordings (including eye tracking) should use the `_physio`
suffix, and signals related to the stimulus should use `_stim` suffix. For
motion parameters acquired from scanner side motion correction please use
`_physio` suffix.

More than one continuous recording file can be included (with different sampling
frequencies). In such case use different labels. For example:
`_recording-contrast`, `_recording-saturation`. The full file name could then
look like this: `sub-control01_task-nback_run-2_recording-movie_stim.tsv.gz`

For multi-echo data, physio.tsv file is applicable to all echos of particular
run. For eg:

```Text
sub-01_task-cuedSGT_run-1_physio.tsv.gz
sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
```

Example:

```Text
sub-control01/
    func/
        sub-control01_task-nback_physio.tsv.gz
```

(after decompression)

```Text
34  110 0
44  112 0
23  100 1
```

```Text
sub-control01/
    func/
        sub-control01_task-nback_physio.json
```

```JSON
{
   "SamplingFrequency": 100.0,
   "StartTime": -22.345,
    "Columns": ["cardiac", "respiratory", "trigger"],
   "cardiac": {
       "Units": "mV"
   }
}
```
