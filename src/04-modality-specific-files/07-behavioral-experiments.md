# Behavioral experiments (with no neural recordings)

{{ MACROS___make_filename_template(datatypes=["beh"]) }}

{{ MACROS___make_entity_table(datatypes=["beh"]) }}

In addition to logs from behavioral experiments performed alongside imaging data
acquisitions, one can also include data from experiments performed with no neural
recordings.
The results of those experiments can be stored in the `beh` folder using the same
formats for event timing (`_events.tsv`), metadata (`_events.json`),
physiological (`_physio.tsv.gz`, `_physio.json`)
and other continuous recordings (`_stim.tsv.gz`, `_stim.json`)
as for tasks performed during MRI, electrophysiological or other neural recordings.
Additionally, events files that do not include the mandatory `onset` and
`duration` columns can still be included, but should be labeled `_beh.tsv`
rather than `_events.tsv`.

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) key/value pair corresponds to a custom label to
distinguish different conditions present during multiple runs of the same task.
For example, if a study includes runs of an n-back task, with deep brain
stimulation turned on or off, the data files may be labelled
`sub-01_task-nback_acq-dbson_beh.tsv` and `sub-01_task-nback_acq-dbsoff_beh.tsv`.
