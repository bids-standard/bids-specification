# Common data types

## Preprocessed or cleaned data

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        <datatype>/
            <source_keywords>[_space-<space>][_desc-<label>]_<suffix>.<ext>
```

Preprocessing in this context means transformations of data that do not change
the number of dimensions of the input and are not explicitly covered by other
data types in the specification.
Examples:

 -  Motion-corrected, temporally denoised, and transformed to MNI space BOLD series
 -  Inhomogeneity corrected and skull stripped T1w files
 -  Motion-corrected DWI files
 -  Time-domain filtered EEG data
 -  Spatially filtered EEG data

The `space` keyword is recomended to distinguish files with different underlying
coordinate systems or registered to different reference maps.
The `desc` (description) keyword is a general purpose field with freeform values,
which SHOULD be used to distinguish between multiple different versions of
processing for the same input data.

Note that even though `space` and `desc` are optional at least one of them MUST
be defined to avoid name conflict with the raw file.

Examples:

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_space-MNI305_bold.nii.gz
            sub-001_task-rest_run-1_space-MNI305_bold.json
```

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_desc-MC_bold.nii.gz
            sub-001_task-rest_run-1_desc-MC_bold.json
```

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_desc-fmriprep_bold.nii.gz
            sub-001_task-rest_run-1_desc-fmriprep_bold.json
```

All REQUIRED metadata fields coming from a derivative file’s source file(s) MUST
be propagated to the JSON description of the derivative unless the processing
makes them invalid (e.g., if a source 4D image is averaged to create a single
static volume, a SamplingFrequency property would no longer be relevant).
