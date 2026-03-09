# Diffusion derivatives

## Diffusion-based tractography

Tractography based on diffusion-weighted MRI data is stored as streamlines in
the TRX file format:

```Text
<pipeline_name>/
    sub-<label>/
        [ses-<label>/]
            <modality/
                <source-entities>[space-<space>]_[tract-<tract name>]_[track-<tracking method>]_tractogram.trx
                <source-entities>[space-<space>]_[tract-<tract name>]_[track-<tracking method>]_tractogram.json
```

Where "tract” is the anatomical/structural entity that is being imaged, and
“track” uses as its value one of the items in a controlled vocabulary.

For example:

```Text

AFQ/
    sub–01/
        dwi/
            sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.trx
            sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.json
            sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-left_track-eudx_tractogram.trx
            sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-left_track-eudx_tractogram.json
```
