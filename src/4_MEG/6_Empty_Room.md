### 6 Empty-room files (`sub-emptyroom`)
Empty-room MEG files capture the environment and system noise. Their collection is RECOMMENDED, before/during/after each session. This data is stored inside a subject folder named `sub-emptyroom`. The `session label` SHOULD be that of the date of the empty-room recording (e.g. `ses-YYYYMMDD`). The `scans.tsv` file containing the date/time of the acquisition SHOULD also be included. Hence, users will be able to retrieve the empty-room recording that best matches a particular session with a participant, based on date/time of recording.

Example:

```
sub-control01/
sub-control02/
sub-emptyroom/
    ses-20170801/
        sub-emptyroom_ses-20170801_scans.tsv
        meg/
            sub-emptyroom_ses-20170801_task-noise_meg.ds
            sub-emptyroom_ses-20170801_task-noise_meg.json
```

`TaskName` in the `*_meg.json` file should be set to "noise".
