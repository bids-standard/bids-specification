# Task events

The purpose of this file is to describe timing and other properties of events
recorded during a run.
Events are, for example, stimuli presented to the participant or participant responses
(see [Definitions](../common-principles.md#definitions)).
A single event file MAY include any combination of stimulus, response, and other events.
Events MAY overlap in time.
Please mind that this does not imply that only so called "event related" study designs
are supported (in contrast to "block" designs) - each "block of events" can be
represented by an individual row in the `events.tsv` file (with a long
duration).

Template:

```Text
sub-<label>/[ses-<label>]
    <data_type>/
        <matches>_events.tsv
        <matches>_events.json
```

Where `<matches>` corresponds to task filename. For example:
`sub-control01_task-nback`.

Each task events file REQUIRES a corresponding task data file.
It is also possible to have a single `events.tsv` file describing events
for all participants and runs (see
[Inheritance Principle](../common-principles.md#the-inheritance-principle)).
As with all other tabular data, `events.tsv` files MAY be accompanied
by a JSON file describing the columns in detail
(see [Tabular Files](../common-principles.md#tabular-files)).

The tabular files consists of one row per event and a set of REQUIRED
and OPTIONAL columns:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("task.TaskEvents") }}

The content of  `events.tsv` files SHOULD be sorted by values in the `onset` column.

An arbitrary number of additional columns can be added.
Those allow describing other properties of events that could be later referenced in modeling and
hypothesis extensions of BIDS.
Note that the `trial_type` and any additional columns in a TSV file
SHOULD be documented in an accompanying JSON sidecar file.

!!! note "Regarding the precision of numeric metadata"

    For the precision of numeric metadata,
    it is RECOMMENDENDED that dataset curators specify numeric metadata like `onset` and
    `duration` with as much decimal precision as is reasonable in the context of the experiment.
    For example in an EEG experiment with devices operating at 1000 Hz sampling frequency,
    dataset curators SHOULD specify **at least** 3 figures after the decimal point.

!!! note "For fMRI data"

    For fMRI data
    if any acquired scans have been discarded before forming the imaging data file,
    ensure that an `onset` of 0 corresponds to the time the first image was stored.
    For example in case there is an in scanner training phase that
    begins before the scanning sequence has started events from this sequence should
    have negative onset time counting down to the beginning of the acquisition of
    the first volume.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-control01": {
      "func": {
         "sub-control01_task-stopsignal_events.tsv": "",
         "sub-control01_task-stopsignal_events.json": "",
         },
      },
   }
) }}

Example of the content of the TSV file:

```tsv
onset	duration	trial_type	response_time	stim_file	channel	annots
1.23	0.65	start	1.435	images/red_square.jpg	n/a	n/a
5.65	0.65	stop	1.739	images/blue_square.jpg	n/a	n/a
12.1	2.35	n/a	n/a	n/a	F,1|F,2|Cz	musc
```

In the accompanying JSON sidecar, the `trial_type` column might look as follows:

```JSON
{
    "trial_type": {
        "LongName": "Event category",
        "Description": "Indicator of type of action that is expected",
        "Levels": {
            "start": "A red square is displayed to indicate starting",
            "stop": "A blue square is displayed to indicate stopping"
        }
    },
    "channel": {
        "Description": "Channel(s) associated with the event",
        "Delimiter": "|"
    },
    "annots": {
        "LongName": "Annotations",
        "Description": "Annotations associated with channels indicated in the channel column.",
        "Levels": {
            "musc": "Muscle artifact. A very common, high frequency, sharp artifact that corresponds with agitation/nervousness in a patient."
        },
        "HED": {
            "musc": "EMG-artifact"
        }
    }
}
```

!!! note

    In the example above:

    1.  Only a subset of columns are described for the sake of brevity.
        In a real dataset, all other columns SHOULD also be described.

    1.  The `channel` column contains a list of values that are separated
        by a delimiter (`|`), as is declared in the `Delimiter` metadata field
        of the `events.json` file.
        Thus, the channels related to the event in the third row of the example
        are called `F,1`, `F,2`, and `Cz`.

    1.  The example contains a column called `annots`.
        This column is not defined in BIDS, and constitutes additional,
        arbitrary (that is, unofficial) metadata.
        In the present case, it is used to describe artifacts in the data,
        in reference to the `channel` column.
        The `annots` column is making use of the powerful HED system
        for documenting events, see below.

Events MAY also be documented in machine-actionable form
using HED (Hierarchical Event Descriptor) tags.
This type of documentation is particularly useful for datasets likely to be used
in event-related analyses.
See [Hierarchical Event Descriptors](../appendices/hed.md)
for additional information and examples.

For multi-echo files, the `events.tsv` file is applicable
to all echos of a particular run:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
        "sub-01_task-cuedSGT_run-1_events.tsv": "",
        "sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz": "",
        "sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz": "",
        "sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz": "",
         },
      },
   }
) }}

## Stimuli

Additional information about the stimuli can be added in the `events.tsv`
and `events.json` files.

This can be done by using a `/stimuli` directory or by reference to a stimuli database.

### Stimuli directory

The stimulus files can be added in a `/stimuli` directory
(under the root directory of the dataset; with optional subdirectories) AND using a
`stim_file` column in `events.tsv` mentioning which stimulus file was used
for a given event,

There are no restrictions on the file formats of the stimuli files,
but they should be stored in the `/stimuli` directory.

### Stimuli databases

References to existing databases can also be encoded using additional columns.
The following example includes references to the
[Karolinska Directed Emotional Faces (KDEF) database](https://www.kdef.se/).

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-control01": {
      "func": {
         "sub-control01_task-emoface_events.tsv": "",
         "sub-control01_task-emoface_events.json": "",
         },
      },
   }
) }}

Example of the content of the TSV file:

```Text
onset duration  trial_type  identifier  database  response_time
1.2 0.6 afraid  AF01AFAF  kdef  1.435
5.6 0.6 angry AM01AFAN  kdef  1.739
5.6 0.6 sad AF01ANSA  kdef  1.739
```

The `trial_type` and `identifier` columns from the `events.tsv` files might be described
in the accompanying JSON sidecar as follows:

```JSON
{
    "trial_type": {
        "LongName": "Emotion image type",
        "Description": "Type of emotional face from Karolinska database that is displayed",
        "Levels": {
            "afraid": "A face showing fear is displayed",
            "angry": "A face showing anger is displayed",
            "sad": "A face showing sadness is displayed"
        }
    },
    "identifier": {
        "LongName": "Karolinska (KDEF) database identifier",
        "Description": "ID from KDEF database used to identify the displayed image"
    }
}
```

Note that all other columns SHOULD also be described but are omitted
for the sake of brevity.

### Stimulus presentation details

It is RECOMMENDED to include details of the stimulus presentation software,
when applicable:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("events.StimulusPresentation") }}

The object supplied for `StimulusPresentation` SHOULD include the following key-value pairs:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.StimulusPresentation") }}

The operating system description SHOULD include the following attributes:

- type (for example, Windows, macOS, Linux)
- distribution (if applicable, for example, Ubuntu, Debian, CentOS)
- the version number (for example, 18.04.5)

Examples:

- Windows 10, Version 2004
- macOS 10.15.6
- Linux Ubuntu 18.04.5

The amount of information supplied for the `OperatingSystem` SHOULD be sufficient
to re-run the code under maximally similar conditions.

The information related to stimulus presentation might be described
in the accompanying JSON sidecar as follows (based on the example of the previous section):

```JSON
{
    "trial_type": {
        "LongName":   "Emotion image type",
        "Description": "Type of emotional face from Karolinska database that is displayed",
        "Levels": {
            "afraid": "A face showing fear is displayed",
            "angry":  "A face showing anger is displayed",
            "sad":    "A face showing sadness is displayed"
        }
    },
    "identifier": {
        "LongName": "Unique identifier from Karolinska (KDEF) database",
        "Description": "ID from KDEF database used to identify the displayed image"
    },
    "StimulusPresentation": {
        "OperatingSystem": "Linux Ubuntu 18.04.5",
        "SoftwareName": "Psychtoolbox",
        "SoftwareRRID": "SCR_002881",
        "SoftwareVersion": "3.0.14",
        "Code": "doi:10.5281/zenodo.3361717",
        "ScreenDistance": 1.8,
        "ScreenRefreshRate": 60,
        "ScreenResolution": [1920, 1200],
        "ScreenSize": [0.472, 0.295],
        "HeadStabilization": "none"
    },
    "VisionCorrection": "lenses"
}
```

### Continuously-sampled, stimulus-related signals

!!! example "Example datasets"

      The following [BIDS-Examples](https://bids-standard.github.io/bids-examples/#dataset-index)
      showcase stimulus-related signals and may be used as a reference
      when curating a new dataset:

      -   ["synthetic" example dataset](https://github.com/bids-standard/bids-examples/tree/master/synthetic).

Signals related to stimuli (such as parameters of a film or audio stimuli) that are
evenly recorded at a constant sampling frequency MUST be specified using a
[compressed tabular file](../common-principles.md#compressed-tabular-files)
([TSV.GZ file](../glossary.md#tsv_gz-extensions)) and a corresponding
JSON file for storing metadata fields (see below).

Template:

```Text
sub-<label>/[ses-<label>/]
    <datatype>/
        <matches>_stim.tsv.gz
        <matches>_stim.json
```

For the template directory name, `<datatype>` can correspond to any data
recording modality.

In the template filenames, the `<matches>` part corresponds to task filename
before the suffix.
For example for the file `sub-control01_task-nback_run-1_bold.nii.gz`,
`<matches>` would correspond to `sub-control01_task-nback_run-1`.

!!! warning "Caution"

    `<matches>_stim.tsv.gz` files MUST NOT include a header line,
    as established by the [common-principles](../common-principles.md#compressed-tabular-files).
    As a result, when supplying a `<matches>_stim.tsv.gz` file, an accompanying
    `<matches>_stim.json` MUST be present to indicate the column names.

If the same continuous recording has been used for all subjects (for example in
the case where they all watched the same movie), one file placed in the
root directory (for example, `<root>/task-movie_stim.<tsv.gz|json>`) MAY be used
and will apply to all `<matches>_task-movie_<matches>_<suffix>.<ext>` files.
In the following example, the two `task-nback_stim.<json|tsv.gz>` apply
to all the `task-nback` runs across the two available subjects:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "sub-01": {
    "func": {
      "sub-01_task-nback_run-1_bold.nii.gz": "",
      "sub-01_task-nback_run-2_bold.nii.gz": "",
    },
  },
  "sub-02": {
    "func": {
      "sub-02_task-nback_run-1_bold.nii.gz": "",
      "sub-02_task-nback_run-2_bold.nii.gz": "",
    },
  },
  "task-nback_stim.json": "",
  "task-nback_stim.tsv.gz": "",
}) }}

The following table specifies metadata fields for the
`<matches>_stim.json` file.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table(["continuous.Continuous"]) }}

Additional metadata may be included as in
[any TSV file](../common-principles.md#tabular-files) to specify, for
example, the units of the recorded time series for each column.

## Standardization of Stimulus Files and Annotations

To ensure consistency and facilitate reuse, the BIDS specifications provide guidelines for standardizing stimulus files and their annotations. This section outlines the recommended practices for storing and referencing stimulus files within a BIDS dataset.

### Storing Stimulus Files

Stimulus files should be stored in the `/stimuli` directory under the root directory of the dataset. The `/stimuli` directory can contain subdirectories to organize the stimulus files. There are no restrictions on the file formats of the stimulus files.

Example directory structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "stimuli": {
    "images": {
      "cat01.jpg": "",
      "cat02.jpg": "",
    },
    "videos": {
      "movie01.mp4": "",
      "movie02.mp4": "",
    },
  },
}) }}

### Referencing Stimulus Files in `events.tsv`

To reference stimulus files in the `events.tsv` file, use the `stim_file` column. The values in the `stim_file` column should represent the relative path to the stimulus file within the `/stimuli` directory.

Example `events.tsv` file:

```Text
onset	duration	trial_type	response_time	stim_file
1.23	0.65	start	1.435	images/cat01.jpg
5.65	0.65	stop	1.739	images/cat02.jpg
12.1	2.35	n/a	n/a	videos/movie01.mp4
```

In the accompanying JSON sidecar, the `stim_file` column might be described as follows:

```JSON
{
    "stim_file": {
        "LongName": "Stimulus file",
        "Description": "Represents the location of the stimulus file (such as an image, video, or audio file) presented at the given onset time. The values correspond to a path relative to the /stimuli directory."
    }
}
```

### Referencing Stimulus Identifiers in `events.tsv`

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column. The `stim_id` corresponds to the unique identifier of the stimulus files and their annotations stored under the `/stimuli` directory. This allows linking each event to multiple related files associated with that stimulus.

Example `events.tsv` file:

```Text
onset	duration	trial_type	response_time	stim_id
1.23	0.65	start	1.435	stim-face01
5.65	0.65	stop	1.739	stim-face02
12.1	2.35	n/a	n/a	stim-video01
```

In the accompanying JSON sidecar, the `stim_id` column might be described as follows:

```JSON
{
    "stim_id": {
        "LongName": "Stimulus identifier",
        "Description": "Represents a unique identifier for the stimulus presented at the given onset time. Links to files and annotations in the /stimuli directory."
    }
}
```

The `stim_id` in the events file links to corresponding files:

```Text
stimuli/
├── stim-face01_image.jpg
├── stim-face01_image.json
├── stim-face01_annotations.tsv
├── stim-face02_image.jpg
├── stim-face02_image.json
├── stim-face02_annotations.tsv
├── stim-face02_annotations.tsv
├── stimuli.tsv
└── stimuli.json
```

By using `stim_id`, multiple annotations and stimulus files associated with the same identifier can be efficiently linked to events in the `events.tsv` file. The `stim_id` is a unique identifier for the stimulus that can be used to reference the stimulus files, annotations, and metadata stored in `stimuli.tsv` and `stimuli.json`. For more information on the structure of stimulus files and annotations, refer to the [Stimuli](./stimuli.md) BIDS specifications.

### Advantages of Standardization

Standardizing stimulus files and their annotations within the BIDS specifications offers several advantages:

1. **Consistency**: Ensures that stimulus files are stored and referenced in a consistent manner across different datasets.
2. **Reusability**: Facilitates the reuse of stimulus files and annotations in other studies by providing a standardized structure.
3. **Efficiency**: Reduces redundancy by avoiding the need to replicate annotations across subjects, modalities, tasks, and runs.
4. **Flexibility**: Allows for easy modification of annotations by updating a single file, enabling the reuse of datasets with alternative annotations.

By following these guidelines, researchers can enhance the interoperability and reproducibility of their studies, making it easier to share and reuse data within the scientific community.
