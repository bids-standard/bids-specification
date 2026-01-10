# Behavioral recordings

!!! example "Example datasets"

    Datasets containing behavioral data can be found
    in the [BIDS examples repository](https://bids-website.readthedocs.io/en/latest/datasets/examples.html#behavioral)
    and can be used as helpful guidance when curating new datasets.

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["beh"]) }}

The `beh` directory MAY store behavioral recordings such as audio (`_audio.*`), video (`_video.*`), and combined audio-video (`_audiovideo.*`) recordings, physiological (`_physio.*`) recordings, and other continuous recordings (`_stim.tsv.gz`, `_stim.json`).
Audio, video, and audio-video recordings MAY be of subjects performing tasks, resting-state behavior, or recordings of stimuli being presented to the subject.
Audio/video recordings MAY occur simultaneously with other recordings, such as BOLD or EEG.
Relative timing between files may be determined by consulting the `scans.tsv` file.
If no `scans.tsv` file is present, the alignment is undefined.
The `beh` directory MAY also contain event timing files (`_events.tsv`) and their associated metadata (`_events.json`) for behavioral experiments that do not have corresponding neuroimaging or functional data.

Additionally, events files that do not include the mandatory `onset` and `duration` columns MAY be included,
but MUST be labeled `_beh.tsv` rather than `_events.tsv`.

The following OPTIONAL columns are pre-defined for behavioral data files:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("events.Behavioral") }}

## Sidecar JSON (`*_beh.json`)

In addition to the metadata that is either:

-   RECOMMENDED for sidecar JSON files for [tabular data](../common-principles.md#tabular-files), or

-   REQUIRED for some data that can be found in the `beh` directory
    (for example `SamplingFrequency` and `StartTime` for `*_<physio|stim>.tsv.gz` files),

it is RECOMMENDED to add the following metadata to the JSON files of this directory.

### Task information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_sidecar_table("beh.BEHTaskInformation") }}

### Institution information

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("beh.BEHInstitutionInformation") }}

## Audio, video, and audio-video recordings

Audio and video recordings of behaving subjects MAY be stored in the `beh` directory
using the `_audio`, `_video`, and `_audiovideo` suffixes.
The `_audio` suffix is for audio-only recordings, `_video` for video-only recordings,
and `_audiovideo` for recordings that contain both audio and video streams.
These recordings are typically used to capture vocalizations, speech, facial expressions,
body movements, or other behavioral aspects during experimental tasks or rest periods.

!!! warning "Privacy and personally identifiable information"

    Audio and video recordings of human subjects often contain personally identifiable
    information (PII) such as faces, voices, and other identifying features.
    Data curators MUST take special care to ensure compliance with applicable privacy
    regulations (such as HIPAA in the United States, GDPR in the European Union, or other
    local data protection laws) when handling these recordings.

    These recordings are generally more suitable for internal use or for sharing
    non-human subject data, unless appropriate privacy protections are implemented.

### File formats

Audio recordings MUST use one of the following extensions:

-   `.flac` - Free Lossless Audio Codec
-   `.mp3` - MPEG Audio Layer III
-   `.ogg` - Ogg Vorbis
-   `.wav` - Waveform Audio File Format

Video (and audio-video) recordings MUST use one of the following extensions:

-   `.mp4` - MPEG-4 Part 14
-   `.mkv` - Matroska video container
-   `.avi` - Audio Video Interleave

### Entities

Audio and video files MAY use the following entities:

-   `task` - OPTIONAL for audio and video recordings
-   `acq` - OPTIONAL, can distinguish different recording setups
-   `run` - OPTIONAL, for multiple recordings with identical parameters
-   `recording` - OPTIONAL, to differentiate simultaneous recordings from different angles, locations, or devices
-   `split` - OPTIONAL, for continuous recordings split into multiple files

### Examples

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "beh": {
         "sub-01_task-rest_video.mp4": "",
         "sub-01_task-rest_video.json": "",
         "sub-01_task-interview_audiovideo.mp4": "",
         "sub-01_task-interview_audiovideo.json": "",
         "sub-01_task-stroop_recording-face_video.mp4": "",
         "sub-01_task-stroop_recording-face_video.json": "",
         "sub-01_task-stroop_recording-room_video.mp4": "",
         "sub-01_task-stroop_recording-room_video.json": "",
         "sub-01_task-vocalization_audio.wav": "",
         "sub-01_task-vocalization_audio.json": "",
         },
      },
   }
) }}

For continuous recordings split into multiple files:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "ses-01": {
         "beh": {
            "sub-01_ses-01_task-freeplay_run-01_split-001_video.mp4": "",
            "sub-01_ses-01_task-freeplay_run-01_split-002_video.mp4": "",
            "sub-01_ses-01_task-freeplay_run-01_split-003_video.mp4": "",
            "sub-01_ses-01_task-freeplay_run-01_video.json": "",
            },
         },
      },
   }
) }}

### Sidecar JSON for audio, video, and audio-video recordings

The following metadata fields are available for audio, video, and audio-video recordings:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("beh.AudioVideoDevice") }}

The following fields are available for audio recordings (`_audio`) and audio-video recordings (`_audiovideo`):

{{ MACROS___make_sidecar_table("beh.AudioStreams") }}

The following fields are available for video recordings (`_video`) and audio-video recordings (`_audiovideo`):

{{ MACROS___make_sidecar_table("beh.VideoStreams") }}

### Example audio-video sidecar JSON

For an audio-video file containing both video and audio streams:

```JSON
{
  "TaskName": "RestingState",
  "Device": "Sony FDR-AX53",
  "AudioChannelCount": 2,
  "AudioSampleRate": 48000,
  "FrameRate": 30.0,
  "Height": 1080,
  "Width": 1920,
  "Duration": 600.5
}
```

### Example video sidecar JSON

For a video-only recording:

```JSON
{
  "TaskName": "RestingState",
  "Device": "Sony FDR-AX53",
  "FrameRate": 30.0,
  "Height": 1080,
  "Width": 1920,
  "Duration": 600.5
}
```

### Example audio sidecar JSON

For an audio-only recording:

```JSON
{
  "TaskName": "Vocalization",
  "Device": "Zoom H6 Handy Recorder",
  "AudioChannelCount": 2,
  "AudioSampleRate": 44100,
  "Duration": 300.2
}
```

### Annotations and events

Behavioral annotations or event markers for audio and video recordings
SHOULD be stored in accompanying `_events.tsv` files following the standard
[events file format](../modality-agnostic-files/events.md).
These events files use the same filename entities as the audio/video file they describe,
but with the `_events` suffix.

For example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "beh": {
         "sub-01_task-speech_audio.wav": "",
         "sub-01_task-speech_audio.json": "",
         "sub-01_task-speech_events.tsv": "",
         "sub-01_task-speech_events.json": "",
         },
      },
   }
) }}

## Example `_beh.tsv`

```tsv
trial	response	response_time	stim_file
congruent	red	1.435	images/word-red_color-red.jpg
incongruent	red	1.739	images/word-red_color-blue.jpg
```

In the accompanying JSON sidecar, the `trial` column might be documented as follows:

```JSON
{
   "TaskName": "Stroop",
   "trial": {
      "LongName": "Trial name",
      "Description": "Indicator of the type of trial",
      "Levels": {
         "congruent": "Word and font color match.",
         "incongruent": "Word and font color do not match."
      }
   }
}
```
