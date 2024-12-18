# Near-Infrared Spectroscopy

Support for Near-Infrared Spectroscopy (NIRS) was developed as a
[BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

!!! example "Example datasets"

    Several [example NIRS datasets](https://bids-standard.github.io/bids-examples/#nirs)
    have been formatted using this specification and can be used for practical guidance when curating a new dataset.

## NIRS recording data

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["nirs"],
   suffixes=["nirs", "events", "channels", "optodes", "coordsystem", "physio", "stim"])
}}

Only the *Shared Near Infrared Spectroscopy Format* ([SNIRF](https://github.com/fNIRS/snirf))
file specification is supported in BIDS. The SNIRF
specification supports one or more NIRS datasets to be stored in a single
`.snirf` file. However, to be BIDS compatible, each SNIRF file MUST contain
only a single run. A limited set of fields from the SNIRF specification are
replicated  in the BIDS specification. This redundancy allows the data to be
easily parsed by humans and machines that do not have a SNIRF reader at hand,
which improves findability and tooling development.

### Terminology

For proper documentation of NIRS recording metadata, it is important
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

It is common within the NIRS community for researchers to build their own caps
and optode holders to position their sources and detectors, or for optodes to
be directly attached to the scalp with adhesive. To facilitate description of
the wide variety of possible configurations, several fields are RECOMMENDED within
the `*_nirs.json` file.
Additionally, in certain situations, reserved keywords MUST be used.
When custom modifications are made to a commercially available cap or a custom cap is used,
then the reserved keyword `custom` MUST be used for the `CapManufacturersModelName` field.
When a custom-made cap is used, that is, no (modified) commercially available cap,
the reserved keyword `custom` MUST be used in the `CapManufacturer` field.
If no cap is used, the reserved keyword `none` MUST be used in the `CapManufacturer`
and `CapManufacturersModelName` field.
The use of `NIRSPlacementScheme` is RECOMMENDED when no cap or a customized cap is used,
and describes the positioning of the optodes.
This field may also contain a reference to a file providing a graphical depiction of the cap,
for example a PDF file, a photo, or a bitmap drawing.
If the referred file is not specified in BIDS, it MAY be placed in the
[`/sourcedata`](../common-principles.md#source-vs-raw-vs-derived-data) directory.
To clarify the usage and interaction of these fields, the following examples are provided:

-   If a commercial cap such as EasyCap actiCAP 64 Ch Standard-2 was used:
    ```JSON
    "CapManufacturer": "EasyCap",
    "CapManufacturersModelName": "actiCAP 64 Ch Standard-2",
    "NIRSPlacementScheme": "10-20"
    ```

-   If an Artinis Medical Systems cap with custom positions,
as may be done by cutting custom holes in the cap,
was used:
    ```JSON
    "CapManufacturer": "Artinis Medical Systems",
    "CapManufacturersModelName": "headcap with print, size L, it was modified by adding holes for the optodes according to the NIRSPlacementScheme and optode_layout.pdf",
    "NIRSPlacementScheme": "see optode_layout.pdf: 2 groups over the left and right dlPFC, 2 groups over the left and right PPC, 1 group over the left M1 and PMC"
    ```

-   If a completely custom cap was knitted:
    ```JSON
    "CapManufacturer": "custom",
    "CapManufacturersModelName": "custom knitted cap with holes for optodes according to the NIRSPlacementScheme and optode_knitted_layout.jpg",
    "NIRSPlacementScheme": "see optode_knitted_layout.jpg: 2 groups over the left and right dlPFC, 2 groups over the left and right PPC."
    ```

-   If no cap was used and optodes were taped to the scalp
    at positions Cz, C1 and C2:
    ```JSON
    "CapManufacturer": "none",
    "CapManufacturersModelName": "none",
    "NIRSPlacementScheme": ["Cz", "C1", "C2"],
    ```
    In these cases additional information regarding channels and optodes SHOULD be placed in `*_channels.tsv` and `*_optodes.tsv` files.

Closely spaced or short-separation source-detector pairs are often included in NIRS measurements to
obtain a measure of systemic, rather than neural, activity. These source-detector
pairs are referred to as *short channels*. There is variation in how manufacturers
implement these short channels, some use specialized sources or detectors,
and the placement mechanisms vary.
It is beyond the scope of the BIDS specification to define what constitutes a short channel,
and detailed characteristics of channels may be stored within the SNIRF file
(for example, in the `sourcePower` field).
However, to improve searchability and ease of access for users, it is useful to
know if short channels were included in the NIRS measurements; the presence of short channels is
is stored in the field `ShortChannelCount`.
If the field `ShortChannelCount` is populated, then the optional column `short_channel`
may be used in `*_channels.tsv` to describe which channels were specified as short.

For consistency between studies and institutions, we encourage users to extract
the values of these fields from the actual raw data. Whenever possible, please
avoid using ad hoc wording.

Specific NIRS fields that are REQUIRED or may be REQUIRED depending on other
metadata values:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsRequired") }}

Specific NIRS fields that SHOULD be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsRecommend") }}

#### Generic information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsBase") }}

#### Hardware information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsHardware") }}

#### Institution information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsInstitutionInformation") }}

#### Task information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("nirs.NirsTaskInformation") }}

#### Example `*_nirs.json`

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

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["nirs"],
   suffixes=["channels"])
}}

This file is RECOMMENDED as it provides easily searchable information across BIDS datasets.
Channels are a pairing of source and detector optodes with a specific wavelength of light.
Unlike in other modalities, not all pairings of optodes correspond to meaningful data
and not all pairs have to be recorded or represented in the data.  Note that the source
and detector names used in the channel specifications are specified in the `*_optodes.tsv`
file below. If a `*_channels.tsv` file is specified, an `*_optodes.tsv` file MUST be specified as well.
The required columns in the `*_channels.tsv` file MUST be ordered as listed below.

The BIDS specification supports several types of NIRS devices which output raw data in
different forms. The type of measurement is specified in the `type` column. For example,
when measurements are taken with a continuous wave (CW) device that saves the data
as optical density, the `type` should be `NIRSCWOPTICALDENSITY` and the `units` should be `unitless`,
this is equivalent to SNIRF data type `dOD`.

The columns of the channels description table stored in `*_channels.tsv` are:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_columns_table("nirs.nirsChannels") }}

### Restricted keyword list for the channel types

All NIRS channels types MUST correspond to a [valid SNIRF data type](https://github.com/fNIRS/snirf/blob/master/snirf_specification.md#appendix).
Additional channels that are recorded simultaneously with the NIRS
device and stored in the same data file SHOULD be included as well.
However, additional channels that are simultaneously recorded with a different device
SHOULD be stored according to their appropriate modality specification.
For example, motion data that was simultaneously recorded with a different device should be specified
according to the [Motion](../modality-specific-files/motion.md) and not according to the NIRS data type.
Whereas, if the motion data was acquired in with the NIRS device itself, it should be included here with the NIRS data.
Any of the channel types defined in other BIDS specification MAY be used here as well such as `ACCEL` or `MAGN`.
As several of these data types are commonly acquired using NIRS devices they are included as an example at the base of the table.
Note that upper-case is REQUIRED.

| **Keyword**                 | **Description**                                                                                                                                            |
| --------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| NIRSCWAMPLITUDE             | Continuous wave amplitude measurements. Equivalent to dataType 001 in SNIRF.                                                                               |
| NIRSCWFLUORESCENSEAMPLITUDE | Continuous wave fluorescence amplitude measurements. Equivalent to dataType 051 in SNIRF.                                                                  |
| NIRSCWOPTICALDENSITY        | Continuous wave change in optical density measurements. Equivalent to dataTypeLabel dOD in SNIRF.                                                          |
| NIRSCWHBO                   | Continuous wave oxygenated hemoglobin (oxyhemoglobin) concentration measurements. Equivalent to dataTypeLabel HbO in SNIRF.                                |
| NIRSCWHBR                   | Continuous wave deoxygenated hemoglobin (deoxyhemoglobin) concentration measurements. Equivalent to dataTypeLabel HbR in SNIRF.                            |
| NIRSCWMUA                   | Continuous wave optical absorption  measurements. Equivalent to dataTypeLabel mua in SNIRF.                                                                |
| ACCEL                       | Accelerometer channel, one channel for each spatial axis. An extra column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z). |
| GYRO                        | Gyrometer channel, one channel for each spatial axis. An extra column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z).     |
| MAGN                        | Magnetomenter channel, one channel for each spatial axis. An extra column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z). |
| MISC                        | Miscellaneous                                                                                                                                              |

### Example `*_channels.tsv`

```tsv
Name	type	source	detector	wavelength_nominal	units
S1-D1	NIRSCWAMPLITUDE	A1	Fz	760	V
S1-D1	NIRSCWAMPLITUDE	A1	Fz	850	V
S1-D2	NIRSCWAMPLITUDE	A1	Cz	760	V
S2-D1	NIRSCWAMPLITUDE	A2	Fz	760	V
S3-D4	NIRSCWAMPLITUDE	VisS2	VisD4	760	V
```

## Optode description (`*_optodes.tsv`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["nirs"],
   suffixes=["optodes"])
}}

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

The columns of the optodes description table stored in `*_optodes.tsv` are:

{{ MACROS___make_columns_table("nirs.nirsOptodes") }}

### Example `*_optodes.tsv`

```tsv
name	type	x	y	z	template_x	template_y	template_z
A1	source	-0.0707	0.0000	-0.0707	-0.07	0.00	0.07
Fz	detector	0.0000	0.0714	0.0699	0.0	0.07	0.07
S1	source	-0.2707	0.0200	-0.1707	-0.03	0.02	-0.2
D2	detector	0.0022	0.1214	0.0299	0.0	0.12	0.03
VisS2	source	-0.1707	0.1200	-0.3707	-0.1	0.1	-0.4
VisD4	detector	0.0322	0.2214	0.2299	0.02	0.22	0.23
```

## Coordinate System JSON (`*_coordsystem.json`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["nirs"],
   suffixes=["coordsystem"])
}}

A `*_coordsystem.json` file is used to specify the fiducials, the location of anatomical landmarks,
and the coordinate system and units in which the position of optodes and landmarks is expressed.
Fiducials are objects with a well-defined location used to facilitate the localization of sensors
and co-registration, anatomical landmarks are locations on a research subject such as the nasion
(for a detailed definition see [coordinate system appendix](../appendices/coordinate-systems.md)).
The `*_coordsystem.json` is REQUIRED if the optional `*_optodes.tsv` is present. If a corresponding
anatomical MRI is available, the locations of anatomical landmarks in that scan should also be stored
in the `*_T1w.json` file which goes alongside the NIRS data.

Not all NIRS systems provide 3D coordinate information or digitization capabilities.
In this case, only x and y are specified and z is `"n/a"`.

General fields:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_json_table("json.nirs.CoordsystemGeneral") }}

Fields relating to the NIRS optode positions:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_json_table(["json.nirs.CoordinateSystem", "json.nirs.CoordinateSystemDescriptionRec"]) }}

Fields relating to the position of fiducials measured during an NIRS session/run:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_json_table(["json.nirs.Fiducials", "json.nirs.FiducialsCoordinateSystemDescriptionRec"]) }}

Fields relating to the position of anatomical landmarks measured during an NIRS session/run:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_json_table(["json.nirs.AnatomicalLandmark", "json.nirs.AnatomicalLandmarkCoordinateSystemDescriptionRec"]) }}

`*_coordsystem.json` files SHOULD NOT be duplicated for each data file,
for example, across multiple tasks.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate coordinate system description for a given data file.
If optodes are repositioned, it is RECOMMENDED to use multiple sessions to indicate this.

### Example `*_coordsystem.json`

```json
{
  "NIRSCoordinateSystem": "Other",
  "NIRSCoordinateUnits": "mm",
  "NIRSCoordinateSystemDescription": "RAS orientation: Origin halfway between LPA and RPA, positive x-axis towards RPA, positive y-axis orthogonal to x-axis through Nasion, z-axis orthogonal to xy-plane, pointing in superior direction.",
  "FiducialsDescription": "Optodes and fiducials were digitized with Polhemus, fiducials were recorded as the center of vitamin E capsules sticked on the left/right pre-auricular and on the nasion, these are also visible on the T1w MRI"
}
```
