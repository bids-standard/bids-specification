# Eye-tracking including gaze position and pupil size

Support for eye-tracking dataset developed as a
[BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids) on how to
appropriately credit this extension when referring to it in the context
of the academic literature.

## Terminology and conventions

Eyetracking-BIDS is fully consistent with the BIDS specification as a whole.
However, BIDS was initially developed in the context of MRI,
so some terminology may be unfamiliar to researchers from other fields.
This section adds clarifications to
[Common Principles - Definitions](../common-principles.md#definitions) for the
eye-tracking context.

-   **Eye-tracker** - refers to the apparatus allowing the records of gaze
    position and/or pupil size.

-   **Screen** - Video display used to present visual stimulation (for example
    projector, monitor, tablet).

## Eye-tracking data

With EyeTracking-BIDS, we wish to promote the adoption of good practices in
the management of scientific data.

### Template

<!--
This block generates a filetree exanple.
A guide for editing it can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md.
-->
{{ MACROS___make_filetree_example(

   {
   "sub-<label>": {
      "<datatype>": {
         "<matches>_eyetrack.json": "",
         "<matches>_eyetrack.tsv.gz": "",
         },
      }
   }

) }}

Eye-tracking data MUST be stored in the main data recording modality or
 `<datatype>` directory (for example `func` when combined with fMRI, or
 `beh` when combined with behavioral measures).

In the template filenames, the `<matches>` part corresponds to task filename
before the suffix. For example, when fMRI is considered the main modality with
files such as `sub-01_ses-1_task-pRF_run-1_bold.nii.gz`, `<matches>` would
then correspond to `sub-01_ses-1_task-pRF_run-1`.

### Tabular file (`*_eyetrack.tsv.gz`)

The eye-tracking data must be saved in `.tsv.gz` format.
The tabular files consist of one row per sample and a set of REQUIRED and
OPTIONAL columns.

<!--
This block generates a columns table.
The definitions of these fields can be found in
  src/schema/rules/tabular_data/eyetrack.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_columns_table("eyetrack.EyeTracking") }}

Throughout BIDS you can indicate missing values with `n/a` (for "not
available").

We encourage users to put the eye-tracking raw data within the
`/sourcedata` directory (for example put eye-tracker proprietary files before
conversion to `tsv.gz` format in the sourcedata directory).

### Sidecar JSON document (`*_eyetrack.json`)

#### Required fields

The following specific eye-tracking fields MUST be present:

<!-- This block generates a metadata table.
These tables are defined in
 src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
 src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("eyetrack.EyeTrackingRequired") }}

Note that `ScreenSize`, `ScreenResolution` and `ScreenDistance` are REQUIRED as
they are considered essential in eye-tracking data analysis.

#### Recommended fields

Although not REQUIRED for the validity of your dataset, the following fields
are important and should be well documented. In particular, we highly
RECOMMEND to carefully document the calibration metadata.

<!-- This block generates a metadata table.
These tables are defined in
 src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
 src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("eyetrack.EyeTrackingRecommended") }}

### Example sidecar JSON document

```JSON
{
"Manufacturer": "SR-Research",
"ManufacturersModelName": "EYELINK II CL v4.56 Aug 18 2010",
"SoftwareVersion": "SREB1.10.1630 WIN32 LID:F2AE011 Mod:2017.04.21 15:19 CEST",
"SamplingFrequency": 1000,
"SampleCoordinateUnits": "pixel",
"SampleCoordinateSystem": "gaze-on-screen",
"EnvironmentCoordinates": "top-left",
"RecordedEye": "Both",
"ScreenSize": [38.6, 29],
"ScreenResolution": [1024, 768],
"ScreenDistance": 60,
"ScreenAOIDefinition": ["square",
                        [100, 150, 300, 350]]
}
```

### Example Datasets
<!--
1. Datasets will be updated later to adapt to the agreed format.
2. We aim at adding a last example converting published dataset from openeuro.
-->

-   Combined behavior and eye-tracking fixation and saccade data,
    measured with an Eyelink (SR Research), from 8 particpants reading 320
    embedded target words and invisible boundary (see
    [Gagl, 2016](https://peerj.com/articles/2467/)).

    [BIDS dataset](https://zenodo.org/record/1228659)

-   Combined behavior and eye-tracking position and pupil data, measured with
    an Eyelink (SR Research), from 26 participants performing a
    binocular rivalry task (see
    [Brascamp et.al, 2021](https://doi.org/10.7554/eLife.66161)).

    [BIDS dataset](https://doi.org/10.5061/dryad.41ns1rncp)

-   Combined resting-state fMRI and eye-tracking data, measured with an Eyelink
    (SR research), from 20 participants keeping their gaze steady at the
    screen center.

    [BIDS dataset](https://openneuro.org/datasets/ds004158/versions/1.0.1)
