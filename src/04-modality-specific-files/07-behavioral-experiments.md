# Behavioral experiments (with no MRI)

Template:

```Text
sub-<label>/[ses-<label>/]
    beh/
        sub-<label>[_ses-<label>]_task-<label>_events.tsv
        sub-<label>[_ses-<label>]_task-<label>_events.json
        sub-<label>[_ses-<label>]_task-<label>_beh.tsv
        sub-<label>[_ses-<label>]_task-<label>_beh.json
        sub-<label>[_ses-<label>]_task-<label>_physio.tsv.gz
        sub-<label>[_ses-<label>]_task-<label>_physio.json
        sub-<label>[_ses-<label>]_task-<label>_stim.tsv.gz
        sub-<label>[_ses-<label>]_task-<label>_stim.json
```

In addition to logs from behavioral experiments performed along imaging data
acquisitions one can also include data from experiments performed outside of the
scanner. The results of those experiments can be stored in the `beh` folder using
the same formats for event timing (`_events.tsv`), metadata (`_events.json`),
physiological (`_physio.tsv.gz`, `_physio.json`) and other continuous recordings
(`_stim.tsv.gz`, `_stim.json`) as for tasks performed during MRI acquisitions.
Additionally, events files that do not include the mandatory `onset` and
`duration` columns can still be included, but should be labeled `_beh.tsv`
rather than `_events.tsv`.
