# Common principles

## The Inheritance Principle

Any metadata file (`.json`, `.bvec`, `.tsv`, etc.) may be defined at any directory level, but no more than one applicable file may be defined at a given level (Example 1).  The values from the top level are inherited by all lower levels unless they are overridden by a file at the lower level. For example, `sub-*_task-rest_bold.json` may be specified at the participant level, setting TR to a specific value. If one of the runs has a different TR than the one specified in that file, another `sub-*_task-rest_bold.json` file can be placed within that specific series directory specifying the TR for that specific run.
There is no notion of "unsetting" a key/value pair. For example if there is a JSON file corresponding to particular participant/run defining a key/value and there is a JSON file on the root level of the dataset that does not define this key/value it will not be "unset" for all subjects/runs.
Files for a particular participant can exist only at participant level directory, i.e
`/dataset/sub-*[/ses-*]/sub-*_T1w.json`. Similarly, any  file that is not specific to a participant is to be declared only at top level of dataset for eg: `task-sist_bold.json` must be placed under `/dataset/task-sist_bold.json`

Example 1: Two JSON files at same level that are applicable for NIfTI
file.

```
sub-01/
    ses-test/
        sub-test_task-overtverbgeneration_bold.json
        sub-test_task-overtverbgeneration_run-2_bold.json
        anat/
            sub-01_ses-test_T1w.nii.gz
        func/
            sub-01_ses-test_task-overtverbgeneration_run-1_bold.nii.gz
            sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz
```

In the above example, two JSON files are listed under
`sub-01/ses-test/`, which are each applicable to `sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz`, violating the constraint that no more than one file may be defined at a given level of the directory structure. Instead `task-overtverbgeneration_run-2_bold.json` should have been under `sub-01/ses-test/func/`.

Example 2:  Multiple run and rec with same acquisition (acq) parameters acq-test1

```
sub-01/
    anat/
    func/
        sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
        sub-01_task-xyz_acq-test1_run-2_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
        sub-01_task-xyz_acq-test1_bold.json
```

For the above example, all NIfTI files are acquired with same scanning parameters (`acq-test1`). Hence a JSON file describing the acq parameters will apply to different runs and rec files. Also if the JSON file (`task-xyz_acq-test1_bold.json`) is defined at dataset top level  directory, it  will be applicable to all task runs with `test1` acquisition parameter.

Case 2:  Multiple json files at different levels for same task and acquisition parameters
```
sub-01/
   sub-01_task-xyz_acq-test1_bold.json
         anat/
         func/
             sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
             sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
             sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
```

In the above example, the fields from `task-xyz_acq-test1_bold.json` file will apply to all bold runs. However, if there is a key with different value in `sub-01/func/sub-01_task-xyz_acq-test1_run-1_bold.json`,
the new value will be applicable for that particular run/task NIfTI
file/s.

## File Formation specification

### Imaging files

All imaging data MUST be stored using the NIfTI file format. We RECOMMEND using compressed NIfTI files (.nii.gz), either version 1.0 or 2.0. Imaging data SHOULD be converted to the NIfTI format using a tool that provides as much of the NIfTI header information (such as orientation and slice timing information) as possible. Since the NIfTI standard offers limited support for the various image acquisition parameters available in DICOM files, we RECOMMEND that users provide additional meta information extracted from DICOM files in a sidecar JSON file (with the same filename as the `.nii[.gz]` file, but with a `.json` extension). Extraction of BIDS
compatible metadata can be performed using dcm2nii [https://www.nitrc.org/projects/dcm2nii/](https://www.nitrc.org/projects/dcm2nii/) and dicm2nii [http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m](http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m) DICOM to NIfTI converters. A provided validator[https://github.com/INCF/bids-validator](https://github.com/INCF/bids-validator) will
check for conflicts between the JSON file and the data recorded in the
NIfTI header.

### Tabular files

Tabular data MUST be saved as tab delimited values (`.tsv`) files, i.e. csv files where commas are replaced by tabs. Tabs MUST  be true tab characters and MUST NOT be a series of space characters. Each TSV file MUST start with a header line listing the names of all columns (with the exception of physiological and other continuous acquisition data - see below for details). Names MUST be separated with tabs. String values containing tabs MUST be escaped using double quotes. Missing and non-applicable values MUST be coded as `n/a`.

Example:
```
onset duration  response_time correct stop_trial  go_trial
200 200 0 n/a n/a n/a
```

Tabular files MAY be optionally accompanied by a simple data dictionary in a JSON format (see below). The data dictionaries MUST have the same name as their corresponding tabular files but with `.json` extensions. Each entry in the data dictionary has a name corresponding to a column name and the following fields:

| Field name  | Definition                                                     |
|:------------|:---------------------------------------------------------------|
| LongName    | Long (unabbreviated) name of the column.                       |
| Description | Description of the column.                                     |
| Levels      | For  categorical variables: a dictionary of possible values (keys) and their descriptions (values). |
| Units       | Measurement units.  `[<prefix symbol>] <unit symbol>` format following the SI standard is RECOMMENDED (see Appendix V). |
| TermURL     | URL pointing to a formal definition of this type of data in an ontology available on the web. |

Example:

```JSON
{
  "test": {
    "LongName": "Education level",
    "Description": "Education level, self-rated by participant",
    "Levels": {
      "1": "Finished primary school",
      "2": "Finished secondary school",
      "3": "Student at university",
      "4": "Has degree from university"
    }
  },
  "bmi": {
    "LongName": "Body mass index",
    "Units": "kilograms per squared meters",
    "TermURL": "http://purl.bioontology.org/ontology/SNOMEDCT/60621009"
  }
}
```

## Key/value files (dictionaries)

JavaScript Object Notation (JSON) files MUST be used for storing key/value pairs. Extensive documentation of the format can be found here: [http://json.org/](http://json.org/).  Several editors have built-in support for JSON syntax highlighting that aids manual creation of such files. An online editor for JSON with built-in validation is available at: [http://jsoneditoronline.org](http://jsoneditoronline.org). JSON
files MUST be in UTF-8 encoding.

Example:
```JSON
{
  "RepetitionTime": 3,
  "Instruction": "Lie still and keep your eyes open"
}
```

Participant names and other labels
----------------------------------

BIDS uses custom user-defined labels in several situations (naming of participants, sessions, acquisition schemes, etc.) Labels are strings and MUST only consist of letters (lower or upper case) and/or numbers. If numbers are used we RECOMMEND  zero padding (e.g., `01` instead of `1` if you have more than nine subjects) to make alphabetical sorting more intuitive. Please note that the sub- prefix is not part of the subject label, but must be included in file names (similarly to other key names).
In contrast to other labels, run and echo labels MUST be integers. Those labels MAY include zero padding, but this is NOT RECOMMENDED to maintain their uniqueness.

Units
-----

All units SHOULD be specified as per International System of Units (abbreviated as SI, from the French Système international (d'unités)) and can be SI units or SI derived units. In case there are valid reasons to deviate from  SI units or SI derived units, the units MUST be specified in the sidecar JSON file. In case data is expressed in SI units or SI derived units,  the units MAY be specified in the sidecar JSON file.  In case prefixes are added to SI or non-SI units (e.g. mm), the prefixed units MUST be specified in the JSON file (see Appendix V: Units).  In particular:

-   Elapsed time SHOULD be expressed in seconds. Please note that some DICOM parameters have been traditionally expressed in milliseconds. Those need to be converted to seconds.
-   Frequency SHOULD be expressed in Hertz.

Describing dates and timestamps:

-   Date time information MUST be expressed in the following format `YYYY-MM-DDThh:mm:ss` (one of the [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time formats). For example: `2009-06-15T13:45:30`
-   Time stamp information MUST be expressed in the following format: `13:45:30`
-   Dates can be shifted by a random number of days for privacy protection reasons. To distinguish real dates from shifted dates always use year 1900 or earlier when including shifted years. For longitudinal studies please remember to shift dates within one subject by the same number of days to maintain the interval information. Example: `1867-06-15T13:45:30`
-   Age SHOULD be given as the number of years since birth at the time of scanning (or first scan in case of multi session datasets). Using higher accuracy (weeks) should in general be avoided due to privacy protection, unless when appropriate given the study goals, e.g., when scanning babies.

Directory structure
-------------------

### Single session example

This is an example of the folder and file structure. Because there is only one session, the session level is not required by the
format. For details on individual files see descriptions in the next
section:

```
sub-control01/
    anat/
        sub-control01_T1w.nii.gz
        sub-control01_T1w.json
        sub-control01_T2w.nii.gz
        sub-control01_T2w.json
    func/
        sub-control01_task-nback_bold.nii.gz
        sub-control01_task-nback_bold.json
        sub-control01_task-nback_events.tsv
        sub-control01_task-nback_physio.tsv.gz
        sub-control01_task-nback_physio.json
        sub-control01_task-nback_sbref.nii.gz
    dwi/
        sub-control01_dwi.nii.gz
        sub-control01_dwi.bval
        sub-control01_dwi.bvec
    fmap/
        sub-control01_phasediff.nii.gz
        sub-control01_phasediff.json
        sub-control01_magnitude1.nii.gz
        sub-control01_scans.tsv

    code/
        deface.py
    derivatives/
    README
    participants.tsv
    dataset_description.json
    CHANGES
```

Additional files and folders containing raw data may be added as needed for special cases.  They should be named using all lowercase with a name that reflects the nature of the scan (e.g., `calibration`).  Naming of files within the directory should follow the same scheme as above (e.g., `sub-control01_calibration_Xcalibration.nii.gz`)
