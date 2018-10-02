The Brain Imaging Data Structure (BIDS) Specification
=====================================================

version 1.1.1 (working copy)
Available under the CC-BY 4.0 International license.

Browse example datasets:
[https://github.com/INCF/BIDS-examples](https://github.com/INCF/BIDS-examples)

Download example datasets:
[https://openneuro.org/public/datasets](https://openneuro.org/public/datasets)

3 Introduction
==============

3.1 Motivation
--------------

Neuroimaging experiments result in complicated data that can be arranged in many different ways. So far there is no consensus how to organize and share data obtained in neuroimaging experiments. Even two researchers working in the same lab can opt to arrange their data in a different way. Lack of consensus (or a standard) leads to misunderstandings and time wasted on rearranging data or rewriting scripts expecting certain structure. Here we describe a simple and easy-to-adopt way of organising neuroimaging and behavioural data. By using this standard you will benefit in the following ways:

-   It will be easy for another researcher to work on your data. To understand the organisation of the files and their format you will only need to refer them to this document. This is especially important if you are running your own lab and anticipate more than one person working on the same data over time. By using BIDS you will save time trying to understand and reuse data acquired by a graduate student or postdoc that has already left the lab.
-   There are a growing number of data analysis software packages that can understand data organised according to BIDS (see [http://bids.neuroimaging.io](http://bids.neuroimaging.io) for the most up to date list).
-   Databases such as OpenNeuro.org accept datasets organised according to BIDS. If you ever plan to share your data publicly (nowadays some journals require this) you can minimize the additional time and energy spent on publication, and speed up the curation process by using BIDS to structure and describe your data right after acquisition.
-   There are [validation tools](https://github.com/Squishymedia/BIDS-Validator) that can check your dataset integrity and let you easily spot missing values.

BIDS is heavily inspired by the format used internally by OpenfMRI.org and has been supported by the International Neuroinformatics Coordinating Facility and the Neuroimaging Data Sharing Task Force. While working on BIDS we consulted many neuroscientists to make sure it covers most common experiments, but at the same time is intuitive and easy to adopt. The specification is intentionally based on simple file formats and folder structures to reflect current lab practices and make it accessible to a wide range of scientists coming from different backgrounds.

3.2 Definitions
---------------

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in
[[RFC2119](https://www.ietf.org/rfc/rfc2119.txt)].

Throughout this protocol we use a list of terms. To avoid misunderstanding we clarify them here.

1.  Dataset - a set of neuroimaging and behavioural data acquired for a purpose of a particular study. A dataset consists of data acquired from one or more subjects, possibly from multiple sessions.
2.  Subject - a person or animal participating in the study.
3.  Session - a logical grouping of neuroimaging and behavioural data consistent across subjects. Session can (but doesn't have to) be synonymous to a visit in a longitudinal study. In general, subjects will stay in the scanner during one session. However, for example, if a subject has to leave the scanner room and then be re-positioned on the scanner bed, the set of MRI acquisitions will still be considered as a session and match sessions acquired in other subjects. Similarly, in situations where different data types are obtained over several visits (for example fMRI on one day followed by DWI the day after) those can be grouped in one session. Defining multiple sessions is appropriate when several identical or similar data acquisitions are planned and performed on all -or most- subjects, often in the case of some intervention between sessions (e.g., training).
4.  Data acquisition - a continuous uninterrupted block of time during which a brain scanning instrument was acquiring data according to particular scanning sequence/protocol.
5.  Data type - a functional group of different types of  data. In BIDS we define five data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.), meg (magnetoencephalography).
6.  Task - a set of structured activities performed by the participant. Tasks are usually accompanied by stimuli and responses, and can greatly vary in complexity. For the purpose of this protocol we consider the so-called "resting state" a task. In the context of brain scanning, a task is always tied to one data acquisition. Therefore, even if during one acquisition the subject performed multiple conceptually different behaviours (with different sets of instructions) they will be considered one (combined) task.
7.  Event - a stimulus or subject response recorded during a task. Each event has an onset time and duration. Note that not all tasks will have recorded events (e.g., resting state).
8.  Run - an uninterrupted repetition of data acquisition that has the same acquisition parameters and task (however events can change from run to run due to different subject response or randomized nature of the stimuli). Run is a synonym of a data acquisition.

3.3 Compulsory, optional, and additional data and metadata
----------------------------------------------------------

The following standard describes a way of arranging data and writing down metadata for a subset of neuroimaging experiments. Some aspects of the standard are compulsory. For example a particular file name format is required when storing structural scans. Some aspects are regulated but optional. For example a T2 volume does not need to be included, but when it is available it should be saved under a particular file name specified in the standard.
This standard aspires to describe a majority of datasets, but acknowledges that there will be cases that do not fit. In such cases one can include additional files and subfolders to the existing folder structure following common sense. For example one may want to include eye tracking data in a vendor specific format that is not covered by this standard. The most sensible place to put it is next to the continuous recording file with the same naming scheme but different extensions. The solutions will change from case to case and publicly available datasets will be reviewed to include common data types in the future releases of the BIDS spec.

3.4 Source vs. raw vs. derived data
-----------------------------------

BIDS in its current form is designed to harmonize and describe raw (unprocessed or minimally processed due to file format conversion) data. During analysis such data will be transformed and partial as well as final results will be saved. Derivatives of the raw data (other than products of DICOM to NIfTI conversion) MUST be kept separate from the raw data. This way one can protect the raw data from accidental changes by file permissions. In addition it is easy to distinguish partial results from the raw data and share the latter. Similar rules apply to source data which is defined as data before harmonization and/or file format conversion (for example E-Prime event logs or DICOM files).

This specification currently does not go into details of recommending a particular naming scheme for including different types of source data (raw event logs, parameter files, etc. before conversion to BIDS) and data derivatives (correlation maps, brain masks, contrasts maps, etc.). However, in the case that these data are to be included:

1.  These data MUST be kept in separate `sourcedata` and `derivatives`
    folders each with a similar folder structure as presented below for the BIDS-managed data. For example:
    `derivatives/fmriprep/sub-01/ses-pre/sub-01_ses-pre_mask.nii.gz` or `sourcedata/sub-01/ses-pre/func/sub-01_ses-pre_task-rest_bold.dicom.tgz` or `sourcedata/sub-01/ses-pre/func/MyEvent.sce`.
2.  A README file SHOULD be found at the root of the `sourcedata` or the
    `derivatives` folder (or both). This file should describe the nature of the raw data or the derived data. In the case of the existence of a `derivatives` folder, we RECOMMEND including details about the software stack and settings used to generate the results. Inclusion of non-imaging objects that improve reproducibility are encouraged (scripts, settings files, etc.).
3.  We RECOMMEND including the PDF print-out with the actual sequence
    parameters generated by the scanner in the  `sourcedata` folder.

3.5 The Inheritance Principle
-----------------------------

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

3.6 Extensions
--------------

The BIDS specification can be extended in a backwards compatible way  and will evolve over time. A number of extensions are currently being worked on:

| Extension label                                                                           | Title                                                                                                                                                                                         | Moderators/leads |
|:------------------------------------------------------------------------------------------|:----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|:--|
| [BEP001](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg) | [Structural acquisitions that include multiple contrasts (multi echo, flip angle, inversion time) sequences](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg) | Gilles de Hollander |
| [BEP002](https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M) | [The BIDS Models Specification](https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M)                                                                              | Tal Yarkoni |
| [BEP003](https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4) | [Common Derivatives](https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4)                                                                                         | Chris Gorgolewski |
| [BEP004](https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc) | [Susceptibility Weighted Imaging (SWI)](https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc)                                                                      | Fidel Alfaro Almagro |
| [BEP005](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c) | [Arterial Spin Labeling (ASL)](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c)                                                                               | Henk-Jan Mutsaerts and Michael Chappell |
| [BEP006](https://docs.google.com/document/d/1ArMZ9Y_quTKXC-jNXZksnedK2VHHoKP3HCeO5HPcgLE) | [Electroencephalography (EEG)](https://docs.google.com/document/d/1ArMZ9Y_quTKXC-jNXZksnedK2VHHoKP3HCeO5HPcgLE)                                                                               | Cyril R Pernet, Robert Oostenveld, Stefan Appelhoff |
| [BEP009](https://docs.google.com/document/d/1mqMLnxVdLwZjDd4ZiWFqjEAmOmfcModA_R535v3eQs0) | [Positron Emission Tomography (PET)](https://docs.google.com/document/d/1mqMLnxVdLwZjDd4ZiWFqjEAmOmfcModA_R535v3eQs0)                                                                         | Melanie Ganz |
| [BEP010](https://docs.google.com/document/d/1qMUkoaXzRMlJuOcfTYNr3fTsrl4SewWjffjMD5Ew6GY) | [intracranial Electroencephalography (iEEG)](https://docs.google.com/document/d/1qMUkoaXzRMlJuOcfTYNr3fTsrl4SewWjffjMD5Ew6GY)                                                                 | Dora Hermes and Chris Holdgraf |
| [BEP011](https://docs.google.com/document/d/1YG2g4UkEio4t_STIBOqYOwneLEs1emHIXbGKynx7V0Y) | [The structural preprocessing derivatives](https://docs.google.com/document/d/1YG2g4UkEio4t_STIBOqYOwneLEs1emHIXbGKynx7V0Y)                                                                   | Andrew Hoopes |
| [BEP012](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU) | [The functional preprocessing derivatives](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU)                                                                   | Camille Maumet and Chris Markiewicz |
| [BEP013](https://docs.google.com/document/d/1qBNQimDx6CuvHjbDvuFyBIrf2WRFUOJ-u50canWjjaw) | [The resting state fMRI derivatives](https://docs.google.com/document/d/1qBNQimDx6CuvHjbDvuFyBIrf2WRFUOJ-u50canWjjaw)                                                                         | Steven Giavasis |
| [BEP014](https://docs.google.com/document/d/11gCzXOPUbYyuQx8fErtMO9tnOKC3kTWiL9axWkkILNE) | [The affine transformations and nonlinear field warps](https://docs.google.com/document/d/11gCzXOPUbYyuQx8fErtMO9tnOKC3kTWiL9axWkkILNE)                                                       | Oscar Esteban |
| [BEP015](https://docs.google.com/document/d/1WYOTXDB7GzlHoWqLjd45I3uGBgPxXddST-NTqBnroJE) | [Mapping file](https://docs.google.com/document/d/1WYOTXDB7GzlHoWqLjd45I3uGBgPxXddST-NTqBnroJE)                                                                                               | Eric Earl, Camille Maumet, and Vasudev Raguram |
| [BEP016](https://docs.google.com/document/d/1cQYBvToU7tUEtWMLMwXUCB_T8gebCotE1OczUpMYW60) | [The diffusion weighted imaging derivatives](https://docs.google.com/document/d/1cQYBvToU7tUEtWMLMwXUCB_T8gebCotE1OczUpMYW60)                                                                 | Franco Pestilli and Oscar Esteban |
| [BEP017](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA) | [Generic BIDS connectivity data schema](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA)                                                                      | Eugene Duff and Paul McCarthy |
| [BEP018](https://docs.google.com/document/d/1uRkgyzESLKuGjXi98Z97Wh6vt-iLN5nOAb9TG16CjUs) | [Genetic information](https://docs.google.com/document/d/1uRkgyzESLKuGjXi98Z97Wh6vt-iLN5nOAb9TG16CjUs)                                                                                        | Cyril R Pernet, Clara Moreau, and Thomas Nichols |
| [BEP019](https://docs.google.com/document/d/1FqJI791ycXr0bfRg2qyLqAf0RpVttJ2cInOgMWrKsNU) | [DICOM Metadata](https://docs.google.com/document/d/1FqJI791ycXr0bfRg2qyLqAf0RpVttJ2cInOgMWrKsNU)                                                                                             | Satrajit Ghosh |
| [BEP020](https://docs.google.com/document/d/1eggzTCzSHG3AEKhtnEDbcdk-2avXN6I94X8aUPEBVsw) | [Eye Tracking including Gaze Position and Pupil Size(ET)](https://docs.google.com/document/d/1eggzTCzSHG3AEKhtnEDbcdk-2avXN6I94X8aUPEBVsw)                                                    | Benjamin Gagl and Dejan Draschkow |
| [BEP021](https://docs.google.com/document/d/1PmcVs7vg7Th-cGC-UrX8rAhKUHIzOI-uIOh69_mvdlw) | [Common Electrophysiological Derivatives](https://docs.google.com/document/d/1PmcVs7vg7Th-cGC-UrX8rAhKUHIzOI-uIOh69_mvdlw)                                                                    | Stefan Appelhoff, Cyril Pernet, Robert Oostenveld, Teon Brooks |


When an extension reaches maturity it is merged into the main body of the specification. If you would like to contribute to BIDS please consult the [BIDS Contributor
Guide](https://docs.google.com/document/d/1pWmEEY-1-WuwBPNy5tDAxVJYQ9Een4hZJM06tQZg8X4/edit?usp%3Dsharing&sa=D&ust=1537468908724000)
All of the ideas that are not backwards compatible and thus will have to wait for BIDS 2.0 are listed [here](https://docs.google.com/document/d/1LEgsMiisGDe1Gv-hBp1EcLmoz7AlKj6VYULUgDD3Zdw)

3.7 Citing BIDS
---------------

When referring to BIDS in context of academic literature please
cite:

> Gorgolewski, K.J., Auer, T., Calhoun, V.D., Craddock, R.C., Das, S., Duff, E.P., Flandin, G., Ghosh, S.S., Glatard, T., Halchenko, Y.O., Handwerker, D.A., Hanke, M., Keator, D., Li, X., Michael, Z., Maumet, C., Nichols, B.N., Nichols, T.E., Pellman, J., Poline, J.-B., Rokem, A., Schaefer, G., Sochat, V., Triplett, W., Turner, J.A., Varoquaux, G., Poldrack, R.A., 2016. [The brain imaging data structure, a
> format for organizing and describing outputs of neuroimaging
> experiments](https://www.nature.com/articles/sdata201644). Sci Data 3, 160044.

as well as other papers describing specific BIDS extensions (see below).

BIDS has also a [Research Resource Identifier
(RRID)](https://www.force11.org/group/resource-identification-initiative) - `RRID:SCR_016124` - which you can also include in your manuscript in addition to citing the paper.

4 File Format specification
===========================

All parts of a BIDS filename are considered case-sensitive. Thus `task-xyz_acq-test1_run-1_bold.json` and `task-xyz_acq-Test1_run-2_bold.json` will
be treated as having different acquisition labels by a BIDS validator or
should be treated as different by bids-aware libraries.

4.1 Imaging files
-----------------

All imaging data MUST be stored using the NIfTI file format. We RECOMMEND using compressed NIfTI files (.nii.gz), either version 1.0 or 2.0. Imaging data SHOULD be converted to the NIfTI format using a tool that provides as much of the NIfTI header information (such as orientation and slice timing information) as possible. Since the NIfTI standard offers limited support for the various image acquisition parameters available in DICOM files, we RECOMMEND that users provide additional meta information extracted from DICOM files in a sidecar JSON file (with the same filename as the `.nii[.gz]` file, but with a `.json` extension). Extraction of BIDS
compatible metadata can be performed using dcm2nii [https://www.nitrc.org/projects/dcm2nii/](https://www.nitrc.org/projects/dcm2nii/) and dicm2nii [http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m](http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m) DICOM to NIfTI converters. A provided validator[https://github.com/INCF/bids-validator](https://github.com/INCF/bids-validator) will
check for conflicts between the JSON file and the data recorded in the
NIfTI header.

4.2 Tabular files
-----------------

Tabular data MUST be saved as tab delimited values (`.tsv`) files, i.e. csv files where commas are replaced by tabs. Tabs MUST  be true tab characters and MUST NOT be a series of space characters. Each TSV file MUST start with a header line listing the names of all columns (with the exception of physiological and other continuous acquisition data - see below for details). Names MUST be separated with tabs. String values containing tabs MUST be escaped using double quotes. Missing and non-applicable values MUST be coded as `n/a`.

### 4.2.1 Example:
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

### 4.2.2 Example:

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

4.3 Key/value files (dictionaries)
----------------------------------

JavaScript Object Notation (JSON) files MUST be used for storing key/value pairs. Extensive documentation of the format can be found here: [http://json.org/](http://json.org/).  Several editors have built-in support for JSON syntax highlighting that aids manual creation of such files. An online editor for JSON with built-in validation is available at: [http://jsoneditoronline.org](http://jsoneditoronline.org). JSON
files MUST be in UTF-8 encoding.

### 4.3.1 Example:
```JSON
{
  "RepetitionTime": 3,
  "Instruction": "Lie still and keep your eyes open"
}
```

5 Participant names and other labels
====================================

BIDS uses custom user-defined labels in several situations (naming of participants, sessions, acquisition schemes, etc.) Labels are strings and MUST only consist of letters (lower or upper case) and/or numbers. If numbers are used we RECOMMEND  zero padding (e.g., `01` instead of `1` if you have more than nine subjects) to make alphabetical sorting more intuitive. Please note that the sub- prefix is not part of the subject label, but must be included in file names (similarly to other key names).
In contrast to other labels, run and echo labels MUST be integers. Those labels MAY include zero padding, but this is NOT RECOMMENDED to maintain their uniqueness.

6 Units
=======

All units SHOULD be specified as per International System of Units (abbreviated as SI, from the French Système international (d'unités)) and can be SI units or SI derived units. In case there are valid reasons to deviate from  SI units or SI derived units, the units MUST be specified in the sidecar JSON file. In case data is expressed in SI units or SI derived units,  the units MAY be specified in the sidecar JSON file.  In case prefixes are added to SI or non-SI units (e.g. mm), the prefixed units MUST be specified in the JSON file (see Appendix V: Units).  In particular:

-   Elapsed time SHOULD be expressed in seconds. Please note that some DICOM parameters have been traditionally expressed in milliseconds. Those need to be converted to seconds.
-   Frequency SHOULD be expressed in Hertz.

Describing dates and timestamps:

-   Date time information MUST be expressed in the following format `YYYY-MM-DDThh:mm:ss` (one of the [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time formats). For example: `2009-06-15T13:45:30`
-   Time stamp information MUST be expressed in the following format: `13:45:30`
-   Dates can be shifted by a random number of days for privacy protection reasons. To distinguish real dates from shifted dates always use year 1900 or earlier when including shifted years. For longitudinal studies please remember to shift dates within one subject by the same number of days to maintain the interval information. Example: `1867-06-15T13:45:30`
-   Age SHOULD be given as the number of years since birth at the time of scanning (or first scan in case of multi session datasets). Using higher accuracy (weeks) should in general be avoided due to privacy protection, unless when appropriate given the study goals, e.g., when scanning babies.

7 Directory structure
=========================

Overall directories hierarchy is

```
sub-<participant_label>/
    [/ses-<session_label>]/
        <data_type>/
[code/]
[derivatives/]
[stimuli/]
[sourcedata/]
```

where square brackets `[]` depicts OPTIONAL content (the same nomenclature is used throughout the spec). Session level is OPTIONAL, first we detail single session example. See below (section 9) for an example with multiple sessions.

7.1 Single session example
--------------------------

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

8 Detailed file descriptions
================================

8.1 Dataset description
---------------------------

Template: `dataset_description.json` `README` `CHANGES`

### 8.1.1 `dataset_description.json`

The file dataset_description.json is a JSON file describing the dataset. Every dataset MUST include this file with the following fields:

| Field name         | Definition                                              |
|:-------------------|:--------------------------------------------------------|
| Name               | REQUIRED. Name of the dataset.                          |
| BIDSVersion        | REQUIRED. The version of the BIDS standard that was used. |
| License            | RECOMMENDED. What license is this dataset distributed under? The use of license name abbreviations is suggested for specifying a license. A list of common licenses with suggested abbreviations can be found in Appendix II. |
| Authors            | OPTIONAL. List of individuals who contributed to the creation/curation of the dataset. |
| Acknowledgements   | OPTIONAL. Text acknowledging contributions of individuals or institutions  beyond those listed in Authors or Funding. |
| HowToAcknowledge   | OPTIONAL. Instructions how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset. |
| Funding            | OPTIONAL. List of sources of funding (grant numbers)    |
| ReferencesAndLinks | OPTIONAL. List of references to publication that contain information on the dataset, or links. |
| DatasetDOI         | OPTIONAL. The Document Object Identifier of the dataset (not the corresponding paper). |

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.0.1",
  "License": "CC0",
  "Authors": [
    "Paul Broca",
    "Carl Wernicke"
  ],
  "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
  "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
  "Funding": [
    "National Institute of Neuroscience Grant F378236MFH1",
    "National Institute of Neuroscience Grant 5RMZ0023106"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. http://doi.org/1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "10.0.2.3/dfjj.10"
}
```

### 8.1.2 `README`

In addition a free form text file (`README`) describing the dataset in more details SHOULD be provided.

### 8.1.3 `CHANGES`

Version history of the dataset (describing changes, updates and corrections) MAY be provided in the form of a `CHANGES` text file. This file MUST follow the CPAN Changelog convention: [http://search.cpan.org/~haarg/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod](https://metacpan.org/pod/release/HAARG/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod). `README` and `CHANGES` files MUST be either in ASCII or UTF-8 encoding.

Example:

```
1.0.1 2015-08-27
 - Fixed slice timing information.

1.0.0 2015-08-17
 - Initial release.
```

8.2 Code
--------

Template:
`code/*`

Source code of scripts that were used to prepare the dataset (for example if it was anonymized or defaced) MAY be stored here. Extra care should be taken to avoid including original IDs or any identifiable information with the source code. There are no limitations or recommendations on the language and/or code organization of these scripts at the moment.

8.3 Magnetic Resonance Imaging data
-----------------------------------

### 8.3.1 Common metadata fields

MR Data described in  sections 8.3.x share the following RECOMMENDED metadata fields (stored in sidecar JSON files). MRI acquisition parameters are divided into several categories based on ["A checklist for fMRI acquisition methods reporting in the literature"](https://thewinnower.com/papers/977-a-checklist-for-fmri-acquisition-methods-reporting-in-the-literature) by Ben Inglis:

#### Scanner Hardware

| Field name                    | Definition                                   |
|:------------------------------|:---------------------------------------------|
| Manufacturer                  | RECOMMENDED. Manufacturer of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0070 `Manufacturer` |
| ManufacturersModelName        | RECOMMENDED. Manufacturer's model name of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1090 `Manufacturers Model Name` |
| DeviceSerialNumber            | RECOMMENDED. The serial number of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1000 `DeviceSerialNumber`. A pseudonym can also be used to prevent the equipment from being identifiable, so long as each pseudonym is unique within the dataset |
| StationName                   | RECOMMENDED. Institution defined name of the machine that produced the composite instances. Corresponds to DICOM Tag 0008, 1010 `Station Name` |
| SoftwareVersions              | RECOMMENDED. Manufacturer’s designation of software version of the equipment that produced the composite instances. Corresponds to DICOM Tag 0018, 1020 `Software Versions` |
| HardcopyDeviceSoftwareVersion | (Deprecated) Manufacturer’s designation of the software of the device that created this Hardcopy Image (the printer). Corresponds to DICOM Tag 0018, 101A `Hardcopy Device Software Version` |
| MagneticFieldStrength         | RECOMMENDED. Nominal field strength of MR magnet in Tesla. Corresponds to DICOM Tag 0018,0087 `Magnetic Field Strength` |
| ReceiveCoilName               | RECOMMENDED. Information describing the receiver coil. Corresponds to DICOM Tag 0018, 1250 `Receive Coil Name`, although not all vendors populate that DICOM Tag, in which case this field can be derived from an appropriate private DICOM field |
| ReceiveCoilActiveElements     | RECOMMENDED. Information describing the active/selected elements of the receiver coil.  This doesn’t correspond to a tag in the DICOM ontology. The vendor-defined terminology for active coil elements can go in this field. As an example, for Siemens, coil channels are typically not activated/selected individually, but rather  in pre-defined selectable "groups" of individual channels, and the list of the  "groups" of elements that are active/selected in any given scan populates  the `Coil String` entry in Siemen’s private DICOM fields (e.g., `HEA;HEP` for the Siemens standard 32 ch coil when both the anterior and posterior groups are activated). This is a flexible field that can be used as most appropriate for a given vendor and coil to define the "active" coil elements. Since individual scans can sometimes not have the intended coil elements selected, it is preferable for this field to be populated directly from the DICOM for each individual scan, so that it can be used as a mechanism for checking that a given scan was collected with the intended coil elements selected |
| GradientSetType               | RECOMMENDED. It should be possible to infer the gradient coil from the scanner model. If not, e.g. because of a custom upgrade or use of a gradient insert set, then the specifications of the actual gradient coil should be reported independently |
| MRTransmitCoilSequence        | RECOMMENDED. This is a relevant field if a non-standard transmit coil is used. Corresponds to DICOM Tag 0018, 9049 `MR Transmit Coil Sequence` |
| MatrixCoilMode                | RECOMMENDED. (If used) A method for reducing the number of independent channels by combining in analog the signals from multiple coil elements. There are typically different default modes when using un-accelerated or accelerated (e.g. GRAPPA, SENSE) imaging |
| CoilCombinationMethod         | RECOMMENDED. Almost all fMRI studies using phased-array coils use root-sum-of-squares (rSOS) combination, but other methods exist. The image reconstruction is changed by the coil combination method (as for the matrix coil mode above), so anything non-standard should be reported |

#### Sequence Specifics

| Field name                  | Definition                                     |
|:----------------------------|:-----------------------------------------------|
| PulseSequenceType           | RECOMMENDED. A general description of the pulse sequence used for the scan (i.e. MPRAGE, Gradient Echo EPI, Spin Echo EPI, Multiband gradient echo EPI). |
| ScanningSequence            | RECOMMENDED. Description of the type of data acquired. Corresponds to DICOM Tag 0018, 0020 `Sequence Sequence`. |
| SequenceVariant             | RECOMMENDED. Variant of the ScanningSequence. Corresponds to DICOM Tag 0018, 0021 `Sequence Variant`. |
| ScanOptions                 | RECOMMENDED. Parameters of ScanningSequence. Corresponds to DICOM Tag 0018, 0022 `Scan Options`. |
| SequenceName                | RECOMMENDED. Manufacturer’s designation of the sequence name. Corresponds to DICOM Tag 0018, 0024 `Sequence Name`. |
| PulseSequenceDetails        | RECOMMENDED. Information beyond pulse sequence type that identifies the specific pulse sequence used (i.e. "Standard Siemens Sequence distributed with the VB17 software," "Siemens WIP ### version #.##," or "Sequence written by X using a version compiled on MM/DD/YYYY"). |
| NonlinearGradientCorrection | RECOMMENDED. Boolean stating if the image saved  has been corrected for gradient nonlinearities by the scanner sequence. |


#### In-Plane Spatial Encoding

| Field name                     | Definition                                  |
|:-------------------------------|:--------------------------------------------|
| NumberShots                    | RECOMMENDED. The number of RF excitations need to reconstruct a slice or volume. Please mind that  this is not the same as Echo Train Length which denotes the number of lines of k-space collected after an excitation. |
| ParallelReductionFactorInPlane | RECOMMENDED. The parallel imaging (e.g, GRAPPA) factor. Use the denominator of the fraction of k-space encoded for each slice. For example, 2 means half of k-space is encoded. Corresponds to DICOM Tag 0018, 9069 `Parallel Reduction Factor In-plane`. |
| ParallelAcquisitionTechnique   | RECOMMENDED. The type of parallel imaging used (e.g. GRAPPA, SENSE). Corresponds to DICOM Tag 0018, 9078 `Parallel Acquisition Technique`. |
| PartialFourier                 | RECOMMENDED. The fraction of partial Fourier information collected. Corresponds to DICOM Tag 0018, 9081 `Partial Fourier`. |
| PartialFourierDirection        | RECOMMENDED. The direction where only partial Fourier information was collected. Corresponds to DICOM Tag 0018, 9036 `Partial Fourier Direction`. |
| PhaseEncodingDirection         | RECOMMENDED. Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-`. The letters `i`, `j`, `k` correspond to the first, second and third axis of the data in the NIFTI file. The polarity of the phase encoding is assumed to go from zero index to maximum index unless `-` sign is present (then the order is reversed - starting from the highest index instead of zero). `PhaseEncodingDirection` is defined as the direction along which phase is was modulated which may result in visible distortions. Note that this is not the same as the DICOM term `InPlanePhaseEncodingDirection` which can have `ROW` or `COL` values. This parameter is REQUIRED if corresponding fieldmap data is present or when using multiple runs with different phase encoding directions (which can be later used for field inhomogeneity correction). |
| EffectiveEchoSpacing           | RECOMMENDED. The "effective" sampling interval, specified in seconds, between lines in the phase-encoding direction, defined based on the size of the reconstructed image in the phase direction.  It is frequently, but incorrectly, referred to as  "dwell time" (see DwellTime parameter below for actual dwell time).  It is  required for unwarping distortions using field maps. Note that beyond just in-plane acceleration, a variety of other manipulations to the phase encoding need to be accounted for properly, including partial fourier, phase oversampling, phase resolution, phase field-of-view and interpolation. This parameter is REQUIRED if corresponding fieldmap data is present. |
| TotalReadoutTime               | RECOMMENDED. This is actually the "effective" total readout time , defined as the readout duration, specified in seconds, that would have generated data with the given level of distortion.  It is NOT the actual, physical duration of the readout train.  If `EffectiveEchoSpacing` has been properly computed, it is just `EffectiveEchoSpacing * (ReconMatrixPE - 1)`. . This parameter is REQUIRED if corresponding "field/distortion" maps acquired with opposing phase encoding directions are present  (see 8.9.4). |


#### Timing Parameters

| Field name             | Definition                                          |
|:-----------------------|:----------------------------------------------------|
| EchoTime               | RECOMMENDED. The echo time (TE) for the acquisition, specified in seconds. This parameter is REQUIRED if corresponding fieldmap data is present or the data comes from a multi echo sequence. Corresponds to DICOM Tag 0018, 0081 `Echo Time`  (please note that the DICOM term is in milliseconds not seconds). |
| InversionTime          | RECOMMENDED. The inversion time (TI) for the acquisition, specified in seconds. Inversion time is the time after the middle of inverting RF pulse to middle of excitation pulse to detect the amount of longitudinal magnetization. Corresponds to DICOM Tag 0018, 0082 `Inversion Time`  (please note that the DICOM term is in milliseconds not seconds). |
| SliceTiming            | RECOMMENDED. The time at which each slice was acquired within each volume (frame) of  the acquisition.  Slice timing is not slice order -- rather, it  is a list of times (in JSON format) containing the time (in seconds) of each slice acquisition in relation to the beginning of volume acquisition.  The list goes through the slices along the slice axis in the slice encoding dimension (see below). Note that to ensure the proper interpretation of the `SliceTiming` field, it is important to check if the (optional) `SliceEncodingDirection` exists. In particular,  if `SliceEncodingDirection` is negative, the entries in `SliceTiming` are defined in reverse order with respect to the slice axis (i.e., the final entry in the `SliceTiming` list is the time of acquisition of slice 0). This parameter is REQUIRED for sparse sequences that do not have the `DelayTime` field set. In addition without this parameter slice time correction will not be possible. |
| SliceEncodingDirection | RECOMMENDED. Possible values: `i`, `j`, `k`, `i-`, `j-`, `k-` (the axis of the NIfTI data along which slices were acquired, and the direction in which SliceTiming is  defined with respect to). `i`, `j`, `k` identifiers correspond to the first, second and third axis of the data in the NIfTI file. A `-` sign indicates that the contents of SliceTiming are defined in reverse order - that is, the first entry corresponds to the slice with the largest index, and the final entry corresponds to slice index zero. When present ,the axis defined by SliceEncodingDirection  needs to be consistent with the ‘slice_dim’ field in the NIfTI header. When absent, the entries in SliceTiming must be in the order of increasing slice index as defined by the NIfTI header. |
| DwellTime              | RECOMMENDED. Actual dwell time (in seconds) of the receiver per point in the readout direction, including any oversampling.  For Siemens, this corresponds to DICOM field (0019,1018) (in ns). This value is necessary for the (optional) readout distortion correction of anatomicals in the HCP Pipelines.  It also usefully provides a handle on the readout bandwidth, which isn’t captured in the other metadata tags.  Not to be confused with `EffectiveEchoSpacing`, and the frequent mislabeling of echo spacing (which is spacing in the phase encoding direction) as "dwell time" (which is spacing in the readout direction). |


#### RF & Contrast

| Field name                  | Definition                                     |
|:----------------------------|:-----------------------------------------------|
| FlipAngle                   | RECOMMENDED. Flip angle for the acquisition, specified in degrees. Corresponds to: DICOM Tag 0018, 1314 `Flip Angle`. |
| MultibandAccelerationFactor | RECOMMENDED. The multiband factor, for multiband acquisitions. |

#### Slice Acceleration

| Field name                    | Definition                                   |
|:------------------------------|:---------------------------------------------|
| MultibandAccelerationFactor | RECOMMENDED. The multiband factor, for multiband acquisitions. |

#### Anatomical landmarks (useful for multimodal co-registration with MEG, (S)EEG, TMS, etc.)


| Field name                    | Definition                                   |
|:------------------------------|:---------------------------------------------|
| AnatomicalLandmarkCoordinates | RECOMMENDED. Key:value pairs of any number of additional anatomical landmarks and their coordinates in voxel units (where first voxel has index 0,0,0) relative to the associated anatomical MRI, (e.g. `{"AC": [127,119,149], "PC": [128,93,141], "IH": [131,114,206]}, or {"NAS": [127,213,139], "LPA": [52,113,96], "RPA": [202,113,91]}`). |

#### Institution information

| Field name                  | Definition                                     |
|:----------------------------|:-----------------------------------------------|
| InstitutionName             | RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0080 `InstitutionName`. |
| InstitutionAddress          | RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0081 `InstitutionAddress`. |
| InstitutionalDepartmentName | RECOMMENDED. The department in the  institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1040 `Institutional Department Name`. |


When adding additional metadata please use the camelcase
version of [DICOM ontology terms](https://scicrunch.org/scicrunch/interlex/dashboard) whenever possible.

### 8.3.2 Anatomy imaging data

Template:

```
sub-<participant_label>/[ses-<session_label>/]
    anat/
        sub-<participant_label>[_ses-<session_label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>]_<modality_label>.nii[.gz]
        sub-<participant_label>[_ses-<session_label>][_acq-<label>][_ce-<label>][_rec-<label>][_run-<index>][_mod-<label>]_defacemask.nii[.gz]
```

Anatomical (structural) data acquired for that participant. Currently supported modalities include:

| Name               | modality_label | Description                            |
|:-------------------|:---------------|:---------------------------------------|
| T1 weighted        | T1w            |                                        |
| T2 weighted        | T2w            |                                        |
| T1 Rho map         | T1rho          | Quantitative T1rho brain imaging<br>[http://www.ncbi.nlm.nih.gov/pubmed/24474423](http://www.ncbi.nlm.nih.gov/pubmed/24474423) <br>  [http://www.ncbi.nlm.nih.gov/pmc/articles/PMC4346383/](http://www.ncbi.nlm.nih.gov/pubmed/24474423) |
| T1 map             | T1map          | quantitative T1 map                    |
| T2 map             | T2map          | quantitative T2 map                    |
| T2*                | T2star         | High resolution T2* image              |
| FLAIR              | FLAIR          |                                        |
| FLASH              | FLASH          |                                        |
| Proton density     | PD             |                                        |
| Proton density map | PDmap          |                                        |
| Combined PD/T2     | PDT2           |                                        |
| Inplane T1         | inplaneT1      | T1-weighted anatomical image matched to functional acquisition |
| Inplane T2         | inplaneT2      | T2-weighted anatomical image matched to functional acquisition |
| Angiography        | angio          |                                        |


If several scans of the same modality are  acquired they MUST be indexed with a key-value pair: `_run-1`, `_run-2`, `_run-3` etc. (only integers are allowed as run labels). When there is only one scan of a given type the run key MAY be omitted. Please note that diffusion imaging data is stored elsewhere (see below).

The OPTIONAL `acq-<label>` key/value pair corresponds to a custom label the user MAY use to distinguish a different set of parameters used for acquiring the same modality. For example this should be used when a study includes two T1w images - one full brain low resolution and and one restricted field of view but high resolution. In such case two files could have the following names: `sub-01_acq-highres_T1w.nii.gz` and `sub-01_acq-lowres_T1w.nii.gz`, however the user is free to choose any other label than `highres` and `lowres` as long as they are consistent across subjects and sessions. In case different sequences are used to record the same modality (e.g. RARE and FLASH for T1w) this field can also be used to make that distinction. At what level of detail to make the distinction (e.g. just between RARE and FLASH, or between RARE, FLASH, and FLASHsubsampled) remains at the discretion of the researcher.

Similarly the OPTIONAL `ce-<label>` key/value can be used to distinguish sequences using different contrast enhanced images. The label is the name of the contrast agent. The key `ContrastBolusIngredient` MAY be also be added in the JSON file, with the same label.

Similarly the OPTIONAL `rec-<label>` key/value can be
used to distinguish different reconstruction algorithms (for example ones using motion correction).

If the structural images included in the dataset were defaced (to protect identity of participants) one CAN provide the binary mask that was used to remove facial features in the form of `_defacemask` files. In such cases the OPTIONAL `mod-<label>` key/value pair corresponds to modality label for eg: T1w, inplaneT1, referenced by a defacemask image. E.g., `sub-01_mod-T1w_defacemask.nii.gz`.

Some meta information about the acquisition MAY be provided in an additional JSON file. See Common MR metadata fields for a list of terms and their definitions. There are also some OPTIONAL JSON fields specific to anatomical scans:


| Field name                    | Definition                                   |
|:------------------------------|:---------------------------------------------|
| ContrastBolusIngredient | OPTIONAL. Active ingredient of agent.  Values MUST be one of: IODINE, GADOLINIUM, CARBON DIOXIDE, BARIUM, XENON Corresponds to DICOM Tag 0018,1048. |

### 8.3.3 Task (including resting state) imaging data

Template:
```
sub-<participant_label>/[ses-<session_label>/]
    func/
        sub-<participant_label>[_ses-<session_label>]_task-<task_label>[_acq-<label>][_rec-<label>][_run-<index>][_echo-<index>]_bold.nii[.gz]
        sub-<participant_label>[_ses-<session_label>]_task-<task_label>[_acq-<label>][_rec-<label>][_run-<index>][_echo-<index>]_sbref.nii[.gz]
```

Imaging data acquired during BOLD imaging. This includes but is not limited to task based fMRI as well as resting state fMRI (i.e. rest is treated as another task). For task based fMRI a corresponding task events file (see below) MUST be provided (please note that this file is not necessary for resting state scans).  For multiband acquisitions, one MAY also save the single-band reference image as type `sbref` (e.g. `sub-control01_task-nback_sbref.nii.gz`).

Each task has a unique label MUST only include of letters and/or numbers (other characters including spaces and underscores are not allowed). Those labels MUST be consistent across subjects and sessions.

If more than one run of the same task has been acquired a key/value pair: `_run-1`, `_run-2`, `_run-3` etc. MUST be used. If only one run was acquired the `run-<index>` can be omitted. In the context of functional imaging a run is defined as the same task, but in some cases it can mean different set of stimuli (for example randomized order) and participant responses.

The OPTIONAL `acq-<label>` key/value pair corresponds to a custom label one may use to distinguish different set of parameters used for acquiring the same task. For example this should be used when a study includes two resting state images - one single band and one multiband. In such case two files could have the following names: `sub-01_task-rest_acq-singleband_bold.nii.gz` and `sub-01_task-rest_acq-multiband_bold.nii.gz`, however the user is MAY choose any other label than `singleband` and `multiband` as long as they are consistent across subjects and sessions and consist only of the legal label characters.

Similarly the optional `rec-<label>` key/value can be used to distinguish different reconstruction algorithms (for example ones using motion correction).

Multi echo data MUST  be split into one file per echo. Each file shares the same name with the exception of the `_echo-<index>` key/value. For example:
```
sub-01/
   func/
      sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-1_bold.json
      sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-2_bold.json
      sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
      sub-01_task-cuedSGT_run-1_echo-3_bold.json
```

Please note that the `<index>` denotes the number/index (in a form of an integer) of the echo not the echo time value which needs to be stored in the field EchoTime of the separate JSON file.

Some meta information about the acquisition MUST be provided in an additional JSON file.

#### Required fields

| Field name     | Definition                                                  |
|:---------------|:------------------------------------------------------------|
| RepetitionTime | REQUIRED. The time in seconds between the beginning of an acquisition of one volume and the beginning of acquisition of the volume following it (TR). Please note that this definition includes time between scans (when no data has been acquired) in case of sparse acquisition schemes. This value needs to be consistent with the `pixdim[4]` field (after accounting for units stored in `xyzt_units` field) in the NIfTI header. This field is mutually exclusive with `VolumeTiming` and is derived from DICOM Tag 0018, 0080 and converted to seconds. |
| VolumeTiming   | REQUIRED. The time at which each volume was acquired during the acquisition. It is described using a list of times (in JSON format) referring to the onset of each volume in the BOLD series. The list must have the same length as the BOLD series, and the values must be non-negative and monotonically increasing. This field is mutually exclusive with RepetitionTime and `DelayTime`. If defined, this requires acquisition time (TA) be defined via either SliceTiming or AcquisitionDuration be defined. |
| TaskName       | REQUIRED. Name of the task. No two tasks should have the same name. Task label (`task-`)  included in the file name is derived from this field by removing all non alphanumeric (``[a-zA-Z0-9]``) characters. For example task name `faces n-back` will corresponds to task label `facesnback`.  An optional but RECOMMENDED convention is to name resting state task using labels beginning with `rest`. |


For the fields described above and in the following section, the term "Volume" refers to a reconstruction of the object being imaged (e.g., brain or part of a brain). In case of multiple channels in a coil, the term "Volume" refers to a combined image rather than an image from each coil.

#### Other RECOMMENDED metadata

##### Timing Parameters

| Field name                        | Definition                               |
|:----------------------------------|:-----------------------------------------|
| NumberOfVolumesDiscardedByScanner | RECOMMENDED. Number of volumes ("dummy scans") discarded by the scanner (as opposed to those discarded by the user post hoc) before saving the imaging file. For example, a sequence that automatically discards the first 4 volumes before saving would have this field as 4. A sequence that doesn't discard dummy scans would have this set to 0. Please note that the onsets recorded in the _event.tsv file should always refer to the beginning of the acquisition of the first volume in the corresponding imaging file - independent of the value of `NumberOfVolumesDiscardedByScanner` field. |
| NumberOfVolumesDiscardedByUser    | RECOMMENDED. Number of volumes ("dummy scans") discarded by the user before including the file in the dataset. If possible, including all of the volumes is strongly recommended. Please note that the onsets recorded in the _event.tsv file should always refer to the beginning of the acquisition of the first volume in the corresponding imaging file - independent of the value of `NumberOfVolumesDiscardedByUser` field. |
| DelayTime                         | RECOMMENDED. User specified time (in seconds) to delay the acquisition of data for the following volume. If the field is not present it is assumed to be set to zero. Corresponds to Siemens CSA header field `lDelayTimeInTR`. This field is REQUIRED for sparse sequences using the RepetitionTime field that do not have the SliceTiming field set to allowed for accurate calculation of  "acquisition time". This field is mutually exclusive with `VolumeTiming`. |
| AcquisitionDuration               | RECOMMENDED. Duration (in seconds) of volume acquisition. Corresponds to DICOM Tag 0018,9073 `Acquisition Duration`. This field is REQUIRED for sequences that are described with the `VolumeTiming` field and that not have the `SliceTiming` field set to allowed for accurate calculation of  "acquisition time". This field is mutually exclusive with `RepetitionTime`. |
| DelayAfterTrigger                 | RECOMMENDED. Duration (in seconds) from trigger delivery to scan onset. This delay is commonly caused by adjustments and loading times. This specification is entirely independent of  `NumberOfVolumesDiscardedByScanner` or `NumberOfVolumesDiscardedByUser`, as the delay precedes the acquisition. |

##### fMRI task information

| Field name      | Definition                                                 |
|:----------------|:-----------------------------------------------------------|
| Instructions    | RECOMMENDED. Text of the instructions given to participants before the scan. This is especially important in context of resting state fMRI and distinguishing between eyes open and eyes closed paradigms. |
| TaskDescription | RECOMMENDED. Longer description of the task.               |
| CogAtlasID      | RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) Task term. |
| CogPOID         | RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term. |

See [8.3.1. Common MR metadata fields](#heading=h.5u721tt1h9pe) for a list of additional terms and their definitions.


Example:
```
sub-control01/
    func/
        sub-control01_task-nback_bold.json
```

```JSON
{
   "TaskName": "N Back",
   "RepetitionTime": 0.8,
   "EchoTime": 0.03,
   "FlipAngle": 78,
   "SliceTiming": [0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6, 0.0, 0.2, 0.4, 0.6],
   "MultibandAccelerationFactor": 4,
   "ParallelReductionFactorInPlane": 2,
   "PhaseEncodingDirection": "j",
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "DeviceSerialNumber": "11035"
}
```

If this information is the same for all participants, sessions and runs it can be provided in `task-<task_label>_bold.json` (in the root directory of the dataset). However, if the information differs between subjects/runs it can be specified in the `sub-<participant_label>/func/sub-<participant_label>_task-<task_label>[_acq-<label>][_run-<index>]_bold.json` file. If both files are specified fields from the file corresponding to a particular participant, task and run takes precedence.

### 8.3.4 Diffusion imaging data
Template:
```
sub-<participant_label>/[ses-<session_label>/]
    dwi/
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_dwi.nii[.gz]
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_dwi.bval
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_dwi.bvec
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_dwi.json
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_sbref.nii[.gz]
       sub-<participant_label>[_ses-<session_label>][_acq-<label>][_run-<index>]_sbref.json
```

Diffusion-weighted imaging data acquired for that participant. The optional `acq-<label>` key/value pair corresponds to a custom label the user may use to distinguish different set of parameters. For example this should be used when a study includes two diffusion images - one single band and one multiband. In such case two files could have the following names: `sub-01_acq-singleband_dwi.nii.gz` and `sub-01_acq-multiband_dwi.nii.gz`, however the user is free to choose any other label than `singleband` and `multiband` as long as they are consistent across subjects and sessions.
For multiband acquisitions, one can also save the single-band reference image as type `sbref` (e.g. `dwi/sub-control01_sbref.nii[.gz]`)
The bvec and bval files are in the FSL format: The bvec files contain 3 rows with n space-delimited floating-point numbers (corresponding to the n volumes in the relevant NIfTI file). The first row contains the x elements, the second row contains the y elements and third row contains the z elements of a unit vector in the direction of the applied diffusion gradient, where the i-th elements in each row correspond together to the i-th volume with `[0,0,0]` for non-diffusion-weighted volumes.  Inherent to the FSL format for bvec specification is the fact that the coordinate system of the bvecs is with respect to the participant (i.e., defined by the axes of the corresponding dwi.nii file) and not  the magnet’s coordinate system, which means that any rotations applied to dwi.nii also need to be applied to the corresponding bvec file.

#### 8.3.4.1 bvec example:

```
0 0 0.021828 -0.015425 -0.70918 -0.2465
0 0 0.80242 0.22098 -0.00063106 0.1043
0 0 -0.59636 0.97516 -0.70503 -0.96351
```

The bval file contains the b-values (in s/mm<sup>2</sup>) corresponding to the volumes in the relevant NIfTI file), with 0 designating non-diffusion-weighted volumes, space-delimited.

#### 8.3.4.2 bval example:

```
0 0 2000 2000 1000 1000
```

`.bval` and `.bvec` files can be saved on any level of the directory structure and thus define those values for all sessions and/or subjects in one place (see Inheritance principle).

See Common MR metadata fields for a list of additional terms that can be included in the corresponding JSON file.

#### 8.3.4.3 JSON example:
```JSON
{
  "PhaseEncodingDirection": "j-",
  "TotalReadoutTime": 0.095
}
```

### 8.3.5 Fieldmap data

Data acquired to correct for B0 inhomogeneities can come in different forms. The current version of this standard considers four different scenarios. Please note that in all cases fieldmap data can be linked to a specific scan(s) it was acquired for by filling the IntendedFor field in the corresponding JSON file. For example:

```JSON
{
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

The IntendedFor field may contain one or more filenames with paths relative to the subject subfolder. The path needs to use forward slashes instead of backward slashes.  Here’s an example with multiple target scans:

```JSON
{
   "IntendedFor": ["ses-pre/func/sub-01_task-motor_run-1_bold.nii.gz",
                   "ses-post/func/sub-01_task-motor_run-1_bold.nii.gz"]
}
```

The IntendedFor field is optional and in case the fieldmaps do not correspond to any particular scans it does not have to be filled.

Multiple fieldmaps can be stored. In such case the `_run-1`, `_run-2` should be used. The optional `acq-<label>` key/value pair corresponds to a custom label the user may use to distinguish different set of parameters.

#### 8.3.5.1 Case 1: Phase difference image and at least one magnitude image
Template:
```
sub-<participant_label>/[ses-<session_label>/]
    fmap/
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phasediff.nii[.gz]
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phasediff.json
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude1.nii[.gz]
```

(optional)
```
sub-<participant_label>/[ses-<session_label>/]
    fmap/
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude2.nii[.gz]
```

This is a common output for build in fieldmap sequence on Siemens scanners. In this particular case the sidecar JSON file has to define the Echo Times of the two phase images used to create the difference image. `EchoTime1` corresponds to the shorter echo time and `EchoTime2` to the longer echo time. Similarly `_magnitude1` image corresponds to the shorter echo time and the OPTIONAL `_magnitude2` image to the longer echo time. For example:

```JSON
{
   "EchoTime1": 0.00600,
   "EchoTime2": 0.00746,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

#### 8.3.5.2 Case 2: Two phase images and two magnitude images
Template:
```
sub-<participant_label>/[ses-<session_label>/]
    fmap/
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phase1.nii[.gz]
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phase1.json
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phase2.nii[.gz]
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_phase2.json
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude1.nii[.gz]
        sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude2.nii[.gz]
```

Similar to the case above, but instead of a precomputed phase difference map two separate phase images are presented. The two sidecar JSON file need to specify corresponding `EchoTime` values. For example:

```JSON
{
   "EchoTime": 0.00746,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

#### 8.3.5.3 Case 3: A single, real fieldmap image (showing the field inhomogeneity in each voxel)
Template:
```
sub-<participant_label>/[ses-<session_label>/]
    fmap/
       sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_magnitude.nii[.gz]
       sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_fieldmap.nii[.gz]
       sub-<label>[_ses-<session_label>][_acq-<label>][_run-<run_index>]_fieldmap.json
```

In some cases (for example GE) the scanner software will output a precomputed fieldmap denoting the B0 inhomogeneities along with a magnitude image used for coregistration. In this case the sidecar JSON file needs to include the units of the fieldmap. The possible options are: `Hz`, `rad/s`, or `Tesla`. For example:

```JSON
{
   "Units": "rad/s",
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

#### 8.3.5.4 Case 4: Multiple phase encoded directions ("pepolar")
Template:
```
sub-<participant_label>/[ses-<session_label>/]
    fmap/
        sub-<label>[_ses-<session_label>][_acq-<label>]_dir-<dir_label>[_run-<run_index>]_epi.nii[.gz]
        sub-<label>[_ses-<session_label>][_acq-<label>]_dir-<dir_label>[_run-<run_index>]_epi.json
```

The phase-encoding polarity (PEpolar) technique combines two or more Spin Echo EPI scans with different phase encoding directions to estimate the underlying inhomogeneity/deformation map. Examples of tools using this kind of images are FSL TOPUP, AFNI 3dqwarp and SPM. In such a case, the phase encoding direction is specified in the corresponding JSON file as one of: `i`, `j`, `k`, `i-`, `j-`, `k-`. For these differentially phase encoded sequences, one also needs to specify the Total Readout Time defined as the time (in seconds) from the center of the first echo to the center of the last echo (aka "FSL definition" - see [here](https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/topup/Faq#How_do_I_know_what_phase-encode_vectors_to_put_into_my_--datain_text_file.3F) and [here](https://lcni.uoregon.edu/kb-articles/kb-0003) how to calculate it). For example

```JSON
{
   "PhaseEncodingDirection": "j-",
   "TotalReadoutTime": 0.095,
   "IntendedFor": "func/sub-01_task-motor_bold.nii.gz"
}
```

`dir_label` value can be set to arbitrary alphanumeric label (``[a-zA-Z0-9]+`` for example `LR` or `AP`) that can help users to distinguish between different files, but should not be used to infer any scanning parameters (such as phase encoding directions) of the corresponding sequence. Please rely only on the JSON file to obtain scanning parameters. _epi files can be a 3D or 4D - in the latter case all timepoints share the same scanning parameters.  To indicate which run is intended to be used with which functional or diffusion scan the IntendedFor field in the JSON file should be used.

8.4 Magnetoencephalography (MEG)
----------------------------------------

Support for MEG was developed as a BIDS Extension Proposal. Please cite the following paper when referring to this part of the standard in context of the academic literature:

> Niso Galan, J.G., Gorgolewski, K.J., Bock, E., Brooks, T.L., Flandin, G., Gramfort, A., Henson, R.N., Jas, M., Litvak, V., Moreau, J., Oostenveld, R., Schoffelen, J.-M., Tadel, F., Wexler, J., Baillet, S., 2018. [MEG-BIDS, the brain imaging data structure extended to
> magnetoencephalography](https://www.nature.com/articles/sdata2018110). Scientific Data volume 5, Article number: 180110 (2018)

### 8.4.1 MEG recording data
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_meg.<manufacturer_specific_extension>
        [sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_meg.json]
```


Unprocessed MEG data MUST be stored in the native file format of the MEG instrument with which the data was collected. With MEG-BIDS, we wish to promote the adoption of good practices in the management of scientific data. Hence, the emphasis of MEG-BIDS is not to impose a new, generic data format for the  modality, but rather to standardize the way data is stored in repositories. Further, there is currently no widely accepted standard file format for MEG, but major software applications, including free and open-source solutions for MEG data analysis provide readers of such raw files.

Some software reader may skip important metadata that is specific to MEG system manufacturers. It is therefore RECOMMENDED that users provide additional meta information extracted from the manufacturer raw data files in a sidecar JSON file. This allows for easy searching and indexing of key metadata elements without the need to parse files in proprietary data format. Other relevant files MAY be included alongside the MEG data; examples are provided below.

This template is for MEG data of any kind, including but not limited to task-based, resting-state, and noise recordings. If multiple Tasks were performed within a single Run, the task description can be set to `task-multitask`.  The _meg.json SHOULD contain details on the Tasks. Some manufacturers data storage conventions use folders which contain data files of various nature: e.g., CTF’s .ds format, or 4D/BTi. Please refer to Appendix VI for examples from a selection of MEG manufacturers.

The `proc` label is analogous to `rec` for MR and denotes a variant of a file that was a result of particular processing performed on the device. This is useful for files produced in particular by Elekta’s MaxFilter (e.g. sss, tsss, trans, quat, mc, etc.), which some installations impose to be run on raw data because of active shielding software corrections before the MEG data can actually be exploited.     

#### 8.4.1.1 Sidecar JSON document (`*_meg.json`)

Generic  fields
MUST be present:

|Field name|Definition|
|:--------------- |:---------- |
|TaskName|REQUIRED. Name of the task (for resting state use the `rest` prefix). Different Tasks SHOULD NOT have the same name. The Task label is derived from this field by removing all non alphanumeric (``[a-zA-Z0-9]``) characters.|

SHOULD be present:
For consistency between studies and institutions, we encourage users to extract the  values of these fields from the actual raw data. Whenever possible, please avoid using ad-hoc wording.

|Field name|Definition|
|:--- |:--- |
|InstitutionName|RECOMMENDED. The name of the institution in charge of the equipment that produced the composite instances.|
|InstitutionAddress|RECOMMENDED. The address of the institution in charge of the equipment that produced the composite instances.|
|Manufacturer|RECOMMENDED. Manufacturer of the MEG system (`CTF`, `Elekta/Neuromag`, `4D/BTi`, `KIT/Yokogawa`, `ITAB`, `KRISS`, `Other`). See Appendix VII with preferred names|
|ManufacturersModelName|RECOMMENDED. Manufacturer’s designation of the MEG scanner model (e.g. `CTF-275`). See Appendix VII with preferred names|
|SoftwareVersions|RECOMMENDED. Manufacturer’s designation of the acquisition software.|
|ManufacturersModelName|RECOMMENDED. Manufacturer’s designation of the MEG scanner model (e.g. `CTF-275`). See Appendix VII with preferred names|
|SoftwareVersions|RECOMMENDED. Manufacturer’s designation of the acquisition software.|
|TaskDescription|RECOMMENDED. Description of the task.|
|Instructions|RECOMMENDED. Text of the instructions given to participants before the scan. This is not only important for behavioural or cognitive tasks but also in resting state paradigms (e.g. to distinguish between eyes open and eyes closed).|
|CogAtlasID|RECOMMENDED. URL of the corresponding [Cognitive Atlas](http://www.cognitiveatlas.org/) term that describes the task (e.g. Resting State with eyes closed "[http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b](http://www.cognitiveatlas.org/term/id/trm_54e69c642d89b)")|
|CogPOID|RECOMMENDED. URL of the corresponding [CogPO](http://www.cogpo.org/) term that describes the task  (e.g. Rest "[http://wiki.cogpo.org/index.php?title=Rest](http://wiki.cogpo.org/index.php?title=Rest)")|
|DeviceSerialNumber|RECOMMENDED. The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset.|


Specific MEG fields
MUST be present:

|Field name|Definition|
|:--- |:--- |
|SamplingFrequency|REQUIRED. Sampling frequency (in Hz) of all the data in the recording, regardless of their type  (e.g., 2400)|
|PowerLineFrequency|REQUIRED. Frequency (in Hz) of the power grid at the geographical location of the MEG instrument (i.e. 50 or 60)|
|DewarPosition|REQUIRED. Position of the dewar during the MEG scan: `upright`, `supine` or `degrees` of angle from vertical: for example on CTF systems, upright=15°, supine = 90°.|
|SoftwareFilters|REQUIRED. List of temporal and/or spatial software filters applied, or ideally  key:value pairs of pre-applied software filters and their parameter values: e.g., {"SSS": {"frame": "head", "badlimit": 7}}, {"SpatialCompensation": {"GradientOrder": Order of the gradient compensation}}. Write `n/a` if no software filters applied.|
|DigitizedLandmarks|REQUIRED. Boolean ("true" or "false") value indicating whether anatomical landmark  points (i.e. fiducials) are contained within this recording.|
|DigitizedHeadPoints|REQUIRED. Boolean (`true` or `false`) value indicating whether head points outlining the scalp/face surface are contained within this recording.|


SHOULD be present

|Field name|Definition|
|:--- |:--- |
|MEGChannelCount|RECOMMENDED. Number of MEG channels (e.g. 275)|
|MEGREFChannelCount|RECOMMENDED. Number of MEG reference channels (e.g. 23). For systems without such channels (e.g. Neuromag Vectorview), `MEGREFChannelCount`=0|
|EEGChannelCount|RECOMMENDED. Number of EEG channels recorded simultaneously (e.g. 21)|
|ECOGChannelCount|RECOMMENDED. Number of ECoG channels|
|SEEGChannelCount|RECOMMENDED. Number of SEEG channels|
|EOGChannelCount|RECOMMENDED. Number of EOG channels|
|ECGChannelCount|RECOMMENDED. Number of ECG channels|
|EMGChannelCount|RECOMMENDED. Number of EMG channels|
|MiscChannelCount|RECOMMENDED. Number of miscellaneous analog channels for auxiliary  signals|
|TriggerChannelCount|RECOMMENDED. Number of channels for digital (TTL bit level) triggers|
|RecordingDuration|RECOMMENDED. Length of the recording in seconds (e.g. 3600)|
|RecordingType|RECOMMENDED. Defines whether the recording is  `continuous` or  `epoched`; this latter limited to time windows about events of interest (e.g., stimulus presentations, subject responses etc.)|
|EpochLength|RECOMMENDED. Duration of individual epochs in seconds (e.g. 1) in case of epoched data|
|ContinuousHeadLocalization|RECOMMENDED. Boolean (`true` or `false`) value indicating whether continuous head localisation was performed.|
|HeadCoilFrequency|RECOMMENDED. List of frequencies (in Hz) used by the head localisation coils (‘HLC’ in CTF systems, ‘HPI’ in Elekta, ‘COH’ in 4D/BTi) that track the subject’s head position in the MEG helmet (e.g. ``[293, 307, 314, 321]``)|
|MaxMovement|RECOMMENDED. Maximum head movement (in mm) detected during the recording, as measured by the head localisation coils (e.g., 4.8)|
|SubjectArtefactDescription|RECOMMENDED. Freeform description of the observed subject artefact and its possible cause (e.g. "Vagus Nerve Stimulator", "non-removable implant"). If this field is set to `n/a`, it will be interpreted as absence of major source of artifacts except cardiac and blinks.|
|AssociatedEmptyRoom|RECOMMENDED. Relative path in BIDS folder structure to empty-room file associated with the subject’s MEG recording. The path needs to use forward slashes instead of backward slashes (e.g. `sub-emptyroom/ses-/meg/sub-emptyroom_ses-_task-noise_run-_meg.ds`).|


Specific EEG fields (if recorded with MEG)
SHOULD be present:

|Field name|Definition|
|:--- |:--- |
|EEGPlacementScheme|OPTIONAL. Placement scheme of EEG electrodes. Either the name of a standardised placement system (e.g., "10-20") or a list of standardised electrode names (e.g. ``["Cz", "Pz"]``).|
|ManufacturersAmplifierModelName|OPTIONAL. Manufacturer’s designation of the EEG amplifier model (e.g., `Biosemi-ActiveTwo`).|
|CapManufacturer|OPTIONAL. Manufacturer of the EEG cap (e.g. `EasyCap`)|
|CapManufacturersModelName|OPTIONAL. Manufacturer’s designation of the EEG cap model (e.g., `M10`)|
|EEGReference|OPTIONAL. Description of the type of EEG reference used (e.g., `M1` for left mastoid, `average`, or `longitudinal bipolar`).|


By construct, EEG when recorded simultaneously with the same MEG system , should have the same `SamplingFrequency` as MEG. Note that if EEG is recorded with a separate amplifier, it should be stored separately under a new /eeg data type (see BEP006).

Example:

```JSON
{
   "InstitutionName": "Stanford University",
   "InstitutionAddress": "450 Serra Mall, Stanford, CA 94305-2004, USA",
   "Manufacturer": "CTF",
   "ManufacturersModelName": "CTF-275",
   "DeviceSerialNumber": "11035",
   "SoftwareVersions": "Acq 5.4.2-linux-20070507",
   "PowerLineFrequency": 60,
   "SamplingFrequency": 2400,
   "MEGChannelCount": 270,
   "MEGREFChannelCount": 26,
   "EEGChannelCount": 0,
   "EOGChannelCount": 2,
   "ECGChannelCount": 1,
   "EMGChannelCount": 0,
     "DewarPosition": "upright",
   "SoftwareFilters": {
     "SpatialCompensation": {"GradientOrder": "3rd"}
   },
   "RecordingDuration": 600,
   "RecordingType": "continuous",
   "EpochLength": 0,
   "TaskName": "rest",
   "ContinuousHeadLocalization": true,
   "HeadCoilFrequency": [1470,1530,1590],
   "DigitizedLandmarks": true,
   "DigitizedHeadPoints": true
}
```

Note that the date and time information SHOULD be stored in the Study key file (`scans.tsv`), see section 8.8. Scans.tsv. As it is indicated there, date time information MUST be expressed in the following format `YYYY-MM-DDThh:mm:ss` ([ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time format). For example: 2009-06-15T13:45:30. It does not need to be fully detailed, depending on local REB/IRB ethics board policy.

### 8.4.2 Channels description table (`*_channels.tsv`)
Template:
```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_channels.tsv]
```

This file is RECOMMENDED as it provides easily searchable information across MEG-BIDS datasets for e.g., general curation, response to queries or batch analysis. To avoid confusion, the channels SHOULD be listed in the order they appear in the MEG data file. Missing values MUST be indicated with  `n/a`.

The columns of the Channels description table stored in `*_channels.tsv` are:

MUST be present:

|Field name|Definition|
|:--- |:--- |
|name|REQUIRED. Channel name (e.g., MRT012, MEG023)|
|type|REQUIRED. Type of channel; MUST use the channel types listed below.|
|units|REQUIRED. Physical unit of the data values recorded by this channel in SI (see Appendix V: Units for allowed symbols).|

SHOULD be present:

|Field name|Definition|
|:--- |:--- |
|description|OPTIONAL. Brief free-text description of the channel, or other information of interest. See examples below.|
|sampling_frequency|OPTIONAL. Sampling rate of the channel in Hz.|
|low_cutoff|OPTIONAL. Frequencies used for the high-pass filter applied to the channel in Hz. If no high-pass filter applied, use `n/a`.|
|high_cutoff|OPTIONAL. Frequencies used for the low-pass filter applied to the channel in Hz. If no low-pass filter applied, use `n/a`. Note that hardware anti-aliasing in A/D conversion of all MEG/EEG electronics applies a low-pass filter; specify its frequency here if applicable.|
|notch|OPTIONAL. Frequencies used for the notch filter applied to the channel, in Hz. If no notch filter applied, use `n/a`.|
|software_filters|OPTIONAL. List of temporal and/or spatial software filters applied (e.g. "SSS", ``"SpatialCompensation"``). Note that parameters should be defined in the general MEG sidecar .json file. Indicate `n/a` in the absence of software filters applied.|
|status|OPTIONAL. Data quality observed on the channel ``(good/bad)``. A channel is considered `bad` if its data quality is compromised by excessive noise. Description of noise type SHOULD be provided in ``[status_description]``.|
|status_description|OPTIONAL. Freeform text description of noise or artifact affecting data quality on the channel. It is meant to explain why the channel was declared bad in ``[status]``.|


Example:

```
name type units description sampling_frequency ...
UDIO001 TRIG V analogue trigger 1200
MLC11 MEGGRADAXIAL T sensor 1st-order grad 1200
```

```
... low_cutoff high_cutoff notch software_filters status
0.1 300 0 n/a good
0 n/a 50 SSS bad
```


Restricted keyword list for field `type`

-   MEGMAG:               MEG magnetometer
-   MEGGRADAXIAL:         MEG axial gradiometer
-   MEGGRADPLANAR:        MEG planar gradiometer
-   MEGREFMAG:            MEG reference magnetometer
-   MEGREFGRADAXIAL:               MEG reference axial  gradiometer
-   MEGREFGRADPLANAR:               MEG reference planar gradiometer
-   MEGOTHER:             Any other type of MEG sensor
-   EEG:                  Electrode channel : electroencephalogram
-   ECOG:                 Electrode channel : electrocorticogram (intracranial)
-   SEEG:                 Electrode channel : stereo-electroencephalogram (intracranial)
-   DBS:                  Electrode channel : deep brain stimulation (intracranial)
-   VEOG:                 Vertical EOG (electrooculogram)
-   HEOG:                 Horizontal EOG
-   EOG:                  Generic EOG channel, if HEOG or VEOG information not available
-   ECG:                  ElectroCardioGram (heart)
-   EMG:                  ElectroMyoGram (muscle)
-   TRIG:                 System Triggers
-   AUDIO:                Audio signal
-   PD:                   Photodiode
-   EYEGAZE:              Eye Tracker gaze
-   PUPIL:                Eye Tracker pupil diameter
-   MISC:                 Miscellaneous
-   SYSCLOCK:             System time showing elapsed time since trial started
-   ADC:                  Analog to Digital input
-   DAC:                  Digital to Analog output
-   HLU:                  Measured position of head and head coils
-   FITERR:               Fit error signal from each head localization coil
-   OTHER:                Any other type of channel

Example of free text for field `description`

-   stimulus, response, vertical EOG, horizontal EOG, skin conductance, sats, intracranial, eyetracker

Example:

```
name type units description
VEOG VEOG V vertical EOG
FDI EMG V left first dorsal interosseous
UDIO001 TRIG V analog trigger signal
UADC001 AUDIO V envelope of audio signal presented to participant
```

### 8.4.3 Coordinate System JSON document (`*_coordsystem.json`)
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>][_acq-<label>]_coordsystem.json]
```

OPTIONAL. A JSON document specifying the coordinate system(s) used for the MEG, EEG, head localization coils, and anatomical landmarks.

MEG and EEG sensors:

|Field name|Description|
|:--- |:--- |
|MEGCoordinateSystem|REQUIRED. Defines the coordinate system for the MEG sensors. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  ``[MEGCoordinateSystemDescription]``.|
|MEGCoordinateUnits|REQUIRED. Units of the coordinates of   `MEGCoordinateSystem`.  MUST be `m`, `cm`, or `mm`.|
|MEGCoordinateSystemDescription|OPTIONAL. Freeform text description or link to document describing the MEG coordinate system system in detail.|
|EEGCoordinateSystem|OPTIONAL. Describes how the coordinates of the EEG sensors are to be interpreted.|
|EEGCoordinateUnits|OPTIONAL. Units of the coordinates of `EEGCoordinateSystem`.  MUST be `m`, `cm`, or `mm`.|
|EEGCoordinateSystemDescription|OPTIONAL. Freeform text description or link to document describing the EEG coordinate system system in detail.|


Head localization coils:

|Field name|Description|
|:--- |:--- |
|HeadCoilCoordinates|OPTIONAL. Key:value pairs describing head localization coil labels and their coordinates, interpreted following the `HeadCoilCoordinateSystem`,  e.g., {`NAS`: ``[12.7,21.3,13.9]``, `LPA`: ``[5.2,11.3,9.6]``, `RPA`: ``[20.2,11.3,9.1]``}. Note that coils are not always placed at locations that have a known anatomical name (e.g. for Elekta, Yokogawa systems); in that case generic labels can be  used (e.g. {`coil1`: ``[12.2,21.3,12.3]``, `coil2`: ``[6.7,12.3,8.6]``, `coil3`: ``[21.9,11.0,8.1]``} ).|
|HeadCoilCoordinateSystem|OPTIONAL. Defines the coordinate system for the coils. See Appendix VIII: preferred names of Coordinate systems. If "Other", provide definition of the coordinate system in  `HeadCoilCoordinateSystemDescription`.|
|HeadCoilCoordinateUnits|OPTIONAL. Units of the coordinates of `HeadCoilCoordinateSystem`. MUST be `m`, `cm`, or `mm`.|
|HeadCoilCoordinateSystemDescription|OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail.|


Digitized head points:

|Field name|Description|
|:--- |:--- |
|DigitizedHeadPoints|OPTIONAL. Relative path to the file containing the locations of digitized head points collected during the session (e.g., `sub-01_headshape.pos`). RECOMMENDED for all MEG systems, especially for CTF and 4D/BTi. For Elekta/Neuromag the head points will be stored in the fif file.|
|DigitizedHeadPointsCoordinateSystem|OPTIONAL. Defines the coordinate system for the digitized head points. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  `DigitizedHeadPointsCoordinateSystemDescription`.|
|DigitizedHeadPointsCoordinateUnits|OPTIONAL. Units of the coordinates of `DigitizedHeadPointsCoordinateSystem`.  MUST be `m`, `cm`, or `mm`.|
|DigitizedHeadPointsCoordinateSystemDescription|OPTIONAL. Freeform text description or link to document describing the Digitized head Points coordinate system system in detail.|


Anatomical MRI:

|Field name|Description|
|:--- |:--- |
|IntendedFor|OPTIONAL. Path or list of path relative to the subject subfolder pointing to the structural  MRI, possibly of different types if a list is specified,  to be used with the MEG recording. The path(s) need(s) to use forward slashes instead of backward slashes (e.g. `ses-/anat/sub-01_T1w.nii.gz`).|


Anatomical landmarks:

|Field name|Description|
|:--- |:--- |
|AnatomicalLandmarkCoordinates|OPTIONAL. Key:value pairs of the labels and  3-D digitized locations of anatomical landmarks, interpreted following the `AnatomicalLandmarkCoordinateSystem`,  e.g., {"NAS": ``[12.7,21.3,13.9]``, "LPA": ``[5.2,11.3,9.6]``, "RPA": ``[20.2,11.3,9.1]``}.|
|AnatomicalLandmarkCoordinateSystem|OPTIONAL. Defines the coordinate system for the anatomical landmarks. See Appendix VIII: preferred names of Coordinate systems. If `Other`, provide definition of the coordinate system in  `AnatomicalLandmarkCoordinateSystemDescription`.|
|AnatomicalLandmarkCoordinateUnits|OPTIONAL. Units of the coordinates of `AnatomicalLandmarkCoordinateSystem`.  MUST be `m`, `cm`, or  `mm`.|
|AnatomicalLandmarkCoordinateSystemDescription|OPTIONAL. Freeform text description or link to document describing the Head Coil coordinate system system in detail.|


It is also RECOMMENDED that the MRI voxel coordinates of the actual anatomical landmarks for co-registration of MEG with structural MRI are stored in the `AnatomicalLandmarkCoordinates` field in the JSON sidecar of the corresponding T1w MRI anatomical data of the subject seen in the MEG session (see section 8.3) -  for example:
`sub-01/ses-mri/anat/sub-01_ses-mri_acq-mprage_T1w.json`

In principle, these locations are those of  absolute anatomical markers. However, the marking of NAS, LPA and RPA is more ambiguous than that of e.g., AC and PC. This may result in some variability in their 3-D digitization from session to session, even for the same participant. The solution would be to use only one T1w file and populate the `AnatomicalLandmarkCoordinates` field with session-specific labels e.g., "NAS-session1": ``[127,213,139]``,"NAS-session2": ``[123,220,142]``, etc.

Fiducials information:

|Field name|Description|
|:--- |:--- |
|FiducialsDescription|OPTIONAL. A freeform text field documenting the anatomical landmarks that were used and how the head localization coils were placed relative to these. This field can describe, for instance, whether the true anatomical locations of the left and right pre-auricular points were used and digitized, or rather whether  they were defined as the intersection between the tragus and the helix (the entry of the ear canal), or any other anatomical description of selected points in the vicinity of  the ears.|


For more information on the definition of anatomical landmarks, please visit:
   [http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_define](http://www.fieldtriptoolbox.org/faq/how_are_the_lpa_and_rpa_points_defined)

For more information on typical coordinate systems for MEG-MRI
coregistration:
   [http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined), or:
   [http://neuroimage.usc.edu/brainstorm/CoordinateSystems](http://neuroimage.usc.edu/brainstorm/CoordinateSystems)

### 8.4.4 Photos of the anatomical landmarks and/or head localization coils (`*_photo.jpg`)
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>][_acq-<label>]_photo.jpg]
```

Photos of the anatomical landmarks and/or head localization coils on the subject’s head are RECOMMENDED. If the coils are not placed at the location of actual anatomical landmarks, these latter may be marked with a piece of felt-tip taped to the skin. Please note that the photos may need to be cropped or blurred to conceal identifying features prior to sharing, depending on the terms of the consent form signed by the participant.

Example of the NAS fiducial placed between the eyebrows, rather than at the actual anatomical nasion:
   `sub-0001_ses-001_acq-NAS_photo.jpg`

### 8.4.5 3-D head point /electrode locations file (`*_headshape.<manufacturer_specific_format>`)
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        [sub-<participant_label>[_ses-<label>][_acq-<label>]_headshape.<manufacturer_specific_extension>]
```

![placement of NAS fiducial](images/sub-0001_ses-001_acq-NAS_photo.jpg "placement of NAS fiducial")
This file is RECOMMENDED.

The 3-D locations of head points and/or EEG electrode locations can be digitized and stored in separate files. The `*_acq-<label>` can be used when more than one type of digitization in done for a session, for example when the head points are in a separate file from the EEG locations. These files are stored in the specific format of the 3-D digitizer’s manufacturer (see Appendix VI).

Example:

```
sub-control01
    ses-01
        sub-control01_ses-01_acq-HEAD_headshape.pos
        sub-control01_ses-01_acq-ECG_headshape.pos
```

Note that the `*_headshape` file(s) is shared by all the runs and tasks in a session. If the subject needs to be taken out of the scanner and the head-shape has to be updated, then for MEG it could be considered to be a new session.

### 8.4.6 Empty-room files (`sub-emptyroom`)
Empty-room MEG files capture the environment and system noise. Their collection is RECOMMENDED, before/during/after each session. This data is stored inside a subject folder named `sub-emptyroom`. The `session label` SHOULD be that of the date of the empty-room recording (e.g. `ses-YYYYMMDD`). The `scans.tsv` file containing the date/time of the acquisition SHOULD also be included. Hence, users will be able to retrieve the empty-room recording that best matches a particular session with a participant, based on date/time of recording.

Example:

```
sub-control01/
sub-control02/
sub-emptyroom/
    ses-20170801/
        sub-emptyroom_ses-20170801_scans.tsv
        meg/
            sub-emptyroom_ses-20170801_task-noise_meg.ds
            sub-emptyroom_ses-20170801_task-noise_meg.json
```

`TaskName` in the `*_meg.json` file should be set to "noise".

8.5 Task events
---------------

Template:
```
sub-<participant_label>/[ses-<session_label>]
    func/
        <matches>_events.tsv
        <matches>_events.json
```

Where `<matches>` corresponds to task file name. For example: `sub-control01_task-nback`. It is also possible to have a single _events.tsv file describing events for all participants and runs (see section "4.2 Inheritance rule"). As with all other tabular data, `_events` files may be accompanied by a JSON file describing the columns in detail (see Section 4.2).

The purpose of this file is to describe timing and other properties of events recorded during the scan. Events MAY be either stimuli presented to the participant or participant responses. A single event file MAY include any combination of stimuli and response events. Events MAY overlap in time. Please mind that this does not imply that only so called "event related" study designs are supported (in contract to "block" designs) - each "block of events" can be represented by an individual row in the _events.tsv file (with a long duration). Each task events file REQUIRES a corresponding task imaging data file (but a single events file MAY be shared by multiple imaging data files - see Inheritance rule). The tabular files consists of one row per event and a set of REQUIRED and OPTIONAL columns:

| Column name   | Description                                                  |
|:--------------|:-------------------------------------------------------------|
| onset         | REQUIRED. Onset (in seconds) of the event measured from the beginning of the acquisition of the first volume in the corresponding task imaging data file. If any acquired scans have been discarded before forming the imaging data file, ensure that a time of 0 corresponds to the first image stored. In other words negative numbers in "onset" are allowed. |
| duration      | REQUIRED. Duration of the event (measured from onset) in seconds. Must always be either zero or positive. A "duration" value of zero implies that the delta function or event is so short as to be effectively modeled as an impulse. |
| trial_type    | OPTIONAL. Primary categorisation of each trial to identify them as instances of the experimental conditions. For example: for a response inhibition task, it could take on values "go" and "no-go" to refer to response initiation and response inhibition experimental conditions. |
| response_time | OPTIONAL. Response time measured in seconds. A negative response time can be used to represent preemptive responses and "n/a" denotes a missed response. |
| stim_file     | OPTIONAL. Represents the location of the stimulus file (image, video, sound etc.) presented at the given onset time. There are no restrictions on the file formats of the stimuli files, but they should be stored in the /stimuli folder (under the root folder of the dataset; with optional subfolders). The values under the stim_file column correspond to a path relative to "/stimuli". For example "images/cat03.jpg" will be translated to "/stimuli/images/cat03.jpg". |
| HED           | OPTIONAL. Hierarchical Event Descriptor (HED) Tag. See Appendix III for details. |

An arbitrary number of additional columns can be added. Those allow describing other properties of events that could be later referred in modelling and hypothesis extensions of BIDS.

In case of multi-echo task run, a single `_events.tsv` file will suffice for all echoes.

Example:
```
sub-control01/
    func/
        sub-control01_task-stopsignal_events.tsv
```
```
onset duration  trial_type  response_time stim_file
1.2 0.6 go  1.435 images/red_square.jpg
5.6 0.6 stop  1.739 images/blue_square.jpg
```

References to existing databases can also be encoded using additional columns. Example 2 includes references to the Karolinska Directed Emotional Faces (KDEF) database:

Example:
```
sub-control01/
    func/
        sub-control01_task-emoface_events.tsv
```
```
onset duration  trial_type  identifier  database  response_time
1.2 0.6 afraid  AF01AFAF  kdef  1.435
5.6 0.6 angry AM01AFAN  kdef  1.739
5.6 0.6 sad AF01ANSA  kdef  1.739
```

For multi-echo files events.tsv file is applicable to all echos of particular run:
```
sub-01_task-cuedSGT_run-1_events.tsv
sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
```

8.6 Physiological and other continuous recordings
-----------------------------------------------------

Template:
sub-<participant_label>/[ses-<session_label>/]
> func/
>> <matches>[_recording-<label>]_physio.tsv.gz

and

sub-<participant_label>/[ses-<session_label>/]
> func/
>> <matches>[_recording-<label>]_physio.json

sub-<participant_label>/[ses-<session_label>/]
> func/
>> <matches>[_recording-<label>]_stim.tsv.gz

and

sub-<participant_label>/[ses-<session_label>/
> func/
>> <matches>[_recording-<label>]_stim.json

Optional: Yes

Where <matches> corresponds to task file name without the _bold.nii[.gz] suffix. For example: sub-control01_task-nback_run-1. If the same continuous recording has been used for all subjects (for example in the case where they all watched the same movie) one file can be used and placed in the root directory. For example: task-movie_stim.tsv.gz

Physiological recordings such as cardiac and respiratory signals and other continuous measures (such as parameters of a film or audio stimuli) can be specified using two files: a gzip compressed TSV file with data (without header line) and a JSON for storing start time, sampling frequency, and name of the columns from the TSV. Please note that in contrast to other TSV files this one does not include a header line. Instead the name of columns are specified in the JSON file. This is to improve compatibility with existing software (FSL PNM) as well as make support for other file formats possible in the future.  Start time should be expressed in seconds in relation to the time of start of acquisition of the first volume in the corresponding imaging file (negative values are allowed). Sampling frequency should be expressed in Hz. Recordings with different sampling frequencies and/or starting times should be stored in separate files. The following naming conventions should be used for column names:

<table>
  <tbody>
    <tr>
      <td>cardiac</td>
      <td>continuous pulse measurement</td>
    </tr>
    <tr>
      <td>respiratory</td>
      <td>continuous breathing measurement</td>
    </tr>
    <tr>
      <td>trigger</td>
      <td>continuous measurement of the scanner trigger signal</td>
    </tr>
  </tbody>
</table>

Any combination of those three can be included as well as any other stimuli related continuous variables (such as low level image properties in a video watching paradigm).

Physiological recordings (including eye tracking) should use the _physio suffix, and signals related to the stimulus should use _stim suffix. For motion parameters acquired from scanner side motion correction please use _physio suffix.

More than one continuous recording file can be included (with different sampling frequencies). In such case use different labels. For example: _recording-contrast, _recording-saturation. The full file name could then look like this: sub-control01_task-nback_run-2_recording-movie_stim.tsv.gz

For multi-echo data, physio.tsv file is applicable to all echos of particular run.
For eg:
> sub-01_task-cuedSGT_run-1_physio.tsv.gz
> sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
> sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
> sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz

### 8.6.1 Example:
sub-control01/
> func/
>> sub-control01_task-nback_physio.tsv.gz (after
decompression)

<table>
  <tbody>
    <tr>
      <td>34</td>
      <td>110</td>
      <td>0</td>
    </tr>
    <tr>
      <td>44</td>
      <td>112</td>
      <td>0</td>
    </tr>
    <tr>
      <td>23</td>
      <td>100</td>
      <td>1</td>
    </tr>
  </tbody>
</table>

sub-control01/
> func/
>> sub-control01_task-nback_physio.json

{
   "SamplingFrequency": 100.0,
   "StartTime": -22.345,
   "Columns": ["cardiac", "respiratory", "trigger"]
}

8.7 Behavioral experiments (with no MRI)
------------------------------------------------
Template:
sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_events.tsv

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_events.json

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_beh.tsv

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_beh.json

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_physio.tsv.gz

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_physio.json

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_stim.tsv.gz

sub-<participant_label>/[ses-<session_label>/]
> beh/
>> sub-<participant_label>[_ses-<session_label>]_task-<task_name>_stim.json

In addition to logs from behavioral experiments performed along imaging data acquisitions one can also include data from experiments performed outside of the scanner. The results of those experiments can be stored in the beh folder using the same formats for event timing (_events.tsv), metadata (_events.json), physiological (_physio.tsv.gz, _physio.json) and other continuous recordings (_stim.tsv.gz, _stim.json) as for tasks performed during MRI acquisitions. Additionally, events files that do not include the mandatory ‘onset’ and ‘duration’ columns can still be included, but should be labelled _beh.tsv rather than _events.tsv.

8.8 Scans file
------------------

Template:
sub-<participant_label>/[ses-<session_label>/]
> sub-<participant_label>[_ses-<session_label>]_scans.tsv

Optional: Yes

The purpose of this file is to describe timing and other properties of each imaging acquisition sequence (each run .nii[.gz] file) within one session. Each .nii[.gz] file should be described by at most one row. Relative paths to files should be used under a compulsory "filename" header.
If acquisition time is included it should be under "acq_time" header. Datetime should be expressed in the following format 2009-06-15T13:45:30 (year, month, day, hour (24h), minute, second; this is equivalent to the RFC3339 "date-time" format, time zone is always assumed as local time). For anonymization purposes all dates within one subject should be shifted by a randomly chosen (but common across all runs etc.) number of days. This way relative timing would be preserved, but chances of identifying a person based on the date and time of their scan would be decreased. Dates that are shifted for anonymization purposes should be set to a year 1900 or earlier to clearly distinguish them from unmodified data. Shifting dates is recommended, but not required.
Additional fields can include external behavioural measures relevant to the scan. For example vigilance questionnaire score administered after a resting state scan.

### 8.8.1 Example:

<table>
  <tbody>
    <tr>
      <td>filename</td>
      <td>acq_time</td>
    </tr>
    <tr>
      <td>func/sub-control01_task-nback_bold.nii.gz</td>
      <td>1877-06-15T13:45:30</td>
    </tr>
    <tr>
      <td>func/sub-control01_task-motor_bold.nii.gz</td>
      <td>1877-06-15T13:55:33</td>
    </tr>
  </tbody>
</table>

8.9 Participant file
------------------------

Template:
(single session case)
participants.tsv
participants.json
phenotype/<measurement_tool_name>.tsv
phenotype/<measurement_tool_name>.json

Optional: Yes

The purpose of this file is to describe properties of participants such as age, handedness, sex, etc. In case of single session studies this file has one compulsory column participant_id that consists of sub-<participant_label>, followed by a list of optional columns describing participants. Each participant needs to be described by one and only one row.

### 8.9.1 participants.tsv example:

<table>
  <tbody>
    <tr>
      <td>participant_id</td>
      <td>age</td>
      <td>sex</td>
      <td>group</td>
    </tr>
    <tr>
      <td>sub-control01</td>
      <td>34</td>
      <td>M</td>
      <td>control</td>
    </tr>
    <tr>
      <td>sub-control02</td>
      <td>12</td>
      <td>F</td>
      <td>control</td>
    </tr>
    <tr>
      <td>sub-patient01</td>
      <td>33</td>
      <td>F</td>
      <td>patient</td>
    </tr>
  </tbody>
</table>

If the dataset includes multiple sets of participant level measurements (for example responses from multiple questionnaires) they can be split into individual files separate from participants.tsv. Those measurements should be kept in phenotype/ folder and end with the .tsv extension. They can include arbitrary set of columns, but one of them has to be participant_id with matching sub-<participant_label>.
As with all other tabular data, those additional phenotypic information files can be accompanied by a JSON file describing the columns in detail (see Section 4.2). In addition to the column description, a section describing the measurement tool (as a whole) can be added under the name "MeasurementToolMetadata". This section consists of two keys: "Description" - a free text description of the tool, and "TermURL" a link to an entity in an ontology corresponding to this tool. For example (content of phenotype/acds_adult.json):
{
       "MeasurementToolMetadata": {
            "Description": "Adult ADHD Clinical Diagnostic Scale V1.2",
            "TermURL": "http://www.cognitiveatlas.org/task/id/trm_5586ff878155d"
       },
       "adhd_b": {
            "Description": "B. CHILDHOOD ONSET OF ADHD (PRIOR TO AGE 7)",
            "Levels": {
                  "1": "YES",
                  "2": "NO"
            }
        },
        "adhd_c_dx": {
            "Description": "As child met A, B, C, D, E and F diagnostic criteria",
            "Levels": {
                  "1": "YES",
                  "2": "NO"
            }
        },
}

Please note that in this example "MeasurementToolMetadata" includes
information about the questionnaire and "adhd_b" and "adhd_c_dx"
correspond to individual columns.

In addition to the keys available to describe columns in all tabular files (LongName, Description, Levels, Units, and TermURL) the participants.json file as well as phenotypic files can also include column descriptions with Derivative field that, when set to true, indicates that values in the corresponding column is a transformation of values from other columns (for example a summary score based on a subset of items in a questionnaire).

9 Longitudinal studies with multiple sessions (visits)
==========================================================

Multiple sessions (visits) are encoded by adding an extra layer of directories and file names in the form of ses-<session_label>. Session label can consist only of alphanumeric characters [a-zA-Z0-9] and should be consistent across subjects. If numbers are used in session labels we recommend using zero padding (for example ses-01, ses-11 instead of ses-1, ses-11). This makes results of alphabetical sorting more intuitive. Acquisition time of session can be defined in the sessions file (see below for details).

The extra session layer (at least one /ses-<session_label> subfolder) should be added for all subjects if at least one subject in the dataset has more than one session. Skipping the session layer for only some subjects in the dataset is not allowed. If a /ses-<session_label> subfolder is included as part of the directory hierarchy, then the same "ses-<session_label>" tag must also be included as part of the file names themselves.

-   sub-control01
    -  ses-predrug
        - anat
            - sub-control01_ses-predrug_T1w.nii.gz
            - sub-control01_ses\-predrug_T1w.json
            - sub-control01_ses\-predrug_T2w.nii.gz
            - sub-control01_ses\-predrug_T2w.json
        - func
            - sub-control01_ses\-predrug_task\-nback_bold.nii.gz
            - sub-control01_ses\-predrug_task\-nback_bold.json
            - sub-control01_ses\-predrug_task\-nback_events.tsv
            - sub-control01_ses\-predrug_task\-nback_cont\-physio.tsv.gz
            - sub-control01_ses\-predrug_task\-nback_cont\-physio.json
            - sub-control01_ses-predrug_task-nback_sbref.nii.gz
        - dwi
            - sub-control01_ses-predrug_dwi.nii.gz
            - sub-control01_ses-predrug_dwi.bval
            - sub-control01_ses-predrug_dwi.bvec
        - fmap
            - sub-control01_ses-predrug_phasediff.nii.gz
            - sub-control01_ses-predrug_phasediff.json
            - sub-control01_ses-predrug_magnitude1.nii.gz
        - sub-control01_ses-predrug_scans.tsv
    - ses-postdrug
        - func
            - sub-control01_ses-postdrug_task-nback_bold.nii.gz
            - sub-control01_ses-postdrug_task-nback_bold.json
            - sub-control01_ses-postdrug_task-nback_events.tsv
            - sub-control01_ses-postdrug_task-nback_cont-physio.tsv.gz
            - sub-control01_ses-postdrug_task-nback_cont-physio.json
            - sub-control01_ses-postdrug_task-nback_sbref.nii.gz
        - fmap
            - sub-control01_ses-postdrug_phasediff.nii.gz
            - sub-control01_ses-postdrug_phasediff.json
            - sub-control01_ses-postdrug_magnitude1.nii.gz
        - sub-control01_ses-postdrug_scans.tsv
    - sub-control01_sessions.tsv
- participants.tsv
- dataset_description.json
- README
- CHANGES

9.1 Sessions file
-------------------------

Template:
sub-<participant_label>/
> sub-<participant_label>_sessions.tsv

Optional: Yes

In case of multiple sessions there is an option of adding an additional participant key files describing variables changing between sessions. In such case one file per participant should be added. These files need to include compulsory "session_id" column and describe each session by one and only one row. Column names in per participant key files have to be different from group level participant key column names.

### 9.1.1 Multiple sessions example:

<table>
  <tbody>
    <tr>
      <td>session_id</td>
      <td>acq_time</td>
      <td>systolic_blood_pressure</td>
    </tr>
    <tr>
      <td>ses-predrug</td>
      <td>2009-06-15T13:45:30</td>
      <td>120</td>
    </tr>
    <tr>
      <td>ses-postdrug</td>
      <td>2009-06-16T13:45:30</td>
      <td>100</td>
    </tr>
    <tr>
      <td>ses-followup</td>
      <td>2009-06-17T13:45:30</td>
      <td>110</td>
    </tr>
  </tbody>
</table>

10 Multi-site or multi-center studies
=========================================

This version of the BIDS specification does not explicitly cover studies with data coming from multiple sites or multiple centers (such extension is planned in BIDS 2.0.0).  There are however ways to model your data without any loss in terms of metadata.

10.1 Option 1: Treat each site/center as a separate dataset.
----------------------------------------------------------------

The simplest way of dealing with multiple sites is to treat data from each site as a separate and independent BIDS dataset with a separate participants.tsv and other metadata files. This way you can feed each dataset individually to BIDS Apps and everything should just work.

10.2 Option 2: Combining sites/centers into one dataset
-----------------------------------------------------------

Alternatively you can combine data from all sites into one dataset. To identify which site each subjects comes from you can add a "site" column in the participants.tsv file indicating the source site. This solution allows you to analyze all of the subjects together in one dataset. One caveat is that subjects from all sites will have to have unique labels. To enforce that and improve readability you can use a subject label prefix identifying the site. For example sub-NUY001, sub-MIT002, sub-MPG002 etc. Remember that hyphens and underscores are not allowed in subject labels.

11 Appendix I: Contributors
=============================================

Legend (source: [https://github.com/kentcdodds/all-contributors](https://github.com/kentcdodds/all-contributors))

<table>
  <tbody>
    <tr>
      <th>Emoji</th>
      <th>Represents</th>
    </tr>
    <tr>
      <td>💬</td>
      <td>Answering Questions (on the mailing list, NeuroStars, GitHub, or in person)</td>
    </tr>
    <tr>
      <td>🐛</td>
      <td>Bug reports</td>
    </tr>
    <tr>
      <td>📝</td>
      <td>Blogposts</td>
    </tr>
    <tr>
      <td>💻 </td>
      <td>Code</td>
    </tr>
    <tr>
      <td>📖</td>
      <td>Documentation and specification</td>
    </tr>
    <tr>
      <td>🎨</td>
      <td>Design</td>
    </tr>
    <tr>
      <td>💡</td>
      <td>Examples</td>
    </tr>
    <tr>
      <td>📋</td>
      <td>Event Organizers</td>
    </tr>
    <tr>
      <td>💵 </td>
      <td>Financial Support</td>
    </tr>
    <tr>
      <td>🔍</td>
      <td>Funding/Grant Finders</td>
    </tr>
    <tr>
      <td>🤔</td>
      <td>Ideas & Planning</td>
    </tr>
    <tr>
      <td>🚇</td>
      <td>Infrastructure (Hosting, Build-Tools, etc)</td>
    </tr>
    <tr>
      <td>🔌</td>
      <td>Plugin/utility libraries</td>
    </tr>
    <tr>
      <td>👀 </td>
      <td>Reviewed Pull Requests</td>
    </tr>
    <tr>
      <td>🔧 </td>
      <td>Tools</td>
    </tr>
    <tr>
      <td>🌍</td>
      <td>Translation</td>
    </tr>
    <tr>
      <td>⚠️</td>
      <td>Tests</td>
    </tr>
    <tr>
      <td>✅ </td>
      <td>Tutorials</td>
    </tr>
    <tr>
      <td>📢 </td>
      <td>Talks</td>
    </tr>
    <tr>
      <td>📹 </td>
      <td>Videos</td>
    </tr>
  </tbody>
</table>

The following individuals have contributed to the Brain Imaging Data Structure ecosystem (in alphabetical order).
If you contributed to the BIDS ecosystem and your name is not listed,
please add it.
Stefan Appelhoff 📖💬🤔🐛💡💻
Tibor Auer 💬📖💡🔧📢
Sylvain Baillet 📖🔍
Elizabeth Bock 📖💡
Eric Bridgeford 📖🔧
Teon L. Brooks 📖💻⚠️💬👀🤔
Suyash Bhogawar 📖💡⚠️🔧💬
Vince D. Calhoun 📖
Alexander L. Cohen 🐛💻📖💬
R. Cameron Craddock 📖📢
Samir Das 📖
Alejandro de la Vega 🐛💻⚠️
Eugene P. Duff 📖
Elizabeth DuPre 📖💡
Eric A. Earl 🤔
Anders Eklund 📖📢💻
Franklin W. Feingold 📋📝✅
Guillaume Flandin 📖💻
Satrajit S. Ghosh 📖💻
Tristan Glatard 📖💻
Mathias Goncalves 💻🔧📢
Krzysztof J. Gorgolewski 📖💻💬🤔🔍📢📝💡🔍🔌
Alexandre Gramfort 📖💡
Yaroslav O. Halchenko 📖📢🔧💬🐛
Daniel A. Handwerker 📖
Michael Hanke 📖🤔🔧🐛📢
Michael P. Harms 📖⚠️🔧
Richard N. Henson 📖
Dora Hermes 📖💻✅
Katja Heuer 🔧
Chris Holdgraf 📖
International Neuroinformatics Coordinating Facility 💵📋
Mainak Jas 📖💻
David Keator 📖
James Kent 💬💻
Gregory Kiar 📖💻🎨🔧
Pamela LaMontagne 📖💡
Kevin Larcher 💬
Laura and John Arnold Foundation 💵
Xiangrui Li 📖💻
Vladimir Litvak 📖
Dan Lurie 🤔📖🔧🔌💻💬
Camille Maumet 📖
Christopher J. Markiewicz 💬📖💻
Jeremy Moreau 📖💡
Zachary Michael 📖
Michael P. Milham 💡🔍
Henk Mutsaerts 📖
National Institute of Mental Health 💵
B. Nolan Nichols 📖
Thomas E. Nichols 📖
Dylan Nielson 📖💻🔧
Guiomar Niso 📖💡📢
Robert Oostenveld 📖🔧📢💡
Dianne Patterson 📖
John Pellman 📖
Cyril Pernet 💬📖💡📋
Dmitry Petrov 📖💻
Russell A. Poldrack 📖🔍📢
Jean-Baptiste Poline 📖📢🤔🎨
Vasudev Raguram 💻🎨📖🔧
Ariel Rokem 📖
Gunnar Schaefer 📖
Jan-Mathijs Schoffelen 📖
Vanessa Sochat 📖
Francois Tadel 📖🔌💡
Roberto Toro 🔧
William Triplett 📖
Jessica A. Turner 📖
Joseph Wexler 📖💡
Gaël Varoquaux 📖
Tal Yarkoni 💻📖🤔🔍🔌👀📢🐛🎨

12 Appendix II: Licenses
============================

This section lists a number of common licenses for datasets and defines suggested abbreviations for use in the dataset metadata
specifications

<table>
  <tbody>
    <tr>
      <td>PD</td>
      <td>Public Domain</td>
      <td>No license required for any purpose; the work is not subject to copyright in any jurisdiction.</td>
    </tr>
    <tr>
      <td>PDDL</td>
      <td>Open Data Commons Public Domain Dedication and License</td>
      <td>License to assign public domain like permissions without giving up the copyright: http://opendatacommons.org/licenses/pddl/</td>
    </tr>
    <tr>
      <td>CC0</td>
      <td>Creative Commons Zero 1.0 Universal.</td>
      <td>Use this if you are a holder of copyright or database rights, and you wish to waive all your interests in your work worldwide: https://creativecommons.org/about/cc0</td>
    </tr>
  </tbody>
</table>

13 Appendix III: Hierarchical Event Descriptor (HED) Tags
=============================================================

Each event can be assigned one or more Hierarchical Event Descriptor (HED) Tag (see [https://github.com/BigEEGConsortium/HED/wiki/HED-Schema](https://github.com/BigEEGConsortium/HED-schema/wiki/HED-Schema) for more details) under the optional HED column.
HED is a controlled vocabulary of terms describing events in a behavioural paradigm. It was originally developed with EEG in mind, but is applicable to all behavioural experiments. Each level of the hierarchical tags are delimited with a forward slash ("/"). Multiple tags are delimited with a comma. Parentheses (brackets) group tags and enable specification of multiple items and their attributes in a single HED string (see section 2.4 in HED Tagging Strategy Guide - [http://www.hedtags.org/downloads/HED%20Tagging%20Strategy%20Guide.pdf](http://www.hedtags.org/downloads/HED%20Tagging%20Strategy%20Guide.pdf)). For more information about HED and tools available to validate and match HED strings, please visit [www.hedtags.org](http://www.hedtags.org).

Since dedicated fields already exist for the overall task classification (CogAtlasID and CogPOID) in the sidecar JSON files HED
tags from the Paradigm subcategory should not be used to annotate
events.

13.1 Example:
---------------------

sub-control01/
> func/
>> sub-control01_task-emoface_events.tsv

<table>
  <tbody>
    <tr>
      <td>onset</td>
      <td>duration</td>
      <td>trial_type</td>
      <td>HED</td>
    </tr>
    <tr>
      <td>1.2</td>
      <td>0.6</td>
      <td>fixationCross</td>
      <td>Event/Category/Experimental stimulus, Event/Label/CrossFix, Event/Description/A cross appears at screen center to serve as a fixation point, Sensory presentation/Visual, Item/Object/2D Shape/Cross, Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen, Attribute/Location/Screen/Center</td>
    </tr>
    <tr>
      <td>5.6</td>
      <td>0.008</td>
      <td>target</td>
      <td>Event/Label/Target image, Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed., Event/Category/Experimental stimulus, (Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target, Sensory presentation/Visual/Rendering type/Screen/2D), (Item/Natural scene/Arial/Satellite, Sensory presentation/Visual/Rendering type/Screen/2D)</td>
    </tr>
    <tr>
      <td>500</td>
      <td>0.008</td>
      <td>nontarget</td>
      <td>Event/Label/Non-target image, Event/Description/A non-target image is displayed for about 8 milliseconds, Event/Category/Experimental stimulus, (Item/Natural scene/Arial/Satellite, Participant/Effect/Cognitive/Expected/Non-target, Sensory presentation/Visual/Rendering type/Screen/2D), Attribute/Onset</td>
    </tr>
  </tbody>
</table>

Alternatively if the same HED tags apply to a group of events with the same trial_type they can be specified in the corresponding data dictionary (_events.json file) using the following syntax:

13.2 Example:
---------------------

{
       "trial_type": {
        "HED": {
         "fixationCross": "Event/Category/Experimental stimulus, Event/Label/CrossFix, Event/Description/A cross appears at screen center to serve as a fixation point, Sensory presentation/Visual, Item/Object/2D Shape/Cross, Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen, Attribute/Location/Screen/Center",
         "target": "Event/Label/Target image, Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed., Event/Category/Experimental stimulus, (Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target, Sensory presentation/Visual/Rendering type/Screen/2D), (Item/Natural scene/Arial/Satellite, Sensory presentation/Visual/Rendering type/Screen/2D)",
         "nontarget": "Event/Label/Non-target image, Event/Description/A non-target image is displayed for about 8 milliseconds, Event/Category/Experimental stimulus, (Item/Natural scene/Arial/Satellite, Participant/Effect/Cognitive/Expected/Non-target, Sensory presentation/Visual/Rendering type/Screen/2D), Attribute/Onset"
        }
       }
}

14 Appendix IV: Entity table
====================================

This section compiles the entities (key-value pairs) described throughout this specification, and establishes a common order within a filename. For example, if a file has an acquisition and reconstruction label, the acquisition entity must precede the reconstruction entity. Required and optional entities for a given file type are denoted. Entity formats indicate whether the value is alphanumeric ("<label>") or numeric ("<index>").

<table>
  <tbody>
    <tr>
      <td>Entity</td>
      <td>Format</td>
      <td>anat (T1w T2w T1rho T1map T2map T2star FLAIR FLASH PD PDmap PDT2 inplaneT1 inplaneT2 angio)</td>
      <td>anat (defacemask)</td>
      <td>func (bold sbref events)</td>
      <td>func (physio stim)</td>
      <td>dwi (dwi bvec bval)</td>
      <td>fmap (phasediff phase1 phase2 magnitude1 magnitude2 magnitude fieldmap)</td>
      <td>fmap (epi)</td>
      <td>beh (events stim physio)</td>
      <td>meg (meg channels)</td>
      <td>meg (photo coordsystem headshape)</td>
    </tr>
    <tr>
      <td>Subject</td>
      <td>sub-<label></td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
    </tr>
    <tr>
    <tr>
      <td>Session</td>
      <td>ses-<label></td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
    </tr>
    <tr>
      <td>Task</td>
      <td>task-<label></td>
      <td></td>
      <td></td>
      <td>Required</td>
      <td>Required</td>
      <td></td>
      <td></td>
      <td></td>
      <td>Required</td>
      <td>Required</td>
      <td>Required</td>
    </tr>
    <tr>
      <td>Acquisition</td>
      <td>acq-<label></td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td></td>
      <td>Optional</td>
      <td>Optional</td>
    </tr>
    <tr>
      <td>Contrast Enhancing Agent</td>
      <td>ce-<label></td>
      <td>Optional</td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Reconstruction</td>
      <td>rec-<label></td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Phase-Encoding Direction</td>
      <td>dir-<label></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Required</td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Run</td>
      <td>run-<index></td>
      <td></td>
      <td></td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td>Optional</td>
      <td></td>
      <td>Optional</td>
      <td>Optional</td>
    </tr>
    <tr>
      <td>Corresponding modality</td>
      <td>mod-<label></td>
      <td></td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Echo</td>
      <td>echo-<index></td>
      <td></td>
      <td></td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Recording</td>
      <td>recording-<label></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
    </tr>
    <tr>
      <td>Processed (on device)</td>
      <td>proc-<label></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Optional</td>
      <td></td>
      <td></td>
      <td></td>
      <td></td>
      <td>Optional</td>
      <td>Optional</td>
    </tr>
  </tbody>
</table>

15 Appendix V: Units
======================================

Following the International System of Units (SI, abbreviated from the French Système international (d'unités))

<table>
  <tbody>
    <tr>
      <th>Unit name</th>
      <th>Unit symbol</th>
      <th>Quantity name</th>
    </tr>
    <tr>
      <td>metre</td>
      <td>m</td>
      <td>length</td>
    </tr>
    <tr>
      <td>kilogram</td>
      <td>kg</td>
      <td>mass</td>
    </tr>
    <tr>
      <td>second</td>
      <td>s</td>
      <td>time</td>
    </tr>
    <tr>
      <td>ampere</td>
      <td>A</td>
      <td>electric current</td>
    </tr>
    <tr>
      <td>kelvin</td>
      <td>K</td>
      <td>thermodynamic temperature</td>
    </tr>
    <tr>
      <td>mole</td>
      <td>mol</td>
      <td>amount of substance</td>
    </tr>
    <tr>
      <td>candela</td>
      <td>cd</td>
      <td>luminous intensity</td>
    </tr>
    <tr>
      <td>radian</td>
      <td>rad</td>
      <td>angle</td>
    </tr>
    <tr>
      <td>steradian</td>
      <td>sr</td>
      <td>solid angle</td>
    </tr>
    <tr>
      <td>hertz</td>
      <td>Hz</td>
      <td>frequency</td>
    </tr>
    <tr>
      <td>newton</td>
      <td>N</td>
      <td>force, weight</td>
    </tr>
    <tr>
      <td>pascal</td>
      <td>Pa</td>
      <td>pressure, stress</td>
    </tr>
    <tr>
      <td>joule</td>
      <td>J</td>
      <td>energy, work, heat</td>
    </tr>
    <tr>
      <td>watt</td>
      <td>W</td>
      <td>power, radiant flux</td>
    </tr>
    <tr>
      <td>coulomb</td>
      <td>C</td>
      <td>electric charge or quantity of electricity</td>
    </tr>
    <tr>
      <td>volt</td>
      <td>V</td>
      <td>voltage (electrical potential), emf</td>
    </tr>
    <tr>
      <td>farad</td>
      <td>F</td>
      <td>capacitance</td>
    </tr>
    <tr>
      <td>ohm</td>
      <td>Ω</td>
      <td>resistance, impedance, reactance</td>
    </tr>
    <tr>
      <td>siemens</td>
      <td>S</td>
      <td>electrical conductance</td>
    </tr>
    <tr>
      <td>weber</td>
      <td>Wb</td>
      <td>magnetic flux</td>
    </tr>
    <tr>
      <td>tesla</td>
      <td>T</td>
      <td>magnetic flux density</td>
    </tr>
    <tr>
      <td>henry</td>
      <td>H</td>
      <td>inductance</td>
    </tr>
    <tr>
      <td>degree Celsius</td>
      <td>°C</td>
      <td>temperature relative to 273.15 K</td>
    </tr>
    <tr>
      <td>lumen</td>
      <td>lm</td>
      <td>luminous flux</td>
    </tr>
    <tr>
      <td>lux</td>
      <td>lx</td>
      <td>illuminance</td>
    </tr>
    <tr>
      <td>becquerel</td>
      <td>Bq</td>
      <td>radioactivity (decays per unit time)</td>
    </tr>
    <tr>
      <td>gray</td>
      <td>Gy</td>
      <td>absorbed dose (of ionizing radiation)</td>
    </tr>
    <tr>
      <td>sievert</td>
      <td>Sv</td>
      <td>equivalent dose (of ionizing radiation)</td>
    </tr>
    <tr>
      <td>katal</td>
      <td>kat</td>
      <td>catalytic activity</td>
    </tr>
  </tbody>
</table>

Prefixes

Multiples

<table>
  <tbody>
    <tr>
      <th>Prefix name</th>
      <th>Prefix symbol</th>
      <th>Factor</th>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Deca-">deca</a></p></td>
      <td>da</td>
      <td>10<sup>1</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Hecto-">hecto</a></p></td>
      <td>h</td>
      <td>10<sup>2</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Kilo-">kilo</a></p></td>
      <td>k</td>
      <td>10<sup>3</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Mega-">mega</a></p></td>
      <td>M</td>
      <td>10<sup>6</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Giga-">giga</a></p></td>
      <td>G</td>
      <td>10<sup>9</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Tera-">tera</a></p></td>
      <td>T</td>
      <td>10<sup>12</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Peta-">peta</a></p></td>
      <td>P</td>
      <td>10<sup>15</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Exa-">exa</a></p></td>
      <td>E</td>
      <td>10<sup>18</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Zetta-">zetta</a></p></td>
      <td>Z</td>
      <td>10<sup>21</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Yotta-">yotta</a></p></td>
      <td>Y</td>
      <td>10<sup>24</sup></td>
    </tr>
  </tbody>
</table>

Submultiples

<table>
  <tbody>
    <tr>
      <th>Prefix name</th>
      <th>Prefix symbol</th>
      <th>Factor</th>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Deci-">deci</a></p></td>
      <td>d</td>
      <td>10<sup>-1</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Centi-">centi</a></p></td>
      <td>c</td>
      <td>10<sup>-2</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Milli-">milli</a></p></td>
      <td>m</td>
      <td>10<sup>-3</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Micro-">micro</a></p></td>
      <td>μ</td>
      <td>10<sup>-6</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Nano-">nano</a></p></td>
      <td>n</td>
      <td>10<sup>-9</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Pico-">pico</a></p></td>
      <td>p</td>
      <td>10<sup>-12</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Femto-">femto</a></p></td>
      <td>f</td>
      <td>10<sup>-15</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Atto-">atto</a></p></td>
      <td>a</td>
      <td>10<sup>-18</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Zepto-">zepto</a></p></td>
      <td>z</td>
      <td>10<sup>-21</sup></td>
    </tr>
    <tr>
      <td><p><a href="https://www.wikiwand.com/en/Yocto-">yocto</a></p></td>
      <td>y</td>
      <td>10<sup>-24</sup></td>
    </tr>
  </tbody>
</table>

16 Appendix  VI: MEG file formats
====================================

Each MEG system brand has specific file organization and data formats.
RECOMMENDED values for [manufacturer_specific_extensions]:
-   ctf = CTF (folder with .ds extension)
-   fif = Neuromag / Elekta / MEGIN  and BabyMEG (file with extension .fif)
-   4d = BTi / 4D Neuroimaging (folder containing multiple files without extensions)
-   kit = KIT / Yokogawa / Ricoh (file with extension .sqd, .con, .raw, .ave or .mrk)
-   kdf = KRISS (file with extension .kdf)
-   itab = Chieti system (file with extension .raw and .mhd)

Below are specifications for each system brand.

16.1 CTF
--------------------------

Each experimental run with a CTF system yields a folder with a .ds extension, containing several files. The (optional) digitized positions of the head points are usually stored in a separate .pos file, not necessarily within the .ds folder.

-   [sub-<participant_label>[_ses-<label>]_headshape.pos]
-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.ds>

CTF’s data storage is therefore via directories containing multiple files. The files contained within a .ds directory are named such that they match the parent directory, but conserve the original file extension (e.g., .meg4, .res4, etc.). The renaming of CTF datasets SHOULD be done using the CTF newDs command-line application.

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_scans.tsv
>> meg/
>>> sub-control01_ses-001_coordsystem.json
>>> sub-control01_ses-001_headshape.pos
>>> sub-control01_ses-001_task-rest_run-01_meg.ds
>>> sub-control01_ses-001_task-rest_run-01_meg.json
>>> sub-control01_ses-001_task-rest_run-01_channels.tsv

To learn more about  CTF’s data organization: [http://www.fieldtriptoolbox.org/getting_started/ctf](http://www.fieldtriptoolbox.org/getting_started/ctf)

16.2 Neuromag/Elekta/MEGIN
------------------------------------------------------------

Neuromag/Elekta/MEGIN data and Tristan Technologies BabyMEG data is stored with file extension .fif. The digitized positions of the head points are saved inside the fif file along with the MEG data, with typically no \*_headshape file.

-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.fif

Note that we do not provide specific specifications for cross-talk and fine-calibration matrix files in the present MEG-BIDS version.

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_scans.tsv
>> meg/
>>> sub-control01_ses-001_coordsystem.json
>>> sub-control01_ses-001_task-rest_run-01_meg.fif
>>> sub-control01_ses-001_task-rest_run-01_meg.json
>>> sub-control01_ses-001_task-rest_run-01_channels.tsv

After applying the MaxFilter pre-processing tool, files should be renamed with the corresponding label (e.g. proc-sss) and placed into a "derivatives" subfolder.

Example:
> sub-control01_ses-001_task-rest_run-01_proc-sss_meg.fif
> sub-control01_ses-001_task-rest_run-01_proc-sss_meg.json

In the case of data runs exceeding 2Gb, the data is stored in two separate files:
> sub-control01_ses-001_task-rest_run-01_meg.fif
> sub-control01_ses-001_task-rest_run-01_meg-1.fif

Each of these two files has a pointer to the next file. In some software applications, like MNE, one can simply specify the name of the first file, and data will be read in both files via this pointer. For this reason, it is RECOMMENDED to rename and write back the file once read, to avoid the persistence of a pointer associated with the old file name.

Naming convention:
> sub-control01_ses-001_task-rest_run-01_part-01_meg.fif
> sub-control01_ses-001_task-rest_run-01_part-02_meg.fif

More about the Neuromag/Elekta/MEGIN data organization at:
[http://www.fieldtriptoolbox.org/getting_started/neuromag](http://www.fieldtriptoolbox.org/getting_started/neuromag)
And BabyMEG :
[http://www.fieldtriptoolbox.org/getting_started/babysquid](http://www.fieldtriptoolbox.org/getting_started/babysquid)

16.3 BTi/4D neuroimaging
------------------------------------------

Each experimental run on a 4D neuroimaging//BTi system results in a folder containing multiple files without extensions.

-   [sub-<participant_label>[_ses-<label>]_headshape.pos]
-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg>

One SHOULD rename/create a father run specific directory and keep the original files for each run inside (e.g. "c,rfhp0.1Hz", "config" and "hs_file").

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_scans.tsv
>> meg/
>>> sub-control01_ses-001_coordsystem.json
>>> sub-control01_ses-001_headshape.pos
>>> sub-control01_ses-001_task-rest_run-01_meg
>>> sub-control01_ses-001_task-rest_run-01_meg.json
>>> sub-control01_ses-001_task-rest_run-01_channels.tsv

Where:
> sub-control01_ses-001_task-rest_run-01_meg/
>> config
>> hs_file
>> e,rfhp1.0Hz.COH
>> c,rfDC

More about the 4D neuroimaging/BTi data organization at: [http://www.fieldtriptoolbox.org/getting_started/bti](http://www.fieldtriptoolbox.org/getting_started/bti)

16.4 KIT/Yokogawa/Ricoh
---------------------------------------------------------

Each experimental run on a KIT/Yokogawa/Ricoh system yields a raw (\*.sqd, \*.con) file with its associated marker coil file (\*.mrk), which contains coil positions in the acquisition system’s native space. Head points and marker points in head space are acquired using third-party hardware. One SHOULD rename/create a father run specific directory and keep the original files for each run inside.

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_scans.tsv
>> meg/
>>> sub-control01_ses-001_coordsystem.json
>>> sub-control01_ses-001_headshape.txt
>>> sub-control01_ses-001_task-rest_run-01_meg
>>> sub-control01_ses-001_task-rest_run-01_meg.json
>>> sub-control01_ses-001_task-rest_run-01_channels.tsv

Where:
> sub-control01_ses-001_task-rest_run-01_meg/
>> sub-control01_ses-001_task-rest_run-01_markers.<mrk,sqd>
>> sub-control01_ses-001_task-rest_run-01_meg.<con,sqd>

More about the KIT/Yokogawa/Ricoh data organization at: [http://www.fieldtriptoolbox.org/getting_started/yokogawa](http://www.fieldtriptoolbox.org/getting_started/yokogawa)

16.5 KRISS
--------------------------

Each experimental run on the KRISS system produces a file with extension .kdf. Additional files can be available in the same folder: the digitized positions of the head points (_digitizer.txt), the position of the center of the MEG coils (.chn) and the event markers (.trg).
-   [sub-<participant_label>[_ses-<label>]_headshape.txt]
-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.kdf
-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.chn
-   sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.trg

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_scans.tsv
>> meg/
>>> sub-control01_ses-001_coordsystem.json
>>> sub-control01_ses-001_headshape.txt
>>> sub-control01_ses-001_task-rest_run-01_meg
>>> sub-control01_ses-001_task-rest_run-01_meg.json
>>> sub-control01_ses-001_task-rest_run-01_channels.tsv

Where:
> sub-control01_ses-001_task-rest_run-01_meg/
>> sub-control01_ses-001_task-rest_run-01_meg.chn
>> sub-control01_ses-001_task-rest_run-01_meg.kdf
>> sub-control01_ses-001_task-rest_run-01_meg.trg

16.6 ITAB
-----------------

Each experimental run on a ITAB-ARGOS153 system yields a raw (\*.raw) data file plus an associated binary header file (\*.mhd). The raw data file has an ASCII header that contains detailed information about the data acquisition system, followed by binary data. The associated binary header file contains part of the information from the ASCII header, specifically the one needed to process data, plus other information on offline preprocessing performed after data acquisition (e.g., sensor position relative to subject’s head, head markers, stimulus information). One should rename/create a father run specific directory and keep the original files for each run inside.

Example:
sub-control01/
> ses-001/
>> sub-control01_ses-001_coordsystem.json
>> sub-control01_ses-001_headshape.txt
>> sub-control01_ses-001_task-rest_run-01_meg
>> sub-control01_ses-001_task-rest_run-01_meg.json
>> sub-control01_ses-001_task-rest_run-01_channels.tsv

Where:
> sub-control01_ses-001_task-rest_run-01_meg/
>> sub-control01_ses-001_task-rest_run-01_meg.raw
>> sub-control01_ses-001_task-rest_run-01_meg.raw.mhd

16.7 Aalto MEG–MRI
------------------------------------

For stand-alone MEG data, the Aalto hybrid device uses the standard .fif data format and follows the conventions of Elekta/Neuromag as described above in section 5.2. The .fif files may contain unreconstructed MRI data. The inclusion of MRI data and information for accurate reconstruction will be fully standardized at a later stage.

17 Appendix VII: preferred names of MEG systems
==================================================================

Restricted keywords for Manufacturer field in the \*meg.json file:

-   CTF
-   [Elekta/Neuromag](https://docs.google.com/document/d/1FWex_kSPWVh_f4rKgd5rxJmxlboAPtQlmBc1gyZlRZM/edit#heading=h.a7ggx48p7aaf)
-   [4D/BTi](https://docs.google.com/document/d/1FWex_kSPWVh_f4rKgd5rxJmxlboAPtQlmBc1gyZlRZM/edit#heading=h.gy0kbzisg1f1)
-   [KIT/Yokogawa/Ricoh](https://docs.google.com/document/d/1FWex_kSPWVh_f4rKgd5rxJmxlboAPtQlmBc1gyZlRZM/edit#heading=h.2gmmxawyna7r)
-   KRISS
-   [ITAB](https://docs.google.com/document/d/1FWex_kSPWVh_f4rKgd5rxJmxlboAPtQlmBc1gyZlRZM/edit#heading=h.58whib3oq56y)
-   Aalto/MEG–MRI
-   Other

Restricted keywords for ManufacturersModelName field in the \*meg.json file:

<table>
  <tbody>
    <tr>
      <th>System Model Name</th>
      <th>Manufacturer</th>
      <th>Details</th>
    </tr>
    <tr>
      <td>CTF-64</td>
      <td>CTF</td>
      <td></td>
    </tr>
    <tr>
      <td>CTF-151</td>
      <td>CTF</td>
      <td>https://www.ctf.com/products</td>
    </tr>
    <tr>
      <td>CTF-275</td>
      <td>CTF</td>
      <td>CTF-275: OMEGA 2000</td>
    </tr>
    <tr>
      <td>Neuromag-122</td>
      <td>Elekta/Neuromag</td>
      <td></td>
    </tr>
    <tr>
      <td>ElektaVectorview</td>
      <td>Elekta/Neuromag</td>
      <td>102 magnetometers + 204 planar gradiometers</td>
    </tr>
    <tr>
      <td>ElektaTRIUX</td>
      <td>Elekta/Neuromag</td>
      <td>https://www.elekta.com/diagnostic-solutions/</td>
    </tr>
    <tr>
      <td>4D-Magnes-WH2500</td>
      <td>4D/BTi</td>
      <td></td>
    </tr>
    <tr>
      <td>4D-Magnes-WH3600</td>
      <td>4D/BTi</td>
      <td></td>
    </tr>
    <tr>
      <td>KIT-157</td>
      <td>KIT/Yokogawa</td>
      <td></td>
    </tr>
    <tr>
      <td>KIT-160</td>
      <td>KIT/Yokogawa</td>
      <td></td>
    </tr>
    <tr>
      <td>KIT-208</td>
      <td>KIT/Yokogawa</td>
      <td></td>
    </tr>
    <tr>
      <td>ITAB-ARGOS153</td>
      <td>ITAB</td>
      <td></td>
    </tr>
    <tr>
      <td>Aalto-MEG-MRI-YYYY/MM</td>
      <td>Aalto/MEG–MRI</td>
      <td>YYYY-MM (year, month; or major version)</td>
    </tr>
  </tbody>
</table>

18 Appendix VIII: preferred names of Coordinate systems
==========================================================================

To interpret a coordinate (x, y, z), it is required that you know relative to which origin the coordinates are expressed, you have to know the interpretation of the three axes, and you have to know the units in which the numbers are expressed. This information is sometimes called the coordinate system.

These letters help describe the coordinate system definition:

A/P means anterior/posterior
L/R means left/right
S/I means superior/inferior

For example: RAS means that the first dimension (X) points towards the right hand side of the head, the second dimension (Y) points towards the Anterior aspect of the head, and the third dimension (Z) points towards the top of the head.

Besides coordinate systems, defined by their origin and direction of the axes, BIDS defines "spaces" as an artificial frame of reference, created to describe different anatomies in a unifying manner (see e.g. [https://doi.org/10.1016/j.neuroimage.2012.01.024](https://www.sciencedirect.com/science/article/pii/S1053811912000419?via%3Dihub)). The "space" and all coordinates expressed in this space are by design a transformation of the real world geometry, and nearly always different from the individual subject space that it stems from. An example is the Talairach-Tournoux space, which is constructed by piecewise linear scaling of an individual's brain to that of the Talairach-Tournoux 1988 atlas. In the Talairach-Tournoux space, the origin of the coordinate system is at the AC and units are expressed in mm.

The coordinate systems below all relate to neuroscience and therefore to the head or brain coordinates. Please be aware that all data acquisition starts with "device coordinates" (scanner), which does not have to be identical to the initial "file format coordinates" (DICOM), which are again different from the "head" coordinates (e.g. NIFTI). Not only do device coordinate vary between hardware manufacturers, but also the head coordinates differ, mostly due to different conventions used in specific software packages developed by different (commercial or academic) groups.

MEG specific Coordinate Systems
---------------------------------------

The first two pieces of information (origin, orientation) are specified in XXXCoordinateSystem, the units are specified in XXXCoordinateSystemUnits.

Restricted keywords for the XXXCoordinateSystem field in the coordinatesystem.json file for MEG datasets:

-   CTF:                        ALS orientation and the origin between the ears
-   ElektaNeuromag:        RAS orientation and the origin between the ears
-   4DBti:                ALS orientation and the origin between the ears
-   KitYokogawa:        ALS orientation and the origin between the ears
-   ChietiItab:                RAS orientation and the origin between the ears
-   Other:                Use this for other coordinate systems and specify further details in the XXXCoordinateSystemDescription field

Note that the short descriptions above do not capture all details,  there are detailed  descriptions of these  coordinate systems on the FieldTrip toolbox web page:
[http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)

EEG specific Coordinate Systems
---------------------------------------

The first two pieces of information (origin, orientation) are specified in XXXCoordinateSystem, the units are specified in XXXCoordinateSystemUnits.

Restricted keywords for the XXXCoordinateSystem field in the coordsystem.json file for EEG  datasets:

-   BESA:         Although natively this is a spherical coordinate system, the electrode positions should be expressed in Cartesian coordinates, with a RAS orientation. The X axis is the T8-T7 line, positive at T8. The Y axis is the Oz-Fpz line, positive at Fpz. The origin of the sphere fitted to the electrodes is approximately 4 cm above the point between the ears.
-   Captrak:        RAS orientation and the origin between the ears

Note that the short descriptions above do not capture all details, There are detailed extensive descriptions of these EEG coordinate systems on the FieldTrip toolbox web page and on the BESA wiki:
[http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)
[http://wiki.besa.de/index.php?title=Electrodes_and_Surface_Locations\#Coordinate_systems](http://wiki.besa.de/index.php?title=Electrodes_and_Surface_Locations#Coordinate_systems
)

iEEG specific Coordinate Systems
--------------------------------------


Template based Coordinate System Spaces
-----------------------------------------------

The transformation of the real world geometry to an artificial frame of reference is described in XXXCoordinateSystem. Unless otherwise specified below, the origin is at the AC and the orientation of the axes is RAS. Unless specified explicitly in the sidecar file in the XXCoordinateSystemUnits field, the units are assumed to be mm.

<table>
  <tbody>
    <tr>
      <td>MNI152Lin</td>
      <td>Also known as ICBM (version with linear coregistration)
      http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152Lin</td>
    </tr>
    <tr>
      <td>MNI152NLin6[Sym|Asym]</td>
      <td>Also known as ICBM 6th generation (non-linear coregistration). Used by SPM99 - SPM8 and FSL (MNI152NLin6Sym).
      http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin6</td>
    </tr>
    <tr>
      <td>MNI152NLin2009[a-c][Sym|Asym]</td>
      <td>Also known as ICBM (non-linear coregistration with 40 iterations, released in 2009). It comes in either three different flavours each in symmetric or asymmetric version.
      http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009</td>
    </tr>
    <tr>
      <td>MNIColin27</td>
      <td>Average of 27 T1 scans of a single subject
      http://www.bic.mni.mcgill.ca/ServicesAtlases/Colin27Highres</td>
    </tr>
    <tr>
      <td>MNI305</td>
      <td>Also known as avg305.</td>
    </tr>
    <tr>
     <td>NIHPD</td>
     <td>Pediatric templates generated from the NIHPD sample.
     Available for different age groups (4.5–18.5 y.o., 4.5–8.5 y.o., 7–11 y.o., 7.5–13.5 y.o., 10–14 y.o., 13–18.5 y.o. This template also comes in either -symmetric or -asymmetric flavor.
     http://www.bic.mni.mcgill.ca/ServicesAtlases/NIHPD-obj1</td>
   </tr>
   <tr>
     <td>Talairach</td>
     <td>Piecewise linear scaling of the brain is implemented as described in TT88. http://www.talairach.org/</td>
   </tr>
   <tr>
     <td>OASIS30AntsOASISAnts</td>
     <td>https://figshare.com/articles/ANTs_ANTsR_Brain_Templates/915436</td>
   </tr>
   <tr>
     <td>OASIS30Atropos</td>
     <td>http://www.mindboggle.info/data.html</td>
   </tr>
   <tr>
     <td>ICBM452AirSpace</td>
     <td>Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" with "linear transforms of the subjects into the atlas space using a 12-parameter affine transformation"
     http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml</td>
   </tr>
   <tr>
     <td>ICBM452Warp5Space</td>
     <td>Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" "based on a 5th order polynomial transformation into the atlas space"
     http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml</td>
   </tr>
   <tr>
     <td>IXI549Space</td>
     <td>Reference space defined by the average of the "549 [...] subjects from the IXI dataset" linearly transformed to ICBM MNI 452.Used by SPM12.
     http://www.brain-development.org/</td>
   </tr>
   <tr>
     <td>fsaverage[3|4|5|6|sym]</td>
     <td>Images were sampled to the FreeSurfer surface reconstructed from the subject’s T1w image, and registered to an fsaverage template</td>
   </tr>
   <tr>
     <td>UNCInfant[0|1|2]V[21|22|23]</td>
     <td>Infant Brain Atlases from Neonates to 1- and 2-year-olds. https://www.nitrc.org/projects/pediatricatlas</td>
   </tr>
  </tbody>
</table>

------------------------------------------------------------------------

<div>

<a name="footnote1">1</a> Note that to make the display clearer, the second row does contain two successive tabs, which should not happen in an actual BIDS tsv file.

</div>

<div>

<a name="footnote2">2</a> Storing actual source files with the data
is preferred over links to external source repositories to maximize long
term preservation (which would suffer if an external repository would
not be available anymore).]{.c35 .c44 .c30}

</div>

<div>

<a name="footnote3">3</a> Conveniently, for Siemens’ data, this value is easily obtained as 1/[BWPPPE * ReconMatrixPE], where BWPPPE is the "BandwidthPerPixelPhaseEncode in DICOM tag (0019,1028) and  ReconMatrixPE is the size of the actual reconstructed data in the phase direction (which is NOT reflected in a single DICOM tag for all possible aforementioned scan manipulations). See [here](https://lcni.uoregon.edu/kb-articles/kb-0003) and [here](https://github.com/neurolabusc/dcm_qa/tree/master/In/TotalReadoutTime)

</div>

<div>

<a name="footnote4">4</a> We use the "FSL definition", i.e, the time between the center of the first "effective" echo and the center of the last "effective" echo.

</div>

<div>

<a name="footnote5">5</a> [http://fsl.fmrib.ox.ac.uk/fsl/fsl4.0/fdt/fdt_dtifit.html](hhttp://fsl.fmrib.ox.ac.uk/fsl/fsl4.0/fdt/fdt_dtifit.html)

</div>

<div>

<a name="footnote6">6</a> For example in case there is an in scanner training phase that begins before the scanning sequence has started events from this sequence should have negative onset time counting down to the beginning of the acquisition of the first volume.

</div>

<div>

<a name="footnote7">7</a> [http://www.emotionlab.se/resources/kdef](http://www.emotionlab.se/resources/kdef)

</div>
