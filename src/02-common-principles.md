# Common principles

## Definitions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [[RFC2119](https://www.ietf.org/rfc/rfc2119.txt)].

Throughout this specification we use a list of terms and abbreviations. To avoid
misunderstanding we clarify them here.

1.  **Dataset** - a set of neuroimaging and behavioral data acquired for a
    purpose of a particular study. A dataset consists of data acquired from one
    or more subjects, possibly from multiple sessions.

1.  **Subject** - a person or animal participating in the study.  Used
    interchangeably with term **Participant**.

1.  **Session** - a logical grouping of neuroimaging and behavioral data
    consistent across subjects. Session can (but doesn't have to) be synonymous
    to a visit in a longitudinal study. In general, subjects will stay in the
    scanner during one session. However, for example, if a subject has to leave
    the scanner room and then be re-positioned on the scanner bed, the set of
    MRI acquisitions will still be considered as a session and match sessions
    acquired in other subjects. Similarly, in situations where different data
    types are obtained over several visits (for example fMRI on one day followed
    by DWI the day after) those can be grouped in one session. Defining multiple
    sessions is appropriate when several identical or similar data acquisitions
    are planned and performed on all -or most- subjects, often in the case of
    some intervention between sessions (e.g., training).

1.  **Data acquisition** - a continuous uninterrupted block of time during which
    a brain scanning instrument was acquiring data according to particular
    scanning sequence/protocol.

1.  **Data type** - a functional group of different types of data. In BIDS we
    define eight data types: `func` (task based and resting state functional MRI),
    `dwi` (diffusion weighted imaging), `fmap` (field inhomogeneity mapping data
    such as field maps), `anat` (structural imaging such as T1, T2, etc.), `meg`
    (magnetoencephalography), `eeg` (electroencephalography), `ieeg` (intracranial
    electroencephalography), `beh` (behavioral).

1.  **Task** - a set of structured activities performed by the participant.
    Tasks are usually accompanied by stimuli and responses, and can greatly vary
    in complexity. For the purpose of this specification we consider the so-called
    "resting state" a task. In the context of brain scanning, a task is always
    tied to one data acquisition. Therefore, even if during one acquisition the
    subject performed multiple conceptually different behaviors (with different
    sets of instructions) they will be considered one (combined) task.

1.  **Event** - a stimulus or subject response recorded during a task. Each
    event has an onset time and duration. Note that not all tasks will have
    recorded events (e.g., “resting state”).

1.  **Run** - an uninterrupted repetition of data acquisition that has the same
    acquisition parameters and task (however events can change from run to run
    due to different subject response or randomized nature of the stimuli). Run
    is a synonym of a data acquisition.

1.  **`<index>`** - a numeric value, possibly prefixed with arbitrary number of
    0s for consistent indentation, e.g., it is `01` in `run-01` following
    `run-<index>` specification.

1.  **`<label>`** - an alphanumeric value, possibly prefixed with arbitrary
    number of 0s for consistent indentation, e.g., it is `rest` in `task-rest`
    following `task-<label>` specification.

1.  **`suffix`** - an alphanumeric value, located after the `key-value_` pairs (thus after
    the final `_`), right before the **File extension**, e.g., it is `eeg` in
    `sub-05_task-matchingpennies_eeg.vhdr`.

1.  **File extension** - a portion of the the file name after the left-most
    period (`.`) preceded by any other alphanumeric. For example, `.gitignore` does
    not have a file extension, but the file extension of `test.nii.gz` is `.nii.gz`.
    Note that the left-most period is included in the file extension.

## Compulsory, optional, and additional data and metadata

The following standard describes a way of arranging data and writing down
metadata for a subset of neuroimaging experiments. Some aspects of the standard
are compulsory. For example a particular file name format is required when
storing structural scans. Some aspects are regulated but optional. For example a
T2 volume does not need to be included, but when it is available it should be
saved under a particular file name specified in the standard. This standard
aspires to describe a majority of datasets, but acknowledges that there will be
cases that do not fit. In such cases one can include additional files and
subfolders to the existing folder structure following common sense. For example
one may want to include eye tracking data in a vendor specific format that is
not covered by this standard. The most sensible place to put it is next to the
continuous recording file with the same naming scheme but different extensions.
The solutions will change from case to case and publicly available datasets will
be reviewed to include common data types in the future releases of the BIDS
specification.

## File name structure

A file name consists of a chain of *entities*, or key-value pairs, a *suffix* and an
*extension*.
Two prominent examples of entities are `subject` and `session`.

For a data file that was collected in a given `session` from a given
`subject`, the file name will begin with the string `sub-<label>_ses-<label>`.

Note that `sub-<label>` corresponds to the `subject` entity because it has
the `sub-` "key" and`<label>` "value", where `<label>` would in a real data file
correspond to a unique identifier of that subject, such as `01`.
The same holds for the `session` entity with its `ses-` key and its `<label>`
value.

A chain of entities, followed by a suffix, connected by underscores (`_`)
produces a human readable file name, such as `sub-01_task-rest_eeg.edf`.
It is evident from the file name alone that the file contains resting state
data from subject `01`.
The suffix `eeg` and the extension `.edf` depend on the imaging modality and
the data format and indicate further details of the file's contents.

A summary of all entities in BIDS and the order in which they MUST be
specified is available in the [entity table](./99-appendices/04-entity-table.md)
in the appendix.

## Source vs. raw vs. derived data

BIDS was originally designed to describe and apply consistent naming conventions
to raw (unprocessed or minimally processed due to file format conversion) data.
During analysis such data will be transformed and partial as well as final results
will be saved.
Derivatives of the raw data (other than products of DICOM to NIfTI conversion)
MUST be kept separate from the raw data. This way one can protect the raw data
from accidental changes by file permissions. In addition it is easy to
distinguish partial results from the raw data and share the latter.
See [Storage of derived datasets](#storage-of-derived-datasets) for more on
organizing derivatives.

Similar rules apply to source data, which is defined as data before
harmonization, reconstruction, and/or file format conversion (for example, E-Prime event logs or
DICOM files). This specification currently does not go into details of
recommending a particular naming scheme for including different types of
source data (raw event logs, parameter files, etc. before conversion to BIDS).
However, in the case that these data are to be included:

1.  These data MUST be kept in separate `sourcedata` folder with a similar
    folder structure as presented below for the BIDS-managed data. For example:
    `sourcedata/sub-01/ses-pre/func/sub-01_ses-pre_task-rest_bold.dicom.tgz` or
    `sourcedata/sub-01/ses-pre/func/MyEvent.sce`.

1.  A README file SHOULD be found at the root of the `sourcedata` folder or the
    `derivatives` folder, or both.
    This file should describe the nature of the raw data or the derived data.
    We RECOMMEND including the PDF print-out with the actual sequence
    parameters generated by the scanner in the `sourcedata`  folder.

Alternatively one can organize their data in the following way

```Text
my_dataset/
  sourcedata/
    ...
  rawdata/
    dataset_description.json
    participants.tsv
    sub-01/
    sub-02/
    ...
  derivatives/
    pipeline_1/
    pipeline_2/
    ...
```

In this example, where `sourcedata` and `derivatives` are not nested inside
`rawdata`, **only the `rawdata` subfolder** needs to be a BIDS-compliant
dataset.
The subfolders of `derivatives` MAY be BIDS-compliant derivatives datasets
(see [Non-compliant derivatives][#non-compliant-derivatives] for further discussion).
This specification does not prescribe anything about the contents of `sourcedata`
folders in the above example - nor does it prescribe the `sourcedata`,
`derivatives`, or `rawdata` folder names.
The above example is just a convention that can be useful for organizing raw,
source, and derived data while maintaining BIDS compliancy of the raw data
folder. When using this convention it is RECOMMENDED to set the `SourceDatasets`
field in `dataset_description.json` of each subfolder of `derivatives` to:

```JSON
{
  "SourceDatasets": [ {"URL": "file://../../rawdata/"} ]
}
```

### Storage of derived datasets

Derivatives can be stored/distributed in two ways:

1.  Under a `derivatives/` subfolder in the root of the source BIDS dataset
    folder to make a clear distinction between raw data and results of data
    processing. A data processing pipeline will typically have a dedicated directory
    under which it stores all of its outputs. Different components of a pipeline can,
    however, also be stored under different subfolders. There are few restrictions on
    the directory names; it is RECOMMENDED to use the format `<pipeline>-<variant>` in
    cases where it is anticipated that the same pipeline will output more than one variant (e.g.,
    `AFNI-blurring`, `AFNI-noblurring`, etc.). For the sake of consistency, the
    subfolder name SHOULD be the `GeneratedBy.Name` field in
    `data_description.json`, optionally followed by a hyphen and a suffix (see
    [Derived dataset and pipeline description][derived-dataset-description]).

    Example of derivatives with one directory per pipeline:

    ```Plain
    <dataset>/derivatives/fmriprep-v1.4.1/sub-0001
    <dataset>/derivatives/spm/sub-0001
    <dataset>/derivatives/vbm/sub-0001
    ```

    Example of a pipeline with split derivative directories:

    ```Plain
    <dataset>/derivatives/spm-preproc/sub-0001
    <dataset>/derivatives/spm-stats/sub-0001
    ```

    Example of a pipeline with nested derivative directories:

    ```Plain
    <dataset>/derivatives/spm-preproc/sub-0001
    <dataset>/derivatives/spm-preproc/derivatives/spm-stats/sub-0001
    ```


1.  As a standalone dataset independent of the source (raw or derived) BIDS
    dataset.
    This way of specifying derivatives is particularly useful when the source
    dataset is provided with read-only access, for publishing derivatives as
    independent bodies of work, or for describing derivatives that were created
    from more than one source dataset.
    The `sourcedata/` subdirectory MAY be used to include the source dataset(s)
    that were used to generate the derivatives.
    Likewise, any code used to generate the derivatives from the source data
    MAY be included in the `code/` subdirectory.

    Example of a derivative dataset including the raw dataset as source:

    ```Plain
    my_processed_data/
      code/
        processing_pipeline-1.0.0.img
        hpc_submitter.sh
        ...
      sourcedata/
        dataset_description.json
        participants.tsv
        sub-01/
        sub-02/
        ...
      dataset_description.json
      sub-01/
      sub-02/
      ...
    ```

Throughout this specification, if a section applies particularly to derivatives,
then Case 1 will be assumed for clarity in templates and examples, but removing
`/derivatives/<pipeline>` from the template name will provide the equivalent for
Case 2.
In both cases, every derivatives dataset is considered a BIDS dataset and must
include a `dataset_description.json` file at the root level (see
[Dataset description][dataset-description].
Consequently, files should be organized to comply with BIDS to the full extent
possible (that is, unless explicitly contradicted for derivatives).
Any subject-specific derivatives should be housed within each subject’s directory;
if session-specific derivatives are generated, they should be deposited under a
session subdirectory within the corresponding subject directory; and so on.

### Non-compliant deriatives

Nothing in this specification should be interpreted to disallow the
storage/distribution of non-compliant derivatives of BIDS datasets.
In particular, if a BIDS dataset contains a `derivatives/` sub-directory,
the contents of that directory may be a heterogeneous mix of BIDS Derivatives
datasets and non-compliant derivatives.

## The Inheritance Principle

Any metadata file (`.json`, `.bvec`, `.tsv`, etc.) may be defined at any
directory level, but no more than one applicable file may be defined at a given
level (Example 1). The values from the top level are inherited by all lower
levels unless they are overridden by a file at the lower level. For example,
`sub-*_task-rest_bold.json` may be specified at the participant level, setting
TR to a specific value. If one of the runs has a different TR than the one
specified in that file, another `sub-*_task-rest_bold.json` file can be placed
within that specific series directory specifying the TR for that specific run.
There is no notion of "unsetting" a key/value pair.
Once a key/value pair is set in a given level in the dataset, lower down in
the hierarchy that key/value pair will always have some assigned value.
Files for a particular participant can exist only at participant level directory, i.e
`/dataset/sub-*[/ses-*]/sub-*_T1w.json`. Similarly, any file that is not
specific to a participant is to be declared only at top level of dataset for eg:
`task-sist_bold.json` must be placed under `/dataset/task-sist_bold.json`

Example 1: Two JSON files that are erroneously at the same level

```Text
sub-01/
    ses-test/
        sub-01_ses-test_task-overtverbgeneration_bold.json
        sub-01_ses-test_task-overtverbgeneration_run-2_bold.json
        anat/
            sub-01_ses-test_T1w.nii.gz
        func/
            sub-01_ses-test_task-overtverbgeneration_run-1_bold.nii.gz
            sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz
```

In the above example, two JSON files are listed under `sub-01/ses-test/`, which
are each applicable to
`sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz`, violating the
constraint that no more than one file may be defined at a given level of the
directory structure. Instead `sub-01_ses-test_task-overtverbgeneration_run-2_bold.json`
should have been under `sub-01/ses-test/func/`.

Example 2: Multiple `run`s and `rec`s with same acquisition (`acq`) parameters

```Text
sub-01/
    anat/
    func/
        sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
        sub-01_task-xyz_acq-test1_run-2_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
        sub-01_task-xyz_acq-test1_bold.json
```

For the above example, all NIfTI files are acquired with same scanning
parameters (`acq-test1`). Hence a JSON file describing the acq parameters will
apply to different runs and rec files. Also if the JSON file
(`task-xyz_acq-test1_bold.json`) is defined at dataset top level directory, it
will be applicable to all task runs with `test1` acquisition parameter.

Example 3: Multiple JSON files at different levels for same task and acquisition parameters

```Text
task-xyz_acq-test1_bold.json
sub-01/
    anat/
    func/
        sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
        sub-01_task-xyz_acq-test1_bold.json
```

In the above example, the fields from the `task-xyz_acq-test1_bold.json` file
at the top directory will apply to all bold runs. However, if there is a key
with different value in the
`sub-01/func/sub-01_task-xyz_acq-test1_bold.json` file defined at a
deeper level, that value will be applicable for that particular run/task NIfTI
file/s. In other words, the `.json` file at the deeper level overrides values
that are potentially also defined in the `.json` at a more shallow level. If the
`.json` file at the more shallow level contains key-value-pairs that are not
present in the `.json` file at the deeper level, these key-value-pairs are
inherited by the `.json` file at the deeper level (but NOT vice versa!).

### Good practice recommendations

**Try to avoid excessive amount of overrides.**  Do not specify a field
value in the upper levels if lower levels have more or less even
distribution of multiple possible values. E.g., if a field `X` has one
value for all `ses-01/` and another for all `ses-02/` it better not to be
defined at all in the `.json` at the upper level.

## File Formation specification

### Imaging files

All imaging data MUST be stored using the NIfTI file format. We RECOMMEND using
compressed NIfTI files (.nii.gz), either version 1.0 or 2.0. Imaging data SHOULD
be converted to the NIfTI format using a tool that provides as much of the NIfTI
header information (such as orientation and slice timing information) as
possible. Since the NIfTI standard offers limited support for the various image
acquisition parameters available in DICOM files, we RECOMMEND that users provide
additional meta information extracted from DICOM files in a sidecar JSON file
(with the same filename as the `.nii[.gz]` file, but with a `.json` extension).
Extraction of BIDS compatible metadata can be performed using [dcm2niix](https://github.com/rordenlab/dcm2niix)
and [dicm2nii](http://www.mathworks.com/matlabcentral/fileexchange/42997-dicom-to-nifti-converter/content/dicm2nii.m)
DICOM to NIfTI converters. The [BIDS-validator](https://github.com/bids-standard/bids-validator)
will check for conflicts between the JSON file and the data recorded in the
NIfTI header.

### Tabular files

Tabular data MUST be saved as tab delimited values (`.tsv`) files, i.e., CSV
files where commas are replaced by tabs. Tabs MUST be true tab characters and
MUST NOT be a series of space characters. Each TSV file MUST start with a header
line listing the names of all columns (with the exception of
[physiological and other continuous recordings](04-modality-specific-files/06-physiological-and-other-continuous-recordings.md)).
Names MUST be separated with tabs.
It is RECOMMENDED that the column names in the header of the TSV file are
written in [`snake_case`](https://en.wikipedia.org/wiki/Snake_case) with the
first letter in lower case (e.g., `variable_name`, not `Variable_name`).
String values containing tabs MUST be escaped using double
quotes. Missing and non-applicable values MUST be coded as `n/a`. Numerical
values MUST employ the dot (`.`) as decimal separator and MAY be specified
in scientific notation, using `e` or `E` to separate the significand from the
exponent. TSV files MUST be in UTF-8 encoding.

Example:

```Text
onset duration  response_time correct stop_trial  go_trial
200 200 0 n/a n/a n/a
```

Tabular files MAY be optionally accompanied by a simple data dictionary
in the form of a [JSON object](https://www.w3schools.com/js/js_json_objects.asp)
within a JSON file.
The JSON files containing the data dictionaries MUST have the same name as
their corresponding tabular files but with `.json` extensions.
If a data dictionary
is provided, it MAY contain one or more fields describing the columns found in
the TSV file (in addition to any other metadata one wishes to include that
describe the file as a whole). Note that if a field name included in the data
dictionary matches a column name in the TSV file, then that field MUST contain a
description of the corresponding column, using an object containing the following
fields:

| Field name  | Definition                                                                                                      |
| :---------- | :-------------------------------------------------------------------------------------------------------------- |
| LongName    | Long (unabbreviated) name of the column.                                                                        |
| Description | Description of the column.                                                                                      |
| Levels      | For categorical variables: a dictionary of possible values (keys) and their descriptions (values).              |
| Units       | Measurement units. SI units in CMIXF formatting are RECOMMENDED (see [Units](./02-common-principles.md#units)). |
| TermURL     | URL pointing to a formal definition of this type of data in an ontology available on the web.                   |

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
    "Units": "kg/m^2",
    "TermURL": "http://purl.bioontology.org/ontology/SNOMEDCT/60621009"
  }
}
```

### Key/value files (dictionaries)

JavaScript Object Notation (JSON) files MUST be used for storing key/value
pairs. JSON files MUST be in UTF-8 encoding. Extensive documentation of the
format can be found here: [http://json.org/](http://json.org/). Several editors
have built-in support for JSON syntax highlighting that aids manual creation of
such files. An online editor for JSON with built-in validation is available at:
[http://jsoneditoronline.org](http://jsoneditoronline.org). 
It is RECOMMENDED that keys in a JSON file are written in [CamelCase](https://en.wikipedia.org/wiki/Camel_case)
with the first letter in upper case (e.g., `SamplingFrequency`, not
`samplingFrequency`). Note however, when a JSON file is used as an accompanying
sidecar file for a [TSV file](#tabular-files), the keys linking a TSV column
with their description in the JSON file need to follow the exact formatting
as in the TSV file.

Example of a hypothetical `*_bold.json` file, accompanying a `*_bold.nii` file:

```JSON
{
  "RepetitionTime": 3,
  "Instruction": "Lie still and keep your eyes open"
}
```

Example of a hypothetical `*_events.json` file, accompanying an
`*_events.tsv` file. Note that the JSON file contains a key describing an
*arbitrary* column `stim_presentation_side` in the TSV file it accompanies.
See [task events section](04-modality-specific-files/05-task-events.md)
for more information.

```JSON
{
  "stim_presentation_side": {
    "Levels": {
      "1": "stimulus presented on LEFT side",
      "2": "stimulus presented on RIGHT side"
    }
  }
}
```

## Participant names and other labels

BIDS allows for custom user-defined `<label>`s and `<index>`es e.g.,
for naming of participants, sessions, acquisition schemes, etc. Note
that they MUST consist only of allowed characters as described in
[Definitions](02-common-principles.md#definitions) above. In `<index>`es
we RECOMMEND using zero padding (e.g., `01` instead of `1` if you have more than
nine subjects) to make alphabetical sorting more intuitive. Note that
zero padding SHOULD NOT be used to merely maintain uniqueness
of `<index>`es.

Please note that a given label or index is distinct from the "prefix"
it refers to. For example `sub-01` refers to the `sub` entity (a
subject) with the label `01`. The `sub-` prefix is not part of the subject
label, but must be included in file names (similarly to other key names).

## Units

All units SHOULD be specified as per [International System of Units](https://en.wikipedia.org/wiki/International_System_of_Units)
(abbreviated as SI, from the French Système international (d'unités)) and can
be SI units or [SI derived units](https://en.wikipedia.org/wiki/SI_derived_unit).
In case there are valid reasons to deviate from SI units or SI derived units,
the units MUST be specified in the sidecar JSON file.
In case data is expressed in SI units or SI derived units, the units MAY be
specified in the sidecar JSON file.
In case non-standard prefixes are added to SI or non-SI units, these
non-standard prefixed units MUST be specified in the JSON file.
See [Appendix V](99-appendices/05-units.md) for a list of standard units and
prefixes.
Note also that for the *formatting* of SI units, the [CMIXF-12](https://people.csail.mit.edu/jaffer/MIXF/CMIXF-12)
convention for encoding units is RECOMMENDED.
CMIXF provides a consistent system for all units and prefix symbols with only basic
characters, avoiding symbols that can cause text encoding problems; for example the
CMIXF formatting for "micro volts" is `uV`, "degrees Celsius" is `oC` and "Ohm" is `Ohm`.
See [Appendix V](99-appendices/05-units.md) for more information.

For additional rules, see below:

-   Elapsed time SHOULD be expressed in seconds. Please note that some DICOM
    parameters have been traditionally expressed in milliseconds. Those need to
    be converted to seconds.

-   Frequency SHOULD be expressed in Hertz.

Describing dates and timestamps:

-   Date time information MUST be expressed in the following format
    `YYYY-MM-DDThh:mm:ss[.000000]` (year, month, day, hour (24h), minute,
    second, and optionally fractional second).
    This is equivalent to the RFC3339 "date-time" format, time zone is always
    assumed as local time).
    No specific precision is required for fractional seconds, but the precision
    SHOULD be consistent across the dataset.
    For example `2009-06-15T13:45:30`

-   Time stamp information MUST be expressed in the following format:
    `13:45:30[.000000]`

-   Dates can be shifted by a random number of days for privacy protection
    reasons.
    To distinguish real dates from shifted dates, always use year 1925
    or earlier when including shifted years.
    For longitudinal studies dates MUST be shifted by the same number of days
    within each subject to maintain the interval information.
    For example: `1867-06-15T13:45:30`

-   Age SHOULD be given as the number of years since birth at the time of
    scanning (or first scan in case of multi session datasets). Using higher
    accuracy (weeks) should in general be avoided due to privacy protection,
    unless when appropriate given the study goals, e.g., when scanning babies.

## Directory structure

### Single session example

This is an example of the folder and file structure. Because there is only one
session, the session level is not required by the format. For details on
individual files see descriptions in the next section:

```Text
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

## Unspecified data

Additional files and folders containing raw data MAY be added as needed for
special cases.
All non-standard file entities SHOULD conform to BIDS-style naming conventions, including
alphabetic entities and suffixes and alphanumeric labels/indices.
Non-standard suffixes SHOULD reflect the nature of the data, and existing
entities SHOULD be used when appropriate.
For example, an ASSET calibration scan might be named
`sub-01_acq-ASSET_calibration.nii.gz`.

Non-standard files and directories should be named with care.
Future BIDS efforts may standardize new entities and suffixes, changing the
meaning of file names and setting requirements on their contents or metadata.
Validation and parsing tools MAY treat the presence of non-standard files and
directories as an error, so consult the details of these tools for mechanisms
to suppress warnings or provide interpretations of your file names.

[]: <> (################)
[]: <> (Link definitions)
[]: <> (################)

[dataset-description]: 03-modality-agnostic-files.md#dataset-description
[derived-dataset-description]: 03-modality-agnostic-files.md#derived-dataset-and-pipeline-description
