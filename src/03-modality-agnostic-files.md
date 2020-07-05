# Modality agnostic files

## Dataset description

Templates:

-   `dataset_description.json`
-   `README`
-   `CHANGES`
-   `LICENSE`

### `dataset_description.json`

The file `dataset_description.json` is a JSON file describing the dataset.
Every dataset MUST include this file with the following fields:

| Field name         | Definition                                                                                                                                                                                                                                                         |
| ------------------------------------------------------------------------------| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name               | REQUIRED. Name of the dataset.                                                                                                                                                                                                                                     |
| BIDSVersion        | REQUIRED. The version of the BIDS standard that was used.                                                                                                                                                                                                          |
| DatasetType        | RECOMMENDED. The interpretaton of the dataset. MUST be one of `"raw"` or `"derivative"`. For backwards compatibility, the default value is `"raw"`.                                                                                                                |
| License            | RECOMMENDED. The license for the dataset. The use of license name abbreviations is RECOMMENDED for specifying a license (see [Appendix II](./99-appendices/02-licenses.md)). The corresponding full license text MAY be specified in an additional `LICENSE` file. |
| Authors            | OPTIONAL. List of individuals who contributed to the creation/curation of the dataset.                                                                                                                                                                             |
| Acknowledgements   | OPTIONAL. Text acknowledging contributions of individuals or institutions beyond those listed in Authors or Funding.                                                                                                                                               |
| HowToAcknowledge   | OPTIONAL. Text containing instructions on how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset.                               |
| Funding            | OPTIONAL. List of sources of funding (grant numbers).                                                                                                                                                                                                              |
| EthicsApprovals    | OPTIONAL. List of ethics committee approvals of the research protocols and/or protocol identifiers.                                                                                                                                                                |
| ReferencesAndLinks | OPTIONAL. List of references to publication that contain information on the dataset, or links.                                                                                                                                                                     |
| DatasetDOI         | OPTIONAL. The Document Object Identifier of the dataset (not the corresponding paper).                                                                                                                                                                             |

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.4.0",
  "DatasetType": "raw",
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
  "EthicsApprovals": [
    "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. http://doi.org/1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "10.0.2.3/dfjj.10"
}
```

#### Derived dataset and pipeline description

As for any BIDS dataset, a `dataset_description.json` file MUST be found at the
top level of the a derived dataset:
`<dataset>/derivatives/<pipeline_name>/dataset_description.json`

In addition to the keys for raw BIDS datasets,
derived BIDS datasets include the following REQUIRED and RECOMMENDED
`dataset_description.json` keys:

| **Key name**   | **Description**                                                                                                                                                                    |
| -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| GeneratedBy    | REQUIRED. List of [objects][object] with at least one element.                                                                                                                     |
| SourceDatasets | RECOMMENDED. A list of [objects][object] specifying the locations and relevant attributes of all source datasets. Valid fields in each object include `URL`, `DOI`, and `Version`. |

Each object in the `GeneratedBy` list includes the following REQUIRED, RECOMMENDED
and OPTIONAL keys:

| **Key name** | **Description**                                                                                                                                                                                              |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Name         | REQUIRED. Name of the pipeline or process that generated the outputs. Use `"Manual"` to indicate the derivatives were generated by hand, or adjusted manually after an initial run of an automated pipeline. |
| Version      | RECOMMENDED. Version of the pipeline.                                                                                                                                                                        |
| Description  | OPTIONAL. Plain-text description of the pipeline or process that generated the outputs. RECOMMENDED if `Name` is `"Manual"`.                                                                                 |
| CodeURL      | OPTIONAL. URL where the code used to generate the derivatives may be found.                                                                                                                                  |
| Container    | OPTIONAL. [Object][object] specifying the location and relevant attributes of software container image used to produce the derivative. Valid fields in this object include `Type`, `Tag` and `URI`.          |

Example:

```JSON
{
  "Name": "FMRIPREP Outputs",
  "BIDSVersion": "1.4.0",
  "DatasetType": "derivative",
  "GeneratedBy": [
    {
      "Name": "fmriprep",
      "Version": "1.4.1",
      "Container": {
        "Type": "docker",
        "Tag": "poldracklab/fmriprep:1.4.1"
        }
    },
    {
      "Name": "Manual",
      "Description": "Re-added RepetitionTime metadata to bold.json files"
    }
  ],
  "SourceDatasets": [
    {
      "DOI": "10.18112/openneuro.ds000114.v1.0.1",
      "URL": "https://openneuro.org/datasets/ds000114/versions/1.0.1",
      "Version": "1.0.1"
    }
  ]
}
```

If a derived dataset is stored as a subfolder of the raw dataset, then the `Name` field
of the first `GeneratedBy` object MUST be a substring of the derived dataset folder name.
That is, in a directory `<dataset>/derivatives/<pipeline>[-<variant>]/`, the first
`GeneratedBy` object should have a `Name` of `<pipeline>`.

### `README`

In addition a free form text file (`README`) describing the dataset in more
details SHOULD be provided.
The `README` file MUST be either in ASCII or UTF-8 encoding.

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

### `LICENSE`

A `LICENSE` file MAY be provided in addition to the short specification of the
used license in the `dataset_description.json` `"License"` field.
The `"License"` field and `LICENSE` file MUST correspond.
The `LICENSE` file MUST be either in ASCII or UTF-8 encoding.

## Participants file

Template:

```Text
participants.tsv
participants.json
```

The purpose of this RECOMMENDED file is to describe properties of participants
such as age, sex, handedness etc.
In case of single-session studies, this file has one compulsory column
`participant_id` that consists of `sub-<label>`, followed by a list of optional
columns describing participants.
Each participant MUST be described by one and only one row.

Commonly used *optional* columns in `participant.tsv` files are `age`, `sex`,
and `handedness`. We RECOMMEND to make use of these columns, and
in case that you do use them, we RECOMMEND to use the following values
for them:

-   `age`: numeric value in years (float or integer value)

-   `sex`: string value indicating phenotypical sex, one of "male", "female",
    "other"

    -   for "male", use one of these values: `male`, `m`, `M`, `MALE`, `Male`

    -   for "female", use one of these values: `female`, `f`, `F`, `FEMALE`,
      ` Female`

    -   for "other", use one of these values: `other`, `o`, `O`, `OTHER`,
        `Other`

-   `handedness`: string value indicating one of "left", "right",
    "ambidextrous"

    -   for "left", use one of these values: `left`, `l`, `L`, `LEFT`, `Left`

    -   for "right", use one of these values: `right`, `r`, `R`, `RIGHT`,
        `Right`

    -   for "ambidextrous", use one of these values: `ambidextrous`, `a`, `A`,
        `AMBIDEXTROUS`, `Ambidextrous`

Throughout BIDS you can indicate missing values with `n/a` (i.e., "not
available").

`participants.tsv` example:

```Text
participant_id age sex handedness group
sub-01 34 M right read
sub-02 12 F right write
sub-03 33 F n/a read
```

It is RECOMMENDED to accompany each `participants.tsv` file with a sidecar
`participants.json` file to describe the TSV column names and properties of their values (see also
the [section on tabular files](02-common-principles.md#tabular-files)).
Such sidecar files are needed to interpret the data, especially so when
optional columns are defined beyond `age`, `sex`, and `handedness`, such as
`group` in this example, or when a different age unit is needed (e.g., gestational weeks).
If no `units` is provided for age, it will be assumed to be in years relative to date of birth.

`participants.json` example:

```JSON
{
    "age": {
        "Description": "age of the participant",
        "Units": "years"
    },
    "sex": {
        "Description": "sex of the participant as reported by the participant",
        "Levels": {
            "M": "male",
            "F": "female"
        }
    },
    "handedness": {
        "Description": "handedness of the participant as reported by the participant",
        "Levels": {
            "left": "left",
            "right": "right"
        }
    },
    "group": {
        "Description": "experimental group the participant belonged to",
        "Levels": {
            "read": "participants who read an inspirational text before the experiment",
            "write": "participants who wrote an inspirational text before the experiment"
        }
    }
}
```

## Phenotypic and assessment data

Template:

```Text
phenotype/<measurement_tool_name>.tsv
phenotype/<measurement_tool_name>.json
```

Optional: Yes

If the dataset includes multiple sets of participant level measurements (for
example responses from multiple questionnaires) they can be split into
individual files separate from `participants.tsv`.

Each of the measurement files MUST be kept in a `/phenotype` directory placed
at the root of the BIDS dataset and MUST end with the `.tsv` extension.
File names SHOULD be chosen to reflect the contents of the file.
For example, the "Adult ADHD Clinical Diagnostic Scale" could be saved in a file
called `/phenotype/acds_adult.tsv`.

The files can include an arbitrary set of columns, but one of them MUST be
`participant_id` and the entries of that column MUST correspond to the subjects
in the BIDS dataset and `participants.tsv` file.

As with all other tabular data, the additional phenotypic information files
MAY be accompanied by a JSON file describing the columns in detail
(see [Tabular files](02-common-principles.md#tabular-files)).
In addition to the column description, a section describing the measurement tool
(as a whole) MAY be added under the name `MeasurementToolMetadata`.
This section consists of two keys:

  - `Description`: A free text description of the measurement tool
  - `TermURL`: A link to an entity in an ontology corresponding to this tool.

As an example, consider the contents of a file called
`phenotype/acds_adult.json`:

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
descriptions with a `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).

## Scans file

Template:

```Text
sub-<label>/[ses-<label>/]
    sub-<label>[_ses-<label>]_scans.tsv
    sub-<label>[_ses-<label>]_scans.json    
```

Optional: Yes

The purpose of this file is to describe timing and other properties of each
imaging acquisition sequence (each *run* file) within one session.
Each neural recording file should be described by at most one row.
Relative paths to files should be used under a compulsory `filename` header.
If acquisition time is included it should be under `acq_time` header.
Datetime should be expressed as described in [Units](./02-common-principles.md#units).
For anonymization purposes all dates within one subject should be shifted by a
randomly chosen (but consistent across all runs etc.) number of days.
This way relative timing would be preserved, but chances of identifying a
person based on the date and time of their scan would be decreased.
Dates that are shifted for anonymization purposes should be set to a year 1925
or earlier to clearly distinguish them from unmodified data.
Shifting dates is RECOMMENDED, but not required.

Additional fields can include external behavioral measures relevant to the
scan.
For example vigilance questionnaire score administered after a resting
state scan.
All such included additional fields SHOULD be documented in an accompanying
`_scans.json` file that describes these fields in detail
(see [Tabular files](02-common-principles.md#tabular-files)).

Example `_scans.tsv`:

```Text
filename	acq_time
func/sub-control01_task-nback_bold.nii.gz	1877-06-15T13:45:30
func/sub-control01_task-motor_bold.nii.gz	1877-06-15T13:55:33
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
