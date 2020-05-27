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
the data type of the input (as expressed by its BIDS `suffix`).
For instance, a change in the number of dimensions is likely to disrupt the propagation
of the input's `suffix` and generally, the outcomes of such transformation
cannot be considered _preprocessed_ or _cleaned data_.
Examples:

 -  Motion-corrected, temporally denoised, and transformed to MNI space BOLD series
 -  Inhomogeneity corrected and skull stripped T1w files
 -  Motion-corrected DWI files
 -  Time-domain filtered EEG data
 -  MaxFilter (for example, SSS) cleaned MEG data

The `space` keyword is recomended to distinguish files with different underlying
coordinate systems or registered to different reference maps.
The `desc` (description) keyword is a general purpose field with freeform values,
which SHOULD be used to distinguish between multiple different versions of
processing for the same input data.

Examples of preprocessed data:

```Text
pipeline1/
    sub-001/
        anat/
            sub-001_space-MNI305_T1w.nii.gz
            sub-001_space-MNI305_T1w.json
        func/
            sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.nii.gz
            sub-001_task-rest_run-1_space-MNI305_desc-preproc_bold.json
```

```Text
pipeline2/
    sub-001/
        eeg/
            sub-001_task-listening_run-1_desc-autoannotation_events.tsv
            sub-001_task-listening_run-1_desc-autoannotation_events.json
            sub-001_task-listening_run-1_desc-filtered_eeg.edf
            sub-001_task-listening_run-1_desc-filtered_eeg.json
```

All REQUIRED metadata fields coming from a derivative file’s source file(s) MUST
be propagated to the JSON description of the derivative unless the processing
makes them invalid (e.g., if a source 4D image is averaged to create a single
static volume, a `RepetitionTime` property would no longer be relevant).
