# Common principles

## Definitions

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be
interpreted as described in [[RFC2119](https://www.ietf.org/rfc/rfc2119.txt)].

Throughout this specification we use a list of terms and abbreviations. To avoid
misunderstanding we clarify them here.

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___define_common_principles() }}

## Entities

An "entity" is an attribute that can be associated with a file, contributing
to the identification of that file as a component of its filename in the
form of a hyphen-separated key-value pair.

Each entity has the following attributes:

1.  *Name*: A comprehensive name describing the context of information
    to be provided via the entity.

1.  *Key*: A short string, typically a compression of the entity name,
    which uniquely identifies the entity when part of a filename.

1.  *Value type*: The requisite form of the value that gets specified
    alongside the key whenever the entity appears in a filename.
    For each entity, the value is of one of two possible types:

    1.  *Index*: A non-negative integer, potentially zero-padded for
        consistent width.

    1.  *Label*: An alphanumeric string.
        Note that labels MUST not collide when casing is ignored
        (see [Case collision intolerance](#case-collision-intolerance)).

The entity *format* is a string that prescribes how the entity appears within
any given filename.
For a hypothetical entity with key "`key`", the format can be either
"`key-<index>`" or "`key-<label>`", depending on the value type of that entity.

An entity *instance* is the specific manifestation of an entity within the
name of a specific file, based on the format of the entity but with a value
that provides identifying information to the particular file in whose name
it appears.

Depending on context, any one of the entity name, key, format, or a specific
entity instance, may be referred to as simply an "entity".

"Subject", "session", "sample", "task", and "run" from the list of definitions
above are all examples of entities.
The comprehensive list of supported entities is defined in
[Appendix IX](99-appendices/09-entities.md);
further, whether each is OPTIONAL, REQUIRED, or MUST NOT be provided for
various data files, as well as their relative ordering in a filename, are
defined in the Entity Table in
[Appendix IV](99-appendices/04-entity-table.md).

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

It is RECOMMENDED that non-compulsory metadata fields (like `notch` in `channels.tsv` files)
and/or files (like `events.tsv`) are fully omitted *when they are unavailable or unapplicable*,
instead of specified with an `n/a` value, or included as an empty file
(for example an empty `events.tsv` file with only the headers included).

## Filesystem structure

Data for each subject are placed in sub-directories named "`sub-<label>`",
where string "`<label>`" is substituted with the unique identification
label of each subject.
Additional information on each participant MAY be provided in a
[participants file](03-modality-agnostic-files.md#participants-file)
in the root directory of the dataset.

If data for the subject were acquired across multiple sessions, then within
the subject directory resides sub-directories named "`ses-<label>`",
where string "`<label>`" is substituted with a unique identification
label for each session.
In datasets where at least one subject has more than one session, this
additional sub-directory later SHOULD be added for all subjects in the dataset.
Additional information on each session MAY be provided in a
[sessions file](03-modality-agnostic-files.md#sessions-file)
within the subject directory.

Within the session sub-directory (or the subject sub-directory if no
session sub-directories are present) are sub-directories named according to
data type as defined above.
A data type directory SHOULD NOT be defined if there are no files to be placed
in that directory.

## Filenames

A filename consists of a chain of *entity instances* and a *suffix*
all separated by underscores, and an *extension*.
This pattern forms filenames that are both human- and machine-readable.
For instance, file "`sub-01_task-rest_eeg.edf`" contains instances of the
"subject" and "task" entities, making it evident from the filename alone that it
contains resting-state data from subject `01`;
the suffix `eeg` and extension `.edf` depend on the imaging modality and the data
format, and can therefore convey further details of the file's contents.

For a data file that was collected in a given session from a given
subject, the filename MUST begin with the string `sub-<label>_ses-<label>`.
Conversely, if the session level is omitted in the directory structure, the file
name MUST begin with the string `sub-<label>`, without `ses-<label>`.

Any given entity MUST NOT appear more than once in any filename. For example,
filename "`sub-01_acq-laser_acq-uneven_electrodes.tsv`" is invalid because
it uses the "acquisition" entity twice.

In cases where an entity and a metadata field convey similar contextual
information, the presence of an entity should not be used as a replacement for
the corresponding metadata field.
For instance, in echo-planar imaging MRI, the
[`dir-<label>`](./99-appendices/09-entities.md#dir) entity MAY be used
to distinguish files with different phase-encoding directions,
but the file's `PhaseEncodingDirection` MUST be specified as metadata.

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
It is RECOMMENDED that the column names in the header of the TSV file are
written in [`snake_case`](https://en.wikipedia.org/wiki/Snake_case) with the
first letter in lower case (for example, `variable_name`, not `Variable_name`).
As for all other data in the TSV files, column names MUST be separated with tabs.
Furthermore, column names MUST NOT be blank (that is, an empty string) and MUST NOT
be duplicated within a single TSV file.
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

### Key-value files (dictionaries)

JavaScript Object Notation (JSON) files MUST be used for storing key-value
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
label, but must be included in filenames (similarly to other entities).

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
Bare DOIs such as `10.18112/openneuro.ds000001.v1.0.0` are [DEPRECATED][].

### BIDS URI

To reference files in BIDS datasets, the following URI scheme may be used:

```plain
bids:[<dataset-name>]:<relative-path>
```

The scheme component `bids` identifies a BIDS URI,
which defines a `path` component of the form `<dataset-name>:<relative-path>`.
The `dataset-name` component is an identifier for a BIDS dataset,
and the `relative-path` component is the location of a resource within that
BIDS dataset, relative to the root of that dataset.
The `relative-path` MUST NOT start with a forward-slash character (`/`).

Examples:

```plain
bids::sub-01/fmap/sub-01_dir-AP_epi.nii.gz
bids:ds000001:sub-02/anat/sub-02_T1w.nii.gz
bids:myderivatives:sub-03/func/sub-03_task-rest_space-MNI152_bold.nii.gz
```

If no dataset name is specified, the URI is relative to the current BIDS dataset.
This is made more precise in the next section.

#### Resolution of BIDS URIs

In order to resolve a BIDS URI, the dataset name must be mapped to a BIDS dataset.

The special case `""` (that is, the empty string) refers to the BIDS dataset in
which the BIDS URI is found.
The dataset root is the nearest parent directory that contains a valid
`dataset_description.json`.

All other dataset names MUST be specified in the `DatasetLinks` object in
[dataset_description.json][], which maps dataset names to URIs that point
to BIDS dataset locations.
If the scheme is omitted from a URI in `DatasetLinks`,
that path is resolved relative to the current dataset root
(see `deriv1` example, below).

BIDS URIs cannot be interpreted outside a BIDS dataset,
as they require a `dataset_description.json` file to resolve.

#### Examples

Consider this example `dataset_description.json`:

```YAML
{
    ...
    "DatasetLinks": {
        "deriv1": "derivatives/derivative1",
        "phantoms": "file:///data/phantoms",
        "ds000001": "doi:10.18112/openneuro.ds000001.v1.0.0"
    }
}
```

Here `deriv1` refers to a BIDS Derivatives dataset contained within the current
dataset, `phantoms` refers to a BIDS dataset of phantom data stored on the local
filesystem, and `ds000001` refers to a BIDS dataset that must be resolved by DOI.

Note that resolving `bids:phantoms:sub-phantom01/anat/sub-phantom01_T1w.nii.gz`
is a straightforward concatenation:
`file:///data/phantoms/sub-phantom01/anat/sub-phantom01_T1w.nii.gz`.
However, retrieving `bids:ds000001:sub-02/anat/sub-02_T1w.nii.gz` requires
first resolving the DOI, identifying the retrieval method, possibly retrieving
the entire dataset, and finally constructing a URI to the desired resource.

No protocol is currently proposed to automatically resolve all possible BIDS URIs.

#### Future statement

BIDS URIs are parsable as standard [URIs][] with scheme `bids` and path
`[<dataset-name>]:<relative-path>`.
The authority, query and fragment components are unused.
Future versions of BIDS may specify interpretations for these components,
but MUST NOT change the interpretation of a previously valid BIDS URI.
For example, a future version may specify an authority that would allow BIDS
URIs to be resolved without reference to a local `dataset_description.json`.

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
[dataset_description.json]: 03-modality-agnostic-files.md#dataset_descriptionjson
[derived-dataset-description]: 03-modality-agnostic-files.md#derived-dataset-and-pipeline-description
[deprecated]: #definitions
[uris]: #uniform-resource-indicator
