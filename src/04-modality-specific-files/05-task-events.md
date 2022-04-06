# Task events

The purpose of this file is to describe timing and other properties of events
recorded during a run.
Events are, for example, stimuli presented to the participant or participant responses
(see [Definitions](../02-common-principles.md#definitions)).
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
[Inheritance Principle](../02-common-principles.md#the-inheritance-principle)).
As with all other tabular data, `events.tsv` files MAY be accompanied by a JSON
file describing the columns in detail (see
[Tabular Files](../02-common-principles.md#tabular-files)).

The tabular files consists of one row per event and a set of REQUIRED
and OPTIONAL columns:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "onset": "REQUIRED",
      "duration": "REQUIRED",
      "sample": "OPTIONAL",
      "trial_type": "OPTIONAL",
      "response_time": "OPTIONAL",
      "value": "OPTIONAL",
      "HED": "OPTIONAL",
   }
) }}

<sup>5</sup> Note for MRI data:
If any acquired scans have been discarded before forming the imaging data file,
ensure that an `onset` of 0 corresponds to the time the first image was stored.
For example in case there is an in scanner training phase that
begins before the scanning sequence has started events from this sequence should
have negative onset time counting down to the beginning of the acquisition of
the first volume.

An arbitrary number of additional columns can be added. Those allow describing
other properties of events that could be later referred in modelling and
hypothesis extensions of BIDS.
Note that the `trial_type` and any additional columns in a TSV file
SHOULD be documented in an accompanying JSON sidecar file.

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

```Text
onset	duration	trial_type	response_time	stim_file
1.23	0.65	start	1.435	images/red_square.jpg
5.65	0.65	stop	1.739	images/blue_square.jpg
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
    }
}
```

Note that all other columns SHOULD also be described but are omitted for the
sake of brevity.

For multi-echo files, the `events.tsv` file is applicable to all echos of
a particular run:

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

Note: Events can also be documented in machine-actionable form
using HED (Hierarchical Event Descriptor) tags.
This type of documentation is particularly useful for datasets likely to be used
in event-related analyses.
See [Hierarchical Event Descriptors](../99-appendices/03-hed.md)
for additional information and examples.

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

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/objects/columns.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table(
   {
      "stim_file": "OPTIONAL",
   }
) }}

### Stimuli databases

References to existing databases can also be encoded using additional columns.
The following example includes references to the
[Karolinska Directed Emotional Faces (KDEF) database](https://www.emotionlab.se/resources/kdef).

Example:

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

Note that all other columns SHOULD also be described but are omitted for the
sake of brevity.

### Stimulus presentation details

It is RECOMMENDED to include details of the stimulus presentation software,
when applicable:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "StimulusPresentation": "RECOMMENDED",
   }
) }}

The object supplied for `StimulusPresentation` SHOULD include the following key-value pairs:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "OperatingSystem": "RECOMMENDED",
      "SoftwareName": "RECOMMENDED",
      "SoftwareRRID": "RECOMMENDED",
      "SoftwareVersion": "RECOMMENDED",
      "Code": "RECOMMENDED",
   }
) }}

The operating system description SHOULD include the following attributes:

-   type (for example, Windows, macOS, Linux)
-   distribution (if applicable, for example, Ubuntu, Debian, CentOS)
-   the version number (for example, 18.04.5)

Examples:

-   Windows 10, Version 2004
-   macOS 10.15.6
-   Linux Ubuntu 18.04.5

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
        "Code": "doi:10.5281/zenodo.3361717"
    }
}
```
