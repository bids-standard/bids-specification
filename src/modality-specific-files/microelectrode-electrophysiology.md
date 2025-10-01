# Microelectrode Electrophysiology

Support for Microelectrode Electrophysiology was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals) [BEP032: Animal electrophysiology (ephys)](https://bids.neuroimaging.io/bep032).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension
when referring to it in the context of the academic literature.

This BEP has been initiated by members of the INCF Working Group on Standardized Data Structures,
that was initiated in 2020 to develop a set of specifications and tools
that would allow the standardization of a directory structure for experimental data recorded
with animal models in neuroscience, and its associated metadata.

Most core principles of the original BIDS and particulars of BIDS-iEEG specification are adopted
for this modality as well, though some special considerations and additional fields were added.

!!! example "Example datasets"

    Several [example Microelectrode Electrophysiology datasets](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#microephys)
    have been formatted using this specification and can be used for practical guidance when curating a new dataset.

## Primary Data File Formats

Microelectrode electrophysiology (`microephys`) modality data (of `icephys` or `ecephys` datatypes) must be stored in an [open file format](https://en.wikipedia.org/wiki/Open_format),
while the native format, if different, can be stored in an optional  `sourcedata/` directory.
The native file format is used in case conversion elicits the loss of crucial metadata specific to manufacturers and specific acquisition systems.
Metadata should be included alongside the data in the `.json` and `.tsv` files.
The current list of allowed data file formats:

<!-- We should define icephys and ecephys -->

| **Format**                                                                          | **Extension(s)** | **Description**                                                                                                                                                                                                           |
| ----------------------------------------------------------------------------------- | ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [Neuroscience Information Exchange Format](https://nixio.readthedocs.io/en/latest/) | `.nix`           | A generic and open  framework with an hdf5 backend and a defined interface to many microephys formats via the [Neo library](https://neo.readthedocs.io/en/latest/). The `.nix` file has to contain a valid Neo structure. |
| [Neurodata Without Borders](https://www.nwb.org)                                    | `.nwb`           | An open data standard for neurophysiology, including data from intracellular and extracellular electrophysiology experiments.                                                                                             |

Both of these formats can also store essential metadata of the datasets.
Some of this metadata needs to be duplicated in BIDS `.tsv` and `.json` sidecar files.
Even though the duplication requires additional effort to ensure the consistency of the data, it provides several advantages:

-   It makes the dataset easier for humans to scan, as essential information is easily accessible without loading the data files.
-   The dataset adheres to the BIDS standard and can benefit from tools built on top of this standard, such as [bids-validator](https://github.com/bids-standard/bids-validator).
-   It simplifies the separation of data and basic metadata, enabling, for example, the publication of a dataset in a lightweight fashion with access to the data files on request (as implemented by [DataLad](https://www.datalad.org)).

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

<!-- Link Definitions -->

### icephys

{{ MACROS___make_filename_template(
"raw",
datatypes=["icephys"],
suffixes=["icephys", "events", "channels", "electrodes","scans","probes","coordsystem"]
)
}}

### ecephys

{{ MACROS___make_filename_template(
"raw",
datatypes=["ecephys"],
suffixes=["ecephys", "events", "channels", "electrodes","scans","probes","coordsystem"]
)
}}

## Sidecar JSON (`*_icephys.json` and `*_ecephys.json`)

We propose to store all metadata that is not directly related to one of the other metadata files (probe/electrode/channel information) into a single JSON file corresponding to the datatype: `_icephys.json` or `_ecephys.json` for intracellular and extracellular correspondingly.

There should be one such JSON file for each data file.

The `*_ephys.json` file can be used to store any microephys-specific metadata for the dataset. We recommend storing all setup-related metadata in a dedicated node of the JSON file called `Setup`.
We recommend using the following keys to describe the setup:

### Institution Information

{{ MACROS___make_sidecar_table("microephys.microephysInstitutionInformation") }}

### Setup Information

{{ MACROS___make_sidecar_table("microephys.microephysSetup") }}

### Processing Information

{{ MACROS___make_sidecar_table("microephys.microephysProcessing") }}

### Additional Procedure Information

Furthermore, additional information can be stored about the recording procedure.
We RECOMMEND to use a dedicated `Procedure` node with the following keys:

-   `Pharmaceuticals`
-   `Sample`
-   `Supplementary`

<!-- TODO: Yarik replaced Pharmaceuticals with PharmaceuticalName and others for now but we might look to define list of Pharmaceuticals of records with PharmaceuticalDoseAmount and PharmaceuticalDoseUnit -->

#### Pharmaceuticals

For each pharmaceutical we RECOMMEND to use a dedicated node with the name of the Pharmaceuticals containing the following administration details:

{{ MACROS___make_sidecar_table("microephys.microephysPharmaceuticals") }}

#### Sample

{{ MACROS___make_sidecar_table("microephys.microephysSample") }}

#### Supplementary

{{ MACROS___make_sidecar_table("microephys.microephysSupplementary") }}

### Task Information

If the OPTIONAL [` task-<label>`](../appendices/entities.md#task) is used, the following metadata SHOULD be used.

{{ MACROS___make_sidecar_table("microephys.microephysTaskInformation") }}

### Example `*_icephys.json` and `*_ecephys.json`

<!-- TODO: below there is Procedure.Pharmaceuticals which is not standardized since ATM there is only single pharmaceutical "allowed" and we have no "Procedure" -->

```JSON
{
  "PowerLineFrequency": 50,
  "Manufacturer": "OpenEphys",
  "ManufacturerModelName": "OpenEphys Starter Kit",
  "ManufacturerModelVersion": "OEPS-9031",
  "SamplingFrequency": 30000,
  "SamplingFrequencyUnit": "Hz",
  "Location": "Institut de Neurosciences de la Timone, Faculté de Médecine, 27, boulevard Jean Moulin, 13005 Marseille - France",
  "Software": "Cerebus",
  "SoftwareVersion": "1.5.1",
  "Creator": "John Doe",
  "Maintainer": "John Doe jr.",
  "Procedure": {
    "Pharmaceuticals": {
      "isoflurane": {
        "PharmaceuticalName": "isoflurane",
        "PharmaceuticalDoseAmount": 50,
        "PharmaceuticalDoseUnit": "ug/kg/min"
      },
      "ketamine": {
        "PharmaceuticalName": "ketamine",
        "PharmaceuticalDoseAmount": 0.1,
        "PharmaceuticalDoseUnit": "ug/kg/min"
      }
    },
    "Sample": {
      "BodyPart": "BRAIN",
      "BodyPartDetails": "Motor Cortex"
    },
    "TaskName": "Reach-to-Grasp",
    "TaskDescription": "A task that involves the reaching of an object and holding it for a specific time"
  }
}
```

## Microephys Specific Files

The following metadata files are REQUIRED for a given microephys session:

1.  `[_ses-<session_label>]_channels.tsv`: A REQUIRED file listing information on the recorded signals, such as preprocessing, filtering, ids, and others.
1.  `[_ses-<session_label>]_electrodes.tsv`: A REQUIRED file listing information on the points of electrical contact to the tissue, such as impedance, names, relative positions, and others.
1.  `[_ses-<session_label>]_probes.tsv`: A REQUIRED file listing information on the device used to acquire the electrophysiology data, such as implant or probe specification, location, material, and others.

As with all tsv-based metadata files in BIDS the probes, electrodes and channels tsv files can be accompanied by json sidecar files.

### Channels Description  (`*_channels.tsv`)

Channels are recorded signals.
These may be of neuronal origin (for example, online filtered LFP signals) or generated by the recording setup
(for example, synchronization or behavioral signals).

The channel properties are stored in a `.tsv` file.
This file contains the following information:

-   `channel_id`
-   `electrode_id` (in the case of neuronal signals)
-   Amplifier information
-   …

This table stores information about the recorded signals, *not* the electrodes. The distinction is particularly important in cases where multiple signals are recorded from a single electrode (such as Neuropixel probes). For more information about the distinction between electrodes and channels, see [the corresponding section in iEEG](./intracranial-electroencephalography.md#terminology-electrodes-vs-channels).

Columns in the `*_channel.tsv` file are:

{{ MACROS___make_columns_table("microephys.microephysChannels") }}

#### Example *_channels.tsv

```tsv
channel_id	electrode_id	gain	type	units	sampling_frequency	status
c0123	        con0123	        30	EXT	mV	30000	                good
c234	        con234	        30	EXT	mV	30000	                good
c934	        con934	        50	EXT	mV	30000	                bad
c234	        n/a	        1	SYNC	mV	1000	                good
```

Note: In many datasets multiple sets of identifiers are used for probes, electrodes and channels.
We RECOMMEND to include alternative sets of identifiers, for instance identifiers that enumerate electrodes according to their spatial arrangement, as additional custom columns in the `.tsv` file.

-*Recommended Channel Type Values**

For the `type` column we recommend to use the following terms (adapted from [iEEG](intracranial-electroencephalography.md#channels-description-_channelstsv))

| **Keyword**  | **Description**                                                                                                                 |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------- |
| **LFP**      | Low-pass filtered extracellular voltage signal that represents local field potentials                                           |
| **HP**       | High-pass filtered extracellular voltage signal as used for spike sorting                                                       |
| **MUA**      | High-pass filtered and rectified or thresholded extracellular voltage signal that represents an estimate of multi-unit activity |
| **BB**       | Unfiltered (broadband) extracellular voltage signal                                                                             |
| **SPIKES**   | Discrete signal indicating spike events as derived from spike detection or spike sorting                                        |
| **VM**       | Membrane voltage                                                                                                                |
| **IM**       | Membrane current                                                                                                                |
| **SYNC**     | Signal used for synchronization between different recording systems / channels                                                  |
| **STIM**     | Electrical stimulation                                                                                                          |
| **EEG**      | Electrode channel from electroencephalogram                                                                                     |
| **ECOG**     | Electrode channel from electrocorticogram (intracranial)                                                                        |
| **SEEG**     | Electrode channel from stereo-electroencephalogram (intracranial)                                                               |
| **DBS**      | Electrode channel from deep brain stimulation electrode (intracranial)                                                          |
| **VEOG**     | Vertical EOG (electrooculogram)                                                                                                 |
| **HEOG**     | Horizontal EOG                                                                                                                  |
| **EOG**      | Generic EOG channel if HEOG or VEOG information not available                                                                   |
| **ECG**      | ElectroCardioGram (heart)                                                                                                       |
| **EMG**      | ElectroMyoGram (muscle)                                                                                                         |
| **TRIG**     | System Triggers                                                                                                                 |
| **AUDIO**    | Audio signal                                                                                                                    |
| **PD**       | Photodiode                                                                                                                      |
| **EYEGAZE**  | Eye Tracker gaze                                                                                                                |
| **PUPIL**    | Eye Tracker pupil diameter                                                                                                      |
| **BEH**      | Behavioral signals                                                                                                              |
| **MISC**     | Miscellaneous                                                                                                                   |
| **SYSCLOCK** | System time showing elapsed time since trial started                                                                            |
| **ADC**      | Analog to Digital input                                                                                                         |
| **DAC**      | Digital to Analog output                                                                                                        |
| **REF**      | Reference channel                                                                                                               |
| **OTHER**    | Any other type of channel                                                                                                       |

### Electrodes Description  (`*_electrodes.tsv`)

Electrodes are the physical recording sites that make electrical contact with neural tissue to capture electrophysiological signals.

The electrode positions and properties are stored in a `.tsv` file (amplifier information is in `channels.tsv`).

This file contains the following information:

-   The electrode name
-   The electrode coordinates in 3 columns (`xyz`) (use `n/a` for values if a dimension is absent). By default, this is the position on the probe (not the brain).
-   The ID of the probe the electrode is located on

{{ MACROS___make_columns_table("microephys.microephysElectrodes") }}

#### Example *_electrodes.tsv

```tsv
electrode_id	probe_id	impedance	x  y  z  material	location
e0123	p01	1.1	-11.87	-1.30	-3.37	iridium-oxide	V1
e234	p01	1.5	-11.64	0.51	-4.20	iridium-oxide	V2
e934	p02	3.5	-12.11	-3.12	-2.54	iridium-oxide	V4
e234	p02	7.0	-9.94	-1.19	-2.86	iridium-oxide	V3
```

### Probes Description  (`*_probes.tsv`)

Probes are electrode-bearing devices that interface with neural tissue to record electrophysiological activity, ranging from multi-electrode arrays to single recording pipettes. They can be permanently implanted (chronic recordings) or inserted temporarily for the recording (acute recordings).

The probe positions and properties are stored in a `.tsv` file.
This file contains the probe ID, the type of recording (acute/chronic), and the probe coordinates.

#### ProbeInterface Library

[ProbeInterface](https://github.com/SpikeInterface/probeinterface) is a standard for specifying electrode layouts on probes.
The [ProbeInterface library](https://github.com/SpikeInterface/probeinterface_library) includes layouts for many common probes.

The `ProbeInterface` model corresponding to your probe can be referenced using:

-   `probeinterface_manufacturer`
-   `probeinterface_model`

For example, you could use `probeinterface_manufacturer: "neuronexus"` and `probeinterface_model: "A1x32-Poly3-10mm-50-177"` to specify a NeuroNexus A1x32 probe.

If the probe is not listed in the ProbeInterface library, you SHOULD define it using the [ProbeInterface format](https://probeinterface.readthedocs.io/en/latest/format_spec.html) and include it in a directory called `probes/` in the root of the dataset. Probes defined within the `probes/` directory MUST follow the naming convention `probeinterface_<manufacturer>_<model>.json` and comply with the [ProbeInterface specification](https://probeinterface.readthedocs.io/en/latest/format_spec.html) and [JSON schema](https://raw.githubusercontent.com/SpikeInterface/probeinterface/refs/heads/main/src/probeinterface/schema/probe.json.schema).

For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "probes": {
      "probeinterface_neuronexus_A4x8-5mm-100-200-177.json": "",
      "probeinterface_plexon_1S256.json": "",
      "...": "",
      },
   }
) }}

{{ MACROS___make_columns_table("microephys.microephysProbes") }}

#### Example *_probes.tsv

```tsv
probe_id	hemisphere	AP	ML	DV	AP_angle	ML_angle	rotation_angle	material	location	probeinterface_manufacturer	probeinterface_model
p023	left	-11.87	-1.30	-3.37	0.0	0.0	0.0	iridium-oxide	V1	neuronexus	A1x32-Poly3-10mm-50-177
p023	left	-11.64	0.51	-4.20	0.0	0.0	0.0	iridium-oxide	V2	neuronexus	A1x32-Poly3-10mm-50-177
p021	left	-12.11	-3.12	-2.54	0.0	0.0	0.0	iridium-oxide	V4	neuronexus	A1x32-Poly3-10mm-50-177
p021	left	-9.94	-1.19	-2.86	0.0	0.0	0.0	iridium-oxide	V3	neuronexus	A1x32-Poly3-10mm-50-177
```

## Surgical Coordinates System

The surgical coordinates system provides a standard way to describe the placement of an intracrial probe implantation during surgery.

### Anatomical Reference Points

In neurosurgery or in research, it is important to define coordinates for where in the brain a surgical intervention will take place. These coordinates rely on anatomical markers that are uniform across individuals. There are two major anatomical markers on the dorsal surface of the brain that are formed when the plates of the skull fuse during development, and these markers are often used to identify the location of various anatomical structures of the brain.

![Bregma and Lambda anatomical reference points](images/bregma_and_lambda.png)

**Bregma**: the anatomical point on the skull at which the coronal suture (between frontal and parietal bones) is intersected perpendicularly by the sagittal suture (between left and right parietal bones).

**Lambda**: the meeting point of the sagittal suture (between left and right parietal bones) and the lambdoid suture (between parietal and occipital bones).

Both points serve as standard reference points for stereotaxic coordinates in neuroscience research. `(0,0,0)` is assumed to be Bregma when working with rodents. It may optionally be defined differently using `coordinate_reference_point`, and **must** be defined for other species.

### Stereotaxic Coordinate System Conventions

#### Basic Coordinate System

All stereotaxic coordinate systems follow a right-handed coordinate system with the following conventions:

![AP_ML_DV coordinate system](images/AP_ML_DV.png)

-   **AP (Anterior-Posterior) axis:** Positive values are anterior to reference point
-   **ML (Medial-Lateral) axis:** Positive values are to the right (as seen from behind)
-   **DV (Dorsal-Ventral) axis:** Positive values are ventral (following right-hand rule). For humans, this is the superior-inferior axis, and positive values point to inferior.

#### Angle Measurement System

Proper understanding and application of these angles is critical for accurate probe placement and experimental reproducibility. All stereotaxic measurements use three angles to specify orientation:

##### AP angle (Anterior-Posterior rotation)

![AP angle rotation diagram](images/AP_angle.png)

-   Measured as rotation from the vertical axis in the sagittal plane
-   0° represents vertical along DV axis
-   Range: -180° to +180°
-   Positive values indicate anterior rotation
-   Example: +15° indicates probe tilted 15° anteriorly from vertical

##### ML angle (Medial-Lateral rotation)

![ML angle rotation diagram](images/ML_angle.png)

-   Measured as rotation from the vertical axis in the coronal plane
-   0° represents vertical along DV axis
-   Range: -180° to +180°
-   Positive values indicate rightward/clockwise rotation (as seen from behind)
-   Example: +20° indicates probe tilted 20° to the right from vertical

##### Rotation angle (around probe axis)

![Rotation angle diagram](images/rotation_angle.png)

-   0° when probe features align with the coronal plane
-   Range: -180° to +180° (or 0° to 360°)
-   Positive rotation is clockwise when viewed from above

!!! note "Source Attribution"

    The coordinate system conventions and angle definitions presented in this section are adapted from the [BrainSTEM documentation](https://support.brainstem.org/datamodel/schemas/coordinates/).


## Coordinate System JSON (`*_coordsystem.json`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["icephys", "ecephys"], suffixes=["coordsystem"]) }}

This `*_coordsystem.json` file contains the coordinate system in which electrode
positions are expressed. The associated MRI, CT, X-Ray, or operative photo can
also be specified.

This file is **OPTIONAL** when electrode positions are probe-relative (default case).
This file is **REQUIRED** when electrode positions are expressed in an absolute coordinate system.
When provided, the [`space-<label>`](../appendices/entities.md#space) entity is **REQUIRED** in the filename to specify the coordinate system reference.

General fields:

<!--
This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table("json.microephys.microephysCoordsystemGeneral") }}

Fields relating to the microelectrode electrophysiology electrode positions:

<!--
This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_json_table("json.microephys.microephysCoordsystemPositions") }}

`*_coordsystem.json` files SHOULD NOT be duplicated for each data file,
for example, across multiple tasks.
The [inheritance principle](../common-principles.md#the-inheritance-principle) MUST
be used to find the appropriate coordinate system description for a given data file.
If electrodes are repositioned, it is RECOMMENDED to use multiple sessions to indicate this.

### Default probe-relative coordinate systems

Microelectrode electrophysiology allows for electrode positions to be
specified without an accompanying `*_coordsystem.json` file. In this case, electrode positions
in `*_electrodes.tsv` are assumed to be **probe-relative coordinates**:

-   The origin (0, 0, 0) is at the probe tip or a standard reference point on the probe
<!-- TODO: Unsure if this reference is what we discussed in the surgical coordinate system -->
-   The `x`, `y`, and `z` coordinates describe electrode positions relative to this probe reference
- This the most common case for in-vivo recordings where electrodes are not localized in a 3D anatomical space

### Recommended 3D coordinate systems

It is preferred that electrodes are localized in a 3D coordinate system (with
respect to anatomical reference images, stereotactic coordinates, or in a
standard space as specified in the BIDS [Coordinate Systems Appendix](../appendices/coordinate-systems.md)
about preferred names of coordinate systems, such as StereoTaxic).

### Allowed 2D coordinate systems

If electrodes are localized in 2D space (only x and y are specified and z is `"n/a"`),
then the positions in this file MUST correspond to the locations expressed
in pixels on the photo/drawing/rendering of the electrodes on the brain.
In this case, `MicroephysCoordinateSystem` MUST be defined as `"Pixels"`,
and `MicroephysCoordinateUnits` MUST be defined as `"pixels"`
(note the difference in capitalization).
Furthermore, the coordinates MUST be (row,column) pairs,
with (0,0) corresponding to the upper left pixel and (N,0) corresponding to the lower left pixel.

### Multiple coordinate systems

If electrode positions are known in multiple coordinate systems (for example, probe-relative, StereoTaxic,
and AllenCCFv3), these spaces can be distinguished by the optional [`space-<label>`](../appendices/entities.md#space)
field, see the [`*_electrodes.tsv`-section](#electrodes-description-_electrodestsv)
for more information.
Note that the [`space-<label>`](../appendices/entities.md#space) fields must correspond
between `*_electrodes.tsv` and `*_coordsystem.json` if they refer to the same
data.

For examples:
-   `*_space-StereoTaxic` (electrodes are localized in stereotactic coordinate system with bregma origin)
  <!-- TODO: Add 'StereoTaxic', 'AllenCCFv3', 'PaxinosWatson', etc coordinate systems to appendix coordinate-systems.md under "Microelectrode Electrophysiology Specific Coordinate Systems" with appropriate definitions for each standard reference frame used in animal electrophysiology -->
-   `*_space-individual` (electrodes are localized in subject-specific anatomical coordinate system)
-   `*_space-AllenCCFv3` (electrodes are mapped to Allen Common Coordinate Framework v3)
-   `*_space-PaxinosWatson` (electrodes are mapped to Paxinos-Watson rat brain atlas coordinates)

When referring to the `*_electrodes.tsv` file in a certain _space_ as defined
above, the [`space-<label>`](../appendices/entities.md#space) of the accompanying `*_coordsystem.json` MUST
correspond.

For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "sub-01_electrodes.tsv": "",
      "sub-01_space-StereoTaxic_electrodes.tsv": "",
      "sub-01_space-StereoTaxic_coordsystem.json": "",
      "...": "",
      },
   }
) }}

The order of the required columns in the `*_electrodes.tsv` file MUST be as listed below.
The `x`, `y`, and `z` columns indicate the positions of the center of each electrode in Cartesian coordinates.
Units are specified in `*_coordsystem.json`.

!!! note "Coordinate system requirement"

    If a `*_space-<label>_coordsystem.json` file exists, a corresponding `*_space-<label>_electrodes.tsv` file with the same space label MUST also be present.

## Photos of the electrode positions (`*_photo.<extension>`)

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["icephys", "ecephys"], suffixes=["photo"]) }}

These can include photos of the electrodes on the brain surface, photos of
anatomical features or landmarks (such as cortical vasculature, stereotactic coordinates), and fiducials. Photos
can also include histological sections showing electrode tracks, microscope images of electrode placements,
or screenshots of a brain atlas with electrode positions.
The photos may need to be cropped and/or blurred to conceal identifying features
or entirely omitted prior to sharing, depending on obtained consent and institutional protocols.

If there are photos of the electrodes, the [`acq-<label>`](../appendices/entities.md#acq) entity should be specified
with:

-   `*_photo.<extension>` in case of an operative or in-vivo photo

-   `*_acq-<label>_photo.<extension>` where `<label>` describes the acquisition type (for example: `histology` for histological sections showing electrode tracks, `microscopy` for microscope images of electrode placements, `atlas` for screenshots showing electrodes overlaid on brain atlas)

-   `*_acq-drawing#_photo.<extension>` in case of a drawing or sketch of electrode placements

The [`ses-<label>`](../appendices/entities.md#ses) entity may be used to specify when the photo was taken.

The [`sample-<label>`](../appendices/entities.md#sample) entity may be used to specify the tissue sample for histological photos.

The [`space-<label>`](../appendices/entities.md#space) entity may be used to specify the coordinate system for atlas overlay photos.


## Recording Events (`*_events.tsv`)

The `*_events.tsv` and corresponding `*_events.json` sidecar files are OPTIONAL and can be used to
indicate time points of recording events. Each task events file requires a corresponding task data
file. These events can be internal recording system events, task-related events, or events triggered
by the experimentalist (for example, manual reward). Note that these events must share a common clock
with the corresponding microephys recording data. For more details, see the
Task Events documentation.
Note that this file can also be used to describe stimulation performed during the recording. For this,
please follow the iEEG stimulation documentation.

## Multi-part Recordings

Two different procedures are supported to handle multi-part recordings. The two options are:

1.  each recording is stored in an independent data file, and the corresponding metadata is described in the `*_scans.tsv` file; or
1.  several recordings are stored in a single data file, and the corresponding metadata is described in the `*_events.tsv` file.

These two options are made available to support different usages and habits of the experimenters, as
well as to benefit from the capability of the supported data formats (NWB and NIX).
They are described in the following subsections, and made explicit through some of the example data sets.

### Multiple tasks / runs in separate files (`*_scans.tsv`)

The `*_scans.tsv` should be used to provide information about multiple parts of an acquisition
session (for example, recording start times in case the recording was paused and restarted)
when the data from each of these different recordings is stored in separate files.
Each data file should have a name that contains a `_task-XX` and/or `_run-XX` suffix, and
should be described by at most one row in the `*_scans.tsv` file. See also the BIDS Scans
specification.
Relative paths to files should be used under a compulsory "filename" header.
If acquisition time is included, it should be with the `acq_time` header. Datetime should
be expressed in the following format 2009-06-15T13:45:30 (year, month, day, hour (24h),
minute, second; this is equivalent to the RFC3339 "date-time" format, time zone is always
assumed as local time).
The run and task keywords and the corresponding `*_scans.tsv` file are OPTIONAL and can be
ignored if the dataset consists of only one continuous recording and a single or no task.

Optional: Yes

Example of a `*_scans.tsv`:

```tsv
filename	acq_time
ephys/sub-P001_task-pull_run-01_ephys.nix	2018-07-15T09:45:30
ephys/sub-P001_task-pull_run-02_ephys.nix	2018-07-15T13:24:00
ephys/sub-P001_task-push_run-01_ephys.nix	2018-07-15T14:24:00
ephys/sub-P001_task-push_run-02_ephys.nix	2018-07-15T15:24:00
```

It is recommended to accompany the  `*_scans.tsv` file with a corresponding `*_scans.json`
sidecar file, as described in the [BIDS specifications](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file).

### Multiple recordings in a single data file (`*_events.tsv`)

The `*_events.tsv` should be used to provide information about multiple parts of an acquisition
session when the data from each of these different recordings is stored in a single data file.
In such a case, this file is REQUIRED.
This allows benefiting from the capability of the supported data formats (NIX and NWB) to store multiple
recordings in a single file, which can be convenient when these recordings share numerous characteristics
(for example, for subsequent recordings obtained on a single cell in intracellular electrophysiology).
In such case, the information about these recordings should be stored in columns added in the
`*_events.tsv` file, which are listed now.

Optional column names in `events.tsv` to support multiple recordings in a single data file:

<!-- TODO: Macro for events -->

## Microelectrode Electrophysiology Examples

### Toy datasets

#### Extracellular Electrophysiology

This dataset contains data from a single subject (subject A), that was recorded on two
days (2022-01-01 and 2022-01-02).
On the first day it performed two tasks (nose-poke & rest), and on the second day only a
rest task was performed.
Detailed information about these tasks can be found in the `tasks.tsv` and `tasks.json` files.
The electrophysiology data for each of the three recordings are stored in the corresponding
session and microephys directories in the `nix` format. Metadata about the probes, their electrodes
and the corresponding recording channels are stored in `tsv` format. Note that in this case,
this information is shared between data files (see BIDS Inheritance Principle): in the first session,
the probe, electrode and channel files apply to both data files of that session, as they do not
contain a `task` entity in their name. For the nose-poke task, additional behavioral timestamps
(events) were recorded and stored in an additional `events.tsv` file.

{{ MACROS___make_filetree_example(

{
"dataset_description.json": "",
"tasks.tsv": "",
"tasks.json": "",
"participants.tsv": "",
"sub-A/": {
"ses-20220101/": {
"ecephys/": {
"sub-A_ses-20220101_task-nosepoke_ecephys.nix": "",
"sub-A_ses-20220101_task-nosepoke_ecephys.json": "",
"sub-A_ses-20220101_task-nosepoke_events.tsv": "",
"sub-A_ses-20220101_task-rest_ecephys.nix": "",
"sub-A_ses-20220101_task-rest_ecephys.json": "",
"sub-A_ses-20220101_channels.tsv": "",
"sub-A_ses-20220101_electrodes.tsv": "",
"sub-A_ses-20220101_probes.tsv": ""
}
},
"ses-20220102/": {
"ecephys/": {
"sub-A_ses-20220102_task-rest_ecephys.nix": "",
"sub-A_ses-20220102_task-rest_ecephys.json": "",
"sub-A_ses-20220102_channels.tsv": "",
"sub-A_ses-20220102_electrodes.tsv": "",
"sub-A_ses-20220102_probes.tsv": ""
}
}
}
}

) }}

#### Intracellular Electrophysiology (Patch)

This dataset contains intracellular data from slices acquired from two subjects (20220101-A and 20220101B). Details about the subjects and the sample generation are documented in the samples (tsv/json) files. Data of each subject is stored in separate subject directories (top level directories), each of which contains an ‘icephys/’ subdirectory. Note that there is no session-level directory in this case. Here, we choose the option of having "multiple tasks/runs in separate files" as described in 3.81., to demonstrate the high level of readability offered by the filenames in this case.

For the first subject only a single sample (a cell for patch-clamp terminology) was extracted (sample-cell001), on which two recordings (runs 1 and 2) were performed. Here, the `scans.tsv` file can be used to store information such as the starting recording times. The detailed information on the recording channel (such as the recording mode used) is stored in the `channels.tsv` which, in this case, is common to all available recordings. The probes and electrodes files provide information on the pipette and solutions used for the recordings and are also shared for the two data files.

For the second subject two samples (sample-cell003 and sample-cell004) were extracted and a single recording performed on each of them. Each recording was performed using a different probe (listed in the probes.tsv) having specific electrode and channel information. Therefore, each data file has a dedicated channel and electrode file with the same name as the data file.

{{ MACROS___make_filetree_example(

{
"samples.tsv": "",
"samples.json": "",
"participants.tsv": "",
"dataset_description.json": "",
"sub-20220101A/": {
"sub-20220101A_sample-cell001_scans.tsv": "",
"icephys/": {
"sub-20220101A_sample-cell001_run-1_icephys.nwb": "",
"sub-20220101A_sample-cell001_run-1_events.tsv": "",
"sub-20220101A_sample-cell001_run-2_icephys.nwb": "",
"sub-20220101A_sample-cell001_run-2_events.tsv": "",
"sub-20220101A_channels.tsv": "",
"sub-20220101A_electrodes.tsv": "",
"sub-20220101A_probes.tsv": "",
"sub-20220101A_icephys.json": "",
"sub-20220101A_events.json": ""
}
},
"sub-20220101B/": {
"sub-20220101B_sample-cell001_scans.tsv": "",
"icephys/": {
"sub-20220101B_sample-cell002_icephys.nwb": "",
"sub-20220101B_sample-cell002_events.tsv": "",
"sub-20220101B_sample-cell002_channels.tsv": "",
"sub-20220101B_sample-cell002_electrodes.tsv": "",
"sub-20220101B_sample-cell003_icephys.nwb": "",
"sub-20220101B_sample-cell003_events.tsv": "",
"sub-20220101B_sample-cell003_channels.tsv": "",
"sub-20220101B_sample-cell003_electrodes.tsv": "",
"sub-20220101B_probes.tsv": "",
"sub-20220101B_icephys.json": "",
"sub-20220101B_events.json": ""
}
}
}

) }}

This toy data set can be found in [this repository,](https://gin.g-node.org/NeuralEnsemble/BEP032-examples/src/master/toy-dataset_patchclamp_single-record-per-file) with the content of the metadata files. The other option available to organize such data consists in storing several recordings in a single data file (as described in 3.8.2); the same data set is presented using this latter option in [this other repository](https://gin.g-node.org/NeuralEnsemble/BEP032-examples/src/master/toy-dataset_patchclamp_multiple-records-per-file), so that both options can be compared for the same data set.

## Examples of Real Datasets

Multiple datasets have been converted to follow this BEP proposal.
These datasets typically have pruned data files to reduce the data file size, but are accompanied by the full set of metadata.
A current version of these datasets [can be found on GIN](https://gin.g-node.org/NeuralEnsemble/BEP032-examples) .

For a complete dataset including all data samples the extracellular microelectrode dataset published in [Brochier (2018)](https://doi.org/10.1038/sdata.2018.55) has been reorganized according to the current version of this BEP, using the NIX data format.
The up-to-date version of the dataset [can be found on GIN](https://gin.g-node.org/sprenger/multielectrode_grasp/src/bep_animalephys) .

We will also publish another dataset using the NWB data format in the near future, and a dataset acquired
