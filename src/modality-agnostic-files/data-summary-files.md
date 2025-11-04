# Data summary files

## Participants file

Template:

```Text
participants.tsv
participants.json
```

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.participants.description") }}

We RECOMMEND to make use of these columns, and
in case that you do use them, we RECOMMEND to use the following values
for them:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Participants") }}

Throughout BIDS you can indicate missing values with `n/a` (for "not
available").

`participants.tsv` example:

```tsv
participant_id	age	sex	handedness	group
sub-01	34	M	right	read
sub-02	12	F	right	write
sub-03	33	F	n/a	read
```

It is RECOMMENDED to accompany each `participants.tsv` file with a sidecar
`participants.json` file to describe the TSV column names and properties of their values (see also
the [section on tabular files](../common-principles.md#tabular-files)).
Such sidecar files are needed to interpret the data, especially so when
optional columns are defined beyond `age`, `sex`, `handedness`, `species`, `strain`,
and `strain_rrid`, such as `group` in this example, or when a different
age unit is needed (for example, gestational weeks).
If no `units` is provided for age, it will be assumed to be in years relative
to date of birth.

`participants.json` example:

```JSON
{
    "participant_id": {
        "Description": "participant identifier"
    },
    "age": {
        "Description": "age of the participant",
        "Units": "year"
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

It is RECOMMENDED to use the `age` column to record participant age
at every session in longitudinal or multi-session data sets.
This reduces data duplication across tabular data files. The `Units` of `age`
do not have to be years so long as the units of the age
are written in `participants.json`.
Consider participant privacy or study objectives when selecting
the `Units` of `age` or the accuracy of `age` data.

## Samples file

Template:

```Text
samples.tsv
samples.json
```

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.samples.description") }}

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Samples") }}

`samples.tsv` example:

```tsv
sample_id	participant_id	sample_type	derived_from
sample-01	sub-01	tissue	n/a
sample-02	sub-01	tissue	sample-01
sample-03	sub-01	tissue	sample-01
sample-04	sub-02	tissue	n/a
sample-05	sub-02	tissue	n/a
```

It is RECOMMENDED to accompany each `samples.tsv` file with a sidecar
`samples.json` file to describe the TSV column names and properties of their values
(see also the [section on tabular files](../common-principles.md#tabular-files)).

`samples.json` example:

```JSON
{
    "sample_type": {
        "Description": "type of sample from ENCODE Biosample Type (https://www.encodeproject.org/profiles/biosample_type)",
    },
    "derived_from": {
        "Description": "sample_id from which the sample is derived"
    }
}
```

## Scans file

Template:

```Text
sub-<label>/
    [ses-<label>/]
        sub-<label>[_ses-<label>]_scans.tsv
        sub-<label>[_ses-<label>]_scans.json
```

Optional: Yes

The purpose of this file is to describe timing and other properties of each recording *file* within one session.
In general, each of these files SHOULD be described by exactly one row.

For *file formats* that are based on several files of different extensions,
or a directory of files with different extensions (multi-file file formats),
only that file SHOULD be listed that would also be passed to analysis software for reading the data.
For example for BrainVision data (`.vhdr`, `.vmrk`, `.eeg`),
only the `.vhdr` SHOULD be listed;
for EEGLAB data (`.set`, `.fdt`),
only the `.set` file SHOULD be listed;
and for CTF data (`.ds`),
the whole `.ds` directory SHOULD be listed,
and not the individual files in that directory.

Some neural recordings consist of multiple parts,
that span several files,
but that share the same extension.
For example in [entity-linked file collections](../common-principles.md#entity-linked-file-collections),
commonly used for qMRI,
where recordings may be linked through entities such as `echo` and `part`
(using `.nii` or `.nii.gz` extensions).
For another example consider the case of large files in `.fif` format that are linked through the `split` entity
(see [Split files](../appendices/meg-file-formats.md#split-files)).
Such recordings MUST be documented with one row per file
(unlike the case of multi-file file formats described above).

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Scans") }}

Additional fields can include external behavioral measures relevant to the
scan.
For example vigilance questionnaire score administered after a resting
state scan.
All such included additional fields SHOULD be documented in an accompanying
`_scans.json` file that describes these fields in detail
(see [Tabular files](../common-principles.md#tabular-files)).

Example `_scans.tsv`:

```tsv
filename	acq_time
func/sub-control01_task-nback_bold.nii.gz	1877-06-15T13:45:30
func/sub-control01_task-motor_bold.nii.gz	1877-06-15T13:55:33
meg/sub-control01_task-rest_split-01_meg.nii.gz	1877-06-15T12:15:27
meg/sub-control01_task-rest_split-02_meg.nii.gz	1877-06-15T12:15:27
```

## Sessions file

In case of multiple sessions there is an option of adding an additional
`sessions.tsv` file describing each session and variables changing between sessions.
It is RECOMMENDED to provide this as a single file at the root-level of the dataset.
It is OPTIONAL to instead provide these as separate files at the subject-level of the dataset.
The intent of the sessions file is to describe the sessions
in a data set and non-demographic variables changing between sessions.
Column names in `sessions.tsv` files MUST be different from participant key column names in
the [participants file](#participants-file).

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Sessions") }}

`sessions.json` example:

```JSON
{
    "participant_id": {
        "Description": "Participant identifier"
    },
    "session_id": {
        "Description": "Session identifier for the session",
        "Levels": {
            "ses-predrug": "session before drug administration",
            "ses-postdrug": "session after drug administration",
            "ses-followup": "follow-up session"
        }
    },
    "acq_time": {
        "Description": "Acquisition time of the session"
    },
    "systolic_blood_pressure": {
        "Description": "Systolic blood pressure measured at the beginning of the session in mmHg"
    }
}
```

### RECOMMENDED: Root-level sessions file

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sessions.tsv": "",
   "[sessions.json]": "",
   }
) }}

Optional: Yes

An aggregated sessions file is RECOMMENDED to be provided at the dataset root.
If a root-level sessions file is provided, then it MUST begin with
a `participant_id` column followed immediately after by a `session_id` column.

`sessions.tsv` example:

```tsv
participant_id	session_id	acq_time	systolic_blood_pressure
sub-01	ses-predrug	2009-06-15T13:45:30	120
sub-01	ses-postdrug	2009-06-16T13:45:30	100
sub-01	ses-followup	2009-06-17T13:45:30	110
sub-02	ses-predrug	2009-06-22T12:22:05	105
sub-02	ses-postdrug	2009-06-23T12:22:05	95
sub-03	ses-postdrug	2009-06-30T14:06:40	115
sub-03	ses-followup	2009-07-01T14:06:40	120
```

### OPTIONAL: Participant-level sessions files

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-<label>": {
      "sub-<label>_sessions.tsv": "",
      "[sub-<label>_sessions.json]": "",
      }
   }
) }}

Optional: Yes

When one sessions file per participant is used,
these files MUST include a `session_id` column and describe each session by one and only one row.
`sub-<label>/sub-<label>_sessions.tsv` example:

```tsv
session_id	acq_time	systolic_blood_pressure
ses-predrug	2009-06-15T13:45:30	120
ses-postdrug	2009-06-16T13:45:30	100
ses-followup	2009-06-17T13:45:30	110
```

### Additional validation

When the [`AdditionalValidation` key](dataset-description.md#additional-validation)
contains `"Phenotype"` in the `dataset_description.json`,
the following tabular phenotypic data guidelines
apply to sessions files:

-   [6.](../appendices/phenotype.md#6-record-participant-properties-in-the-participants-file-and-session-properties-in-the-sessions-file)
    Record participant properties in the participants file
    and session properties in the sessions file

-   [7.](../appendices/phenotype.md#7-use-the-sessions-file-at-the-root-level)
    Use the sessions file at the root-level

-   [8.](../appendices/phenotype.md#8-record-acquisition-time-of-all-sessions-with-acq_time)
    Record acquisition time of all sessions with `acq_time`

To read more about the guidelines for tabular phenotypic data and examples,
see the [tabular phenotypic data guidelines appendix](../appendices/phenotype.md).
