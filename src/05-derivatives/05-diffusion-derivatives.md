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

Diffusion MRI can be modeled using various paradigms to extract more
informative representations of the diffusion process and the underlying
biological structure. A wide range of such models are available, each of
which has its own unique requirements with respect to:

-   The [input](#paramdef-input) parameters required in order to
    define / constrain the model;

-   The appropriate [data representations](#data-representations) utilised to
    store information parameterised [by](#paramdef-intrinsic) or
    [from](#paramdef-extrinsic) the model onto the filesystem;

-   The requirements for encapsulation and complete representation of
    derived [orientation information](#orientation-specification), which is
    a key strength of diffusion MRI but presents unique challenges for
    correct interpretation.

### Parameter terminology

Throughout this document, the term "parameter" is used to refer to
multiple distinct sources of information. The distinction between
these uses is defined thus:

1.  <a name="paramdef-input">*Input*</a> model parameter:

    Value or non-numerical setting that influences the conformation
    of the diffusion model to the empirical diffusion-weighted data.

1.  <a name="paramdef-intrinsic">*Intrinsic*</a> model parameter:

    Value that is the direct result of fitting the diffusion model to the
    empirical diffusion-weighted data.

1.  <a name="paramdef-extrinsic">*Extrinsic*</a> model parameter:

    Value that can be calculated directly from previously estimated
    intrinsic model parameters, without necessitating reference to
    the empirical diffusion-weighted data.

For example, consider a diffusion tensor model fit: the number of
iterations in the optimisation algorithm would be an *input* parameter;
the six unique diffusion tensor coefficients would be the *intrinsic*
parameters; the Fractional Anisotropy (FA) would be an *extrinsic*
parameter (as it is calculated from the diffusion tensor coefficients
rather than the image data).

### File names

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>][_desc-<label>]_param-<intparam1>_<model>.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_param-<intparam2>_<model>.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_<model>.json

            [<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam1>_<model>.nii[.gz]]
            [<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam1>_<model>.json]
            [<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam2>_<model>.nii[.gz]]
            [<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam2>_<model>.json]
```

-   Field "`<model>`" is a unique identifier corresponding to the particular
    diffusion model. If the particular diffusion model is one that is included
    in this specification, then the [prescribed model label](intrinsic-model-parameters)
    MUST be utilised; e.g. "`tensor`" for the diffusion tensor model.

-   Files "`<source_keywords>[_space-<space>][_desc-<label>]_param-<intparam*>_<model>.nii[.gz]`"
    provide data corresponding to the various [intrinsic](#paramdef-intrinsic) parameters
    of the model. In cases where [intrinsic](#paramdef-intrinsic) model parameters are all
    contained within a single image file, field "`_param-`" nevertheless MUST be
    included, with value "`all`"; e.g.:

    ```Text
    <pipeline_name>/
        sub-<participant_label>/
            dwi/
                <source_keywords>[_space-<space>][_desc-<label>]_param-all_<model>.nii[.gz]
                <source_keywords>[_space-<space>][_desc-<label>]_<model>.json
    ```

-   File "`<source_keywords>[_space-<space>][_desc-<label>]_<model>.json`"
    provides basic model information and [input](#paramdef-input)
    model parameters.

-   OPTIONAL images "`<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam*>_<model>.nii[.gz]`"
    may be defined, in order to provide additional [extrinsic](#paramdef-extrinsic)
    model parameters.

-   OPTIONAL files "`<source_keywords>[_space-<space>][_desc-<label>]_param-<extparam*>_<model>.json`"
    may be defined to provide only information or parameters relevant to
    derivation of each relevant [extrinsic](#paramdef-extrinsic) model
    parameter image.

### Data representations

There are multiple techniques by which data that relate to the anisotropic
nature of either the diffusion process or underlying tissue may be
arranged and/or encoded into NIfTI image data. A list of known techniques
is enumerated below, accompanied by requisite information specific to the
reading / writing of each representation.

For data that encode orientation information, there are fields that MUST
be specified in the sidecar JSON file in order to ensure appropriate
interpretation of that information; see [orientation specification](#orientation-specification)).

1.  <a name="data-scalar">*Scalars*</a>:

    Any model parameter image (whether [intrinsic](#paramdef-intrinsic) or
    [extrinsic](#paramdef-extrinsic)) where a solitary numerical value is
    defined in each 3D image voxel is referred to here as a "scalar" image.

1.  <a name="data-dec">*Directionally-Encoded Colours (DEC)*</a>:

    4D image with three volumes, intended to be interpreted as red, green
    and blue colour intensities for visualisation
    \[[Pajevic1999](#pajevic1999)\]. Image data MUST NOT contain negative
    values.

1.  <a name="data-spherical">*Spherical coordinates*</a>:

    4D image where data across volumes within each voxel encode one or
    more discrete orientations using angles on the 2-sphere, optionally
    exploiting the distance from origin to encode the value of some parameter.

    This may take one of two forms:

    1.  Value per direction

        Each consecutive triplet of image volumes encodes a spherical
        coordinate, using ISO convention for both the order of parameters
        and reference frame for angles:

        1.  Distance from origin; value of embedded parameter MUST be
            indicated in "`_param-*`" filename field;

        1.  Inclination / polar angle, in radians, relative to the zenith
            direction being the positive direction of the *third* reference
            axis (see [orientation specification](#orientation-specification));

        1.  Azimuth angle, in radians, orthogonal to the zenith direction,
            with value of 0.0 corresponding to the *first* reference axis
            (see [orientation specification](#orientation-specification)),
            increasing according to the right-hand rule about the zenith
            direction.

        Number of image volumes is equal to (3x*N*), where *N* is the maximum
        number of discrete orientations in any voxel in the image.

    1.  Directions only

        Each consecutive pair of image volumes encodes inclination /
        azimuth pairs, with order & convention identical to that above
        (equivalent to spherical coordinate with assumed unity distance from
        origin).

        Number of image volumes is equal to (2x*N*), where *N* is the maximum
        number of discrete orientations in any voxel in the image.

1.  <a name="data-3vector">*3-Vectors*</a>:

    4D image where data across volumes within each voxel encode one or
    more discrete orientations using triplets of axis dot products.

    This representation may be used in one of two ways:

    1.  Value per direction

        Each 3-vector, once explicitly normalized, provides a direction
        on the unit sphere; the *norm* of each 3-vector additionally encodes
        the magnitude of some model parameter, the nature of which MUST be
        indicated in the "`_param-*`" filename field.

    1.  Directions only

        Each triplet of values encodes an orientation on the unit sphere
        (i.e. the 3-vector data are normalized); no quantitative value is
        associated with each triplet.

    Number of image volumes is equal to (3x*N*), where *N* is the maximum
    number of discrete orientations in any voxel in the image.

1.  <a name="data-sh">*Spherical Harmonics (SH)*</a>:

    4D image where data across volumes within each voxel represent a
    continuous function spanning the 2-sphere as coefficient values using a
    spherical harmonics basis.

    Number of image volumes depends on the spherical harmonic basis employed,
    and the maximal spherical harmonic degree *l<sub>max</sub>* (see
    [spherical harmonics bases](#spherical-harmonics-bases)).

1.  <a name="data-amp">*Amplitudes*</a>:

    4D image where data across volumes within each voxel represent
    amplitudes of a discrete function spanning the 2-sphere.

    Number of image volumes corresponds to the number of discrete directions
    on the unit sphere along which samples for the spherical function in
    each voxel are provided; these directions MUST themselves be provided
    in the associated sidecar JSON file (see [orientation specification](#orientation-specification)).

1.  <a name="data-param">*Parameter vectors*</a>:

    4D image containing, for every image voxel, data corresponding to some
    set of model parameters, the names and order of which are defined within
    the [intrinsic](#paramdef-intrinsic) model parameters section.

### Intrinsic model parameters

The following models are codified within the specification, and the model
label should be used as the final field in the filename for storage of any
intrinsic or extrinsic parameters. If a new model is used, common sense
should be used to derive a name following the BIDS standard, and should
ideally be integrated in a future version of the specification.

| Model label | Full Name                                                                                                                                       | [Data representation](#data-representations)                                                                                                                                                                                                                                                                                                                                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bs`        | Ball-and-Stick(s) model \[[Behrens2003](#behrens2003)\],\[[Behrens2007](#behrens2007)\],\[[Jbabdi2012](#jbabdi2012)\]                           | One [spherical coordinates](#data-spherical) image with parameter name "`sticks`", providing both fibre volume fractions and orientations using polar angles;<br>Optional scalar images with parameter names {"`bzero`", "`dmean`", "`dstd`"} providing the model-estimated *b*=0 signal intensity, mean stick diffusivity, and standard deviation of stick diffusivities respectively                              |
| `csd`       | Constrained Spherical Deconvolution \[[Tournier2007](#tournier2007)\],\[[Descoteaux2009](#descoteaux2009)\],\[[Jeurissen2014](#jeurissen2014)\] | [Spherical harmonics](#data-sh) image<br>If a multi-tissue decomposition is performed, provide one individual 4D image per tissue, with "`_desc-<desc>`" filename field being an abbreviation of the tissue estimated by that particular ODF                                                                                                                                                                        |
| `tensor`    | Diffusion Tensor \[[Basser1994](#basser1994)\]                                                                                                  | Single [parameter vectors](#data-param) image with parameter name "`all`" with 6 volumes in the order: *D<sub>xx</sub>*, *D<sub>xy</sub>*, *D<sub>xz</sub>*, *D<sub>yy</sub>*, *D<sub>yz</sub>*, *D<sub>zz</sub>*<br>OR<br>Tensor coefficients as [parameter vectors](#data-param) image with parameter name "`tensor`";<br>Estimated *b*=0 intensity as [scalar](#data-scalar) image with parameter name "`bzero`" |

The JSON sidecar for the intrinsic diffusion model parameters may contain
the following key/value pairs irrespective of the particular model:

| **Key name**     | **Description**                                                                                                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gradients        | OPTIONAL. List of 3-vectors. Subset of gradients utilized to fit the model, as a list of three-elements lists. If not present, all gradients were used.                                      |
| Shells           | OPTIONAL. List of floats. Shells that were utilized to fit the model, as a list of b-values. If the key is not present, it should be assumed that all shells were used during model fitting. |
| Mask             | OPTIONAL. String. Name of image that was used as a binary mask to specify those voxels for which the model was fit.                                                                          |
| ModelDescription | OPTIONAL. String. Extended information to describe the model.                                                                                                                                |
| ModelURL         | OPTIONAL. String. URL to the implementation of the specific model utilized.                                                                                                                  |
| Parameters       | OPTIONAL. Dictionary. [Input](#paramdef-input) model parameters that are constant across the image (see examples below).                                                                     |

#### Model bootstrapping

Results of model bootstrapping can be provided by concatenating multiple
realisations of model intrinsic parameters along an additional image axis.

The corresponding sidecar JSON file may include dictionary field
"`BootstrapParameters`", describing those input parameters specific to
the determination and export of multiple realisations of the model fit
in each image voxel.

### Input model parameters

Parameters that may / must be stored within the JSON sidecar "`Parameters`"
field depends on the particular model used.

"`Parameters`" fields that may be applicable to multiple models:

| **Key name**     | **Description**                                                                                                                                                                                                                                                                                        |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| FitMethod        | OPTIONAL. String. The optimisation procedure used to fit the intrinsic model parameters to the empirical diffusion-weighted signal. Options are: "`ols`" (Ordinary Least Squares); "`wls`" (Weighted Least Squares); "`iwls`" (Iterative Weighted Least Squares); "`nlls`" (Non-Linear Least Squares). |
| Iterations       | OPTIONAL. Integer. The number of iterations used for any form of model fitting procedure where the number of iterations is a fixed input parameter.                                                                                                                                                    |
| OutlierRejection | OPTIONAL. Boolean. Value indicating whether or not rejection of outlier values was performed during fitting of the intrinsic model parameters.                                                                                                                                                         |
| Samples          | OPTIONAL. Integer. The number of realisations of a diffusion model from which statistical summaries (e.g. mean, standard deviation) of those parameters are provided.                                                                                                                                  |

Reserved keywords for models built into the specification are as follows:

-   `bs` :

    -   `ARDFudgeFactor`: Float. Weight applied to Automatic Relevance Determination (ARD).
    -   `Fibers`: Integer. Number of discrete fibres to fit in each voxel.
    -   `ModelBall`: String. Model used to describe the "ball" component in the model.
    -   `ModelSticks`: String. Model used to describe the "stick" component in the model.

-   `csd`:

    -   `NonNegativityConstraint`: String. Options are: { `soft`, `hard` }. Specifies whether the ODF was estimated using regularisation ("`soft`") or prevention ("`hard`") of negative values.

    -   `ResponseFunctionZSH`: Two options:

        -   Vector of floating-point values, where values correspond to the response function coefficient for each consecutive even zonal spherical harmonic degree starting from zero (in this case field "`Shells`" should contain a single integer value);
        -   Matrix of floating-point values: 1 row per unique *b*-value as listed in "`Shells`"; 1 column per even zonal spherical harmonic degree starting from zero; if there are a different number of non-zero zonal spherical harmonic coefficients for different *b*-values, these must be padded with zeroes such that all rows contain the same number of columns.

    -   `ResponseFunctionTensor`: Vector of 4 floating-point values: three tensor eigenvalues, then reference *b*=0 intensity

    -   `SphericalHarmonicBasis`: String. Options are: { `MRtrix3` }. Details are provided in the [spherical harmonics bases](#spherical-harmonics-bases) section.

    -   `SphericalHarmonicDegree`: Integer. The maximal spherical harmonic order *l<sub>max</sub>*; the number of volumes in the associated NIfTI image must correspond to this value as per the relationship described in [spherical harmonics bases](#spherical-harmonics-bases) section.

    -   `Tissue`: String. A more verbose description for the tissue estimated via this specific ODF.

-   `tensor` :

    -   `RESTORESigma`: Float

### Extrinsic model parameters

| `<parameter>` value | Description                                                            | [Data representation](#data-representations) | Possible Model sources | Unit or scale                                                  |
| ------------------- | ---------------------------------------------------------------------- | -------------------------------------------- | ---------------------- | -------------------------------------------------------------- |
| `ad`                | Axial Diffusivity (also called parallel diffusivity)                   | [Scalar](#data-scalar)                       | { `tensor` }           | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `afdtotal`          | Total Apparent Fibre Density (AFD) \[[Calamante2015](#calamante2015)\] | [Scalar](#data-scalar)                       | { `csd` }              | Unitless                                                       |
| `cl`                | Tensor linearity \[[Westin1997](#westin1997)\]                         | [Scalar](#data-scalar)                       | { `tensor` }           |                                                                |
| `cp`                | Tensor planarity \[[Westin1997](#westin1997)\]                         | [Scalar](#data-scalar)                       | { `tensor` }           |                                                                |
| `cs`                | Tensor sphericity \[[Westin1997](#westin1997)\]                        | [Scalar](#data-scalar)                       | { `tensor` }           |                                                                |
| `evec`              | Eigenvector(s)                                                         | [3-vectors](#data-3vector)                   | { `tensor` }           | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `fa`                | Fractional Anisotropy \[[Basser1996](#basser1996)\]                    | [Scalar](#data-scalar)                       | { `tensor` }           | Proportion \[0.0-1.0\]                                         |
| `fsum`              | Sum of partial volume fractions of stick components                    | [Scalar](#data-scalar)                       | { `bs` }               | Volume fraction \[0.0-1.0\]                                    |
| `gfa`               | Generalized Fractional Anisotropy \[[Tuch2004](#tuch2004)\]            | [Scalar](#data-scalar)                       | { `csd` }              | Proportion \[0.0-1.0\]                                         |
| `md`                | Mean diffusivity (also called apparent diffusion coefficient, ADC)     | [Scalar](#data-scalar)                       | { `tensor` }           | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `mode`              | Mode of the tensor                                                     | [Scalar](#data-scalar)                       | { `tensor` }           |                                                                |
| `peak`              | Direction(s) and amplitude(s) of ODF maximum (maxima)                  | [3-vectors](#data-3vector)                   | { `csd` }              | Same units as ODF                                              |
| `rd`                | Radial Diffusivity (also called perpendicular diffusivity)             | [Scalar](#data-scalar)                       | { `tensor` }           | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |

While not explicitly included in the table above, *any* [scalar](#data-scalar)
[extrinsic](paramdef-extrinsic) parameter can theoretically be combined
with a separate source of orientation information from the diffusion model
in order to produce a [directionally-encoded colour](#data-dec),
[spherical coordinates](#data-spherical) or [3-vectors](#data-3vector) image.

### Orientation specification

| **Key name**                | **Relevant [data representations](#data-representations)**                                                                                                                                                        | **Description**                                                                                                                                                                                                                                           |
| --------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `AntipodalSymmetry`         | [Spherical coordinates](#data-spherical), [3-vectors](#data-3vector), [spherical harmonics](#data-sh), [amplitudes](#data-amp), [probability distribution functions](#data-pdf), [parameter vectors](#data-param) | OPTIONAL. Boolean. Indicates whether orientation information should be interpreted as being antipodally symmetric. Assumed to be True if omitted.                                                                                                         |
| `Directions`                | [Amplitudes](#data-amp)                                                                                                                                                                                           | REQUIRED. List. Data are either [spherical coordinates (directions only)](#data-spherical) or [3-vectors](#data-3vector) with unit norm. Defines the dense directional basis set on which samples of a spherical function within each voxel are provided. |
| `FillValue`                 | [Spherical coordinates](#data-spherical), [3-vectors](#data-3vector)                                                                                                                                              | OPTIONAL. Float; allowed values: { 0.0, NaN }. Value stored in image when number of discrete orientations in a voxel is fewer than the maximal number for that image.                                                                                     |
| `OrientationRepresentation` | All except [scalar](#data-scalar)                                                                                                                                                                                 | REQUIRED. String; allowed values: { `dec`, `unitspherical`, `spherical`, `unit3vector`, `3vector`, `sh`, `amp`, `pdf`, `param` }. The [data representation](#data-representations) used to encode orientation information within the NIfTI image.         |
| `ReferenceAxes`             | All except [scalar](#data-scalar)                                                                                                                                                                                 | REQUIRED. String; allowed values: { `ijk`, `xyz` }. Indicates whether the NIfTI image axes, or scanner-space axes, are used as reference axes for orientation information.                                                                                |
| `SphericalHarmonicBasis`    | [Spherical harmonics](#data-sh)                                                                                                                                                                                   | REQUIRED. String; allowed values: { `MRtrix3` }. Basis by which to define the interpretation of image values across volumes as spherical harmonics coefficients.                                                                                          |
| `SphericalHarmonicDegree`   | [Spherical harmonics](#data-sh)                                                                                                                                                                                   | REQUIRED. Integer. Maximal degree of the spherical harmonic basis employed.                                                                                                                                                                               |

If `AntipodalSymmetry` is True, then no constraints are imposed with respect
to the domain on the 2-sphere in which orientations may be specified;
for instance, 3-vectors { 0.57735, 0.57735, 0.57735 } and
{ -0.57735, -0.57735, -0.57735 } are both permissible and equivalent to one
another.

#### Spherical Harmonics

-   Concepts shared across all spherical harmonics bases:

    -   Basis functions:

        ![SH basis functions](https://latex.codecogs.com/gif.latex?Y_l^m(\theta,\phi)&space;=&space;\sqrt{\frac{(2l&plus;1)}{4\pi}\frac{(l-m)!}{(l&plus;m)!}}&space;P_l^m(\cos&space;\theta)&space;e^{im\phi}")

        for integer *order* *l*, *phase* *m*, associated Legendre polynomials *P*.

    -   (Truncated) basis coefficients:

        ![SH basis coefficients](https://latex.codecogs.com/gif.latex?f(\theta,\phi)&space;=&space;\sum_{l=0}^{l_\text{max}}&space;\sum_{m=-l}^{l}&space;c_l^m&space;Y_l^m(\theta,\phi)")

        for *maximum* spherical harmonic order *l<sub>max</sub>*.

-   `MRtrix3`

    -   Functions assumed to be real: conjugate symmetry is assumed, i.e.
        *Y*(*l*,-*m*) = *Y*(*l*,*m*)\*, where \* denotes the complex
        conjugate.

    -   Antipodally symmetric: all basis functions with odd degree are
        assumed zero; `AntipodalSymmetry` MUST NOT be set to `False`.

    -   Utilised basis functions:

        ![MRtrix3 SH basis functions](https://latex.codecogs.com/gif.latex?Y_{lm}(\theta,\phi)=\begin{Bmatrix}&space;0&\text{if&space;}l\text{&space;is&space;odd},\\&space;\sqrt{2}\times\text{Im}\left[Y_l^{-m}(\theta,\phi)\right]&\text{if&space;}m<0,\\&space;Y_l^0(\theta,\phi)&\text{if&space;}m=0,\\&space;\sqrt{2}\times\text{Re}\left[Y_l^m(\theta,\phi)\right]&\text{if&space;}m>0\\&space;\end{Bmatrix})

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
        | ...     | etc.               |

    -   Relationship between maximal spherical harmonic degree *l<sub>max</sub>*
        and number of image volumes *N*:

        *N* = ((*l<sub>max</sub>*+1) x (*l<sub>max</sub>*+2)) / 2

        | ***l<sub>max</sub>*** | 0 | 2 | 4  | 6  | 8  | ...  |
        | --------------------- |--:|--:|--: |--: |--: | :--: |
        | ***N***               | 1 | 6 | 15 | 28 | 45 | etc. |

    -   Relationship between maximal degree of *zonal* spherical harmonic
        function (spherical harmonics function where all *m* != 0 terms are
        assumed to be zero; used for e.g. response function definition) and
        number of coefficients *N*:

        *N* = 1 + (*l<sub>max</sub>* / 2)

        | ***l<sub>max</sub>*** | 0 | 2 | 4 | 6 | 8 | ...  |
        | --------------------- |--:|--:|--:|--:|--:| :--: |
        | ***N***               | 1 | 2 | 3 | 4 | 5 | etc. |

## Demonstrative examples

-   A basic Diffusion Tensor fit:

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_param-all_tensor.nii.gz
                sub-01_tensor.json
    ```

    Dimensions of NIfTI image "`sub-01_param-all_tensor.nii.gz`": *I*x*J*x*K*x6 ([parameter vectors](#data-param))

    Contents of JSON file:

    ```JSON
    {
        "Model": "Diffusion Tensor",
        "OrientationRepresentation": "param",
        "ReferenceAxes": "xyz",
        "Parameters": {
            "FitMethod": "ols",
            "OutlierRejection": false
        }
    }
    ```

-   A multi-shell, multi-tissue Constrained Spherical Deconvolution fit:

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_param-wm_csd.nii.gz
                sub-01_param-wm_csd.json
                sub-01_param-gm_csd.nii.gz
                sub-01_param-gm_csd.json
                sub-01_param-csf_csd.nii.gz
                sub-01_param-csf_csd.json
                sub-01_csd.json
    ```

    Dimensions of NIfTI image "`sub-01_param-wm_csd.nii.gz`": *I*x*J*x*K*x45 ([spherical harmonics](#data-sh))
    Dimensions of NIfTI image "`sub-01_param-gm_csd.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#data-sh))
    Dimensions of NIfTI image "`sub-01_param-csf_csd.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#data-sh))

    Contents of file "`sub-01_csd.json`" (common to all [intrinsic](#paramdef-intrinsic) model parameter images):

    ```JSON
    {
        "Model": "Multi-Shell Multi-Tissue (MSMT) Constrained Spherical Deconvolution (CSD)",
        "ModelURL": "https://mrtrix.readthedocs.io/en/latest/constrained_spherical_deconvolution/multi_shell_multi_tissue_csd.html",
        "Shells": [ 0, 1000, 2000, 3000 ],
        "Parameters": {
            "SphericalHarmonicBasis": "MRtrix3",
            "NonNegativityConstraint": "hard"
        }
    }
    ```

    Contents of JSON file "`sub-01_param-wm_csd.json`":

    ```JSON
    {
        "OrientationRepresentation": "sh",
        "ReferenceAxes": "xyz",
        "ResponseFunctionZSH": [ [ 600.2 0.0 0.0 0.0 0.0 0.0 ],
                                 [ 296.3 -115.2 24.7 -4.4 -0.5 1.8 ],
                                 [ 199.8 -111.3 41.8 -10.2 2.1 -0.7 ],
                                 [ 158.3 -98.7 48.4 -17.1 4.5 -1.4 ] ],
        "SphericalHarmonicDegree": 8,
        "Tissue": "White matter"
    }
    ```

    Contents of JSON file "`sub-01_param-gm_csd.json`":

    ```JSON
    {
        "OrientationRepresentation": "sh",
        "ReferenceAxes": "xyz",
        "ResponseFunctionZSH": [ [ 1041.0 ],
                                 [ 436.6 ],
                                 [ 224.9 ],
                                 [ 128.8 ] ],
        "SphericalHarmonicDegree": 0,
        "Tissue": "Grey matter"
    }
    ```

-   An FSL `bedpostx` Ball-And-Sticks fit (including both mean parameters and
    bootstrap realisations):

    ```Text
    my_diffusion_pipeline/
        sub-01/
            dwi/
                sub-01_desc-mean_param-bzero_bs.nii.gz
                sub-01_desc-mean_param-dmean_bs.nii.gz
                sub-01_desc-mean_param-dstd_bs.nii.gz
                sub-01_desc-mean_param-sticks_bs.nii.gz
                sub-01_desc-mean_param-sticks_bs.json
                sub-01_desc-merged_param-sticks_bs.nii.gz
                sub-01_desc-merged_param-sticks_bs.json
                sub-01_bs.json
    ```

    Dimensions of NIfTI image "`sub-01_desc-mean_param-bzero_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
    Dimensions of NIfTI image "`sub-01_desc-mean_param-dmean_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
    Dimensions of NIfTI image "`sub-01_desc-mean_param-dstd_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
    Dimensions of NIfTI image "`sub-01_desc-mean_param-sticks_bs.nii.gz`": *I*x*J*x*K*x9 ([spherical coordinates](#data-spherical), distance from origin encodes fibre volume fraction)
    Dimensions of NIfTI image "`sub-01_desc-merged_param-sticks_bs.nii.gz`": *I*x*J*x*K*x9x50 ([spherical coordinates](#data-spherical), distance from origin encodes fibre volume fraction; 50 bootstrap realisations)

    Contents of JSON files "`sub-01_desc-mean_param-sticks_bs.json`"
    and "`sub-01_desc-merged_param-sticks_bs.json`" (contents of two
    files are identical):

    ```JSON
    {
        "OrientationRepresentation": "spherical",
        "ReferenceAxes": "ijk"
    }
    ```

    Contents of JSON file "`sub-01_bs.json`":

    ```JSON
    {
        "Model": "Ball-And-Sticks model using FSL bedpostx",
        "ModelURL": "https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FDT",
        "Parameters": {
            "ARDFudgeFactor": 1.0,
            "Fibers": 3,
            "Samples": 50
        },
        "BootstrapParameters": {
            "Burnin": 1000,
            "Jumps": 1250,
            "SampleEvery": 25
        }
    }
    ```

---

<a name="diffusivity"><sup>1</sup></a>: For example, for free water in body
temperature, the diffusivity in units of \mu m<sup>2</sup>.ms<sup>-1</sup>
should be approximately 3.0.

---

<a name="basser1994">\[Basser1994\]</a>: Basser et al. 1994

<a name="basser1996">\[Basser1996\]</a>: Basser et al. 1996

<a name="behrens2003">\[Behrens2003\]</a> Behrens et al. 2003

<a name="behrens2007">\[Behrens2007\]</a> Behrens et al. 2007

<a name="calamante2015">\[Calamante2015\]</a>: Calamante et al. 2015

<a name="descoteaux2009">\[Descoteaux2009\]</a>: Descoteaux et al. 2009

<a name="jbabdi2012">\[Jbabdi2012\]</a> Jbabdi et al. 2012

<a name="jeurissen2014">\[Jeurissen2014\]</a>: Jeurissen et al. 2014

<a name="pajevic1999">\[Pajevic1999\]</a>: Pajevic et al 1999

<a name="tournier2007">\[Tournier2007\]</a>: Tournier et al. 2007

<a name="tuch2004">\[Tuch2004\]</a>: Tuch 2004

<a name="westin1997">\[Westin1997\]</a>: Westin 1997
