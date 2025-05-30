# Phenotypic and assessment data

Template:

```Text
phenotype/
    <measurement_tool_name>.tsv
    <measurement_tool_name>.json
```

Optional: Yes

If the dataset includes multiple sets of participant level measurements (for
example responses from multiple questionnaires) they can be split into
individual files separate from `participants.tsv`.

Each of the measurement files MUST be kept in a `/phenotype` directory placed
at the root of the BIDS dataset and MUST end with the `.tsv` extension.
Filenames SHOULD be chosen to reflect the contents of the file.
For example, the "Adult ADHD Clinical Diagnostic Scale" could be saved in a file
called `phenotype/acds_adult.tsv`.

The files can include an arbitrary set of columns, but one of them MUST be
`participant_id` and the entries of that column MUST correspond to the subjects
in the BIDS dataset and `participants.tsv` file.

!!! success "Guideline 2"

    For [best tabular phenotypic data](../appendices/phenotype.md):
    It is REQUIRED to aggregate all participant data into
    one TSV per tabular phenotypic file.

In phenotypic and assessment data each measurement tool has
an independent aggregated data TSV file in which the user collects
all subjects, sessions, and/or runs of data as one entry per row
(with a row defined by the smallest unit of acquisition). In other words:

1. Each row MUST start with `participant_id`.
2. Each TSV file SHOULD contain a `session_id` column
when multiple [sessions](../glossary.md#session-entities) are present
in the data set regardless of whether those sessions are in
the `phenotype/` data, `sub-<label>/` data, or a combination of the two.
3. If more than one of the same measurement tool is acquired
within the same `session_id`, a `run` column SHOULD be added.
4. To encode the acquisition time for a measurement tool’s `session_id`,
add the `session_id` to the sessions file
and include the OPTIONAL `acq_time` column.

!!! success "Guideline 3"

    For [best tabular phenotypic data](../appendices/phenotype.md):

    | **Column name**  | **Requirement** | **Description** |
    | :--------------- | :-------------- | :-------------- |
    | `participant_id` | REQUIRED        | MUST be the first column in the file. Note that data for one participant MAY be represented across multiple rows in case of multiple sessions or runs, and therefore the entry in the `participant_id` column will be repeated. |
    | `session _id`    | CONDITIONAL ; If sessions are defined in the dataset | A `session_id` column MUST be added to all tabular files in the phenotype directory as soon as multiple sessions are present in the data set regardless of whether those sessions are in the  `phenotype/` data, `sub-<label>/` data, or a combination of the two. |
    | `run`            | CONDITIONAL ; If there are multiple runs within any session | A chronological `run` number is used when a measurement tool or assessment described by a tabular file was repeated within a session. |
    | `acq_time`       | OPTIONAL        | If acquisition time is available, the `acq_time` column CAN be used to record the time of acquisition of each row in the tabular file. |

    Furthermore, if you have to add a `session_id` column to the tabular phenotypic data, you then MUST also introduce a session directory to the imaging data, even if only one imaging session has been created. This rule can be considered as "**if anyone uses sessions, everyone uses sessions**." And vice versa, if imaging data has session directories, all imaging data and tabular phenotypic data MUST have sessions.

    This produces a file in which same-participant entries can take up as many rows as needed according to the smallest unit of acquisition. The combination of values in the `participant_id`, `session_id`, and `run` (if present) columns MUST be unique for the entire tabular file.

As with all other tabular data, the additional phenotypic information files
MAY be accompanied by a JSON file describing the columns in detail
(see [Tabular files](../common-principles.md#tabular-files)).

!!! success "Guideline 1"

    For [best tabular phenotypic data](../appendices/phenotype.md):
    Each tabular phenotypic data TSV file MUST be accompanied by
    a corresponding data dictionary JSON file.

In addition to the column descriptions, the JSON file MAY contain the following fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "MeasurementToolMetadata": "OPTIONAL",
      "Derivative": "OPTIONAL",
   }
) }}

As an example, consider the contents of a file called
`phenotype/acds_adult.json`:

```JSON
{
  "MeasurementToolMetadata": {
    "Description": "Adult ADHD Clinical Diagnostic Scale V1.2",
    "TermURL": "https://www.cognitiveatlas.org/task/id/trm_5586ff878155d"
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

!!! success "Guideline 4"

    For [best tabular phenotypic data](../appendices/phenotype.md):
    Whenever possible, it is RECOMMENDED to add `MeasurementToolMetadata` to
    each `phenotype/<measurement_tool_name>.json` data dictionary.
    This improves reusability and provides clarity about the measurement tool.


In addition to the keys available to describe columns in all tabular files
(`LongName`, `Description`, `Levels`, `Units`, and `TermURL`) the
`participants.json` file as well as phenotypic files can also include column
descriptions with a `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).
