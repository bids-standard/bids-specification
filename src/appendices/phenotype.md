# Tabular phenotypic data guidelines

This appendix is a collection of guidelines and examples for creating well-organized aggregated tabular phenotypic data.

## Guidelines

These guidelines are all **RECOMMENDED** when preparing
tabular phenotypic data like the
participants file, sessions file, demographics file,
or phenotypic and assessment data.
The language below uses REQUIRED, MUST, and others to imply
these are the requirements for these **RECOMMENDED** guidelines.

### 1. Always pair tabular data with data dictionaries

Tabular phenotypic data MUST be prepared as one pair of a tabular file
in tab-separated value (TSV) format and a corresponding data dictionary
in JavaScript Object Notation (JSON) format.

### 2. Aggregate data across sessions

Aggregation refers to the contents of the TSV file. It is REQUIRED
to collect all participant data into one TSV per tabular phenotypic file.

### 3. Ensure minimal annotation for phenotypic and assessment data

In phenotypic and assessment data each measurement tool has an independent
aggregated data TSV file in which the user collects all subjects, sessions,
and/or runs of data as one entry per row (with a row defined by
the smallest unit of acquisition). In other words:

1. Each row MUST start with `participant_id`.
2. Each TSV file MUST contain a `session_id` column when
multiple [sessions](../glossary.md#session-entities)[^1] are present
in the data set regardless of whether those sessions are in
the `phenotype/` data, `sub-<label>/` data, or a combination of the two.
3. If more than one of the same measurement tool is acquired within
the same `session_id`, a `run` column MUST be added.
4. To encode the acquisition time for a measurement tool’s `session_id`,
add the `session_id` to the sessions file and
include the OPTIONAL `acq_time` column.

To summarize this guideline as a table:

| **Column name**  | **Requirement** | **Description** |
| :--------------- | :-------------- | :-------------- |
| `participant_id` | REQUIRED        | MUST be the first column in the file.   Note that data for one participant MAY be represented across multiple rows in case of multiple sessions or runs, and therefore the entry in the `participant_id` column will be repeated. |
| `session _id`    | CONDITIONAL ; If sessions are defined in the dataset | A `session_id` column MUST be added to all tabular files in the phenotype directory as soon as multiple sessions are present in the data set regardless of whether those sessions are in the  `phenotype/` data, `sub-<label>/` data, or a combination of the two. |
| `run`            | CONDITIONAL ; If there are multiple runs within any session | A chronological `run` number is used when a measurement tool or assessment described by a tabular file was repeated within a session. |
| `acq_time`       | OPTIONAL        | If acquisition time is available, the `acq_time` column CAN be used to record the time of acquisition of each row in the tabular file. |

Furthermore, if you have to add a `session_id` column to the
tabular phenotypic data, you then MUST also introduce a session directory to the
imaging data, even if only one imaging session has been created.
This rule can be considered as "**if anyone uses sessions, everyone uses sessions**."
And vice versa, if imaging data has session directories,
all imaging data and tabular phenotypic data MUST have sessions.

This produces a file in which same-participant entries can take up as many rows
as needed according to the smallest unit of acquisition.
The combination of values in the `participant_id`, `session_id`, and `run` (if present)
columns MUST be unique for the entire tabular file.

### 4. Add `MeasurementToolMetadata` to each tabular phenotypic measurment tool

Whenever possible, it is RECOMMENDED to add `MeasurementToolMetadata` to
each `phenotype/<measurement_tool_name>.json` data dictionary.
This improves reusability and provides clarity about the measurement tool.

### 5. Use the demographics file for common variables about participants

Some studies collect demographics into their own tabular phenotypic data file already.
In these cases, it is RECOMMENDED to house this data in the `phenotype/` directory
as a TSV called `demographics.tsv` and its corresponding data dictionary JSON
called `demographics.json`.

### 6. Store longitudinal age in the demographics file

It is RECOMMENDED to use the `age` column to record participant age
at every session in longitudinal or multi-session data sets.
This reduces data duplication across tabular data files. The `Units` of `age`
do not have to be years so long as the units of the age
are written in `phenotype/demographics.json`.
Consider participant privacy or study objectives when selecting
the `Units` of `age` or the accuracy of `age` data.

### 7. Use the sessions file at the root level

If there is more than one session for any one participant, then
it is REQUIRED to provide a sessions file at the dataset root.
The sessions file MUST list all sessions for all subjects across
imaging and tabular phenotypic data.

When a sessions file is in use, you MUST NOT provide additional sessions files
at the participant-level which would otherwise use the inheritance principle.
If a sessions file is provided, then it MUST begin with a `participant_id` column
followed immediately by a `session_id` column. The data dictionary JSON file’s
`session_id` field MUST include `Levels` with the description of each `session_id`.

### 8. Record acquisition time of sessions with `acq_time`

Whenever possible, it is RECOMMENDED to also collect acquisition time for
tabular phenotypic data and store the time of acquisition[^2] of each row
inside a column named `acq_time` in the sessions file.
This is consistent with how acquisition time is recorded for MRI data
and other time-sensitive measurements (e.g. systolic blood pressure).

When needed to preserve participant privacy, you SHOULD record
relative acquisition times with respect to the earliest session.
Relative session acquisition times MAY be listed as durations from
the earliest session (baseline) in days, months, or years
using the `acq_time` column.

## Summary

This appendix described seven guidelines for best tabular phenotypic data.
A short summary table here describes when to use which files.

| File                           | Single session data | Multiple session data |
| :----------------------------- | :------------------ | :-------------------- |
| Participants                   | RECOMMENDED         | RECOMMENDED           |
| Phenotypic and assessment data | RECOMMENDED         | RECOMMENDED           |
| Sessions                       | OPTIONAL            | REQUIRED              |
| Demographics                   | OPTIONAL            | RECOMMENDED           |

## Examples

What follows are a few common use case examples for tabular phenotypic files.

### 1 participant session with both non-tabular and tabular phenotypic data

File tree

```Text
phenotype/
    <measurement_tool_name>.json
    <measurement_tool_name>.tsv
sub-01/anat/
    sub-01_T1w.json
    sub-01_T1w.nii.gz
```

Contents of `phenotype/<measurement_tool_name>.tsv`

```Text
participant_id measurement_1 measurement_2
sub-01 value1 value2
```

### 1 participant with 2 sessions, where 1 session is only tabular phenotype and the other is only imaging

With only one imaging and one phenotypic session each in this example you might want
to merge both imaging and phenotypic data under one session. But it is more correct to
have separate sessions for the imaging and phenotypic data, especially if
the sessions were collected days, weeks, or months apart. You can denote both sessions
and their acquisition time in the `sessions.tsv` file and have `session_id` `Levels` noted
in the `sessions.json` sidecar. Below are a CORRECT and an INCORRECT example
of prepared data following these guidelines.

#### CORRECT

File tree

```Text
phenotype/
    <measurement_tool_name>.json
    <measurement_tool_name>.tsv
sub-01/ses-MRI/anat/
    sub-01_ses-MRI_T1w.json
    sub-01_ses-MRI_T1w.nii.gz
```

Contents of `phenotype/<measurement_tool_name>.tsv`

```Text
participant_id session_id measurement_1 measurement_2
sub-01         ses-pheno  value1        value2
```

#### INCORRECT

File tree

```Text
phenotype/
    <measurement_tool_name>.json
    <measurement_tool_name>.tsv
sub-01/anat/
    sub-01_T1w.json
    sub-01_T1w.nii.gz
```

Contents of `phenotype/<measurement_tool_name>.tsv`

```Text
participant_id measurement_1 measurement_2
sub-01         value1        value2
```

A session directory **MUST** be present in the participant directory and
the `session_id` column **MUST** be present in `<measurement_tool_name>.tsv` as well.
Sessions must be used consistently for the combination of tabular and
non-tabular phenotypic data.

### 2 participants with a mix of tabular phenotypic data and imaging sessions

File tree

```Text
phenotype/
    <measurement_tool_name>.json
    <measurement_tool_name>.tsv
sub-01/
    ses-MRI1/
        anat/
            sub-01_ses-MRI1_T1w.json
            sub-01_ses-MRI1_T1w.nii.gz
    ses-MRI2/
        anat/
            sub-01_ses-MRI2_T1w.json
            sub-01_ses-MRI2_T1w.nii.gz
sub-02/
    ses-MRI1/
        anat/
            sub-02_ses-MRI1_T1w.json
            sub-02_ses-MRI1_T1w.nii.gz
```

Contents of `phenotype/<measurement_tool_name>.tsv`

```Text
participant_id session_id measurement_1 measurement_2
sub-01         ses-pheno1 value1        value2
sub-02         ses-pheno1 value3        value4
sub-02         ses-pheno2 value5        value6
```

### 3 participants with 3 different kinds of sessions among them

The `ses-baseline` session collects an MRI and tabular phenotypic data.

File tree

```Text
participants.json
participants.tsv
sessions.json
sessions.tsv
phenotype/
    demographics.json
    demographics.tsv
    ...
sub-01/
    ses-baseline/
    ses-followupMRI/
sub-02/
    ses-baseline/
sub-03/
    ses-baseline/
    ses-followupMRI/
```

Contents of `sessions.tsv`.

```Text
participant_id session_id      acq_time
sub-01         ses-baseline    2001-01-01T12:05:00
sub-01         ses-followupMRI 2001-07-01T13:33:00
sub-01         ses-interview   2002-01-01T11:21:00
sub-02         ses-baseline    2001-04-01T11:01:00
sub-02         ses-interview   2002-04-01T14:08:00
sub-03         ses-baseline    2001-09-01T11:45:00
sub-03         ses-followupMRI 2002-03-01T12:17:00
```

Contents of `sessions.json`. Note how the `session_id` `Levels` are clearly described.

```json
{
    "participant_id": {
        "Description": "BIDS participant identifier"
    },
    "session_id": {
        "Description": "BIDS session identifier",
        "Levels": {
            "ses-baseline": "Baseline visit for MRI and assessments",
            "ses-followupMRI": "6-months after baseline MRI follow-up",
            "ses-interview": "1-year after baseline in-person follow-up"
        }
    },
    "acq_time": {
        "Description": "When the data acquisition started"
    }
}
```

Contents of `participants.tsv`.

```Text
participant_id sex
sub-01         M
sub-02         F
sub-03         F
```

Contents of `phenotype/demographics.tsv`. Measures or features that can change
from session to session belong here especially.

```Text
participant_id session_id      age gender race household_income
sub-01         ses-baseline    10  3      4    5
sub-01         ses-followupMRI 10  3      4    5
sub-01         ses-interview   11  4      4    6
sub-02         ses-baseline    9   1      3    3
sub-02         ses-interview   10  1      7    3
sub-03         ses-baseline    11  2      10   4
sub-03         ses-followupMRI 12  5      10   4
```

For more complete examples, see the `pheno00*`
[bids-examples on GitHub](https://github.com/bids-standard/bids-examples/).

[^1]: A session is any logical grouping of imaging and behavioral data consistent
across participants. Session can (but doesn't have to) be synonymous to a visit
in a longitudinal study. In situations where different data types are obtained over
several visits (for example fMRI on one day followed by DWI the day after)
those can still be grouped in one session. Refer to the
[definition of session](../glossary.md#session-entities) for more details.

[^2]: Datetime format and the anonymization procedure are
described in [Units](../common-principles.md#units).
