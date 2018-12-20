# Electroencephalography (EEG)

Support for EEG was developed as a BIDS Extension Proposal. Please cite the
following paper when referring to this part of the standard in context of the
academic literature:

> Pernet, C. R., Appelhoff, S., Flandin, G., Phillips, C., Delorme, A., &
> Oostenveld, R. (2018, December 6). BIDS-EEG: an extension to the Brain
> Imaging Data Structure (BIDS) Specification for electroencephalography.
> [https://doi.org/10.31234/osf.io/63a4y](https://doi.org/10.31234/osf.io/63a4y)

## EEG recording data

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_eeg.<manufacturer_specific_extension>
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_eeg.json

```

While there are many file formats to store EEG data, there are two officially
supported data formats in EEG-BIDS: The [European data format](https://www.edfplus.info/)
(`.edf`), and the [BrainVision data format](https://www.brainproducts.com/productdetails.php?id=21&tab=5)
(`.vhdr`, `.vmrk`, `.eeg`) by Brain Products GmbH. There are also two
*unofficial* data formats that are currently accepted: The format used by the
MATLAB toolbox [EEGLAB](https://sccn.ucsd.edu/eeglab) (`.set` and `.fdt` files)
and the [Biosemi](https://www.biosemi.com/) data format (`.bdf`). The original
data format, if different from the supported formats, can be stored in the
`/sourcedata` directory.

The original data format is especially valuable in case conversion elicits the
loss of crucial metadata specific to manufacturers and specific EEG systems. We
also encourage users to provide additional meta information extracted from the
manufacturer specific data files in the sidecar JSON file. Other relevant files
MAY be included alongside the EEG data.

Note that for proper documentation of EEG recording metadata it is important to
understand the difference between electrode and channel: An EEG electrode is
attached to the skin, whereas a channel is the combination of the analog
differential amplifier and analog-to-digital converter that result in a
potential (voltage) difference that is stored in the EEG dataset. We employ
the following short definitions:

-   Electrode = A single point of contact between the acquisition system and
    the recording site (e.g., scalp, neural tissue, ...). Multiple electrodes
    can be organized as caps (for EEG), arrays, grids, leads, strips, probes,
    shafts, etc.

-   Channel = A single analogue-digital-converter in the recording system that
    regularly samples the value of a transducer, which results in a signal
    being represented as a time series in the data. This can be connected to
    two electrodes (to measure the potential difference between them), a
    magnetic field or magnetic gradient sensor,  temperature sensor,
    accelerometer, etc.

Although the "reference" and "ground" are often referred to as channels, they
are in most common EEG systems not amplified and recorded by themselves, and
therefore should not be represented as channels but as electrodes. The type of
referencing and optionally the location of the reference electrode and the
location of the ground electrode MAY be specified.

### Sidecar JSON document (`*_eeg.json`)

Generic fields MUST be present:

| Field name | Definition                                                                                                                                                                                                                  |
| :--------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TaskName   | REQUIRED. Name of the task (for resting state use the `rest` prefix). Different Tasks SHOULD NOT have the same name. The Task label is derived from this field by removing all non alphanumeric (`[a-zA-Z0-9]`) characters. |

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad-hoc wording.

| Field name             | Definition                                                                                                                                                                                                                                                                       |
| :--------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| InstitutionName        | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                       |
| InstitutionAddress     | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                    |
| Manufacturer           | RECOMMENDED. Manufacturer of the EEG system (e.g., `Biosemi`, `Brain Products`, `Other`).                                                                                                                                                                                        |
| ManufacturersModelName | RECOMMENDED. Manufacturer’s designation of the EEG system model (e.g., `BrainAmp DC`).                                                                                                                                                                                           |
| SoftwareVersions       | RECOMMENDED. Manufacturer’s designation of the acquisition software.                                                                                                                                                                                                             |
| TaskDescription        | RECOMMENDED. Description of the task.                                                                                                                                                                                                                                            |
| Instructions           | RECOMMENDED. Text of the instructions given to participants before the scan. This is not only important for behavioral or cognitive tasks but also in resting state paradigms (e.g., to distinguish between eyes open and eyes closed).                                          |
| CogAtlasID             | RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) term that describes the task (e.g., Resting State with eyes closed "[http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b](http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b)") |
| CogPOID                | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task (e.g., Rest "[http://wiki.cogpo.org/index.php?title=Rest](http://wiki.cogpo.org/index.php?title=Rest)")                                                                        |
| DeviceSerialNumber     | RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset.                                                    |

Specific EEG fields MUST be present:

| Field name          | Definition                                                                                                                                                                                                                                                                            |
| :------------------ | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SamplingFrequency   | REQUIRED. Sampling frequency (in Hz) of all the data in the recording, regardless of their type (e.g., 2400)                                                                                                                                                                          |
| PowerLineFrequency  | REQUIRED. Frequency (in Hz) of the power grid at the geographical location of the EEG instrument (i.e., 50 or 60)                                                                                                                                                                     |
| EEGChannelCount     | REQUIRED. Number of EEG channels included in the recording (e.g., 128).                                                                                                                                                                                                               |
| SoftwareFilters     | REQUIRED. List of temporal software filters applied. Ideally key:value pairs of pre-applied software filters and their parameter values: e.g., `{"Anti-aliasing filter": {"half-amplitude cutoff (Hz)": 500, "Roll-off": "6dB/Octave"}}`. Write `n/a` if no software filters applied. |

SHOULD be present:

| Field name                 | Definition                                                                                                                                                                                                                                                                                                     |
|----------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CapManufacturer            | RECOMMENDED. Name of the cap manufacturer (e.g., "EasyCap")                                                                                                                                                                                                                                                    |
| CapManufacturersModelName  | RECOMMENDED. Manufacturer's designation of the EEG cap model (e.g., "actiCAP 64 Ch Standard-2")                                                                                                                                                                                                                |
| ECGChannelCount            | RECOMMENDED. Number of ECG channels                                                                                                                                                                                                                                                                            |
| EMGChannelCount            | RECOMMENDED. Number of EMG channels                                                                                                                                                                                                                                                                            |
| EOGChannelCount            | RECOMMENDED. Number of EOG channels                                                                                                                                                                                                                                                                            |
| MiscChannelCount           | RECOMMENDED. Number of miscellaneous analog channels for auxiliary signals                                                                                                                                                                                                                                     |
| TriggerChannelCount        | RECOMMENDED. Number of channels for digital (TTL bit level) trigger                                                                                                                                                                                                                                            |
| RecordingDuration          | RECOMMENDED. Length of the recording in seconds (e.g., 3600)                                                                                                                                                                                                                                                   |
| RecordingType              | RECOMMENDED. Defines whether the recording is `continuous` or `epoched`                                                                                                                                                                                                                                        |
| EpochLength                | RECOMMENDED. Duration of individual epochs in seconds (e.g., 1) in case of epoched data                                                                                                                                                                                                                        |
| HeadCircumference          | RECOMMENDED. Circumference of the participants head, expressed in cm (e.g., 58)                                                                                                                                                                                                                                |
| EEGPlacementScheme         | Placement scheme of EEG electrodes. Either the name of a standardised placement system (e.g., "10-20") or a list of standardised electrode names (e.g. `["Cz", "Pz"]`)                                                                                                                                         |
| EEGGround                  | RECOMMENDED. Description of the location of the ground electrode (e.g., "placed on right mastoid (M2)")                                                                                                                                                                                                        |
| HardwareFilters            | RECOMMENDED. List of temporal hardware filters applied. Ideally key:value pairs of pre-applied hardware filters and their parameter values: e.g., `{"HardwareFilters": {"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dB/Octave"}}}`. Write `n/a` if no hardware filters applied. |
| SubjectArtefactDescription | RECOMMENDED. Freeform description of the observed subject artefact and its possible cause (e.g. "Vagus Nerve Stimulator", "non-removable implant"). If this field is set to `n/a`, it will be interpreted as absence of major source of artifacts except cardiac and blinks.                                   |

Example:

```JSON
{
  "TaskName":"Seeing stuff",
  "TaskDescription":"Subjects see various images for which phase, amplitude spectrum, and color vary continuously",
  "Instructions":"Your task is to detect images when they appear for the 2nd time, only then press the response button with your right/left hand (counterbalanced across subjects)",
  "InstitutionName":"The world best university, 10 beachfront avenue, Papeete",
  "SamplingFrequency":2400,
  "Manufacturer":"Brain Products",
  "ManufacturersModelName":"BrainAmp DC",
  "CapManufacturer":"EasyCap",
  "CapManufacturersModelName":"M1-ext",
  "EEGChannelCount":87,
  "EOGChannelCount":2,
  "ECGChannelCount":1,
  "EMGChannelCount":0,
  "MiscChannelCount":0,
  "TriggerChannelCount":1,
  "PowerLineFrequency":50,
  "EEGPlacementScheme":"10 percent system",
  "EEGReference":"single electrode placed on FCz",
  "EEGGround":"placed on AFz",
  "HardwareFilters":{
    "ADC's decimation filter (hardware bandwidth limit)":{
      "-3dB cutoff point (Hz)":480,
      "Filter order sinc response":5
    }
  },
  "RecordingDuration":600,
  "RecordingType":"continuous"
}
```

Note that the date and time information SHOULD be stored in the Study key file
(`scans.tsv`), see [Scans.tsv](../03-modality-agnostic-files.md#scans-file). As
it is indicated there, date time information MUST be expressed in the following
format `YYYY-MM-DDThh:mm:ss`
([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For
example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending
on local REB/IRB ethics board policy.

## Channels description table (`*_channels.tsv`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        [sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_channels.tsv]
```

Although this information can often be extracted from the EEG recording,
listing it in a simple .tsv document makes it easy to browse or search. The
required columns are channel `name`, `type` and `units`. Channels should appear
in the table in the same order they do in the EEG data file. Any number of
additional columns may be provided to provide additional information about the
channels. Note that electrode positions should not be added to this file, but
to `*_electrodes.tsv`.


The columns of the Channels description table stored in `*_channels.tsv` are:

MUST be present:

| Field name | Definition                                                                                                                                             |
| :--------- | :----------------------------------------------------------------------------------------------------------------------------------------------------- |
| name       | REQUIRED. Channel name (e.g., FC1, Cz)                                                                                                                 |
| type       | REQUIRED. Type of channel; MUST use the channel types listed below.                                                                                    |
| units      | REQUIRED. Physical unit of the data values recorded by this channel in SI (see [Appendix V](../99-appendices/05-units.md): Units for allowed symbols). |

SHOULD be present:

| Field name         | Definition                                                                                                                                                                                                                                                                    |
| :----------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| description        | OPTIONAL. Brief free-text description of the channel, or other information of interest. See examples below.                                                                                                                                                                   |
| sampling_frequency | OPTIONAL. Sampling rate of the channel in Hz.                                                                                                                                                                                                                                 |
| reference          | OPTIONAL. Name of the reference electrode(s) (not needed when it is common to all channels, in that case it can be specified in `eeg.json` as `EEGReference`).                                                                                                                |
| low_cutoff         | OPTIONAL. Frequencies used for the high-pass filter applied to the channel in Hz. If no high-pass filter applied, use `n/a`.                                                                                                                                                  |
| high_cutoff        | OPTIONAL. Frequencies used for the low-pass filter applied to the channel in Hz. If no low-pass filter applied, use `n/a`. Note that hardware anti-aliasing in A/D conversion of all EEG electronics applies a low-pass filter; specify its frequency here if applicable.     |
| notch              | OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use `n/a`.                                                                                                                                                         |
| status             | OPTIONAL. Data quality observed on the channel `(good/bad)`. A channel is considered `bad` if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in `[status_description]`.                                                     |
| status_description | OPTIONAL. Freeform text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in `[status]`.                                       

Restricted keyword list for field `type` in alphabetic order (shared with the
MEG modality; however, MEG specific types are not listed here):

| Keyword  | Description                                                  |
|----------|--------------------------------------------------------------|
| AUDIO    | Audio signal                                                 |
| EEG      |  Electroencephalogram channel                                |
| EOG      | Generic electrooculogram (eye), different from HEOG and VEOG |
| ECG      | Electrocardiogram (heart)                                    |
| EMG      |  Electromyogram (muscle)                                     |
| EYEGAZE  | Eye tracker gaze                                             |
| GSR      | Galvanic skin resistance                                     |
| HEOG     |  Horizontal EOG (eye)                                        |
| MISC     | Miscellaneous                                                |
| PUPIL    | Eye tracker pupil diameter                                   |
| REF      | Reference channel                                            |
| RESP     | Respiration                                                  |
| SYSCLOCK | System time showing elapsed time since trial started         |
| TEMP     | Temperature                                                  |
| TRIG     |  System triggers                                             |
| VEOG     |  Vertical EOG (eye)                                          |

Example of free text for field `description`

-   n/a, stimulus, response, skin conductance, battery status

Example:

```Text
name	type	units	description	status	status_description
VEOG	VEOG	microV	n/a	good	n/a
FDI	EMG	microV	left first dorsal interosseous	good	n/a
Cz	EEG	microV	n/a	bad	high frequency noise
UADC001	MISC	n/a	enevelope of audio signal	good	n/a
```
