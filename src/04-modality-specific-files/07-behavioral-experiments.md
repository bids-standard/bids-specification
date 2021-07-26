# Behavioral experiments (with no neural recordings)

{{ MACROS___make_filename_template(datatypes=["beh"]) }}

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

In addition of the metadata REQUIRED for some data that can be found in the `beh` folder
(for example `SamplingFrequency` and `StartTime` for `*_<physio|stim>.tsv.gz` files),
it is RECOMMENDED to add the following metadata to the JSON files of this folder.

| **Key name**       | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                      |
| ------------------ | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| TaskName           | RECOMMENDED           | [string][]    | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this `TaskName` field by removing all non-alphanumeric (`[a-zA-Z0-9]`) characters. For example `TaskName` `"faces n-back"` will correspond to task label `facesnback`. |
| TaskDescription    | RECOMMENDED           | [string][]    | Description of the task.                                                                                                                                                                                                                                                                                                                                                             |
| Instructions       | RECOMMENDED           | [string][]    | Text of the instructions given to participants before the scan. This is not only important for behavioral or cognitive tasks but also in resting state paradigms (for example, to distinguish between eyes open and eyes closed).                                                                                                                                                    |
| CogAtlasID         | RECOMMENDED           | [string][]    | [URI][uri] of the corresponding [Cognitive Atlas](https://www.cognitiveatlas.org/) term that describes the task (for example, Stroop task "<https://www.cognitiveatlas.org/task/id/tsk_4a57abb949e27>").                                                                                                                                                          |
| CogPOID            | RECOMMENDED           | [string][]    | [URI][uri] of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task (for example, Stroop "<http://wiki.cogpo.org/index.php?title=Stroop_Task_Paradigm>") .                                                                                                                                                                                                                     |
| InstitutionName    | RECOMMENDED           | [string][]    | The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                                                                                                                                        |
| InstitutionAddress | RECOMMENDED           | [string][]    | The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                                                                                                                                     |
