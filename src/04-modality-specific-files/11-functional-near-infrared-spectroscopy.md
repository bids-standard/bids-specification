# Functional Near-Infrared Spectroscopy

Support for functional Near-Infrared Spectroscopy (fNIRS) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Several [example fNIRS datasets](https://github.com/bids-standard/bids-examples#fnirs-datasets)
have been formatted using this specification and can be used for practical guidance when curating a new dataset.

## fNIRS recording data

{{ MACROS___make_filename_template(datatypes=["nirs"], suffixes=["nirs", "events", "channels", "optodes", "coordsystem"]) }}

Only the *Shared Near Infrared Spectroscopy Format* ([SNIRF](https://github.com/fNIRS/snirf))
file specification is supported in BIDS. The SNIRF
specification supports one or more fNIRS datasets to be stored in a single
`.snirf` file. However, to be BIDS compatible, each SNIRF file MUST contain
only a single run. A limited set of fields from the SNIRF specification are
replicated  in the BIDS specification. This redundancy allows the data to be
easily parsed by humans and machines that do not have a SNIRF reader at hand,
which improves findability and tooling development.

Raw fNIRS data in the native format, if different from SNIRF, can also
be stored in the [`/sourcedata`](../02-common-principles.md#source-vs-raw-vs-derived-data)
directory along with code to convert the data to
SNIRF in the [`/code`](../02-common-principles.md#storage-of-derived-datasets) directory.
The unprocessed raw data should be stored in
the manufacturer's format before any additional processing or conversion is applied.
Retaining the native file format is especially valuable in a case when conversion elicits the
loss of crucial metadata unique to specific manufacturers and fNIRS systems.

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
Additionally, in certain situations, reserved keywords MUST be used.
When a custom made cap is used, the reserved keyword `custom` MUST be used in the
`CapManufacturer` field.
Similarly, when a custom cap is used or custom modifications are made to a cap,
then the reserved keyword `custom` MUST be used for the `CapManufacturersModelName` field.
If no cap is used, the reserved keyword `none` MUST be used in the `CapManufacturer`
and `CapManufacturersModelName` field.
To clarify the usage and interaction of these fields, the following examples are provided:

-   If a commercial cap such as EasyCap actiCAP 64 Ch Standard-2 was used:
    ```JSON
    "CapManufacturer": "EasyCap",
    "CapManufacturersModelName": "actiCAP 64 Ch Standard-2",
    "NIRSPlacementScheme": "n/a"
    ```

-   If an EasyCap was used but with custom positions,
    as may be done by cutting custom holes in the cap,
    was used:
    ```JSON
    "CapManufacturer": "EasyCap",
    "CapManufacturersModelName": "custom",
    "NIRSPlacementScheme": "n/a"
    ```

-   If a completely custom cap was knitted:
    ```JSON
    "CapManufacturer": "custom",
    "CapManufacturersModelName": "custom",
    "NIRSPlacementScheme": "n/a"
    ```

-   If no cap was used and optodes were taped to the scalp
    at positions Cz, C1 and C2:
    ```JSON
    "CapManufacturer": "none",
    "CapManufacturersModelName": "none",
    "NIRSPlacementScheme": ["Cz", "C1", "C2"],
    ```
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
know if short channels were included in the fNIRS measurements; the presence of short channels is
is stored in the field `ShortChannelCount`.
If the field `ShortChannelCount` is populated, then the optional column `short_channel`
may be used in `*_channels.tsv` to describe which channels were specified as short.

Generic fields: For consistency between studies and institutions,
we encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

{{ MACROS___make_sidecar_table("nirs.NirsBase") }}

Specific fNIRS fields that are REQUIRED or may be REQUIRED depending on other metadata values:

{{ MACROS___make_sidecar_table("nirs.NirsRequired") }}

Specific fNIRS fields that SHOULD be present:

{{ MACROS___make_sidecar_table("nirs.NirsRecommend") }}

Example:

```JSON
{
  "TaskName": "visual",
  "InstitutionName": "Macquarie University. Australian Hearing Hub",
  "InstitutionAddress": "6 University Ave, Macquarie University NSW 2109 Australia",
  "Manufacturer": "NIRx",
  "ManufacturersModelName": "NIRScout",
  "TaskDescription": "visual gratings and noise patterns",
  "Instructions": "look at the dot in the center of the screen and press the button when it changes color",
  "SamplingFrequency": 3.7,
  "NIRSChannelCount": 56,
  "NIRSSourceOptodeCount": 16,
  "NIRSDetectorOptodeCount": 16,
  "ACCELChannelCount": 0,
  "SoftwareFilters": "n/a",
  "RecordingDuration": 233.639,
  "HardwareFilters": {"Highpass RC filter": {"Half amplitude cutoff (Hz)": 0.0159, "Roll-off": "6dBOctave"}},
  "CapManafacturer": "NIRx",
  "CapManufacturersModelName": "Headband with print (S-M)",
  "NIRSPlacementScheme": "n/a",
}
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
this is equivalent to SNIRF data type `dOD`.

The following columns MUST be present:

{{ MACROS___make_columns_table(
   {
      "name__channels": "REQUIRED",
      "type__nirs_channels": "REQUIRED",
      "source__channels": "REQUIRED",
      "detector__channels": "REQUIRED",
      "wavelength_nominal": "REQUIRED",
      "units__nirs": "REQUIRED",
      "sampling_frequency": "OPTIONAL but REQUIRED if `SamplingFrequency` is `n/a` in `_nirs.json`",
      "orientation_component": "OPTIONAL but REQUIRED if `type` is `ACCEL`, `GYRO` or `MAGN`",
   }
) }}

The following columns MAY be present:

{{ MACROS___make_columns_table(
   {
      "wavelength_actual": "OPTIONAL",
      "description": "OPTIONAL",
      "wavelength_emission_actual": "OPTIONAL",
      "short_channel": "OPTIONAL",
      "status": "OPTIONAL",
      "status_description": "OPTIONAL",
   }
) }}

### Restricted keyword list for the channel types

All fNIRS channels types MUST correspond to a [valid SNIRF data type](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md#appendix).
Additional channels that are recorded simultaneously with the fNIRS
device and stored in the same data file SHOULD be included as well.
However, additional channels that are  simultaneously recorded with a different device
SHOULD be stored according to their appropriate modality specification.
For example, motion data that was simultaneously recorded with a different device should be specified
according to BEP029 and not according to the fNIRS data type.
Whereas, if the motion data was acquired in with the fNIRS device itself, it should be included here with the fNIRS data.
Any of the channel types defined in other BIDS specification MAY be used here as well such as `ACCEL` or `MAGN`.
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
| ACCEL                       | Accelerometer channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `*_channels.tsv` file (x, y or z). |
| GYRO                        | Gyrometer channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `*_channels.tsv` file (x, y or z).     |
| MAGN                        | Magnetomenter channel, one channel for each orientation. An extra column `component` for the axis of the orientation MUST be added to the `*_channels.tsv` file (x, y or z). |
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
digitizer. If you also have idealized positions, where you wish the optodes to be
placed, these can be listed in the template values
(for example for "template positions" computed on a sphere).
SNIRF contains arrays for both
the 3D and 2D locations of data. In BIDS the `*_optodes.tsv` file MUST contain the 3D locations. Only in case 3D positions are unavailable the 2D locations should be used, setting the z field to an `n/a` value.

The following columns MUST be present:

{{ MACROS___make_columns_table(
   {
      "name__optodes": "REQUIRED",
      "type__optodes": "REQUIRED",
      "x__optodes": "REQUIRED",
      "y__optodes": "REQUIRED",
      "z__optodes": "REQUIRED",
   }
) }}

The following columns MAY be present:

{{ MACROS___make_columns_table(
   {
      "x__template": "OPTIONAL but REQUIRED if `x` is `n/a`",
      "y__template": "OPTIONAL but REQUIRED if `y` is `n/a`",
      "z__template": "OPTIONAL but REQUIRED if `z` is `n/a`",
      "description__optode": "OPTIONAL",
      "detector_type": "OPTIONAL",
      "source__optodes": "OPTIONAL",
   }
) }}

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
Fiducials are objects with a well-defined location used to facilitate the localization of sensors
and co-registration, anatomical landmarks are locations on a research subject such as the nasion
(for a detailed definition see [coordinate system appendix](../99-appendices/08-coordinate-systems)).
The `*_coordsystem.json` is REQUIRED if the optional `*_optodes.tsv` is present. If a corresponding
anatomical MRI is available, the locations of anatomical landmarks in that scan should also be stored
in the `*_T1w.json` file which goes alongside the fNIRS data.

Not all fNIRS systems provide 3D coordinate information or digitization capabilities.
In this case, only x and y are specified and z is `"n/a"`.

Fields relating to the fNIRS optode positions:

{{ MACROS___make_sidecar_table(["nirs.CoordinateSystem", "nirs.CoordinateSystemDescriptionRec"]) }}

Fields relating to the position of fiducials measured during an fNIRS session/run:

{{ MACROS___make_sidecar_table(["nirs.Fiducials", "nirs.FiducialsCoordinateSystemDescriptionRec"]) }}

Fields relating to the position of anatomical landmarks measured during an fNIRS session/run:

{{ MACROS___make_sidecar_table(["nirs.AnatomicalLandmark", "nirs.AnatomicalLandmarkCoordinateSystemDescriptionRec"]) }}

Example:
```text
{
  "NIRSCoordinateSystem": "Other",
  "NIRSCoordinateUnits": "mm",
  "NIRSCoordinateSystemDescription": "RAS orientation: Origin halfway between LPA and RPA, positive x-axis towards RPA, positive y-axis orthogonal to x-axis through Nasion, z-axis orthogonal to xy-plane, pointing in superior direction.",
  "FiducialsDescription": "Optodes and fiducials were digitized with Polhemus, fiducials were recorded as the centre of vitamin E capsules sticked on the left/right pre-auricular and on the nasion, these are also visible on the T1w MRI"
}
```
