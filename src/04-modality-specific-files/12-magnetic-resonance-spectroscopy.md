# Magnetic Resonance Spectroscopy

Support for Magnetic Resonance Spectroscopy (MRS) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Several [example MRS datasets](https://github.com/bids-standard/bids-examples#mrs-datasets)
have been formatted using this specification and can be used for practical guidance when curating a new dataset.

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

Each manufacturer has its own file format (sometimes multiple formats) for exporting MRS data from the scanner console for offline processing.
GE exports a P-file that stores unprocessed, un-coil-combined data with metadata embedded in a proprietary data header.
Philips has multiple export formats, the most common being the SDAT/SPAR format.
The `*.sdat` file contains either each coil-combined average stored separately or all averages summed into a signal average.
The `*.spar` file is a plaintext file describing acquisition parameters.
It is also possible to export raw data as .data/.list and DICOM files.
Siemens scanners allow data export in 4 formats:
1) a proprietary DICOM structured file known as IMA (`*.ima`);
2) a conventional DICOM MR Spectroscopy Storage format (`*.dcm`);
3) RDA (`*.rda`) a proprietary file format with a text formatted header followed by the binary data points and
4) TWIX (`*.dat`) a proprietary file format designed for storing unreconstructed and unprocessed MRS data from each individual coil element.
IMA, DICOM MRS and RDA formats are typically used to export the reconstructed and processed data,
however the sequence designer may choose to also allow the export of un-averaged transients or data from individual coil elements.
Contrarily, Bruker stores two binary files: one file stores each average separately,
while the other file stores the sum of the average.
Bruker stores the sequence, voxel position, and voxel orientation;
other metadata are stored in a separate plaintext file.

Due to the diversity in manufacturer MRS data formats, we define a single standardized format for storing MRS data.
For compliance, data MUST be converted to the [NIfTI-MRS format](https://onlinelibrary.wiley.com/doi/10.1002/mrm.29418) (`*.nii.gz`),
a data format based on the NIfTI framework designed to accommodate the nuances of raw MRS data.
All necessary information to parse this `*.nii.gz` file (e.g., spectrometer frequency,
echo time, repetition time, etc.) will be stored in a sidecar JSON (`*.json`) file.
Conversion of proprietary MRS file formats to NIfTI-MRS and extraction of
some (but not all) BIDS-compliant metadata can be performed using [spec2nii](https://github.com/wtclarke/spec2nii).
Note that the "rawness" of data stored in the NIfTI-MRS file will depend
on what format the source data are in.
It is RECOMMENDED that users export their source data in an appropriately raw format
prior to conversion.

For MRSI data, "raw" signifies spatially reconstructed data
(i.e., in image space rather than (k,t)-space),
given the complexity and diversity of sampling approaches.
NIfTI-MRS is not designed to store data that has not been spatially reconstructed.

### Single-voxel spectroscopy and MRS imaging

A major distinction between MRS acquisitions is whether the acquisition technique probes
spectral information from a single volume (single-voxel spectroscopy, SVS)
or encodes this information along 1, 2 or 3 spatial dimensions
resulting in multiple subvolumes (MRS imaging, MRSI).
To avoid confusion, a suffix MUST be included in the filename and MUST be denoted as `svs` or `mrsi`.
For cases where localization is not used, the suffix `unloc` SHOULD be used.

Furthermore, it is common to acquire an additional MRS dataset that may serve
as a reference for scaling metabolite levels (e.g., to obtain concentrations)
and/or aid preprocessing steps such as eddy-current correction, RF coil combination, phasing, and frequency calibration.
This could be either an external reference (e.g., a phantom or a synthetic signal) or,
more typically, an internal tissue water reference.
For such datasets, the suffix ref MUST be used.
Should multiple references exist for a given dataset, the user MAY use the `acq-<label>` entity to distinguish the files.
For example, `sub-01_acq-conc_ref.nii.gz` and `sub-01_acq-ecc_ref.nii.gz` could be used
to name two references to be used for concentration scaling and eddy-current correction, respectively.

| **Name**                                        | **`label`**         | **Description**                                                                                                                                                                                      |
| ------------------------------------------------- | ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Single-voxel spectroscopy | svs                   | MRS acquisitions where the detected MR signal is spatially localized to a single volume.                           |
| Magnetic resonance spectroscopic imaging | mrsi                   | MRS acquisitions where additional imaging gradients are used to detect the MR signal from 1, 2, or 3 spatial dimensions.                          |
| Concentration or calibration reference | ref                   | A separate MRS acquisition acquired to detect a signal to serve as a concentration reference for absolute quantification or for preprocessing (e.g., eddy-current correction).                          |
| Unlocalized spectroscopy | unloc                   | MRS acquisitions run without localization. This includes signals detected using coil sensitivity only.                           |

### MRS metadata JSON sidecar

#### Scanner Hardware

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("mri.MRIScannerHardware") }}

#### Example `*_svs.json`
