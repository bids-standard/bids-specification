# Stimuli

## Stimulus Files Organization

Stimulus files MAY be stored in the `/stimuli` directory under the root directory of the dataset.
A `/stimuli` directory that contains a `stimuli.tsv` file follows this specification:
its files MUST be stored directly in `/stimuli`
and MUST follow the naming conventions and formats described below,
and `events.tsv` files SHOULD reference the stimuli through the `stim_id` column.
A `/stimuli` directory without a `stimuli.tsv` file is not restricted by this specification,
so that existing datasets remain valid.

The standardization of stimulus files and their annotations within BIDS offers several key benefits:

1.  **Consistency**: Ensures uniform storage and referencing across datasets
1.  **Reusability**: Enables stimulus reuse across studies through standardized structure
1.  **Efficiency**: Minimizes redundancy by centralizing annotations
1.  **Flexibility**: Facilitates dataset reuse with alternative annotations

Existing datasets reference stimulus files directly through the `stim_file` column,
as described in [Task events](events.md#stimulus-organization).
Following this specification for the `/stimuli` directory
and using the `stim_id` column in `events.tsv` files is RECOMMENDED.

## File Organization

Stimulus files, their metadata, and their annotations are stored directly in the `/stimuli` directory:

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "raw",
   datatypes=["stimuli"],
   n_dupes_to_combine=3)
}}

The `stim-<label>` entity identifies a stimulus:
all files that share the same `stim-<label>`
(the stimulus files, their JSON metadata, and their annotation files)
describe the same stimulus.
A stimulus MAY be stored in several files with different suffixes or extensions,
for example the separate audio and video tracks of a movie.
The `part-<label>` entity MAY be used to split a single stimulus into parts,
such as the chapters of an audiobook or the segments of a long movie.

Stimuli that differ across participants or presentations are stored
in the participant's directories instead
(see [Subject-specific stimulus files](#subject-specific-stimulus-files)).

### Stimulus File Formats

The following table lists the supported stimulus file formats and their corresponding suffixes.
The suffix identifies the type of stimulus file and follows the entities in the file name.

| suffix      | extensions                                                | description                  |
| ----------- | --------------------------------------------------------- | ---------------------------- |
| audio       | `.wav`, `.flac`, `.mp3`, `.aac`, `.ogg`                   | Audio-only stimulus files    |
| image       | `.jpg`, `.jpeg`, `.png`, `.svg`, `.webp`, `.tif`, `.tiff` | Static visual stimulus files |
| video       | `.mp4`, `.avi`, `.mkv`, `.webm`                           | Video-only stimulus files    |
| audiovideo  | `.mp4`, `.avi`, `.mkv`, `.webm`                           | Combined audio-visual files  |

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

In addition to the fields above,
the media stream fields of the [Media Files appendix](../appendices/media-files.md)
apply to the sidecar according to the suffix of the stimulus file,
for example `ImageWidth` and `ImageHeight` for an `image` file.
These fields are not columns of `stimuli.tsv`.

A `stim-<label>_<suffix>.json` file accompanies a shared stimulus file.
A stimulus file that cannot be shared, for example because of copyright,
is described by its row in `stimuli.tsv` instead
(see [Stimuli Description](#stimuli-description-stimulitsv)).
See [Stimulus-level and file-level metadata](#stimulus-level-and-file-level-metadata-stimulitsv-vs-stim-label_suffixjson) for when to use each file.

### Example `stim-<label>_<suffix>.json`

```JSON
{
    "License": "CC-BY-4.0",
    "Copyright": "2023 Lab Name lab@university.edu",
    "URL": "https://example.com/stimuli/face01.png",
    "Description": "A female face with a neutral expression",
    "ImageWidth": 640,
    "ImageHeight": 480
}
```

The `License` field SHOULD provide a known identifier,
such as `PDL`, `CC0`, or `CC-BY-4.0` from the [Licenses appendix](../appendices/licenses.md),
or from common license lists such as [SPDX](https://spdx.org/licenses/)
or [Creative Commons](https://creativecommons.org/licenses/).
The `Copyright` field SHOULD provide the year, copyright holder's name,
and if available, the email address of the copyright holder.
The `URL` field links to the stimulus file itself,
not to a directory or collection of files.

## Stimuli Description (`stimuli.tsv`)

The `stimuli.tsv` file is used to provide information about the stimuli based on their `stimulus_id`.
This file is similar in usage to `participants.tsv`, `scans.tsv`, and `sessions.tsv`,
which list descriptions about subjects, scans, and sessions, respectively.
A `stimuli.tsv` file in the `/stimuli` directory is RECOMMENDED;
its presence marks the directory as following this specification.

The `stimuli.tsv` file contains information about each stimulus,
including its identifier, type, license, whether its file is present, and other relevant details.
The following table describes the REQUIRED, RECOMMENDED, and OPTIONAL columns for the `stimuli.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Stimuli") }}

The `type`, `license`, and `present` columns are REQUIRED:
a stimulus that is not shared has no file from which its type could be inferred,
the license of each stimulus is stated in `stimuli.tsv`
so that tools can read it without opening every sidecar,
and `present` tells readers and validators whether to expect the stimulus file in `/stimuli`.
The value `n/a` MAY be used for `license`
when the license is unknown or the stimulus is not licensed for sharing.

### Example `stimuli.tsv`

```tsv
stimulus_id	type	license	present	copyright	description	URL
stim-face01	image	CC-BY-4.0	true	Lab 2023	A female face with neutral expression	https://example.com/faces/face01.jpg
stim-tone01	audio	CC-BY-4.0	true	Lab 2023	A 440Hz pure tone	https://example.com/tones/tone01.wav
stim-movie01	video	n/a	false	Studio XYZ	A clip from a copyrighted movie	https://example.com/movies/movie01.mp4
```

The `stimuli.json` file provides detailed descriptions of the columns in the `stimuli.tsv` file. There MAY be extra entries in the `stimuli.json` in addition to the columns in the `stimuli.tsv` to provide more details about the stimulus.

A stimulus that is not shared SHOULD be listed in `stimuli.tsv`
with the `present` column set to `false`
and its license (or `n/a`), copyright, URL, and description filled in,
as for `stim-movie01` in the example above.

### Stimulus-level and file-level metadata (`stimuli.tsv` vs. `stim-<label>_<suffix>.json`)

The `stimuli.tsv` file and the `stim-<label>_<suffix>.json` sidecars describe stimuli at two levels.

The `stimuli.tsv` file describes each _stimulus_, with one row per `stimulus_id`,
even when the stimulus is stored in several files or parts.
It lists all stimuli in a single file,
so that tools and readers can load it without opening every sidecar,
and it is the only place to describe a stimulus that is not shared.

A `stim-<label>[_part-<label>]_<suffix>.json` sidecar describes the stimulus files that match its name,
following the [Inheritance Principle](../common-principles.md#the-inheritance-principle):
a sidecar without `part-<label>` applies to all parts of the stimulus,
and a sidecar with `part-<label>` applies to that part only.
Sidecars carry the metadata that a single `stimuli.tsv` row cannot express:

1.  Technical metadata of the media streams,
    such as the codec, frame rate, sampling rate, or image size
    (see the [Media Files appendix](../appendices/media-files.md)).
    These fields depend on the suffix of the file,
    so as `stimuli.tsv` columns they would be `n/a` for most rows,
    and their values can differ between the parts of one stimulus,
    for example parts of a long movie encoded at different frame rates or resolutions.

1.  Descriptive metadata that differs between the parts of one stimulus,
    for example parts that come from different sources, with different URLs or licenses.

A sidecar can also keep the license and provenance next to its file
when the file is copied to another dataset.

The `license`, `copyright`, `URL`, and `description` columns of `stimuli.tsv`
correspond to the `License`, `Copyright`, `URL`, and `Description` fields of the sidecar.
Metadata that applies to the whole stimulus belongs in `stimuli.tsv`.
A sidecar SHOULD contain the media stream metadata of its files,
and MAY repeat the `License` and `Copyright` fields.
Values given in both files SHOULD agree;
when they differ, the value in the sidecar applies to the files that the sidecar describes.

## Stimulus Annotations

Annotations of the still images or general description of the stimuli (such as frequency and duration of a beep sound) can be stored in the `stimuli.tsv` as an additional column, or, for annotations specific to a stimulus file, in its `stim-<label>_<suffix>.json` sidecar. Here is an example of how annotations can be stored in the `stimuli.tsv` file for an image from the Natural Scenes Dataset (NSD):

```tsv
stimulus_id	type	license	present	description	HED	NSD_id	COCO_id
stim-nsd02951	image	n/a	true	an open market full of people and piles of vegetables	((Item-count, High), Ingestible-object), (Background-view, ((Human, Body, Agent-trait/Adult), Outdoors, Furnishing, Natural-feature/Sky, Urban, Man-made-object))	2951	262145
```

For time-varying stimuli, such as audio or video,
it is RECOMMENDED to store annotations in `stim-<label>_annot-<label>_events.tsv` files.
These files follow the format of `events.tsv` files,
including the REQUIRED `onset` and `duration` columns,
with onsets expressed relative to the start of the stimulus.
There can be multiple annotation files for a single stimulus,
each with a unique `annot-<label>`.
Annotation files MUST be stored in the `/stimuli` directory.
When more than one stimulus file shares the same `stim-<label>`,
the `Sources` field of the annotation file's JSON sidecar
SHOULD list the stimulus files that the annotations describe,
using [BIDS URIs](../common-principles.md#bids-uri):

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimuli.AnnotationSources") }}

### Example `stim-<label>_annot-<label>_events.tsv`

The file `stim-thepresent_annot-action_events.tsv` annotates the visible actions in an animated short film,
`stim-thepresent_audiovideo.mp4`,
with onsets in seconds from the start of the film:

```tsv
onset	duration	boy_action	dog_action	environment_action
0.01	2.531	n/a	n/a	black screen
2.55	1	n/a	n/a	credits appear on the screen
7.25	0.105	eyes and mouth of the boy wide open	n/a	n/a
```

A second file, `stim-thepresent_annot-auditory_events.tsv`,
can annotate the speech and sounds of the same film,
so that each annotation set can be added, replaced, or reused independently.

## Annotation Description (`annotations.tsv`)

The `annotations.tsv` file lists the annotation sets available for the stimuli,
one row per `annot-<label>`,
so that tools and readers can discover which annotations exist
and what each describes without opening every annotation file.
There MAY be a single `annotations.tsv` file for all the stimuli
or separate `stim-<label>_annotations.tsv` files for each stimulus.
The values of the `annot_id` column are the labels of the `annot-<label>` entity.
The following columns are defined for the `annotations.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Annotations") }}

### Example `*_annotations.tsv`

```tsv
annot_id	description
action	Actions of the characters and changes in the environment, one row per visible action
auditory	Speech, animal sounds, and foley sounds, one row per sound
```

## Subject-specific stimulus files

Some stimuli differ across participants or presentations, for example:

1.  A recording of the stimulus as it was presented to a participant,
    such as a screen or audio capture made during the session,
    kept to document the exact timing and appearance of the presentation.

1.  Cooperative or dyadic experiments,
    where one participant's behavior is another participant's stimulus.

1.  Stimuli generated or personalized for a single participant.

Such files MAY be stored in the participant's data directories,
next to the recordings they align with,
using the `stim-<label>` entity:

```Text
sub-<label>/
    [ses-<label>/]
        <datatype>/
            sub-<label>[_ses-<label>]_task-<label>_stim-<label>[_acq-<label>][_run-<index>][_part-<label>]_<suffix>.<extension>
            sub-<label>[_ses-<label>]_task-<label>_stim-<label>[_acq-<label>][_run-<index>][_part-<label>]_<suffix>.json
```

where `<datatype>` is one of `beh`, `eeg`, `emg`, `func`, `ieeg`, `meg`, `motion`, or `nirs`,
and `<suffix>` and `<extension>` follow the [Stimulus File Formats](#stimulus-file-formats) table.

The `stim-<label>` entity marks the file as a stimulus presented to the participant,
not as data recorded from them,
and names the stimulus that was presented.
A subject-specific stimulus MAY be stored in several files with different suffixes or extensions.

If files with the same `stim-<label>` are stored in the `/stimuli` directory,
the subject-specific file records the presentation of that stimulus to the participant.
Its content MAY differ from the file in `/stimuli`,
for example in timing, resolution, or display artifacts.
In this case, the `Sources` field of its JSON sidecar SHOULD list the presented files in `/stimuli`,
using [BIDS URIs](../common-principles.md#bids-uri).
If no file in `/stimuli` shares the `stim-<label>`,
the stimulus is specific to the participant.
Listing subject-specific stimuli in `stimuli.tsv` is OPTIONAL,
so that the `/stimuli` directory and its annotations remain self-contained and reusable.

As for stimuli in `/stimuli`,
the `stim_id` column of `events.tsv` files MAY name subject-specific stimuli
to mark when they were presented.

Subject-specific stimulus files are distinct from `*_stim.tsv.gz` files,
which store continuously sampled stimulus signals in tabular form
(see [Physiological recordings](../modality-specific-files/physiological-recordings.md)).

As for other files with a `task` entity, the `TaskName` field is RECOMMENDED.
The JSON sidecar of a subject-specific stimulus file SHOULD describe its media streams
(see the [Media Files appendix](../appendices/media-files.md)).
The following fields are also defined:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimuli.SubjectStimulusSources") }}

### Example: subject-specific stimulus files

```Text
sub-01/
    beh/
        sub-01_task-dyad_events.tsv
        sub-01_task-dyad_stim-partner_audio.wav
        sub-01_task-dyad_stim-partner_audio.json
    func/
        sub-01_task-movie_run-1_bold.nii.gz
        sub-01_task-movie_run-1_events.tsv
        sub-01_task-movie_stim-movie01_run-1_audiovideo.mkv
        sub-01_task-movie_stim-movie01_run-1_audiovideo.json
stimuli/
    stimuli.tsv
    stimuli.json
    stim-movie01_audiovideo.mp4
    stim-movie01_audiovideo.json
```

Here, `sub-01_task-dyad_stim-partner_audio.wav` is the speech of the participant's partner in a dyadic task,
which has no counterpart in `/stimuli`,
and `sub-01_task-movie_stim-movie01_run-1_audiovideo.mkv` is a capture of the movie as it was displayed during the run,
with the following sidecar:

```JSON
{
    "TaskName": "movie",
    "Sources": ["bids::stimuli/stim-movie01_audiovideo.mp4"],
    "VideoCodec": "h264",
    "VideoFrameRate": 60,
    "ImageWidth": 1920,
    "ImageHeight": 1080,
    "AudioCodec": "aac",
    "AudioSampleRate": 48000,
    "AudioChannelCount": 2,
    "RecordingDuration": 600.2
}
```

## Referencing Stimulus Identifiers in `events.tsv`

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column.
Each value of the `stim_id` column MUST take the form `stim-<label>`
and refers to all files (both stimulus and annotation files) that share the same `stim-<label>`.
Each `stim_id` value SHOULD match the `stimulus_id` of an entry in `stimuli.tsv`
or the `stim-<label>` of stimulus files in `/stimuli` or in the participant's directories.
See [Task events](events.md#stimulus-organization) for using `stim_id` together with the `stim_file` column.

Example `events.tsv` file:

```tsv
onset	duration	trial_type	response_time	stim_id
1.23	0.65	face	1.435	stim-face01
5.65	0.65	face	1.739	stim-face02
12.1	2.35	tone	n/a	stim-tone01
```

In the accompanying JSON sidecar, the `stim_id` column might be described as follows:

```JSON
{
    "stim_id": {
        "LongName": "Stimulus identifier",
        "Description": "Represents a unique identifier for the stimulus presented at the given onset time."
    }
}
```
