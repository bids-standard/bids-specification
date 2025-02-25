# Modality agnostic files

## Dataset description

Templates:

-   `dataset_description.json`
-   `README[.md|.rst|.txt]`
-   `CITATION.cff`
-   `CHANGES`
-   `LICENSE[.md|.rst|.txt]`

### `dataset_description.json`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.dataset_description.description") }}

Every dataset MUST include this file with the following fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Name": "REQUIRED",
      "BIDSVersion": "REQUIRED",
      "HEDVersion": "RECOMMENDED",
      "DatasetLinks": "REQUIRED if [BIDS URIs][] are used",
      "DatasetType": "RECOMMENDED",
      "License": "RECOMMENDED",
      "Authors": "RECOMMENDED if CITATION.cff is not present",
      "Acknowledgements": "OPTIONAL",
      "HowToAcknowledge": "OPTIONAL",
      "Funding": "OPTIONAL",
      "EthicsApprovals": "OPTIONAL",
      "ReferencesAndLinks": "OPTIONAL",
      "DatasetDOI": "OPTIONAL",
      "GeneratedBy": "RECOMMENDED",
      "SourceDatasets": "RECOMMENDED",
   }
) }}

Each object in the `GeneratedBy` array includes the following REQUIRED, RECOMMENDED
and OPTIONAL keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.GeneratedBy.items") }}

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.6.0",
  "DatasetType": "raw",
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
  "EthicsApprovals": [
    "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. doi:1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "doi:10.0.2.3/dfjj.10",
  "HEDVersion": "8.0.0",
  "GeneratedBy": [
    {
      "Name": "reproin",
      "Version": "0.6.0",
      "Container": {
        "Type": "docker",
        "Tag": "repronim/reproin:0.6.0"
      }
    }
  ],
  "SourceDatasets": [
    {
      "URL": "s3://dicoms/studies/correlates",
      "Version": "April 11 2011"
    }
  ]
}
```

#### Derived dataset and pipeline description

As for any BIDS dataset, a `dataset_description.json` file MUST be found at the
top level of every derived dataset:
`<dataset>/derivatives/<pipeline_name>/dataset_description.json`.

In contrast to raw BIDS datasets, derived BIDS datasets MUST include a
`GeneratedBy` key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "REQUIRED"
   }
) }}

If a derived dataset is stored as a subdirectory of the raw dataset, then the `Name` field
of the first `GeneratedBy` object MUST be a substring of the derived dataset directory name.
That is, in a directory `<dataset>/derivatives/<pipeline>[-<variant>]/`, the first
`GeneratedBy` object should have a `Name` of `<pipeline>`.

Example:

```JSON
{
  "Name": "FMRIPREP Outputs",
  "BIDSVersion": "1.6.0",
  "DatasetType": "derivative",
  "GeneratedBy": [
    {
      "Name": "fmriprep",
      "Version": "1.4.1",
      "Container": {
        "Type": "docker",
        "Tag": "poldracklab/fmriprep:1.4.1"
        }
    },
    {
      "Name": "Manual",
      "Description": "Re-added RepetitionTime metadata to bold.json files"
    }
  ],
  "SourceDatasets": [
    {
      "DOI": "doi:10.18112/openneuro.ds000114.v1.0.1",
      "URL": "https://openneuro.org/datasets/ds000114/versions/1.0.1",
      "Version": "1.0.1"
    }
  ]
}
```

### `README`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.README.description") }}

### `CITATION.cff`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.CITATION.description") }}

For most redundant fields between `CITATION.cff` and `dataset_description.json`,
the `CITATION.cff` SHOULD take precedence.
To avoid inconsistency, metadata present in `CITATION.cff` SHOULD NOT be
be included in `dataset_description.json`, with the exception of `Name` and
`DatasetDOI`, to ensure that `CITATION.cff`-unaware tools can generate
references to the dataset.
In particular, if `CITATION.cff` is present,
the `"Authors"` field of `dataset_description.json` MUST be omitted,
and the `"HowToAcknowledge"`, `"License"` and `"ReferencesAndLinks"` SHOULD be omitted
in favor of the `CITATION.cff` fields `message`/`preferred-citation`, `license` and
`references`.

### `CHANGES`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.CHANGES.description") }}

Example:

```Text
1.0.1 2015-08-27
  - Fixed slice timing information.

1.0.0 2015-08-17
  - Initial release.
```

### `LICENSE`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.LICENSE.description") }}

## Participants file

Template:

```Text
participants.tsv
participants.json
```

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.participants.description") }}

We RECOMMEND to make use of these columns, and
in case that you do use them, we RECOMMEND to use the following values
for them:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Participants") }}

Throughout BIDS you can indicate missing values with `n/a` (for "not
available").

`participants.tsv` example:

```tsv
participant_id	age	sex	handedness	group
sub-01	34	M	right	read
sub-02	12	F	right	write
sub-03	33	F	n/a	read
```

It is RECOMMENDED to accompany each `participants.tsv` file with a sidecar
`participants.json` file to describe the TSV column names and properties of their values (see also
the [section on tabular files](common-principles.md#tabular-files)).
Such sidecar files are needed to interpret the data, especially so when
optional columns are defined beyond `age`, `sex`, `handedness`, `species`, `strain`,
and `strain_rrid`, such as `group` in this example, or when a different
age unit is needed (for example, gestational weeks).
If no `units` is provided for age, it will be assumed to be in years relative
to date of birth.

`participants.json` example:

```JSON
{
    "age": {
        "Description": "age of the participant",
        "Units": "year"
    },
    "sex": {
        "Description": "sex of the participant as reported by the participant",
        "Levels": {
            "M": "male",
            "F": "female"
        }
    },
    "handedness": {
        "Description": "handedness of the participant as reported by the participant",
        "Levels": {
            "left": "left",
            "right": "right"
        }
    },
    "group": {
        "Description": "experimental group the participant belonged to",
        "Levels": {
            "read": "participants who read an inspirational text before the experiment",
            "write": "participants who wrote an inspirational text before the experiment"
        }
    }
}
```

## Samples file

Template:

```Text
samples.tsv
samples.json
```

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.samples.description") }}

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Samples") }}

`samples.tsv` example:

```tsv
sample_id	participant_id	sample_type	derived_from
sample-01	sub-01	tissue	n/a
sample-02	sub-01	tissue	sample-01
sample-03	sub-01	tissue	sample-01
sample-04	sub-02	tissue	n/a
sample-05	sub-02	tissue	n/a
```

It is RECOMMENDED to accompany each `samples.tsv` file with a sidecar
`samples.json` file to describe the TSV column names and properties of their values
(see also the [section on tabular files](common-principles.md#tabular-files)).

`samples.json` example:

```JSON
{
    "sample_type": {
        "Description": "type of sample from ENCODE Biosample Type (https://www.encodeproject.org/profiles/biosample_type)",
    },
    "derived_from": {
        "Description": "sample_id from which the sample is derived"
    }
}
```

## Phenotypic and assessment data

Template:

```Text
phenotype/
    <measurement_tool_name>.tsv
    <measurement_tool_name>.json
```

Optional: Yes

If the dataset includes multiple sets of participant level measurements (for
example responses from multiple questionnaires) they can be split into
individual files separate from `participants.tsv`.

Each of the measurement files MUST be kept in a `/phenotype` directory placed
at the root of the BIDS dataset and MUST end with the `.tsv` extension.
Filenames SHOULD be chosen to reflect the contents of the file.
For example, the "Adult ADHD Clinical Diagnostic Scale" could be saved in a file
called `/phenotype/acds_adult.tsv`.

The files can include an arbitrary set of columns, but one of them MUST be
`participant_id` and the entries of that column MUST correspond to the subjects
in the BIDS dataset and `participants.tsv` file.

As with all other tabular data, the additional phenotypic information files
MAY be accompanied by a JSON file describing the columns in detail
(see [Tabular files](common-principles.md#tabular-files)).

In addition to the column descriptions, the JSON file MAY contain the following fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "MeasurementToolMetadata": "OPTIONAL",
      "Derivative": "OPTIONAL",
   }
) }}

As an example, consider the contents of a file called
`phenotype/acds_adult.json`:

```JSON
{
  "MeasurementToolMetadata": {
    "Description": "Adult ADHD Clinical Diagnostic Scale V1.2",
    "TermURL": "https://www.cognitiveatlas.org/task/id/trm_5586ff878155d"
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
  }
}
```

Please note that in this example `MeasurementToolMetadata` includes information
about the questionnaire and `adhd_b` and `adhd_c_dx` correspond to individual
columns.

In addition to the keys available to describe columns in all tabular files
(`LongName`, `Description`, `Levels`, `Units`, and `TermURL`) the
`participants.json` file as well as phenotypic files can also include column
descriptions with a `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).

## Scans file

Template:

```Text
sub-<label>/
    [ses-<label>/]
        sub-<label>[_ses-<label>]_scans.tsv
        sub-<label>[_ses-<label>]_scans.json
```

Optional: Yes

The purpose of this file is to describe timing and other properties of each recording *file* within one session.
In general, each of these files SHOULD be described by exactly one row.

For *file formats* that are based on several files of different extensions,
or a directory of files with different extensions (multi-file file formats),
only that file SHOULD be listed that would also be passed to analysis software for reading the data.
For example for BrainVision data (`.vhdr`, `.vmrk`, `.eeg`),
only the `.vhdr` SHOULD be listed;
for EEGLAB data (`.set`, `.fdt`),
only the `.set` file SHOULD be listed;
and for CTF data (`.ds`),
the whole `.ds` directory SHOULD be listed,
and not the individual files in that directory.

Some neural recordings consist of multiple parts,
that span several files,
but that share the same extension.
For example in [entity-linked file collections](./common-principles.md#entity-linked-file-collections),
commonly used for qMRI,
where recordings may be linked through entities such as `echo` and `part`
(using `.nii` or `.nii.gz` extensions).
For another example consider the case of large files in `.fif` format that are linked through the `split` entity
(see [Split files](./appendices/meg-file-formats.md#split-files)).
Such recordings MUST be documented with one row per file
(unlike the case of multi-file file formats described above).

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Scans") }}

Additional fields can include external behavioral measures relevant to the
scan.
For example vigilance questionnaire score administered after a resting
state scan.
All such included additional fields SHOULD be documented in an accompanying
`_scans.json` file that describes these fields in detail
(see [Tabular files](common-principles.md#tabular-files)).

Example `_scans.tsv`:

```tsv
filename	acq_time
func/sub-control01_task-nback_bold.nii.gz	1877-06-15T13:45:30
func/sub-control01_task-motor_bold.nii.gz	1877-06-15T13:55:33
meg/sub-control01_task-rest_split-01_meg.nii.gz	1877-06-15T12:15:27
meg/sub-control01_task-rest_split-02_meg.nii.gz	1877-06-15T12:15:27
```

## Sessions file

Template:

```Text
sub-<label>/
    sub-<label>_sessions.tsv
```

Optional: Yes

In case of multiple sessions there is an option of adding additional
`sessions.tsv` files describing variables changing between sessions.
In such case one file per participant SHOULD be added.
These files MUST include a `session_id` column and describe each session by one and only one row.
Column names in `sessions.tsv` files MUST be different from group level participant key column names in the
[`participants.tsv` file](./modality-agnostic-files.md#participants-file).

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("modality_agnostic.Sessions") }}

`_sessions.tsv` example:

```tsv
session_id	acq_time	systolic_blood_pressure
ses-predrug	2009-06-15T13:45:30	120
ses-postdrug	2009-06-16T13:45:30	100
ses-followup	2009-06-17T13:45:30	110
```

## Code

Template: `code/*`

Source code of scripts that were used to prepare the dataset MAY be stored here.
Examples include deidentification or defacing of the data, or
the conversion from the format of the source data to the BIDS format
(see [source vs. raw vs. derived data](./common-principles.md#source-vs-raw-vs-derived-data)).
Extra care should be taken to avoid including original IDs or
any identifiable information with the source code.
There are no limitations or recommendations on the language and/or
code organization of these scripts at the moment.

<!-- Link Definitions -->

[bids uris]: ./common-principles.md#bids-uri
