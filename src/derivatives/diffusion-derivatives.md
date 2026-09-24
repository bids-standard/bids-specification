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

```Text
    pyAFQ/
        sub–01/
            dwi/
                sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.trx
                sub-01_space-MNI152NLin2009cAsym_tract-wholebrain_track-eudx_tractogram.json
                sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-L_track-eudx_tractogram.trx
                sub-01_space-MNI152NLin2009cAsym_tract-ArcuateFasciculus_hemi-L_track-eudx_tractogram.json
```

The JSON sidecar accompanying the tractogram contains the following metadata
fields:

{{ MACROS___make_metadata_table(
    {
        "Name": ("OPTIONAL", "A human-readable name corresponding to the primary tractography algorithm and/or software used to generate the streamlines data."),
        "Description": ("OPTIONAL", "A longer description of the nature of the tractography experiment"),
        "URL": ("OPTIONAL", "A web link to a more exhaustive description of the process by which the tractography data were generated. This could be a reference to a journal article, software, software command, documentation, or pipeline description."),
        "StreamlineSeeding": ("REQUIRED", "The contents of this dictionary are described in Table 2a."),
        "StreamlinePropagation": ("REQUIRED", "The contents of this dictionary are described in Table 3a."),
        "StreamlineTermination": ("REQUIRED", "The contents of this dictionary are described in Table 4a."),
        "StreamlineAcceptanceCriteria": ("REQUIRED", "The contents of this dictionary are described in Table 5a."),
        "StreamlineReconstructionDensity": ("OPTIONAL", "The contents of this dictionary are described in Table 6a."),
    }
) }}

Table 2a (contents of the value for key `StreamlineSeeding`)

{{ MACROS___make_metadata_table(
    {
        "Sources": ("REQUIRED", "A list where each item describes a mechanism by which streamline seed points were derived. The contents of the elements of this list are described in Table 2b"),
        "AcceptanceCriteria": ("OPTIONAL", "he contents of this list are described in Table 2c"),
    }
) }}

Table 2b (contents of elements within list `StreamlineSeeding["Sources"]`):

{{ MACROS___make_metadata_table(
    {
        "Type": ("REQUIRED", "Selection from the following: ['Random', 'Sphere', 'RandomPerElement', 'GridPerElement', 'CountPerElement', 'RejectionSampling', 'Dynamic']. 'Element' can refer to voxels, fixels, or surface vertex elements based on the filepath referenced by key 'Source'. 'CountPerElement' is interpreted as being, for example, seeding some number of streamlines from precisely the center of each image element, as opposed to other mechanisms that, for each image element, spread the seeds out within the volume ascribed to that image element."),
        "Source": ("REQUIRED unless Type is 'Sphere' in which case MUST NOT be specified.", " Filesystem path or BIDS URI corresponding to the data source used to draw streamline seeds."),
        "SeedsPerElement": ("Either REQUIRED or MUST NOT be specified based on the value of 'Type'", "For seeding mechanisms that involve a fixed number of streamline seeds for every image element in the seeding source ('RandomPerElement', 'GridPerElement', 'CountPerElement'), this value dictates the number of seeds to be drawn for each such element. For 'GridPerElement', this number must be a perfect cube."),
        "AttemptsPerSeed": ("OPTIONAL", " If specified, it must be a positive integer. For a stochastic tracking algorithm, this is the number of attempts of initiation that are allowed in each seed."),
        "Unidirectional": ("OPTIONAL", "Specifies whether streamline propagation occurred in one direction from the seed point only, or in two antipodally symmetric directions."),
        "InitialDirection": ("OPTIONAL", "If absent, assume that the initial streamline tangent from the seed point was determined using the same mechanism as that used for orientation sampling during streamline propagation, but unconstrained by a prior incoming tangent. See Table 2d for possible values."),
    }
) }}

Table 2c (contents of elements of dict `StreamlineSeeding["AcceptanceCriteria"]`):

{{ MACROS___make_metadata_table(
    {
        "Metric": ("REQUIRED", "Text description of the anisotropy metric mediating whether a streamline was permitted to propagate from the seed point."),
        "Source": ("REQUIRED", "Filesystem path or BIDS URI of image data from which the corresponding anisotropy metric can be extracted/computed."),
        "Threshold": ("REQUIRED", "Numerical threshold applied to anisotropy metric."),
    }
) }}

Table 2d (contents of elements of dict `StreamlineSeeding["InitialDirection"]`):

TODO

Table 3a (contents of the value for key `StreamlinePropagation`):

{{ MACROS___make_metadata_table(
    {
        "Algorithm": ("REQUIRED", "The contents of this dictionary are described in Table 3b."),
        "AnglePerStep": ("OPTIONAL", "The maximal change in degrees in the streamline tangent between successive steps. Note that exactly how this parameter is interpreted may depend on the value of IntegrationOrder."),
        "Interpolation": ("REQUIRED", "Selection from the following: ['Nearest', 'Linear', 'Cubic', 'Spline']. The mechanism by which sub-voxel information is drawn from the Source based on the precise streamline location."),
        "InterpolationOrder": ("REQUIRED", "The order of interpolation used (or 0 if linear)"),
        "MinimumRadius": ("OPTIONAL", "The radius in mm of the circle formed by a streamline consistently turning at the maximum curvature angle at each step."),
        "IntegrationOrder": ("OPTIONAL", "Polynomial complexity of numerical integration of fibre orientations over space to form the streamlines."),
        "Source": ("REQUIRED", "Filesystem path or BIDS URI to data used in the determination of streamline tangents during propagation."),
        "StepSize": ("OPTIONAL", "The distance in mm covered by successive steps of the streamline algorithm. Note that this is not necessarily equivalent to the distance in mm between vertices in the tractogram as stored on file."),
        "AttemptsPerVertex": ("OPTIONAL", "The maximal number of probabilistic attempts to make in propagating from a streamline vertex before ceasing propagation."),
    }
) }}

Table 3b (contents of dict `StreamlinePropagation["Algorithm"]`):

{{ MACROS___make_metadata_table(
    {
        "Name": ("REQUIRED", "A human-readable name corresponding to the tractography algorithm used to generate the streamlines."),
        "Description": ("OPTIONAL", "A longer description of the nature of the tractography algorithm."),
        "URL": ("OPTIONAL", "A web link to a more exhaustive description of the algorithm used to generate the tractography data."),
    }
) }}

Table 4a (contents of the value for key `StreamlineTermination`):

{{ MACROS___make_metadata_table(
    {
        "AnatomicalSegmentation": ("OPTIONAL", "Path to data containing anatomical segmentation that was used to constrain streamline termination."),
        "Anisotropy": ("OPTIONAL", "The contents of each element of this list are described in Table 4b."),
        "AnglePerStep": ("OPTIONAL", "If a streamline changes tangent between successive steps of greater than this value in degrees, it is terminated."),
        "MinimumRadius": ("OPTIONAL", "If a streamline changes tangent between successive steps corresponding to a circle of radius smaller than this value in mm, it is terminated."),
        "Masks": ("OPTIONAL", "List of strings corresponding to mask images; a streamline is terminated as soon as it exits the region defined by these masks."),
        "SatisfiedAllAcceptance": ("OPTIONAL", "Set to True if streamlines were immediately terminated at the first vertex upon which that streamline had satisfied all acceptance criteria."),
        "MaximumLength": ("OPTIONAL", "Units of mm. Any streamline exceeding this length was no longer propagated."),
    }
) }}

Table 4b (contents of elements of list `StreamlineTermination["Anisotropy"]`):

{{ MACROS___make_metadata_table(
    {
        "Metric": ("REQUIRED", "Text description of the anisotropy metric mediating whether a streamline was terminated."),
        "Source": ("REQUIRED", "Filesystem path or BIDS URI of image data from which the corresponding anisotropy metric can be extracted."),
        "Threshold": ("REQUIRED", "Numerical threshold applied to anisotropy metric."),
    }
) }}

Table 5a (contents of the value for key `StreamlineAcceptanceCriteria`):

{{ MACROS___make_metadata_table(
    {
        "InclusionRegions": ("OPTIONAL", "List of filesystem paths. A streamline must visit every item in this list at any location along its length in order to be deemed acceptable."),
        "OrderedInclusionRegions": ("OPTIONAL", "List of filesystem paths. A streamline must visit every item in this list in the same sequence as the order in which they appear during streamline propagation."),
        "ExclusionRegions": ("OPTIONAL", "List of filesystem paths. A streamline must not visit any item in this list at any location along its length."),
        "MinimumLength": ("OPTIONAL", "In units of mm. Any streamline shorter than this length was discarded."),
        "MaximumLength": ("OPTIONAL", "In units of mm. Any streamline exceeding this length was discarded."),
        "AnatomicalSegmentation": ("OPTIONAL", "Path to data containing anatomical segmentation that influenced whether streamlines were discarded."),
    }
) }}

Table 6a (contents of the value for key `StreamlineReconstructionDensity`):

{{ MACROS___make_metadata_table(
    {
        "Seeds": ("OPTIONAL", "Tractogram generation was terminated if this number of unique seed vertices was drawn."),
        "GeneratedStreamlines": ("OPTIONAL", "Tractogram generation was terminated if this number of streamlines were generated."),
        "AcceptedStreamlines": ("OPTIONAL", "Tractogram generation was terminated once this number of streamlines was written to the output tractogram."),
    }
) }}

## Tracking methods

The `track` entity uses a controlled vocabulary of tracking method abbreviations,
as defined in the schema `enum` for this entity:

{{ MACROS___make_subobject_table("metadata.Track") }}
