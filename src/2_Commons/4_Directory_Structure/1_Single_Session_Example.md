1 Single session example
------------------------

This is an example of the folder and file structure. Because there is only one session, the session level is not required by the
format. For details on individual files see descriptions in the next
section:

```
sub-control01/
    anat/
        sub-control01_T1w.nii.gz
        sub-control01_T1w.json
        sub-control01_T2w.nii.gz
        sub-control01_T2w.json
    func/
        sub-control01_task-nback_bold.nii.gz
        sub-control01_task-nback_bold.json
        sub-control01_task-nback_events.tsv
        sub-control01_task-nback_physio.tsv.gz
        sub-control01_task-nback_physio.json
        sub-control01_task-nback_sbref.nii.gz
    dwi/
        sub-control01_dwi.nii.gz
        sub-control01_dwi.bval
        sub-control01_dwi.bvec
    fmap/
        sub-control01_phasediff.nii.gz
        sub-control01_phasediff.json
        sub-control01_magnitude1.nii.gz
        sub-control01_scans.tsv

    code/
        deface.py
    derivatives/
    README
    participants.tsv
    dataset_description.json
    CHANGES
```

Additional files and folders containing raw data may be added as needed for special cases.  They should be named using all lowercase with a name that reflects the nature of the scan (e.g., `calibration`).  Naming of files within the directory should follow the same scheme as above (e.g., `sub-control01_calibration_Xcalibration.nii.gz`)
