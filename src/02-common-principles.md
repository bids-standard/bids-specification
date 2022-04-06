# Common principles

## Definitions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [[RFC2119](https://www.ietf.org/rfc/rfc2119.txt)].

Throughout this specification we use a list of terms and abbreviations. To avoid
misunderstanding we clarify them here.

1.  **Dataset** - a set of neuroimaging and behavioral data acquired for a
    purpose of a particular study. A dataset consists of data acquired from one
    or more subjects, possibly from multiple sessions.

1.  **Subject** - a person or animal participating in the study.  Used
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
    some intervention between sessions (for example, training).
    In the [PET](04-modality-specific-files/09-positron-emission-tomography.md)
    context, a session may also indicate a group of related scans,
    taken in one or more visits.

1.  **Sample** - a sample pertaining to a subject such as tissue, primary cell
    or cell-free sample.
    The `sample-<label>` key/value pair is used to distinguish between different
    samples from the same subject.
    The label MUST be unique per subject and is RECOMMENDED to be unique
    throughout the dataset.

1.  **Data acquisition** - a continuous uninterrupted block of time during which
    a brain scanning instrument was acquiring data according to particular
    scanning sequence/protocol.

1.  **Data type** - a functional group of different types of data.
    BIDS defines the following data types:

    1.  `func` (task based and resting state functional MRI)
    1.  `dwi` (diffusion weighted imaging)
    1.  `fmap` (field inhomogeneity mapping data such as field maps)
    1.  `anat` (structural imaging such as T1, T2, PD, and so on)
    1.  `perf` (perfusion)
    1.  `meg` (magnetoencephalography)
    1.  `eeg` (electroencephalography)
    1.  `ieeg` (intracranial electroencephalography)
    1.  `beh` (behavioral)
    1.  `pet` (positron emission tomography)
    1.  `micr` (microscopy)

    Data files are contained in a directory named for the data type.
    In raw datasets, the data type directory is nested inside subject and
    (optionally) session directories.

1.  **Task** - a set of structured activities performed by the participant.
    Tasks are usually accompanied by stimuli and responses, and can greatly vary
    in complexity. For the purpose of this specification we consider the so-called
    "resting state" a task. In the context of brain scanning, a task is always
    tied to one data acquisition. Therefore, even if during one acquisition the
    subject performed multiple conceptually different behaviors (with different
    sets of instructions) they will be considered one (combined) task.

1.  **Event** - something that happens or may be perceived by a test subject as happening
    at a particular instant during the recording.
    Events are most commonly associated with on- or offset of stimulus presentations,
    or with the distinct marker of on- or offset of a subject's response or motor action.
    Other events may include unplanned incidents
    (for example, sudden onset of noise and vibrations due to construction work,
    laboratory device malfunction),
    changes in task instructions (for example, switching the response hand),
    or experiment control parameters (for example,
    changing the stimulus presentation rate over experimental blocks),
    and noted data feature occurrences (for example, a recording electrode producing noise).
    In BIDS, each event has an onset time and duration.
    Note that not all tasks will have recorded events (for example, "resting state").

1.  **Run** - an uninterrupted repetition of data acquisition that has the same
    acquisition parameters and task (however events can change from run to run
    due to different subject response or randomized nature of the stimuli). Run
    is a synonym of a data acquisition.
    Note that "uninterrupted" may look different by modality due to the nature of the
    recording.
    For example, in [MRI](04-modality-specific-files/01-magnetic-resonance-imaging-data.md)
    or [MEG] (04-modality-specific-files/02-magnetoencephalography.md),
    if a subject leaves the scanner, the acquisition must be restarted.
    For some types of [PET](04-modality-specific-files/09-positron-emission-tomography.md) acquisitions,
    a subject may leave and re-enter the scanner without interrupting the scan.

1.  **Modality** - the category of brain data recorded by a file.
    For MRI data, different pulse sequences are considered distinct modalities,
    such as `T1w`, `bold` or `dwi`.
    For passive recording techniques, such as EEG, MEG or iEEG,
    the technique is sufficiently uniform to define the modalities `eeg`,
    `meg` and `ieeg`.
    When applicable, the modality is indicated in the **suffix**.
    The modality may overlap with, but should not be confused with
    the **data type**.

1.  **`<index>`** - a nonnegative integer, possibly prefixed with arbitrary number of
    0s for consistent indentation, for example, it is `01` in `run-01` following
    `run-<index>` specification.

1.  **`<label>`** - an alphanumeric value, possibly prefixed with arbitrary
    number of 0s for consistent indentation, for example, it is `rest` in `task-rest`
    following `task-<label>` specification. Note that labels MUST not collide when
    casing is ignored (see [Case collision intolerance](#case-collision-intolerance)).

1.  **`suffix`** - an alphanumeric value, located after the `key-value_` pairs (thus after
    the final `_`), right before the **File extension**, for example, it is `eeg` in
    `sub-05_task-matchingpennies_eeg.vhdr`.

1.  **File extension** - a portion of the filename after the left-most
    period (`.`) preceded by any other alphanumeric. For example, `.gitignore` does
    not have a file extension, but the file extension of `test.nii.gz` is `.nii.gz`.
    Note that the left-most period is included in the file extension.

1.  **DEPRECATED** - A "deprecated" entity or metadata field SHOULD NOT be used in the
    generation of new datasets.
    It remains in the standard in order to preserve the interpretability of existing datasets.
    Validating software SHOULD warn when deprecated practices are detected and provide a
    suggestion for updating the dataset to preserve the curator's intent.

## Compulsory, optional, and additional data and metadata

The following standard describes a way of arranging data and writing down
metadata for a subset of neuroimaging experiments. Some aspects of the standard
are compulsory. For example a particular filename format is required when
storing structural scans. Some aspects are regulated but optional. For example a
T2 volume does not need to be included, but when it is available it should be
saved under a particular filename specified in the standard. This standard
aspires to describe a majority of datasets, but acknowledges that there will be
cases that do not fit. In such cases one can include additional files and
subdirectories to the existing directory structure following common sense. For example
one may want to include eye tracking data in a vendor specific format that is
not covered by this standard. The most sensible place to put it is next to the
continuous recording file with the same naming scheme but different extensions.
The solutions will change from case to case and publicly available datasets will
be reviewed to include common data types in the future releases of the BIDS
specification.

## File name structure

A filename consists of a chain of *entities*, or key-value pairs, a *suffix* and an
*extension*.
Two prominent examples of entities are `subject` and `session`.

For a data file that was collected in a given `session` from a given
`subject`, the filename MUST begin with the string `sub-<label>_ses-<label>`.
If the `session` level is omitted in the directory structure, the filename MUST begin
with the string `sub-<label>`, without `ses-<label>`.

Note that `sub-<label>` corresponds to the `subject` entity because it has
the `sub-` "key" and`<label>` "value", where `<label>` would in a real data file
correspond to a unique identifier of that subject, such as `01`.
The same holds for the `session` entity with its `ses-` key and its `<label>`
value.

The extra session layer (at least one `/ses-<label>` subdirectory) SHOULD
be added for all subjects if at least one subject in the dataset has more than
one session.
If a `/ses-<label>` subdirectory is included as part of the directory hierarchy,
then the same [`ses-<label>`](./99-appendices/09-entities.md#ses)
key/value pair MUST also be included as part of the filenames themselves.
Acquisition time of session can
be defined in the [sessions file](03-modality-agnostic-files.md#sessions-file).

A chain of entities, followed by a suffix, connected by underscores (`_`)
produces a human readable filename, such as `sub-01_task-rest_eeg.edf`.
It is evident from the filename alone that the file contains resting state
data from subject `01`.
The suffix `eeg` and the extension `.edf` depend on the imaging modality and
the data format and indicate further details of the file's contents.

Entities within a filename MUST be unique.
For example, the following filename is not valid because it uses the `acq`
entity twice:
`sub-01_acq-laser_acq-uneven_electrodes.tsv`

In cases where entities duplicate metadata,
the presence of an entity should not be used as a replacement for
the corresponding metadata field.
For instance, in echo-planar imaging MRI,
the [`dir-<label>`](./99-appendices/09-entities.md#dir) entity MAY be used
to distinguish files with different phase-encoding directions,
but the file's `PhaseEncodingDirection` can only be specified as metadata.

A summary of all entities in BIDS and the order in which they MUST be
specified is available in the [entity table](./99-appendices/04-entity-table.md)
in the appendix.

### Entity-linked file collections

An entity-linked file collection is a set of files that are related to each other
based on a repetitive acquisition of sequential data
by changing acquisition parameters one (or multiple) at a time
or by being inherent components of the same data.
Entity-linked collections are identified by a common suffix,
indicating the group of files that should be considered a logical unit.
Within each collection, files MUST be distinguished from each other by at least one
entity (for example, `echo`) that corresponds to an altered acquisition parameter
(`EchoTime`) or that defines a component relationship (for example, `part`).
Note that these entities MUST be described by the specification and
the parameter changes they declare MUST NOT invalidate the definition of the accompanying suffix.
For example, the use of the `echo` entity along with the `T1w` suffix casts doubt on
the validity of the identified contrast weighting.
Provided the conditions above are satisfied,
any suffix (such as `bold`) can identify an entity-linked file collection,
although certain suffixes are exclusive for this purpose (for example, `MP2RAGE`).
Use cases concerning this convention are compiled in the
[file collections](./99-appendices/10-file-collections.md) appendix.
This convention is mainly intended for but not limited to MRI modalities.

### Case collision intolerance

File name components are case sensitive,
but collisions MUST be avoided when casing is ignored.
For example, a dataset cannot contain both `sub-s1` and `sub-S1`,
as the labels would collide on a case-insensitive filesystem.
Additionally, because the suffix `eeg` is defined,
then the suffix `EEG` will not be added to future versions of the standard.

## Source vs. raw vs. derived data

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
harmonization, reconstruction, and/or file format conversion (for example, E-Prime event logs or DICOM files).
Storing actual source files with the data is preferred over links to
external source repositories to maximize long term preservation,
which would suffer if an external repository would not be available anymore.
This specification currently does not go into the details of
recommending a particular naming scheme for including different types of
source data (such as the raw event logs or parameter files, before conversion to BIDS).
However, in the case that these data are to be included:

1.  These data MUST be kept in separate `sourcedata` directory with a similar
    directory structure as presented below for the BIDS-managed data. For example:
    `sourcedata/sub-01/ses-pre/func/sub-01_ses-pre_task-rest_bold.dicom.tgz` or
    `sourcedata/sub-01/ses-pre/func/MyEvent.sce`.

1.  A README file SHOULD be found at the root of the `sourcedata` directory or the
    `derivatives` directory, or both.
    This file should describe the nature of the raw data or the derived data.
    We RECOMMEND including the PDF print-out with the actual sequence
    parameters generated by the scanner in the `sourcedata`  directory.

Alternatively one can organize their data in the following way

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "my_dataset-1": {
            "sourcedata": "",
            "...": "",
            "rawdata": {
                "dataset_description.json": "",
                "participants.tsv": "",
                "sub-01": {},
                "sub-02": {},
                "...": "",
            },
            "derivatives": {
                "pipeline_1": {},
                "pipeline_2": {},
                "...": "",
            },
        }
    }
) }}

In this example, where `sourcedata` and `derivatives` are not nested inside
`rawdata`, **only the `rawdata` subdirectory** needs to be a BIDS-compliant
dataset.
The subdirectories of `derivatives` MAY be BIDS-compliant derivatives datasets
(see [Non-compliant derivatives](#non-compliant-derivatives) for further discussion).
This specification does not prescribe anything about the contents of `sourcedata`
directories in the above example - nor does it prescribe the `sourcedata`,
`derivatives`, or `rawdata` directory names.
The above example is just a convention that can be useful for organizing raw,
source, and derived data while maintaining BIDS compliance of the raw data
directory. When using this convention it is RECOMMENDED to set the `SourceDatasets`
field in `dataset_description.json` of each subdirectory of `derivatives` to:

```JSON
{
  "SourceDatasets": [ {"URL": "file://../../rawdata/"} ]
}
```

### Storage of derived datasets

Derivatives can be stored/distributed in two ways:

1.  Under a `derivatives/` subdirectory in the root of the source BIDS dataset
    directory to make a clear distinction between raw data and results of data
    processing.
    A data processing pipeline will typically have a dedicated directory
    under which it stores all of its outputs.
    Different components of a pipeline can, however, also be stored under different
    subdirectories.
    There are few restrictions on the directory names;
    it is RECOMMENDED to use the format `<pipeline>-<variant>` in cases where
    it is anticipated that the same pipeline will output more than one variant
    (for example, `AFNI-blurring` and `AFNI-noblurring`).
    For the sake of consistency, the subdirectory name SHOULD be
    the `GeneratedBy.Name` field in `data_description.json`,
    optionally followed by a hyphen and a suffix (see
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

    <!-- This block generates a file tree.
    A guide for using macros can be found at
    https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
    -->
    {{ MACROS___make_filetree_example(
        {
        "my_processed_data": {
            "code": {
                "processing_pipeline-1.0.0.img": "",
                "hpc_submitter.sh": "",
                "...": "",
            },
            "sourcedata": {
                "sub-01": {},
                "sub-02": {},
                "...": "",
            },
            "sub-01": {},
            "sub-02": {},
            "...": "",
            }
        }
    ) }}

Throughout this specification, if a section applies particularly to derivatives,
then Case 1 will be assumed for clarity in templates and examples, but removing
`/derivatives/<pipeline>` from the template name will provide the equivalent for
Case 2.
In both cases, every derivatives dataset is considered a BIDS dataset and must
include a `dataset_description.json` file at the root level (see
[Dataset description][dataset-description]).
Consequently, files should be organized to comply with BIDS to the full extent
possible (that is, unless explicitly contradicted for derivatives).
Any subject-specific derivatives should be housed within each subject’s directory;
if session-specific derivatives are generated, they should be deposited under a
session subdirectory within the corresponding subject directory; and so on.

### Non-compliant derivatives

Nothing in this specification should be interpreted to disallow the
storage/distribution of non-compliant derivatives of BIDS datasets.
In particular, if a BIDS dataset contains a `derivatives/` subdirectory,
the contents of that directory may be a heterogeneous mix of BIDS Derivatives
datasets and non-compliant derivatives.

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
Extraction of BIDS compatible metadata can be performed using [dcm2niix](https://github.com/rordenlab/dcm2niix)
and [dicm2nii](https://www.mathworks.com/matlabcentral/fileexchange/42997-xiangruili-dicm2nii)
DICOM to NIfTI converters. The [BIDS-validator](https://github.com/bids-standard/bids-validator)
will check for conflicts between the JSON file and the data recorded in the
NIfTI header.

### Tabular files

Tabular data MUST be saved as tab delimited values (`.tsv`) files, that is, CSV
files where commas are replaced by tabs. Tabs MUST be true tab characters and
MUST NOT be a series of space characters. Each TSV file MUST start with a header
line listing the names of all columns (with the exception of
[physiological and other continuous recordings](04-modality-specific-files/06-physiological-and-other-continuous-recordings.md)).
Names MUST be separated with tabs.
It is RECOMMENDED that the column names in the header of the TSV file are
written in [`snake_case`](https://en.wikipedia.org/wiki/Snake_case) with the
first letter in lower case (for example, `variable_name`, not `Variable_name`).
String values containing tabs MUST be escaped using double
quotes. Missing and non-applicable values MUST be coded as `n/a`. Numerical
values MUST employ the dot (`.`) as decimal separator and MAY be specified
in scientific notation, using `e` or `E` to separate the significand from the
exponent. TSV files MUST be in UTF-8 encoding.

Example:

```Text
onset	duration	response_time	correct	stop_trial	go_trial
200	200	0	n/a	n/a	n/a
```

**Note**: The TSV examples in this document (like the one above this note)
are occasionally formatted using space characters instead of tabs to improve
human readability.
Directly copying and then pasting these examples from the specification
for use in new BIDS datasets can lead to errors and is discouraged.

Tabular files MAY be optionally accompanied by a simple data dictionary
in the form of a JSON [object](https://www.json.org/json-en.html)
within a JSON file.
The JSON files containing the data dictionaries MUST have the same name as
their corresponding tabular files but with `.json` extensions.
If a data dictionary is provided,
it MAY contain one or more fields describing the columns found in the TSV file
(in addition to any other metadata one wishes to include that describe the file as a whole).
Note that if a field name included in the data dictionary matches a column name in the TSV file,
then that field MUST contain a description of the corresponding column,
using an object containing the following fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
        "LongName": "OPTIONAL",
        "Description": (
            "RECOMMENDED",
            "The description of the column.",
        ),
        "Levels": "RECOMMENDED",
        "Units": "RECOMMENDED",
        "TermURL": "RECOMMENDED",
        "HED": "OPTIONAL",
   }
) }}

Please note that while both `Units` and `Levels` are RECOMMENDED, typically only one
of these two fields would be specified for describing a single TSV file column.

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
    "TermURL": "https://purl.bioontology.org/ontology/SNOMEDCT/60621009"
  }
}
```

### Key/value files (dictionaries)

JavaScript Object Notation (JSON) files MUST be used for storing key/value
pairs. JSON files MUST be in UTF-8 encoding. Extensive documentation of the
format can be found at [https://www.json.org/](https://www.json.org/),
and at [https://tools.ietf.org/html/std90](https://tools.ietf.org/html/std90).
Several editors have built-in support for JSON syntax highlighting that aids
manual creation of such files.
An online editor for JSON with built-in validation is available at
[https://jsoneditoronline.org](https://jsoneditoronline.org).
It is RECOMMENDED that keys in a JSON file are written in [CamelCase](https://en.wikipedia.org/wiki/Camel_case)
with the first letter in upper case (for example, `SamplingFrequency`, not
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

## The Inheritance Principle

1.  Any metadata file (such as `.json`, `.bvec` or `.tsv`) MAY be defined at any directory level.

1.  For a given data file, any metadata file is applicable to that data file if:
    1.  It is stored at the same directory level or higher;
    1.  The metadata and the data filenames possess the same suffix;
    1.  The metadata filename does not include any entity absent from the data filename.

1.  A metadata file MUST NOT have a filename that would be otherwise applicable
    to some data file based on rules 2.b and 2.c but is made inapplicable based on its
    location in the directory structure as per rule 2.a.

1.  There MUST NOT be multiple metadata files applicable to a data file at one level
    of the directory hierarchy.

1.  If multiple metadata files satisfy criteria 2.a-c above:

    1.  For [tabular files](#tabular-files) and other simple metadata files
        (for instance, [`bvec` / `bval` files for diffusion MRI](#04-modality-specific-files/01-magnetic-resonance-imaging#required-gradient-orientation-information)),
        accessing metadata associated with a data file MUST consider only the
        applicable file that is lowest in the filesystem hierarchy.

    1.  For [JSON files](#key-value-files-dictionaries), key-values are loaded
        from files from the top of the directory hierarchy downwards, such that
        key-values from the top level are inherited by all data files at lower
        levels to which it is applicable unless overridden by a value for the
        same key present in another metadata file at a lower level
        (though it is RECOMMENDED to minimize the extent of such overrides).

Corollaries:

1.  As per rule 3, metadata files applicable only to a specific participant / session
    MUST be defined in or below the directory corresponding to that participant / session;
    similarly, a metadata file that is applicable to multiple participants / sessions
    MUST NOT be placed within a directory corresponding to only one such participant / session.

1.  It is permissible for a single metadata file to be applicable to multiple data
    files at that level of the hierarchy or below. Where such metadata content is consistent
    across multiple data files, it is RECOMMENDED to store metadata in this
    way, rather than duplicating that metadata content across multiple metadata files.

1.  Where multiple applicable JSON files are loaded as per rule 5.b, key-values can
    only be overwritten by files lower in the filesystem hierarchy; the absence of
    a key-value in a later file does not imply the "unsetting" of that field
    (indeed removal of existing fields is not possible).

Example 1: Demonstration of inheritance principle

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-01": {
        "func": {
            "sub-01_task-rest_acq-default_bold.nii.gz": "",
            "sub-01_task-rest_acq-longtr_bold.nii.gz": "",
            "sub-01_task-rest_acq-longtr_bold.json": "",
            }
        },
    "task-rest_bold.json": "",
    }
) }}

Contents of file `task-rest_bold.json`:

```JSON
{
    "EchoTime": 0.040,
    "RepetitionTime": 1.0
}
```

Contents of file `sub-01/func/sub-01_task-rest_acq-longtr_bold.json`:

```JSON
{
    "RepetitionTime": 3.0
}
```

When reading image `sub-01/func/sub-01_task-rest_acq-default_bold.nii.gz`, only
metadata file `task-rest_bold.json` is read; file
`sub-01/func/sub-01_task-rest_acq-longtr_bold.json` is inapplicable as it contains
entity "`acq-longtr`" that is absent from the image path (rule 2.c). When reading image
`sub-01/func/sub-01_task-rest_acq-longtr_bold.nii.gz`, metadata file
`task-rest_bold.json` at the top level is read first, followed by file
`sub-01/func/sub-01_task-rest_acq-longtr_bold.json` at the bottom level (rule 5.b);
the value for field "`RepetitionTime`" is therefore overridden to the value `3.0`.
The value for field "`EchoTime`" remains applicable to that image, and is not unset by its
absence in the metadata file at the lower level (rule 5.b; corollary 3).

Example 2: Impermissible use of multiple metadata files at one directory level (rule 4)

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-01": {
        "ses-test":{
            "anat": {
                "sub-01_ses-test_T1w.nii.gz": "",
                },
            "func": {
                "sub-01_ses-test_task-overtverbgeneration_run-1_bold.nii.gz": "",
                "sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz": "",
                "sub-01_ses-test_task-overtverbgeneration_bold.json": "",
                "sub-01_ses-test_task-overtverbgeneration_run-2_bold.json": "",
                }
            }
        }
    }
) }}

Example 3: Modification of filesystem structure from Example 2 to satisfy inheritance
principle requirements

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-01": {
        "ses-test":{
            "sub-01_ses-test_task-overtverbgeneration_bold.json": "",
            "anat": {
                "sub-01_ses-test_T1w.nii.gz": "",
                },
            "func": {
                "sub-01_ses-test_task-overtverbgeneration_run-1_bold.nii.gz": "",
                "sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz": "",
                "sub-01_ses-test_task-overtverbgeneration_run-2_bold.json": "",
                }
            }
        }
    }
) }}

Example 4: Single metadata file applying to multiple data files (corollary 2)

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-01": {
        "anat": {},
        "func": {
            "sub-01_task-xyz_acq-test1_run-1_bold.nii.gz": "",
            "sub-01_task-xyz_acq-test1_run-2_bold.nii.gz": "",
            "sub-01_task-xyz_acq-test1_bold.json": "",
            }
        }
    }
) }}

## Participant names and other labels

BIDS allows for custom user-defined `<label>`s and `<index>`es for example,
for naming of participants, sessions, acquisition schemes.
Note that they MUST consist only of allowed characters as described in
[Definitions](02-common-principles.md#definitions) above.
In `<index>`es we RECOMMEND using zero padding (for example, `01` instead of `1`
if you have more than nine subjects) to make alphabetical sorting more intuitive.
Note that zero padding SHOULD NOT be used to merely maintain uniqueness
of `<index>`es.

Please note that a given label or index is distinct from the "prefix"
it refers to. For example `sub-01` refers to the `sub` entity (a
subject) with the label `01`. The `sub-` prefix is not part of the subject
label, but must be included in filenames (similarly to other key names).

## Specification of paths

Several metadata fields in BIDS require the specification of paths,
that is, a string of characters used to uniquely identify a location in a directory structure.
For example the `IntendedFor` or `AssociatedEmptyroom` metadata fields.

Throughout BIDS all such paths MUST be specified using the slash character (`/`),
regardless of the operating system that a particular dataset is curated on or used on.

Paths SHOULD NOT be absolute local paths,
because these might break when a dataset is used on a different machine.
It is RECOMMENDED that all paths specified in a BIDS dataset are relative paths,
as specified in the respective descriptions of metadata fields that require the use of paths.

## Uniform Resource Indicator

A Uniform Resource Indicator (URI) is a string referring to a resource and SHOULD
have the form `<scheme>:[//<authority>]<path>[?<query>][#<fragment>]`, as specified
in [RFC 3986](https://tools.ietf.org/html/rfc3986).
This applies to URLs and other common URIs, including Digital Object Identifiers (DOIs),
which may be fully specified as `doi:<path>`,
for example, [doi:10.5281/zenodo.3686061](https://doi.org/10.5281/zenodo.3686061).
A given resource may have multiple URIs.
When selecting URIs to add to dataset metadata, it is important to consider
specificity and persistence.

Several fields are designated for DOIs, for example, `DatasetDOI` in `dataset_description.json`.
DOI values SHOULD be fully specified URIs such as `doi:10.18112/openneuro.ds000001.v1.0.0`.
Bare DOIs such as `10.18112/openneuro.ds000001.v1.0.0` are [DEPRECATED][deprecated].

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

-   Arbitrary units SHOULD be indicated with the string `"arbitrary"`.

Describing dates and timestamps:

-   Date time information MUST be expressed in the following format
    `YYYY-MM-DDThh:mm:ss[.000000][Z]` (year, month, day, hour (24h), minute,
    second, optional fractional seconds, and optional UTC time indicator).
    This is almost equivalent to the [RFC3339](https://tools.ietf.org/html/rfc3339)
    "date-time" format, with the exception that UTC indicator `Z` is optional and
    non-zero UTC offsets are not indicated.
    If `Z` is not indicated, time zone is always assumed to be the local time of the
    dataset viewer.
    No specific precision is required for fractional seconds, but the precision
    SHOULD be consistent across the dataset.
    For example `2009-06-15T13:45:30`.

-   Time stamp information MUST be expressed in the following format:
    `hh:mm:ss[.000000]`
    For example `13:45:30`.

-   Note that, depending on local ethics board policy, date time information may not
    need to be fully detailed.
    For example, it is permissible to set the time to `00:00:00` if reporting the
    exact recording time is undesirable.
    However, for privacy protection reasons, it is RECOMMENDED to shift dates, as
    described below, without completely removing time information, as time information
    can be useful for research purposes.

-   Dates can be shifted by a random number of days for privacy protection
    reasons.
    To distinguish real dates from shifted dates,
    is is RECOMMENDED to set shifted dates to the year 1925 or earlier.
    Note that some data formats do not support arbitrary recording dates.
    For example, the [EDF](https://www.edfplus.info/)
    data format can only contain recording dates after 1985.
    For longitudinal studies dates MUST be shifted by the same number of days
    within each subject to maintain the interval information.
    For example: `1867-06-15T13:45:30`

-   WARNING: The Neuromag/Elekta/MEGIN file format for MEG (`.fif`) does *not*
    support recording dates earlier than `1902` roughly.
    Some analysis software packages (for example, MNE-Python) handle their data as `.fif`
    internally and will break if recording dates are specified prior to `1902`,
    even if the original data format is not `.fif`.
    See [MEG-file-formats](./99-appendices/06-meg-file-formats.md#recording-dates-in-fif-files)
    for more information.

-   Age SHOULD be given as the number of years since birth at the time of
    scanning (or first scan in case of multi session datasets). Using higher
    accuracy (weeks) should in general be avoided due to privacy protection,
    unless when appropriate given the study goals, for example, when scanning babies.

## Directory structure

### Single session example

This is an example of the directory and file structure. Because there is only one
session, the session level is not required by the format. For details on
individual files see descriptions in the next section:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
    {
    "sub-control01": {
        "anat":{
            "sub-control01_T1w.nii.gz": "",
            "sub-control01_T1w.json": "",
            "sub-control01_T2w.nii.gz": "",
            "sub-control01_T2w.json": "",
            },
        "func":{
            "sub-control01_task-nback_bold.nii.gz": "",
            "sub-control01_task-nback_bold.json": "",
            "sub-control01_task-nback_events.tsv": "",
            "sub-control01_task-nback_physio.tsv.gz": "",
            "sub-control01_task-nback_physio.json": "",
            "sub-control01_task-nback_sbref.nii.gz": "",
            },
        "dwi":{
            "sub-control01_dwi.nii.gz": "",
            "sub-control01_dwi.bval": "",
            "sub-control01_dwi.bvec": "",
            },
        "fmap":{
            "sub-control01_phasediff.nii.gz": "",
            "sub-control01_phasediff.json": "",
            "sub-control01_magnitude1.nii.gz": "",
            }
        },
    "code": {
        "deface.py": ""
        },
    "derivatives": {},
    "README": "",
    "participants.tsv": "",
    "dataset_description.json": "",
    "CHANGES": "",
    }
) }}

## Unspecified data

Additional files and directories containing raw data MAY be added as needed for
special cases.
All non-standard file entities SHOULD conform to BIDS-style naming conventions, including
alphabetic entities and suffixes and alphanumeric labels/indices.
Non-standard suffixes SHOULD reflect the nature of the data, and existing
entities SHOULD be used when appropriate.
For example, an ASSET calibration scan might be named
`sub-01_acq-ASSET_calibration.nii.gz`.

Non-standard files and directories should be named with care.
Future BIDS efforts may standardize new entities and suffixes, changing the
meaning of filenames and setting requirements on their contents or metadata.
Validation and parsing tools MAY treat the presence of non-standard files and
directories as an error, so consult the details of these tools for mechanisms
to suppress warnings or provide interpretations of your filenames.

<!-- Link Definitions -->

[dataset-description]: 03-modality-agnostic-files.md#dataset-description

[derived-dataset-description]: 03-modality-agnostic-files.md#derived-dataset-and-pipeline-description

[deprecated]: ./02-common-principles.md#definitions
