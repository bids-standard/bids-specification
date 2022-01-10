# Appendix III: Hierarchical Event Descriptors

Hierarchical Event Descriptors (HED) are a controlled vocabulary of terms describing
events in a machine-actionable form so that algorithms can use the information without
manual recoding.
HED annotation can be used to describe any experimental events by combining
information from the dataset's `_events.tsv` files and `_events.json` sidecars.

## HED annotations and vocabulary.

A HED annotation consists of terms selected from a controlled 
hierarchical vocabulary (the HED schema). 
Individual terms are comma-separated and may be grouped using parentheses to indicate
association. 
See [https://www.hedtags.org/display_hed.html](https://www.hedtags.org/display_hed.html)
to view the HED schema and the
[HED documentation](https://hed-specification.readthedocs.io/en/latest/index.html)
for additional resources. HED annotations

## Annotating each event

BIDS events appear in tab-separated value (`_events.tsv`)
files in various places in the dataset hierarchy. 
BIDS event files must have `onset` and a `duration` columns. 
BIDS allows the user to include additional columns and to define their
meanings in associated JSON sidecar files (`_events.json`).

Example: An excerpt from an `*_events.tsv` containing three columns in addition to
the required `onset` and `duration` columns.

```Text
onset  duration  trial_type  response_time stim_file
1.2    0.6       go          1.435         images/red_square.jpg
5.6    0.6       stop        1.739         images/blue_square.jpg
```

The `trial_type` column in the above example contains a limited number of distinct
values (e.g., `go` and `stop`). 
This type of column is referred to as a *categorical* column, 
and the column's meaning can be annotated by assigning HED tags to describe
each of these distinct values. 
The JSON sidecar provides a dictionary of annotations for these categorical values.

In contrast, the `response_time` and `stim_file` columns could potentially contain
distinct values in every row.
These columns are referred to as *value* columns and
are annotated by creating a HED tag string to describe the general
characteristics of these values.
The HED string must include a `#` placeholder which tools will replace by the actual
column value when the annotations are assembled for analysis.

Example: An accompanying `*_events.json` sidecar describing both categorical and
value columns of the previous example.
The `Duration` column is also annotated as a value column.

```JSON
{
  "Duration": {
    "LongName": "Image duration",
    "Description": "Duration of the image presentations",
    "Units": "s",
    "HED": "Duration/# s"
  }, 
  "trial_type": {
    "LongName": "Event category", 
    "Description": "Indicator of type of action that is expected",
    "Levels": {
      "go": "A red square is displayed to indicate starting",
      "stop": "A blue square is displayed to indicate stopping"
    }, 
    "HED": {
          "go": "Sensory-event, Visual-presentation, ((Square, Blue),(Computer-screen, Center-of))",
          "stop": "Sensory-event, Visual-presentation, ((Square, Blue), (Computer-screen, Center-of))"
       }
   },
   "response_time": {
       "LongName": "Response time after stimulus",
       "Description": "Time from stimulus presentation until subject presses button",
       "Units": "ms",
       "HED": "(Delay/# ms, Agent-action, (Experiment-participant, (Press, Mouse-button))),"
   },
   "stim_file": {
       "LongName": "Stimulus filename",
       "Description": "Relative path of the stimulus image file",
       "HED": "Pathname/#"
   }
}
```

Tools assemble an annotation for each event by concatenating the 
annotations for each column.  

Example: The full assembled annotation for the first event in the above
`_events.tsv` file with onset 1.2s is:

```
Duration/0.6 s, Sensory-event, Visual-presentation,
((Square, Blue), (Computer-screen, Center-of)),
(Delay/1.435 ms, Agent-action, 
(Experiment-participant, (Press, Mouse-button))),
Pathname/images/red_square.jpg

```

## Annotation using the `HED` column

Another tagging strategy is to annotate individual events directly by
including a `HED` column in the `_events.tsv`. 
This approach is necessary when each event has annotations that are unique
and do not fit into a standard set of patterns. 
Some acquisition/presentation software systems directly
write annotations during the experiment, and these might also be placed in the
`HED` column of the `_events.tsv` file.
Tools that assemble the full annotation for events treat do not distinguish
between HED annotations extracted from `_events.json` sidecars and those 
appearing in the `HED` column of `_events.tsv` files. 
The HED strings from all sources are concatenated to form the final 
event annotations.

Annotations placed in sidecars are preferred to those placed
directly in the `HED` column, because they are simpler, more compact, 
more easily edited, and less prone to inconsistent annotation.

## HED and the BIDS inheritance principle

Most studies have event files whose columns contain categorical and 
numerical values that are similar across the recordings in the study.
Ideally, these columns should be annotated in a single `*_events.json` sidecar
placed at the top level in the dataset.
If some recordings in the dataset have a column whose values deviate from a
standard pattern, then the annotations for that column MUST be placed in
sidecars at lower levels in the hierarchy.
According to the BIDS [inheritance principle](../02-common-principles.md#the-inheritance-principle), 
once a column key in a sidecar (e.g. the column name found in the `_events.tsv` files)
is set, it cannot be unset.

## HED schema and HED versions

The HED vocabulary is specified by a HED schema,
which delineates the allowed HED path strings. 
By default, BIDS uses the latest HED schema available in the
[hed-specification](https://github.com/hed-standard/hed-specification/tree/master/hedxml) repository
maintained by the hed-standard group.

You can override the default by providing a specific HED version number in the
`dataset_description.json` file using the `HEDVersion` field.
The preferred approach is to validate with the latest version (the default),
but to use the `HEDVersion` field to specify which version was used for later reference.

Example: The following `dataset_description.json` file specifies that
`HED8.0.0.xml` from the [hed-specification](https://github.com/hed-standard/hed-specification/tree/master/hedxml) repository
should be used to validate the study event annotations.

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.4.0",
  "HEDVersion": "8.0.0"
}
```
