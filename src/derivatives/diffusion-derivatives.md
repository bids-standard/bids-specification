# Diffusion derivatives

## Diffusion-based tractography

Tractography based on diffusion-weighted MRI data is stored as streamlines in
the [TRX file format](https://tee-ar-ex.github.io):

```Text
<pipeline_name>/
    sub-<label>/
        [ses-<label>/]
            <modality>/
                <source-entities>[space-<space>]_[tract-<tract name>]_[track-<tracking method>]_tractogram.trx
                <source-entities>[space-<space>]_[tract-<tract name>]_[track-<tracking method>]_tractogram.json
```

Where `tract` is the anatomical/structural entity that is being imaged, and
`track` is fully specified in the sidecar as described below.

For the most common case, a tractogram will be generated from some DWI data, so
<modality> will typically be “dwi”. In any case, the <modality> allows to
unequivocally identify the data type from which the tractogram originated.

For example:

    sub–01/
        dwi/
            sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.trx
            sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.json
            sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-L_track-eudx_tractogram.trx
            sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-L_track-eudx_tractogram.json
```

The JSON sidecar accompanying the tractogram can contain the following metadata
fields:

{{ MACROS___make_metadata_table(
    {
        "Name": ("OPTIONAL", "String", "A human-readable name corresponding to the primary tractography algorithm and/or software used to generate the streamlines data."),
        "Description": ("OPTIONAL", "String", "A longer description of the nature of the tractography experiment"),
        "URL": ("OPTIONAL", "String", "A web link to a more exhaustive description of the process by which the tractography data were generated. This could be a reference to a journal article, software, software command, documentation, or pipeline description."),
        "StreamlineSeeding": ("REQUIRED", "Dict", "The contents of this dictionary are described in Table 5a."),
        "StreamlinePropagation": ("REQUIRED", "Dict", "The contents of this dictionary are described in Table 6a."),
        "StreamlineTermination": ("REQUIRED", "Dict", "The contents of this dictionary are described in Table 7a."),
        "StreamlineAcceptanceCriteria": ("REQUIRED", "Dict", "The contents of this dictionary are described in Table 8a."),
        "StreamlineReconstructionDensity": ("REQUIRED", "Dict", "The contents of this dictionary are described in Table 9a."),
    }
) }}

Table 5a (contents of the value for key “StreamlineSeeding”)

{{ MACROS___make_metadata_table(
    {
        "Sources": ("REQUIRED", "List", "A list where each item describes a mechanism by which streamline seed points were derived. The contents of the elements of this list are described in Table 5b"),
        "AcceptanceCriteria": ("OPTIONAL", "List", "he contents of this list are described in Table 5c"),
    }
) }}

Table 5b (contents of elements within list `StreamlineSeeding[“Sources”]`):

{{ MACROS___make_metadata_table(
    {
        "Type": ("REQUIRED", "String", "Selection from the following: ['Random', 'Sphere', 'RandomPerElement', 'GridPerElement', 'CountPerElement', 'RejectionSampling', 'Dynamic']. 'Element' can refer to voxels, fixels, or surface vertex elements based on the filepath referenced by key 'Source'. 'CountPerElement' is interpreted as being, for example, seeding some number of streamlines from precisely the center of each image element, as opposed to other mechanisms that, for each image element, spread the seeds out within the volume ascribed to that image element."),
        "Source": ("REQUIRED unless Type is 'Sphere' in which case MUST NOT be specified.", "String", " Filesystem path or BIDS URI corresponding to the data source used to draw streamline seeds."),
        "SeedsPerElement": ("Either REQUIRED or MUST NOT be specified based on the value of 'Type'", "Int", "For seeding mechanisms that involve a fixed number of streamline seeds for every image element in the seeding source ('RandomPerElement', 'GridPerElement', 'CountPerElement'), this value dictates the number of seeds to be drawn for each such element. For 'GridPerElement', this number must be a perfect cube."),
        "AttemptsPerSeed": ("OPTIONAL", "Int", " If specified, it must be a positive integer. For a stochastic tracking algorithm, this is the number of attempts of initiation that are allowed in each seed."),
        "Unidirectional": ("OPTIONAL", "Binary", "Specifies whether streamline propagation occurred in one direction from the seed point only, or in two antipodally symmetric directions."),
        "InitialDirection": ("OPTIONAL", "Dict", "If absent, assume that the initial streamline tangent from the seed point was determined using the same mechanism as that used for orientation sampling during streamline propagation, but unconstrained by a prior incoming tangent. See Table 5c for possible values."),
    }
) }}

Table 5c (contents of elements of dict `StreamlineSeeding[AcceptanceCriteria]`):

{{ MACROS___make_metadata_table(
    {
        "Metric": ("REQUIRED", "String", "Text description of the anisotropy metric mediating whether a streamline was permitted to propagate from the seed point."),
        "Source": ("REQUIRED", "String", "Filesystem path or BIDS URI of image data from which the corresponding anisotropy metric can be extracted/computed."),
        "Threshold": ("REQUIRED", "Float", "Numerical threshold applied to anisotropy metric."),
    }
) }}


# Tracking methods

{{ MACROS___make_subobject_table("metadata.Track") }}
