# Hierarchical Event Descriptors

Hierarchical Event Descriptors (HED) are a controlled vocabulary of terms describing
events in a machine-actionable form so that algorithms can use the information without
manual recoding.
HED annotation can be used to describe any experimental events by combining
information from the dataset's `events.tsv` files and `events.json` sidecars.

## HED annotations and vocabulary

A HED annotation consists of terms selected from a controlled
hierarchical vocabulary (the HED schema).
Individual terms are comma-separated and may be grouped using parentheses to indicate
association.
See the [HED Schema Browser](https://www.hedtags.org/display_hed.html)
to view the HED schema and the
[HED resources](https://www.hed-resources.org/en/latest/) site for additional information.

Starting with HED version 8.0.0, HED allows users to annotate using individual
terms or partial paths in the HED vocabulary (for example, `Red` or `Visual-presentation`)
rather than the full paths in the HED hierarchy (
`Property/Sensory-property/Sensory-attribute/Visual-attribute/Color/CSS-color/Red-color/Red`
or
`Property/Sensory-property/Sensory-presentation/Visual-presentation`).

HED specific tools MUST treat the short (single term) and long (full path) HED tag forms interchangeably,
converting between the forms, when necessary, based on the HED schema.
Examples of test datasets using the various forms can be found in
[hed-examples/datasets](https://github.com/hed-standard/hed-examples/tree/main/datasets)
on GitHub.
**Using the short form for tags is strongly RECOMMENDED whenever possible**.

## Annotating events

Event-related data in BIDS appears in tab-separated value (`events.tsv`)
files in various places in the dataset hierarchy
(see [Events](../modality-specific-files/task-events.md)).

`events.tsv` files MUST have `onset` and `duration` columns.
Dataset curators MAY also include additional columns and define their
meanings in associated JSON sidecar files (`events.json`).

**Example:** An excerpt from an `events.tsv` file containing three columns
(`trial_type`, `response_time`, and `stim_file`) in addition to
the required `onset` and `duration` columns.

```tsv
onset	duration	trial_type	response_time	stim_file
1.2	0.6	go	1.435	images/red_square.jpg
5.6	0.6	stop	n/a	images/blue_square.jpg
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

**Example:** An accompanying `events.json` sidecar describing both categorical and
value columns of the previous example.
The `duration` column is also annotated as a value column.

```JSON
{
  "duration": {
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
          "go": "Sensory-event, Visual-presentation, (Square, Red)",
          "stop": "Sensory-event, Visual-presentation, (Square, Blue)"
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

Dedicated HED tools MUST assemble the HED annotation for each event (row) by concatenating the
annotations for each column, along with the annotation contained directly in a `HED` column
of that row, as described in the next section.

**Example:** The fully assembled annotation for the first event in the above
`events.tsv` file with onset `1.2` (the first row) is:

```Text
Duration/0.6 s, Sensory-event, Visual-presentation,
((Square, Red), (Computer-screen, Center-of)),
(Delay/1.435 ms, Agent-action, (Experiment-participant,
(Press, Mouse-button))),
Pathname/images/red_square.jpg
```

### Annotation using the `HED` column

Another tagging strategy is to annotate individual events directly by
including a `HED` column in the `events.tsv` file.
This approach is necessary when each event has annotations that are unique
and do not fit into a standard set of patterns,
such as during manual annotation of artifacts or signal features.

Some acquisition or presentation software systems may produce
individual annotations for each event during the experiment.
These individualized annotations may be placed into the `HED` column of the `events.tsv` file
when the data is converted into BIDS format.

Dedicated HED tools that assemble the full annotation for events MUST not distinguish
between HED annotations extracted from `events.json` sidecars and those
appearing in the `HED` column of `events.tsv` files.
The HED strings from all sources are concatenated to form the final
event annotations.

Annotations placed in sidecars are the RECOMMENDED way to annotate data using HED.
These annotations are preferred to those placed
directly in the `HED` column because they are simpler, more compact,
more easily edited, and less prone to inconsistencies.

## HED and the BIDS inheritance principle

Most studies have event files whose columns contain categorical and
numerical values that are similar across the recordings in the study.
If possible, users should annotate these columns in a single
`events.json` sidecar placed at the top level in the dataset.

If some recordings in the dataset have a column whose values deviate from a
standard pattern, then the annotations for that column MUST be placed in
sidecars located deeper in the dataset directory hierarchy.
According to the BIDS [Inheritance Principle](../common-principles.md#the-inheritance-principle),
once a column key in a sidecar (that is, the column name found in the `events.tsv` files) is set,
information about that column cannot be overridden by a sidecar appearing in a directory
closer to the dataset root.

## HED schema versions

The HED vocabulary is specified by a HED schema,
which delineates the allowed HED path strings.
The version of HED used in tagging a dataset should be provided in the `HEDVersion`
field of the `dataset_description.json` file located in the dataset root directory.
This allows for properly validating the HED annotations
(for example, using the `bids-validator`).

**Example:** The following `dataset_description.json` file specifies that the
[`HED8.2.0.xml`](https://github.com/hed-standard/hed-schemas/blob/main/standard_schema/hedxml/HED8.2.0.xml)
file from the `standard_schema/hedxml` directory of the
[`hed-schemas`](https://github.com/hed-standard/hed-schemas)
repository on GitHub should be used to validate the study event annotations.

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.8.0",
  "HEDVersion": "8.2.0"
}
```

The BIDS validator will generate an error if your dataset uses HED
and the `HEDVersion` field is missing from the dataset description file.
To avoid this, include a `HEDVersion` field in the `dataset_description.json`
if you are using HED annotations.

### Using HED library schemas

HED also allows you to use one or more specialized vocabularies
along with or instead of the standard vocabulary.
These specialized vocabularies are developed by communities of users
and are available in the
[hed-schemas](https://github.com/hed-standard/hed-schemas) GitHub repository.
A library schema is specified in the form `<library-name<_>library-version>`.

#### Partnered library schemas

A partnered schema is one whose vocabulary trees are merged with
its standard schema partner when the schema is released.
Thus, the two vocabularies appear as one vocabulary to the annotator.
Partnered library schemas were introduced in HED specification version 3.2.0
and are supported by HED standard schema versions ≥ 8.2.0.
Each partnered library schema is tied to a specific version of
the HED standard schema as specified in its header.
A given library schema version is either partnered or standalone.

**Note:** Whether a particular library schema version is partnered or
unpartnered is fixed when the library is released and cannot be changed.
For example,
[HED-SCORE version 1.0.0](https://github.com/hed-standard/hed-schemas/blob/main/library_schemas/score/hedwiki/HED_score_1.0.0.mediawiki)
is unpartnered, but [HED-SCORE version 1.1.0](https://github.com/hed-standard/hed-schemas/blob/main/library_schemas/score/hedwiki/HED_score_1.1.0.mediawiki)
is partnered with standard schema version 8.2.0.

##### Unpartnered library schema example

The following `dataset_description.json` file specifies that the
[HED8.1.0.xml](https://github.com/hed-standard/hed-schemas/blob/main/standard_schema/hedxml/HED8.1.0.xml)
standard schema should be used along with the HED-SCORE library schema
for clinical neurological annotation located at
[HED_score_1.0.0.xml](https://github.com/hed-standard/hed-schemas/blob/main/library_schemas/score/hedxml/HED_score_1.0.0.xml).

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.7.0",
  "HEDVersion": ["8.1.0", "sc:score_1.0.0"]
}
```
The `sc:` is a user-chosen prefix used to distinguish the source schemas
of the terms in the HED annotation.
The prefixes MUST be alphanumeric.
Any number of prefixed schemas may be used in addition to a non-prefixed one.

The following HED annotation from this dataset uses the `sc:` prefix with
`Eye-blink-artifact` and `Seizure-PNES` because these terms are from the
HED-SCORE library schema, while `Data-feature` is from the standard HED schema.

```Text
Data-feature, sc:Eye-blink-artifact, sc:Seizure-PNES
```

##### Single unpartnered library schema example

If only one schema is used for annotation, the prefix can be omitted entirely.
The following `dataset_description.json` indicates that only the HED-SCORE library schema version
1.0.0 will be used for HED annotation in this dataset.

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.7.0",
  "HEDVersion": "score_1.0.0"
}
```

The corresponding annotations in the dataset do not have a prefix:

```Text
Eye-blink-artifact, Seizure-PNES
```

##### Partnered library schema example

The following `dataset_description.json` file specifies that
the HED-SCORE library schema
[version 1.1.0](https://github.com/hed-standard/hed-schemas/blob/main/library_schemas/score/hedwiki/HED_score_1.1.0.mediawiki) is used.
This particular library schema version is partnered with the standard schema version
[8.2.0](https://github.com/hed-standard/hed-schemas/blob/main/standard_schema/hedxml/HED8.2.0.xml).

```JSON
{
  "Name": "A great experiment",
  "BIDSVersion": "1.8.0",
  "HEDVersion": "score_1.1.0"
}
```
The corresponding annotations in the dataset use tags from the
HED-SCORE library schema (`Eye-blink-artifact` and `Seizure-PNES`) and from the standard HED (`Data-feature`)
as follows:

```Text
Data-feature, Eye-blink-artifact, Seizure-PNES
```
