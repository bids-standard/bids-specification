# Microelectrode Electrophysiology

Support for Microelectrode Electrophysiology was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals) [BEP032: Animal electrophysiology (ephys)](https://bids.neuroimaging.io/bep032).

Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension
when referring to it in the context of the academic literature.

This BEP has been initiated by members of the INCF Working Group on Standardized Data Structures,
that was initiated in 2020 to develop a set of specifications and tools
that would allow the standardization of a directory structure for experimental data recorded
with animal models in neuroscience, and its associated metadata.

Please consider joining this working group if you would like to contribute to this effort.
You can also reach the moderators of this BEP through our [main discussion forum](https://github.com/INCF/neuroscience-data-structure/issues), where you can participate in existing discussions or raise new questions / issues.

Most core principles of the original BIDS and particulars of BIDS-iEEG specification are adopted
for this modality as well, though some special considerations and additional fields were added.

Several [example Microelectrode Electrophysiology datasets](https://bids-standard.github.io/bids-examples/#microephys)
have been formatted using this specification and can be used for practical guidance when curating a new dataset.

## Primary data file formats

Unprocessed microelectrode electrophysiology (`icephys` and `ecephys` modalities) data must be stored in an [open file format](https://en.wikipedia.org/wiki/Open_format),
while the native format, if different, can be stored in an optional  `sourcedata/` directory.
The native file format is used in case conversion elicits the loss of crucial metadata specific to manufacturers and specific acquisition systems.
Metadata should be included alongside the data in the `.json` and `.tsv` files.
The current list of allowed data file formats:

| **Format**                                                                          | **Extension(s)** | **Description**                                                                                                                                                                                                      |
--------------------------------------------------------------------------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Neuroscience Information Exchange Format](https://nixio.readthedocs.io/en/latest/) | `.nix`           | A generic and open  framework with an hdf5 backend and a defined interface to many ephys formats via the [Neo library](https://neo.readthedocs.io/en/latest/). The `.nix` file has to contain a valid Neo structure. |
| [Neurodata Without Borders](https://www.nwb.org)                                    | `.nwb`           | BRAIN Initiative Data Standard based on an hdf5 backend ...                                                                                                                                                          |



Both of these formats can also store essential metadata of the datasets.
Some of these need to be duplicated in BIDS `.tsv` and `.json` sidecar files.
Even though the duplication requires additional effort to ensure the consistency of the data, it provides a number of advantages:
-   Making the dataset easier for humans to scan as essential information is easily accessible without loading the data files
-   The dataset follows the BIDS standard and can benefit from tools building on top of this standard, starting with [bids-validator](https://github.com/bids-standard/bids-validator).
-   It simplifies the separation of data and basic metadata, for example to publish a dataset in a light-weight fashion with access to the data files on request (as implemented by [DataLad](https://www.datalad.org)).

##

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "raw",
   datatypes=["ecephys", "icephys"],
   suffixes=["ecephys", "icephys", "events", "channels", "electrodes","scans"]
)
}}

<!-- Link Definitions -->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["icephys"],
   suffixes=["icephys", "events", "channels", "electrodes","scans","probes","coordsystem"]
)
}}

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["ecephys"],
   suffixes=["ecephys", "events", "channels", "electrodes","scans","probes","coordsystem"]
)
}}


#  PARTICIPANT keyfiles
## Participant information

The participants.tsv file is located at the root of the data set directory. Its presence is RECOMMENDED in order to describe information about the individual subjects (animals) from which the data was recorded. It follows the [general BIDS specifications to describe participants](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file). 

On top of the existing columns that can be present in this file and that are described in the BIDS specifications (participant_id, species, strain, strain_rrid, sex, handedness and age), we propose to allow adding the following ones:

{{ MACROS___make_columns_table("modality_agnostic.Participants_micro") }}

##  EPHYS specific files

The following **metadata files are required for a ** given animal-ephys session:



1. <code>*[_ses-<session_label>]<strong>_probes.tsv</strong></code>: A REQUIRED probes .tsv file listing information on the device used to acquire the electrophysiology data (implant / probe specification, location, material, etc.)
2. <code>*[_ses-<session_label>]<strong>_electrodes.tsv</strong></code>: A REQUIRED electrodes .tsv file listing information on the points of electrical contact to the tissue (impedance,  names, relative positions etc.)
3. <code>*[_ses-<session_label>]<strong>_channels.tsv</strong></code>: A REQUIRED channels.tsv file listing information on the recorded signals (preprocessing, filtering, ids, etc)

As with all tsv-based metadata files in BIDS the probes, electrodes and channels tsv files can be accompanied by json sidecar files.


### Coordinate System JSON (*_coordsystem.json) & Photos of electrode positions (`_photo.jpg)

This file provides metadata on the global coordinate system in which the electrodes are placed. This file is RECOMMENDED, the listed required fields below have to be contained in case a `*_coordsystem.json` is provided. This system can be defined via reference pictures, anatomical landmarks, images of the brain or a reference atlas. For more details see the [BIDS Coordinate Systems specifications](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html).

Fields relating to the ephys probe and electrode  positions:



* `MicroephysCoordinateSystem`: REQUIRED - Defines the coordinate system for the ephys probes. See the[ Coordinate Systems Appendix](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html) for a list of restricted keywords for coordinate systems. If `"Other"`, provide definition of the coordinate system in `ephysCoordinateSystemDescription`. If positions correspond to pixel indices in a 2D image (of either a volume-rendering, surface-rendering, operative photo, or operative drawing), this MUST be `"Pixels"`. For more information, see the section on[ 2D coordinate systems](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/04-intracranial-electroencephalography.html#allowed-2d-coordinate-systems). For a list of valid values for this field, see the[ associated glossary entry](https://bids-specification.readthedocs.io/en/stable/glossary.html#objects.metadata.iEEGCoordinateSystem).
* `MicroephysCoordinateUnits`: REQUIRED - Units of the `MicroephysCoordinateSystem`. MUST be `"pixels"` if `MicroephysCoordinateSystem` is `Pixels`. Must be one of: `"m"`, `"mm"`, `"cm"`, `"pixels"`, `"n/a"`. Unless specified explicitly in the sidecar file in the `ephysCoordinateUnits` field, the units are assumed to be mm.
* `MicroephysCoordinateSystemDescription`: RECOMMENDED, but REQUIRED if ephysCoordinateSystem is “Other”.
* `MicroephysCoordinateSystemPhoto`: OPTIONAL, but REQUIRED if ephysCoordinateSystem is “Pixels” - The reference to the reference photo used as coordinate system. See optional `_photo.jpg` files below.


### **Allowed 2D coordinate systems**

If electrodes are localized in 2D space (only x and y are specified and z is `"n/a"`), then the positions in this file MUST correspond to the locations expressed in pixels on the photo/drawing/rendering of the electrodes on the brain. In this case, `ephysCoordinateSystem` MUST be defined as `"Pixels"`, and `ephysCoordinateUnits` MUST be defined as `"pixels"` (note the difference in capitalization). Furthermore, the coordinates MUST be (row,column) pairs, with (0,0) corresponding to the upper left pixel and (N,0) corresponding to the lower left pixel.


## **Photos of the electrode positions (*_photo.jpg)**

These can include photos of the electrodes on the brain surface, photos of anatomical features or landmarks (such as sulcal structure), and fiducials. Photos can also include an X-ray picture, a flatbed scan of a schematic drawing made during surgery, or screenshots of a brain rendering with electrode positions. The photos may need to be cropped and/or blurred to conceal identifying features or entirely omitted prior to sharing, depending on obtained consent.

If there are photos of the electrodes, the [acq-<label>] (https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#acq) entity should be specified with:



* `*_photo.jpg` in case of an operative photo
* `*_acq-xray#_photo.<extension>` in case of an x-ray picture
* `*_acq-drawing#_photo.<extension>` in case of a drawing or sketch of electrode placements
* `*_acq-render#_photo.<extension>` in case of a rendering

The file `<extension>` for photos MUST be either `.jpg`, `.png` or `.tif`.

The[ ses-<label>](https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#ses) entity may be used to specify when the photo was taken.

## **Multiple coordinate systems**

The optional[ space-<label>](https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#space) entity (`*[_space-<label>]_coordsystem.json`) can be used to indicate how to interpret the electrode positions. The space `<label>` MUST be taken from one of the modality specific lists in the[ Coordinate Systems Appendix](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html). For example for iEEG data, the restricted keywords listed under[ iEEG Specific Coordinate Systems](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html#ieeg-specific-coordinate-systems) are acceptable for `<label>`.


### Probes (*_probes.tsv)

Probes are physical devices used for recording animal ephys data. They can be permanently implanted (chronic recordings) or inserted just for the recording (acute recordings). The probe positions and properties are stored in a .tsv file. This file contains the probe id, the type of recording (acute/chronic) and the probe coordinates.



* `probe_id`: REQUIRED - A unique identifier of the probe, can be identical with the device_serial_number (expected to match probe_ids listed in electrodes.tsv)
* `type`: REQUIRED - The type of the probe
* 
* coordinate_space: RECOMMENDED - The name of the reference space used for the coordinate definition, can be one of the following terms: ‘anatomical’ , ‘recording chamber’, ‘sample’, ‘other’. In case of ‘anatomical’ the ‘anatomical_axes_orientation’ is REQUIRED
* placement_picture: OPTIONAL - Path to a photograph showing the placement of the probe
* `x:` RECOMMENDED - probe  position along the global x-axis.` `
* `y:` RECOMMENDED - probe  position along the global y-axis.
* `z:` RECOMMENDED - probe  position along the global z-axis.
* xyz_position_unit: RECOMMENDED - units used for x,y and z values
* `manufacturer:` RECOMMENDED - Manufacturer of the probes system  (e.g. "openephys”, “alphaomega",”blackrock”) 
* `device_serial_number:` RECOMMENDED - The serial number of the probe (provided by the manufacturer). 
* `electrode_count`: OPTIONAL - Number of miscellaneous analog electrodes for auxiliary signals (e.g. 2). 
* `width`: OPTIONAL Physical width of the probe, e.g. 5. This dimension corresponds to the x’ axis of the Euler transformation defined by alpha, beta and gamma rotations values below.
* `height`: OPTIONAL - Physical height of the probe, e.g. 5. This dimension corresponds to the y’ axis of the Euler transformation defined by alpha, beta and gamma rotations values below.
* `depth`: OPTIONAL - Physical depth of the probe, e.g. 0.3. This dimension should be omitted or set to 0 for two-dimensional (shank-type) probes. This dimension corresponds to the z’ axis of the Euler transformation defined by alpha, beta and gamma rotations values below.
* `dimension_unit`: OPTIONAL - Units of the physical dimensions  ‘width’, ‘height’ and `depth` of the probe, e.g. ‘mm’
* `alpha_rotation`: RECOMMENDED - Euler angle in degree to match probe extension dimensions (width, height, depth) to global x, y, z coordinates.
* `beta_rotation`: RECOMMENDED - Euler angle in degree to match probe extension dimensions (width, height, depth) to global x, y, z coordinates.
* `gamma_rotation`: RECOMMENDED - Euler angle in degree to match probe extension dimensions (width, height, depth) to global x, y, z coordinates.
* `coordinate_reference_point`: RECOMMENDED - Point of the probe that is described by the probe coordinates and on which the alpha, beta and gamma rotations are applied
* `hemisphere: RECOMMENDED - `Which brain hemisphere was the probe  located
* `associated_brain_region`: RECOMMENDED - A textual  indication on the location of the probe. We recommend to use species-independent terms based on Uberon ([https://obophenotype.github.io/uberon](https://obophenotype.github.io/uberon/))
* `associated_brain_region_id`: RECOMMENDED An identifier of the associated brain region based on the Uberon ([https://obophenotype.github.io/uberon](https://obophenotype.github.io/uberon/)) ontology for  anatomical structures in animals. E.g. ‘UBERON:0010415’ 
* `associated_brain_region_quality_type`: RECOMMENDED The method used to identify the associated brain region (estimated|proof) depending on anatomical pictures proofing the location or indirect estimation of the location.
* `reference_atlas`: RECOMMENDED  reference atlas used for associated brain region, we recommend using an ebrains supported atlas if compatible ([https://ebrains.eu/services/atlases#services](https://ebrains.eu/services/atlases#services))
* `material`: OPTIONAL - A textual description of the base material of the probe.

Example of * _probes.tsv:



|probe_id|hemisphere|x|y|z|type|material|location|
|--------|----------|-|-|-|----|--------|--------|
|p023|left|-11.87|-1.30|-3.37|utah-array|iridium-oxide|V1|
|p023|left|-11.64|0.51|-4.20|utah-array|iridium-oxide|V2|
|p021|left|-12.11|-3.12|-2.54|utah-array|iridium-oxide|V4|
|p021|left|-9.94|-1.19|-2.86|utah-array|iridium-oxide|V3|




### Electrodes  (*_electrodes.tsv)

electrodes describe the points of electrodes to the tissue used for recording electrophysiological signals. The electrode positions and properties are stored in a .tsv file (amplifier information is in channels.tsv). This file contains the electrode name, the electrode coordinates in 3 columns (xyz) and the id of the probe it’s located on.  The coordinates are the relative coordinates on the probe.



* `electrode_id:`  REQUIRED - ID of the electrode (expected to match channel.tsv)
* `probe_id`: REQUIRED - Id of the probe the electrode is on
* `hemisphere:`  RECOMMENDED - Which brain hemisphere was the electrode located. Must be one of “L” or “R”.
* x: RECOMMENDED - recorded position along the local width-axis relative to the probe origin and rotation (see probes.tsv)
* `y:` RECOMMENDED - recorded position along the local height-axis relative to the probe origin and rotation (see probes.tsv)`. `
* `z:` RECOMMENDED - recorded position along the local depth-axis relative to the probe origin and rotation (see probes.tsv).` `
* `physical_unit`: RECOMMENDED - units used for x, y and z coordinates as well as electrode size, internal_pipette_diameter and external_pipette_diameter
* `impedance:`  RECOMMENDED - Impedance of the electrode or pipette (pipette_resistance). This can be a single value or a list of two values indicating a value range.
* impedance_unit: RECOMMENDED - The unit of the impedance. If not specified it’s assumed to be in kOhm
* `shank_id`: OPTIONAL - Id to specify which shank of the probe the electrode is on.
* `electrode_size:` OPTIONAL - size of the electrode, e.g. non-insulated surface area or length of non-insulated cable in the unit of `physical_unit`^2
* electrode_shape: OPTIONAL - description of the shape of the electrode, e.g. square, circle,
* `material:` OPTIONAL - material of the electrode surface for solid electrodes, pipette material for hollow electrodes, e.g. Tin, Ag/AgCl, Gold, glass
* `location`: RECOMMENDED - An indication on the location of the electrode (e.g. cortical layer 3, CA1, etc)
* insulation: RECOMMENDED- Material used for insulation around the electrode
* `pipette_solution` : OPTIONAL - Solution used to fill the pipette, see also [openMINDS pipette](https://github.com/openMetadataInitiative/openMINDS_ephys/blob/v1/schemas/device/pipetteUsage.schema.tpl.json)
* `internal_pipette_diameter`: OPTIONAL - internal diameter of the pipette, see also [openMINDS pipette](https://github.com/HumanBrainProject/openMINDS_ephys/blob/v1/schemas/device/pipette.schema.tpl.json), Value has to be provided in the `physical_units` 
* `external_pipette_diameter`: OPTIONAL - external diameter of the pipette, see also [openMINDS pipette](https://github.com/HumanBrainProject/openMINDS_ephys/blob/v1/schemas/device/pipette.schema.tpl.json). Value has to be  provided  in the `physical_units` 
* Do we want a field about target or histological brain area?

Example of * _electrodes.tsv:



|electrode_id|probe_id|impedance|x|y|z|material|location|
|------------|--------|---------|-|-|-|--------|--------|
|e0123	 	|p023		|1.1		|-11.87|	-1.30|-3.37|iridium-oxide|	V1|
|e234		|p023		|1.5		|-11.64|	0.51|-4.20|iridium-oxide|	V2|
|e934		|p021		|3.5		|-12.11|	-3.12|-2.54|iridium-oxide|	V4|
|e234		|p021		|7.0		|-9.94|	-1.19|-2.86|iridium-oxide|	V3|

