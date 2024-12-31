# Stimuli

## Stimulus Files Organization

Stimulus files MUST be stored in the `/stimuli` directory under the root directory of the dataset.
The `/stimuli` directory can contain subdirectories to organize the stimulus files.
Stimulus files MUST follow the BIDS naming conventions and SHOULD be referenced in the `events.tsv`
file using the `stim_id` column.

The standardization of stimulus files and their annotations within BIDS offers several key benefits:

1. **Consistency**: Ensures uniform storage and referencing across datasets
2. **Reusability**: Enables stimulus reuse across studies through standardized structure
3. **Efficiency**: Minimizes redundancy by centralizing annotations
4. **Flexibility**: Facilitates dataset reuse with alternative annotations

To preserve backward compatibility with existing datasets (see the Legacy section below), the use of these specifications for `/stimuli` directory and the `stim_id` column in the `events.tsv` files is RECOMMENDED but not required. Researchers are encouraged to follow these guidelines to enhance the interoperability and reproducibility of their studies.

Following these guidelines will help ensure that stimulus files and their annotations are stored and referenced consistently across different datasets, facilitating data sharing, reuse, and reproducibility.

## File Organization

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
   "stimuli": {
    "stimuli.tsv": "",
    "stimuli.json": "",
    "[stim-<label>[_part-<label>]<suffix>.<extension>]": "",
    "[stim-<label>[_part-<label>]<suffix>.json]": "",
    "[[stim-<label>_]annotations.tsv]": "",
    "[[stim-<label>_]annotations.json]": "",
    "[stim-<label>[_part-<label>]_annot-<label>_events.tsv]": "",
    "[stim-<label>[_part-<label>]_annot-<label>_events.json]": ""
    }
  }) }}

Note: The presence of `stimuli.tsv` file indicates that the content of the `/stimuli` folder follows this BIDS specification for stimulus organization. This structure is planned to become mandatory in BIDS 2.0.

### Stimulus File Formats

The following table lists the supported stimulus file formats and their corresponding suffixes. The suffixes are used to identify the type of stimulus file and are appended to the `stim-<label>` prefix in the file name.

| **suffix**  | **extensions**          | **description**                   |
|-------------|-------------------------|-----------------------------------|
| audio       | `.wav`, `.mp3`, `.aac`, `.ogg` | Audio-only stimulus files        |
| image       | `.jpg`, `.png`, `.svg`  | Static visual stimulus files      |
| video       | `.mp4`, `.avi`, `.mkv`, `.webm` | Video-only stimulus files        |
| audiovideo  | `.mp4`, `.avi`, `.mkv`, `.webm` | Combined audio-visual files      |

## Stimulus description (`stim-<label>_<suffix>.json`)
The `stim-<label>_<suffix>.json` file provides metadata about the *singular* stimulus file.
The following fields are defined to describe the stimulus file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimulus.Stimulus") }}

In some cases, such as observing the copyright of a stimulus file, the actual stimulus file may not be shared. In such cases, the `stim-<label>_<suffix>.json` file SHOULD be used to provide metadata about the stimulus file, including the license, copyright, URL, and description.

### Example `stim-<label>_<suffix>.json`

```JSON
{
    "License": "CC-BY-4.0",
    "Copyright": "Lab 2023",
    "URL": "https://example.com/stimuli/",
    "Description": "Collection of face images, tones, and movie clips used in the experiment"
}
```

## Stimuli Description (`stimuli.tsv`)

The `stimuli.tsv/json` files are used to provide information about the stimuli based on their `stim_id`. This file is similar in usage as `participants.tsv`, `scans.tsv` and `sessions.tsv`, which list descriptions about subjects, scans and sessions, respectively. The `stimluli.tsv/json` files MUST be placed in the `/stimuli` directory.

The `stimuli.tsv` file contains information about each stimulus, including stimulus ID, type, URL, and other relevant details. The following table describes the REQUIRED, RECOMMENDED, and OPTIONAL columns for the `stimuli.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Stimuli") }}

### Example `stimuli.tsv`

```Text
stimulus_id    type     URL                                     license      copyright    description                                  present
stim-face01   image    https://example.com/faces/face01.jpg    CC-BY-4.0   Lab 2023    A female face with neutral expression       true
stim-tone01   audio    https://example.com/tones/tone01.wav    CC-BY-4.0   Lab 2023    A 440Hz pure tone                          true
stim-movie01  video    https://example.com/movies/movie01.mp4  n/a         Studio XYZ  A clip from copyrighted movie              false
```

The `stimuli.json` file provides detailed descriptions of the columns in the `stimuli.tsv` file. There MAY be extra entries in the `stimuli.json` in addition to the columns in the `stimuli.tsv` to provide more details about the stimulus.

In cases where the stimulus is not shared, the `stimuli.tsv` file can be used to provide metadata about the stimuli, including the license, copyright, URL, and description. This is simialr to the use of `stim-<label>_<suffix>.json` files for individual stimuli files. In the case of conflict between the metadata in the `stimuli.tsv` and `stim-<label>_<suffix>.json` files, the metadata in the `stim-<label>_<suffix>.json` file takes precedence.

## Stimulus Annotations
Annotations of the still images or general description of the stimuli (such as frequency and duration of a beep sound) can be stored in the `stimuli.tsv` as an additional column or `stim-<label>_<suffix>.json` as described above. Here is an example of how annotations can be stored in the `stimuli.tsv` file for an image from the Natural Scene Dataset (NSD):

| stimulus_id  | type  | description | HED | NSD_id | COCO_id |
|--------------|-------|-------------|-----|--------|---------|
| stim-nsd02951 | image | an open market full of people and piles of vegetables | ((Item-count, High), Ingestible-object), (Background-view, ((Human, Body, Agent-trait/Adult), Outdoors, Furnishing, Natural-feature/Sky, Urban, Man-made-object)) | 2951 | 262145 |

However, for time-varying stimuli, such as audio or video, it is RECOMMENDED to use specific annotations files in the form of `stim-<label>_annot-<label>_events.tsv/json` to store the annotations. These files have the same structure as the `events.tsv/json` files and are used to store annotations for the stimuli. There can be multiple annotation files for a single stimulus file, each with a unique annotation label. The annotation files MUST be stored in the `/stimuli` directory.

## Annotation Description (`annotations.tsv`)

The `annotations.tsv` file contains additional metadata about stimulus annotations. There MAY be a single `annotations.tsv` file for all the stimuli or separate `stim-<label>_annotations.tsv` files for each stimulus.
The following columns are defined for the `annotations.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Annotations") }}

### Example `*_annotations.tsv`

```Text
annot_id     description
face01_emo   Emotion annotation for face01 stimulus
face01_gen   Gender annotation for face01 stimulus
face01_age   Age group annotation for face01 stimulus
```

## Referencing Stimulus Identifiers in `events.tsv`

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column. The values in the `stim_id` column should represent unique identifiers for the stimuli. Stimulus ID (`stim_id`) should correspond to the unique identifier of the stimulus file in the /stimuli directory and expands to all files (both stimulus and annotation files) that share the same stimulus ID.

Example `events.tsv` file:

| onset | duration | trial_type | response_time | stim_id |
|-------|----------|------------|---------------|---------|
| 1.23  | 0.65     | start      | 1.435         | `stim-<label>` |
| 5.65  | 0.65     | stop       | 1.739         | `stim-<label>` |
| 12.1  | 2.35     | n/a        | n/a           | `stim-<label>` |

In the accompanying JSON sidecar, the `stim_id` column might be described as follows:

```JSON
{
    "stim_id": {
        "LongName": "Stimulus identifier",
        "Description": "Represents a unique identifier for the stimulus presented at the given onset time."
    }
}
```
