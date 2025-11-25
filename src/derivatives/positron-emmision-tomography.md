# Positron Emission Tomography Derivatives

Support for PET Derivatives was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals). Please see [Citing BIDS](../introduction.md#citing-bids) on how to
appropriately credit this extension when referring to it in the context of academic literature.

## Goals and scope of this extension

PET-BIDS Derivatives is a representation of the outputs of common PET preprocessing pipelines, capturing data and meta-data sufficient for a researcher to understand and (critically) reuse those outputs in subsequent processing. It is motivated by use cases where formalized machine readable access to processed data enables higher level processing. In general, it will still follow the “Guidelines for the content and format of PET brain data in publications and archives: A consensus paper”.

## The PET-BIDS Derivatives specification

We can distinguish two broad categories of derivatives, in case 1, the different preprocessing
steps are saved and documented, in case 2, only a few final outputs are saved and all steps are
documented in the corresponding json sidecar file. In both cases, changes are documented both
in the filename and the json file to indicate the chain of events. For example, motion corrected
PET data should have the filename `sub-XX_desc-mc_pet.nii.gz`, and then if partial volume
correction using Muller-Gartner (mg) is subsequently applied, the filename should be
`sub-XX-desc-mc_pvc-mg_pet.nii.gz`. For case 2, description values and the chain of events
can be documented using a descriptions.json file, as specified here. Below, we outline the
set of preprocessing steps often carried out in PET brain imaging
(motion correction, registration etc), and also specify the set of files and naming
conventions adopted in the PET-BIDS derivatives specification.

![Diagram of PET Preprocessing Steps](../modality-specific-files/images/PET_preprocessing_steps_overview.png)

<!--
This block generates a filename template.
The inputs for this macro can be found in the directory
  src/schema/rules/files/deriv/pet.yaml
-->
{{ MACROS___make_filename_template(
    "raw",
    datatypes=["pet"],
    suffixes=["pet", "kinpar"]
) }}

## Motion Correction (MC)

Motion correction is a critical preprocessing step in PET imaging to account for patient movements during the scan. The output files should document both the motion-corrected PET images and the estimated motion metrics (e.g. rotation and translation).

