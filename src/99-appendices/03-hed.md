# Appendix III: Hierarchical Event Descriptors

Hierarchical Event Descriptors (HED) are a controlled vocabulary of terms describing
events in a machine-actionable form so that algorithms can use the information without
manual recoding.
HED annotation can be used to describe any experimental events by combining
information from the dataset's `_events.tsv` files and `_events.json` sidecars.

## HED annotations and vocabulary

A HED annotation consists of terms selected from a controlled
hierarchical vocabulary (the HED schema).
Individual terms are comma-separated and may be grouped using parentheses to indicate
association.
See [https://www.hedtags.org/display_hed.html](https://www.hedtags.org/display_hed.html)
to view the HED schema and the
[HED documentation](https://hed-specification.readthedocs.io/en/latest/index.html)
for additional resources.

Starting with HED version 8.0.0, HED allows users to annotate using individual
terms or partial paths in the HED vocabulary (for example `Red` or `Visual-presentation`)
rather than the full paths in the HED hierarchy (
`Property/Sensory-property/Sensory-attribute/Visual-attribute/Color/CSS-color/Red-color/Red`
or
`Property/Sensory-property/Sensory-presentation/Visual-presentation`).

HED specific tools MUST treat the short and long HED tag forms interchangeably,
converting between the forms when necessary, based on the HED schema.
Examples of test datasets using the various forms can be found in
[hed-examples/datasets](https://github.com/hed-standard/hed-examples/tree/main/datasets)
on GitHub.
**Using the short form for tags is strongly RECOMMENDED whenever possible**.

## Annotating events

Event-related data in BIDS appears in tab-separated value (`events.tsv`)
files in various places in the dataset hierarchy
(see [Events](../04-modality-specific-files/05-task-events.md)).

`events.tsv` files MUST have `onset` and `duration` columns.
Dataset curators MAY also include additional columns and define their
meanings in associated JSON sidecar files (`events.json`).

Example: An excerpt from an `events.tsv` file containing three columns
(`trial_type`, `response_time`, and `stim_file`) in addition to
the required `onset` and `duration` columns.

```Text
onset  duration  trial_type  response_time stim_file
1.2    0.6       go          1.435         images/red_square.jpg
5.6    0.6       stop        1.739         images/blue_square.jpg
```

The `trial_type` column in the above example contains a limited number of distinct
values (`go` and `stop`).
This type of column is referred to as a *categorical* column,
and the column's meaning can be annotated by assigning HED tags to describe
each of these distinct values.
The JSON sidecar provides a [JSON object](https://www.json.org/json-en.html) of annotations for these categorical values.
That is, the object is a dictionary mapping the categorical values to corresponding HED annotations.

In contrast, the `response_time` and `stim_file` columns could potentially contain
distinct values in every row.
These columns are referred to as *value* columns and are annotated by creating
a HED tag string to describe a general pattern for these values.
The HED annotation for a value column must include a `#` placeholder,
which dedicated HED tools MUST replace by the actual column value when the annotations
are assembled for analysis.

Example: An accompanying `events.json` sidecar describing both categorical and
value columns of the previous example.
The `duration` column is also annotated as a value column.

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

Dedicated HED tools MUST assemble an annotation for each event by concatenating the
annotations for each column.

Example: The fully assembled annotation for the first event in the above
`events.tsv` file with onset `1.2` (the first row) is:

```Text
Duration/0.6 s, Sensory-event, Visual-presentation,
((Square, Blue), (Computer-screen, Center-of)),
(Delay/1.435 ms, Agent-action,
(Experiment-participant, (Press, Mouse-button))),
Pathname/images/red_square.jpg
```

## Annotation using the `HED` column

Another tagging strategy is to annotate individual events directly by
including a `HED` column in the `events.tsv` file.
This approach is necessary when each event has annotations that are unique
and do not fit into a standard set of patterns.

Some acquisition or presentation software systems directly
write annotations during the experiment, and these MAY also be placed in the
`HED` column of the `events.tsv` file.

Dedicated HED tools that assemble the full annotation for events treat MUST not distinguish
between HED annotations extracted from `_events.json` sidecars and those
appearing in the `HED` column of `_events.tsv` files.
The HED strings from all sources are concatenated to form the final
event annotations.

Annotations placed in sidecars are the RECOMMENDED way
to annotate data using HED.
These annnotations are preferred to those placed
directly in the `HED` column, because they are simpler, more compact,
more easily edited, and less prone to inconsistencies.

## HED and the BIDS inheritance principle

Most studies have event files whose columns contain categorical and
numerical values that are similar across the recordings in the study.
If possible, users should annotate these columns in a single
`events.json` sidecar placed at the top level in the dataset.

If some recordings in the dataset have a column whose values deviate from a
standard pattern, then the annotations for that column MUST be placed in
sidecars located deeper in the dataset directory hierarchy.
According to the BIDS [Inheritance Principle](../02-common-principles.md#the-inheritance-principle),
once a column key in a sidecar (that is, the column name found in the `events.tsv` files) is set,
information about that column cannot be overridden by a sidecar appearing in a directory
closer to the dataset root.

## HED schema versions

The HED vocabulary is specified by a HED schema,
which delineates the allowed HED path strings.
The version of HED used in tagging a dataset should be provided in the `HEDVersion`
field of the `dataset_description.json` file located in the dataset root directory.
This allows for a proper validation of the HED annotations
(for example using the `bids-validator`).

Example: The following `dataset_description.json` file specifies that the
[`HED8.1.0.xml`](https://github.com/hed-standard/hed-specification/tree/master/hedxml/HED8.1.0.xml)
file from the `hedxml` directory of the
[`hed-specification`](https://github.com/hed-standard/hed-specification)
repository on GitHub should be used to validate the study event annotations.

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.7.0",
  "HEDVersion": "8.1.0"
}
```

If you omit the `HEDVersion` field from the dataset description file,
any present HED information will be validated using the latest version of the HED schema,
which is bound to result in problems.
Hence, it is strongly RECOMMENDED that the `HEDVersion` field be included when using HED
in a BIDS dataset.

### Using HED library schemas

HED also allows you to use one or more specialized vocabularies along with
the base vocabulary. These specialized vocabularies are developed by
communities of users and are available in the GitHub
[hed-schema-library](https://github.com/hed-standard/hed-schema-library) repository.

Example: The following `dataset_description.json` file specifies that the
[`HED8.1.0.xml`](https://github.com/hed-standard/hed-specification/tree/master/hedxml/HED8.1.0.xml)
base schema should be used along with the
SCORE library for clinical neurological annotation and a test library
located at [HED_score_0.0.1.xml](https://github.com/hed-standard/hed-schema-library/blob/main/library_schemas/score/hedxml/HED_score_0.0.1.xml) and [HED_testlib_1.0.2.xml](https://github.com/hed-standard/hed-schema-library/blob/main/library_schemas/testlib/hedxml/HED_testlib_1.0.2.xml), respectively.

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.7.0",
  "HEDVersion": {
      "base": "8.1.0",
      "libraries": {
          "sc": "score_0.0.1",
          "ts": "testlib_1.0.2"
      }
  }
}
```
The `sc:` and `ts:` are user-chosen prefixes used to distinguish the sources
of the terms in the HED annotation. In the following HED annotation:

```Text
Data-feature, sc:Photmyogenic-response, sc:Wicket-spikes
```

The tag `Data-feature` is from HED8.1.0,
while `Photmyogenic-response` and `Wicket-spikes` are from HED_score_0.0.1.