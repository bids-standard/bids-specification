# Task events

Template:

```Text
sub-<label>/[ses-<label>]
    func/
        <matches>_events.tsv
        <matches>_events.json
```

Where `<matches>` corresponds to task file name. For example:
`sub-control01_task-nback`. It is also possible to have a single \_events.tsv
file describing events for all participants and runs (see [Inheritance Principle](../02-common-principles.md#the-inheritance-principle)).
As with all other tabular data, `_events` files may be
accompanied by a JSON file describing the columns in detail (see [here](../02-common-principles.md#tabular-files)).

The purpose of this file is to describe timing and other properties of events
recorded during the scan. Events MAY be either stimuli presented to the
participant or participant responses. A single event file MAY include any
combination of stimuli and response events. Events MAY overlap in time. Please
mind that this does not imply that only so called "event related" study designs
are supported (in contrast to "block" designs) - each "block of events" can be
represented by an individual row in the \_events.tsv file (with a long
duration). Each task events file REQUIRES a corresponding task imaging data file
(but a single events file MAY be shared by multiple imaging data files - see
Inheritance principle). The tabular files consists of one row per event and a set of
REQUIRED and OPTIONAL columns:

| Column name   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
|-----------------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| onset         | REQUIRED. Onset (in seconds) of the event measured from the beginning of the acquisition of the first volume in the corresponding task imaging data file. If any acquired scans have been discarded before forming the imaging data file, ensure that a time of 0 corresponds to the first image stored. In other words negative numbers in "onset" are allowed<sup>5</sup>.                                                                                                     |
| duration      | REQUIRED. Duration of the event (measured from onset) in seconds. Must always be either zero or positive. A "duration" value of zero implies that the delta function or event is so short as to be effectively modeled as an impulse.                                                                                                                                                                                                                                            |
| sample        | OPTIONAL. Onset of the event according to the sampling scheme of the recorded modality (i.e., referring to the raw data file that the `events.tsv` file accompanies).                                                                                                                                                                                                                                                                                                            |
| trial_type    | OPTIONAL. Primary categorisation of each trial to identify them as instances of the experimental conditions. For example: for a response inhibition task, it could take on values "go" and "no-go" to refer to response initiation and response inhibition experimental conditions.                                                                                                                                                                                              |
| response_time | OPTIONAL. Response time measured in seconds. A negative response time can be used to represent preemptive responses and "n/a" denotes a missed response.                                                                                                                                                                                                                                                                                                                         |
| stim_file     | OPTIONAL. Represents the location of the stimulus file (image, video, sound etc.) presented at the given onset time. There are no restrictions on the file formats of the stimuli files, but they should be stored in the /stimuli folder (under the root folder of the dataset; with optional subfolders). The values under the stim_file column correspond to a path relative to "/stimuli". For example "images/cat03.jpg" will be translated to "/stimuli/images/cat03.jpg". |
| value         | OPTIONAL. Marker value associated with the event (e.g., the value of a TTL trigger that was recorded at the onset of the event).                                                                                                                                                                                                                                                                                                                                                 |
| HED           | OPTIONAL. Hierarchical Event Descriptor (HED) Tag. See [Appendix III](../99-appendices/03-hed.md) for details.                                                                                                                                                                                                                                                                                                                                                                   |

<sup>5</sup> For example in case there is an in scanner training phase that
begins before the scanning sequence has started events from this sequence should
have negative onset time counting down to the beginning of the acquisition of
the first volume.

An arbitrary number of additional columns can be added. Those allow describing
other properties of events that could be later referred in modelling and
hypothesis extensions of BIDS. Note that any additional columns in a TSV file
SHOULD be documented in an accompanying JSON sidecar file.

In case of multi-echo task run, a single `_events.tsv` file will suffice for all
echoes.

Example:

```Text
sub-control01/
    func/
        sub-control01_task-stopsignal_events.tsv
```

```Text
onset duration  trial_type  response_time stim_file
1.2 0.6 go  1.435 images/red_square.jpg
5.6 0.6 stop  1.739 images/blue_square.jpg
```

References to existing databases can also be encoded using additional columns.
Example 2 includes references to the Karolinska Directed Emotional Faces (KDEF)
database<sup>6</sup>:

<sup>6</sup>[http://www.emotionlab.se/resources/kdef](http://www.emotionlab.se/resources/kdef)

Example:

```Text
sub-control01/
    func/
        sub-control01_task-emoface_events.tsv
```

```Text
onset duration  trial_type  identifier  database  response_time
1.2 0.6 afraid  AF01AFAF  kdef  1.435
5.6 0.6 angry AM01AFAN  kdef  1.739
5.6 0.6 sad AF01ANSA  kdef  1.739
```

For multi-echo files events.tsv file is applicable to all echos of particular
run:

```Text
sub-01_task-cuedSGT_run-1_events.tsv
sub-01_task-cuedSGT_run-1_echo-1_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-2_bold.nii.gz
sub-01_task-cuedSGT_run-1_echo-3_bold.nii.gz
```
