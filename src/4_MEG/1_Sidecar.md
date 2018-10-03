#### 1.1 Sidecar JSON document (`*_meg.json`)

Generic  fields
MUST be present:

| Field name | Definition                                                      |
|:-----------|:----------------------------------------------------------------|
| TaskName   | REQUIRED. Name of the task (for resting state use the `rest` prefix). Different Tasks SHOULD NOT have the same name. The Task label is derived from this field by removing all non alphanumeric (``[a-zA-Z0-9]``) characters. |

SHOULD be present:
For consistency between studies and institutions, we encourage users to extract the  values of these fields from the actual raw data. Whenever possible, please avoid using ad-hoc wording.

| Field name             | Definition                                          |
|:-----------------------|:----------------------------------------------------|
| InstitutionName        | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances. |
| InstitutionAddress     | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances. |
| Manufacturer           | RECOMMENDED. Manufacturer of the MEG system (`CTF`, `Elekta/Neuromag`, `4D/BTi`, `KIT/Yokogawa`, `ITAB`, `KRISS`, `Other`). See Appendix VII with preferred names |
| ManufacturersModelName | RECOMMENDED. Manufacturer’s designation of the MEG scanner model (e.g. `CTF-275`). See Appendix VII with preferred names |
| SoftwareVersions       | RECOMMENDED. Manufacturer’s designation of the acquisition software. |
| ManufacturersModelName | RECOMMENDED. Manufacturer’s designation of the MEG scanner model (e.g. `CTF-275`). See Appendix VII with preferred names |
| SoftwareVersions       | RECOMMENDED. Manufacturer’s designation of the acquisition software. |
| TaskDescription        | RECOMMENDED. Description of the task.               |
| Instructions           | RECOMMENDED. Text of the instructions given to participants before the scan. This is not only important for behavioural or cognitive tasks but also in resting state paradigms (e.g. to distinguish between eyes open and eyes closed). |
| CogAtlasID             | RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) term that describes the task (e.g. Resting State with eyes closed "[http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b](http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b)") |
| CogPOID                | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task  (e.g. Rest "[http://wiki.cogpo.org/index.php?title=Rest](http://wiki.cogpo.org/index.php?title=Rest)") |
| DeviceSerialNumber     | RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset. |


Specific MEG fields
MUST be present:

| Field name          | Definition                                             |
|:--------------------|:-------------------------------------------------------|
| SamplingFrequency   | REQUIRED. Sampling frequency (in Hz) of all the data in the recording, regardless of their type  (e.g., 2400) |
| PowerLineFrequency  | REQUIRED. Frequency (in Hz) of the power grid at the geographical location of the MEG instrument (i.e. 50 or 60) |
| DewarPosition       | REQUIRED. Position of the dewar during the MEG scan: `upright`, `supine` or `degrees` of angle from vertical: for example on CTF systems, upright=15°, supine = 90°. |
| SoftwareFilters     | REQUIRED. List of temporal and/or spatial software filters applied, or ideally  key:value pairs of pre-applied software filters and their parameter values: e.g., {"SSS": {"frame": "head", "badlimit": 7}}, {"SpatialCompensation": {"GradientOrder": Order of the gradient compensation}}. Write `n/a` if no software filters applied. |
| DigitizedLandmarks  | REQUIRED. Boolean ("true" or "false") value indicating whether anatomical landmark  points (i.e. fiducials) are contained within this recording. |
| DigitizedHeadPoints | REQUIRED. Boolean (`true` or `false`) value indicating whether head points outlining the scalp/face surface are contained within this recording. |


SHOULD be present

| Field name                 | Definition                                      |
|:---------------------------|:------------------------------------------------|
| MEGChannelCount            | RECOMMENDED. Number of MEG channels (e.g. 275)  |
| MEGREFChannelCount         | RECOMMENDED. Number of MEG reference channels (e.g. 23). For systems without such channels (e.g. Neuromag Vectorview), `MEGREFChannelCount`=0 |
| EEGChannelCount            | RECOMMENDED. Number of EEG channels recorded simultaneously (e.g. 21) |
| ECOGChannelCount           | RECOMMENDED. Number of ECoG channels            |
| SEEGChannelCount           | RECOMMENDED. Number of SEEG channels            |
| EOGChannelCount            | RECOMMENDED. Number of EOG channels             |
| ECGChannelCount            | RECOMMENDED. Number of ECG channels             |
| EMGChannelCount            | RECOMMENDED. Number of EMG channels             |
| MiscChannelCount           | RECOMMENDED. Number of miscellaneous analog channels for auxiliary  signals |
| TriggerChannelCount        | RECOMMENDED. Number of channels for digital (TTL bit level) triggers |
| RecordingDuration          | RECOMMENDED. Length of the recording in seconds (e.g. 3600) |
| RecordingType              | RECOMMENDED. Defines whether the recording is  `continuous` or  `epoched`; this latter limited to time windows about events of interest (e.g., stimulus presentations, subject responses etc.) |
| EpochLength                | RECOMMENDED. Duration of individual epochs in seconds (e.g. 1) in case of epoched data |
| ContinuousHeadLocalization | RECOMMENDED. Boolean (`true` or `false`) value indicating whether continuous head localisation was performed. |
| HeadCoilFrequency          | RECOMMENDED. List of frequencies (in Hz) used by the head localisation coils (‘HLC’ in CTF systems, ‘HPI’ in Elekta, ‘COH’ in 4D/BTi) that track the subject’s head position in the MEG helmet (e.g. ``[293, 307, 314, 321]``) |
| MaxMovement                | RECOMMENDED. Maximum head movement (in mm) detected during the recording, as measured by the head localisation coils (e.g., 4.8) |
| SubjectArtefactDescription | RECOMMENDED. Freeform description of the observed subject artefact and its possible cause (e.g. "Vagus Nerve Stimulator", "non-removable implant"). If this field is set to `n/a`, it will be interpreted as absence of major source of artifacts except cardiac and blinks. |
| AssociatedEmptyRoom        | RECOMMENDED. Relative path in BIDS folder structure to empty-room file associated with the subject’s MEG recording. The path needs to use forward slashes instead of backward slashes (e.g. `sub-emptyroom/ses-/meg/sub-emptyroom_ses-_task-noise_run-_meg.ds`). |


Specific EEG fields (if recorded with MEG)
SHOULD be present:

| Field name                      | Definition                                 |
|:--------------------------------|:-------------------------------------------|
| EEGPlacementScheme              | OPTIONAL. Placement scheme of EEG electrodes. Either the name of a standardised placement system (e.g., "10-20") or a list of standardised electrode names (e.g. ``["Cz", "Pz"]``). |
| ManufacturersAmplifierModelName | OPTIONAL. Manufacturer’s designation of the EEG amplifier model (e.g., `Biosemi-ActiveTwo`). |
| CapManufacturer                 | OPTIONAL. Manufacturer of the EEG cap (e.g. `EasyCap`) |
| CapManufacturersModelName       | OPTIONAL. Manufacturer’s designation of the EEG cap model (e.g., `M10`) |
| EEGReference                    | OPTIONAL. Description of the type of EEG reference used (e.g., `M1` for left mastoid, `average`, or `longitudinal bipolar`). |


By construct, EEG when recorded simultaneously with the same MEG system , should have the same `SamplingFrequency` as MEG. Note that if EEG is recorded with a separate amplifier, it should be stored separately under a new /eeg data type (see BEP006).

Example:

```JSON
{
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "Manufacturer": "CTF",
   "ManufacturersModelName": "CTF-275",
   "DeviceSerialNumber": "11035",
   "SoftwareVersions": "Acq 5.4.2-linux-20070507",
   "PowerLineFrequency": 60,
   "SamplingFrequency": 2400,
   "MEGChannelCount": 270,
   "MEGREFChannelCount": 26,
   "EEGChannelCount": 0,
   "EOGChannelCount": 2,
   "ECGChannelCount": 1,
   "EMGChannelCount": 0,
     "DewarPosition": "upright",
   "SoftwareFilters": {
     "SpatialCompensation": {"GradientOrder": "3rd"}
   },
   "RecordingDuration": 600,
   "RecordingType": "continuous",
   "EpochLength": 0,
   "TaskName": "rest",
   "ContinuousHeadLocalization": true,
   "HeadCoilFrequency": [1470,1530,1590],
   "DigitizedLandmarks": true,
   "DigitizedHeadPoints": true
}
```

Note that the date and time information SHOULD be stored in the Study key file (`scans.tsv`), see section 8.8. Scans.tsv. As it is indicated there, date time information MUST be expressed in the following format `YYYY-MM-DDThh:mm:ss` ([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending on local REB/IRB ethics board policy.
