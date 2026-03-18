# Media Files

## Introduction

Several BIDS datatypes make use of media files — audio recordings, video recordings,
combined audio-video recordings, and still images.
This appendix defines the common file formats, metadata conventions,
and codec identification schemes shared across all datatypes that use media files.

Datatypes that incorporate media files (for example, behavioral recordings or stimuli)
define their own file-naming rules, directory placement, and datatype-specific metadata.
The conventions described here apply uniformly to all such datatypes.

## Supported Formats

### Audio formats

| Format                 | Extension | Description                                   |
|------------------------|-----------|-----------------------------------------------|
| Waveform Audio (WAV)   | `.wav`    | Uncompressed PCM audio; lossless, large files |
| MP3                    | `.mp3`    | Lossy compressed audio; widely supported      |
| Advanced Audio Coding  | `.aac`    | Lossy compressed audio; successor to MP3      |
| Ogg Vorbis             | `.ogg`    | Open lossy compressed audio format            |

### Video container formats

| Format                 | Extension | Description                              |
|------------------------|-----------|------------------------------------------|
| MPEG-4 Part 14         | `.mp4`    | Widely supported multimedia container    |
| Audio Video Interleave | `.avi`    | Legacy multimedia container              |
| Matroska               | `.mkv`    | Open, flexible multimedia container      |
| WebM                   | `.webm`   | Open format optimized for web delivery   |

### Image formats

| Format                    | Extension | Description                                  |
|---------------------------|-----------|----------------------------------------------|
| JPEG                      | `.jpg`    | Lossy compressed photographic images         |
| Portable Network Graphics | `.png`    | Lossless compressed images with transparency |
| Scalable Vector Graphics  | `.svg`    | XML-based vector image format                |
| WebP                      | `.webp`   | Modern format supporting lossy and lossless  |
| Tag Image File Format     | `.tiff`   | Lossless format common in scientific imaging |

When choosing a format, consider the trade-off between file size and data fidelity.
Uncompressed or lossless formats (WAV, PNG, TIFF) preserve full quality
but produce larger files.
Lossy formats (MP3, AAC, JPEG) significantly reduce file size
at the cost of some data loss.

## Media Stream Metadata

Media files SHOULD be accompanied by a JSON sidecar file
containing technical metadata about the media streams.
The following metadata fields are defined for media files:

### Duration

| Field      | Suffix                          | Requirement Level |
|------------|---------------------------------|-------------------|
| `Duration` | `audio`, `video`, `audiovideo`  | RECOMMENDED       |

`Duration` is the total duration of the media file in seconds.
For audio-video files, this is the duration of the longest stream.

### Audio stream properties

| Field               | Suffix                | Requirement Level |
|---------------------|-----------------------|-------------------|
| `AudioCodec`        | `audio`, `audiovideo` | RECOMMENDED       |
| `AudioSampleRate`   | `audio`, `audiovideo` | RECOMMENDED       |
| `AudioChannelCount` | `audio`, `audiovideo` | RECOMMENDED       |
| `AudioCodecRFC6381` | `audio`, `audiovideo` | OPTIONAL          |

### Visual properties

| Field    | Suffix                              | Requirement Level |
|----------|-------------------------------------|-------------------|
| `Width`  | `video`, `audiovideo`, `image`      | RECOMMENDED       |
| `Height` | `video`, `audiovideo`, `image`      | RECOMMENDED       |

### Video stream properties

| Field               | Suffix                | Requirement Level |
|---------------------|-----------------------|-------------------|
| `VideoCodec`        | `video`, `audiovideo` | RECOMMENDED       |
| `FrameRate`         | `video`, `audiovideo` | RECOMMENDED       |
| `VideoCodecRFC6381` | `video`, `audiovideo` | OPTIONAL          |

## Codec Identification

Codec identification uses two complementary naming systems:

### FFmpeg codec names (RECOMMENDED)

The `AudioCodec` and `VideoCodec` fields use
[FFmpeg codec names](https://www.ffmpeg.org/ffmpeg-codecs.html) as the RECOMMENDED
convention. These names are the de facto standard in scientific computing and can be
auto-extracted from media files using:

```bash
ffprobe -v quiet -print_format json -show_streams <file>
```

### RFC 6381 codec strings (OPTIONAL)

The `AudioCodecRFC6381` and `VideoCodecRFC6381` fields use
[RFC 6381](https://datatracker.ietf.org/doc/html/rfc6381) codec strings.
These provide precise codec profile and level information useful for
web and broadcast interoperability.

### Common codec reference

| Codec          | FFmpeg Name | RFC 6381 String    | Notes                   |
|----------------|-------------|--------------------|-------------------------|
| H.264 / AVC    | `h264`      | `avc1.640028`      | Most widely supported   |
| H.265 / HEVC   | `hevc`      | `hev1.1.6.L93.B0`  | High efficiency         |
| VP9            | `vp9`       | `vp09.00.10.08`    | Open, royalty-free      |
| AV1            | `av1`       | `av01.0.01M.08`    | Next-gen open codec     |
| AAC-LC         | `aac`       | `mp4a.40.2`        | Default audio for MP4   |
| MP3            | `mp3`       | `mp4a.6B`          | Legacy lossy audio      |
| Opus           | `opus`      | `Opus`             | Open, low-latency audio |
| FLAC           | `flac`      | `fLaC`             | Open lossless audio     |
| PCM 16-bit LE  | `pcm_s16le` | —                  | Uncompressed (WAV)      |

The FFmpeg name column shows the value to use for `VideoCodec` or `AudioCodec`.
The RFC 6381 column shows the value for `VideoCodecRFC6381` or `AudioCodecRFC6381`.
RFC 6381 strings vary by profile and level;
the values shown are representative examples.

## Privacy Considerations

Media files — particularly audio and video recordings — may contain
personally identifiable information (PII), including but not limited to:

-   Voices and speech content
-   Facial features and other physical characteristics
-   Background environments that could identify locations
-   Metadata embedded in file headers (for example, GPS coordinates, device identifiers)

Researchers MUST ensure that sharing of media files complies with the
informed consent obtained from participants and with applicable privacy regulations.
De-identification techniques (for example, voice distortion, face blurring,
metadata stripping) SHOULD be applied where appropriate before data sharing.

## Example

A complete sidecar JSON file for an audio-video recording:

```json
{
    "Duration": 312.5,
    "VideoCodec": "h264",
    "VideoCodecRFC6381": "avc1.640028",
    "FrameRate": 30,
    "Width": 1920,
    "Height": 1080,
    "AudioCodec": "aac",
    "AudioCodecRFC6381": "mp4a.40.2",
    "AudioSampleRate": 48000,
    "AudioChannelCount": 2
}
```
