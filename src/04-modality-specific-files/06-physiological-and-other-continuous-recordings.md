# Physiological and other continuous recordings

Template:

```Text
sub-<label>/[ses-<label>/]
    <datatype>/
        <matches>[_recording-<label>]_physio.tsv.gz
        <matches>[_recording-<label>]_physio.json
        <matches>[_recording-<label>]_stim.tsv.gz
        <matches>[_recording-<label>]_stim.json
```

Optional: Yes

For the template directory name, `<datatype>` can correspond to any data
recording modality, for example `func`, `anat`, `dwi`, `meg`, `eeg`, `ieeg`,
or `beh`.

In the template file names, the `<matches>` part corresponds to task file name
before the suffix.
For example for the file `sub-control01_task-nback_run-1_bold.nii.gz`,
`<matches>` would correspond to `sub-control01_task-nback_run-1`.

The `recording-<label>` entity can be used to distinguish between several
recording files.
For example `sub-01_task-bart_recording-eyetracking_physio.tsv.gz` to contain
the eyetracking data in a certain sampling frequency, and
`sub-01_task-bart_recording-breathing_physio.tsv.gz` to contain respiratory
measurements in a different sampling frequency.

Physiological recordings (including eyetracking) SHOULD use the `_physio`
suffix, and signals related to the stimulus SHOULD use `_stim` suffix.

Physiological recordings such as cardiac and respiratory signals and other
continuous measures (such as parameters of a film or audio stimuli) can be
specified using two files: a gzip compressed TSV file with data (without header
line) and a JSON for storing the following metadata fields:

| Field name        | Definition                                                                                                                                                          |
| ------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SamplingFrequency | REQUIRED. Sampling frequency in Hz of all columns in the file.                                                                                                      |
| StartTime         | REQUIRED. Start time in seconds in relation to the start of acquisition of the first data sample in the corresponding neural dataset (negative values are allowed). |
| Columns           | REQUIRED. Names of columns in file.                                                                                                                                 |

Additional metadata may be included as in
[any TSV file](../02-common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series.
Please note that, in contrast to other TSV files in BIDS, the TSV files specified
for phsyiological and other continuous recordings *do not* include a header
line.
Instead the name of columns are specified in the JSON file.
This is to improve compatibility with existing software (e.g., FSL, PNM) as well
as to make support for other file formats possible in the future.

Example `*_physio.tsv.gz`:

```Text
sub-control01/
    func/
        sub-control01_task-nback_physio.tsv.gz
```

(after decompression)

```Text
34    110    0
44    112    0
23    100    1
```

Example `*_physio.json`:

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

## Recommendations for specific use cases

To store pulse or breathing measurements, or the scanner trigger signal, the
following naming conventions SHOULD be used for the column names:

| Column name | Definition                                           |
| ----------------- | ------------------------------------------------------- |
| cardiac     | continuous pulse measurement                         |
| respiratory | continuous breathing measurement                     |
| trigger     | continuous measurement of the scanner trigger signal |

For any other data to be specified in columns, the column names can be chosen
as deemed appropriate by the researcher.

Recordings with different sampling frequencies and/or starting times should be
stored in separate files.

If the same continuous recording has been used for all subjects (for example in
the case where they all watched the same movie), one file MAY be used and
placed in the root directory.
For example, `task-movie_stim.tsv.gz`

For motion parameters acquired from MRI scanner side motion correction, the
`_physio` suffix SHOULD be used.

For multi-echo data, a given `physio.tsv` file is applicable to all echos of
a particular run.
For example:

```Text
sub-01_task-cuedSGT_run-1_physio.tsv.gz
sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
```
