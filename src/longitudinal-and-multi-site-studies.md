# Longitudinal and multi-site studies

Multiple sessions (visits) are encoded by adding an extra layer of directories
and [filenames](common-principles.md#filenames)
in the form of a session (for example `ses-<label>`) and
with a [`*_sessions.tsv` file](modality-agnostic-files.md#sessions-file).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-control01": {
        "ses-predrug": {
            "anat": {
                "sub-control01_ses-predrug_T1w.nii.gz": "",
                "sub-control01_ses-predrug_T1w.json": "",
                "sub-control01_ses-predrug_T2w.nii.gz": "",
                "sub-control01_ses-predrug_T2w.json": "",
                },
            "func": {
                "sub-control01_ses-predrug_task-nback_bold.nii.gz": "",
                "sub-control01_ses-predrug_task-nback_bold.json": "",
                "sub-control01_ses-predrug_task-nback_events.tsv": "",
                "sub-control01_ses-predrug_task-nback_physio.tsv.gz": "",
                "sub-control01_ses-predrug_task-nback_physio.json": "",
                "sub-control01_ses-predrug_task-nback_sbref.nii.gz": "",
                },
            "dwi": {
                "sub-control01_ses-predrug_dwi.nii.gz": "",
                "sub-control01_ses-predrug_dwi.bval": "",
                "sub-control01_ses-predrug_dwi.bvec": "",
                },
            "fmap": {
                "sub-control01_ses-predrug_phasediff.nii.gz": "",
                "sub-control01_ses-predrug_phasediff.json": "",
                "sub-control01_ses-predrug_magnitude1.nii.gz": "",
                },
            "sub-control01_ses-predrug_scans.tsv": "",
            },
        "ses-postdrug": {
            "func": {
                "sub-control01_ses-postdrug_task-nback_bold.nii.gz": "",
                "sub-control01_ses-postdrug_task-nback_bold.json": "",
                "sub-control01_ses-postdrug_task-nback_events.tsv": "",
                "sub-control01_ses-postdrug_task-nback_physio.tsv.gz": "",
                "sub-control01_ses-postdrug_task-nback_physio.json": "",
                "sub-control01_ses-postdrug_task-nback_sbref.nii.gz": "",
                },
            "fmap": {
                "sub-control01_ses-postdrug_phasediff.nii.gz": "",
                "sub-control01_ses-postdrug_phasediff.json": "",
                "sub-control01_ses-postdrug_magnitude1.nii.gz": "",
                }
            },
        "sub-control01_sessions.tsv": "",
        },
    "participants.tsv": "",
    "dataset_description.json": "",
    "README": "",
    "CHANGES": "",
    }
) }}

`sub-control01_sessions.tsv` content:

```tsv
session_id	acq_time	systolic_blood_pressure
ses-predrug	2009-06-15T13:45:30	120
ses-postdrug	2009-06-16T13:45:30	100
```

See this [example dataset](https://github.com/bids-standard/bids-examples/tree/master/7t_trt)
that has been formatted
using this specification and can be used
for practical guidance when curating a new longitudinal dataset.

## Multi-site or multi-center studies

This version of the BIDS specification does not explicitly cover studies with
data coming from multiple sites or multiple centers (such extension is planned
in [BIDS `2.0`](https://github.com/bids-standard/bids-2-devel/issues/11)).
There are however ways to model your data without any loss in terms of metadata.

### Option 1: Treat each site/center as a separate dataset

The simplest way of dealing with multiple sites is to treat data from each site
as a separate and independent BIDS dataset with a separate participants.tsv and
other metadata files. This way you can feed each dataset individually to BIDS
Apps and everything should just work.

### Option 2: Combining sites/centers into one dataset

Alternatively you can combine data from all sites into one dataset.
This can be done in two ways:

#### Option 2.a: Collate sites at subject level

To identify which site each subjects comes from you can add a `site` column in the
`participants.tsv` file indicating the source site. This solution allows you to
analyze all subjects together in one dataset. One caveat is that subjects
from all sites will have to have unique labels. To enforce that and improve
readability you can use a subject label prefix identifying the site. For example
`sub-NUY001`, `sub-MIT002`, `sub-MPG002` and so on. Remember that hyphens and
underscores are not allowed in subject labels.

#### Option 2.b: Use different sessions for different sites

In case of studies such as "Traveling Human Phantom" it is possible to incorporate site within session label.
For example `sub-human1/ses-NUY`, `sub-human1/ses-MIT`, `sub-phantom1/ses-NUY`, `sub-phantom1/ses-MIT` and so on.
