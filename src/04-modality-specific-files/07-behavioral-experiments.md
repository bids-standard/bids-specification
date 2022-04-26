# Behavioral experiments (with no neural recordings)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(datatypes=["beh"]) }}

In addition to logs from behavioral experiments performed alongside imaging data
acquisitions, one can also include data from experiments performed with no neural
recordings.
The results of those experiments can be stored in the `beh` directory using the same
formats for event timing (`_events.tsv`), metadata (`_events.json`),
physiological (`_physio.tsv.gz`, `_physio.json`)
and other continuous recordings (`_stim.tsv.gz`, `_stim.json`)
as for tasks performed during MRI, electrophysiological or other neural recordings.
Additionally, events files that do not include the mandatory `onset` and
`duration` columns can still be included, but should be labeled `_beh.tsv`
rather than `_events.tsv`.

Each task has a unique label that MUST only consist of letters and/or numbers
(other characters, including spaces and underscores, are not allowed) with the
[`task-<label>`](../99-appendices/09-entities.md#task) key/value pair.
Those labels MUST be consistent across subjects and sessions.

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair corresponds to a custom label to
distinguish different conditions present during multiple runs of the same task.
For example, if a study includes runs of an n-back task, with deep brain
stimulation turned on or off, the data files may be labelled
`sub-01_task-nback_acq-dbson_beh.tsv` and `sub-01_task-nback_acq-dbsoff_beh.tsv`.

## RECOMMENDED metadata

In addition to the metadata that is either:

-   RECOMMENDED for sidecar JSON files for [tabular data](../02-common-principles.md#tabular-data), or

-   REQUIRED for some data that can be found in the `beh` directory
    (for example `SamplingFrequency` and `StartTime` for `*_<physio|stim>.tsv.gz` files),

it is RECOMMENDED to add the following metadata to the JSON files of this directory:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "TaskName": "RECOMMENDED",
      "Instructions": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
      "InstitutionName": "RECOMMENDED",
      "InstitutionAddress": "RECOMMENDED",
      "InstitutionalDepartmentName": "RECOMMENDED",
   }
) }}

Example of the content of a `_beh.tsv` and its accompanying `_beh.json` sidecar file:

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
