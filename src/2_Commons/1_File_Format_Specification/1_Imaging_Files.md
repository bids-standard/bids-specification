Imaging files
-------------

All imaging data MUST be stored using the NIfTI file format. We RECOMMEND using compressed NIfTI files (.nii.gz), either version 1.0 or 2.0. Imaging data SHOULD be converted to the NIfTI format using a tool that provides as much of the NIfTI header information (such as orientation and slice timing information) as possible. Since the NIfTI standard offers limited support for the various image acquisition parameters available in DICOM files, we RECOMMEND that users provide additional meta information extracted from DICOM files in a sidecar JSON file (with the same filename as the `.nii[.gz]` file, but with a `.json` extension). Extraction of BIDS
compatible metadata can be performed using dcm2nii [https://www.nitrc.org/projects/dcm2nii/](https://www.nitrc.org/projects/dcm2nii/) and dicm2nii [http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m](http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m) DICOM to NIfTI converters. A provided validator[https://github.com/INCF/bids-validator](https://github.com/INCF/bids-validator) will
check for conflicts between the JSON file and the data recorded in the
NIfTI header.
