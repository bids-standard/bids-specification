# Longitudinal and multi-site studies

Multiple sessions (visits) are encoded by adding an extra layer of directories
and file names in the form of `ses-<label>`. Session label can consist
only of alphanumeric characters `[a-zA-Z0-9]` and should be consistent across
subjects. If numbers are used in session labels we recommend using zero padding
(for example `ses-01`, `ses-11` instead of `ses-1`, `ses-11`). This makes
results of alphabetical sorting more intuitive. Acquisition time of session can
be defined in the sessions file (see below for details).

The extra session layer (at least one `/ses-<label>` subfolder) should
be added for all subjects if at least one subject in the dataset has more than
one session. Skipping the session layer for only some subjects in the dataset is
not allowed. If a `/ses-<label>` subfolder is included as part of the
directory hierarchy, then the same `ses-<label>` tag must also be
included as part of the file names themselves.

```Text
sub-control01/
    ses-predrug/
        anat/
            sub-control01_ses-predrug_T1w.nii.gz
            sub-control01_ses-predrug_T1w.json
            sub-control01_ses-predrug_T2w.nii.gz
            sub-control01_ses-predrug_T2w.json
        func/
            sub-control01_ses-predrug_task-nback_bold.nii.gz
            sub-control01_ses-predrug_task-nback_bold.json
            sub-control01_ses-predrug_task-nback_events.tsv
            sub-control01_ses-predrug_task-nback_cont-physio.tsv.gz
            sub-control01_ses-predrug_task-nback_cont-physio.json
            sub-control01_ses-predrug_task-nback_sbref.nii.gz
        dwi/
            sub-control01_ses-predrug_dwi.nii.gz
            sub-control01_ses-predrug_dwi.bval
            sub-control01_ses-predrug_dwi.bvec
        fmap/
            sub-control01_ses-predrug_phasediff.nii.gz
            sub-control01_ses-predrug_phasediff.json
            sub-control01_ses-predrug_magnitude1.nii.gz
        sub-control01_ses-predrug_scans.tsv
    ses-postdrug/
        func/
            sub-control01_ses-postdrug_task-nback_bold.nii.gz
            sub-control01_ses-postdrug_task-nback_bold.json
            sub-control01_ses-postdrug_task-nback_events.tsv
            sub-control01_ses-postdrug_task-nback_cont-physio.tsv.gz
            sub-control01_ses-postdrug_task-nback_cont-physio.json
            sub-control01_ses-postdrug_task-nback_sbref.nii.gz
        fmap/
            sub-control01_ses-postdrug_phasediff.nii.gz
            sub-control01_ses-postdrug_phasediff.json
            sub-control01_ses-postdrug_magnitude1.nii.gz
        sub-control01_ses-postdrug_scans.tsv
    sub-control01_sessions.tsv
participants.tsv
dataset_description.json
README
CHANGES
```

## Sessions file

Template:

```Text
sub-<label>/
    sub-<label>_sessions.tsv
```

Optional: Yes

In case of multiple sessions there is an option of adding additional
participant key files describing variables changing between sessions. In such
case one file per participant should be added. These files need to include
compulsory `session_id` column and describe each session by one and only one
row. Column names in per participant key files have to be different from group
level participant key column names.

`_sessions.tsv` example:

```Text
session_id  acq_time  systolic_blood_pressure
ses-predrug 2009-06-15T13:45:30 120
ses-postdrug  2009-06-16T13:45:30 100
ses-followup  2009-06-17T13:45:30 110
```

## Multi-site or multi-center studies

This version of the BIDS specification does not explicitly cover studies with
data coming from multiple sites or multiple centers (such extension is planned
in [BIDS `2.0`](https://docs.google.com/document/d/1LEgsMiisGDe1Gv-hBp1EcLmoz7AlKj6VYULUgDD3Zdw/)).
There are however ways to model your data without any loss in terms of metadata.

### Treat each site/center as a separate dataset

The simplest way of dealing with multiple sites is to treat data from each site
as a separate and independent BIDS dataset with a separate participants.tsv and
other metadata files. This way you can feed each dataset individually to BIDS
Apps and everything should just work.

### Option 2: Combining sites/centers into one dataset

Alternatively you can combine data from all sites into one dataset. To identify
which site each subjects comes from you can add a `site` column in the
`participants.tsv` file indicating the source site. This solution allows you to
analyze all of the subjects together in one dataset. One caveat is that subjects
from all sites will have to have unique labels. To enforce that and improve
readability you can use a subject label prefix identifying the site. For example
`sub-NUY001`, `sub-MIT002`, `sub-MPG002` etc. Remember that hyphens and
underscores are not allowed in subject labels.
