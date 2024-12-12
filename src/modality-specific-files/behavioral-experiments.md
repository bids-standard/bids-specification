# Behavioral experiments (with no neural recordings)

!!! example "Example datasets"

    Datasets containing behavioral data can be found
    in the [BIDS examples repository](https://bids-standard.github.io/bids-examples/#behavioral)
    and can be used as helpful guidance when curating new datasets.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["beh"]) }}

In addition to logs from behavioral experiments
performed alongside imaging data acquisitions,
one MAY also include data from experiments
performed with no neural recordings.
The results of those experiments MAY be stored in the `beh` directory
using the same formats for event timing (`_events.tsv`),
metadata (`_events.json`),
physiological (`_physio.tsv.gz`, `_physio.json`)
and other continuous recordings (`_stim.tsv.gz`, `_stim.json`)
as for tasks performed during MRI, electrophysiological or other neural recordings.
Additionally, events files
that do not include the mandatory `onset` and `duration` columns
MAY be included,
but MUST be labeled `_beh.tsv` rather than `_events.tsv`.

The following OPTIONAL columns are pre-defined for behavioral data files:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("task.Behavioral") }}

## Sidecar JSON (`*_beh.json`)

In addition to the metadata that is either:

-   RECOMMENDED for sidecar JSON files for [tabular data](../common-principles.md#tabular-files), or

-   REQUIRED for some data that can be found in the `beh` directory
    (for example `SamplingFrequency` and `StartTime` for `*_<physio|stim>.tsv.gz` files),

it is RECOMMENDED to add the following metadata to the JSON files of this directory.

### Task information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_sidecar_table("beh.BEHTaskInformation") }}

### Institution information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("beh.BEHInstitutionInformation") }}

## Example `_beh.tsv`

```Text
trial	response	response_time	stim_file
congruent	red	1.435	images/word-red_color-red.jpg
incongruent	red	1.739	images/word-red_color-blue.jpg
```

In the accompanying JSON sidecar, the `trial` column might be documented as follows:

```JSON
{
   "TaskName": "Stroop",
   "trial": {
      "LongName": "Trial name",
      "Description": "Indicator of the type of trial",
      "Levels": {
         "congruent": "Word and font color match.",
         "incongruent": "Word and font color do not match."
      }
   }
}
```
