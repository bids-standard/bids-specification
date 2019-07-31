# Modality-agnostic files

## Dataset description

Template: `dataset_description.json` `README` `CHANGES`

### `dataset_description.json`

The file dataset_description.json is a JSON file describing the dataset. Every
dataset MUST include this file with the following fields:

| Field name         | Definition                                                                                                                                                                                                                    |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name               | REQUIRED. Name of the dataset.                                                                                                                                                                                                |
| BIDSVersion        | REQUIRED. The version of the BIDS standard that was used.                                                                                                                                                                     |
| License            | RECOMMENDED. What license is this dataset distributed under? The use of license name abbreviations is suggested for specifying a license. A list of common licenses with suggested abbreviations can be found in Appendix II. |
| Authors            | OPTIONAL. List of individuals who contributed to the creation/curation of the dataset.                                                                                                                                        |
| Acknowledgements   | OPTIONAL. Text acknowledging contributions of individuals or institutions beyond those listed in Authors or Funding.                                                                                                          |
| HowToAcknowledge   | OPTIONAL. Instructions how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset.             |
| Funding            | OPTIONAL. List of sources of funding (grant numbers)                                                                                                                                                                          |
| ReferencesAndLinks | OPTIONAL. List of references to publication that contain information on the dataset, or links.                                                                                                                                |
| DatasetDOI         | OPTIONAL. The Document Object Identifier of the dataset (not the corresponding paper).                                                                                                                                        |

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.0.1",
  "License": "CC0",
  "Authors": [
    "Paul Broca",
    "Carl Wernicke"
  ],
  "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
  "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
  "Funding": [
    "National Institute of Neuroscience Grant F378236MFH1",
    "National Institute of Neuroscience Grant 5RMZ0023106"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. http://doi.org/1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "10.0.2.3/dfjj.10"
}
```

### `README`

In addition a free form text file (`README`) describing the dataset in more
details SHOULD be provided. The `README` file MUST be either in ASCII or UTF-8
encoding.

### `CHANGES`

Version history of the dataset (describing changes, updates and corrections) MAY
be provided in the form of a `CHANGES` text file. This file MUST follow the CPAN
Changelog convention:
[http://search.cpan.org/~haarg/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod](https://metacpan.org/pod/release/HAARG/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod).
The `CHANGES` file MUST be either in ASCII or UTF-8 encoding.

Example:

```Text
1.0.1 2015-08-27
 - Fixed slice timing information.

1.0.0 2015-08-17
 - Initial release.
```

## Participants file

Template:

```Text
participants.tsv
participants.json
phenotype/<measurement_tool_name>.tsv
phenotype/<measurement_tool_name>.json
```

Optional: Yes

The purpose of this file is to describe properties of participants such as age,
handedness, sex, etc. In case of single session studies this file has one
compulsory column `participant_id` that consists of `sub-<label>`,
followed by a list of optional columns describing participants. Each participant
needs to be described by one and only one row.

`participants.tsv` example:

```Text
participant_id  age sex group
sub-control01 34  M control
sub-control02 12  F control
sub-patient01 33  F patient
```

If the dataset includes multiple sets of participant level measurements (for
example responses from multiple questionnaires) they can be split into
individual files separate from `participants.tsv`. Those measurements should be
kept in phenotype/ folder and end with the `.tsv` extension. They can include
arbitrary set of columns, but one of them has to be participant_id with matching
`sub-<label>`. As with all other tabular data, those additional
phenotypic information files can be accompanied by a JSON file describing the
columns in detail (see [here](02-common-principles.md#tabular-files)).
In addition to the column description, a
section describing the measurement tool (as a whole) can be added under the name
`MeasurementToolMetadata`. This section consists of two keys: `Description` - a
free text description of the tool, and `TermURL` a link to an entity in an
ontology corresponding to this tool. For example (content of
phenotype/acds_adult.json):

```JSON
{
  "MeasurementToolMetadata": {
    "Description": "Adult ADHD Clinical Diagnostic Scale V1.2",
    "TermURL": "http://www.cognitiveatlas.org/task/id/trm_5586ff878155d"
  },
  "adhd_b": {
    "Description": "B. CHILDHOOD ONSET OF ADHD (PRIOR TO AGE 7)",
    "Levels": {
      "1": "YES",
      "2": "NO"
    }
  },
  "adhd_c_dx": {
    "Description": "As child met A, B, C, D, E and F diagnostic criteria",
    "Levels": {
      "1": "YES",
      "2": "NO"
    }
  }
}
```

Please note that in this example `MeasurementToolMetadata` includes information
about the questionnaire and `adhd_b` and `adhd_c_dx` correspond to individual
columns.

In addition to the keys available to describe columns in all tabular files
(`LongName`, `Description`, `Levels`, `Units`, and `TermURL`) the
`participants.json` file as well as phenotypic files can also include column
descriptions with `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).

## Scans file

Template:

```Text
sub-<label>/[ses-<label>/]
    sub-<label>[_ses-<label>]_scans.tsv
```

Optional: Yes

The purpose of this file is to describe timing and other properties of each
imaging acquisition sequence (each run `.nii[.gz]` file) within one session.
Each `.nii[.gz]` file should be described by at most one row. Relative paths to
files should be used under a compulsory `filename` header. If acquisition time
is included it should be under `acq_time` header. Datetime should be expressed
in the following format `2009-06-15T13:45:30` (year, month, day, hour (24h),
minute, second; this is equivalent to the RFC3339 "date-time" format, time zone
is always assumed as local time). For anonymization purposes all dates within
one subject should be shifted by a randomly chosen (but common across all runs
etc.) number of days. This way relative timing would be preserved, but chances
of identifying a person based on the date and time of their scan would be
decreased. Dates that are shifted for anonymization purposes should be set to a
year 1900 or earlier to clearly distinguish them from unmodified data. Shifting
dates is recommended, but not required.

Additional fields can include external behavioral measures relevant to the
scan. For example vigilance questionnaire score administered after a resting
state scan.

Example:

```Text
filename  acq_time
func/sub-control01_task-nback_bold.nii.gz 1877-06-15T13:45:30
func/sub-control01_task-motor_bold.nii.gz 1877-06-15T13:55:33
```

## Code

Template: `code/*`

Source code of scripts that were used to prepare the dataset (for example if it
was anonymized or defaced) MAY be stored here.<sup>1</sup> Extra care should be
taken to avoid including original IDs or any identifiable information with the
source code. There are no limitations or recommendations on the language and/or
code organization of these scripts at the moment.

<sup>1</sup>Storing actual source files with the data is preferred over links to
external source repositories to maximize long term preservation (which would
suffer if an external repository would not be available anymore).
