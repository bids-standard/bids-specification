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

Each survey `.tsv` file MUST be accompanied by a JSON sidecar with the same
filename stem.
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
| `ShortName`            | OPTIONAL    | Common abbreviation of the instrument (for example, `"PSS-10"`).                                     |
| `Version`              | OPTIONAL    | Version or edition of the instrument.                                                                |
| `Authors`              | OPTIONAL    | Array of instrument authors.                                                                         |
| `DOI`                  | OPTIONAL    | DOI for the instrument or its primary validation paper.                                              |
| `License`              | OPTIONAL    | License under which the instrument may be used.                                                      |
| `Construct`            | OPTIONAL    | Psychological or clinical construct measured (for example, `"perceived stress"`).                    |
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
├── sub-01/
│   ├── ses-baseline/
│   │   └── survey/
│   │       ├── sub-01_ses-baseline_task-pss_run-01_survey.tsv
│   │       └── sub-01_ses-baseline_task-pss_run-01_survey.json
│   └── ses-week04/
│       └── survey/
│           ├── sub-01_ses-week04_task-pss_run-01_survey.tsv
│           ├── sub-01_ses-week04_task-pss_run-01_survey.json
│           ├── sub-01_ses-week04_task-pss_run-02_survey.tsv
│           └── sub-01_ses-week04_task-pss_run-02_survey.json
└── phenotype/
    └── pss_summary.tsv
```

The `phenotype/` entry in this example is an optional aggregated downstream
view of the subject-resolved survey data.

## Example `*_survey.tsv`

```tsv
participant_id	Q01	Q02	Q03
sub-01	2	1	3
```

## Example `*_survey.json`

```json
{
  "TaskName": "pss",
  "OriginalName": "Perceived Stress Scale",
  "ShortName": "PSS-10",
  "StimulusType": "Questionnaire",
  "FileFormat": "tsv",
  "Language": "en",
  "Respondent": "self",
  "AdministrationMethod": "online",
  "Q01": {
    "Description": "In the last month, how often have you been upset because of something that happened unexpectedly?",
    "Levels": {
      "0": "Never",
      "1": "Almost never",
      "2": "Sometimes",
      "3": "Fairly often",
      "4": "Very often"
    },
    "MinValue": 0,
    "MaxValue": 4,
    "DataType": "integer"
  },
  "Q02": {
    "Description": "In the last month, how often have you felt that you were unable to control the important things in your life?",
    "Levels": {
      "0": "Never",
      "1": "Almost never",
      "2": "Sometimes",
      "3": "Fairly often",
      "4": "Very often"
    },
    "MinValue": 0,
    "MaxValue": 4,
    "DataType": "integer"
  }
}
```
