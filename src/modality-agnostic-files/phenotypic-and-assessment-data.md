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

Each of the measurement tool files MUST be kept in a `/phenotype` directory placed
at the root of the BIDS dataset and MUST end with the `.tsv` extension.
Filenames SHOULD be chosen to reflect the contents of the file.
For example, the "Adult ADHD Clinical Diagnostic Scale" could be saved in a file
called `/phenotype/acds_adult.tsv`.

The files can include an arbitrary set of columns, but one of them MUST be
`participant_id` and the entries of that column MUST correspond to the subjects
in the BIDS dataset and `participants.tsv` file.

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Phenotypes") }}

As with all other tabular data, the additional tabular phenotypic data
MAY be accompanied by a JSON data dictionary file describing the columns in detail
(see [Tabular files](../common-principles.md#tabular-files)).
When the [`AdditionalValidation` key](dataset-description.md#additional-validation)
contains `"Phenotype"` in the `dataset_description.json`,
then the additional tabular phenotypic data
MUST be accompanied by a JSON data dictionary file.

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

In addition to the keys available to describe columns in all tabular files
(`LongName`, `Description`, `Levels`, `Units`, and `TermURL`) the
`participants.json` file as well as phenotypic files can also include column
descriptions with a `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).

## Additional validation

When the [`AdditionalValidation` key](dataset-description.md#additional-validation)
contains `"Phenotype"` in the `dataset_description.json`,
the following tabular phenotypic data guidelines
apply to phenotypic and assessment data.

-   [1.](../appendices/phenotype.md#1-aggregate-data-across-sessions)
    Aggregate data across sessions

-   [2.](../appendices/phenotype.md#2-always-pair-tabular-data-with-data-dictionaries)
    Always pair tabular data with data dictionaries

-   [3.](../appendices/phenotype.md#3-add-measurementtoolmetadata-to-each-tabular-phenotypic-measurement-tool)
    Add `MeasurementToolMetadata` to each tabular phenotypic measurement tool

-   [4.](../appendices/phenotype.md#4-ensure-minimal-annotation-for-phenotypic-and-assessment-data)
    Ensure minimal annotation for phenotypic and assessment data

-   [5.](../appendices/phenotype.md#5-store-demographic-data-in-the-participants-file-and-instrument-data-in-the-phenotype-directory)
    Store demographic data in the participants file
    and instrument data in the phenotype directory

To read more about the guidelines for tabular phenotypic data and examples,
see the [tabular phenotypic data guidelines appendix](../appendices/phenotype.md).
