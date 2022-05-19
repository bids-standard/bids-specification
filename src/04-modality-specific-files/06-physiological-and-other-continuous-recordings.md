# Physiological and other continuous recordings

[Example datasets](https://github.com/bids-standard/bids-examples)
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

Optional: Yes

For the template directory name, `<datatype>` can correspond to any data
recording modality, for example `func`, `anat`, `dwi`, `meg`, `eeg`, `ieeg`,
or `beh`.

In the template filenames, the `<matches>` part corresponds to task filename
before the suffix.
For example for the file `sub-control01_task-nback_run-1_bold.nii.gz`,
`<matches>` would correspond to `sub-control01_task-nback_run-1`.

The [`recording-<label>`](../99-appendices/09-entities.md#recording) entity can be used to distinguish between several
recording files.
For example `sub-01_task-bart_recording-eyetracking_physio.tsv.gz` to contain
the eyetracking data in a certain sampling frequency, and
`sub-01_task-bart_recording-breathing_physio.tsv.gz` to contain respiratory
measurements in a different sampling frequency.

Physiological recordings (including eyetracking) SHOULD use the `_physio`
suffix, and signals related to the stimulus SHOULD use `_stim` suffix.

Physiological recordings such as cardiac and respiratory signals and other
continuous measures (such as parameters of a film or audio stimuli) can be
specified using two files: a [gzip](https://datatracker.ietf.org/doc/html/rfc1952)
compressed TSV file with data (without header line)
and a JSON file for storing the following metadata fields.

Note that when supplying a `*_<physio|stim>.tsv.gz` file, an accompanying
`*_<physio|stim>.json` MUST be supplied as well.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "SamplingFrequency": "REQUIRED",
      "StartTime": "REQUIRED",
      "Columns": "REQUIRED",
   }
) }}

Additional metadata may be included as in
[any TSV file](../02-common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series.
Please note that, in contrast to other TSV files in BIDS, the TSV files specified
for phsyiological and other continuous recordings *do not* include a header
line.
Instead the name of columns are specified in the JSON file.
This is to improve compatibility with existing software (for example, FSL, PNM)
as well as to make support for other file formats possible in the future.

Example `*_physio.tsv.gz`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-control01": {
      "func": {
         "sub-control01_task-nback_physio.tsv.gz": "",
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

Example `*_physio.json`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-control01": {
      "func": {
         "sub-control01_task-nback_physio.json": "",
         },
      },
   }
) }}

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

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "cardiac": "OPTIONAL",
      "respiratory": "OPTIONAL",
      "trigger": "OPTIONAL",
   }
) }}

For any other data to be specified in columns, the column names can be chosen
as deemed appropriate by the researcher.

Recordings with different sampling frequencies or starting times should be
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

### Other RECOMMENDED metadata for physiological data

The following RECOMMENDED metadata can also be added in the side-car JSON files
of any `*_<physio>.tsv.gz` file.

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Manufacturer": "RECOMMENDED",
      "ManufacturersModelName": "RECOMMENDED",
      "SoftwareVersions": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
   }
) }}

<!-- Link Definitions -->
