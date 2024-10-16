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
   suffixes=["ecephys", "icephys", "events", "channels", "electrodes", "scans"]
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

The participants.tsv file is located at the root of the data set directory.
Its presence is RECOMMENDED in order to describe information about the individual subjects (animals) from which the data was recorded.
It follows the [general BIDS specifications to describe participants](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#participants-file).

On top of the existing columns that can be present in this file and that are described in the BIDS specifications (participant_id, species, strain, strain_rrid, sex, handedness and age), we propose to allow adding the following ones:

{{ MACROS___make_columns_table("modality_agnostic.Participants_micro") }}

##  EPHYS specific files

The following **metadata files are required for a** given animal-ephys session:



1. <code>*[_ses-<session_label>]<strong>_probes.tsv</strong></code>: A REQUIRED probes .tsv file listing information on the device used to acquire the electrophysiology data (implant / probe specification, location, material, etc.)
2. <code>*[_ses-<session_label>]<strong>_electrodes.tsv</strong></code>: A REQUIRED electrodes .tsv file listing information on the points of electrical contact to the tissue (impedance,  names, relative positions etc.)
3. <code>*[_ses-<session_label>]<strong>_channels.tsv</strong></code>: A REQUIRED channels.tsv file listing information on the recorded signals (preprocessing, filtering, ids, etc)

As with all tsv-based metadata files in BIDS the probes, electrodes and channels tsv files can be accompanied by json sidecar files.


### Coordinate System JSON (*_coordsystem.json) & Photos of electrode positions (`_photo.jpg)

This file provides metadata on the global coordinate system in which the electrodes are placed. This file is RECOMMENDED, the listed required fields below have to be contained in case a `*_coordsystem.json` is provided. This system can be defined via reference pictures, anatomical landmarks, images of the brain or a reference atlas. For more details see the [BIDS Coordinate Systems specifications](https://bids-specification.readthedocs.io/en/stable/appendices/coordinate-systems.html).

Fields relating to the ephys probe and electrode  positions:

{{ MACROS___make_metadata_table(
   {
        "MicroephysCoordinateSystem":"REQUIRED",
        "MicroephysCoordinateUnits":"REQUIRED",
        "MicroephysCoordinateSystemDescription":"RECOMMENDED",
        "MicroephysCoordinateSystemPhoto":"OPTIONAL",
        "MEGCoordinateSystem":"REQUIRED",
   }
) }}

### **Allowed 2D coordinate systems**

If electrodes are localized in 2D space (only x and y are specified and z is `"n/a"`), then the positions in this file MUST correspond to the locations expressed in pixels on the photo/drawing/rendering of the electrodes on the brain. In this case, `ephysCoordinateSystem` MUST be defined as `"Pixels"`, and `ephysCoordinateUnits` MUST be defined as `"pixels"` (note the difference in capitalization). Furthermore, the coordinates MUST be (row,column) pairs, with (0,0) corresponding to the upper left pixel and (N,0) corresponding to the lower left pixel.


## **Photos of the electrode positions (*_photo.jpg)**

These can include photos of the electrodes on the brain surface, photos of anatomical features or landmarks (such as sulcal structure), and fiducials. Photos can also include an X-ray picture, a flatbed scan of a schematic drawing made during surgery, or screenshots of a brain rendering with electrode positions. The photos may need to be cropped and/or blurred to conceal identifying features or entirely omitted prior to sharing, depending on obtained consent.

If there are photos of the electrodes, the [acq-<label>](https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#acq) entity should be specified with:

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

{{ MACROS___make_columns_table("microephys.microephysProbes") }}


Example of `_probes.tsv`:


|probe_id|hemisphere|x|y|z|type|material|location|
|--------|----------|-|-|-|----|--------|--------|
|p023|left|-11.87|-1.30|-3.37|utah-array|iridium-oxide|V1|
|p023|left|-11.64|0.51|-4.20|utah-array|iridium-oxide|V2|
|p021|left|-12.11|-3.12|-2.54|utah-array|iridium-oxide|V4|
|p021|left|-9.94|-1.19|-2.86|utah-array|iridium-oxide|V3|


### Electrodes  (*_electrodes.tsv)

electrodes describe the points of electrodes to the tissue used for recording electrophysiological signals. The electrode positions and properties are stored in a .tsv file (amplifier information is in channels.tsv). This file contains the electrode name, the electrode coordinates in 3 columns (xyz) and the id of the probe it’s located on.  The coordinates are the relative coordinates on the probe.


{{ MACROS___make_columns_table("microephys.microephysElectrodes") }}


Example of * _electrodes.tsv:


|electrode_id|probe_id|impedance|x|y|z|material|location|
|------------|--------|---------|-|-|-|--------|--------|
|e0123	 	|p023		|1.1		|-11.87|	-1.30|-3.37|iridium-oxide|	V1|
|e234		|p023		|1.5		|-11.64|	0.51|-4.20|iridium-oxide|	V2|
|e934		|p021		|3.5		|-12.11|	-3.12|-2.54|iridium-oxide|	V4|
|e234		|p021		|7.0		|-9.94|	-1.19|-2.86|iridium-oxide|	V3|

### Channels  (*_channels.tsv)

Channels are virtual sources of recorded signals. These might be of neuronal origin (e.g. online filtered LFP signals) or generated by the recording setup (e.g. synchronization signals, behavioral signals, …). The channel properties are stored in a .tsv file. This file contains the channel_id, the electrode_id (in case of neuronal signals), the amplifier information, …

For more information about the distinction between electrodes and channels, see [the corresponding section in iEEG](https://bids-specification.readthedocs.io/en/stable/modality-specific-files/intracranial-electroencephalography.html#terminology-electrodes-vs-channels).

Columns in the `*_channel.tsv` file are:

{{ MACROS___make_columns_table("microephys.microephysChannels") }}


Example of * _channels.tsv:


|channel_id|electrode_id|gain|type|units|sampling_frequency|status|
|----------|------------|----|----|-----|------------------|------|
|c0123   |con0123		|30	|EXT		|mV	|30000			|good|
|c234|con234		|30	|EXT		|mV	|30000|			good|
|c934		|con934 		|50	|EXT		|mV	|30000|			bad|
|c234		|-|		1|	SYNC|	       V|	1000|			good|


Note: In many datasets multiple sets of identifiers are used for probes, electrodes and channels. We RECOMMEND to include alternative sets of identifiers, e.g. identifiers that enumerate electrodes according to their spatial arrangement, as additional custom columns in the .tsv file.

**Recommended Channel Type Values**

For the `type` column we recommend to use the following terms (modified from https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/04-intracranial-electroencephalography.html#channelselectrode-description-_channelselectrodestsv)
