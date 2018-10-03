Appendix III: Hierarchical Event Descriptor (HED) Tags
------------------------------------------------------

Each event can be assigned one or more Hierarchical Event Descriptor (HED) Tag (see [https://github.com/BigEEGConsortium/HED/wiki/HED-Schema](https://github.com/BigEEGConsortium/HED-schema/wiki/HED-Schema) for more details) under the optional `HED` column.
HED is a controlled vocabulary of terms describing events in a behavioural paradigm. It was originally developed with EEG in mind, but is applicable to all behavioural experiments. Each level of the hierarchical tags are delimited with a forward slash ("/"). Multiple tags are delimited with a comma. Parentheses (brackets) group tags and enable specification of multiple items and their attributes in a single HED string (see section 2.4 in [HED Tagging Strategy Guide](http://www.hedtags.org/downloads/HED%20Tagging%20Strategy%20Guide.pdf)). For more information about HED and tools available to validate and match HED strings, please visit [www.hedtags.org](http://www.hedtags.org).

Since dedicated fields already exist for the overall task classification (`CogAtlasID` and `CogPOID`) in the sidecar JSON files HED
tags from the Paradigm subcategory should not be used to annotate
events.

Example:
```
sub-control01/
    func/
        sub-control01_task-emoface_events.tsv
```
```
onset duration  trial_type  HED
1.2 0.6 fixationCross Event/Category/Experimental stimulus, Event/Label/CrossFix, Event/Description/A cross appears at screen center to serve as a fixation point, Sensory presentation/Visual, Item/Object/2D Shape/Cross, Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen, Attribute/Location/Screen/Center
5.6 0.008 target  Event/Label/Target image, Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed., Event/Category/Experimental stimulus, (Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target, Sensory presentation/Visual/Rendering type/Screen/2D), (Item/Natural scene/Arial/Satellite, Sensory presentation/Visual/Rendering type/Screen/2D)
500 0.008 nontarget Event/Label/Non-target image, Event/Description/A non-target image is displayed for about 8 milliseconds, Event/Category/Experimental stimulus, (Item/Natural scene/Arial/Satellite, Participant/Effect/Cognitive/Expected/Non-target, Sensory presentation/Visual/Rendering type/Screen/2D), Attribute/Onset
```

Alternatively if the same HED tags apply to a group of events with the same `trial_type` they can be specified in the corresponding data dictionary (`_events.json` file) using the following syntax:

Example:
```JSON
{
  "trial_type": {
    "HED": {
      "fixationCross": "Event/Category/Experimental stimulus, Event/Label/CrossFix, Event/Description/A cross appears at screen center to serve as a fixation point, Sensory presentation/Visual, Item/Object/2D Shape/Cross, Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen, Attribute/Location/Screen/Center",
      "target": "Event/Label/Target image, Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed., Event/Category/Experimental stimulus, (Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target, Sensory presentation/Visual/Rendering type/Screen/2D), (Item/Natural scene/Arial/Satellite, Sensory presentation/Visual/Rendering type/Screen/2D)",
      "nontarget": "Event/Label/Non-target image, Event/Description/A non-target image is displayed for about 8 milliseconds, Event/Category/Experimental stimulus, (Item/Natural scene/Arial/Satellite, Participant/Effect/Cognitive/Expected/Non-target, Sensory presentation/Visual/Rendering type/Screen/2D), Attribute/Onset"
    }
  }
}
```
