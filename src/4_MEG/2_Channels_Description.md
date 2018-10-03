### 8.4.2 Channels description table (`*_channels.tsv`)
Template:
```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_channels.tsv]
```

This file is RECOMMENDED as it provides easily searchable information across MEG-BIDS datasets for e.g., general curation, response to queries or batch analysis. To avoid confusion, the channels SHOULD be listed in the order they appear in the MEG data file. Missing values MUST be indicated with  `n/a`.

The columns of the Channels description table stored in `*_channels.tsv` are:

MUST be present:

| Field name | Definition                                                      |
|:-----------|:----------------------------------------------------------------|
| name       | REQUIRED. Channel name (e.g., MRT012, MEG023)                   |
| type       | REQUIRED. Type of channel; MUST use the channel types listed below. |
| units      | REQUIRED. Physical unit of the data values recorded by this channel in SI (see Appendix V: Units for allowed symbols). |

SHOULD be present:

| Field name         | Definition                                              |
|:-------------------|:--------------------------------------------------------|
| description        | OPTIONAL. Brief free-text description of the channel, or other information of interest. See examples below. |
| sampling_frequency | OPTIONAL. Sampling rate of the channel in Hz.           |
| low_cutoff         | OPTIONAL. Frequencies used for the high-pass filter applied to the channel in Hz. If no high-pass filter applied, use `n/a`. |
| high_cutoff        | OPTIONAL. Frequencies used for the low-pass filter applied to the channel in Hz. If no low-pass filter applied, use `n/a`. Note that hardware anti-aliasing in A/D conversion of all MEG/EEG electronics applies a low-pass filter; specify its frequency here if applicable. |
| notch              | OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use `n/a`. |
| software_filters   | OPTIONAL. List of temporal and/or spatial software filters applied (e.g. "SSS", ``"SpatialCompensation"``). Note that parameters should be defined in the general MEG sidecar .json file. Indicate `n/a` in the absence of software filters applied. |
| status             | OPTIONAL. Data quality observed on the channel ``(good/bad)``. A channel is considered `bad` if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in ``[status_description]``. |
| status_description | OPTIONAL. Freeform text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in ``[status]``. |


Example:

```
name type units description sampling_frequency ...
UDIO001 TRIG V analogue trigger 1200
MLC11 MEGGRADAXIAL T sensor 1st-order grad 1200
```

```
... low_cutoff high_cutoff notch software_filters status
0.1 300 0 n/a good
0 n/a 50 SSS bad
```


Restricted keyword list for field `type`

-   MEGMAG:               MEG magnetometer
-   MEGGRADAXIAL:         MEG axial gradiometer
-   MEGGRADPLANAR:        MEG planar gradiometer
-   MEGREFMAG:            MEG reference magnetometer
-   MEGREFGRADAXIAL:               MEG reference axial  gradiometer
-   MEGREFGRADPLANAR:               MEG reference planar gradiometer
-   MEGOTHER:             Any other type of MEG sensor
-   EEG:                  Electrode channel : electroencephalogram
-   ECOG:                 Electrode channel : electrocorticogram (intracranial)
-   SEEG:                 Electrode channel : stereo-electroencephalogram (intracranial)
-   DBS:                  Electrode channel : deep brain stimulation (intracranial)
-   VEOG:                 Vertical EOG (electrooculogram)
-   HEOG:                 Horizontal EOG
-   EOG:                  Generic EOG channel, if HEOG or VEOG information not available
-   ECG:                  ElectroCardioGram (heart)
-   EMG:                  ElectroMyoGram (muscle)
-   TRIG:                 System Triggers
-   AUDIO:                Audio signal
-   PD:                   Photodiode
-   EYEGAZE:              Eye Tracker gaze
-   PUPIL:                Eye Tracker pupil diameter
-   MISC:                 Miscellaneous
-   SYSCLOCK:             System time showing elapsed time since trial started
-   ADC:                  Analog to Digital input
-   DAC:                  Digital to Analog output
-   HLU:                  Measured position of head and head coils
-   FITERR:               Fit error signal from each head localization coil
-   OTHER:                Any other type of channel

Example of free text for field `description`

-   stimulus, response, vertical EOG, horizontal EOG, skin conductance, sats, intracranial, eyetracker

Example:

```
name type units description
VEOG VEOG V vertical EOG
FDI EMG V left first dorsal interosseous
UDIO001 TRIG V analog trigger signal
UADC001 AUDIO V envelope of audio signal presented to participant
```
