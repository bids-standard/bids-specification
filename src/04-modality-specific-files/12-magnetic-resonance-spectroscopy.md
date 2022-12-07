# Magnetic Resonance Spectroscopy

Support for Magnetic Resonance Spectroscopy (MRS) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Several [example MRS datasets](https://github.com/bids-standard/bids-examples#mrs-datasets) have
been formatted using this specification and can be used for practical guidance when curating a new
dataset.

## MRS data

<!--
This block generates filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "raw",
   datatypes=["mrs"],
   suffixes=["svs", "mrsi", "ref", "unloc"])
}}

Each manufacturer has its own file format (sometimes multiple formats) for exporting MRS data from
the scanner console for offline processing. GE exports a P-file that stores unprocessed,
un-coil-combined data with metadata embedded in a proprietary data header. Philips has multiple
export formats, the most common being the SDAT/SPAR format. The `*.sdat` file contains either each
coil-combined average stored separately or all averages summed into a signal average. The `*.spar`
file is a plaintext file describing acquisition parameters. It is also possible to export raw data
as `*.data`/`*.list` and DICOM files. Siemens scanners allow data export in four formats: i) a
proprietary DICOM structured file known as IMA (`*.ima`); ii) a conventional DICOM MR Spectroscopy
Storage format (`*.dcm`); iii) RDA (`*.rda`) a proprietary file format with a text formatted header
followed by the binary data points; and iv) TWIX (`*.dat`) a proprietary file format designed for
storing unreconstructed and unprocessed MRS data from each individual coil element. IMA, DICOM MRS,
and RDA formats are typically used to export reconstructed and processed data; however, the sequence
designer may choose to also allow the export of un-averaged transients or data from individual coil
elements. Contrarily, Bruker stores two binary files: one file stores each average separately, while
the other file stores the sum of the average. Bruker stores the sequence name, voxel position, voxel
orientation, and other metadata in a separate plaintext file. These files are considered source data
and, if present, MUST be stored x.

Due to the diversity in manufacturers' MRS data formats, raw data MUST be converted into the
[NIfTI-MRS format](https://onlinelibrary.wiley.com/doi/10.1002/mrm.29418) (`*.nii[.gz]`). This
format is based on the NIfTI framework and is designed to accommodate the nuances of raw MRS data.
All necessary information to parse this `*.nii[.gz]` file (e.g., spectrometer frequency, echo time,
repetition time, etc.) are stored in an JSON header extension. Conversion of proprietary MRS file
formats to NIfTI-MRS and extractiaon of some (but not all) BIDS-compliant metadata can be performed
using [spec2nii](https://github.com/wtclarke/spec2nii). Note that the "rawness" of data stored in
the NIfTI-MRS file will depend on the format of the source data. It is RECOMMENDED that users export
their source data from the scanner in an appropriately raw format prior to conversion.

For MRSI data, "raw" signifies spatially reconstructed data (that is, in image space rather than
(*k*,*t*)-space), given the complexity and diversity of sampling approaches. Note that NIfTI-MRS is
not designed to store data that has not been spatially reconstructed.

### Single-voxel spectroscopy and MRS imaging

A major distinction between MRS acquisitions is whether the acquisition technique probes spectral
information from a single volume (single-voxel spectroscopy, SVS) or encodes this information along
1, 2, or 3 spatial dimensions resulting in multiple subvolumes (MRS imaging, MRSI). To avoid
confusion, the suffixes `svs` amd `mrsi` MUST be used to distinguish the two techniques. For cases
where localization is not used, the suffix `unloc` MUST be used.

Furthermore, it is common to acquire an additional MRS dataset that may serve as a reference for
scaling metabolite levels (e.g., to obtain concentrations) and/or aid preprocessing steps such as
eddy-current correction, RF coil combination, phasing, and frequency calibration. This could be
either an external reference (e.g., a phantom or a synthetic signal) or, more typically, an internal
tissue water reference. For such datasets, the suffix `ref` MUST be used. Should multiple references
exist for a given dataset, the user MAY use the `acq-<label>` entity to distinguish the files. For
example, `sub-01_acq-conc_ref.nii.gz` and `sub-01_acq-ecc_ref.nii.gz` could be used to name two
references to be used for concentration scaling and eddy-current correction, respectively.

| **Name**                                        | **`suffix`**         | **Description**                                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single-voxel spectroscopy | svs                   | MRS acquisitions where the detected MR signal is spatially localized to a single volume.                           |
| Magnetic resonance spectroscopic imaging | mrsi                   | MRS acquisitions where additional imaging gradients are used to detect the MR signal from 1, 2, or 3 spatial dimensions.                          |
| Concentration or calibration reference | ref                   | A separate MRS acquisition acquired to detect a signal to serve as a concentration reference for absolute quantification or for preprocessing (e.g., eddy-current correction).                          |
| Unlocalized spectroscopy | unloc                   | MRS acquisitions run without localization. This includes signals detected using coil sensitivity only.                           |

### MRS sequences

Given the large variety of MRS sequences, there will be times when providing sufficient detail of
acquisition parameters is helpful or indeed necessary to distinguish between datasets in a given
study. Thus, it is beneficial to provide sufficient detail in each sidecar JSON file.

The following labels for the most commonly used in vivo MRS sequences/techniques are OPTIONAL to use
when using the `acq-<label>` entity in the filename. Users are free to choose any label they wish as
long as they are consistent across participants and sessions and use only legal label characters. If
used, the chosen label SHOULD also be described in the `PulseSequenceType` field in the sidecar JSON
file.

| **Name**                                        | **`label`**         | **Description**                                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PRESS                              | press                  | A double spin-echo sequence that achieves spatial localization by employing three slice-selective RF pulses: 90°–180°–180°–acq                |
| STEAM                              | steam                  | A stimulated echo sequence that uses three 90° slice-selective pulses for spatial localization.              |
| LASER/sLASER                       | laser/slaser           | LASER uses three pairs of slice-selective 180° adiabatic full-passage (AFP) refocusing pulses for localization. These are preceded by a non-slice-selective adiabatic half-passage (AHP) excitation pulse. In sLASER, the AHP and first pair of AFP pulses are replaced with a non-adiabatic slice-selective 90° excitation pulse, typically employed to reduce the minimum TE.                                   |
| SPECIAL                            | special                | SPECIAL is a two-shot experiment. In the first shot, a pre-excitation slice-selective 180° degree AFP inversion pulse precedes a spin-echo acquisition with slice selection (90°–180°–acq). In the second shot, the adiabatic pulse is not applied. The 3D localized signal is derived by subtracting the two shots.          |
| MEGA                               | mega                   | This spectral editing technique employs a pair of frequency-selective 180° pulses to refocus *J*-coupled spins at a narrowband frequency without affecting the spins of metabolites with resonances beyond the frequency range. Applying these pulses in alternating scans (e.g., edit-ON and edit-OFF) and then subtracting the ON/OFF pairs results in a *J*-difference-edited spectrum that removes the unedited signals leaving only those signals that were affected by the editing pulses.                  |
| HERMES/HERCULES                    | hermes/hercules        | HERMES is an extension of MEGA editing whereby the two-step experiment becomes a four-step experiment. This permits multiple metabolites to be edited in a multiplexed manner. By employing Hadamard combination of the four edited sub-spectra, HERMES can reveal several metabolites unambiguously. HERCULES is a different flavor of HERMES that targets more metabolites using the same four-step experiment.                |
| Multiple-quantum coherence editing | mqc                    | Multiple-quantum coherence (MQC) editing targets *J*-coupled resonances by selecting desired coherence pathways using MQ gradients and frequency-selective RF pulses.                |
| L-COSY                             | lcosy                  | Localized correlation spectroscopy (L-COSY) is a 2D MRS technique whereby one of the interpulse durations is changed sequentially. A 2D Fourier transform produces a 2D spectrum that displays singlets on the diagonal and *J*-coupled metabolites on the off-diagonal, with the offsets equal to the *J*-coupling constants.          |
| *J*-resolved spectroscopy          | j                      | Another 2D technique, in a *J*-resolved acquisition, a series of transients are collected at different TEs. A 2D Fourier transform is applied to generate a 2D spectrum where one dimension characterizes both chemical shift and *J*-coupling and the other only the *J*-coupling constant.                              |
| Diffusion-weighted spectroscopy    | dw                     | The diffusion of intracellular metabolites can be characterized using diffusion-weighted MRS. In such acquisitions, the strength of gradients in a conventional MRS sequence is modulated to sensitize the metabolite signals to diffusion.          |
| FID spectroscopy                   | fid                    | FID spectroscopy is a pulse-acquire acquisition where an excitation pulse is followed by direct acquisition of the FID. When combined with slice- or slab-selection, , this approach is most often used in MRSI (i.e., FID-MRSI).         |
| Spin-echo spectroscopy             | spinecho               | An MRS experiment whereby the MR signal is detected using a spin-echo acquisition: e.g., 90°–180°–acq.          |

Each `<label>` in the table MAY be combined with another to describe the localization approach used
for more specific description of the acquisition. For example, `megaspecial`, `jpress`, `dwslaser`,
and so on.

## MRS metadata

MRS data MUST be described by metadata fields, stored in sidecar JSON files (`*.json`).

### Common metadata fields

Metadata described in the following sections are shared with other MR modalities
and SHOULD be present in sidecar JSON files.

#### Scanner hardware

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mrs.MRSScannerHardware") }}

#### Sequence specifics

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mrs.MRSSequenceSpecifics") }}

### MRS-specific fields

Metadata fields that MUST be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mrs.MRSRequiredFields") }}

SHOULD be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

MAY be present:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

### Example `*_svs.json`
