# Diffusion derivatives

## Preprocessed diffusion-weighted images

Multiple different versions of preprocessing can be stored for the same source
data. To distinguish them from each other, the `desc` filename keyword can be
used. Details of preprocessing performed for each variation of the processing
should be included in the pipeline documentation.

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>][_desc-<label>]_dwi.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_dwi.bvals
            <source_keywords>[_space-<space>][_desc-<label>]_dwi.bvecs
            <source_keywords>[_space-<space>][_desc-<label>]_dwi.json
```

The JSON sidecar file is REQUIRED (due to the REQUIRED `SkullStripped` field -
see [Common Data Types](02-common-data-types.md)), and MAY additionally be used to
store information about what preprocessing options were used (for example
whether denoising was performed, corrections applied for field inhomogeneity /
gradient non-linearity / subject motion / eddy currents, etc.).

Additional reserved JSON metadata fields:

| **Key name**                           | **Description**                                                                                                                                   |
| -------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Denoising                              | OPTIONAL. String. Denoising method                                                                                                                |
| GibbsRingingCorrection                 | OPTIONAL. Boolean. Removal of Gibbs ringing artifacts                                                                                             |
| MotionCorrection                       | OPTIONAL. String. Motion correction; allowed values: `none`, `volume`, `slice`                                                                    |
| EddyCurrentCorrection                  | OPTIONAL. String. Eddy current distortion correction; reserved values: `none`, `linear`, `quadratic`, `cubic`                                     |
| IntensityNormalizationMethod           | OPTIONAL. String. Method (if any) used for intensity normalization                                                                                |
| FieldInhomogeneityEstimation           | OPTIONAL. String. Method (if any) used for estimation of the B0 inhomogeneity field; reserved values: `multiecho`, `phaseencode`, `registration`  |
| FieldInhomogeneityCorrection           | OPTIONAL. String. Correction for geometric distortions arising from B0 magnetic field inhomogeneity; reserved values: `none`, `static`, `dynamic` |
| GradientNonLinearityGeometryCorrection | OPTIONAL. Boolean. Correction for geometric distortions arising from non-linearity of gradients                                                   |
| GradientNonLinearityQSpaceCorrection   | OPTIONAL. Boolean. Correction for spatial inhomogeneity of diffusion sensitisation gradient strength                                              |
| SliceDropoutDetection                  | OPTIONAL. Boolean. Detection of signal dropout in acquired slices during pre-processing                                                           |
| SliceDropoutReplacement                | OPTIONAL. Boolean. Replacement of image data within slices containing signal dropout with predicted values                                        |
| BiasFieldCorrectionMethod              | OPTIONAL. String. Method (if any) used for correction of B1 RF field inhomogeneity                                                                |

## Diffusion models

Diffusion MRI can be modeled using various paradigms to extract more
informative representations of the diffusion process and the underlying
biological structure. A wide range of such models are available, each of
which has its own unique requirements with respect to:

-  The [input](#paramdef-input) parameters required in order to
   define / constrain the model;

-  The appropriate [data representations](#data-representations) utilised to
   store information parameterised [by](#paramdef-intrinsic) or
   [from](#paramdef-extrinsic) the model onto the filesystem;

-  The requirements for encapsulation and complete representation of
   derived [orientation information](#orientation-specification), which is
   a key strength of diffusion MRI but presents unique challenges for
   correct interpretation.

### Parameter terminology

Throughout this document, the term "parameter" is used to refer to
multiple distinct sources of information. The distinction between
these uses is defined thus:

1. <a name="paramdef-input">*Input*</a> model parameter:

   Value or non-numerical setting that influences the conformation
   of the diffusion model to the empirical diffusion-weighted data.

1. <a name="paramdef-intrinsic">*Intrinsic*</a> model parameter:

   Value that is the direct result of fitting the diffusion model to the
   empirical diffusion-weighted data.

1. <a name="paramdef-extrinsic">*Extrinsic*</a> model parameter:

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
            <source_keywords>[_space-<space>][_desc-<label>]_parameter-<intparam1>_<model>.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_parameter-<intparam2>_<model>.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_<model>.json

            [<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam1>_<model>.nii[.gz]]
            [<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam1>_<model>.json]
            [<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam2>_<model>.nii[.gz]]
            [<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam2>_<model>.json]
```

-  Field "`<model>`" is a unique identifier corresponding to the particular
   diffusion model. If the particular diffusion model is one that is included
   in this specification, then the [prescribed model label](intrinsic-model-parameters)
   MUST be utilised; e.g. "`dti`" for the diffusion tensor model.

-  Files "`<source_keywords>[_space-<space>][_desc-<label>]_parameter-<intparam*>_<model>.nii[.gz]`"
   provide data corresponding to the various [intrinsic](#paramdef-intrinsic) parameters
   of the model. In cases where [intrinsic](#paramdef-intrinsic) model parameters are all
   contained within a single image file, field "`_parameter-`" nevertheless MUST be
   included, with value "`all`"; e.g.:

   ```Text
   <pipeline_name>/
       sub-<participant_label>/
           dwi/
               <source_keywords>[_space-<space>][_desc-<label>]_parameter-all_<model>.nii[.gz]
               <source_keywords>[_space-<space>][_desc-<label>]_<model>.json
   ```

-  File "`<source_keywords>[_space-<space>][_desc-<label>]_<model>.json`"
   provides basic model information and [input](#paramdef-input)
   model parameters.

-  OPTIONAL images "`<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam*>_<model>.nii[.gz]`"
   may be defined, in order to provide additional [extrinsic](#paramdef-extrinsic)
   model parameters.

-  OPTIONAL files "`<source_keywords>[_space-<space>][_desc-<label>]_parameter-<extparam*>_<model>.json`"
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

1. <a name="data-scalar">*Scalars*</a>:

   Any model parameter image (whether [intrinsic](#paramdef-intrinsic) or
   [extrinsic](#paramdef-extrinsic)) where a solitary numerical value is
   defined in each 3D image voxel is referred to here as a "scalar" image.

1. <a name="data-dec">*Directionally-Encoded Colours (DEC)*</a>:

   4D image with three volumes, intended to be interpreted as red, green
   and blue colour intensities for visualisation
   \[[Pajevic1999](#pajevic1999)\]. Image data MUST NOT contain negative
   values.

1. <a name="data-spherical">*Spherical coordinates*</a>:

   4D image where data across volumes within each voxel encode one or
   more discrete orientations using angles on the 2-sphere, optionally
   exploiting the distance from origin to encode the value of some parameter.

   This may take one of two forms:

   1. Value per direction

      Each consecutive triplet of image volumes encodes a spherical
      coordinate, using ISO convention for both the order of parameters
      and reference frame for angles:

      1. Distance from origin; value of embedded parameter MUST be
         indicated in "`_parameter-*`" filename field;

      1. Inclination / polar angle, in radians, relative to the zenith
         direction being the positive direction of the *third* reference
         axis (see [orientation specification](#orientation-specification));

      1. Azimuth angle, in radians, orthogonal to the zenith direction,
         with value of 0.0 corresponding to the *first* reference axis
         (see [orientation specification](#orientation-specification)),
         increasing according to the right-hand rule about the zenith
         direction.

      Number of image volumes is equal to (3x*N*), where *N* is the maximum
      number of discrete orientations in any voxel in the image.

   1. Directions only

      Each consecutive pair of image volumes encodes inclination /
      azimuth pairs, with order & convention identical to that above
      (equivalent to spherical coordinate with assumed unity distance from
      origin).

      Number of image volumes is equal to (2x*N*), where *N* is the maximum
      number of discrete orientations in any voxel in the image.

1. <a name="data-3vector">*3-Vectors*</a>:

   4D image where data across volumes within each voxel encode one or
   more discrete orientations using triplets of axis dot products.

   This representation may be used in one of two ways:

   1. Value per direction

      Each 3-vector, once explicitly normalized, provides a direction
      on the unit sphere; the *norm* of each 3-vector additionally encodes
      the magnitude of some model parameter, the nature of which MUST be
      indicated in the "`_parameter-*`" filename field.

   2. Directions only

      Each triplet of values encodes an orientation on the unit sphere
      (i.e. the 3-vector data are normalized); no quantitative value is
      associated with each triplet.

   Number of image volumes is equal to (3x*N*), where *N* is the maximum
   number of discrete orientations in any voxel in the image.

1. <a name="data-sh">*Spherical Harmonics (SH)*</a>:

   4D image where data across volumes within each voxel represent a
   continuous function spanning the 2-sphere as coefficient values using a
   spherical harmonics basis.

   Number of image volumes depends on the spherical harmonic basis employed,
   and the maximal spherical harmonic degree *l<sub>max</sub>* (see
   [spherical harmonics bases](#spherical-harmonics-bases)).

1. <a name="data-amp">*Amplitudes*</a>:

   4D image where data across volumes within each voxel represent
   amplitudes of a discrete function spanning the 2-sphere.

   Number of image volumes corresponds to the number of discrete directions
   on the unit sphere along which samples for the spherical function in
   each voxel are provided; these directions MUST themselves be provided
   in the associated sidecar JSON file (see [orientation specification](#orientation-specification)).

1. <a name="data-pdf">*Probability Distribution Functions (PDFs)*</a>:

   ***TODO***

1. <a name="data-param">*Parameter vectors*</a>:

   4D image containing, for every image voxel, data corresponding to some
   set of model parameters, the names and order of which are defined within
   the [intrinsic](#paramdef-intrinsic) model parameters section.

### Intrinsic model parameters

The following models are codified within the specification, and the model
label should be used as the final field in the filename for storage of any
intrinsic or extrinsic parameters. If a new model is used, common sense
should be used to derive a name following the BIDS standard, and should
ideally be integrated in a future version of the specification.

| Model label | Full Name                                                                                                                                       | [Data representation](#data-representations)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `bs`        | Ball-and-Stick(s) model \[[Behrens2003](#behrens2003)\],\[[Behrens2007](#behrens2007)\],\[[Jbabdi2012](#jbabdi2012)\]                           | One [spherical coordinates](#data-spherical) image with parameter name "`sticks`", providing both fibre volume fractions and orientations using polar angles;<br>Optional scalar images with parameter names {"`bzero`", "`dmean`", "`dstd`"} providing the model-estimated *b*=0 signal intensity, mean stick diffusivity, and standard deviation of stick diffusivities respectively                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `csa`       | Constant Solid Angle \[[Aganj2010](#aganj2010)\]                                                                                                | [Spherical harmonics](#data-sh) image                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `csd`       | Constrained Spherical Deconvolution \[[Tournier2007](#tournier2007)\],\[[Descoteaux2009](#descoteaux2009)\],\[[Jeurissen2014](#jeurissen2014)\] | [Spherical harmonics](#data-sh) image<br>If a multi-tissue decomposition is performed, provide one individual 4D image per tissue, with "`_desc-<desc>`" filename field being an abbreviation of the tissue estimated by that particular ODF                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| `dki`       | Diffusion Kurtosis Imaging \[[Jensen2005](#jensen2005)\]                                                                                        | Single [parameter vectors](#data-param) image with parameter name "`all`" with 21 volumes in the order: *D<sub>xx</sub>*, *D<sub>xy</sub>*, *D<sub>xz</sub>*, *D<sub>yy</sub>*, *D<sub>yz</sub>*, *D<sub>zz</sub>*, *W<sub>xxxx</sub>*, *W<sub>yyyy</sub>*, *W<sub>zzzz</sub>*, *W<sub>xxxy</sub>*, *W<sub>xxxz</sub>*, *W<sub>xyyy</sub>*, *W<sub>yyyz</sub>*, *W<sub>xzzz</sub>*, *W<sub>yzzz</sub>*, *W<sub>xxyy</sub>*, *W<sub>xxzz</sub>*, *W<sub>yyzz</sub>*, *W<sub>xxyz</sub>*, *W<sub>xyyz</sub>*, *W<sub>xyzz</sub>* (*D* is the diffusion tensor, *W* is the kurtosis tensor)<br>OR<br>6 diffusion tensor coefficients as [parameter vectors](#data-param) image with parameter name "`tensor`";<br>15 kurtosis tensor coefficients as [parameter vectors](#data-param) image with parameter name "`kurtosis`";<br>Optional: estimated *b*=0 intensity as scalar image with parameter name "`bzero`"                                                                              |
| `dsi`       | Diffusion Spectrum Imaging \[[Wedeen2008](#wedeen2008)\],\[[Paquette2017](paquette2017)\]                                                       | [Probability distribution functions](#data-pdf)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| `dti`       | Diffusion Tensor Imaging \[[Basser1994](#basser1994)\]                                                                                          | Single [parameter vectors](#data-param) image with parameter name "`all`" with 6 volumes in the order: *D<sub>xx</sub>*, *D<sub>xy</sub>*, *D<sub>xz</sub>*, *D<sub>yy</sub>*, *D<sub>yz</sub>*, *D<sub>zz</sub>*<br>OR<br>Tensor coefficients as [parameter vectors](#data-param) image with parameter name "`tensor`";<br>Estimated *b*=0 intensity as [scalar](#data-scalar) image with parameter name "`bzero`"                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `forecast`  | Fiber ORientation Estimated using Continuous Axially Symmetric Tensors \[[Zuchelli2017](#zuchelli2017)\]                                        | [Spherical harmonics](#data-sh) image                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `fwdti`     | Free water DTI \[[Hoy2015](#hoy2015)\]                                                                                                          | One [parameter vectors](#data-param) image with parameter name "`tensor`", containing 6 volumes in the order: *Dc<sub>xx</sub>*, *Dc<sub>xy</sub>*, *Dc<sub>xz</sub>*, *Dc<sub>yy</sub>*, *Dc<sub>yz</sub>*, *Dc<sub>zz</sub>* (*Dc* is the free-water-corrected diffusion tensor);<br>One [scalar](#data-scalar) image with parameter name "`fwf`" corresponding to the estimated free water fraction                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| `mapmri`    | Mean Apparent Propagator MRI \[[Ozarslan2013](#ozarslan2013)\]                                                                                  |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `noddi`     | Neurite Orientation Dispersion and Density Imaging \[[Zhang2012](#zhang2012)\],\[[Daducci2015](#daducci2015)\]                                  | Three [scalar](#data-scalar) images, with parameter names equal to {"`icvf`", "`isovf`", "`od`"} (ICVF is the “intracellular volume fraction” (also known as NDI); ISOVF is the "isotropic component volume fraction"; OD is the “orientation dispersion” (the variance of the Watson distribution; also known as ODI));<br>One [3-vectors](#data-3vector) image with parameter name "`direction`" to provide the estimated fibre orientation                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| `qbi`       | Q-Ball Imaging \[[Tuch2004](#tuch2004)\], \[[Hess2006](#hess2006)\]                                                                             | Single [amplitudes](#data-amp) image<br>OR<br>Single [spherical harmonics](#data-sh) image                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| `shore`     | Simple Harmonic Oscillator-based Reconstruction and Estimation \[[Ozarslan2008](#ozarslan2008)\]                                                |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| `wmti`      | White Matter Tract Integrity \[[Fieremans2011](#fieremans2011)\]                                                                                | One [parameter vectors](#data-param) image with parameter name "`coeffs`", with 33 volumes in the order: *D<sub>xx</sub>*, *D<sub>xy</sub>*, *D<sub>xz</sub>*, *D<sub>yy</sub>*, *D<sub>yz</sub>*, *D<sub>zz</sub>*, *W<sub>xxxx</sub>*, *W<sub>yyyy</sub>*, *W<sub>zzzz</sub>*, *W<sub>xxxy</sub>*, *W<sub>xxxz</sub>*, *W<sub>xyyy</sub>*, *W<sub>yyyz</sub>*, *W<sub>xzzz</sub>*, *W<sub>yzzz</sub>*, *W<sub>xxyy</sub>*, *W<sub>xxzz</sub>*, *W<sub>yyzz</sub>*, *W<sub>xxyz</sub>*, *W<sub>xyyz</sub>*, *W<sub>xyzz</sub>*, *Dh<sub>xx</sub>*, *Dh<sub>xy</sub>*, *Dh<sub>xz</sub>*, *Dh<sub>yy</sub>*, *Dh<sub>yz</sub>*, *Dh<sub>zz</sub>*, *Dr<sub>xx</sub>*, *Dr<sub>xy</sub>*, *Dr<sub>xz</sub>*, *Dr<sub>yy</sub>*, *Dr<sub>yz</sub>*, *Dr<sub>zz</sub>* (*D* is the diffusion tensor and *W* is the kurtosis tensor);<br>One [scalar](#data-scalar) image with parameter name "`awf`", representing the estimated axonal water fraction |

The JSON sidecar for the intrinsic diffusion model parameters may contain
the following key/value pairs irrespective of the particular model:

| **Key name**     | **Description**                                                                                                                                                                              |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Gradients        | OPTIONAL. List of 3-vectors. Subset of gradients utilized to fit the model, as a list of three-elements lists. If not present, all gradients were used.                                      |
| Shells           | OPTIONAL. List of floats. Shells that were utilized to fit the model, as a list of b-values. If the key is not present, it should be assumed that all shells were used during model fitting. |
| Mask             | OPTIONAL. String. Name of image that was used as a binary mask to specify those voxels for which the model was fit.                                                                          |
| ModelDescription | OPTIONAL. String. Extended information to describe the model.                                                                                                                                |
| ModelURL         | OPTIONAL. String. URL to the implementation of the specific model utilized.                                                                                                                  |
| Parameters       | OPTIONAL. Dictionary. [Input](#paramdef-input) model parameters that are constant across the image (see examples below).                                                                    |

#### Model bootstrapping

Results of model bootstrapping can be provided by concatenating multiple
realisations of model intrinsic parameters along an additional image axis.

The corresponding sidecar JSON file may include dictionary field
"`BootstrapParameters`", descibing those input parameters specific to
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

-  `bs` :

   -  `ARDFudgeFactor`: Float. Weight applied to Automatic Relevance Determination (ARD).
   -  `Fibers`: Integer. Number of discrete fibres to fit in each voxel.
   -  `ModelBall`: String. Model used to describe the "ball" component in the model.
   -  `ModelSticks`: String. Model used to describe the "stick" component in the model.

-  `csa` :

   -  `SphericalHarmonicOrder` : value
   -  `Smoothing` : value
   -  `Basis` : value

-  `csd`:

   -  `NonNegativityConstraint`: String. Options are: { `soft`, `hard` }. Specifies whether the ODF was estimated using regularisation ("`soft`") or prevention ("`hard`") of negative values.
   -  `ResponseFunctionZSH`: Two options:
      -  Vector of floating-point values, where values correspond to the response function coefficient for each consecutive even zonal spherical harmonic degree starting from zero (in this case field "`Shells`" should contain a single integer value);
      -  Matrix of floating-point values: 1 row per unique *b*-value as listed in "`Shells`"; 1 column per even zonal spherical harmonic degree starting from zero; if there are a different number of non-zero zonal spherical harmonic coefficients for different *b*-values, these must be padded with zeroes such that all rows contain the same number of columns.
   -  `ResponseFunctionTensor`: Vector of 4 floating-point values: three tensor eigenvalues, then reference *b*=0 intensity
   -  `SphericalHarmonicBasis`: String. Options are: { `MRtrix3`, `Descoteaux` }. Details are provided in the [spherical harmonics bases](#spherical-harmonics-bases) section.
   -  `SphericalHarmonicDegree`: Integer. The maximal spherical harmonic order *l<sub>max</sub>*; the number of volumes in the associated NIfTI image must correspond to this value as per the relationship described in [spherical harmonics bases](#spherical-harmonics-bases) section.
   -  `Tissue`: String. A more verbose description for the tissue estimated via this specific ODF.

-  `dsi` :

   -  `GridSize` : value
   -  `RStart` : value
   -  `RStep` : value
   -  `REnd` : value
   -  `FilterWidth` : value

-  `dti` :

   -  `RESTORESigma`: Float

-  `forecast` :

   -  `Sphere` : value
   -  `DecAlg` : value
   -  `LambdaLb` : value
   -  `SphericalHarmonicsOrder` : value

-  `mapmri` :

   -  `RadialOrder` : value
   -  `LaplacianRegularization` : bool
   -  `LaplacianWeighting` : value
   -  `PositivityConstraint` : bool
   -  `Tau` : value
   -  `ConstrainE0` : value
   -  `PositiveConstraint` : value
   -  `PosGrid` : value
   -  `PosRadius` : value
   -  `AnisotropicScaling` : bool
   -  `EigenvalueThreshold` : value
   -  `PosGrid` : value
   -  `BvalThreshold` : value
   -  `DTIScaleEstimation` : bool
   -  `StaticDiffusivity` : value

-  `noddi`:

   -  `DPar` : value
   -  `DIso` : value
   -  `Lambda1` : value
   -  `Lambda2` : value

-  `shore` :

   -  `RadialOrder` : value
   -  `Zeta` : value
   -  `LambdaN` : value
   -  `LambdaL` : value
   -  `Tau` : value
   -  `ConstrainE0` : value
   -  `PositiveConstraint` : value
   -  `PosGrid` : value
   -  `PosRadius` : value

### Extrinsic model parameters

| `<parameter>` value | Description                                                            | [Data representation](#data-representations) | Possible Model sources                          | Unit or scale                                                  |
| ------------------- | ---------------------------------------------------------------------- | -------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------- |
| `ad`                | Axial Diffusivity (also called parallel diffusivity)                   | [Scalar](#data-scalar)                       | { `dki`, `dti`, `forecast`, `fwdti`, `wmti` }   | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `ak`                | Axial kurtosis                                                         | [Scalar](#data-scalar)                       | { `dki`, `wmti` }                               | Unitless                                                       |
| `afdtotal`          | Total Apparent Fibre Density (AFD) \[[Calamante2015](#calamante2015)\] | [Scalar](#data-scalar)                       | { `csd` }                                       | Unitless                                                       |
| `cl`                | Tensor linearity \[[Westin1997](#westin1997)\]                         | [Scalar](#data-scalar)                       | { `dki`, `dti`, `fwdti`, `wmti` }               |                                                                |
| `cp`                | Tensor planarity \[[Westin1997](#westin1997)\]                         | [Scalar](#data-scalar)                       | { `dki`, `dti`, `fwdti`, `wmti` }               |                                                                |
| `cs`                | Tensor sphericity \[[Westin1997](#westin1997)\]                        | [Scalar](#data-scalar)                       | { `dki`, `dti`, `fwdti`, `wmti` }               |                                                                |
| `evec`              | Eigenvector(s)                                                         | [3-vectors](#data-3vector)                   | { `dki`, `dti`, `fwdti`, `wmti` }               | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `fa`                | Fractional Anisotropy \[[Basser1996](#basser1996)\]                    | [Scalar](#data-scalar)                       | { `dki`, `dti`, `forecast`, `fwdti`, `wmti` }   | Proportion \[0.0-1.0\]                                         |
| `fsum`              | Sum of partial volume fractions of stick components                    | [Scalar](#data-scalar)                       | { `bs` }                                        | Volume fraction \[0.0-1.0\]                                    |
| `gfa`               | Generalized Fractional Anisotropy \[[Tuch2004](#tuch2004)\]            | [Scalar](#data-scalar)                       | { `csa`, `csd`, `forecast`, `mapmri`, `shore` } | Proportion \[0.0-1.0\]                                         |
| `md`                | Mean diffusivity (also called apparent diffusion coefficient, ADC)     | [Scalar](#data-scalar)                       | { `dki`, `dti`, `forecast`, `fwdti`, `wmti` }   | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `mk`                | Mean kurtosis                                                          | [Scalar](#data-scalar)                       | { `dki`, `wmti` }                               | Unitless                                                       |
| `mode`              | Mode of the tensor                                                     | [Scalar](#data-scalar)                       | { `dki`, `dti`, `fwdti`, `wmti` }               |                                                                |
| `msd`               | Mean-Squared Displacement                                              | [Scalar](#data-scalar)                       | { `mapmri`, `shore` }                           |                                                                |
| `pdf`               | Diffusion propagator                                                   | [3-vectors](#data-3vector)                   |                                                 |                                                                |
| `peak`              | Direction(s) and amplitude(s) of ODF maximum (maxima)                  | [3-vectors](#data-3vector)                   | { `csa`, `csd`, `forecast`, `shore` }           | Same units as ODF                                              |
| `rd`                | Radial Diffusivity (also called perpendicular diffusivity)             | [Scalar](#data-scalar)                       | { `dki`, `dti`, `forecast`, `fwdti`, `wmti` }   | \mu m<sup>2</sup>.ms<sup>-1</sup> <sup>[1](#diffusivity)</sup> |
| `rk`                | Radial kurtosis                                                        | [Scalar](#data-scalar)                       | { `dki`, `wmti` }                               | Unitless                                                       |
| `rtap`              | Return To Axis Probability                                             | [Scalar](#data-scalar)                       | { `mapmri` }                                    | Probability \[0.0-1.0\]                                        |
| `rtop`              | Return To Origin Probability                                           | [Scalar](#data-scalar)                       | { `shore` }                                     | Probability \[0.0-1.0\]                                        |
| `rtpp`              | Return To Plane Probability                                            | [Scalar](#data-scalar)                       | { `mapmri` }                                    | Probability \[0.0-1.0\]                                        |
| `tort`              | Tortuosity of extra-cellular space                                     | [Scalar](#data-scalar)                       | { `dki` }                                       |                                                                |

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
| `SphericalHarmonicBasis`    | [Spherical harmonics](#data-sh)                                                                                                                                                                                   | REQUIRED. String; allowed values: { `MRtrix3`, `Descoteaux` }. Basis by which to define the interpretation of image values across volumes as spherical harmonics coefficients.                                                                            |
| `SphericalHarmonicDegree`   | [Spherical harmonics](#data-sh)                                                                                                                                                                                   | REQUIRED. Integer. Maximal degree of the spherical harmonic basis employed.                                                                                                                                                                               |

If `AntipodalSymmetry` is True, then no constraints are imposed with respect
to the domain on the 2-sphere in which orientations may be specified;
for instance, 3-vectors { 0.57735, 0.57735, 0.57735 } and
{ -0.57735, -0.57735, -0.57735 } are both permissible and equivalent to one
another.

#### Spherical Harmonics bases

-  `MRtrix3`

   -  Antipodally symmetric: all basis functions with odd degree are
      assumed zero; `AntipodalSymmetry` MUST NOT be set to True.

   -  Functions assumed to be real: conjugate symmetry is assumed, i.e.
      *Y*(*l*,-*m*) = *Y*(*l*,*m*)\*, where \* denotes the complex
      conjugate.

   -  Mapping of image volumes to spherical harmonic basis function
      coefficients:

      | **Volume** | **Coefficient**                   |
      | ---------- | --------------------------------- |
      | 0          | *l* = 0, *m* = 0                  |
      | 1          | *l* = 2, *m* = 2 (imaginary part) |
      | 2          | *l* = 2, *m* = 1 (imaginary part) |
      | 3          | *l* = 2, *m* = 0                  |
      | 4          | *l* = 2, *m* = 1 (real part)      |
      | 5          | *l* = 2, *m* = 2 (real part)      |
      | 6          | *l* = 4, *m* = 4 (imaginary part) |
      | 7          | *l* = 4, *m* = 3 (imaginary part) |
      | ...        | etc.                              |

   -  Normalisation: ***TODO***

   -  Relationship between maximal spherical harmonic degree *l<sub>max</sub>*
      and number of image volumes *N*:

      *N* = ((*l<sub>max</sub>*+1) x (*l<sub>max</sub>*+2)) / 2

      | ***l<sub>max</sub>*** |  0  |  2  |  4  |  6  |  8  | ...  |
      | --------------------- | --: | --: | --: | --: | --: | :--: |
      | ***N***               |   1 |   6 |  15 |  28 |  45 | etc. |

   -  Relationship between maximal degree of *zonal* spherical harmonic
      function (spherical harmonics function where all *m* != 0 terms are
      assumed to be zero; used for e.g. response function definition) and
      number of coefficients *N*:

      *N* = 1 + (*l<sub>max</sub>* / 2)

      | ***l<sub>max</sub>*** |  0  |  2  |  4  |  6  |  8  | ...  |
      | --------------------- | --: | --: | --: | --: | --: | :--: |
      | ***N***               |   1 |   2 |  3  |  4  |  5  | etc. |

-  `Descoteaux`

   ***TODO***

## Demonstrative examples

-  A basic Diffusion Tensor fit:

   ```Text
   my_diffusion_pipeline/
       sub-01/
           dwi/
               sub-01_dti.nii.gz
               sub-01_dti.json
   ```

   Dimensions of NIfTI image "`sub-01_dti.nii.gz`": *I*x*J*x*K*x6 ([parameter vectors](#data-param))

   Contents of JSON file:

   ```JSON
   {
       "Model": "Diffusion Tensor",
       "OrientationRepresentation": "param",
       "ReferenceAxes": "xyz",
       "Parameters": {
           "FitMethod": "ols",
           "OutlierRejection": False
       }
   }
   ```

-  A multi-shell, multi-tissue Constrained Spherical Deconvolution fit:

   ```Text
   my_diffusion_pipeline/
       sub-01/
           dwi/
               sub-01_desc-wm_csd.nii.gz
               sub-01_desc-wm_csd.json
               sub-01_desc-gm_csd.nii.gz
               sub-01_desc-gm_csd.json
               sub-01_desc-csf_csd.nii.gz
               sub-01_desc-csf_csd.json
               sub-01_csd.json
   ```

   Dimensions of NIfTI image "`sub-01_desc-wm_csd.nii.gz`": *I*x*J*x*K*x45 ([spherical harmonics](#data-sh))
   Dimensions of NIfTI image "`sub-01_desc-gm_csd.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#data-sh))
   Dimensions of NIfTI image "`sub-01_desc-csf_csd.nii.gz`": *I*x*J*x*K*x1 ([spherical harmonics](#data-sh))

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

   Contents of JSON file "`sub-01_desc-wm_csd.json`":

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

   Contents of JSON file "`sub-01_desc-gm_csd.json`":

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

-  A NODDI fit:

   ```Text
   my_diffusion_pipeline/
       sub-01/
           dwi/
               sub-01_parameter-icvf_noddi.nii.gz
               sub-01_parameter-isovf_noddi.nii.gz
               sub-01_parameter-od_noddi.nii.gz
               sub-01_parameter-direction_noddi.nii.gz
               sub-01_parameter-direction_noddi.json
               sub-01_noddi.json
   ```

   Dimensions of NIfTI image "`sub-01_parameter-icvf_noddi.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_parameter-isovf_noddi.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_parameter-od_noddi.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_parameter-direction_noddi.nii.gz`": *I*x*J*x*K*x3 ([3-vectors](#data-3vector))

   Contents of file "`sub-01_noddi.json`" (common to all [intrinsic](#paramdef-intrinsic) model parameter images):

   ```JSON
   {
       "Model": "Neurite Orientation Dispersion and Density Imaging (NODDI)",
       "ModelURL": "https://www.nitrc.org/projects/noddi_toolbox"
   }
   ```

   Contents of JSON file "`sub-01_parameter-direction_noddi.json`":

   ```JSON
   {
       "OrientationRepresentation": "3vector",
       "ReferenceAxes": "???"
   }
   ```

-  An FSL `bedpostx` Ball-And-Sticks fit (including both mean parameters and
   bootstrap realisations):

   ```Text
   my_diffusion_pipeline/
       sub-01/
           dwi/
               sub-01_desc-mean_parameter-bzero_bs.nii.gz
               sub-01_desc-mean_parameter-dmean_bs.nii.gz
               sub-01_desc-mean_parameter-dstd_bs.nii.gz
               sub-01_desc-mean_parameter-sticks_bs.nii.gz
               sub-01_desc-mean_parameter-sticks_bs.json
               sub-01_desc-merged_parameter-sticks_bs.nii.gz
               sub-01_desc-merged_parameter-sticks_bs.json
               sub-01_bs.json
   ```

   Dimensions of NIfTI image "`sub-01_desc-mean_parameter-bzero_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_desc-mean_parameter-dmean_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_desc-mean_parameter-dstd_bs.nii.gz`": *I*x*J*x*K* ([scalar](#data-scalar))
   Dimensions of NIfTI image "`sub-01_desc-mean_parameter-sticks_bs.nii.gz`": *I*x*J*x*K*x9 ([spherical coordinates](#data-spherical), distance from origin encodes fibre volume fraction)
   Dimensions of NIfTI image "`sub-01_desc-merged_parameter-sticks_bs.nii.gz`": *I*x*J*x*K*x9x50 ([spherical coordinates](#data-spherical), distance from origin encodes fibre volume fraction; 50 bootstrap realisations)

   Contents of JSON files "`sub-01_desc-mean_parameter-sticks_bs.json`"
   and "`sub-01_desc-merged_parameter-sticks_bs.json`" (contents of two
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

-----

<a name="diffusivity"><sup>1</sup></a>: For example, for free water in body
temperature, the diffusivity in units of \mu m<sup>2</sup>.ms<sup>-1</sup>
should be approximately 3.0.

-----

<a name="aganj2010">\[Aganj2010\]</a>: Aganj et al. 2010

<a name="basser1994">\[Basser1994\]</a>: Basser et al. 1994

<a name="basser1996">\[Basser1996\]</a>: Basser et al. 1996

<a name="behrens2003">\[Behrens2003\]</a> Behrens et al. 2003

<a name="behrens2007">\[Behrens2007\]</a> Behrens et al. 2007

<a name="calamante2015">\[Calamante2015\]</a>: Calamante et al. 2015

<a name="daducci2015">\[Daducci2015\]</a>: Daducci et al. 2015

<a name="descoteaux2009">\[Descoteaux2009\]</a>: Descoteaux et al. 2009

<a name="fieremans2011">\[Fieremans2011\]</a>: Fieremans et al. 2011

<a name="hess2006">\[Hess2006\]</a>: Hess et al. 2006

<a name="hoy2014">\[Hoy2014\]</a>: Hoy et al. 2014

<a name="jbabdi2012">\[Jbabdi2012\]</a> Jbabdi et al. 2012

<a name="jensen2005">\[Jensen2005\]</a>: Jensen et al. 2005

<a name="jeurissen2014">\[Jeurissen2014\]</a>: Jeurissen et al. 2014

<a name="ozarslan2008">\[Ozarslan2008\]</a>: Ozarslan et al. 2008

<a name="ozarslan2013">\[Ozarslan2013\]</a>: Ozarslan 2013

<a name="paquette2017">\[Paquette2017\]</a>: Paquette et al 2017

<a name="pajevic1999">\[Pajevic1999\]</a>: Pajevic et al 1999

<a name="tournier2007">\[Tournier2007\]</a>: Tournier et al. 2007

<a name="tuch2004">\[Tuch2004\]</a>: Tuch 2004

<a name="wedeen2008">\[Wedeen2008\]</a>: Wedeen et al. 2008

<a name="westin1997">\[Westin1997\]</a>: Westin 1997

<a name="zhang2012">\[Zhang2012\]</a>: Zhang et al. 2012

<a name="zuchelli2017">\[Zuchelli2017\]</a>: Zuchelli et al. 2017
