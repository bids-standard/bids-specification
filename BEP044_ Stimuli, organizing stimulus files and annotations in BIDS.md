**THERE is a PR for this BEP: [BIDS-Spec \#2022](https://github.com/bids-standard/bids-specification/pull/2022). Please do not make changes here.**

**Provide your edits and comments on the PR or directly email the moderators.**

**Main BIDS issue [\#153](https://github.com/bids-standard/bids-specification/issues/153),**

**Example PR [\#433](https://github.com/bids-standard/bids-examples/pull/433)**

with references and insights from issues [\#751](https://github.com/bids-standard/bids-specification/issues/751), [\#750](https://github.com/bids-standard/bids-specification/issues/750),  and [BIDS2-devel/\#54](https://github.com/bids-standard/bids-2-devel/issues/54) (regarding alternative hierarchies). Another related issue is [\#1170](https://github.com/bids-standard/bids-specification/issues/1770) to include media files within the data folders.

# BIDS Extension Proposal 44 (BEP044):

# Stimuli

## version 0.0.1

## Available under the CC-BY 4.0 International license.

Extension moderators/leads: [Seyed Yahya Shirazi](mailto:shirazi@ieee.org)  
Contributors: Dora Hermes, Yaroslav O. Halchenko, Kay Robbins, Scott Makeig, Monique Denissen

| This document contains a draft for BEP0X44. It is a community effort to define standards in data / metadata storage for Stimuli. This is a working document in draft stage and any comments are welcome.  This specification is an extension of BIDS, and general principles are shared. The specification should work for many different settings and facilitate the integration with other imaging methods. To see the original BIDS specification, see [this link](https://bids-specification.readthedocs.io). This document inherits all components of the original specification (e.g. how to store imaging data, events, stimuli and behavioral data), and should be seen as an extension of it, not a replacement. |
| :---- |

**Meta-notes (to be deleted in actual BEPs)**

This template provides a general outline that conforms to the patterns in some previously existing BEPs. However, no BEP fully follows this template, and this should not be interpreted as a list of requirements. Anything that does not apply to your BEP can be freely deleted, and anything else can be freely added. For more inspiration, see the [BEP Lead Guidelines](https://docs.google.com/document/d/1pWmEEY-1-WuwBPNy5tDAxVJYQ9Een4hZJM06tQZg8X4/edit?usp%3Dsharing&sa=D&ust=1537468908724000), and [other BEPs](https://bids.neuroimaging.io/get_involved.html#extending-the-bids-specification).

# **Table of contents**

[**Introduction	2**](#introduction)

[**Terminology	3**](#terminology)

[**Stim-BIDS	3**](#stim-bids)

[**Structure	3**](#3.1.-directory-structure)

[**Entities and suffixes (modalities) introduced for this feature request:	3**](#heading=h.g82534ipxafy)

[**Examples:	4**](#examples:)

[Example 1: Image presentation (still, not time-varying)	4](#example-1:-image-presentation-\(still,-not-time-varying\))

[Example 2: Face presentation (still, not time-varying)	7](#example-2:-face-presentation-\(still,-not-time-varying\))

[Example 3: Movie example (time-varying)	8](#example-3:-movie-example-\(time-varying\))

[Example of a stimulus file with a link to a movie and annotations	9](#example-4:-non-shareable-copyrighted-movie-example-\(time-varying\))

[Other examples…	10](#other-examples-\(what-are-common-use-cases?\)…)

[**Relation to  \`\*\_events.tsv\` and \`\*\_stim.tsv.gz\` files	10**](#relation-to-\`*_events.tsv\`-and-\`*_stim.tsv.gz\`-files)

1. # **Introduction** {#introduction}

Current BIDS specifications provide an option to include stimulus files (e.g., still images, movies, sounds, etc.) in the top \`/stimuli\` directory and to use the \`\*\_events.json\` and \`\*\_events.tsv\` files to define “which stimulus file was used for a given event.” This solution is a convenient method to avoid the need to repeat these stimulus files across subject or session directories, and to point to stimuli from public databases. However, **there is not currently a solution to list these stimuli and to hold the annotations related to the stimulus files.** Providing a structure and metadata for the stimulus files will make the experiments using specific stimuli more Findable, Accessible, Interoperable, and Reusable (FAIR). Also, possible annotations of the stimulus files do not need to be repeated in all `_events.tsv` files across subjects and sessions, and can be included and disseminated once in the `stimuli` directory.

Following the BIDS convention of having a list of entities in the hierarchy (such as participants.tsv, scan.tsv, sessions.tsv, etc.), we propose having a similar `stimuli.tsv` that lists all the stimulus files in the `stimuli/` directory. For the annotation of the stimulus files, a straightforward solution is to include the annotations in the \`/stimuli\` folder with a distinction between annotations for **still (i.e., non-time-varying) stimulus files** (e.g., images, VR physical constructs, etc.) and annotations for **time-varying stimulus files** (i.e., movies, sounds, haptic feedback, etc.). A single-line annotation would be sufficient for the still stimulus files. However, a time-varying stimulus file could need separate annotations for every frame (i.e., the smallest temporal resolution of the stimulus file).

Based on (1) the BIDS Common Principles for file names to “consist of a chain of entity instances and a suffix all separated by underscores,” (2) existing facilities to include Tabular files and Key-Value files with data files, (3) and an existing mechanism for summary tables (such as `participants.tsv` and `scans.tsv`), we propose a structure for the `stimuli/` directory to accommodate (i) stimulus files with multiple parts and tracks, (ii) annotation of both still and time-varying stimuli, and (ii) multiple annotations of the stimulus files. 

2. # **Terminology** {#terminology}

BIDS contains “required”, “recommended” and “optional” fields. These are indicated throughout the document:

* REQUIRED: essential to be BIDS compliant (i.e. MUST as per RFC2199)  
* RECOMMENDED: gives a warning if not present (i.e. SHOULD as per RFC2199)  
* OPTIONAL: no warning if missing (i.e. MAY as per RFC2199)


As in BIDS-Raw, the following apply:

1) All specifications of paths need to use forward slashes.  
2) The inheritance principle applies: any metadata file (.json, .tsv, etc.) may be defined at any directory level. The values from the top level are inherited by all lower levels unless they are overridden by a file at the lower level. For details see BIDS-Raw ([The Inheritance Principle](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#the-inheritance-principle)).

## **2.1 Entites and data types**

We propose the following entities and data types to be added to BIDS to properly annotate the stimulus files.  
**stim- (entity):** The standard entity for the stimulus files, indicating that the files do not belong to a specific subject or participant but rather are likely to be used across subjects throughout the experiment. Subsequently, the `stimuli.tsv/json` (plural of stimulus) and `stimulus_id` will be generated for the stim-xxx stimulus files.

**\_{audio, image, video, audiovideo} (suffix)**: Any data file (medium, plural: media) used as a stimulus. Media files usually have an audio-visual file type (such as png/jpg/mp4/mp3/mkv). The JSON file associated with each media file should contain information such as License (RECOMMENDED), Copyright (RECOMMENDED), URL (OPTIONAL), and Description (OPTIONAL) to describe the origin and the nature of the media. However, **in the case of the imposed distribution restrictions of the stimulus, the media stimulus file may not be present with only JSON sidecar file containing the aforementioned pertinent metadata.**  
Other types of stimuli to consider (10%?):   
\- \_ros(tactile?).ros \- Robot Operating System program file … simulink is another file format for the same.

| modality | extension | extension specification source | license |
| :---- | :---- | :---- | :---- |
| audio | .wav, .mp3, .aac, .ogg |  |  |
| image | .jpg, .png, .svg |  |  |
| video | .mp4, .avi, .mkv, .webm |  |  |
| audiovideo | .mp4, .avi, .mkv, .webm |  |  |

**annot- (entity):** Accommodates multiple annotations for a single (usually, but not necessarily, time-varying) stimulus id. Similar to `stimuli.tsv`, there can be one or multiple `annotations.tsv` files with `annotation_id`, providing a list of the annotations in the directory, or for a specific stimulus respectively (see 3.1).

**part- (entity):** The `_part-` entity could be used to tell apart different, possibly overlapping, parts of a single stimulus, e.g. a long movie (e.g. `_part-1`, `_part-2`) or an audiobook (e.g. `_part-epilog`, `_part-chapter1`, …). Part is currently defined in BIDS specifications as “indicate which component of the complex representation of the MRI signal is represented in voxel data.” The definition should be expanded for all modalities, including stimuli. 

**stim\_file (column in the *events.tsv):*** *Currently, it can only point to a stimulus file or a database.* The column name should be expanded to also  `stim_id`. The definition should be expanded to be either a specific file in the stimuli directory, a database, or a `stimulus_id`. In the latter case, all files sharing the `stimulus_id` will be in scope as well as the entry associated with the `stimulus_id` in `stimuli.tsv`.

3. # **Stim-BIDS** {#stim-bids}

## **3.1. Directory Structure** {#3.1.-directory-structure}

└── stimuli/

├── stimuli.tsv

└── stimuli.json

**Note:** presence of stimuli.tsv file would mandate the bids-validator to validate the content of stimuli/ folder to follow BEP044 specification.  
**Proposal:** make BEP044 layout of stimuli/ to be mandatory for BIDS 2.0 ([bids-2-devel/issues/83](https://github.com/bids-standard/bids-2-devel/issues/83)).

If stimuli.tsv is present the stimulus files in this directory MUST follow this naming structure: *(If non-audio, image, or video files are stored here, what will the extension become?)*

 └── stimuli

├── \[stim-\<label\>\[\_part-\<label\>\]\_\<suffix\>.\<extension\>\]

└── \[stim-\<label\>\[\_part-\<label\>\]\_\<suffix\>.json\]

Currently supported suffixes (see 2.1):

- audio  
- audiovideo  
- image  
- video

If annotations are added:

└── stimuli

├── \[\[stim-\<label\>\_\]annotations.tsv\]

├── \[\[stim-\<label\>\_\]annotations.json\]

├── stim-\<label\>\[\_part-\<label\>\]\_annot-\<label\>\_events.tsv

└── \[stim-\<label\>\[\_part-\<label\>\]\_annot-\<label\>\_events.json\]

with annotations.tsv providing description similarly to [descriptions.tsv](https://bids-specification.readthedocs.io/en/stable/derivatives/common-data-types.html#descriptionstsv) providing descriptions to \_desc- entities with two REQUIRED columns `annotation_id` and `description`, followed by arbitrary number of OPTIONAL columns (e.g., rater\_age, annotation\_modality, etc). annotations.json would provide a description of columns in the annotations.tsv (similarly to `descriptions.json`, `participants.json` etc).

If annotations and their features are generic to all stimuli, a single common `annotations.tsv` file can be used. If annotations are specific for a certain stimulus, the optional `[stim-<label>_]` prefix can be used. (This is analogous to the way in which `sessions.tsv` is used)

For still images or body of words (that are not time-varying), multiple annotations could be included in the `stimuli.tsv/json` in separate columns. NOTE: Image-type stimuli SHOULD NOT use `_annot-events.tsv/json`. Additional annotations can be added to `stimuli.tsv/json` or the `stim-<label>.json` sidecar.

Sidecar metadata and extensions most likely to align with 

- [https://github.com/bids-standard/bids-specification/issues/1771](https://github.com/bids-standard/bids-specification/issues/1771) RFC: BEP for audio/video capture of behaving subjects 

## 

## **3.3. `stimuli.tsv/json`**

The `stimuli.json` file describes the columns of the `stimuli.tsv` file, therefore snake\_case.

If `stimuli.tsv` is present, it is RECOMMENDED that `stimuli.json` is also present.

| Column name | Requirement Level | Data type | Description |
| :---- | :---- | :---- | :---- |
| stimulus\_id | REQUIRED | String | A stimulus ID in the form of stim-\<label\>, Represents a pointer stimulus file (such as an image, video, or audio file). There are no restrictions on the file formats of the stimuli files, but they should be stored in the /stimuli directory (under the root directory of the dataset; with OPTIONAL subdirectories). The values under the stim\_file column correspond to a path relative to /stimuli. For example for  stim-nsd02951\_image.png the stimulus\_id is stim-nsd0251.  This column MUST appear as the first column in the file. Alternative 1: stimulus\_id should be unique and only file of a single type could be associated with stimulus\_id.  In case of different stimulus types for the same stimulus concept, stimulus\_id should reflect composition of stimulus concept and type. |
| type | REQUIRED | String | Freeform or ‘one of’ video, image, audio, audiovideo. If present, this column MUST appear as the second column in the file. Alternative 2: In case of files with different types for the same stimulus\_id, type MUST NOT be used. If it is desired to have per-type row/description \- stimulus\_id should reflect composition of stimulus concept and type. Aleternatively, the type can be sdescribed in the individual stimulus JSON sidecar. |
| URL | OPTIONAL (REQUIRED, if the stimulus file or json is not available) | String | Location (origin) for the stimuli file. |
| license  | RECOMMENDED | String | The license for the stimulus set. The use of license name abbreviations is OPTIONAL for specifying a license (see [Licenses](https://bids-specification.readthedocs.io/en/stable/appendices/licenses.html)). The corresponding full license text MAY be specified in an additional LICENSE file. |
| copyright | OPTIONAL | String | Year(s) and Copyright owner for the particular stimuli media |
| description | OPTIONAL | String | Freeform description of stimuli |
| HED | OPTIONAL | String | Hierarchical Event Descriptor (HED) Tag. See the [HED Appendix](https://bids-specification.readthedocs.io/en/stable/appendices/hed.html) for details. This column may appear anywhere in the file. |
| filename | OPTIONAL | String | For annotations corresponding to a single file (for example, when there is a multi-part stimulus), users may optionally include the filename of the stimulus being annotated.   Tools may then use this name to locate the stimulus file corresponding to this annotation. This column may appear anywhere in the file. |
| present | OPTIONAL | Bool | Bool (true/false), Indicating whether the stimulus file is present in the directory (true). |
| partDescription | OPTIONAL | String | Description of the multiple parts of a stimulus. |
| Additional columns | OPTIONAL | String | Additional columns are allowed. |

# **3.4. `annotations.tsv/json`**

If `annotations.tsv` is present, it is RECOMMENDED that `annotations.json` is also present.

| Column name | Requirement Level | Data type | Description |
| :---- | :---- | :---- | :---- |
| annot\_id | REQUIRED | [string](https://www.w3schools.com/js/js_json_datatypes.asp) | A desc-\<label\> entity present in the derivatives dataset. The desc\_id column contains the labels used with the [desc entity](https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#desc), within the particular nesting that the descriptions.tsv file is placed. For example, if the descriptions.tsv file is placed at the root of the derivative dataset, its desc\_id column SHOULD contain all labels of the desc entity) used across the entire derivative dataset.  Values in desc\_id MUST be unique. This column must appear first in the file. |
| [description](https://bids-specification.readthedocs.io/en/stable/glossary.html#objects.columns.description__entities) | REQUIRED | [string](https://www.w3schools.com/js/js_json_datatypes.asp) | Free-form text description of the entity's label (defined in \<entity\>\_id column). The corresponding label column is desc\_id. This column must appear second in the file. |
| Additional Columns | OPTIONAL | n/a | Additional columns are allowed. |

# **3.5. `stim-<label>.json`**

Key values follow 3.3 stimuli.tsv/json. If a field is present in both `stim-<label>.json` and stimuli.tsv/json, the `stim-<label>.json` SHOULD override.

# **Examples:** {#examples:}

A draft pull request is created on the BIDS Examples to include the examples below in detail.

## **Example 1: Image presentation (still, not time-varying)** {#example-1:-image-presentation-(still,-not-time-varying)}

Below is an example of a \`/stimuli\` directory with three images from the NSD image database, as HED-annotated by Clair Holmes at Mayo Clinic (in the [NSD-HED-label](https://github.com/MultimodalNeuroimagingLab/nsd_hed_labels/blob/main/shared1000_HED.tsv) repository):

The example */stimuli* directory:

└── stimuli

├── stimuli.tsv

├── stimuli.json

├── stim-nsd02951\_image.png

├── \[stim-nsd02951\_image.json\]

├── stim-nsd02991\_image.png

├── \[stim-nsd02991\_image.json\]

├── stim-nsd03050\_image.png

└── \[stim-nsd03050\_image.json\]

When optional columns in stimuli.tsv file are added as in the example below, these must be described in the stimuli.json 

| NSD\_id | OPTIONAL. Image ID in the Natural Scenes Dataset  [https://naturalscenesdataset.org/](https://naturalscenesdataset.org/)  |
| :---- | :---- |
| COCO\_id | OPTIONAL. Image ID in the COCO database  [https://cocodataset.org/](https://cocodataset.org/)  |

The example */stimuli/stimuli.tsv* file:

| stimulus\_id | type | description | HED | NSD\_id | COCO\_id |
| :---- | :---- | :---- | :---- | :---- | :---- |
| stim-nsd02951 | image | an open market full of people and piles of vegetables | ((Item-count, High), Ingestible-object), (Background-view, ((Human, Body, Agent-trait/Adult), Outdoors, Furnishing, Natural-feature/Sky, Urban, Man-made-object)) | 2951 | 262145 |
| stim-nsd02991 | image | a couple of people are cooking in a room | (Foreground-view, ((Item-count/1, (Human, Body, Agent-trait/Adult)), (Item-count/1, (Human, Body, (Face, Away-from), Male, Agent-trait/Adult)), ((Item-count, High), Furnishing))), (Background-view, (Ingestible-object, Furnishing, Room, Indoors, Man-made-object, Assistive-device)) | 2991 | 262239 |
| stim-nsd03050 | image | a person standing on a surfboard riding a wave | (Foreground-view, ((Item-count/1, ((Human, Human-agent), Body, Male, Agent-trait/Adolescent)), (Play, (Item-count/1, Man-made-object)))), (Background-view, (Outdoors, Natural-feature/Ocean)) | 3050 | 262414 |

Exemplary downstream \*\_events.tsv (bids\_dir/sub-\<label\>/sub-\<label\>*task-\<label\>\_*events.tsv)

Imagine that, in a study, the three images listed above are shown to the subject, the following would be one row of the data-level \`\*\_events.tsv\` file:

\[\*\_events.tsv file example, subject file\] (non-expanded version)

| onset | duration | stim\_file |
| :---- | :---- | :---- |
| 25.033 | 1.02 | stim-nsd02951\_image.png |

## **Example 2: Face presentation (still, not time-varying)**  {#example-2:-face-presentation-(still,-not-time-varying)}

\[This is from the Wakeman-Hansen dataset (ds000117, ds003645), currently the most cited electrophysiology dataset on OpenNeuro\]. The example uses direct annotation of the stimulus images by HED in the stimuli.tsv file without the use of a stimuli.json file. 

**Example:** stimuli.tsv using direct HED annotation with no stimuli.json

| stimulus\_id | type | description | HED |
| :---- | :---- | :---- | :---- |
| stim-cross | image | A white fixation cross on a black background in the center of the screen. | (Foreground-view, (White, Cross), (Center-of, Computer-screen)), (Background-view, Black) |
| stim-f001 | image | A female face that should be recognized by the participants. | (Foreground-view, (Image, (Face, Famous, Female), (Center-of, Computer-screen)), (Background-view, Black) |
| stim-s005 | image | A scrambled face image generated by taking face 2D FFT. | (Foreground-view, (Image, (Face, Disordered), (Center-of, Computer-screen)), (Background-view, Black) |
| stim-u112 | image | A male face that should not be recognized by the participants. | (Foreground-view, (Image, (Face, Male, Unfamiliar), (Center-of, Computer-screen)),(Background-view, Black) |

The stimulus files themselves are named stim-cross\_image.bmp, stim-f001\_image.bmp, stim-s005\_image.bmp, and stim-u112\_image.bmp.

An edited version of the main  sub\_002\_task-FacePerception\_run-1\_events.tsv file is:

| onset | duration | event\_type | stim\_file |
| :---- | :---- | :---- | :---- |
| 26.731 | n/a | show\_cross | stim-cross |
| 27.246 | n/a | show\_face | stim-u143 |
| 27.893 | n/a | left\_press | n/a |
| 29.796 | n/a | show\_cross | stim-cross |
| 30.353 | n/a | show\_face | stim-f001 |
| 32.884 | n/a | show\_cross | stim-cross |
| 33.360 | n/a | show\_face | stim-s005 |

| onset | duration | event\_type | stim\_file |
| :---- | :---- | :---- | :---- |
| 26.731 | n/a | show\_cross | cross.bmp |
| 27.246 | n/a | show\_face | u143.bmp |
| 27.893 | n/a | left\_press | n/a |
| 29.796 | n/a | show\_cross | cross.bmp |
| 30.353 | n/a | show\_face | f0001.bmp |
| 32.884 | n/a | show\_cross | cross.bmp |
| 33.360 | n/a | show\_face | s005.bmp |

Since the stim\_file column entries do not have extensions, they are interpreted as stimulus\_id values, and their annotations are looked up using the stimulus\_id column of stimuli.tsv. If the values in the stim\_file column of the main \_events.tsv file have an extension, tools may search for corresponding annotations in the optional filename column of stimuli.tsv.  
The above example annotated each of the images individually, resulting in duplication of annotations.  Users can also use the stimuli.json file and categorical columns with HED to reduce this redundancy. HED support of the stimuli.tsv/stimuli.json will be handled similarly to the annotation of the participants.tsv/participants.json.

## 

## **Example 3: Movie example (time-varying)** {#example-3:-movie-example-(time-varying)}

Below is an example of a `/stimuli` directory with a movie (called [The Present](https://youtu.be/WjqiU5FgsYc)) used for the [Healthy Brain Network’s](https://healthybrainnetwork.org) EEG and fMRI studies:

The example */stimuli* directory:

└── stimuli

├── stimuli.tsv

├── stimuli.json 

├── \[annotations.tsv\]

├── \[annotations.json\]

├── stim-thepresent\_audiovideo.mp4

├── \[stim-thepresent\_audiovideo.json\]

├── stim-thepresent\_annot-LogLumRatio\_events.tsv

└── stim-thepresent\_annot-LogLumRatio\_events.json

The example /stimuli/stimuli.tsv file:

| stimulus\_id | type | HED |
| :---- | :---- | :---- |
| stim-thepresent | audiovideo | Visual-presentation, Movie |

The example /stimuli/stim-thepresent\_annot-LogLumRatio\_events.tsv file:

| onset | duration | shot\_number | LLR |
| :---- | :---- | :---- | :---- |
| 0 | n/a | video\_start | n/a |
| 0 | 7.25 | 1 | n/a |
| 7.25 | 3.542 | 2 | \-1.557820733 |
| 10.792 | 5.208 | 3 | 0.3358234903 |

\[sub-01\_task-thepresent\_events.tsv file example for a specific subject\](non-expanded version)

| onset | duration | value | stim\_file |
| :---- | :---- | :---- | :---- |
| 1.0380 | 1.0 | video\_start | stim-thepresent\_annot-LogLumRatio\_events.tsv |
| 204.10 | 1 | video\_stop | stim-thepresent\_annot-LogLumRatio\_events.tsv |

## **Example 4: Non-shareable copyrighted movie example (time-varying)** {#example-4:-non-shareable-copyrighted-movie-example-(time-varying)}

In some cases it may not be possible to share stimuli or movies shown to participants due to e.g. copyright or confidentiality issues. In this case, a link to a stimulus can be included or annotations for all stimuli can be shared. One such example would look as follows:

Below is an example of a `/stimuli` directory with a movie:

The example `/stimuli` directory:

└── stimuli

├── stimuli.tsv

├── stimuli.json

├── **stim-thepresent\_audiovideo.json**

├── stim-thepresent\_annot-LogLumRatio\_events.tsv

└── stim-thepresent\_annot-LogLumRatio\_events.json

The example /stimuli/stimuli.tsv file:

| stimulus\_id | type | HED |
| :---- | :---- | :---- |
| stim-thepresent | audiovideo | Visual-presentation, Movie |

The example of stim-thepresent\_audiovideo.json would be:

| stimSource | OPTIONAL. A link to the stimulus source file In this example:  [https://youtu.be/3XA0bB79oGc?si=Tnyd-7oFRzd0xCr9](https://youtu.be/3XA0bB79oGc?si=Tnyd-7oFRzd0xCr9)  |
| :---- | :---- |

## **Other examples (what are common use cases?)…** {#other-examples-(what-are-common-use-cases?)…}

- Example 5: (long) Movie or audiobook split into parts.  
  - Counter-example: since \_part in mri means something else, corresponding data file would **not** be 1-to-1 matching via \_task-forrest\_part-... and need to be ad-hoc like \_task-forrest1 or \_task-forrest\_run-1  
  - This may be a good example: [https://github.com/psychoinformatics-de/studyforrest-data-annotations.git](https://github.com/psychoinformatics-de/studyforrest-data-annotations.git)   
- Example 6: Parts of the story randomized for investigation of temporal structuring

# **Relation to  \`\*\_events.tsv\` and \`\*\_stim.tsv.gz\` files** {#relation-to-`*_events.tsv`-and-`*_stim.tsv.gz`-files}

\[*\`\*\_events.tsv\` is defined under [BIDS-specificaitons/modality-specifc files/task events](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/05-task-events.html). \`\*\_stim.tsv.gz\` files is defined in [BIDS-specificaitons/modality-specifc files/Physiological and other continuous recordings](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/06-physiological-and-other-continuous-recordings.html)*.\]

The annotations within the `stimuli.tsv` and `_annot-<label>_events.tsv` files can be expanded in the downstream `*_events.tsv` files when the file name is mentioned in the `stim_file` or `stim_id` column *(The use of `stim_id` is not defined under BIDS events specifications, and should be expanded in the pull request)*.

While the contents of `stimuli.tsv` and `_annot-<label>_events.tsv` can also be included in the individual `*_events.tsv` files, such implementation unnecessarily replicates annotations across subjects, modalities, tasks, and runs. Also, using `stimuli.tsv` and `_annot-<label>_events.tsv` increases the possibility of both (1) reusing the same annotations in other studies and (2) reusing the dataset with alternative annotations – by merely changing one file. Using the current inefficient ‘within-\`\_events.tsv\`’ mechanism hinders reusing the annotations (for example, annotations of complex stimuli or standard stimulus sets) and complicates reusing the datasets using alternate annotations – as in the current specification, these annotations would have to be replaced in every data directory `*_events.tsv` and `*_events.json` file.

Another advantage of top-level `stimuli.tsv` and `_annot-<label>_events.tsv` is avoiding the need to create and edit large `*_events.tsv/json` files for datasets that use complex stimuli, such as movies. By avoiding the need to include annotations in every data folder, the processing toolbox will retrieve these annotations housed in the single top-level `/stimuli` directory during the analysis. This will increase the readability of all the data level  `*_events.tsv` and `*_events.json` files and avoid using fixed, lengthy annotations to annotate every instance of a constant stimulus. For large, standard stimulus sets, such as the [Natural Scene Dataset](https://naturalscenesdataset.org) or the immense [COCO image dataset](https://cocodataset.org/), holding a list of images used across the BIDS dataset in the top-level `/stimuli` directory, with their complete annotations, would give a useful cross-reference for debugging and design of analyses.