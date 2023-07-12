## BEP???: DICOM as a file format for imaging and other modalities

### High-level Description

Make `.dcm` (DICOM) file/folder to become acceptable file format for the imaging, and possibly other modalities.

### Motivation

BIDS already supports a **wide** range of file formats across different data modalities.
Choices for any particular format were typically made based on the presence of dominant in research field file format (e.g., NIfTI for neuroimaging data) or absence of such, which lead to allowing for multiple formats (e.g., [`ctf`](#ctf), [`fif`](#neuromagelektamegin), [`4d`](#bti4d-neuroimaging) + 3 more for [MEG](../appendices/meg-file-formats.md)).
A BRAIN Initiative® supported [NWB](#nwb) file format (although supporting many modalities) was added to support intracranial electroencephalography.

From a paragraph within "The Future of BIDS" of WiP draft of the PPFofBIDS paper:

> Another direction for future efforts is further integration with other related standards.  Whereas the NIfTi file format has become standard within the MRI research community, DICOM has grown into the industry standard for a wide range of imaging modalities (such as physiology, etc.), while addressing the many shortcomings that had originally turned the neuroimaging research community towards simpler formats. As a result, many standardization efforts have been duplicated. As DICOM is the industry standard and more data will be arriving in DICOMs, coordination with developments in DICOM could help to ensure more rapid adoption of new imaging sequences and even modalities into the BIDS standard, which provides an umbrella organization at the study level.

And I am of an opinion that "native" DICOM support for imaging files should be seriously considered for BIDS for the outlined in the paragraph reasons. 
Moreover, adoption of DICOM file format would bridge a gap between research and clinical communities.
And overall, to avoid silo-ed development of BIDS, it is important to introduce support for the data format which is used widely in vast domain of the clinical research, and which has being actively developed. 

### Current state & Prior Work
 
Ongoing related projects in DICOM and BIDS ecosystems:

- a long list of working groups (WGs) working, quite alike to our BEPs, to support new data modalities etc: https://www.dicomstandard.org/activity/wgs . 
We got in touch with WG-16 (#1515)  and some possible work items were identified (#1516 and so on).
- DICOM is adopting existing dictionaries and ontologies in favor of "free text" for various fields, e.g. SNOMED CT for Body Part ([table_CID_8134](https://dicom.nema.org/medical/dicom/current/output/chtml/part16/sect_CID_8134.html#table_CID_8134)
and [chapter_L](https://dicom.nema.org/medical/dicom/current/output/chtml/part16/chapter_L.html))
- data archives such as [NCI Imaging Data Commons](https://imaging.datacommons.cancer.gov/) operate on DICOMs
  - developed libraries such as [highdicom](https://github.com/ImagingDataCommons/highdicom) to "to facilitate the creation and handling of DICOM objects for image-derived information"
- We are already re-using many of DICOM tags and hopefully would harmonize that reuse more (#1450). Given aforementioned switch by DICOM to use ontologies, we are already playing a long catch up game here, and also in turn might want to contribute back may be re the NIDM-Terms effort (attn @dbkeator)
- Projects such a http://chrisproject.org on the edge between clinical and research communities provide infrastructure centered around digestion of data from PACS
- ... contribute here as suggestions ...


Having observed limitations of NIfTI format, as part of the https://github.com/matthew-brett/czi-nibabel grant work @matthew-brett  carried out a number of journal club meetings in late 2021 reviewing different possible file formats for imaging data. 

@matthew-brett - do you have recording/notes from those sessions? I don't recall DICOM being considered.

### Summary of proposed developments

Develop BEP for allowing `.dcm` to be the allowed file format for MRI and other data types (work on BEP would decide on which specifically) 

#### Cons: Possible problems and ways to overcome

- duplication of metadata between `.dcm` and BIDS-sidecar `.json`
  - nothing new, specific to DICOM: need to be addressed conceptually in BIDS (https://github.com/bids-standard/bids-specification/pull/761)
  - actually provides a **benefit** of harmonization of metadata especially whenever DICOM or manufacturers do not yet provide information in non-manufacturer specific sections of DICOM
- libraries needed to support DICOM I/O to support BIDS: experiences of `dcm2niix` suggest that it remains non-trivial to access imaging data in a consistent way from DICOMs
  - there is a good range of implementation already available, and just need to be improved?
- ... contribute here as suggestions ...


#### Pros: Extra benefits to reap

- research community would contribute more actively to DICOM thus helping to ensure that DICOM fulfills the needs of the research community (intead of it playing "catch-up" game)
- no need for actual data conversion
  - see above in "Cons:" remaining need for metadata harmonization
- establishing tight(er) collaboration between DICOM and BIDS communities
- acceptance/adoption of BIDS within community 
- ... contribute here as suggestions ...