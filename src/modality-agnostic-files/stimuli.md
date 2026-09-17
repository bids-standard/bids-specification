# Stimuli

## Stimulus Files Organization

Stimulus files MUST be stored in the `/stimuli` directory under the root directory of the dataset.
The `/stimuli` directory can contain subdirectories to organize the stimulus files.
Stimulus files MUST follow the BIDS naming conventions and are referenced in the `events.tsv`
file using the `stim_id` column.

The standardization of stimulus files and their annotations within BIDS offers several key benefits:

1.  **Consistency**: Ensures uniform storage and referencing across datasets
1.  **Reusability**: Enables stimulus reuse across studies through standardized structure
1.  **Efficiency**: Minimizes redundancy by centralizing annotations
1.  **Flexibility**: Facilitates dataset reuse with alternative annotations

To preserve backward compatibility with existing datasets (which reference stimulus files directly through the `stim_file` column, as described in [Task events](events.md#stimulus-organization)), the use of these specifications for the `/stimuli` directory and the `stim_id` column in the `events.tsv` files is RECOMMENDED but not required. Researchers are encouraged to follow these guidelines to enhance the interoperability and reproducibility of their studies.

Following these guidelines will help ensure that stimulus files and their annotations are stored and referenced consistently across different datasets, facilitating data sharing, reuse, and reproducibility.

## File Organization

<!--
This block generates a filename templates for root-level directories.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_root_filename_template(
   "raw",
   path="stimuli")
}}

Note: The presence of a `stimuli.tsv` file anywhere under the `/stimuli` directory indicates that the content of the `/stimuli` directory follows this BIDS specification for stimulus organization.

### Directory hierarchy and inheritance

The `/stimuli` directory MAY contain subdirectories to organize stimulus files,
for example by stimulus category, task, or acquisition batch.
Stimulus identifiers MUST remain unique across the entire `/stimuli` hierarchy:
the `stim-<label>` entity identifies a stimulus
regardless of the subdirectory in which its files are stored.

Subdirectories MAY contain their own `stimuli.tsv`, `stimuli.json`,
`annotations.tsv`, and `annotations.json` files
that apply only to the stimuli stored in that subdirectory and below.
This makes a subdirectory fully self-describing,
so a stimulus set (its files, catalog, annotations, and metadata)
can be moved between datasets as a portable unit.
A dataset-wide `stimuli.tsv` (with an accompanying `stimuli.json`)
stored directly in the `/stimuli` directory is RECOMMENDED,
even a sparse one listing only the `stimulus_id` of every stimulus:
it provides a single entry point for tools and readers,
and serves as the place for dataset-wide amendments and overrides.
Because the `stim-<label>` entity, not the directory path,
identifies a stimulus, the same `stimulus_id` MUST NOT be defined
by catalog files in sibling subdirectories:
the Inheritance Principle can only reconcile re-descriptions
along a single ancestor chain.
Following the [Inheritance Principle](../common-principles.md#the-inheritance-principle),
information defined deeper in the hierarchy amends or replaces
information defined closer to the `/stimuli` root:
columns and metadata fields introduced in a subdirectory file
are added to those defined at higher levels,
and entries for the same `stimulus_id` (or `annot_id`)
override the corresponding higher-level entries.

For example:

```Text
stimuli/
    stimuli.tsv
    stimuli.json
    annotations.tsv
    faces/
        stimuli.tsv          # amends/overrides root entries for stimuli in faces/
        stim-face01_image.png
        stim-face02_image.png
    sounds/
        stim-tone01_audio.wav
        stim-tone01_annot-pitch_events.tsv
```

### Stimulus File Formats

The following table lists the supported stimulus file formats and their corresponding suffixes. The suffixes are used to identify the type of stimulus file and are appended to the `stim-<label>` prefix in the file name.

| suffix      | extensions                                       | description                  |
| ----------- | ------------------------------------------------ | ---------------------------- |
| audio       | `.wav`, `.flac`, `.mp3`, `.aac`, `.ogg`          | Audio-only stimulus files    |
| image       | `.jpg`, `.png`, `.svg`, `.webp`, `.tif`, `.tiff` | Static visual stimulus files |
| video       | `.mp4`, `.avi`, `.mkv`, `.webm`                  | Video-only stimulus files    |
| audiovideo  | `.mp4`, `.avi`, `.mkv`, `.webm`                  | Combined audio-visual files  |

See the [Media Files appendix](../appendices/media-files.md) for format details and
the recommended technical metadata for media streams.

## Stimulus description (`stim-<label>_<suffix>.json`)

The `stim-<label>_<suffix>.json` file provides metadata about the _singular_ stimulus file.
The following fields are defined to describe the stimulus file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimuli.Stimuli") }}

In some cases, such as observing the copyright of a stimulus file, the actual stimulus file may not be shared. In such cases, the `stim-<label>_<suffix>.json` file SHOULD be used to provide metadata about the stimulus file, including the license, copyright, URL, and description.

### Example `stim-<label>_<suffix>.json`

```JSON
{
    "License": "CC-BY-4.0",
    "Copyright": "2023 Lab Name lab@university.edu",
    "URL": "https://example.com/stimuli/",
    "Description": "Collection of face images, tones, and movie clips used in the experiment"
}
```

The `License` field SHOULD provide the known identifiers, such as `PDL`, `CC0`, `CC-BY` from the [BIDS Licensees Appendix](https://bids-specification.readthedocs.io/en/stable/appendices/licenses.html), or common license lists such as [SPDX](https://spdx.org/licenses/) or [Creative Commons](https://creativecommons.org/licenses/).
The `Copyright` field SHOULD provide the year, copyright holder's name, and if available, the email address of the copyright holder.
If the stimulus file is not shared, the `URL` field SHOULD provide a link to the stimulus file.

## Stimuli Description (`stimuli.tsv`)

The `stimuli.tsv` files are used to provide information about the stimuli based on their `stim_id`. This file is similar in usage as `participants.tsv`, `scans.tsv` and `sessions.tsv`, which list descriptions about subjects, scans and sessions, respectively. A dataset-wide `stimuli.tsv` file placed directly in the `/stimuli` directory is RECOMMENDED;
scoped `stimuli.tsv` files MAY be placed in subdirectories
(see [Directory hierarchy and inheritance](#directory-hierarchy-and-inheritance)).

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

In cases where the stimulus is not shared, the `stimuli.tsv` file can be used to provide metadata about the stimuli, including the license, copyright, URL, and description. This is similar to the use of `stim-<label>_<suffix>.json` files for individual stimuli files. In the case of conflict between the metadata in the `stimuli.tsv` and `stim-<label>_<suffix>.json` files, the metadata in the `stim-<label>_<suffix>.json` file takes precedence.

## Stimulus Annotations

Annotations of the still images or general description of the stimuli (such as frequency and duration of a beep sound) can be stored in the `stimuli.tsv` as an additional column or `stim-<label>_<suffix>.json` as described above. Here is an example of how annotations can be stored in the `stimuli.tsv` file for an image from the Natural Scene Dataset (NSD):

| stimulus_id   | type  | description                                           | HED                                                                                                                                                               | NSD_id | COCO_id |
| ------------- | ----- | ----------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ | ------- |
| stim-nsd02951 | image | an open market full of people and piles of vegetables | ((Item-count, High), Ingestible-object), (Background-view, ((Human, Body, Agent-trait/Adult), Outdoors, Furnishing, Natural-feature/Sky, Urban, Man-made-object)) | 2951   | 262145  |

However, for time-varying stimuli, such as audio or video, it is RECOMMENDED to use specific annotations files in the form of `stim-<label>_annot-<label>_events.tsv` to store the annotations. These files have the same structure as the `events.tsv` files and are used to store annotations for the stimuli. There can be multiple annotation files for a single stimulus file, each with a unique annotation label. The annotation files MUST be stored under the `/stimuli` hierarchy, and it is RECOMMENDED to store them in the same directory as the stimulus files they annotate.

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

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column. The values in the `stim_id` column should represent unique identifiers for the stimuli. Stimulus ID (`stim_id`) should correspond to the unique identifier of the stimulus file in the /stimuli directory and expand to all files (both stimulus and annotation files) that share the same stimulus ID.

Example `events.tsv` file:

| onset | duration | trial_type | response_time | stim_id        |
| ----- | -------- | ---------- | ------------- | -------------- |
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
