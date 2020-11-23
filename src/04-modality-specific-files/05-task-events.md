# Task events

Template:

```Text
sub-<label>/[ses-<label>]
    func/
        <matches>_events.tsv
        <matches>_events.json
```

Where `<matches>` corresponds to task file name. For example:
`sub-control01_task-nback`.
It is also possible to have a single `_events.tsv` file describing events
for all participants and runs (see
[Inheritance Principle](../02-common-principles.md#the-inheritance-principle)).
As with all other tabular data, `_events.tsv` files MAY be accompanied by a JSON
file describing the columns in detail (see
[Tabular Files](../02-common-principles.md#tabular-files)).

The purpose of this file is to describe timing and other properties of events
recorded during the scan.
Events MAY be either stimuli presented to the participant or participant responses.
A single event file MAY include any combination of stimuli and response events.
Events MAY overlap in time.
Please mind that this does not imply that only so called "event related" study designs
are supported (in contrast to "block" designs) - each "block of events" can be
represented by an individual row in the \_events.tsv file (with a long
duration).
Each task events file REQUIRES a corresponding task imaging data file
(but a single events file MAY be shared by multiple imaging data files - see
[Inheritance Principle](../02-common-principles.md#the-inheritance-principle)).
The tabular files consists of one row per event and a set of REQUIRED
and OPTIONAL columns:

| **Column name** | **Requirement level** | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
|-----------------|-----------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| onset           | REQUIRED              | Onset (in seconds) of the event measured from the beginning of the acquisition of the first volume in the corresponding task imaging data file. If any acquired scans have been discarded before forming the imaging data file, ensure that a time of 0 corresponds to the first image stored. In other words negative numbers in "onset" are allowed<sup>5</sup>.                                                                                                                   |
| duration        | REQUIRED              | Duration of the event (measured from onset) in seconds. Must always be either zero or positive. A "duration" value of zero implies that the delta function or event is so short as to be effectively modeled as an impulse.                                                                                                                                                                                                                                                          |
| sample          | OPTIONAL              | Onset of the event according to the sampling scheme of the recorded modality (that is, referring to the raw data file that the `events.tsv` file accompanies).                                                                                                                                                                                                                                                                                                                       |
| trial_type      | OPTIONAL              | Primary categorisation of each trial to identify them as instances of the experimental conditions. For example: for a response inhibition task, it could take on values "go" and "no-go" to refer to response initiation and response inhibition experimental conditions.                                                                                                                                                                                                            |
| response_time   | OPTIONAL              | Response time measured in seconds. A negative response time can be used to represent preemptive responses and "n/a" denotes a missed response.                                                                                                                                                                                                                                                                                                                                       |
| stim_file       | OPTIONAL              | Represents the location of the stimulus file (such as an image, video, or audio file) presented at the given onset time. There are no restrictions on the file formats of the stimuli files, but they should be stored in the /stimuli folder (under the root folder of the dataset; with optional subfolders). The values under the stim_file column correspond to a path relative to "/stimuli". For example "images/cat03.jpg" will be translated to "/stimuli/images/cat03.jpg". |
| value           | OPTIONAL              | Marker value associated with the event (for example, the value of a TTL trigger that was recorded at the onset of the event).                                                                                                                                                                                                                                                                                                                                                        |
| HED             | OPTIONAL              | Hierarchical Event Descriptor (HED) Tag. See [Appendix III](../99-appendices/03-hed.md) for details.                                                                                                                                                                                                                                                                                                                                                                                 |

<sup>5</sup> For example in case there is an in scanner training phase that
begins before the scanning sequence has started events from this sequence should
have negative onset time counting down to the beginning of the acquisition of
the first volume.

An arbitrary number of additional columns can be added. Those allow describing
other properties of events that could be later referred in modelling and
hypothesis extensions of BIDS.
Note that the `trial_type` and any additional columns in a TSV file
SHOULD be documented in an accompanying JSON sidecar file.

Example:

```Text
sub-control01/
    func/
        sub-control01_task-stopsignal_events.tsv
        sub-control01_task-stopsignal_events.json
```

Example of the content of the TSV file:

```Text
onset duration  trial_type  response_time stim_file
1.2 0.6 go  1.435 images/red_square.jpg
5.6 0.6 stop  1.739 images/blue_square.jpg
```

In the accompanying JSON sidecar, the `trial_type` column might look as follows:

```JSON
{
    "trial_type": {
        "LongName": "Event category",
        "Description": "Indicator of type of action that is expected",
        "Levels": {
            "go": "A red square is displayed to indicate starting",
            "stop": "A blue square is displayed to indicate stopping",
        }
    }
}
```

Note that all other columns SHOULD also be described but are omitted for the
sake of brevity.

For multi-echo files, the `*_events.tsv` file is applicable to all echos of
a particular run:

```Text
sub-01_task-cuedSGT_run-1_events.tsv
sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
```

## Stimuli databases

References to existing databases can also be encoded using additional columns.
The following example includes references to the
[Karolinska Directed Emotional Faces (KDEF) database](https://www.emotionlab.se/resources/kdef).

Example:

```Text
sub-control01/
    func/
        sub-control01_task-emoface_events.tsv
        sub-control01_task-emoface_events.json
```

Example of the content of the TSV file:

```Text
onset duration  trial_type  identifier  database  response_time
1.2 0.6 afraid  AF01AFAF  kdef  1.435
5.6 0.6 angry AM01AFAN  kdef  1.739
5.6 0.6 sad AF01ANSA  kdef  1.739
```

The `trial_type` and `identifier` columns from the `*_events.tsv` files might be described
in the accompanying JSON sidecar as follows:

```JSON
{
    "trial_type": {
        "LongName": "Emotion image type",
        "Descripton": "Type of emotional face from Karolinska database that is displayed",
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

## Stimulus presentation details

It is RECOMMENDED to include details of the stimulus presentation software,
when applicable:

| **Key name**         | **Requirement level** | **Data type**             | **Description**                                                                                                                                                                                                                                       |
| -------------------- | --------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| StimulusPresentation | RECOMMENDED           | [object][] of [strings][] | [Object][] containing key value pairs related to the software used to present the stimuli during the experiment, specifically: `OperatingSystem`, `SoftwareName`, `SoftwareRRID`, `SoftwareVersion` and `Code`. See table below for more information. |

The object supplied for `StimulusPresentation` SHOULD include the following key-value pairs:

| **Key name**    | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                  |
| --------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| OperatingSystem | RECOMMENDED           | [string][]    | Operating system used to run the stimuli presentation software (for formatting recommendations, see examples below this table).                                                                                  |
| SoftwareName    | RECOMMENDED           | [string][]    | Name of the software that was used to present the stimuli.                                                                                                                                                       |
| SoftwareRRID    | RECOMMENDED           | [string][]    | [Research Resource Identifier](https://scicrunch.org/resources) of the software that was used to present the stimuli. Examples: The RRID for Psychtoolbox is 'SCR_002881', and that of PsychoPy is 'SCR_006571'. |
| SoftwareVersion | RECOMMENDED           | [string][]    | Version of the software that was used to present the stimuli.                                                                                                                                                    |
| Code            | RECOMMENDED           | [string][]    | [URI][uri] of the code used to present the stimuli. Persistent identifiers such as DOIs are preferred. If multiple versions of code may be hosted at the same location, revision-specific URIs are recommended.  |

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
        "Descripton": "Type of emotional face from Karolinska database that is displayed",
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

Note: Events can also be documented in machine-actionable form using HED (Hierarchical Event Descriptor) tags.
This type of documentation is particularly useful for datasets likely to be used in event-related analyses.
See [Hierarchical Event Descriptors](../99-appendices/03-hed.md) for additional information and examples.

<!-- Link Definitions -->

[object]: https://www.json.org/json-en.html
[string]: https://www.w3schools.com/js/js_json_datatypes.asp
[strings]: https://www.w3schools.com/js/js_json_datatypes.asp
[uri]: ../02-common-principles.md#uniform-resource-indicator
