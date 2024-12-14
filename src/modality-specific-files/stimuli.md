# Stimuli

The purpose of this file is to describe the specifications for the stimuli directory within the BIDS specifications.

## Storing Stimulus Files

Stimulus files should be stored in the `/stimuli` directory under the root directory of the dataset. The `/stimuli` directory can contain subdirectories to organize the stimulus files. There are no restrictions on the file formats of the stimulus files.

Example directory structure:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example({
  "stimuli": {
    "images": {
      "cat01.jpg": "",
      "cat02.jpg": "",
    },
    "videos": {
      "movie01.mp4": "",
      "movie02.mp4": "",
    },
  },
}) }}

## Referencing Stimulus Files in `events.tsv`

To reference stimulus files in the `events.tsv` file, use the `stim_file` column. The values in the `stim_file` column should represent the relative path to the stimulus file within the `/stimuli` directory.

Example `events.tsv` file:

```Text
onset	duration	trial_type	response_time	stim_file
1.23	0.65	start	1.435	images/cat01.jpg
5.65	0.65	stop	1.739	images/cat02.jpg
12.1	2.35	n/a	n/a	videos/movie01.mp4
```

In the accompanying JSON sidecar, the `stim_file` column might be described as follows:

```JSON
{
    "stim_file": {
        "LongName": "Stimulus file",
        "Description": "Represents the location of the stimulus file (such as an image, video, or audio file) presented at the given onset time. The values correspond to a path relative to the /stimuli directory."
    }
}
```

## Referencing Stimulus Identifiers in `events.tsv`

To reference stimulus identifiers in the `events.tsv` file, use the `stim_id` column. The values in the `stim_id` column should represent unique identifiers for the stimuli.

Example `events.tsv` file:

```Text
onset	duration	trial_type	response_time	stim_file	stim_id
1.23	0.65	start	1.435	images/cat01.jpg	stim001
5.65	0.65	stop	1.739	images/cat02.jpg	stim002
12.1	2.35	n/a	n/a	videos/movie01.mp4	stim003
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

## Standardization of Stimulus Files and Annotations

To ensure consistency and facilitate reuse, the BIDS specifications provide guidelines for standardizing stimulus files and their annotations. This section outlines the recommended practices for storing and referencing stimulus files within a BIDS dataset.

### Advantages of Standardization

Standardizing stimulus files and their annotations within the BIDS specifications offers several advantages:

1. **Consistency**: Ensures that stimulus files are stored and referenced in a consistent manner across different datasets.
2. **Reusability**: Facilitates the reuse of stimulus files and annotations in other studies by providing a standardized structure.
3. **Efficiency**: Reduces redundancy by avoiding the need to replicate annotations across subjects, modalities, tasks, and runs.
4. **Flexibility**: Allows for easy modification of annotations by updating a single file, enabling the reuse of datasets with alternative annotations.

By following these guidelines, researchers can enhance the interoperability and reproducibility of their studies, making it easier to share and reuse data within the scientific community.

## Stimuli.tsv and Stimuli.json

The `stimuli.tsv` and `stimuli.json` files are used to provide additional information about the stimuli used in the experiment. These files should be placed in the `/stimuli` directory.

### Stimuli.tsv

The `stimuli.tsv` file contains information about each stimulus, including its onset time, duration, and other relevant details. The following table describes the required, recommended, and optional columns for the `stimuli.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("stimuli.Stimuli") }}

### Stimuli.json

The `stimuli.json` file provides detailed descriptions of the columns in the `stimuli.tsv` file. The following table describes the required, recommended, and optional fields for the `stimuli.json` file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimuli.Stimuli") }}

## Annotations.tsv and Annotations.json

The `annotations.tsv` and `annotations.json` files are used to provide additional information about the annotations associated with the stimuli. These files should be placed in the `/stimuli` directory.

### Annotations.tsv

The `annotations.tsv` file contains information about each annotation, including its onset time, duration, and other relevant details. The following table describes the required, recommended, and optional columns for the `annotations.tsv` file:

<!-- This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/*.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("annotations.Annotations") }}

### Annotations.json

The `annotations.json` file provides detailed descriptions of the columns in the `annotations.tsv` file. The following table describes the required, recommended, and optional fields for the `annotations.json` file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("annotations.Annotations") }}

## Stim-<label>.json

The `stim-<label>.json` file provides detailed information about a specific stimulus. This file should be placed in the `/stimuli` directory and named according to the unique identifier of the stimulus.

### Stim-<label>.json

The following table describes the required, recommended, and optional fields for the `stim-<label>.json` file:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("stimulus.Stimulus") }}
