# Appendix III: Hierarchical Event Descriptor (HED) Tags

Events in a given study are often annotated using study-specific codes, making it difficult to compare events across studies. Hierarchical Event Descriptor (HED) Tags (see [https://github.com/BigEEGConsortium/HED/wiki/HED-Schema](https://github.com/BigEEGConsortium/HED-schema/wiki/HED-Schema) for more details) provide a mechanism for annotating events in a study-independent way. 

HED is a controlled vocabulary of terms describing events in a behavioural paradigm. HED was originally developed with EEG in mind, but is applicable to all behavioural experiments. Each level of a hierarchical tag is delimited with a forward slash ("/"). A HED string contains one or more HED tags separated by commas. Parentheses (brackets) group tags and enable specification of multiple items and their attributes in a single HED string (see section 2.4 in [HED Tagging Strategy Guide](http://www.hedtags.org/downloads/HED%20Tagging%20Strategy%20Guide.pdf)). For more information about HED and tools available to validate and match HED strings, please visit [www.hedtags.org](http://www.hedtags.org). Since dedicated fields already exist for the overall task classification (`CogAtlasID` and `CogPOID`) in the sidecar JSON files HED tags from the Paradigm subcategory should not be used to annotate events.  

There are several ways to associate HED annotations with events within the BIDS framework.  The most direct way is to use the `HED` column of the `_events.tsv` file to annotate events:  

Example:  

```
onset  duration  HED
1.1    n/a       Event/Category/Experimental stimulus, Event/Label/CrossFix,  Sensory presentation/Visual, Item/Object/2D Shape/Cross
1.3    n/a       Event/Category/Participant response, Event/Label/ButtonPress, Action/Button press
...

```
The direct approach requires that each line in the event file be annotated. Since there are typically thousands of events in each experiment, this method of annotation is usually not convenient unless the annotations are automatically generated. In many experiments, the event instances fall into a much smaller number of categories and often these categories are labeled with numerical codes or short names. It is usually more convenient to associate the HED annotations with the categories and allow the analysis tools to make the association with individual event instances during analysis. To use this approach, your `_events.tsv` file should associate a category (often called an event code) with each event instance. Since BIDS allows an arbitrary number of columns to be included in an `event.tsv` file, you can make this association by including a column with the event category in your `_events.tsv` file.

Example:  

```
onset  duration  mycodes     HED
1.1    n/a       Fixation  
1.3    n/a       Button
1.8    n/a       Target
...

```
If you provide an `_events.json` file somewhere in your data hierarchy that has a HED map for `mycodes`. The HED tags associated with a given `mycodes` value can then be associated with the events in that category.  You may also provide a `HED` column and multiple categories.  The union of the relevant HED tags will then be associated with the event instance.

Example:  

```JSON
{
  "mycodes": {
    "HED": {
      "Fixation": "Event/Category/Experimental stimulus, Event/Label/CrossFix, Event/Description/A cross appears at screen center to serve as a fixation point, Sensory presentation/Visual, Item/Object/2D Shape/Cross, Attribute/Visual/Fixation point, Attribute/Visual/Rendering type/Screen, Attribute/Location/Screen/Center",
      "Target": "Event/Label/Target image, Event/Description/A white airplane as the RSVP target superimposed on a satellite image is displayed., Event/Category/Experimental stimulus, (Item/Object/Vehicle/Aircraft/Airplane, Participant/Effect/Cognitive/Target, Sensory presentation/Visual/Rendering type/Screen/2D), (Item/Natural scene/Arial/Satellite, Sensory presentation/Visual/Rendering type/Screen/2D)"
      "Button": ...
    }
  }
}
```

Both the event_type column and the HED column may be included for each event (i.e., as columns in "_events.tsv"). In this case, an individual event is described by the union of the tags in the HED column of events.tsv and the tags associated with the dictionary entry for the event_type specified in data dictionary "_events.json". The tags in the HED column are often specific to the event instances, while the common properties associated with the event_type are encapsulated in the event_type dictionary. Downstream tools should not distinguish between tags specified using the different mechanisms.  

Note: An "_events.tsv" file can have several named columns that have HED data dictionaries in "_events.json" files. All dictionaries should be applied.  Further, the normal BIDS inheritance rules apply so these data dictionaries can appear higher in the BIDS hierachy.  
