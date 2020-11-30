# Appendix III: Hierarchical Event Descriptors

Hierarchical Event Descriptors (HED) are a controlled vocabulary of terms describing
events in a machine-actionable form so that algorithms can use the information without
manual recoding.
HED was originally developed with EEG in mind, but is applicable to
all behavioral experiments.

Each level of a hierarchical tag is delimited with a forward slash (`/`).
A HED string contains one or more HED tags separated by commas (`,`).
Parentheses (brackets, `()`) group tags and enable specification of multiple items
and their attributes in a single **HED string** (see section 2.4 in
[HED Tagging Strategy Guide](https://www.hedtags.org/downloads/HED%20Tagging%20Strategy%20Guide.pdf)).
For more information about HED and tools available to validate and match HED
strings, please visit [www.hedtags.org](https://www.hedtags.org).
Since dedicated fields already exist for the overall task classification in the
sidecar JSON files (`CogAtlasID` and `CogPOID`), HED tags from the `Paradigm`
HED subcategory should not be used to annotate events.

## Annotating each event

There are several ways to associate HED annotations with events within the BIDS
framework.
The most direct way is to use the `HED` column of the `*_events.tsv`
file to annotate events.

Example: An `*_events.tsv` annotated using HED tags for individual events.

```Text
onset  duration  HED
1.1    n/a       Event/Category/Experimental stimulus, Event/Label/CrossFix,  Sensory presentation/Visual, Item/Object/2D Shape/Cross
1.3    n/a       Event/Category/Participant response, Event/Label/ButtonPress, Action/Button press
...
```

The direct approach requires that each line in the events file be annotated.
Since there are typically thousands of events in each experiment,
this method of annotation is not convenient unless the annotations are
automatically generated.
Usually annotations that appear in the `HED` column are specific to each individual event.
Information that is common to groups of events can be annotated by category.
Numerical values associated with each event can be annotated by value type.
Annotating by category and by valuegreatly reduces the effort required to HED tag
data and improves the clarity for data users.

## Annotating events by categories

In many experiments, the event instances fall into a much smaller number of
categories, and often these categories are labeled with numerical codes or short names.
This categorical information usually corresponds to one or more columns in `*_events.tsv`
representing categorical values.
Instead of tagging this information for each individual event,
you can assign HED tags for each distinct categorical value
in an accompanying `*_events.json` sidecar and allow the analysis tools to make
the association with individual event instances during analysis.
The column name in the `*_events.tsv` identifies the type of categorical variable.
The following `*_events.tsv` file has one categorical variable called `mycodes` that
takes on three possible values: `Fixation`, `Button`, and `Target`.

Example: An `*_events.tsv` containing the `mycodes` categorical column.

```Text
onset  duration  mycodes
1.1    n/a       Fixation
1.3    n/a       Button
1.8    n/a       Target
...

```

Example: An accompanying `*_events.json` sidecar describing the `mycodes` categorical variable.

```JSON
{
   "mycodes": {
       "LongName": "Local event type names",
       "Description": "Main types of events that comprise a trial",
       "Levels": {
          "Fixation": "Fixation cross is displayed",
          "Target": "Target image appears",
          "Button": "Subject presses a button"
       },
       "HED": {
           "Fixation": "Event/Category/Experimental stimulus, Event/Label/CrossFix,
               Event/Description/A cross appears at screen center to serve as a fixation point,
               Sensory presentation/Visual, Item/Object/2D Shape/Cross,
               Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen,
               Attribute/Location/Screen/Center",
           "Target": "Event/Label/TargetImage, Event/Category/Experimental stimulus,
               Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed.,
               Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target,
               Sensory presentation/Visual/Rendering type/Screen/2D),
               (Item/Natural scene/Aerial/Satellite,
               Sensory presentation/Visual/Rendering type/Screen/2D)",
           "Button": "Event/Category/Participant response, Event/Label/PressButton,
               Event/Description/The participant presses the button as soon as the target is visible,
               Action/Button press"
        }
   }
}
```

## Annotating events by value type

Each column of `*_events.tsv` containing non-categorical values usually represents a
particular type of data, for example the `speed` of a stimulus object across the
screen or the file name of the stimulus image.
These variables could be annotated in the HED column of `*_events.tsv`.
However, that approach requires repeating the values appearing in the individual
columns in the HED column.
A better approach is to annotate the type of value contained in each of these
columns in the `*_events.json` sidecar.
Value variables are annotated in a manner similar to categorical values,
except that the HED string must contain exactly one `#` specifying a placeholder
for the actual column values.
Tools are responsible for substituting the actual column values for the `#` during analysis.

Example: An `*_events.tsv` containing a categorical column (`trial_type`) and two value
columns (`response_time` and `stim_file`).

```Text
onset  duration  trial_type  response_time stim_file
1.2    0.6       go          1.435         images/red_square.jpg
5.6    0.6       stop        1.739         images/blue_square.jpg
```
Example: An accompanying `*_events.json` sidecar describing both categorical and value columns.

```JSON
{
   "trial_type": {
       "LongName": "Event category",
       "Description": "Indicator of type of action that is expected",
       "Levels": {
          "go": "A red square is displayed to indicate starting",
          "stop": "A blue square is displayed to indicate stopping",
       },
       "HED": {
          "go": "Event/Category/Experimental stimulus, Event/Label/RedSquare,
          Event/Description/A red square is displayed to indicate starting,
          Sensory presentation/Visual, Item/Object/2D Shape/Square,
          Attribute/Visual/Color/Red, Attribute/Visual/Rendering type/Screen,
          Attribute/Location/Screen/Center",
          "stop": "Event/Category/Experimental stimulus, Event/Label/BlueSquare,
          Event/Description/A blue square is displayed to indicate stopping,
          Sensory presentation/Visual, Item/Object/2D Shape/Square,
          Attribute/Visual/Color/Blue, Attribute/Visual/Rendering type/Screen,
          Attribute/Location/Screen/Center",
       }
   },
   "response_time": {
       "LongName": "Response time after stimulus",
       "Description": "Time from stimulus presentation until subject presses button",
       "Units": "ms",
       "HED": "Attribute/Response start delay/# ms, Action/Button press"
   },
   "stim_file": {
       "LongName": "Stimulus file name",
       "Description": "Relative path of the stimulus image file",
       "HED": "Attribute/File/#"
   }
}
```

## Best practices

Most studies will have event categorical variables and value variables that
are common across many of the datasets in the study.
You should try to annotate these columns in a `*_events.json` sidecar
as high in the study hierarchy as possible to avoid duplicate annotations.
Annotations that can be placed in sidecars are preferred to those placed
directly in the HED column, because they are simpler, more compact, and
less prone to inconsistent annotation.
Downstream tools should not distinguish between tags specified using
the explicit HED column and the categorical specifications, but should
form the union before analysis.
Further, the [inheritance principle](../02-common-principles.md#the-inheritance-principle)
applies, so the data dictionaries can appear higher in the BIDS hierarchy.

You should try to annotate in as much detail as possible.
The HED path structure makes it easy for analysis tools to extract tags
at different levels of detail: For example a user can consider extracting
events associated with 2D shapes for stimuli, ignoring the particular
color or shape details for the stimuli.

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
`HED7.1.1.xml` from the [hed-specification](https://github.com/hed-standard/hed-specification/tree/master/hedxml) repository
should be used to validate the study event annotations.

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.4.0",
  "HEDVersion": "7.1.1"
}
```
