# Functional Near-Infrared Spectroscopy

Support for functional Near-Infrared Spectroscopy (fNIRS) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

## fNIRS recording data

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["nirs", "events"]) }}

Only the Shared Near Infrared Spectroscopy Format ([SNIRF](https://github.com/fNIRS/snirf))
file specification is supported in BIDS. The SNIRF
specification supports one or more fNIRS datasets to be stored in a single
`.snirf` file. However, to be BIDS compatible, each SNIRF file MUST contain
only a single run. A limited set of fields from the SNIRF specification are
replicated  in the BIDS specification. This redundancy allows the data to be
easily parsed by humans and machines that do not have a SNIRF reader at hand,
which improves findability and tooling development.

Raw fNIRS data in the native format, if different from SNIRF, can also
be stored in the [`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data)
along with code to convert the data to
SNIRF in the [`/code` directory](../02-common-principles.md#storage-of-derived-datasets).
The unprocessed raw data should be stored in
the manufacturer's format before any additional processing or conversion is applied.
Retaining the native file format is especially valuable in a case when conversion elicits the
loss of crucial metadata unique to specific manufacturers and fNIRS systems.
We also encourage users to provide additional meta information extracted from
the manufacturer-specific data files in the sidecar JSON file. This allows for
easy searching and indexing of key metadata elements without needing to parse
the various proprietary (typically binary) native data files. Other relevant
files should  be included alongside the fNIRS data.

### Terminology

For proper documentation of fNIRS recording metadata, it is important
to understand the difference between a Source, Detector, and Channel as these
are defined differently to other modalities, such as EEG. The following definitions
apply in this document:

-   Source - A light emitting device, sometimes called a transmitter.

-   Detector - A photoelectric transducer, sometimes called a receiver.

-   Optode - Refers to either a source or detector.

-   Channel - A paired coupling of a source and a detector with one specific wavelength of light.
    It is common for a single Source-Detector pair to result in two or more channels
    with different wavelengths.

### Sidecar JSON (`*_nirs.json`)

It is common within the fNIRS community for researchers to build their own caps
and optode holders to position their sources and detectors, or for optodes to
be directly attached to the scalp with adhesive. To facilitate description of
the wide variety of possible configurations, several fields are RECOMMENDED within
the `*_nirs.json` file.
To clarify the usage and interaction of these fields, the following examples are provided.
-   If a commercial cap such as EasyCap actiCAP 64 Ch Standard-2
was used, then the values `CapManufacturer = "EasyCap"`, `CapManufacturersModelName = "actiCAP
64 Ch Standard-2"` and `NIRSPlacementScheme = "n/a"` should be used.
-   If an EasyCap was used but with custom positions,
as may be done by cutting custom holes in the cap,
then the values `CapManufacturer = "EasyCap"`, `CapManufacturersModelName = "custom"` and
`NIRSPlacementScheme = "n/a"` should be used.
-   If a completely custom cap was knitted, then
`CapManufacturer = "custom"`, `CapManufacturersModelName = "custom"` and
`NIRSPlacementScheme = "n/a"`.
-   If no cap was used and optodes were taped to the scalp
at positions Cz, C1 and C2, then the values `CapManufacturer = "none"`, `CapManufacturersModelName
= "n/a"` and `NIRSPlacementScheme = "["Cz", "C1", "C2"]"` should be used.
In these cases additional information regarding channels and optodes SHOULD be placed in `*_channels.tsv` and `*_optodes.tsv` files.

Closely spaced or short-separation source-detector pairs are often included in fNIRS measurements to
obtain a measure of systemic, rather than neural, activity. These source-detector
pairs are referred to as *short channels*. There is variation in how manufacturers
implement these short channels, some use specialised sources or detectors,
and the placement mechanisms vary.
It is beyond the scope of the BIDS specification to define what constitutes a short channel,
and detailed characteristics of channels may be stored within the SNIRF file
(for example, in the `sourcePower` field).
However, to improve searchability and ease of access for users, it is useful to
know if short channels were included in the fNIRS measurements; this information
is stored in the field `ShortChannelCount`.
If the field `ShortChannelCount` is populated, then the optional column `short_channel`
may be used in `*_channels.tsv` to describe which channels were specified as short.

Generic fields that MUST be present:

{{ MACROS___make_metadata_table(
   {
      "TaskName": "REQUIRED",
   }
) }}

Generic fields which SHOULD be present: For consistency between studies and institutions,
we encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

{{ MACROS___make_metadata_table(
   {
      "InstitutionName": "RECOMMENDED",
      "InstitutionAddress": "RECOMMENDED",
      "Manufacturer": "RECOMMENDED",
      "ManufacturersModelName": "RECOMMENDED",
      "SoftwareVersions": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "Instructions": "RECOMMENDED",
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
      "RecordingDuration": "RECOMMENDED",
      "HeadCircumference": "RECOMMENDED",
      "HardwareFilters": "RECOMMENDED",
      "SubjectArtefactDescription": "RECOMMENDED",
   }
) }}

| **Key name**              | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                    |
| ------------------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| CapManufacturer           | RECOMMENDED           | [string][]    | Name of the cap manufacturer (for example, "Artinis") If a custom-made cap is used then the string “custom” should be used. If no cap was used, such as with optodes that are directly taped to the scalp, then the string “none” should be used and NIRSPlacementScheme field may be used to specify the optode placement scheme. |
| CapManufacturersModelName | RECOMMENDED           | [string][]    | Manufacturer's designation of the fNIRS cap model (for example, "Headband with print (S-M)"). If a cap from a standard manufacturer was modified, then the field should be set to “custom.” If no cap was used, then the CapManafacturer field should be “none” and this field should be “n/a.”                                    |

Specific fNIRS fields that MUST be present:

| **Key name**            | **Requirement level**                                | **Data type**     | **Description**                                                                                                                                                                                                                                                                                        |
| ----------------------- | ---------------------------------------------------- | ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| SamplingFrequency       | REQUIRED                                             | [number][] or n/a | Sampling frequency (in Hz) of all the data in the recording, regardless of their type (for example, 12).  If individual channels have different sampling rates, then the field here should be specified as “n/a” and the values  should be specified in the sampling_frequency column in channels.tsv. |
| NIRSChannelCount        | REQUIRED                                             | [number][]        | Number of fNIRS channels.                                                                                                                                                                                                                                                                              |
| NIRSSourceOptodeCount   | REQUIRED                                             | [number][]        | Number of fNIRS sources.                                                                                                                                                                                                                                                                               |
| NIRSDetectorOptodeCount | REQUIRED                                             | [number][]        | Number of fNIRS detectors.                                                                                                                                                                                                                                                                             |
| ACCELChannelCount       | RECOMMENDED but REQUIRED if any channel type is ACC  | [number][]        | Number of accelerometer channels.                                                                                                                                                                                                                                                                      |
| GYROChannelCount        | RECOMMENDED but REQUIRED if any channel type is GYRO | [number][]        | Number of gyrometer channels.                                                                                                                                                                                                                                                                          |
| MAGNChannelCount        | RECOMMENDED but REQUIRED if any channel type is MAGN | [number][]        | Number of magnetometer channels.                                                                                                                                                                                                                                                                       |

Specific fNIRS fields that SHOULD be present:

| **Key name**        | **Requirement level** | **Data type**         | **Description**                                                                                                                                                                                                                                                                                                                                                                        |
| ------------------- | --------------------- | --------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| SourceType          | RECOMMENDED           | [number][] or `mixed` | Type of source. Preferably a specific model/part number is supplied. This is a freeform description, but the following keywords are suggested: LED, LASER, VCSEL. If individual channels have different SourceTypes, then the field here should be specified as `mixed`  and this column should be included in `optodes.tsv`.                                                          |
| DetectorType        | RECOMMENDED           | [number][] or `mixed` | Type of detector. This is a free form description with the following suggested terms: SiPD, APD. Preferably a specific model/part number is supplied. If individual channels have different DetectorTypes, then the field here should be specified as `mixed`  and this column should be included in `optodes.tsv`.                                                                    |
| ShortChannelCount   | RECOMMENDED           | [number][]            | The number of short channels. 0 indicates no short channels.                                                                                                                                                                                                                                                                                                                           |
| NIRSPlacementScheme | RECOMMENDED           | [string][]            | Placement scheme of NIRS optodes. Either the name of a standardized placement system (for example, "10-20") or a list of standardized position names (for example, ["Cz", "Pz"]). This field should only be used if a cap was not used. If a standard cap was used, then it should be specified in CapManufacturer and CapManufacturersModelName and this field should be set to “n/a” |

Example:

```JSON
{
  "TaskName":"visual",
  "InstitutionName":"Macquarie University. Australian Hearing Hub",
  "InstitutionAddress":"6 University Ave, Macquarie University NSW 2109 Australia",
  "Manufacturer":"NIRx",
  "ManufacturersModelName":"NIRScout",
  "TaskDescription":"visual gratings and noise patterns",
  "Instructions":"look at the dot in the center of the screen and press the button when it changes color",
  "SamplingFrequency":3.7,
  "NIRSChannelCount":56,
  "NIRSSourceOptodeCount":16,
  "NIRSDetectorOptodeCount":16,
  "ACCELChannelCount":0,
  "SoftwareFilters":"n/a",
  "RecordingDuration":233.639,
  "DCOffsetCorrection":0,
  "HardwareFilters":{"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dBOctave"}},
  "CapManafacturer":"NIRx",
  "CapManufacturersModelName":"Headband with print (S-M)",
}
```

### Participant file

For fNIRS data, the modality agnostic participant.tsv and json files SHOULD contain
the `age` field, as this is required for calculation of age-specific pathlength factors.
If the dataset contains multiple groups, for example patients and controls, then
a column labeled `group` MAY be included (see [participants.tsv](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file)).

```text
participant_id	age	 sex	hand  group
sub-01       	34	 M	    n/a   patient
sub-02	        32	 F	    n/a   control
```

## Channels description (`*_channels.tsv`)

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["channels"]) }}

Channels are a pairing of source and detector optodes with a specific wavelength of light.
Unlike in other modalities, not all pairings of optodes correspond to meaningful data
and not all pairs have to be recorded or represented in the data.  Note that the source
and detector names used in the channel specifications are specified in the `*_optodes.tsv`
file below. The required columns in the `*_channels.tsv` file MUST be ordered as listed below.

The BIDS specification supports several types of fNIRS devices which output raw data in
different forms. The type of measurement is specified in the `type` column. For example,
when measurements are taken with a continuous wave (CW) device that saves the data
as optical density, the `type` should be `NIRSCWOPTICALDENSITY` and the `units` should be `unitless`,
this is equivalent to SNIRF data type dOD.

The following columns MUST be present:

| **Column name**       | **Requirement level**                                                    | **Data type**       | **Definition**                                                                                                                                                                                                                                                              |
| --------------------- | ------------------------------------------------------------------------ | ------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name                  | REQUIRED                                                                 | [string][]          | Name of the channel.                                                                                                                                                                                                                                                        |
| type                  | REQUIRED                                                                 | [string][]          | Type of measurement; MUST be a valid measurement type keyword. See table below.                                                                                                                                                                                             |
| source                | REQUIRED                                                                 | [string][] or `n/a` | Name of the source as specified in the `*_optodes.tsv` file. `n/a` for channels that do not contain fNIRS signals (for example, acceleration).                                                                                                                              |
| detector              | REQUIRED                                                                 | [string][] or `n/a` | Name of the detector as specified in the `*_optodes.tsv` file. `n/a` for channels that do not contain fNIRS signals (for example, acceleration).                                                                                                                            |
| wavelength_nominal    | REQUIRED                                                                 | [number][] or `n/a` | Specified wavelength of light in nm. `n/a` for channels that do not contain raw fNIRS signals (acceleration). This field is equivalent to `/nirs(i)/probe/wavelengths` in the SNIRF specification.                                                                          |
| units                 | REQUIRED                                                                 | [string][]          | Physical unit of the value represented in this channel, specified according to the SI unit symbol and possibly prefix symbol, or as a derived SI unit (for example, V, or unitless for changes in optical densities). For guidelines for Units and Prefixes see Appendix V. |
| sampling_frequency    | OPTIONAL but REQUIRED if `SamplingFrequency` is to `n/a` in `_nirs.json` | [number][]          | Sampling frequency of the channel in Hz.                                                                                                                                                                                                                                    |
| orientation_component | OPTIONAL but REQUIRED if type is ACCEL, GYRO or MAGN                     | [string][]          | Description of the orientation of the ACCEL, GYRO, MAGN type. Either x, y, or z.                                                                                                                                                                                            |

The following columns SHOULD be present:

| **Column name**            | **Requirement level** | **Data type** | **Definition**                                                                                                                                                                                                          |
| -------------------------- | --------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| wavelength_actual          | OPTIONAL              | [number][]    | Measured wavelength of light in nm. `n/a` for channels that do not contain raw NIRS signals (acceleration). This field is equivalent to `measurementList.wavelengthActual` in the SNIRF specification.                  |
| description                | OPTIONAL              | [string][]    | Free-form text description of the channel, or other information of interest.                                                                                                                                            |
| wavelength_emission_actual | OPTIONAL              | [number][]    | Measured emission wavelength of light in nm. `n/a` for channels that do not contain raw NIRS signals (acceleration). This field is equivalent to `measurementList.wavelengthEmissionActual` in the SNIRF specification. |
| short_channel              | OPTIONAL              | [boolean][]   | Is the channel designated as short. The total number of channels listed as short channels should be stored in `ShortChannelCount` in `*_fnirs.csv`.                                                                     |
| status                     | OPTIONAL              | [string][]    | Data quality observed on the channel (`good`, `bad`). A channel is considered `bad` if its data quality is compromised. Description of noise type SHOULD be provided in `status_description`.                           |
| status_description         | OPTIONAL              | [string][]    | Free-form text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in `status`.                                                             |

### Restricted keyword list for the channel types

All fNIRS channels types MUST correspond to a [valid SNIRF data type](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md#appendix).
Additional channels that are recorded simultaneously with the fNIRS
device and stored in the same data file should be included as well.
However, additional channels that are  simultaneously recorded with a different device
should be stored according to their appropriate modality specification.
For example, motion data that was simultaneously recorded with a different device should be specified
according to BEP029 and not according to the fNIRS data type.
Whereas, if the motion data was acquired in with the fNIRS device itself, it should be included here with the fNIRS data.
Any of the channel types defined in other BIDS specification can be used here as well such as ACCEL or MAGN.
As several of these data types are commonly acquired using fNIRS devices they are included as an example at the base of the table.
Note that upper-case is REQUIRED.

| **Keyword**                 | **Description**                                                                                                                                                              |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIRSCWAMPLITUDE             | Continuous wave amplitude measurements. Equivalent to dataType 001 in SNIRF.                                                                                                 |
| NIRSCWFLUORESCENSEAMPLITUDE | Continuous wave fluorescence amplitude measurements. Equivalent to dataType 051 in SNIRF.                                                                                    |
| NIRSCWOPTICALDENSITY        | Continuous wave change in optical density measurements. Equivalent to dataTypeLabel dOD in SNIRF.                                                                            |
| NIRSCWHBO                   | Continuous wave oxygenated hemoglobin (oxyhemoglobin) concentration measurements. Equivalent to dataTypeLabel HbO in SNIRF.                                                  |
| NIRSCWHBR                   | Continuous wave deoxygenated hemoglobin (deoxyhemoglobin) concentration measurements. Equivalent to dataTypeLabel HbR in SNIRF.                                              |
| NIRSCWMUA                   | Continuous wave optical absorption  measurements. Equivalent to dataTypeLabel mua in SNIRF.                                                                                  |
| ACCEL                       | Accelerometer channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `_*channels.tsv` file (x, y or z). |
| GYRO                        | Gyrometer channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `_*channels.tsv` file (x, y or z).     |
| MAGN                        | Magnetomenter channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `_*channels.tsv` file (x, y or z). |
| MISC                        | Miscellaneous                                                                                                                                                                |

Example:

```Text
Name         type                   source      detector      wavelength_nominal   units
S1-D1        NIRSCWAMPLITUDE        A1          Fz            760                  V
S1-D1        NIRSCWAMPLITUDE        A1          Fz            850                  V
S1-D2        NIRSCWAMPLITUDE        A1          Cz            760                  V
S2-D1        NIRSCWAMPLITUDE        A2          Fz            760                  V
S3-D4        NIRSCWAMPLITUDE        VisS2       VisD4         760                  V
```

## Optode description (`*_optodes.tsv`)

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["optodes"]) }}

File that provides the location and type of optodes. Note that coordinates MUST be
expressed  in Cartesian coordinates according to the NIRSCoordinateSystem and
NIRSCoordinateSystemUnits fields in `*_coordsystem.json`. If an `*_optodes.tsv`
file is specified, a `*_coordsystem.json` file MUST be specified as well.
The order of the required columns in the `*_optodes.tsv` file MUST be as listed below.

The x, y, and z positions are for measured locations, for example, with a polhemus
digitizer. If you also have idealised positions, where you wish the optodes to be
placed, these can be listed in the template values. SNIRF contains arrays for both
the 3D and 2D locations of data. The BIDS format MUST store the 3D locations if
available, and only the 2D locations if 3D positions are unavailable. The storage
of 2D locations would be indicated by the z field containing an n/a value.

The following columns MUST be present:

| **Column name** | **Requirement level** | **Data type**       | **Definition**                                              |
| --------------- | --------------------- | ------------------- | ----------------------------------------------------------- |
| name            | REQUIRED              | [string][]          | Name of the optode must be unique.                          |
| type            | REQUIRED              | [string][]          | Either source or detector.                                  |
| x               | REQUIRED              | [number][] or `n/a` | Measured position along the x-axis. `n/a` if not available. |
| y               | REQUIRED              | [number][] or `n/a` | Measured position along the y-axis. `n/a` if not available. |
| z               | REQUIRED              | [number][] or `n/a` | Measured position along the z-axis. `n/a` if not available. |

The following columns MAY be present:

| **Column name** | **Requirement level**               | **Data type**       | **Definition**                                                                                        |
| --------------- | ----------------------------------- | ------------------- | ----------------------------------------------------------------------------------------------------- |
| template_x      | OPTIONAL but REQUIRED if x is `n/a` | [number][] or `n/a` | Assumed or ideal position along the x axis.                                                           |
| template_y      | OPTIONAL but REQUIRED if x is `n/a` | [number][] or `n/a` | Assumed or ideal position along the y axis.                                                           |
| template_z      | OPTIONAL but REQUIRED if x is `n/a` | [number][] or `n/a` | Assumed or ideal position along the z axis.                                                           |
| description     | OPTIONAL.                           | [string][]          | Free-form text description of the optode, or other information of interest.                           |
| detector_type   | OPTIONAL.                           | [string][]          | The type of detector. Only to be used if the field `DetectorType` in `*_nirs.json` is set to `mixed`. |
| source_type     | OPTIONAL.                           | [string][]          | The type of source. Only to be used if the field `SourceType` in `*_nirs.json` is set to `mixed`.     |

Example:
```Text
name    type         x          y         z          template_x    template_y   template_z
A1      source       -0.0707    0.0000    -0.0707    -0.07         0.00         0.07
Fz      detector     0.0000     0.0714    0.0699     0.0           0.07         0.07
S1      source       -0.2707    0.0200    -0.1707    -0.03         0.02         -0.2
D2      detector     0.0022     0.1214    0.0299     0.0           0.12         0.03
VisS2   source       -0.1707    0.1200    -0.3707    -0.1          0.1          -0.4
VisD4   detector     0.0322     0.2214    0.2299     0.02          0.22         0.23
```

## Coordinate System JSON (`*_coordsystem.json`)

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["coordsystem"]) }}

A `*_coordsystem.json` file is used to specify the fiducials, the location of anatomical landmarks,
and the coordinate system and units in which the position of optodes and landmarks is expressed.
Ficiduals are objects with a well-defined location used to facilitate the localization of sensors
and co-registration, anatomical landmarks are locations on a research subject such as the nasion
(for a detailed definition see the coordinate system description in the BIDS specification).
The `*_coordsystem.json` is REQUIRED if the optional `*_optodes.tsv` is specified. If a corresponding
anatomical MRI is available, the locations of anatomical landmarks in that scan should also be stored
in the `*_T1w.json` file which goes alongside the fNIRS data.

Not all fNIRS systems provide 3D coordinate information or digitisation capabilities. In this case, the only x and y are specified and z is "n/a"

Fields relating to the fNIRS optode positions:

| **Key name**                        | **Requirement level**                                          | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                      |
| ----------------------------------- | -------------------------------------------------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIRSCoordinateSystem                | REQUIRED                                                       | [string][]    | Defines the coordinate system in which  the optode positions are expressed. See Appendix VIII for a list of restricted keywords for coordinate systems. If `"Other"`, provide definition of the coordinate system in NIRSCoordinateSystemDescription.                                                                                                |
| NIRSCoordinateUnits                 | REQUIRED                                                       | [string][]    | Units in which the coordinates that are listed in the field NIRSCoordinateSystem are represented. MUST be m, cm, or mm.                                                                                                                                                                                                                              |
| NIRSCoordinateSystemDescription     | RECOMMENDED, but REQUIRED if `NIRSCoordinateSystem` is `Other` | [string][]    | Free-form text description or link to document describing the NIRS coordinate system in detail (for example, "Coordinate system with the origin at anterior commissure (AC), negative y-axis going through the posterior commissure (PC), z-axis going to a mid-hemisperic point which lies superior to the AC-PC line, x-axis going to the right"). |
| NIRSCoordinateProcessingDescription | RECOMMENDED                                                    | [string][]    | Free-form text description of any post-processing (such as projection) that has been done on the optode positions (for example, "surface_projection", "none").                                                                                                                                                                                       |

Fields relating to the position of fiducials measured during an fNIRS session/run:

{{ MACROS___make_metadata_table(
   {
      "FiducialsDescription": "OPTIONAL",
      "FiducialsCoordinates": "RECOMMENDED",
      "FiducialsCoordinateSystem": "RECOMMENDED",
      "FiducialsCoordinateUnits": "RECOMMENDED",
      "FiducialsCoordinateSystemDescription": 'RECOMMENDED, but REQUIRED if `FiducialsCoordinateSystem` is `"Other"`',
   }
) }}

Fields relating to the position of anatomical landmarks measured during an fNIRS session/run:

{{ MACROS___make_metadata_table(
   {
      "AnatomicalLandmarkCoordinates": "RECOMMENDED",
      "AnatomicalLandmarkCoordinateSystem": ("RECOMMENDED", "Preferably the same as the `NIRSCoordinateSystem`."),
      "AnatomicalLandmarkCoordinateUnits": "RECOMMENDED",
      "AnatomicalLandmarkCoordinateSystemDescription": 'RECOMMENDED, but REQUIRED if `AnatomicalLandmarkCoordinateSystem` is `"Other"`',
   }
) }}

Example:
```text
{
  "IntendedFor":"/sub-01/ses-01/anat/sub-01_T1w.nii",
  "NIRSCoordinateSystem":"Other",
  "NIRSCoordinateUnits":"mm",
  "NIRSCoordinateSystemDescription":"RAS orientation: Origin halfway between LPA and RPA, positive x-axis towards RPA, positive y-axis orthogonal to x-axis through Nasion,  z-axis orthogonal to xy-plane, pointing in superior direction.",
  "FiducialsDescription":"Optodes and fiducials were digitized with Polhemus, fiducials were recorded as the centre of vitamin E capsules sticked on the left/right pre-auricular and on the nasion, these are also visible on the T1w MRI"
}
```

## Example Datasets

-   [https://github.com/rob-luke/BIDS-NIRS-Tapping](https://github.com/rob-luke/BIDS-NIRS-Tapping) and at MNE-NIRS.
-   See [http://www.fieldtriptoolbox.org/example/bids_nirs/](http://www.fieldtriptoolbox.org/example/bids_nirs/) and the corresponding [ftp server](ftp://ftp.fieldtriptoolbox.org/pub/fieldtrip/example/bids_nirs/) location for three examples of fNIRS data in BIDS format. The conversion is done using FieldTrip data2bids and still preliminary. They will  have to be re-executed when this BEP and data2bids are updated.

## Temporary

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["nirs", "events", "channels", "optodes", "coordsystem"]) }}

<!-- Link Definitions -->

[number]: https://www.w3schools.com/js/js_json_datatypes.asp

[string]: https://www.w3schools.com/js/js_json_datatypes.asp

[boolean]: https://www.w3schools.com/js/js_json_datatypes.asp
