# Survey data (instrument-based phenotypic)

Survey data files contain responses collected from standardized questionnaires or
assessment instruments.
They are organized in the same subject- and session-resolved directory hierarchy
as other BIDS modalities, with one `.tsv` data file per instrument administration
and a corresponding `.json` sidecar that documents the instrument and its items.

This representation complements the aggregated `phenotype/` tables described in
[Phenotypic and assessment data](../modality-agnostic-files/phenotypic-and-assessment-data.md).
Aggregated phenotype tables MAY be generated from subject-resolved survey data
and stored under `phenotype/`,
but the subject-resolved structure is the primary canonical form.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["survey"]) }}

Survey files MUST be stored in a `survey` subdirectory of the subject (and
optionally session) directory.
The `task` entity identifies the instrument (for example, `task-pss` for the
Perceived Stress Scale).
The `run` entity MAY be used when the same instrument is administered more than
once within a session.

## Sidecar JSON (`*_survey.json`)

Each survey `.tsv` file MUST be accompanied by a JSON sidecar.
Following the [Inheritance Principle](../common-principles.md#the-inheritance-principle),
the sidecar MAY be placed at any level of the hierarchy
(for example, at the dataset root as `task-<label>_survey.json`)
to apply to all survey files with matching entities,
or alongside individual `.tsv` files with the same filename stem.
The sidecar documents the instrument-level metadata and the individual items.

### Instrument metadata

The following top-level fields describe the survey instrument and its
administration context.

| Field                  | Requirement | Description                                                                                          |
| ---------------------- | ----------- | ---------------------------------------------------------------------------------------------------- |
| `TaskName`             | REQUIRED    | Short label identifying the instrument as used in this dataset (MUST match the `task` entity value). |
| `OriginalName`         | REQUIRED    | Full canonical name of the instrument.                                                               |
| `StimulusType`         | REQUIRED    | MUST be `"Questionnaire"`.                                                                           |
| `FileFormat`           | REQUIRED    | MUST be `"tsv"`.                                                                                     |
| `Language`             | REQUIRED    | Language code for the administered version (for example, `"en"`, `"de-AT"`).                         |
| `Respondent`           | REQUIRED    | Who provided the responses (`"self"`, `"clinician"`, `"parent"`, or similar).                        |
| `ShortName`            | OPTIONAL    | Common abbreviation of the instrument (for example, `"ESQ-3"`).                                      |
| `Version`              | OPTIONAL    | Version or edition of the instrument.                                                                |
| `Authors`              | OPTIONAL    | Array of instrument authors.                                                                         |
| `DOI`                  | OPTIONAL    | DOI for the instrument or its primary validation paper.                                              |
| `License`              | OPTIONAL    | License under which the instrument may be used.                                                      |
| `Construct`            | OPTIONAL    | Psychological or clinical construct measured (for example, `"sleep quality"`).                       |
| `Instructions`         | OPTIONAL    | Instructions given to the participant.                                                               |
| `AdministrationMethod` | OPTIONAL    | How the instrument was administered (`"online"`, `"paper"`, `"interview"`, `"phone"`, or `"mixed"`). |
| `SoftwarePlatform`     | OPTIONAL    | Software used to administer the instrument (for example, `"LimeSurvey"`, `"REDCap"`).                |

### Item-level metadata

Any top-level key in the sidecar that is not one of the instrument-level fields
listed above is treated as a column-level variable definition (for example, `"Q01"`,
`"item_1"`).

| Field         | Requirement | Description                                                                                         |
| ------------- | ----------- | --------------------------------------------------------------------------------------------------- |
| `Description` | REQUIRED    | The exact text of the question or item.                                                             |
| `Levels`      | OPTIONAL    | Mapping of response values to their labels (for example, `{"0": "Not at all", "4": "Very often"}`). |
| `MinValue`    | OPTIONAL    | Minimum expected value.                                                                             |
| `MaxValue`    | OPTIONAL    | Maximum expected value.                                                                             |
| `DataType`    | OPTIONAL    | Expected data type of the column (`"string"`, `"integer"`, or `"float"`).                           |
| `Units`       | OPTIONAL    | Units, if applicable.                                                                               |

## Example dataset structure

```text
study/
├── dataset_description.json
├── participants.tsv
├── task-sleep_survey.json
├── sub-01/
│   ├── ses-baseline/
│   │   └── survey/
│   │       └── sub-01_ses-baseline_task-sleep_run-01_survey.tsv
│   └── ses-week04/
│       └── survey/
│           ├── sub-01_ses-week04_task-sleep_run-01_survey.tsv
│           └── sub-01_ses-week04_task-sleep_run-02_survey.tsv
└── phenotype/
    └── sleep_summary.tsv
```

The root-level `task-sleep_survey.json` applies to all `task-sleep` survey files
through the inheritance principle, avoiding duplication across sessions and runs.
The `phenotype/` entry is an optional aggregated downstream view of the subject-resolved survey data.

## Example `*_survey.tsv`

```tsv
participant_id	Q01	Q02	Q03
sub-01	7	4	0
```

## Example `task-sleep_survey.json`

```json
{
  "TaskName": "sleep",
  "OriginalName": "Example Sleep Questionnaire",
  "ShortName": "ESQ-3",
  "StimulusType": "Questionnaire",
  "FileFormat": "tsv",
  "Language": "en",
  "Respondent": "self",
  "AdministrationMethod": "online",
  "Q01": {
    "Description": "How many hours did you sleep last night?",
    "MinValue": 0,
    "MaxValue": 24,
    "DataType": "float",
    "Units": "h"
  },
  "Q02": {
    "Description": "How would you rate your overall sleep quality?",
    "Levels": {
      "1": "Very poor",
      "2": "Poor",
      "3": "Fair",
      "4": "Good",
      "5": "Very good"
    },
    "MinValue": 1,
    "MaxValue": 5,
    "DataType": "integer"
  },
  "Q03": {
    "Description": "Did you wake up during the night?",
    "Levels": {
      "0": "No",
      "1": "Yes"
    },
    "DataType": "integer"
  }
}
```
