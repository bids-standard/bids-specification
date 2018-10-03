### 3 Coordinate System JSON document (`*_coordsystem.json`)
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>][_acq-<label>]_coordsystem.json]
```

OPTIONAL. A JSON document specifying the coordinate system(s) used for the MEG, EEG, head localization coils, and anatomical landmarks.

MEG and EEG sensors:

| Field name                     | Description                                 |
|:-------------------------------|:--------------------------------------------|
| MEGCoordinateSystem            | REQUIRED. Defines the coordinate system for the MEG sensors. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  ``[MEGCoordinateSystemDescription]``. |
| MEGCoordinateUnits             | REQUIRED. Units of the coordinates of   `MEGCoordinateSystem`.  MUST be `m`, `cm`, or `mm`. |
| MEGCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the MEG coordinate system system in detail. |
| EEGCoordinateSystem            | OPTIONAL. Describes how the coordinates of the EEG sensors are to be interpreted. |
| EEGCoordinateUnits             | OPTIONAL. Units of the coordinates of `EEGCoordinateSystem`.  MUST be `m`, `cm`, or `mm`. |
| EEGCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the EEG coordinate system system in detail. |


Head localization coils:

| Field name                          | Description                            |
|:------------------------------------|:---------------------------------------|
| HeadCoilCoordinates                 | OPTIONAL. Key:value pairs describing head localization coil labels and their coordinates, interpreted following the `HeadCoilCoordinateSystem`,  e.g., {`NAS`: ``[12.7,21.3,13.9]``, `LPA`: ``[5.2,11.3,9.6]``, `RPA`: ``[20.2,11.3,9.1]``}. Note that coils are not always placed at locations that have a known anatomical name (e.g. for Elekta, Yokogawa systems); in that case generic labels can be  used (e.g. {`coil1`: ``[12.2,21.3,12.3]``, `coil2`: ``[6.7,12.3,8.6]``, `coil3`: ``[21.9,11.0,8.1]``} ). |
| HeadCoilCoordinateSystem            | OPTIONAL. Defines the coordinate system for the coils. See Appendix VIII: preferred names of Coordinate systems. If "Other", provide definition of the coordinate system in  `HeadCoilCoordinateSystemDescription`. |
| HeadCoilCoordinateUnits             | OPTIONAL. Units of the coordinates of `HeadCoilCoordinateSystem`. MUST be `m`, `cm`, or `mm`. |
| HeadCoilCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail. |


Digitized head points:

| Field name                                     | Description                 |
|:-----------------------------------------------|:----------------------------|
| DigitizedHeadPoints                            | OPTIONAL. Relative path to the file containing the locations of digitized head points collected during the session (e.g., `sub-01_headshape.pos`). RECOMMENDED for all MEG systems, especially for CTF and 4D/BTi. For Elekta/Neuromag the head points will be stored in the fif file. |
| DigitizedHeadPointsCoordinateSystem            | OPTIONAL. Defines the coordinate system for the digitized head points. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  `DigitizedHeadPointsCoordinateSystemDescription`. |
| DigitizedHeadPointsCoordinateUnits             | OPTIONAL. Units of the coordinates of `DigitizedHeadPointsCoordinateSystem`.  MUST be `m`, `cm`, or `mm`. |
| DigitizedHeadPointsCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Digitized head Points coordinate system system in detail. |


Anatomical MRI:

| Field name  | Description                                                    |
|:------------|:---------------------------------------------------------------|
| IntendedFor | OPTIONAL. Path or list of path relative to the subject subfolder pointing to the structural  MRI, possibly of different types if a list is specified,  to be used with the MEG recording. The path(s) need(s) to use forward slashes instead of backward slashes (e.g. `ses-/anat/sub-01_T1w.nii.gz`). |


Anatomical landmarks:

| Field name                                    | Description                  |
|:----------------------------------------------|:-----------------------------|
| AnatomicalLandmarkCoordinates                 | OPTIONAL. Key:value pairs of the labels and  3-D digitized locations of anatomical landmarks, interpreted following the `AnatomicalLandmarkCoordinateSystem`,  e.g., {"NAS": ``[12.7,21.3,13.9]``, "LPA": ``[5.2,11.3,9.6]``, "RPA": ``[20.2,11.3,9.1]``}. |
| AnatomicalLandmarkCoordinateSystem            | OPTIONAL. Defines the coordinate system for the anatomical landmarks. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  `AnatomicalLandmarkCoordinateSystemDescription`. |
| AnatomicalLandmarkCoordinateUnits             | OPTIONAL. Units of the coordinates of `AnatomicalLandmarkCoordinateSystem`.  MUST be `m`, `cm`, or  `mm`. |
| AnatomicalLandmarkCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail. |


It is also RECOMMENDED that the MRI voxel coordinates of the actual anatomical landmarks for co-registration of MEG with structural MRI are stored in the `AnatomicalLandmarkCoordinates` field in the JSON sidecar of the corresponding T1w MRI anatomical data of the subject seen in the MEG session (see section 8.3) -  for example:
`sub-01/ses-mri/anat/sub-01_ses-mri_acq-mprage_T1w.json`

In principle, these locations are those of  absolute anatomical markers. However, the marking of NAS, LPA and RPA is more ambiguous than that of e.g., AC and PC. This may result in some variability in their 3-D digitization from session to session, even for the same participant. The solution would be to use only one T1w file and populate the `AnatomicalLandmarkCoordinates` field with session-specific labels e.g., "NAS-session1": ``[127,213,139]``,"NAS-session2": ``[123,220,142]``, etc.

Fiducials information:

| Field name           | Description                                           |
|:---------------------|:------------------------------------------------------|
| FiducialsDescription | OPTIONAL. A freeform text field documenting the anatomical landmarks that were used and how the head localization coils were placed relative to these. This field can describe, for instance, whether the true anatomical locations of the left and right pre-auricular points were used and digitized, or rather whether  they were defined as the intersection between the tragus and the helix (the entry of the ear canal), or any other anatomical description of selected points in the vicinity of  the ears. |


For more information on the definition of anatomical landmarks, please visit:
   [http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_define](http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined)

For more information on typical coordinate systems for MEG-MRI
coregistration:
   [http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined), or:
   [http://neuroimage.usc.edu/brainstorm/CoordinateSystems](http://neuroimage.usc.edu/brainstorm/CoordinateSystems)
