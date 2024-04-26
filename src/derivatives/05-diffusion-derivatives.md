# Diffusion derivatives

## Preprocessed diffusion-weighted images

-   As with [raw diffusion imaging data](../04-modality-specific-files/01-magnetic-resonance-imaging-data.md#required-gradient-orientation-information),
    inclusion of gradient orientation information is REQUIRED. While
    [the inheritance principle](../02-common-principles.md#the-inheritance-principle)
    applies, it is common for DWI preprocessing to include rotation of
    gradient orientations according to subject motion, so series-specific
    gradient information is typically expected.

-   As per [file naming conventions for BIDS Derivatives](01-introduction.md#file-naming-conventions),
    preprocessed DWI data must not possess the same name as that of the raw
    DWI data. It is RECOMMENDED to disambiguate through use of the key-value
    "`_desc-preproc`".

-   As per [common data types](02-common-data-types.md) for derivative data, a
    JSON sidecar file is REQUIRED due to the REQUIRED `SkullStripped` field.

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>]_desc-preproc_dwi.nii[.gz]
            <source_keywords>[_space-<space>]_desc-preproc_dwi.bvals
            <source_keywords>[_space-<space>]_desc-preproc_dwi.bvecs
            <source_keywords>[_space-<space>]_desc-preproc_dwi.json
```

## Diffusion models

Diffusion MRI can be modeled using various paradigms
to extract more informative representations of the diffusion process
and the underlying biological structure.
There are two key attributes of diffusion models
that warrant explicit mention due to their consequence in how they are represented:

-   The encoding of *anisotropic* information;
    that is, quantities for which the value depends on the orientation in which it is sampled.
    Much of the detail in diffusion derivatives is therefore dedicated
    to the definition of how such data are serialised into corresponding NIfTI images,
    and how corresponding metadata is used to facilitate correct interpretation of those data.

-   A diffusion model may represent the contents of each image voxel as the sum of *multiple compartments*;
    further, each of these different compartments may have different intrinsic properties,
    such as units or anisotropy (as above).
    An individual model fit may therefore yield data for its different parameters
    distributed across multiple NIfTI images,
    and each image may require unique metadata fields to facilitate interpretation.

### Basic filesystem structure

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label1>_dwimap.nii[.gz]
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label1>_dwimap.json
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label2>_dwimap.nii[.gz]
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label2>_dwimap.json
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label3>_dwimap.nii[.gz]
            <source_keywords>[_space-<space>]_model-<label>[_desc-<desc>]_param-<label3>_dwimap.json
```

-   Files "`<source_keywords>_model-<label>_param-<label*>_dwimap.nii[.gz]`"
    provide image data encoding the different parameters that may be estimated by the model.
    If the image is a three-dimensional volume,
    then in the absence of any metadata indicating to the contrary,
    the image should be interpreted as yielding a single scalar parameter per voxel.
    If the image is of a higher dimensionality,
    then relevant metadata fields MUST be specified in the corresponding sidecar JSON file
    indicating how data across dimensions beyond the three spatial dimensions
    should be interpreted.

-   Files "`<source_keywords>_model-<label>_param-<label*>_dwimap.json`"
    MUST provide information about the model,
    and SHOULD provide information about how it was fit to the empirical image data.
    In circumstances where the dimensionality of the corresponding NIfTI image is greater than three,
    they MUST also specify requisite metadata fields regarding
    how data across dimensions beyond the three spatial dimensions are to be interpreted.

In cases where a pipeline yields only a single parameter from a model,
entity "`_param-<label>`" MUST NOT be included; e.g.:
```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>]_model-<label>_dwimap.nii[.gz]
            <source_keywords>[_space-<space>]_model-<label>_dwimap.json
```

### Orientation encoding types

There are many mathematical bases that may be used
in the encoding of parameters that vary as a function of orientation.
A list of such functions supported by the specification is enuerated below,
accompanied by requisite information specific to each representation.

For image data that encode orientation information,
there are fields that MUST be specified in the sidecar JSON file
in order to ensure appropriate interpretation of that information;
see [parameter metadata](#parameter-metadata).

1.  <a name="encoding-scalar">*Scalar image*</a>:

    Image data that do not encode orientation information
    are referred to henceforth here as "scalar" parameters.

1.  <a name="encoding-dec">*Directionally-Encoded Colors (DEC)*</a>:

    An image with three volumes,
    intended to be interpreted as red, green and blue color intensities for visualization.
    Image data MUST NOT contain negative values.

1.  <a name="encoding-spherical">*Spherical coordinates*</a>:

    An image where data across volumes within each voxel encode
    one or more discrete orientations using angles on the 2-sphere,
    optionally encoding some parameter as the distance from origin.

    This may take one of two forms:

    1.  Value per direction

        Each consecutive triplet of image volumes encodes a 3-tuple spherical coordinate,
        using ISO convention for both the order of parameters
        and reference frame for angles:

        1.  Distance from origin,
            encoding some non-negative parameter of interest.

        1.  Inclination / polar angle in radians,
            relative to the zenith direction being the positive direction of the *third* reference axis
            (see [parameter metadata](#parameter-metadata));

        1.  Azimuth angle, in radians,
            orthogonal to the zenith direction,
            with value of 0.0 corresponding to the *first* reference axis
            (see [parameter metadata](#parameter-metadata)),
            increasing according to the right-hand rule about the zenith direction.

        Number of image volumes is equal to (3x*N*),
        where *N* is the maximum number of discrete orientations in any voxel in the image.

    1.  Orientations only

        Each consecutive pair of image volumes encodes an inclination / azimuth pair,
        with order & convention identical to that above
        (equivalent to spherical coordinate with assumed unity distance from origin).

        Number of image volumes is equal to (2x*N*), where *N* is the maximum
        number of discrete orientations in any voxel in the image.

1.  <a name="encoding-3vector">*3-Vectors*</a>:

    An image where data across volumes within each voxel encode
    one or more discrete orientations
    using triplets of axis dot products.

    This may take one of two forms:

    1.  Value per orientation

        The *norm* of the 3-vector encodes some non-negative parameter of interest,
        while its normalized form encodes an orientation on the unit sphere.

    1.  Orientations only

        Each triplet of values encodes an orientation on the unit sphere
        (i.e. the vector norm MUST be 1.0);
        no quantitative value is associated with each orientation.

    Number of image volumes is equal to (3x*N*),
    where *N* is the maximum number of discrete orientations in any voxel in the image.

1.  <a name="encoding-tensor">*Tensor*</a>:

    An image where volumes encode coefficients of a tensor.

    -   For *Rank 2* tensors:

        If antipodal symmetry is set (or implicitly assumed),
        then the image MUST contain six volumes, in the order:
        *D<sub>11</sub>*, *D<sub>12</sub>*, *D<sub>13</sub>*, *D<sub>22</sub>*, *D<sub>23</sub>*, *D<sub>33</sub>,
        where *1*, *2* and *3* index the three spatial dimensions according to their reference
        (see field `"OrientationEncoding"["Reference"]` in [parameter metadata](#parameter-metadata)).
        If the data are not antipodally symmetric,
        then the image MUST contain nine volumes, in the order:
        *D<sub>11</sub>*, *D<sub>12</sub>*, *D<sub>13</sub>*, *D<sub>21</sub>*, *D<sub>22</sub>*, *D<sub>23</sub>, *D<sub>31</sub>*, *D<sub>32</sub>*, *D<sub>33</sub>,
        with subscripts indexing row then column.

1.  <a name="encoding-sh">*Spherical Harmonics (SH)*</a>:

    Image where data across volumes within each voxel encode
    a continuous function spanning the 2-sphere
    using coefficients within a spherical harmonics basis.

    Number of image volumes depends on the spherical harmonic basis employed,
    and the maximal spherical harmonic degree *l<sub>max</sub>*
    (see [spherical harmonics bases](#spherical-harmonics-bases)).

1.  <a name="encoding-amp">*Amplitudes*</a>:

    Image where data across volumes within each voxel encode
    amplitudes of a discrete function spanning the 2-sphere.

    Number of image volumes corresponds to the number of discrete orientations
    on the unit sphere along which samples for the spherical function in
    each voxel are provided;
    these orientations MUST themselves be provided in the associated sidecar JSON file
    (see [parameter metadata](#parameter-metadata)).

### Bootstrap encoding

For some models,
it is common to export not only the best fit of the model to the empirical data,
but multiple reaslisations of that fit taking into account image noise,
typically through some form of bootstrapping procedure.
Where this occurs,
the image data for each parameter possess an additional dimension,
along which those multiple realisations are stored.

For some models,
it is common to explicitly store *both* the multiple realisations of the model
*and* either the parameters corresponding to the maximum *a posteriori* fit
or the mean of each parameter computed across those realisations.
In these circumstances,
it is RECOMMENDED to use the same label for the "`_model-`" entity,
and use the "`_desc-`" entity to disambiguate between these two versions
at the filesystem level.

### Metadata fields

#### Model vs. parameter metadata

For a NIfTI image that encodes some parameter of some model,
there are are range of metadata fields that may be relevant.
These can be broadly separated into two categories:

1.  Metadata that apply to *the model as a whole*
    are not specific to any individual parameter estimated by that model.
    It is therefore RECOMMENDED that any such metadata
    be *equivalent* across all sidecar JSON files for all parameters of that model.

1.  Metadata that apply *only to that specific parameter*
    may include attributes such as units and orientation encoding
    essential for correct interpretation of that parameter image *only*.
    it is therefore possible that these metadata fields may *differ*
    across the multiple parameters estimated by that model.

#### Model metadata

At the root of the metadata dictionary,
REQUIRED field `"Model"` defines a dictionary that contains relevant information
about what the model is and how it was fit to empirical image data.
The following table defines reserved fields within the `"Model"` sub-dictionary.

| **Key name**        | **Description**                                                                                                                 |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| BootstrapParameters | OPTIONAL. Dictionary. Parameters relating to the generation of multiple realisations of the model fit using bootstrapping.      |
| Description         | OPTIONAL. String. Extended text-based information to describe the model.                                                        |
| Parameters          | OPTIONAL. Dictionary. Parameters that influenced the process of fitting the model to empirical image data (see examples below). |
| URL                 | OPTIONAL. String. URL to the specific implementation of the model utilized.                                                     |

Dictionary `"Model["Parameters"]"` has the following reserved keywords that may be applicable to a broad range of models:

| **Key name**           | **Description**                                                                                                                                                                                                                                                                                               |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| FitMethod              | OPTIONAL. String. The optimization procedure used to fit the intrinsic model parameters to the empirical diffusion-weighted signal. Resrved values are: "`ols`" (Ordinary Least Squares); "`wls`" (Weighted Least Squares); "`iwls`" (Iterative Weighted Least Squares); "`nlls`" (Non-Linear Least Squares). |
| Iterations             | OPTIONAL. Integer. The number of iterations used for any form of model fitting procedure where the number of iterations is a fixed input parameter.                                                                                                                                                           |
| OutlierRejectionMethod | OPTIONAL. String. Text describing any form of rejection of outlier values that was performed during fitting of the model.                                                                                                                                                                                     |
| Samples                | OPTIONAL. Integer. The number of realisations of a diffusion model from which statistical summaries (e.g. mean, standard deviation) of those parameters were computed.                                                                                                                                        |

#### Parameter metadata

The following table defines reserved fields relevant to individual model parameters.
Some fields are applicable only to specific [orientation encoding types](#orientation-encoding-types).

| **Key name**        | Relevant [orientation encoding types](#orientation-encoding-types)                         | **Description**                                                                                                                                                                                                                       |
| ------------------- | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| BootstrapAxis       | Any                                                                                        | OPTIONAL. Integer. If multiple realisations of a given parameter are stored in a NIfTI image, this field nominates the image axis (indexed from zero) along which those multiple realisations are stored.                             |
| Description         | Any                                                                                        | OPTIONAL. String. Text description of what model parameter is encoded in the corresponding data file.                                                                                                                                 |
| NonNegativity       | All except [spherical coordinates](#encoding-spherical) and [3-vectors](#encoding-3vector) | OPTIONAL. String. Options are: { `regularized`, `constrained` }. Specifies whether, during model fitting, the parameter was regularised to not take extreme negative values, or was explicitly forbidden from taking negative values. |
| OrientationEncoding | Any                                                                                        | REQUIRED if dimensionality of NIfTI image is greater than three. Dictionary. Provides information requisite to the interpretation of orientation information encoded in each voxel; more details below.                               |
| ResponseFunction    | [Spherical harmonics](#encoding-sh)                                                        | OPTIONAL. Dictionary. Specifies a response function that was utilised by a deconvolution algorithm; more details below.                                                                                                               |

Dictionary `"OrientationEncoding"` has the following reserved keywords:

| **Key name**            | Relevant [orientation encoding types](#orientation-encoding-types)                                                                                                         | **Description**                                                                                                                                                                                                                                                                                                                                                                                                              |
| ----------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| AmplitudesDirections    | [Amplitudes](#encoding-amp)                                                                                                                                                | REQUIRED for `"Type": "amplitudes"`; MUST NOT be specified otherwise. List of lists of floats. Data are either [spherical coordinates (directions only)](#encoding-spherical) or [3-vectors](#encoding-3vector) with unit norm. Defines the dense directional basis set on which samples of a spherical function within each voxel are provided. The length of the list must be equal to the number of volumes in the image. |
| AntipodalSymmetry       | [spherical coordinates](#encoding-spherical), [3-vectors](#encoding-3vector), [tensor](#encoding-tensor), [amplitudes](#encoding-amp), [spherical harmonics](#encoding-sh) | OPTIONAL. Boolean. Indicates whether orientation information should be interpreted as being antipodally symmetric. Assumed to be True if omitted.                                                                                                                                                                                                                                                                            |
| EncodingAxis            | All except [scalar](#encoding-scalar)                                                                                                                                      | REQUIRED. Integer. Indicates the image axis (indexed from zero) along which image intensities should be interpreted as corresponding to orientation encoding.                                                                                                                                                                                                                                                                |
| FillValue               | [Scalar](#encoding-scalar), [spherical coordinates](#encoding-spherical), [3-vectors](#encoding-3vector)                                                                   | OPTIONAL. Float; allowed values: { 0.0, NaN }. Value stored in image when the number of discrete orientations in a given voxel is fewer than the maximal number for that image.                                                                                                                                                                                                                                              |
| Reference               | All except [scalar](#encoding-scalar)                                                                                                                                      | REQUIRED. String; allowed values: { `ijk`, `xyz` }. Indicates whether the NIfTI image axes, or scanner-space axes, are used as reference axes for orientation information.                                                                                                                                                                                                                                                   |
| SphericalHarmonicBasis  | [Spherical harmonics](#encoding-sh)                                                                                                                                        | REQUIRED for `"Type": "sh"`; MUST NOT be specified otherwise. String. Options are: { `mrtrix3`, `descoteaux` }. Details are provided in the [spherical harmonics bases](#spherical-harmonics-bases) section.                                                                                                                                                                                                                 |
| SphericalHarmonicDegree | [Spherical harmonics](#encoding-sh)                                                                                                                                        | OPTIONAL for `"Type": "sh"`; MUST NOT be specified otherwise. Integer. The maximal spherical harmonic order *l<sub>max</sub>*; the number of volumes in the associated NIfTI image must correspond to this value as per the relationship described in [spherical harmonics bases](#spherical-harmonics-bases) section.                                                                                                       |
| TensorRank              | [Tensor](#encoding-tensor)                                                                                                                                                 | REQUIRED for `"Type": "tensor"; MUST NOT be specified otherwise. Integer. Rank of tensor reporesentation. Specification currently only supports a value of 2.                                                                                                                                                                                                                                                                |
| Type                    | Any                                                                                                                                                                        | REQUIRED. String. Specifies the type of orientation information (if any) encoded in the NIfTI image. Permitted values: { `scalar`, `dec`, `unitspherical`, `spherical`, `unit3vector`, `3vector`, `tensor`, `sh`, `amplitudes` }.                                                                                                                                                                                            |

Dictionary `"ResponseFunction"` has the following reserved keywords:

| **Key name** | **Description**                                                                                                                                                                            |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Coefficients | REQUIRED. Either a list of floats, or a list of lists of floats, depending on the mathematical form of the response function and possibly the data to which it applies; see further below. |
| Type         | REQUIRED. String. Options are: { `eigen`, `zsh` }. The mathematical form in which the response function coefficients are provided; see further below.                                      |

-   If `"ResponseFunction"["Type"]: "eigen"`,
    then a list of 4 floating-point values must be specified;
    these are interpreted as three ordered eigenvalues of a rank 2 tensor,
    followed by a reference *b*=0 intensity.

-   If `"ResponseFunction"["Type"]": "zsh`",
    then the values provided can be one of the following:

    -   List of floating-point values.
        Values correspond to the response function coefficient for each consecutive even zonal spherical harmonic degree starting from zero.

    -   List of lists of floating-point values.
        One list per unique *b*-value.
        Each individual list contains a coefficient per even zonal spherical harmonic degree starting from zero.
        If the response function utilised has a different number of non-zero zonal spherical harmonic coefficients for different *b*-values,
        these must be padded with zeroes such that all lists contain the same number of floating-point values.

### Demonstrative examples

-   A basic Diffusion Tensor fit:

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_model-tensor_param-diffusivity_dwimap.nii.gz
                sub-01_model-tensor_param-diffusivity_dwimap.json
                sub-01_model-tensor_param-s0_dwimap.nii.gz
                sub-01_model-tensor_param-s0_dwimap.json
                sub-01_model-tensor_param-fa_dwimap.nii.gz
                sub-01_model-tensor_param-fa_dwimap.json
    ```

    Dimensions of NIfTI image "`sub-01_model-tensor_param-diffusivity_dwimap.nii.gz`": *I*x*J*x*K*x6 ([symmetric rank 2 tensor image](#encoding-tensor))
    Dimensions of NIfTI image "`sub-01_model-tensor_param-s0_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))
    Dimensions of NIfTI image "`sub-01_model-tensor_param-fa_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))

    Contents of file `sub-01_model-tensor_param-diffusivity_dwimap.json`:

    ```JSON
    {
        "Description": "Diffusion Coefficient, encoded as a tensor representation",
        "Model": {
            "Description": "Diffusion Tensor",
            "Parameters": {
                "FitMethod": "ols",
                "OutlierRejectionMethod": "None"
            }
        },
        "OrientationEncoding": {
            "AntipodalSymmetry": true,
            "EncodingAxis": 3,
            "Reference": "xyz",
            "TensorRank": 2,
            "Type": "tensor"
        },
        "Units": "mm^2/s"
    }
    ```

    Contents of file `sub-01_model-tensor_param-s0_dwimap.json`:

    ```JSON
    {
        "Description": "Estimated signal intensity with no diffusion weighting, ie. S0",
        "Model": {
            "Description": "Diffusion Tensor",
            "Parameters": {
                "FitMethod": "ols",
                "OutlierRejectionmethod": "None"
            }
        }
    }
    ```

    Contents of file `sub-01_model-tensor_param-fa_dwimap.json`:

    ```JSON
    {
        "Description": "Fractional Anisotropy",
        "Model": {
            "Description": "Diffusion Tensor",
            "Parameters": {
                "FitMethod": "ols",
                "OutlierRejectionmethod": "None"
            }
        }
    }
    ```

    Notes:

    -   "The diffusion tensor" intrinsically is a mathematical model of how
        the diffusivity is estimated to vary as a function of orientation.
        As such, within this model,
        it is not the *parameter* that is a tensor;
        rather, it is the *diffusivity* that is the estimated parameter,
        and the *way in which the anisotropy of that parameter is encoded* is a tensor.

    -   Metadata fields relevant to the interpretation of the anisotropy of the tensor
        are *not relevant* to the scalar measures
        "`s0`" (estimated signal intensity with no diffusion weighting)
        or "`fa`" (Fractional Anisotropy).
        Those fields therefore MUST be omitted from the corresponding sidecar JSONs.

-   A multi-shell, multi-tissue Constrained Spherical Deconvolution fit:

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_model-csd_param-wm_dwimap.nii.gz
                sub-01_model-csd_param-wm_dwimap.json
                sub-01_model-csd_param-gm_dwimap.nii.gz
                sub-01_model-csd_param-gm_dwimap.json
                sub-01_model-csd_param-csf_dwimap.nii.gz
                sub-01_model-csd_param-csf_dwimap.json
    ```

    Dimensions of NIfTI image "`sub-01_model-csd_param-wm_model.nii.gz`": *I*x*J*x*K*x45 ([spherical harmonics](#encoding-sh))
    Dimensions of NIfTI image "`sub-01_model-csd_param-gm_model.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#encoding-sh))
    Dimensions of NIfTI image "`sub-01_model-csd_param-csf_model.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#encoding-sh))

    Contents of JSON file "`sub-01_model-csd_param-wm_model.json`":

    ```JSON
    {
        "Model": {
            "Description": "Multi-Shell Multi-Tissue (MSMT) Constrained Spherical Deconvolution (CSD)",
            "URL": "https://mrtrix.readthedocs.io/en/latest/constrained_spherical_deconvolution/multi_shell_multi_tissue_csd.html",
        },
        "Description": "White matter",
        "NonNegativity": "constrained",
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "Reference": "xyz",
            "SphericalHarmonicBasis": "MRtrix3",
            "SphericalHarmonicDegree": 8,
            "Type": "sh",
        },
        "ResponseFunction": {
            "Coefficients": [ [ 600.2 0.0 0.0 0.0 0.0 0.0 ],
                              [ 296.3 -115.2 24.7 -4.4 -0.5 1.8 ],
                              [ 199.8 -111.3 41.8 -10.2 2.1 -0.7 ],
                              [ 158.3 -98.7 48.4 -17.1 4.5 -1.4 ] ],
            "Type": "zsh"
        }
    }
    ```

    Contents of JSON file "`sub-01_model-csd_param-gm_dwimap.json`":

    ```JSON
    {
        "Model": {
            "Description": "Multi-Shell Multi-Tissue (MSMT) Constrained Spherical Deconvolution (CSD)",
            "URL": "https://mrtrix.readthedocs.io/en/latest/constrained_spherical_deconvolution/multi_shell_multi_tissue_csd.html",
        },
        "Description": "Gray matter",
        "NonNegativity": "constrained",
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "Reference": "xyz",
            "SphericalHarmonicBasis": "MRtrix3",
            "SphericalHarmonicDegree": 0,
            "Type": "sh",
        },
        "ResponseFunction": {
            "Coefficients": [ [ 1041.0 ],
                              [ 436.6 ],
                              [ 224.9 ],
                              [ 128.8 ] ],
            "Type": "zsh"
        }
    }
    ```

    Contents of JSON file "`sub-01_model-csd_param-csf_dwimap.json`":

    ```JSON
    {
        "Model": {
            "Description": "Multi-Shell Multi-Tissue (MSMT) Constrained Spherical Deconvolution (CSD)",
            "URL": "https://mrtrix.readthedocs.io/en/latest/constrained_spherical_deconvolution/multi_shell_multi_tissue_csd.html",
        },
        "Description": "Cerebro-spinal fluid",
        "NonNegativity": "constrained",
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "Reference": "xyz",
            "SphericalHarmonicBasis": "MRtrix3",
            "SphericalHarmonicDegree": 0,
            "Type": "sh"
        },
        "ResponseFunction": {
            "Coefficients": [ [ 3544.90770181 ],
                              [ 134.441453035 ],
                              [ 32.0826839826 ],
                              [ 29.3674604452 ] ],
            "Type": "zsh"
        }
    }
    ```

    Notes:

    -   In this example,
        the gray matter and CSF compartments are specified in the spherical harmonics basis
        with maximal spherical harmonic degrees of zero,
        even though each image only contains a single volume
        and could therefore be interpreted as simply scalar parameters.
        This is recommended in this instance
        given that the spherical harmonic basis imposes a $\sqrt(4\pi)$ scaling
        that should be taken into account if comparing the values of these parameters
        with the *l*=0 term of the white matter ODF.

    -   The response functions for GM and CSF have a maximal zonal spherical harmonic degree of zero,
        such that only one coefficient is required for each unique *b*-value shell.
        It is however nevertheless vital that these data be provided as a list of lists of floats,
        where the length of each list is one;
        storing these values as a list of floats would be erroneously interpreted
        as coefficients of different zonal spherical harmonic degrees for a single *b*-value shell.

-   An FSL `bedpostx` Ball-And-Sticks fit
    (including both mean parameters and bootstrap realisations):

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_model-bs_desc-mean_param-s0_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-s0_dwimap.json
                sub-01_model-bs_desc-mean_param-polar_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-polar_dwimap.json
                sub-01_model-bs_desc-mean_param-vector_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-vector_dwimap.json
                sub-01_model-bs_desc-mean_param-vf_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-vf_dwimap.json
                sub-01_model-bs_desc-mean_param-vfsum_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-vfsum_dwimap.json
                sub-01_model-bs_desc-mean_param-diffusivity_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-diffusivity_dwimap.json
                sub-01_model-bs_desc-mean_param-dstd_dwimap.nii.gz
                sub-01_model-bs_desc-mean_param-dstd_dwimap.json
                sub-01_model-bs_desc-merged_param-polar_dwimap.nii.gz
                sub-01_model-bs_desc-merged_param-polar_dwimap.json
                sub-01_model-bs_desc-merged_param-vf_dwimap.nii.gz
                sub-01_model-bs_desc-merged_param-vf_dwimap.json
    ```

    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-s0_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-polar_dwimap.nii.gz`": *I*x*J*x*K*x(*2*x*N*) ([spherical coordinates](#encoding-spherical), orientations only; *N* orientations per voxel)
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-vector_dwimap.nii.gz`": *I*x*J*x*K*x(*3*x*N*) ([3-vectors](#encoding-3vectors), unit norm; *N* orientations per voxel)
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-vf_dwimap.nii.gz`": *I*x*J*x*K*x*N* ([scalar](#encoding-scalar); *N* values per voxel)
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-vfsum_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-diffusivity_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))
    Dimensions of NIfTI image "`sub-01_model-bs_desc-mean_param-dstd_dwimap.nii.gz`": *I*x*J*x*K* ([scalar](#encoding-scalar))
    Dimensions of NIfTI image "`sub-01_model-bs_desc-merged_param-polar_dwimap.nii.gz`": *I*x*J*x*K*x(*2*x*N*)x*R* ([spherical coordinates](#encoding-spherical), orientations only; *N* orientations per voxel; *R* bootstrap realisations)
    Dimensions of NIfTI image "`sub-01_model-bs_desc-merged_param-vf_dwimap.nii.gz`": *I*x*J*x*K*x*N*x*R* ([scalar](#encoding-scalar); *N* values per voxel; *R* bootstrap realisations)

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-s0_dwimap.json`":

    ```JSON
    {
        "Description": "Estimated signal intensity with no diffusion weighting, ie. S0; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        }
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-polar_dwimap.json`":

    ```JSON
    {
        "Description": "Fibre orientations encoded using polar angles; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "Reference": "ijk",
            "Type": "unitspherical"
        }
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-vector_dwimap.json`":

    ```JSON
    {
        "Description": "Fibre orientations encoded using 3-vectors; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "Reference": "ijk",
            "Type": "unit3vector"
        }
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-vf_dwimap.json`":

    ```JSON
    {
        "Description": "Volume fractions of stick components; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "OrientationEncoding": {
            "Type": "scalar"
        }
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-vfsum_dwimap.json`":

    ```JSON
    {
        "Description": "Sum of volume fractions of stick components; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        }
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-diffusivity_dwimap.json`":

    ```JSON
    {
        "Description": "Diffusivity; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "Units": "mm^2/s"
    }
    ```

    Contents of JSON file "`sub-01_model-bs_desc-mean_param-dstd_dwimap.json`":

    ```JSON
    {
        "Description": "Diffusivity variance parameter; mean across bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "Units": "TODO"
    }

    Contents of JSON file "`sub-01_model-bs_desc-merged_param-polar_dwimap.json`":

    ```JSON
    {
        "BootstrapAxis": 4,
        "Description": "Fibre orientations encoded using polar angles; concatenated bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "OrientationEncoding": {
            "EncodingAxis": 3,
            "ReferenceAxes": "ijk",
            "Type": "unitspherical"
        }
    }

    Contents of JSON file "`sub-01_model-bs_desc-merged_param-vf_dwimap.json`":

    ```JSON
    {
        "BootstrapAxis": 4,
        "Description": "Volume fractions of stick components; concatenated bootstrap realisations",
        "Model": {
            "Description": "Ball-And-Sticks model using FSL bedpostx",
            "URL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
            "Parameters": {
                "ARDFudgeFactor": 1.0,
                "Fibers": 3
            },
            "BootstrapParameters": {
                "Burnin": 1000,
                "Jumps": 1250,
                "SampleEvery": 25
            }
        },
        "OrientationEncoding": {
            "Type": "scalar"
        }
    }

    Notes:

    -   Here the descriptors "`merged`" and "`mean`" have been utilised
        to distinguish between the comprehensive set of all bootstrap realisations
        and the computed mean statistics of parameters across all realisations respectively,
        as this is the terminology utilised by the FSL software itself.
        These labels are not however a part of the specification.

    -   Care must be taken for images of greater than three dimensions
        where additional dimensions do *not* encode anisotropy information:

        -   In image `"*_desc-mean*_param-vf_*"`,
            the fourth image axis encodes scalar information across stick components.
            Since this is *not* coefficients in some orientation encoding,
            but the image possesses more than three axes,
            field `"OrientationEncoding"["Type"]` MUST be specified as `"scalar"`.

        -   Image `"*_param-vfsum_*"`is a three-dimensional image,
            and therefore the fact that it encodes a scalar parameter
            can be robustly inferred without reference to metadata information.

        -   In image `"sub-01_model-bs_desc-merged_param-vf_dwimap.json"`,
            there are two extra image dimensions beyond the three spatial dimensions:
            the fourth image axis encodes across the multiple stick components per voxel,
            and the fifth axis encodes realisations across bootstraps.
            it is therefore necessary to explicitly specify
            that the parameter being encoded in the data,
            being the volume fractions of individual stick components,
            do not have any anisotropy,
            and therefore field `"OrientationEncoding"["Type"]` MUST be specified as `"scalar"`.

    -   TODO CONFIRM WHETHER WE WANT TO ENFORCE THIS OR INCLUDE EXPLICIT METADATA FIELDS
        THAT INDICATE THE AXIS / AXES OF DIRECTION ENCODING VS. BOOTSTRAP REALISATIONS

    -   TODO DISCUSS
        The example presented here is not necessarily a unique solution
        for the storage of the outcomes of the FSL `bedpostx` command as BIDS Derivatives:

        -   WOULD SPLITTING STICK COMPONENTS ACROSS NIFTIS
            REQUIRE A NEW ENTITY BY WHICH TO INDEX THEM?
            OR JUST GIVE THEM EG. `_param-spherical1`, `_param-spherical2`?

        -   While the FSL `bedpostx` command yields the fibre orientation for each individual stick
            as polar angles within separate NIfTI images,
            for BIDS it is RECOMMENDED that such orientation information be encoded
            either as [spherical coordinates](#encoding-spherical) or [3-vectors](#encoding-3vector).

        -   Given that it is possible to encode a scalar parameter
            into either [spherical coordinates](#encoding-spherical) or [3-vectors](#encoding-3vector) encodings,
            it is possible to store an image that encodes,
            for each stick component,
            both volume fraction and orientation.
            It is however RECOMMENDED to encode this information in separate files,
            given that in the more general case there may be multiple scalar parameters
            individually attributed to each component.

### Appendix

#### Spherical Harmonics

-   Concepts shared across all spherical harmonics bases:

    -   Basis functions:

        ![SH basis functions](https://latex.codecogs.com/gif.latex?Y_l^m(\theta,\phi)&space;=&space;\sqrt{\frac{(2l&plus;1)}{4\pi}\frac{(l-m)!}{(l&plus;m)!}}&space;P_l^m(\cos&space;\theta)&space;e^{im\phi}")

        for integer *order* *l*, *phase* *m*, associated Legendre polynomials *P*.

    -   (Truncated) basis coefficients:

        ![SH basis coefficients](https://latex.codecogs.com/gif.latex?f(\theta,\phi)&space;=&space;\sum_{l=0}^{l_\text{max}}&space;\sum_{m=-l}^{l}&space;c_l^m&space;Y_l^m(\theta,\phi)")

        for *maximum* spherical harmonic order *l<sub>max</sub>*.

    -   Functions assumed to be real: conjugate symmetry is assumed, i.e.
        *Y*(*l*,-*m*) = *Y*(*l*,*m*)\*, where \* denotes the complex
        conjugate.

    -   Antipodally symmetric: all basis functions with odd degree are
        assumed zero; `AntipodalSymmetry` MUST NOT be set to `False`.

    -   Utilized basis functions:

        -   `mrtrix3`

        ![MRtrix3 SH basis functions](https://latex.codecogs.com/gif.latex?Y_{lm}(\theta,\phi)=\begin{Bmatrix}&space;0&\text{if&space;}l\text{&space;is&space;odd},\\&space;\sqrt{2}\times\text{Im}\left[Y_l^{-m}(\theta,\phi)\right]&\text{if&space;}m<0,\\&space;Y_l^0(\theta,\phi)&\text{if&space;}m=0,\\&space;\sqrt{2}\times\text{Re}\left[Y_l^m(\theta,\phi)\right]&\text{if&space;}m>0\\&space;\end{Bmatrix})

        -   `descoteaux`

        ![Descoteaux SH basis functions](https://latex.codecogs.com/gif.latex?Y_{lm}(\theta,\phi)=\begin{Bmatrix}&space;0&\text{if&space;}l\text{&space;is&space;odd},\\&space;\sqrt{2}\times\text{Re}\left[Y_l^{-m}(\theta,\phi)\right]&\text{if&space;}m<0,\\&space;Y_l^0(\theta,\phi)&\text{if&space;}m=0,\\&space;\sqrt{2}\times\text{Im}\left[Y_l^m(\theta,\phi)\right]&\text{if&space;}m>0\\&space;\end{Bmatrix})

    -   Mapping between image volume *V* and spherical harmonic basis
        function coefficient *Y<sub>l,m</sub>*:

        *V<sub>l,m</sub>* = (*l*(*l*+1) / 2) + *m*

        | ***V*** | **Coefficient**    |
        | ------- | ------------------ |
        | 0       | *Y<sub>0,0</sub>*  |
        | 1       | *Y<sub>2,-2</sub>* |
        | 2       | *Y<sub>2,-1</sub>* |
        | 3       | *Y<sub>2,0</sub>*  |
        | 4       | *Y<sub>2,1</sub>*  |
        | 5       | *Y<sub>2,2</sub>*  |
        | 6       | *Y<sub>4,-4</sub>* |
        | 7       | *Y<sub>4,-3</sub>* |
        | ...     | ...                |

    -   Relationship between maximal spherical harmonic degree *l<sub>max</sub>*
        and number of image volumes *N*:

        *N* = ((*l<sub>max</sub>*+1) x (*l<sub>max</sub>*+2)) / 2

        | ***l<sub>max</sub>*** | 0 | 2 | 4  | 6  | 8  | 10 | ...  |
        | --------------------- |--:|--:|--: |--: |--: |--: | :--: |
        | ***N***               | 1 | 6 | 15 | 28 | 45 | 66 | ...  |

    -   Relationship between maximal degree of *zonal* spherical harmonic
        function (spherical harmonics function where all *m* != 0 terms are
        assumed to be zero; used for e.g. response function definition) and
        number of coefficients *N*:

        *N* = 1 + (*l<sub>max</sub>* / 2)

        | ***l<sub>max</sub>*** | 0 | 2 | 4 | 6 | 8 | 10 | ...  |
        | --------------------- |--:|--:|--:|--:|--:|--: | :--: |
        | ***N***               | 1 | 2 | 3 | 4 | 5 | 6  | ...  |
