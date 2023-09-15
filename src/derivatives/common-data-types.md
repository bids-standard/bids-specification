# Common data types and metadata

## Common file level metadata fields

Each derivative data file SHOULD be described by a JSON file provided as a sidecar
or higher up in the hierarchy of the derived dataset (according to the
[Inheritance Principle](../common-principles.md#the-inheritance-principle))
unless a particular derivative includes REQUIRED metadata fields, in which case a
JSON file is also REQUIRED.
Each derivative type defines their own set of fields, but all of them
share the following (non-required) ones:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("derivatives.common_derivatives.CommonDerivativeFields") }}

### Examples

Preprocessed `bold` NIfTI file in the original coordinate space of the original run.
The location of the file in the original datasets is encoded in the `Sources` metadata,
and [`_desc-<label>`](../appendices/entities.md#desc)
is used to prevent clashing with the original filename.

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
        "sub-01_task-rest_desc-preproc_bold.nii.gz": "",
        "sub-01_task-rest_desc-preproc_bold.json": "",
         },
      },
   }
) }}

```JSON
{
    "Sources": ["bids:raw:sub-01/func/sub-01_task-rest_bold.nii.gz"]
}
```

Note that `"raw"` must appear in the `DatasetLinks` metadata in
`dataset_description.json`.
For example, in the case that the given derivatives dataset is nested within the
"derivatives" directory of a raw dataset, the entry in `DatasetLinks` may say:
`"raw": "../.."`.

If this file was generated with prior knowledge from additional sources,
such as the same subject's `T1w`,
then both files MAY be included in `Sources`.

```JSON
{
    "Sources": [
        "bids:raw:sub-01/func/sub-01_task-rest_bold.nii.gz",
        "bids:raw:sub-01/anat/sub-01_T1w.nii.gz"
    ]
}
```

On the other hand, if a preprocessed version of the T1w image was used, and it also
occurs in the derivatives, `Sources` may include both the local, derivative file,
and the raw original file.

```JSON
{
    "Sources": [
        "bids::sub-01/anat/sub-01_desc-preproc_T1w.nii.gz"
        "bids:raw:sub-01/func/sub-01_task-rest_bold.nii.gz"
    ],
}
```

## Spatial references

Derivatives are often aligned to a common spatial reference to allow for the
comparison of acquired data across runs, sessions, subjects or datasets.
A file may indicate the spatial reference to which it has been aligned using the
[`space` entity](../appendices/entities.md#space) and/or the `SpatialReference` metadata.

The [`space` entity](../appendices/entities.md#space) may take any value in
[Image-Based Coordinate Systems][coordsys].

If the [`space` entity](../appendices/entities.md#space) is omitted,
or the space is not in the [Standard template identifiers][templates] table,
then the `SpatialReference` metadata is REQUIRED.

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("derivatives.common_derivatives.SpatialReferenceEntity") }}

### SpatialReference key allowed values

| **Value** | **Description**                                                                                                                                          |
| --------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `"orig"`  | A (potentially unique) per-image space. Useful for describing the source of transforms from an input image to a target space.                            |
| [URI][]   | This can be used to point to a specific file. Paths written relative to the root of the derivative dataset are [DEPRECATED][] in favor of [BIDS URIs][]. |

In the case of images with multiple references, an [object][] must link the relevant structures to reference files.
If a single volumetric reference is used for multiple structures, the `VolumeReference` key MAY be used to reduce duplication.
For CIFTI-2 images, the relevant structures are BrainStructure values defined in the BrainModel elements found in the CIFTI-2 header.

### Examples

Preprocessed `bold` NIfTI file in `individual` coordinate space. Please mind
that in this case `SpatialReference` key is REQUIRED.

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
        "sub-01_task-rest_space-individual_bold.nii.gz": "",
        "sub-01_task-rest_space-individual_bold.json": "",
         },
      },
   }
) }}

```JSON
{
    "SpatialReference": "bids::sub-01/anat/sub-01_desc-combined_T1w.nii.gz"
}
```

Preprocessed `bold` CIFTI-2 files that have been sampled to the fsLR surface
meshes defined in the Conte69 atlas along with the MNI152NLin6Asym template.
In this example, because all volumetric structures are sampled to the same
reference, the `VolumeReference` key is used as a default, and only the
surface references need to be specified by BrainStructure names.
Here referred to via "https" [URIs][].

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
   "sub-01": {
      "func": {
        "sub-01_task-rest_space-fsLR_den-91k_bold.dtseries.nii": "",
        "sub-01_task-rest_space-fsLR_den-91k_bold.json": "",
         },
      },
   }
) }}

```JSON
{
    "SpatialReference": {
        "VolumeReference": "https://templateflow.s3.amazonaws.com/tpl-MNI152NLin6Asym_res-02_T1w.nii.gz",
        "CIFTI_STRUCTURE_CORTEX_LEFT": "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/Conte69.L.midthickness.32k_fs_LR.surf.gii",
        "CIFTI_STRUCTURE_CORTEX_RIGHT": "https://github.com/mgxd/brainplot/raw/master/brainplot/Conte69_Atlas/Conte69.R.midthickness.32k_fs_LR.surf.gii"
    }
}
```

## Preprocessed or cleaned data

Template:

```Text
<pipeline_name>/
    sub-<label>/
        <datatype>/
            <source_entities>[_space-<space>][_desc-<label>]_<suffix>.<extension>
```

Data is considered to be *preprocessed* or *cleaned* if the data type of the input,
as expressed by the BIDS `suffix`, is unchanged.
By contrast, processing steps that change the number of dimensions are likely to disrupt
the propagation of the input's `suffix` and generally, the outcomes of such transformation
cannot be considered preprocessed or cleaned data.

Examples of preprocessing:

-   Motion-corrected, temporally denoised, and transformed to MNI space BOLD series
-   Inhomogeneity corrected and skull stripped T1w files
-   Motion-corrected DWI files
-   Time-domain filtered EEG data
-   MaxFilter (for example, SSS) cleaned MEG data

The [`space` entity](../appendices/entities.md#space)
is recommended to distinguish files with different underlying
coordinate systems or registered to different reference maps.
See [Spatial references](#spatial-references) for details.
The [`desc` entity](../appendices/entities.md#desc) ("description")
is a general purpose field with freeform values,
which SHOULD be used to distinguish between multiple different versions of
processing for the same input data.

Examples of preprocessed data:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline1": {
        "sub-001": {
            "anat": {
                "sub-001_space-MNI305_T1w.nii.gz": "",
                "sub-001_space-MNI305_T1w.json": "",
                },
            "func": {
                "sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.nii.gz": "",
                "sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.json": "",
                },
            },
        }
   }
) }}

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "pipeline2": {
        "sub-001": {
            "eeg": {
                "sub-001_task-listening_run-1_desc-autoannotation_events.tsv": "",
                "sub-001_task-listening_run-1_desc-autoannotation_events.json": "",
                "sub-001_task-listening_run-1_desc-filtered_eeg.edf": "",
                "sub-001_task-listening_run-1_desc-filtered_eeg.json": "",
                },
            },
        }
   }
) }}

All REQUIRED metadata fields coming from a derivative file’s source file(s) MUST
be propagated to the JSON description of the derivative unless the processing
makes them invalid (for example, if a source 4D image is averaged to create a single
static volume, a `RepetitionTime` property would no longer be relevant). As each file
includes what was computed by increment, a trail of the computational steps performed
is created. Because many steps can occur until the fully clean data are obtained and
because it is NOT mandatory to save every file or step, the simpler `desc-preproc`
and `desc-proc` are available. It becomes however important to document what such
pre-processing or processing are, and record the order of computational steps. This
can be in the json file or alternatively described in a descriptions.tsv file.

## descriptions.tsv

To keep a record of what has been done to the data, a `descriptions.tsv` file can be used, containing at least two columns: `desc_id` and `description`. This file can be located at the root derivatives level or at the subject level (inheritance principle).

`desc_id` contains all labels used in the [`desc entity`](https://bids-specification.readthedocs.io/en/stable/appendices/entities.html#desc), while `description` is a human-readable description of what was computed. Note that while it is helpful to document how files are generated, we see this as 'light provenance', i.e. it is not aimed at providing full computational reproducibility.

{{ MACROS___make_filetree_example(
   {
    "raw/": {
         CHANGES
         README
         channels.tsv
         dataset_description.tsv
         participants.tsv
          "sub-001": {
            "eeg": {
                "sub-001_task-listening_events.tsv": "",
                "sub-001_task-listening_events.json": "",
                "sub-001_task-listening_eeg.edf": "",
                "sub-001_task-listening_eeg.json": "",
                },
            },
          },
  "derivatives/": {
         descriptions.tsv
        "sub-001": {
            "eeg": {
                "sub-001_task-listening_desc-Filt_eeg.edf": "",
                "sub-001_task-listening_desc-Filt_eeg.json": "",
                "sub-001_task-listening_desc-FiltDs_eeg.edf": "",
                "sub-001_task-listening_desc-FiltDs_eeg.json": "",
                "sub-001_task-listening_desc-preproc_eeg.edf": "",
                "sub-001_task-listening_desc-preproc_eeg.json": "",                },
            },
        }
   }
) }}

`descriptions.tsv`

| desc_id          | description                                                                                    |
|------------------|------------------------------------------------------------------------------------------------|
| Filt             | low-pass filtered at 30Hz                                                                      |
| FiltDs           | low-pass filtered at 30Hz,downsampled to 250Hz                                                 |
| preproc          | low-pass filtered at 30Hz, downsampled to 250Hz and rereferenced to a common average reference |

<!-- Link Definitions -->

[coordsys]: ../appendices/coordinate-systems.md#image-based-coordinate-systems

[templates]: ../appendices/coordinate-systems.md#standard-template-identifiers

[object]: https://www.json.org/json-en.html

[bids uris]: ../common-principles.md#bids-uri

[deprecated]: ../common-principles.md#definitions

[uris]: ../common-principles.md#uniform-resource-indicator

[uri]: ../common-principles.md#uniform-resource-indicator
