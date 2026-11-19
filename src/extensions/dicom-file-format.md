## BEP???: DICOM as a file format for imaging and other modalities

### High-level Description

Propose the adoption of the `.dcm` (DICOM) file/folder as an acceptable file format for imaging and potentially other modalities.

### Motivation

BIDS already supports a **broad** range of file formats spanning various data modalities.
The choice of any particular format was typically made based on the dominance of that format in a research field (e.g., NIfTI for neuroimaging data), or the absence of a dominant format, which led to allowing for multiple formats (e.g., [`ctf`](#ctf), [`fif`](#neuromagelektamegin), [`4d`](#bti4d-neuroimaging) + 3 more for [MEG](../appendices/meg-file-formats.md)).
The BRAIN Initiative®-supported [NWB](#nwb) file format was added for intracranial electroencephalography, even though it supports many modalities.

The following extract from "The Future of BIDS" section of the WiP draft of the PPFofBIDS paper discusses this further:

> Another direction for future efforts is further integration with other related standards.  Whereas the NIfTi file format has become standard within the MRI research community, DICOM has grown into the industry standard for a wide range of imaging modalities (such as physiology, etc.), while addressing the many shortcomings that had originally turned the neuroimaging research community towards simpler formats. As a result, many standardization efforts have been duplicated. As DICOM is the industry standard and more data will be arriving in DICOMs, coordination with developments in DICOM could help to ensure more rapid adoption of new imaging sequences and even modalities into the BIDS standard, which provides an umbrella organization at the study level.

I strongly believe that BIDS should seriously consider "native" DICOM support for imaging files for the reasons outlined above.
Moreover, the adoption of the DICOM file format would bridge the gap between research and clinical communities.
Importantly, to prevent isolated development within BIDS, it is crucial to introduce support for a data format that is widely used in a vast domain of clinical research and is actively being developed.

### Current State & Prior Work

Ongoing projects related to DICOM and BIDS ecosystems include:

- Numerous working groups (WGs), similar to our BEPs, supporting new data modalities: https://www.dicomstandard.org/activity/wgs .
We have contacted WG-16 (#1515)  and identified potential work items (#1516 and so on).
- DICOM is transitioning from "free text" to existing dictionaries and ontologies for various fields, e.g. SNOMED CT for Body Part ([table_CID_8134](https://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_CID_8134.html#table_CID_8134)
and [chapter_L](https://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html)).
- Data archives such as the [NCI Imaging Data Commons](https://imaging.datacommons.cancer.gov/) operate on DICOMs
  - They have developed libraries like [highdicom](https://github.com/ImagingDataCommons/highdicom) to "facilitate the creation and handling of DICOM objects for image-derived information".
  - There likely more developments to benefit from reusing or integrating with, e.g. https://mhub.ai
- We are already using many DICOM tags and aim to harmonize this usage further (#1450). Given DICOM's aforementioned shift to using ontologies, we are already lagging here, and in turn, we might want to contribute back perhaps regarding the NIDM-Terms effort (attn @dbkeator).
- Projects such as the http://chrisproject.org on the border of clinical and research communities provide infrastructure centered around data digestion from PACS.
- ... Please contribute as suggestions ...

As part of the https://github.com/matthew-brett/czi-nibabel grant work, @matthew-brett led a series of journal club meetings in late 2021 to review different possible file formats for imaging data.

@matthew-brett - do you have recordings/notes from those sessions? I don't recall DICOM being considered.

### Summary of Proposed Developments

Develop a BEP to allow `.dcm` to be an accepted file format for MRI and other data types (the BEP work would decide which specifically).

#### Cons: Potential Issues and Solutions

- Duplication of metadata between `.dcm` and BIDS-sidecar `.json`.
  - This issue is not new or specific to DICOM: it needs to be addressed conceptually in BIDS (https://github.com/bids-standard/bids-specification/pull/761).
  - In fact, it offers a **benefit** of metadata harmonization, particularly when DICOM or manufacturers do not yet provide information in non-manufacturer-specific sections of DICOM.
- Libraries needed to support DICOM I/O to support BIDS: experiences with `dcm2niix` suggest that it remains a challenge to consistently access imaging data from DICOMs.
  - A good range of implementations already exist, which could potentially be improved?
- ... Please contribute as suggestions ...

#### Pros: Additional Benefits

- The research community could contribute more actively to DICOM, thereby ensuring that DICOM meets the needs of the research community (instead of it playing "catch-up").
- No need for actual data conversion.
  - Refer to "Cons:" for the remaining need for metadata harmonization.
- Establishing a tighter collaboration between the DICOM and BIDS communities.
- Improved acceptance and adoption of BIDS within the community.
- ... Please contribute as suggestions ...
