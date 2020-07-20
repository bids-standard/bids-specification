# Positron Emission Tomography

Support for Positron Emission Tomography (PET) was developed as a [BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please cite the following paper when referring to this part of the standard in
context of the academic literature:

> Knudsen GM, Ganz M, Appelhoff S, Boellaard R, Bormans G, Carson RE, Catana C, Doudet D, Gee AD, Greve DN, Gunn RN, Halldin C, Herscovitch P, Huang H, Keller SH, Lammertsma AA, Lanzenberger R, Liow JS, Lohith TG, Lubberink M, Lyoo CH, Mann JJ, Matheson GJ, Nichols TE, Nørgaard M, Ogden T, Parsey R, Pike VW, Price J, Rizzo G, Rosa-Neto P, Schain M, Scott PJH, Searle G, Slifstein M, Suhara T, Talbot PS, Thomas A, Veronese M, Wong DF, Yaqub M, Zanderigo F, Zoghbi S, Innis RB. Guidelines for Content and Format of PET Brain Data in Publications and in Archives: A Consensus Paper. Journal of Cerebral Blood Flow and Metabolism, 2020 Aug;40(8):1576-1585. 
> doi: [10.1177/0271678X20905433](https://doi.org/10.1177/0271678X20905433)

The following example PET datasets have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

-   Single dynamic scan (pet, blood): [`pet_example_1`](https://doi.org/10.17605/OSF.IO/CJ2DR)
-   Single dynamic scan (pet, mri): [`pet_example_2`](https://doi.org/10.5281/zenodo.1490922)


Further datasets are available from the [BIDS examples repository](https://github.com/bids-standard/bids-examples).

## Detailed file description

As specified above, this extension is relevant for PET imaging and its associated data, such as blood data. In addition, the extension is in accordance with the guidelines for reporting and sharing brain PET data (Knudsen et al. 2020, [1]). If you want to share structural magnetic resonance (MR) images with your PET data, please distribute them according to the original BIDS specification (https://bids-specification.readthedocs.io/en/stable). Please pay specific attention to the format the MR images are in, such as if they have been unwarped in order to correct for gradient non-linearities. There is a specific field in the MRI BIDS (https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html) called “NonlinearGradientCorrection” which indicates this. The reason for this is that the MRI needs to be corrected for nonlinear gradients in order to fit the accompanying PET scans for co-registration [1, 2]. In general, SI units must be used (we refer to https://bids-specification.readthedocs.io/en/stable/99-appendices/05-units.html) and we recommend to use the CMIXF style formatting for SI units e.g. "kBq/mL" rather than "kilobecquerel per ml". An overview of a common PET experiment (with blood data) can be seen in Figure 1, defined on a single time scale relative to a predefined “time zero” (which should be defined either to be scan start or injection time; please note an exception to this definition is possible if a pharmacological within-scan challenge is performed).


![Figure 1](images/PET_scan_overview.png "placement of NAS fiducial")

Figure 1: Overview of a common PET experiment, including blood measurements, and defined on a common time scale. Note, “time zero”can either be defined as time of injection or scan start, and all the PET and blood data should be decay-corrected to this time point. Furthermore, although in this example tracer injection coincides with scan start, this is not always the case and hence we allow for the flexibility of specifying either time of injection or scan start as “time zero”. 

## PET Imaging data

Template:

```Text
sub-<participant_label>/
      [ses-<session_label>/]
        pet/
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.nii[.gz]
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.json
```

PET data belongs in the /pet folder. PET imaging data SHOULD be stored in 4D (or 3D if only one volume was acquired) NifTI files with _pet suffix. Volumes should be stored in chronological order (the order they were acquired in).

Multiple sessions (visits) are encoded by adding an extra layer of directories and file names in the form of ses-<label>. Session labels can consist only of alphanumeric characters [a-zA-Z0-9] and should be consistent across subjects. If numbers are used in session labels we recommend using zero padding (for example ses-01, ses-11 instead of ses-1, ses-11). This makes results of alphabetical sorting more intuitive. The extra session layer (at least one /ses-<label> subfolder) should be added for all subjects if at least one subject in the dataset has more than one session. Skipping the session layer for only some subjects in the dataset is not allowed. If a /ses-<label> subfolder is included as part of the directory hierarchy, then the same ses-<label> tag must also be included as part of the file names themselves. In general, we assume that a new session wrt PET starts with either a new injection (probably most common case) or with the subject being taken out of the scanner (same injection, but subject leaves the scanner and returns). However, for example, if a subject has to leave the scanner room and then be re-positioned on the scanner bed e.g. to use the bathroom, the set of PET acquisitions will still be considered as a session and match sessions acquired in other subjects. Similarly, in situations where different data types are obtained over several visits (for example FDG PET on one day followed by amyloid PET a couple days after) those can be grouped in one session. Please see the difference with the run-<label> below.

With respect to the task-<label>, data is arranged in a similar way as task-based and resting state BOLD fMRI data. In case of studies using combined PET/fMRI, subject-specific tasks may be carried out during the acquisition within the same session. Therefore, it is possible to specify task-<label> in accordance with the fMRI data. For more information please see https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#task-including-resting-state-imaging-data. 

In case of studies with multiple acquisitions per subject using different tracers, the acq-<label> must be used to distinguish between different tracers. Please keep in mind that the label used is arbitrary and each file requires a separate JSON sidecar with details of the tracer used (see below). Examples are e.g. acq-18FFDG for fludeoxyglucose, acq-11CPIB for Pittsburgh compound B, etc.

The reconstruction key (rec-<label>) has four reserved values: acdyn, for reconstructions with attenuation correction of dynamic data; acstat, for reconstructions with attenuation correction of static data; nacdyn, for reconstructions without attenuation correction of dynamic data; and nacstat, for reconstructions without attenuation correction of static data. Further details regarding reconstruction are in the _pet.json file. In case of multiple reconstructions of the data with the same type, we allow for using a number after the <label> in order to distinguish, e.g. rec-acdyn1 and rec-acdyn2. 

The run entity is used if one scan type/contrast is repeated multiple times within the same scan session/visit. If several scans of the same modality are acquired they MUST be indexed with a key-value pair: _run-1, _run-2, _run-3 etc. (only integers are allowed as run labels). When there is only one scan of a given type the run key MAY be omitted. An example of this would be two consecutive scans performed within the same session, e.g. two short FDG scans right after each other. It is our assumption that the run-<label> is used in PET for the cases where the subject does not leave the scanner. Otherwise, we refer to the ses-<label> definition.

In addition to the imaging data a _pet.json sidecar file needs to be provided. The included metadata are divided into sections described below.


### Sidecar JSON (`*_pet.json`)

Generic fields MUST be present:

| Field name | Definition                                                                                                                                                                                                                                                                                                                              |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TaskName   | REQUIRED. Name of the task (for resting state use the `rest` prefix). No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric (`[a-zA-Z0-9]`) characters. For example TaskName `faces n-back` will correspond to task label `facesnback`. |

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

| Field name             | Definition                                                                                                                                                                                                                                                                        |
| --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| InstitutionName        | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                        |
| InstitutionAddress     | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                     |
| Manufacturer           | RECOMMENDED. Manufacturer of the EEG system (e.g., `Biosemi`, `Brain Products`, `Neuroscan`).                                                                                                                                                                                     |
| ManufacturersModelName | RECOMMENDED. Manufacturer's designation of the EEG system model (e.g., `BrainAmp DC`).                                                                                                                                                                                            |
| SoftwareVersions       | RECOMMENDED. Manufacturer's designation of the acquisition software.                                                                                                                                                                                                              |
| TaskDescription        | RECOMMENDED. Description of the task.                                                                                                                                                                                                                                             |
| Instructions           | RECOMMENDED. Text of the instructions given to participants before the scan. This is not only important for behavioral or cognitive tasks but also in resting state paradigms (e.g., to distinguish between eyes open and eyes closed).                                           |
| CogAtlasID             | RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) term that describes the task (e.g., Resting State with eyes closed "[http://www.cognitiveatlas.org/task/id/trm_54e69c642d89b](http://www.cognitiveatlas.org/task/id/trm_54e69c642d89b)"). |
| CogPOID                | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task (e.g., Rest "[http://wiki.cogpo.org/index.php?title=Rest](http://wiki.cogpo.org/index.php?title=Rest)") .                                                                       |
| DeviceSerialNumber     | RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset.                                                     |

Specific EEG fields MUST be present:

| Field name         | Definition                                                                                                                                                                                                                                                                                                                                                                                       |
| ---------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EEGReference       | REQUIRED. General description of the reference scheme used and (when applicable) of location of the reference electrode in the raw recordings (e.g., "left mastoid", "Cz", "CMS"). If different channels have a different reference, this field should have a general description and the channel specific reference should be defined in the \_channels.tsv file.                               |
| SamplingFrequency  | REQUIRED. Sampling frequency (in Hz) of all the data in the recording, regardless of their type (e.g., 2400).                                                                                                                                                                                                                                                                                    |
| PowerLineFrequency | REQUIRED. Frequency (in Hz) of the power grid at the geographical location of the EEG instrument (i.e., 50 or 60).                                                                                                                                                                                                                                                                               |
| SoftwareFilters    | REQUIRED. A [JSON object](https://www.w3schools.com/js/js_json_objects.asp) of temporal software filters applied, or `"n/a"` if the data is not available. Each key:value pair in the JSON object is a name of the filter and an object in which its parameters are defined as key:value pairs. E.g., `{"Anti-aliasing filter": {"half-amplitude cutoff (Hz)": 500, "Roll-off": "6dB/Octave"}}`. |

SHOULD be present:

| Field name                 | Definition                                                                                                                                                                                                                                                                                                                                                                                          |
|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CapManufacturer            | RECOMMENDED. Name of the cap manufacturer (e.g., "EasyCap").                                                                                                                                                                                                                                                                                                                                        |
| CapManufacturersModelName  | RECOMMENDED. Manufacturer's designation of the EEG cap model (e.g., "actiCAP 64 Ch Standard-2").                                                                                                                                                                                                                                                                                                    |
| EEGChannelCount            | RECOMMENDED. Number of EEG channels included in the recording (e.g., 128).                                                                                                                                                                                                                                                                                                                          |
| ECGChannelCount            | RECOMMENDED. Number of ECG channels.                                                                                                                                                                                                                                                                                                                                                                |
| EMGChannelCount            | RECOMMENDED. Number of EMG channels.                                                                                                                                                                                                                                                                                                                                                                |
| EOGChannelCount            | RECOMMENDED. Number of EOG channels.                                                                                                                                                                                                                                                                                                                                                                |
| MiscChannelCount           | RECOMMENDED. Number of miscellaneous analog channels for auxiliary signals.                                                                                                                                                                                                                                                                                                                         |
| TriggerChannelCount        | RECOMMENDED. Number of channels for digital (TTL bit level) trigger.                                                                                                                                                                                                                                                                                                                                |
| RecordingDuration          | RECOMMENDED. Length of the recording in seconds (e.g., 3600).                                                                                                                                                                                                                                                                                                                                       |
| RecordingType              | RECOMMENDED. Defines whether the recording is `continuous`, `discontinuous`  or `epoched`.                                                                                                                                                                                                                                                                                                          |
| EpochLength                | RECOMMENDED. Duration of individual epochs in seconds (e.g., 1) in case of epoched data.                                                                                                                                                                                                                                                                                                            |
| EEGGround                  | RECOMMENDED. Description of the location of the ground electrode (e.g., "placed on right mastoid (M2)").                                                                                                                                                                                                                                                                                            |
| HeadCircumference          | RECOMMENDED. Circumference of the participants head, expressed in cm (e.g., 58).                                                                                                                                                                                                                                                                                                                    |
| EEGPlacementScheme         | RECOMMENDED. Placement scheme of EEG electrodes. Either the name of a standardized placement system (e.g., "10-20") or a list of standardized electrode names (e.g., `["Cz", "Pz"]`).                                                                                                                                                                                                               |
| HardwareFilters            | RECOMMENDED. A [JSON object](https://www.w3schools.com/js/js_json_objects.asp) of temporal hardware filters applied, or `"n/a"` if the data is not available. Each key:value pair in the JSON object is a name of the filter and an object in which its parameters are defined as key:value pairs. E.g., `{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dB/Octave"}}` |
| SubjectArtefactDescription | RECOMMENDED. Free-form description of the observed subject artifact and its possible cause (e.g., "Vagus Nerve Stimulator", "non-removable implant"). If this field is set to `n/a`, it will be interpreted as absence of major source of artifacts except cardiac and blinks.                                                                                                                      |

Example:

```JSON
{       
	"Modality": "PET",
	"Manufacturer": "Siemens",
	"ManufacturersModelName": "High-Resolution Research Tomograph (HRRT, CTI/Siemens)",
	"BodyPart": "Brain",
	"BodyWeight": 21,
	"BodyWeightUnit": "kg",
	"unit": "Bq/ml", 
	"TracerName": "CIMBI-36",
	"TracerRadionuclide": "C11",
	"TracerMolecularWeight": 380.28,
	"TracerMolecularWeightUnit": "g/mol",
	"TracerInjectionType": "bolus",
	"InjectedRadioactivity": 573,
	"InjectedRadioActivityUnit": "MBq",
	"InjectedMass": 0.62,
	"InjectedMassUnit": "ug",
	"SpecificRadioactivity": 353.51,
	"SpecificRadioactivityUnit": "GBq/umol",
	"ModeOfAdministration": "bolus",
	"MolarActivity": 1.62,
	"MolarActivityUnit": "nmol",
	"MolarActivityMeasTime": "12:59:00",
	"TimeZero": "13:04:42",
	"ScanStart": 0,
	"InjectionStart": 0,
	"FrameTimesStart": [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 240, 300, 360, 420, 480, 540, 660, 780, 900, 1020, 1140, 1260, 1380, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100, 5400, 5700, 6000, 6300, 6600, 6900],
	"FrameDuration": [10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 60, 60, 60, 60, 60, 60, 120, 120, 120, 120, 120, 120, 120, 120, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
	"AcquisitionMode": "list mode",
	"ImageDecayCorrected": "true",
	"ImageDecayCorrectionTime": 0,
	"ReconMatrixSize": [256,256,207,45],
	"ImageVoxelSize": [1.2188,1.2188,1.2188],
	"ReconMethodName": "3D-OSEM-PSF",
	"ReconMethodParameterLabels": ["subsets","iterations"],
	"ReconMethodParameterUnit": ["none","none"],
	"ReconMethodParameterValues": [16,10],
	"ReconFilterType": "none",
	"AttenuationCorrection": "[137Cs]transmission scan-based",
	"PlasmaAvail": "false",
	"MetaboliteAvail": "false",
	"ContinuousBloodAvail": "false",
	"DiscreteBloodAvail: “false”
}
```

Note that the date and time information SHOULD be stored in the Study key file
([`scans.tsv`](../03-modality-agnostic-files.md#scans-file)). As it is
indicated there, date time information MUST be expressed in the following
format `YYYY-MM-DDThh:mm:ss`
([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For
example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending
on local REB/IRB ethics board policy.

## Blood data (`*_blood.tsv`)

This section includes all data needed to perform blood analysis for PET data. The section may be omitted if blood measurements of radioactivity were not made. It contains the values and information regarding plasma samples, discrete blood samples, continuous blood samples from an autosampler, and metabolite fractions. All these measurements should be defined according to a single time-scale in relation to time zero defined by the PET data (Figure 1). Additionally, if blood and metabolite measurements were made one should always report radioactivity in plasma and corresponding parent fraction measurements, including fractions of radiometabolites. All definitions used below are in accordance with Innis et al. 2007 [3]. All method specific information related to the measurements can be stated in the field “description”. 

Template:

```Text
sub-<participant_label>/
      [ses-<session_label>/]
        pet/
          sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.tsv
          sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.json
```

Blood data belongs in the /pet folder along with the corresponding PET data. However, the blood data also follows the inheritance principle (https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#the-inheritance-principle) and may be moved to an upper level folder if it does not change e.g. with multiple reconstructions. The blood data is most often recorded using an autosampler for continuous blood samples, or manually for discrete blood samples. Therefore, the recording key (recording-<label>) has two reserved values: continuous, for continuous whole blood data measurements (2.2.4); and discrete, for discrete blood data, including whole blood (2.2.4), plasma (2.2.2), parent fraction and metabolite fractions (2.2.3). Blood data will be stored in tabular *.tsv files with a _blood suffix (https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#tabular-files). 
The first column in the *.tsv file should be a time column (2.2.1), defined in relation to time zero defined by the _pet.json file. All other information relevant to the blood measurements are recommended, and can be added as an additional column. It is expected that all values are (if relevant) decay corrected to time zero. 

This file is RECOMMENDED as it provides easily searchable information across
BIDS datasets for e.g., general curation, response to queries or batch
analysis.
The required columns are channel `name`, `type` and `units` in this specific
order.
To avoid confusion, the channels SHOULD be listed in the order they
appear in the EEG data file.
Any number of additional columns may be added to provide additional information
about the channels.
Note that electrode positions SHOULD NOT be added to this file, but to [`*_electrodes.tsv`](./03-electroencephalography.md#electrodes-description-_electrodestsv).

The columns of the Channels description table stored in `*_channels.tsv` are:

MUST be present:

| Column name | Definition                                                                                                                                                                       |
| ----------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name        | REQUIRED. Channel name (e.g., FC1, Cz)                                                                                                                                           |
| type        | REQUIRED. Type of channel; MUST use the channel types listed below.                                                                                                              |
| units       | REQUIRED. Physical unit of the value represented in this channel, e.g., `V` for Volt, or `fT/cm` for femto Tesla per centimeter (see [Units](../02-common-principles.md#units)). |

SHOULD be present:

| Column name        | Definition                                                                                                                                                                                                                                                                    |
| -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| description        | OPTIONAL. Free-form text description of the channel, or other information of interest. See examples below.                                                                                                                                                                    |
| sampling_frequency | OPTIONAL. Sampling rate of the channel in Hz.                                                                                                                                                                                                                                 |
| reference          | OPTIONAL. Name of the reference electrode(s) (not needed when it is common to all channels, in that case it can be specified in `*_eeg.json` as `EEGReference`).                                                                                                              |
| low_cutoff         | OPTIONAL. Frequencies used for the high-pass filter applied to the channel in Hz. If no high-pass filter applied, use `n/a`.                                                                                                                                                  |
| high_cutoff        | OPTIONAL. Frequencies used for the low-pass filter applied to the channel in Hz. If no low-pass filter applied, use `n/a`. Note that hardware anti-aliasing in A/D conversion of all EEG electronics applies a low-pass filter; specify its frequency here if applicable.     |
| notch              | OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use `n/a`.                                                                                                                                                         |
| status             | OPTIONAL. Data quality observed on the channel `(good/bad)`. A channel is considered `bad` if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in `[status_description]`.                                                     |
| status_description | OPTIONAL. Free-form text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in `[status]`.                                                                                                       |

Restricted keyword list for field `type` in alphabetic order (shared with the
MEG and iEEG modality; however, only the types that are common in EEG data are listed here):

| Keyword  | Description                                                  |
| -----------------| -------------------------------------------------------------- |
| AUDIO    | Audio signal                                                 |
| EEG      | Electroencephalogram channel                                 |
| EOG      | Generic electrooculogram (eye), different from HEOG and VEOG |
| ECG      | Electrocardiogram (heart)                                    |
| EMG      | Electromyogram (muscle)                                      |
| EYEGAZE  | Eye tracker gaze                                             |
| GSR      | Galvanic skin response                                       |
| HEOG     | Horizontal EOG (eye)                                         |
| MISC     | Miscellaneous                                                |
| PUPIL    | Eye tracker pupil diameter                                   |
| REF      | Reference channel                                            |
| RESP     | Respiration                                                  |
| SYSCLOCK | System time showing elapsed time since trial started         |
| TEMP     | Temperature                                                  |
| TRIG     | System triggers                                              |
| VEOG     | Vertical EOG (eye)                                           |

Example of free-form text for field `description`

-   n/a, stimulus, response, skin conductance, battery status

Example:

```Text
name     type   units   description                     status  status_description
VEOG     VEOG   uV      n/a                             good    n/a
FDI      EMG    uV      left first dorsal interosseous  good    n/a
Cz       EEG    uV      n/a                             bad     high frequency noise
UADC001  MISC   n/a     envelope of audio signal        good    n/a
```

## Electrodes description (`*_electrodes.tsv`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        [sub-<label>[_ses-<label>][_acq-<label>][_run-<index>]_electrodes.tsv]
```

File that gives the location of EEG electrodes. Note that coordinates are
expected in cartesian coordinates according to the `EEGCoordinateSystem` and
`EEGCoordinateSystemUnits` fields in `*_coordsystem.json`. **If an
`*_electrodes.tsv` file is specified, a [`*_coordsystem.json`](#coordinate-system-json-_coordsystemjson)
file MUST be specified as well**. The order of the required columns in the
`*_electrodes.tsv` file MUST be as listed below.

MUST be present:

| Column name | Definition                                   |
| --------------| ------------------------------------------------- |
| name        | REQUIRED. Name of the electrode              |
| x           | REQUIRED. Recorded position along the x-axis |
| y           | REQUIRED. Recorded position along the y-axis |
| z           | REQUIRED. Recorded position along the z-axis |

SHOULD be present:

| Column name | Definition                                                                  |
| ------------------------------| ------------------------------------------------------------------------------- |
| type        | RECOMMENDED. Type of the electrode (e.g., cup, ring, clip-on, wire, needle) |
| material    | RECOMMENDED. Material of the electrode  (e.g., Tin, Ag/AgCl, Gold)          |
| impedance   | RECOMMENDED. Impedance of the electrode, units MUST be in `kOhm`.           |

Example:

```Text
name  x         y        z         type      material
A1    -0.0707   0.0000   -0.0707   clip-on   Ag/AgCl
F3    -0.0567   0.0677   0.0469    cup       Ag/AgCl
Fz    0.0000    0.0714   0.0699    cup       Ag/AgCl
REF   -0.0742   -0.0200  -0.0100   cup       Ag/AgCl
GND   0.0742    -0.0200  -0.0100   cup       Ag/AgCl
```

The `acq` parameter can be used to indicate acquisition of the same data. For
example, this could be the recording of electrode positions with a different
electrode position recording device, or repeated digitization before and after
the recording.

## Coordinate System JSON (`*_coordsystem.json`)

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        [sub-<label>[_ses-<label>][_acq-<label>]_coordsystem.json]
```

A `*_coordsystem.json` file is used to specify the fiducials, the location of
anatomical landmarks, and the coordinate system and units in which the position
of electrodes and landmarks is expressed. **The `*_coordsystem.json` is
REQUIRED if the optional `*_electrodes.tsv` is specified**. If a corresponding
anatomical MRI is available, the locations of landmarks and fiducials according
to that scan should also be stored in the [`*_T1w.json`](./01-magnetic-resonance-imaging-data.md)
file which goes alongside the MRI data.

For disambiguation, we employ the following definitions for fiducials and
anatomical landmarks respectively:

-   Fiducials = objects with a well defined location used to facilitate the
    localization of electrodes and co-registration with other geometric data
    such as the participant's own T1 weighted magnetic resonance head image, a
    T1 weighted template head image, or a spherical head model. Commonly used
    fiducials are vitamin-E pills, which show clearly in an MRI, or reflective
    spheres that are localized with an infrared optical tracking system.

-   Anatomical landmarks = locations on a research subject such as the nasion,
    which is the intersection of the frontal bone and two nasal bones of the
    human skull.

Fiducials are typically used in conjunction with anatomical landmarks. An
example would be the placement of vitamin-E pills on top of anatomical
landmarks, or the placement of LEDs on the nasion and preauricular points to
triangulate the position of other LED-lit electrodes on a research subject's
head.

-   For more information on the definition of anatomical landmarks, please visit:
    [http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined)

-   For more information on coordinate systems for coregistration, please visit:
    [http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)

General fields:

| Keyword              | Description                                                                                |
| -----------------------------------| ------------------------------------------------------------------------------------------------- |
| IntendedFor          | OPTIONAL. Relative path to associate the electrodes, landmarks and fiducials to an MRI/CT. |

Fields relating to the EEG electrode positions:

| Keyword                        | Description                                                                                                                                                            |
| --------------------------------------------------------------------------------------------------------------------------------------------------| --------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EEGCoordinateSystem            | REQUIRED. Refers to the coordinate system in which the EEG electrode positions are to be interpreted (see [Appendix VIII](../99-appendices/08-coordinate-systems.md)). |
| EEGCoordinateUnits             | REQUIRED. Units in which the coordinates that are listed in the field `EEGCoordinateSystem` are represented. MUST be `m`, `cm`, or `mm`.                               |
| EEGCoordinateSystemDescription | RECOMMENDED. Free-form text description of the coordinate system. May also include a link to a documentation page or paper describing the system in greater detail.    |

Fields relating to the position of fiducials measured during an EEG session/run:

| Keyword                                       | Description                                                                                                                                                                                                                              |
| ---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FiducialsDescription                          | OPTIONAL. Free-form text description of how the fiducials such as vitamin-E capsules were placed relative to anatomical landmarks, and how the position of the fiducials were measured (e.g., both with Polhemus and with T1w MRI).      |
| FiducialsCoordinates                          | RECOMMENDED. Key:value pairs of the labels and 3-D digitized position of anatomical landmarks, interpreted following the `FiducialsCoordinateSystem` (e.g., `{"NAS": [12.7,21.3,13.9], "LPA": [5.2,11.3,9.6], "RPA": [20.2,11.3,9.1]}`). |
| FiducialsCoordinateSystem                     | RECOMMENDED. Refers to the coordinate space to which the landmarks positions are to be interpreted - preferably the same as the `EEGCoordinateSystem`.                                                                                   |
| FiducialsCoordinateUnits                      | RECOMMENDED. Units in which the coordinates that are  listed in the field `AnatomicalLandmarkCoordinateSystem` are represented. MUST be `m`, `cm`, or `mm`.                                                                              |
| FiducialsCoordinateSystemDescription          | RECOMMENDED. Free-form text description of the coordinate system. May also include a link to a documentation page or paper describing the system in greater detail.                                                                      |

Fields relating to the position of anatomical landmark measured during an EEG session/run:

| Keyword                                       | Description                                                                                                                                                                                                                                       |
| ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------| ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AnatomicalLandmarkCoordinates                 | RECOMMENDED. Key:value pairs of the labels and 3-D digitized position of anatomical landmarks, interpreted following the `AnatomicalLandmarkCoordinateSystem` (e.g., `{"NAS": [12.7,21.3,13.9], "LPA": [5.2,11.3,9.6], "RPA": [20.2,11.3,9.1]}`). |
| AnatomicalLandmarkCoordinateSystem            | RECOMMENDED. Refers to the coordinate space to which the landmarks positions are to be interpreted - preferably the same as the `EEGCoordinateSystem`.                                                                                            |
| AnatomicalLandmarkCoordinateUnits             | RECOMMENDED. Units in which the coordinates that are  listed in the field `AnatomicalLandmarkCoordinateSystem` are represented. MUST be `m`, `cm`, or `mm`.                                                                                       |
| AnatomicalLandmarkCoordinateSystemDescription | RECOMMENDED. Free-form text description of the coordinate system. May also include a link to a documentation page or paper describing the system in greater detail.                                                                               |

If the position of anatomical landmarks is measured using the same system or
device used to measure electrode positions, and if thereby the anatomical
landmarks are expressed in the same coordinates, the coordinates of the
anatomical landmarks can be specified in `electrodes.tsv`. The same applies to
the coordinates of the fiducials.

Anatomical landmarks or fiducials measured on an anatomical MRI  that match the
landmarks or fiducials during an EEG session/run, must be stored separately in
the corresponding `*_T1w.json` or `*_T2w.json` file and should be expressed in
voxels (starting from `[0, 0, 0]`).

Example:

```JSON
{
  "IntendedFor":"/sub-01/ses-01/anat/sub-01_T1w.nii",
  "EEGCoordinateSystem":"Other",
  "EEGCoordinateUnits":"mm",
  "EEGCoordinateSystemDescription":"RAS orientation: Origin halfway between LPA and RPA, positive x-axis towards RPA, positive y-axis orthogonal to x-axis through Nasion,  z-axis orthogonal to xy-plane, pointing in superior direction.",
  "FiducialsDescription":"Electrodes and fiducials were digitized with Polhemus, fiducials were recorded as the centre of vitamin E capsules sticked on the left/right pre-auricular and on the nasion, these are also visible on the T1w MRI"
}
```

## Landmark photos (`*_photo.jpg`)

Photos of the anatomical landmarks and/or fiducials.

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        [sub-<label>[_ses-<label>][_acq-<label>]_photo.jpg]
```

Photos of the anatomical landmarks and/or fiducials are OPTIONAL.
Please note that the photos may need to be cropped or blurred to conceal
identifying features prior to sharing, depending on the terms of the consent
given by the participant.

The `acq` parameter can be used to indicate acquisition of different photos of
the same face (or other body part in different angles to show, for example, the
location of the nasion (NAS) as opposed to the right periauricular point (RPA).
