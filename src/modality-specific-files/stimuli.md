# Stimuli

Stimulus files should be stored in the `/stimuli` directory under the root directory of the dataset. The `/stimuli` directory can contain subdirectories to organize the stimulus files. Stimulus files SHOULD follow the BIDS naming conventions and SHOULD be referenced in the `events.tsv` file using the `stim_id` column. The `stim_id` column represents unique identifiers for the stimuli. Additional information about the stimuli and their annotations can be provided in the `stimuli.tsv`, `stimuli.json`, `annotations.tsv`, `annotations.json`, and `stim-<label>.json` files.

Standardizing stimulus files and their annotations within the BIDS specifications offers several advantages:

1. **Consistency**: Ensures that stimulus files are stored and referenced in a consistent manner across different datasets.
2. **Reusability**: Facilitates the reuse of stimulus files and annotations in other studies by providing a standardized structure.
3. **Efficiency**: Reduces redundancy by avoiding the need to replicate annotations across subjects, modalities, tasks, and runs.
4. **Flexibility**: Allows for easy modification of annotations by updating a single file, enabling the reuse of datasets with alternative annotations.

To preserve backward compatibility with existing datasets (see the Legacy section below), the use of these specifications for `/stimuli` directory and the `stim_id` column in the `events.tsv` files is RECOMMENDED but not required. Researchers are encouraged to follow these guidelines to enhance the interoperability and reproducibility of their studies.

Following these guidelines will help ensure that stimulus files and their annotations are stored and referenced in a consistent manner across different datasets, facilitating data sharing, reuse, and reproducibility.

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "stimuli": {
    "stimuli.tsv": "",
    "stimuli.json": "",
    "[stim-<label>[_part-<label>]_<suffix>.<extension>]": "",
    "[stim-<label>[_part-<label>]_<suffix>.json]": "",
    "[[stim-<label>_]annotations.tsv]": "",
    "[[stim-<label>_]annotations.json]": "",
    "[stim-<label>[_part-<label>]_annot-<label>_events.tsv]": "",
    "[stim-<label>[_part-<label>]_annot-<label>_events.json]": ""
    }
  }) }}

Note: The presence of `stimuli.tsv` file indicates that the content of the `/stimuli` folder follows this BIDS specification for stimulus organization. This structure is planned to become mandatory in BIDS 2.0.

## Referencing Stimulus Identifiers in `events.tsv`

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column. The values in the `stim_id` column should represent unique identifiers for the stimuli. Stimulus ID (`stim_id`) should correspond to the unique identifier of the stimulus file in the /stimuli directory and expands to all files (both stimulus and annotation files) that share the same stimulus ID.

Example `events.tsv` file:

| onset | duration | trial_type | response_time | stim_id |
|-------|----------|------------|---------------|----------|
| 1.23 | 0.65 | start | 1.435 | stim-\<label\> |
| 5.65 | 0.65 | stop | 1.739 | stim-\<label\> |
| 12.1 | 2.35 | n/a | n/a | stim-\<label\> |

In the accompanying JSON sidecar, the `stim_id` column might be described as follows:

```JSON
{
    "stim_id": {
        "LongName": "Stimulus identifier",
        "Description": "Represents a unique identifier for the stimulus presented at the given onset time.",
    }
}
```

## The stimulus file and JSON sidecar

Stimulus files can be of various types including audio, image, video, and combined audiovideo formats. Each stimulus file SHOULD have an accompanying JSON sidecar file containing metadata about the stimulus. The structure of the stimulus file name and the JSON sidecar file name SHOULD follow the BIDS naming conventions as below:

- Stimulus file: `stim-<label>[_part-<label>]_<suffix>.<extension>`
- JSON sidecar file: `stim-<label>[_part-<label>]_<suffix>.json`

Then stimulus file names MUST start with `stim-` followed by a unique label, and an optional part label if the stimulus is divided into parts. `stim-` is the standard entity for the stimulus files, indicating that the files do not belong to a specific subject or participant but rather are likely to be used across subjects throughout the experiment. The suffix SHOULD describe the type of stimulus (e.g., audio, image, video, audiovideo) and the extension MUST indicate the file format. The JSON sidecar file MUST have the same name as the stimulus file but with a `.json` extension. Here are the allowed suffixes and extensions for the stimulus files:

| Modality | Extensions | Description |
|----------|------------|-------------|
| `audio` | .wav, .mp3, .aac, .ogg | Audio-only stimulus files |
| `image` | .jpg, .png, .svg | Static visual stimulus files |
| `video` | .mp4, .avi, .mkv, .webm | Video-only stimulus files |
| `audioVideo` | .mp4, .avi, .mkv, .webm | Combined audio-visual stimulus files |
<!-- | Tactile | .ros | Robot Operating System program files for tactile stimulation | -->

If distribution restrictions prevent including the actual stimulus file, the JSON sidecar SHOULD still be present with appropriate metadata describing the stimulus.
For the stimuli that can be descibed in a table format (such as image datasets), the `stimuli.tsv` and `stimuli.json` files can be used to provide information about the stimuli based on their `stim_id`, and the presence of the stimulus file and JSON sidecar is OPTIONAL.


The following table describes the REQURIED, RECOMMENDED, and OPTIONAL fields for the `stim-<label>.json` file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimulus.Stimulus") }}

## Stimuli.tsv and Stimuli.json

The `stimuli.tsv` and `stimuli.json` files are used to provide information about the stimuli based on their `stim_id`. This file is similar in usage as `participants.tsv`, `scans.tsv` and `sessions.tsv`, which list descriptions about subjects, scans and sessions, respectively. The `stimluli.tsv/json` files should be placed in the `/stimuli` directory.

### Stimuli.tsv

The `stimuli.tsv` file contains information about each stimulus, including stimulus ID, type, URL, and other relevant details. The following table describes the REQUIRED, RECOMMENDED, and OPTIONAL columns for the `stimuli.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Stimuli") }}

This is an example of the `stimuli.tsv` file describing three images from the natural scence dataset (NSD):

| stimulus_id | type | description | HED | NSD_id | COCO_id |
|------------|------|-------------|-----|---------|----------|
| stim-nsd02951 | image | an open market full of people and piles of vegetables | ((Item-count, High), Ingestible-object), (Background-view, ((Human, Body, Agent-trait/Adult), Outdoors, Furnishing, Natural-feature/Sky, Urban, Man-made-object)) | 2951 | 262145 |
| stim-nsd02991 | image | a couple of people are cooking in a room | (Foreground-view, ((Item-count/1, (Human, Body, Agent-trait/Adult)), (Item-count/1, (Human, Body, (Face, Away-from), Male, Agent-trait/Adult)), ((Item-count, High), Furnishing))), (Background-view, (Ingestible-object, Furnishing, Room, Indoors, Man-made-object, Assistive-device)) | 2991 | 262239 |
| stim-nsd03050 | image | a person standing on a surfboard riding a wave | (Foreground-view, ((Item-count/1, ((Human, Human-agent), Body, Male, Agent-trait/Adolescent)), (Play, (Item-count/1, Man-made-object)))), (Background-view, (Outdoors, Natural-feature/Ocean)) | 3050 | 262414 |


### Stimuli.json

The `stimuli.json` file provides detailed descriptions of the columns in the `stimuli.tsv` file. There can be extra entries in the `stimuli.json` in addition to the columns in the `stimuli.tsv` to provide more details about the stimulus.

## Annotations.tsv and Annotations.json

The `annotations.tsv` and `annotations.json` files are used to provide additional information about the annotations associated with the stimuli. These files should be placed in the `/stimuli` directory.

### Annotations.tsv

The `annotations.tsv` file contains information about each annotation, including the annotation ID and description. The following table describes the REQUIRED, RECOMMENDED, and OPTIONAL columns for the `annotations.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("annotations.Annotations") }}

### Annotations.json

The `annotations.json` file provides detailed descriptions of the columns in the `annotations.tsv` file.

There could be only one `annotations.tsv` in the `/stimuli` directory. Alternatively, each stimulus (with a unique stimulus ID) can have a separate `stim-<label>_annotations.tsv` to describe the annotations for a specific stimulus.
