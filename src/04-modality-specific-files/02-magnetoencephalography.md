# Magnetoencephalography

Support for Magnetoencephalography (MEG) was developed as a [BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please cite the following paper when referring to this part of the standard in
context of the academic literature:

> Niso Galan, J.G., Gorgolewski, K.J., Bock, E., Brooks, T.L., Flandin, G.,
> Gramfort, A., Henson, R.N., Jas, M., Litvak, V., Moreau, J., Oostenveld, R.,
> Schoffelen, J.-M., Tadel, F., Wexler, J., Baillet, S. (2018). **MEG-BIDS, the
> brain imaging data structure extended to magnetoencephalography**. Scientific
> data, 5. doi: [10.1038/sdata.2018.110](https://doi.org/10.1038/sdata.2018.110)

## MEG recording data

Template:

```Text
sub-<label>/
    [ses-<label>]/
      meg/
        sub-<label>[_ses-<label>]_task-<label>[_run-<index>][_proc-<label>]_meg.<manufacturer_specific_extension>
        [sub-<label>[_ses-<label>]_task-<label>[_run-<index>][_proc-<label>]_meg.json]
```

Unprocessed MEG data MUST be stored in the native file format of the MEG
instrument with which the data was collected.
With the MEG specification of BIDS, we wish to promote the adoption of good
practices in the management of scientific data.
Hence, the emphasis is not to impose a new, generic data format for the
modality, but rather to standardize the way data is stored in repositories.
Further, there is currently no widely accepted standard file format for MEG, but
major software applications, including free and open-source solutions for MEG
data analysis, provide readers of such raw files.

Some software readers may skip important metadata that is specific to MEG system
manufacturers. It is therefore RECOMMENDED that users provide additional meta
information extracted from the manufacturer raw data files in a sidecar JSON
file. This allows for easy searching and indexing of key metadata elements
without the need to parse files in proprietary data format. Other relevant files
MAY be included alongside the MEG data; examples are provided below.

This template is for MEG data of any kind, including but not limited to
task-based, resting-state, and noise recordings. If multiple Tasks were
performed within a single Run, the task description can be set to
`task-multitask`. The \_meg.json SHOULD contain details on the Tasks.

Some manufacturers' data storage conventions use folders which contain data
files of various nature: for example, CTF's `.ds` format, or BTi/4D.
Yet other manufacturers split their files once they exceed a certain size
limit. For example Neuromag/Elekta/Megin, which can produce several files
for a single recording. Both `some_file.fif` and `some_file-1.fif` would
belong to a single recording. In BIDS, the `split` entity is RECOMMENDED to
deal with split files.
Please refer to [Appendix VI](../99-appendices/06-meg-file-formats.md) for
general information on how to deal with such manufacturer specifics and to see
more examples.

The `proc` label is analogous to `rec` for MR and denotes a variant of a file
that was a result of particular processing performed on the device. This is
useful for files produced in particular by Elekta’s MaxFilter (e.g. sss, tsss,
trans, quat, mc, etc.), which some installations impose to be run on raw data
because of active shielding software corrections before the MEG data can
actually be exploited.

### Sidecar JSON (`*_meg.json`)

Generic fields MUST be present:

| Field name | Definition                                                                                                                                                                                                                                                                                                                              |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TaskName   | REQUIRED. Name of the task (for resting state use the `rest` prefix). No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric (`[a-zA-Z0-9]`) characters. For example TaskName `faces n-back` will correspond to task label `facesnback`. |

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad-hoc wording.

| Field name             | Definition                                                                                                                                                                                                                                                                      |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| InstitutionName        | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                      |
| InstitutionAddress     | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                   |
| Manufacturer           | RECOMMENDED. Manufacturer of the MEG system (`CTF`, `Elekta/Neuromag`, `BTi/4D`, `KIT/Yokogawa`, `ITAB`, `KRISS`, `Other`). See [Appendix VII](../99-appendices/07-meg-systems.md) with preferred names                                                                         |
| ManufacturersModelName | RECOMMENDED. Manufacturer’s designation of the MEG scanner model (e.g. `CTF-275`). See [Appendix VII](../99-appendices/07-meg-systems.md) with preferred names                                                                                                                  |
| SoftwareVersions       | RECOMMENDED. Manufacturer’s designation of the acquisition software.                                                                                                                                                                                                            |
| TaskDescription        | RECOMMENDED. Description of the task.                                                                                                                                                                                                                                           |
| Instructions           | RECOMMENDED. Text of the instructions given to participants before the scan. This is not only important for behavioral or cognitive tasks but also in resting state paradigms (e.g. to distinguish between eyes open and eyes closed).                                          |
| CogAtlasID             | RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) term that describes the task (e.g. Resting State with eyes closed "[http://www.cognitiveatlas.org/task/id/trm_54e69c642d89b](http://www.cognitiveatlas.org/task/id/trm_54e69c642d89b)") |
| CogPOID                | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task (e.g. Rest "[http://wiki.cogpo.org/index.php?title=Rest](http://wiki.cogpo.org/index.php?title=Rest)")                                                                        |
| DeviceSerialNumber     | RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset.                                                   |

Specific MEG fields MUST be present:

| Field name          | Definition                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SamplingFrequency   | REQUIRED. Sampling frequency (in Hz) of all the data in the recording, regardless of their type (e.g., 2400)                                                                                                                                                                                                                                                                                                                      |
| PowerLineFrequency  | REQUIRED. Frequency (in Hz) of the power grid at the geographical location of the MEG instrument (i.e. 50 or 60)                                                                                                                                                                                                                                                                                                                  |
| DewarPosition       | REQUIRED. Position of the dewar during the MEG scan: `upright`, `supine` or `degrees` of angle from vertical: for example on CTF systems, upright=15°, supine = 90°.                                                                                                                                                                                                                                                              |
| SoftwareFilters     | REQUIRED. A [JSON object](https://www.w3schools.com/js/js_json_objects.asp) of temporal software filters applied, or `"n/a"` if the data is not available. Each key:value pair in the JSON object is a name of the filter and an object in which its parameters are defined as key:value pairs. E.g., `{"SSS": {"frame": "head", "badlimit": 7}, "SpatialCompensation": {"GradientOrder": "Order of the gradient compensation"}}` |
| DigitizedLandmarks  | REQUIRED. Boolean ("true" or "false") value indicating whether anatomical landmark points (i.e. fiducials) are contained within this recording.                                                                                                                                                                                                                                                                                   |
| DigitizedHeadPoints | REQUIRED. Boolean (`true` or `false`) value indicating whether head points outlining the scalp/face surface are contained within this recording.                                                                                                                                                                                                                                                                                  |

SHOULD be present:

| Field name                 | Definition                                                                                                                                                                                                                                                                                                                                                                                          |
| ------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MEGChannelCount            | RECOMMENDED. Number of MEG channels (e.g. 275)                                                                                                                                                                                                                                                                                                                                                      |
| MEGREFChannelCount         | RECOMMENDED. Number of MEG reference channels (e.g. 23). For systems without such channels (e.g. Neuromag Vectorview), `MEGREFChannelCount`=0                                                                                                                                                                                                                                                       |
| EEGChannelCount            | RECOMMENDED. Number of EEG channels recorded simultaneously (e.g. 21)                                                                                                                                                                                                                                                                                                                               |
| ECOGChannelCount           | RECOMMENDED. Number of ECoG channels                                                                                                                                                                                                                                                                                                                                                                |
| SEEGChannelCount           | RECOMMENDED. Number of SEEG channels                                                                                                                                                                                                                                                                                                                                                                |
| EOGChannelCount            | RECOMMENDED. Number of EOG channels                                                                                                                                                                                                                                                                                                                                                                 |
| ECGChannelCount            | RECOMMENDED. Number of ECG channels                                                                                                                                                                                                                                                                                                                                                                 |
| EMGChannelCount            | RECOMMENDED. Number of EMG channels                                                                                                                                                                                                                                                                                                                                                                 |
| MiscChannelCount           | RECOMMENDED. Number of miscellaneous analog channels for auxiliary signals                                                                                                                                                                                                                                                                                                                          |
| TriggerChannelCount        | RECOMMENDED. Number of channels for digital (TTL bit level) triggers                                                                                                                                                                                                                                                                                                                                |
| RecordingDuration          | RECOMMENDED. Length of the recording in seconds (e.g. 3600)                                                                                                                                                                                                                                                                                                                                         |
| RecordingType              | RECOMMENDED. Defines whether the recording is `continuous` or `epoched`; this latter limited to time windows about events of interest (e.g., stimulus presentations, subject responses etc.)                                                                                                                                                                                                        |
| EpochLength                | RECOMMENDED. Duration of individual epochs in seconds (e.g. 1) in case of epoched data                                                                                                                                                                                                                                                                                                              |
| ContinuousHeadLocalization | RECOMMENDED. Boolean (`true` or `false`) value indicating whether continuous head localisation was performed.                                                                                                                                                                                                                                                                                       |
| HeadCoilFrequency          | RECOMMENDED. List of frequencies (in Hz) used by the head localisation coils (‘HLC’ in CTF systems, ‘HPI’ in Elekta, ‘COH’ in BTi/4D) that track the subject’s head position in the MEG helmet (e.g. `[293, 307, 314, 321]`)                                                                                                                                                                        |
| MaxMovement                | RECOMMENDED. Maximum head movement (in mm) detected during the recording, as measured by the head localisation coils (e.g., 4.8)                                                                                                                                                                                                                                                                    |
| SubjectArtefactDescription | RECOMMENDED. Freeform description of the observed subject artefact and its possible cause (e.g. "Vagus Nerve Stimulator", "non-removable implant"). If this field is set to `n/a`, it will be interpreted as absence of major source of artifacts except cardiac and blinks.                                                                                                                        |
| AssociatedEmptyRoom        | RECOMMENDED. Relative path in BIDS folder structure to empty-room file associated with the subject’s MEG recording. The path needs to use forward slashes instead of backward slashes (e.g. `sub-emptyroom/ses-/meg/sub-emptyroom_ses-_task-noise_run-_meg.ds`).                                                                                                                                    |
| HardwareFilters            | RECOMMENDED. A [JSON object](https://www.w3schools.com/js/js_json_objects.asp) of temporal hardware filters applied, or `"n/a"` if the data is not available. Each key:value pair in the JSON object is a name of the filter and an object in which its parameters are defined as key:value pairs. E.g., `{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dB/Octave"}}` |

Specific EEG fields (if recorded with MEG) SHOULD be present:

| Field name                      | Definition                                                                                                                                                                        |
| -------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EEGPlacementScheme              | OPTIONAL. Placement scheme of EEG electrodes. Either the name of a standardised placement system (e.g., "10-20") or a list of standardised electrode names (e.g. `["Cz", "Pz"]`). |
| CapManufacturer                 | OPTIONAL. Manufacturer of the EEG cap (e.g. `EasyCap`)                                                                                                                            |
| CapManufacturersModelName       | OPTIONAL. Manufacturer’s designation of the EEG cap model (e.g., `M10`)                                                                                                           |
| EEGReference                    | OPTIONAL. Description of the type of EEG reference used (e.g., `M1` for left mastoid, `average`, or `longitudinal bipolar`).                                                      |

By construct, EEG when recorded simultaneously with the same MEG system , should
have the same `SamplingFrequency` as MEG. Note that if EEG is recorded with a
separate amplifier, it should be stored separately under a new `/eeg` data type
(see [the EEG specification](03-electroencephalography.md)).

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

Note that the date and time information SHOULD be stored in the Study key file
(`scans.tsv`), see [Scans file](../03-modality-agnostic-files.md#scans-file). As
it is indicated there, date time information MUST be expressed in the following
format `YYYY-MM-DDThh:mm:ss`
([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For
example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending
on local REB/IRB ethics board policy.

## Channels description (`*_channels.tsv`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      meg/
        [sub-<label>[_ses-<label>]_task-<label>[_run-<index>][_proc-<label>]_channels.tsv]
```

This file is RECOMMENDED as it provides easily searchable information across
BIDS datasets for e.g., general curation, response to queries or batch
analysis.
To avoid confusion, the channels SHOULD be listed in the order they
appear in the MEG data file.
Missing values MUST be indicated with `n/a`.

The columns of the Channels description table stored in `*_channels.tsv` are:

MUST be present:

| Column name | Definition                                                                                                                                                                       |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name        | REQUIRED. Channel name (e.g., MRT012, MEG023)                                                                                                                                    |
| type        | REQUIRED. Type of channel; MUST use the channel types listed below.                                                                                                              |
| units       | REQUIRED. Physical unit of the value represented in this channel, e.g., `V` for Volt, or `fT/cm` for femto Tesla per centimeter (see [Units](../02-common-principles.md#units)). |

SHOULD be present:

| Column name        | Definition                                                                                                                                                                                                                                                                    |
| ----------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| description        | OPTIONAL. Brief free-text description of the channel, or other information of interest. See examples below.                                                                                                                                                                   |
| sampling_frequency | OPTIONAL. Sampling rate of the channel in Hz.                                                                                                                                                                                                                                 |
| low_cutoff         | OPTIONAL. Frequencies used for the high-pass filter applied to the channel in Hz. If no high-pass filter applied, use `n/a`.                                                                                                                                                  |
| high_cutoff        | OPTIONAL. Frequencies used for the low-pass filter applied to the channel in Hz. If no low-pass filter applied, use `n/a`. Note that hardware anti-aliasing in A/D conversion of all MEG/EEG electronics applies a low-pass filter; specify its frequency here if applicable. |
| notch              | OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use `n/a`.                                                                                                                                                         |
| software_filters   | OPTIONAL. List of temporal and/or spatial software filters applied (e.g. "SSS", `"SpatialCompensation"`). Note that parameters should be defined in the general MEG sidecar .json file. Indicate `n/a` in the absence of software filters applied.                            |
| status             | OPTIONAL. Data quality observed on the channel `(good/bad)`. A channel is considered `bad` if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in `[status_description]`.                                                     |
| status_description | OPTIONAL. Freeform text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in `[status]`.                                                                                                        |

Example:

```Text
name type units description sampling_frequency  low_cutoff  high_cutoff notch software_filters status
UDIO001 TRIG V analogue trigger 1200  0.1 300 0 n/a good
MLC11 MEGGRADAXIAL T sensor 1st-order grad 1200 0 n/a 50 SSS bad
```

Restricted keyword list for field `type`

| Keyword          | Definition                                           |
| ---------------- | ---------------------------------------------------- |
| MEGMAG           | MEG magnetometer                                     |
| MEGGRADAXIAL     | MEG axial gradiometer                                |
| MEGGRADPLANAR    | MEG planargradiometer                                |
| MEGREFMAG        | MEG reference magnetometer                           |
| MEGREFGRADAXIAL  | MEG reference axial gradiometer                      |
| MEGREFGRADPLANAR | MEG reference planar gradiometer                     |
| MEGOTHER         | Any other type of MEG sensor                         |
| EEG              | Electrode channel                                    |
| ECOG             | Electrode channel                                    |
| SEEG             | Electrode channel                                    |
| DBS              | Electrode channel                                    |
| VEOG             | Vertical EOG (electrooculogram)                      |
| HEOG             | Horizontal EOG                                       |
| EOG              | Generic EOG channel                                  |
| ECG              | ElectroCardioGram (heart)                            |
| EMG              | ElectroMyoGram (muscle)                              |
| TRIG             | System Triggers                                      |
| AUDIO            | Audio signal                                         |
| PD               | Photodiode                                           |
| EYEGAZE          | Eye Tracker gaze                                     |
| PUPIL            | Eye Tracker pupil diameter                           |
| MISC             | Miscellaneous                                        |
| SYSCLOCK         | System time showing elapsed time since trial started |
| ADC              | Analog to Digital input                              |
| DAC              | Digital to Analog output                             |
| HLU              | Measured position of head and head coils             |
| FITERR           | Fit error signal from each head localization coil    |
| OTHER            | Any other type of channel                            |

Example of free text for field `description`

-   stimulus, response, vertical EOG, horizontal EOG, skin conductance, sats,
    intracranial, eyetracker

Example:

```Text
name type units description
VEOG VEOG V vertical EOG
FDI EMG V left first dorsal interosseous
UDIO001 TRIG V analog trigger signal
UADC001 AUDIO V envelope of audio signal presented to participant
```

## Coordinate System JSON (`*_coordsystem.json`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      meg/
        [sub-<label>[_ses-<label>][_acq-<label>]_coordsystem.json]
```

OPTIONAL. A JSON document specifying the coordinate system(s) used for the MEG,
EEG, head localization coils, and anatomical landmarks.

MEG and EEG sensors:

| Field name                     | Description                                                                                                                                                                                                                                                        |
| ----------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MEGCoordinateSystem            | REQUIRED. Defines the coordinate system for the MEG sensors. See [Appendix VIII](../99-appendices/08-coordinate-systems.md): preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in `[MEGCoordinateSystemDescription]`. |
| MEGCoordinateUnits             | REQUIRED. Units of the coordinates of `MEGCoordinateSystem`. MUST be `m`, `cm`, or `mm`.                                                                                                                                                                           |
| MEGCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the MEG coordinate system system in detail.                                                                                                                                                     |
| EEGCoordinateSystem            | OPTIONAL. Describes how the coordinates of the EEG sensors are to be interpreted.                                                                                                                                                                                  |
| EEGCoordinateUnits             | OPTIONAL. Units of the coordinates of `EEGCoordinateSystem`. MUST be `m`, `cm`, or `mm`.                                                                                                                                                                           |
| EEGCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the EEG coordinate system system in detail.                                                                                                                                                     |

Head localization coils:

| Field name                          | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| HeadCoilCoordinates                 | OPTIONAL. Key:value pairs describing head localization coil labels and their coordinates, interpreted following the `HeadCoilCoordinateSystem`, e.g., {`NAS`: `[12.7,21.3,13.9]`, `LPA`: `[5.2,11.3,9.6]`, `RPA`: `[20.2,11.3,9.1]`}. Note that coils are not always placed at locations that have a known anatomical name (e.g. for Elekta, Yokogawa systems); in that case generic labels can be used (e.g. {`coil1`: `[12.2,21.3,12.3]`, `coil2`: `[6.7,12.3,8.6]`, `coil3`: `[21.9,11.0,8.1]`} ). |
| HeadCoilCoordinateSystem            | OPTIONAL. Defines the coordinate system for the coils. See [Appendix VIII](../99-appendices/08-coordinate-systems.md): preferred names of Coordinate systems. If "Other", provide definition of the coordinate system in `HeadCoilCoordinateSystemDescription`.                                                                                                                                                                                                                                       |
| HeadCoilCoordinateUnits             | OPTIONAL. Units of the coordinates of `HeadCoilCoordinateSystem`. MUST be `m`, `cm`, or `mm`.                                                                                                                                                                                                                                                                                                                                                                                                         |
| HeadCoilCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail.                                                                                                                                                                                                                                                                                                                                                                                  |

Digitized head points:

| Field name                                     | Description                                                                                                                                                                                                                                                                                |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DigitizedHeadPoints                            | OPTIONAL. Relative path to the file containing the locations of digitized head points collected during the session (e.g., `sub-01_headshape.pos`). RECOMMENDED for all MEG systems, especially for CTF and BTi/4D. For Elekta/Neuromag the head points will be stored in the fif file.     |
| DigitizedHeadPointsCoordinateSystem            | OPTIONAL. Defines the coordinate system for the digitized head points. See [Appendix VIII](../99-appendices/08-coordinate-systems.md): preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in `DigitizedHeadPointsCoordinateSystemDescription`. |
| DigitizedHeadPointsCoordinateUnits             | OPTIONAL. Units of the coordinates of `DigitizedHeadPointsCoordinateSystem`. MUST be `m`, `cm`, or `mm`.                                                                                                                                                                                   |
| DigitizedHeadPointsCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Digitized head Points coordinate system system in detail.                                                                                                                                                           |

Anatomical MRI:

| Field name  | Description                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| IntendedFor | OPTIONAL. Path or list of path relative to the subject subfolder pointing to the structural MRI, possibly of different types if a list is specified, to be used with the MEG recording. The path(s) need(s) to use forward slashes instead of backward slashes (e.g. `ses-/anat/sub-01_T1w.nii.gz`). |

Anatomical landmarks:

| Field name                                    | Description                                                                                                                                                                                                                                                                              |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnatomicalLandmarkCoordinates                 | OPTIONAL. Key:value pairs of the labels and 3-D digitized locations of anatomical landmarks, interpreted following the `AnatomicalLandmarkCoordinateSystem`, e.g., {"NAS": `[12.7,21.3,13.9]`, "LPA": `[5.2,11.3,9.6]`, "RPA": `[20.2,11.3,9.1]`}.                                       |
| AnatomicalLandmarkCoordinateSystem            | OPTIONAL. Defines the coordinate system for the anatomical landmarks. See [Appendix VIII](../99-appendices/08-coordinate-systems.md): preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in `AnatomicalLandmarkCoordinateSystemDescription`. |
| AnatomicalLandmarkCoordinateUnits             | OPTIONAL. Units of the coordinates of `AnatomicalLandmarkCoordinateSystem`. MUST be `m`, `cm`, or `mm`.                                                                                                                                                                                  |
| AnatomicalLandmarkCoordinateSystemDescription | OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail.                                                                                                                                                                     |

It is also RECOMMENDED that the MRI voxel coordinates of the actual anatomical
landmarks for co-registration of MEG with structural MRI are stored in the
`AnatomicalLandmarkCoordinates` field in the JSON sidecar of the corresponding
T1w MRI anatomical data of the subject seen in the MEG session (see
[here](01-magnetic-resonance-imaging-data.md#anatomy-imaging-data) ) - for
example: `sub-01/ses-mri/anat/sub-01_ses-mri_acq-mprage_T1w.json`

In principle, these locations are those of absolute anatomical markers. However,
the marking of NAS, LPA and RPA is more ambiguous than that of e.g., AC and PC.
This may result in some variability in their 3-D digitization from session to
session, even for the same participant. The solution would be to use only one
T1w file and populate the `AnatomicalLandmarkCoordinates` field with
session-specific labels e.g., "NAS-session1": `[127,213,139]`,"NAS-session2":
`[123,220,142]`, etc.

Fiducials information:

| Field name           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FiducialsDescription | OPTIONAL. A freeform text field documenting the anatomical landmarks that were used and how the head localization coils were placed relative to these. This field can describe, for instance, whether the true anatomical locations of the left and right pre-auricular points were used and digitized, or rather whether they were defined as the intersection between the tragus and the helix (the entry of the ear canal), or any other anatomical description of selected points in the vicinity of the ears. |

For more information on the definition of anatomical landmarks, please visit:
[http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined)

For more information on typical coordinate systems for MEG-MRI coregistration:
[http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined),
or:
[http://neuroimage.usc.edu/brainstorm/CoordinateSystems](http://neuroimage.usc.edu/brainstorm/CoordinateSystems)

## Landmark photos (`*_photo.jpg`)

Photos of the anatomical landmarks and/or head localization coils
(`*_photo.jpg`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      meg/
        [sub-<label>[_ses-<label>][_acq-<label>]_photo.jpg]
```

Photos of the anatomical landmarks and/or head localization coils on the
subject’s head are RECOMMENDED. If the coils are not placed at the location of
actual anatomical landmarks, these latter may be marked with a piece of felt-tip
taped to the skin. Please note that the photos may need to be cropped or blurred
to conceal identifying features prior to sharing, depending on the terms of the
consent given by the participant.

The `acq` parameter can be used to indicate acquisition of different photos of
the same face (or other body part in different angles to show, for example, the
location of the nasion (NAS) as opposed to the right periauricular point (RPA)).

Example of the NAS fiducial placed between the eyebrows, rather than at the
actual anatomical nasion: `sub-0001_ses-001_acq-NAS_photo.jpg`

![placement of NAS fiducial](images/sub-0001_ses-001_acq-NAS_photo.jpg "placement of NAS fiducial")

## Head shape and electrode description (`*_headshape.<ext>`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      meg/
        [sub-<label>[_ses-<label>][_acq-<label>]_headshape.<manufacturer_specific_extension>]
```

This file is RECOMMENDED.

The 3-D locations of points that describe the head shape and/or EEG
electrode locations can be digitized and stored in separate files. The
`*_acq-<label>` can be used when more than one type of digitization in done for
a session, for example when the head points are in a separate file from the EEG
locations. These files are stored in the specific format of the 3-D digitizer’s
manufacturer (see [Appendix VI](../99-appendices/06-meg-file-formats.md)).

Example:

```Text
sub-control01
    ses-01
        sub-control01_ses-01_acq-HEAD_headshape.pos
        sub-control01_ses-01_acq-ECG_headshape.pos
```

Note that the `*_headshape` file(s) is shared by all the runs and tasks in a
session. If the subject needs to be taken out of the scanner and the head-shape
has to be updated, then for MEG it could be considered to be a new session.

## Empty-room MEG recordings

Empty-room MEG recordings capture the environmental and recording system's
noise.
In the context of BIDS it is RECOMMENDED to perform an empty-room recording for
each experimental session.
It is RECOMMENDED to store the empty-room recording inside a subject folder
named `sub-emptyroom`.
The label for the `task-<label>` entity in the empty-room recording SHOULD be
set to `noise`.
If a `session-<label>` entity is present, its label SHOULD be the date of the
empty-room recording in the format `YYYYMMDD`, i.e., `ses-YYYYMMDD`.
The `scans.tsv` file containing the date and time of the acquisition SHOULD
also be included.
The rationale is that this naming scheme will allow users to easily retrieve the
empty-room recording that best matches a particular experimental session, based
on date and time of the recording.
It should be possible to query empty-room recordings just like usual subject
recordings, hence all metadata sidecar files (such as the `channels.tsv`) file
SHOULD be present as well.

Example:

```Text
sub-control01/
sub-control02/
sub-emptyroom/
    ses-20170801/
        sub-emptyroom_ses-20170801_scans.tsv
        meg/
            sub-emptyroom_ses-20170801_task-noise_meg.ds
            sub-emptyroom_ses-20170801_task-noise_meg.json
            sub-emptyroom_ses-20170801_task-noise_channels.tsv
```
