### 5 3-D head point /electrode locations file (`*_headshape.<manufacturer_specific_format>`)
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>][_acq-<label>]_headshape.<manufacturer_specific_extension>]
```

![placement of NAS fiducial](images/sub-0001_ses-001_acq-NAS_photo.jpg "placement of NAS fiducial")
This file is RECOMMENDED.

The 3-D locations of head points and/or EEG electrode locations can be digitized and stored in separate files. The `*_acq-<label>` can be used when more than one type of digitization in done for a session, for example when the head points are in a separate file from the EEG locations. These files are stored in the specific format of the 3-D digitizer’s manufacturer (see Appendix VI).

Example:

```
sub-control01
    ses-01
        sub-control01_ses-01_acq-HEAD_headshape.pos
        sub-control01_ses-01_acq-ECG_headshape.pos
```

Note that the `*_headshape` file(s) is shared by all the runs and tasks in a session. If the subject needs to be taken out of the scanner and the head-shape has to be updated, then for MEG it could be considered to be a new session.
