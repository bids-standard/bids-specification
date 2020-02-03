# Diffusion derivatives

## Preprocessed diffusion weighted images

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
see [Common Data Types](02-common-data-types.md)), and if present can be used to
store information about what preprocessing options were used (for example
whether denoising was performed, corrections applied for field inhomogeneity /
gradient non-linearity / subject motion / eddy currents, intensity normalization was
performed, etc.).

Additional reserved JSON metadata fields:

| **Key name**                   | **Description**                                                                                                              |
| ------------------------------ | ---------------------------------------------------------------------------------------------------------------------------- |
| Denoising                      | OPTIONAL. String. Denoising method                                                                                           |
| MotionCorrection               | OPTIONAL. Boolean. Motion correction                                                                                         |
| EddyCurrentCorrection          | OPTIONAL. Boolean. Eddy currents corrections                                                                                 |
| IntensityNormalizationMethod   | OPTIONAL. String. Method (if any) used for intensity normalization                                                           |
| FieldInhomogeneityCorrection   | OPTIONAL. Boolean. Correction for geometric distortions arising from magnetic field inhomogeneity                            |
| GradientNonLinearityCorrection | OPTIONAL. String. Correction for non-linear gradients; allowed values: `none`, `geometry`, `gradients`, `geometry&gradients` |

## Diffusion Models (and input parameters)

Diffusion MRI can be modeled using various paradigms to extract a more easily
understandable representation of the diffusion process and the underlying
structure. To do so, parameters might be needed to control how the signal is fit
to the model. Those parameters are called **input parameters** in the following.
Once the model is fit, the resulting representation can be saved using a number
of values per voxel. Those values will be called **output** or **estimated
parameters** in the following.

**Estimated parameters** are saved as NIFTI files (see section Models for the
expected content of each model), and **input parameters** are saved in the
sidecar JSON file.

The following is a general example of naming convention:

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>][_desc-<label>]_model-<label>[_parameter-<parameter>]_diffmodel.nii[.gz]
            <source_keywords>[_space-<space>][_desc-<label>]_model-<label>_diffmodel.json
```

The following models are codified and should be used in the `model-<label>`
field. If a new model is used, common sense should be used to derive a name
following the BIDS standard, and should ideally be integrated in a follow-up
version of the specification.

| Model label | Name & citation                                                                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| ----------- | ---------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `DTI`       | Diffusion tensor imaging (Basser et al. 1994)                                                  | 4D image with D<sub>xx</sub>, D<sub>xy</sub>, D<sub>xz</sub>, D<sub>yy</sub>, D<sub>yz</sub>, D<sub>zz</sub>; the 6 unique parameters of the diffusion tensor.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `DKI`       | Diffusion kurtosis imaging (Jensen et al., 2005)                                               | 4D image with D<sub>xx</sub>, D<sub>xy</sub>, D<sub>xz</sub>, D<sub>yy</sub>, D<sub>yz</sub>, D<sub>zz</sub>, W<sub>xxxx</sub>, W<sub>yyyy</sub>, W<sub>zzzz</sub>, W<sub>xxxy</sub>, W<sub>xxxz</sub>, W<sub>xyyy</sub>, W<sub>yyyz</sub>, W<sub>xzzz</sub>, W<sub>yzzz</sub>, W<sub>xxyy</sub>, W<sub>xxzz</sub>, W<sub>yyzz</sub>, W<sub>xxyz</sub>, W<sub>xyyz</sub>, W<sub>xyzz</sub>; Where D is the diffusion tensor and W is the kurtosis tensor.                                                                                                                                                                                                                                                                     |
| `WMTI`      | White matter tract integrity (Fieremans et al., 2011)                                          | 4D image with D<sub>xx</sub>, D<sub>xy</sub>, D<sub>xz</sub>, D<sub>yy</sub>, D<sub>yz</sub>, D<sub>zz</sub>, W<sub>xxxx</sub>, W<sub>yyyy</sub>, W<sub>zzzz</sub>, W<sub>xxxy</sub>, W<sub>xxxz</sub>, W<sub>xyyy</sub>, W<sub>yyyz</sub>, W<sub>xzzz</sub>, W<sub>yzzz</sub>, W<sub>xxyy</sub>, W<sub>xxzz</sub>, W<sub>yyzz</sub>, W<sub>xxyz</sub>, W<sub>xyyz</sub>, W<sub>xyzz</sub>, Dh<sub>xx</sub>, Dh<sub>xy</sub>, Dh<sub>xz</sub>, Dh<sub>yy</sub>, Dh<sub>yz</sub>, Dh<sub>zz</sub>, Dr<sub>xx</sub>, Dr<sub>xy</sub>, Dr<sub>xz</sub>, Dr<sub>yy</sub>, Dr<sub>yz</sub>, Dr<sub>zz</sub>, AWF; where D is the diffusion tensor, W is the kurtosis tensor, AWF is the additional axonal water fraction parameter |
| `CSD`       | Constrained Spherical Deconvolution (Tournier et al. 2007; Descoteaux et al. 2009)             | 4D image with spherical harmonic (SH) coefficients (number of volumes and their ordering depends on the model maximal degree and basis set, specified in the sidecar)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| `NODDI`     | Neurite Orientation Dispersion and Density Imaging (Zhang et al. 2012, Daducci et al., 2015)   | Three 3D images, with <parameter> equal to {`ICVF`,`OD`,`ISOVF`}: ICVF is the “intracellular volume fraction” (also known as NDI); OD is the “orientation dispersion” (the variance of the Bingham; also known as ODI); ISOVF is the isotropic component volume fraction (also known as IVF). Additionally a vector-valued map with the parameter name "`direction`" may provide the XYZ direction of the estimated fibre orientation.                                                                                                                                                                                                                                                                                        |
| `DSI`       | Diffusion Spectrum Imaging (Wedeen et al. 2008; Paquette et al 2017)                           | DSI is generally used to compute the diffusion ODF (Orientation Distribution Function). No parameters are generally returned, but an ODF can be saved as a map.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| `CSA`       | Constant solid angle (Aganj et al. 2010)                                                       | 4D image with SH coefficients (number of volumes and their ordering depends on the model maximal degree and basis set, specified in the side-car)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| `SHORE`     | Simple Harmonic Oscillator based Reconstruction and Estimation. (Ozarslan et al. 2008)         | 4D image with basis coefficients depending on choice of basis.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `MAPMRI`    | Mean Apparent Propagator MRI. (Ozarslan, 2013)                                                 | 4D image with basis coefficients depending on choice of basis.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `FORECAST`  | Fiber ORientation Estimated using Continuous Axially Symmetric Tensors. (Zuchelli et al. 2017) | 4D image with SH coefficients.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| `fwDTI`     | Free water DTI (Hoy et al. 2014)                                                               | One 4D image with parameter name "`tensor`", containing 6 volumes in the order Dc<sub>xx</sub>, Dc<sub>xy</sub>, Dc<sub>xz</sub>, Dc<sub>yy</sub>, Dc<sub>yz</sub>, Dc<sub>zz</sub>, where Dc is the fw-corrected diffusion tensor in each voxel; one 3D image with parameter name "`FWF`" corresponding to the free water fraction in each voxel. .                                                                                                                                                                                                                                                                                                                                                                          |
| `BedpostX`  | Ball-and-Stick model (Behrens et al. 2007; Jabdbi et al, MRM 2012)                             | 5D image (xyz, m, n) for m parameters and n MCMC samples (n=1 implies best-fit parameters). Parameters are f<sub>i</sub>, th<sub>i</sub>, ph<sub>i</sub> (volume fraction, polar angle, azimuthal angle) for up to 3 fibres, D, D<sub>std</sub> (for “multiexponential” model)                                                                                                                                                                                                                                                                                                                                                                                                                                                |

The JSON sidecar contains the following key/value pairs common for all models:

| **Key name**     | **Description**                                                                                                                      |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| Shells           | OPTIONAL. Shells that were utilized to fit the model, as a list of b-values. If the key is not present, all shells were used.        |
| Gradients        | OPTIONAL. Subset of gradients utilized to fit the model, as a list of three-elements lists. If not present, all gradients were used. |
| ModelDescription | OPTIONAL. Extended information to describe the model.                                                                                |
| ModelURL         | OPTIONAL. URL to the implementation of the specific model utilized.                                                                  |
| Parameters       | OPTIONAL. A dictionary of model parameters (see below).                                                                              |

Parameters that may be stored within the JSON sidecar "Parameters" field depend on the particular model used:

-   `DTI` :

    -   `FitMethod` : {`WLS`,`IWLS`,`OLS`,`NLLS`}
    -   `OutlierRejection`: boolean
    -   `RESTORESigma` : value

-   `DKI` and `WMTI`:

    -   `FitMethod` : {`WLS`,`IWLS`,`OLS`,`NLLS`}

-   `CSD`:

    -   `Tissue` : string
    -   `SphericalHarmonicDegree` : value
    -   `ResponseFunctionZSH` : values (1 row per unique *b*-value as listed in "`Shells`"; 1 column per even harmonic degree starting from zero)
    -   `ResponseFunctionTensor` : values (vector of 4 values: three tensor eigenvalues, then reference b=0 intensity)
    -   `SphericalHarmonicBasis` : {`MRtrix3`,`DESCOTEAUX`}
    -   `NonNegativityConstraint` : {`soft`,`hard`}

-   `NODDI`:

    -   `DPar` : value
    -   `DIso` : value
    -   `Lambda1` : value
    -   `Lambda2` : value

-   `DSI` :

    -   `GridSize` : value
    -   `RStart` : value
    -   `RStep` : value
    -   `REnd` : value
    -   `FilterWidth` : value

-   `CSA` :

    -   `SphericalHarmonicOrder` : value
    -   `Smoothing` : value
    -   `Basis` : value

-   `SHORE` :

    -   `RadialOrder` : value
    -   `Zeta` : value
    -   `LambdaN` : value
    -   `LambdaL` : value
    -   `Tau` : value
    -   `ConstrainE0` : value
    -   `PositiveConstraint` : value
    -   `PosGrid` : value
    -   `PosRadius` : value

-   `MAPMRI` :

    -   `RadialOrder` : value
    -   `LaplacianRegularization` : bool
    -   `LaplacianWeighting` : value
    -   `PositivityConstraint` : bool
    -   `Tau` : value
    -   `ConstrainE0` : value
    -   `PositiveConstraint` : value
    -   `PosGrid` : value
    -   `PosRadius` : value
    -   `AnisotropicScaling` : bool
    -   `EigenvalueThreshold` : value
    -   `PosGrid` : value
    -   `BvalThreshold` : value
    -   `DTIScaleEstimation` : bool
    -   `StaticDiffusivity` : value

-   `FORECAST` :

    -   `Sphere` : value
    -   `DecAlg` : value
    -   `LambdaLb` : value
    -   `SphericalHarmonicsOrder` : value

-   `fwDTI` :

    -   `FitMethod` : {"WLS","NLLS"}

-   `BEDPOSTX` :

    -   `NFibers` : value
    -   `Fudge` : value
    -   `BurnIn` : value
    -   `NJumps` : value
    -   `SampleEvery` : value
    -   `Model` : {`monoexponential`,`multiexponentialStick`,`multiexponentialZeppelin`}

Examples:

A Diffusion Tensor fit:

```Text
my_diffusion_pipeline/
    sub-01/
        dwi/
            sub-01_space-T1w_desc-WLS_model-DTI_diffmodel.nii.gz
            sub-01_space-T1w_desc-WLS_model-DTI_diffmodel.json
```

Contents of JSON file:

```JSON
{
    "Parameters": {
        "FitMethod": "WLS"
    }
}
```

A multi-shell, multi-tissue Constrained Spherical Deconvolution fit:

```Text
my_diffusion_pipeline/
    sub-01/
        dwi/
            sub-01_model-CSD_desc-WM_diffmodel.nii.gz
            sub-01_model-CSD_desc-WM_diffmodel.json
            sub-01_model-CSD_desc-GM_diffmodel.nii.gz
            sub-01_model-CSD_desc-GM_diffmodel.json
            sub-01_model-CSD_desc-CSF_diffmodel.nii.gz
            sub-01_model-CSD_desc-CSF_diffmodel.json
```

Contents of JSON file (using "`_tissue-WM`" as example):

```JSON
{
    "Shells": [ 0, 1000, 2000, 3000 ],
    "Parameters": {
        "Tissue": "White matter",
        "SphericalHarmonicDegree": 8,
        "ResponseFunctionZSH": [ [ 15335 0 0 0 0 0 ],
                                 [ 7688 -2766 597 -82 10 -5 ],
                                 [ 5258 -2592 1024 -270 48 -11 ],
                                 [ 4226 -2193 1124 -436 119 -19 ] ],
        "SphericalHarmonicBasis": "MRtrix3",
        "NonNegativityConstraint": "hard"
    }
}
```

A NODDI fit:

```Text
my_diffusion_pipeline/
    sub-01/
        dwi/
            sub-01_model-NODDI_parameter-ICVF_diffmodel.nii.gz
            sub-01_model-NODDI_parameter-OD_diffmodel.nii.gz
            sub-01_model-NODDI_parameter-ISOVF_diffmodel.nii.gz
            sub-01_model-NODDI_parameter-direction_diffmodel.nii.gz
            sub-01_model-NODDI_diffmodel.json
```

## Model-derived maps (output parameters)

Models output maps of estimated parameters. Commonly one parameter is estimated
per voxel; we call these maps of parameters. Two types of maps are described in
this specification: scalar and vector maps. Scalar maps are saved as 3D
.nii/nii.gz files. Vector maps are saved as 4D .nii/nii.gz files. Below the
specification for the naming of the files and a the list of currently accepted
fields for the maps.

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>]_model-<label>[_desc-<label>]_<parameter>.nii[.gz]
```

### Scalar maps

These maps are saved 3D NIfTI files (x,y,z). Some examples of such maps are as follows:

| `<parameter>` value | Description                                                        | Possible Model sources                                                             | Unit or scale                       |
| ------------------- | ------------------------------------------------------------------ | -----------------------------------------------------------------------------------| ----------------------------------- |
| FA                  | Fractional Anisotropy                                              | DTI, DKI, WMTI (D, Dh, Dr)                                                         | Unitless \[0-1\]                    |
| MD                  | Mean diffusivity (also called apparent diffusion coefficient, ADC) | DTI, DKI, WMTI (D, Dh, Dr)                                                         | microns<sup>2</sup>/ms <sup>1</sup> |
| AD                  | Axial Diffusivity (also called parallel diffusivity)               | DTI, DKI, WMTI (D, Dh, Dr)                                                         | microns<sup>2</sup>/ms <sup>1</sup> |
| RD                  | Radial Diffusivity (also called perpendicular diffusivity)         | DTI, DKI, WMTI (D, Dh, Dr)                                                         | microns<sup>2</sup>/ms <sup>1</sup> |
| MODE                | Mode of the tensor                                                 | DTI, DKI, WMTI (D, Dh, Dr)                                                         |                                     |
| LINEARITY           | Tensor linearity (Westin 1997)                                     | DTI, DKI, WMTI (D, Dh, Dr)                                                         |                                     |
| PLANARITY           | Tensor planarity (Westin 1997)                                     | DTI, DKI, WMTI (D, Dh, Dr)                                                         |                                     |
| SPHERICITY          | Tensor sphericity (Westin 1997)                                    | DTI, DKI, WMTI (D, Dh, Dr)                                                         |                                     |
| MK                  | Mean kurtosis                                                      | DKI, WMTI                                                                          | Unitless                            |
| RK                  | Radial kurtosis                                                    | DKI, WMTI                                                                          | Unitless                            |
| AK                  | Axial kurtosis                                                     | DKI, WMTI                                                                          | Unitless                            |
| GFA                 | Generalized Fractional Anisotropy                                  | CSA, CSD, SHORE, MAPMRI, Forecast (or any model that can be represented as an ODF) | Proportion \[0-1\]                  |
| FSUM                | Sum of partial volume fractions of stick components                | Ball-and-stick(s)                                                                  | Volume fraction \[0-1\]             |
| Fi                  | Volume fraction of stick i                                         | Ball-and-stick(s)                                                                  | Volume fraction \[0-1\]             |
| D                   | Diffusivity                                                        | Ball-and-stick(s)                                                                  | microns<sup>2</sup>/ms <sup>1</sup> |
| DSTD                | Standard deviation of diffusivity                                  | Ball-and-stick(s)                                                                  | microns<sup>2</sup>/ms              |
| RTPP                | Return to the plane probability                                    | MAPMRI                                                                             | Probability \[0-1\]                 |
| RTAP                | Return to axis probability                                         | MAPMRI                                                                             | Probability \[0-1\]                 |

<sup>1</sup> For example, for free water in body temperature, the diffusivity in units of microns<sup>2</sup>/ms should be approximately 3.0.

### Directionally-encoded colour (DEC) maps

These maps are saved as 4D NIfTI files with 3 volumes (x,y,z,{RGB}), where the
three values in each voxel correspond to red, green and blue components indicating
directionality of the underlying model (each of which must be a non-negative value),
and the norm of the vector encodes any scalar parameter from the diffusion model.
Images encoded in this way should include the field "`_desc-DEC`" in order to
distinguish them from vector-valued maps (see below).

A common example is DEC FA maps, where the fractional anisotropy from the diffusion
tensor model is coloured according to the direction of the principal eigenvector:

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>_model-DTI_desc-DEC_FA.nii[.gz]
```

### Vector-valued maps

These maps are saved as 4D NIfTI files (x,y,z, 3\*n), where each triplet of volumes
encodes both a direction in 3D space and some quantitiative value (these are
sometimes referred to as "fixels"). The number of volumes in the image must be
3 times the maximal number of fixels that can appear in any voxel in the image
(since 3 volumes are required to represent the data for each individual fixel).
For voxels that contain less than this number of fixels, the excess volumes
should contain either zero-filling, or NaN values. Exactly what is encoded by
the amplitude of each XYZ triplet depends on the underlying model properties
that were used to derive the map, with some examples being:

| `<map_label>` values | Description                                                 |
| -------------------- | ----------------------------------------------------------- |
| PDF                  | Diffusion propagator                                        |
| EVECS                | Eigenvectors of a model that has eigenvectors (such as DTI) |
| PEAKS                | Directions and amplitudes of ODF maxima on the sphere       |

## Describing tractography

Tractography normally generates one of two primary file types: tractograms or
NIfTi files containing maps. Tractograms are files containing a collection of
streamlines, which are objects describing the path of idealized brain fiber
fascicles (ensembles of neural fibers that travel together). Tractography
visitation maps contain 3D spatial histograms of the number / fraction of
streamlines intersecting each voxel, but do not contain the individual
streamlines trajectories themselves. Two tractogram file formats are supported;
tractography visitation maps should be saved as NIfTIs.

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            <source_keywords>[_space-<space>][_desc-<label>][_subset-<label>]_tractography.[trk|tck|nii[.gz]]
```

### Filename keys

`desc` (optional) – A way to refer to a specific instance of the tractography
process. The combination of tractography methods and parameters that were used
to create this tractography result should be described in the associated JSON
file.

`subset` (optional) – A label descriptor for the the subset of streamlines
included in this file; if not specified, a whole brain tractography is assumed
(a tractogram). Example of subsets can be `short` if only short streamlines were
kept, or `subsampled50` if only 50% of the streamlines were kept.

### File formats

-   [.trk - Diffusion Toolkit (+TrackVis)](https://web.archive.org/web/20190103230122/http://www.trackvis.org/docs/?subsect=fileformat)
-   [.tck - MRtrix](https://web.archive.org/web/20190103230209/https://mrtrix.readthedocs.io/en/latest/getting_started/image_data.html#tracks-file-format-tck)

### JSON Metadata

We have two main classes of tractography algorithms: Global or Local
tractography, each with various supported algorithms.

| Class  | Algorithms | Reference                                                                                                                            |
| ------ | ---------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| LOCAL  | PROB       | Sherbondy, A.J., et al. (2008); Tournier J.D. et al. (2012); Behrens et al. (2007)                                                   |
| LOCAL  | DET        | Conturo, T. et al. (1999); Mori, S. et al. (1999)                                                                                    |
| LOCAL  | EUDX       | Garyfallidis et al. (2010); Mori, S. et al. (1999)                                                                                   |
| LOCAL  | FACT       | Jiang, H. et al. (2005)                                                                                                              |
| LOCAL  | STT        | Lazar, M. et al. (2003)                                                                                                              |
| LOCAL  | NULL       | Morris et al. (2008)                                                                                                                 |
| GLOBAL | UKF        | Malcolm J-G. et al. (2009)                                                                                                           |
| GLOBAL | SpinGlass  | Fillard P. et al. (2009)                                                                                                             |
| GLOBAL | ENS        | Takemura et al. (2016)                                                                                                               |
| GLOBAL | Other      | Mangin, J.F. et al. (2013); Aganj, I. et al. (2011); Neher, P.F. et al. (2012); Jbabdi, S., et al. (2007); Reisert, M. et al. (2011) |

The JSON sidecar contains the following key/value pairs:

| **Key name**       | **Description**                                                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------------------- |
| TractographyClass  | REQUIRED. Allowed values: `local`, `global`                                                                          |
| TractographyMethod | REQUIRED. Allowed values: `probabilistic`,`deterministic`,`eudx`,`fact`,`stt`,`null`,`ukf`,`spinglass`,`ens`,`other` |
| Count              | REQUIRED. integer                                                                                                    |
| Description        | OPTIONAL. string                                                                                                     |
| Constraints        | OPTIONAL. A dictionary containing various ways in which the tractography outcome is constrained (see below).         |
| Parameters         | OPTIONAL. A dictionary of model parameters (see below).                                                              |
| Seeding            | OPTIONAL. A dictionary describing how streamlines were initialised (see below).                                      |

RECOMMENDED to appear within the "`Constraints`" field when "`TractographyClass`" is "`local`":

| **Key name**      | **Description**                                                                             |
| ----------------- | ------------------------------------------------------------------------------------------- |
| AnatomicalType    | {`ACT`,`CMC`}                                                                               |
| AnatomicalImage   | string (name of anatomical tissue segmentation image)                                       |
| Include           | list of names of inclusion ROIs (streamlines must intersect all)                            |
| OrderedInclude    | list of names of ordered inclusion ROIs (streamlines must intersect all in order specified) |
| Exclude           | list of names of exclusion ROIs (streamlines must not intersect any)                        |
| Mask              | list of names of mask ROIs (streamlines must exist within)                                  |

RECOMMENDED to appear within the "`Parameters`" field when "`TractographyClass`" is "`local`":

| **Key name**      | **Description**                                      |
| ----------------- | ---------------------------------------------------- |
| Units             | {`mm`,`norm`} (applies to all within "`Parameters`") |
| StepSize          | value                                                |
| AngleCurvature    | value (maximum angle per step)                       |
| RadiusCurvature   | value (minimal radius of curvature)                  |
| MinimumLength     | value                                                |
| MaximumLength     | value                                                |
| IntegrationOrder  | integer                                              |
| Unidirectional    | bool                                                 |

RECOMMENDED to appear within the "Seeding" field when `TractographyClass` is `local`:

| **Key name** | **Description**                                                                                                          |
| ------------ | ------------------------------------------------------------------------------------------------------------------------ |
| SourceType   | {`sphere`,`voxels`,`surface`,`odf`}                                                                                      |
| Location     | values: If "`SourceType`" is "`sphere`", provide a 4-vector containin the XYZ location and radius in mm of the sphere    |
| Name         | string: If "`SourceType`" is not "`sphere`", give the filename from which seeds were derived                             |
| CountType    | {`global`,`local`} (i.e. does Count reflect a count per voxel / vertex, or a single count for the entire reconstruction) |
| Count        | integer                                                                                                                  |

Example:

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            sub-01_desc-DET_tractography.trk
            sub-01_desc-DET_tractography.json
```

```JSON
{
    "TractographyClass": "local",
    "TractographyMethod": "deterministic",
    "Parameters": {
        "StepSize": 0.5
    }
}
```

```Text
<pipeline_name>/
    sub-<participant_label>/
        dwi/
            sub-01_subset-shortfibers_tractography.trk
            sub-01_subset-shortfibers_tractography.json
```

```JSON
{
    "TractographyClass": "global",
    "TractographyMethod": "UKF",
    "Description": "UKF tracking where only short fibers were kept.",
    "Parameters": {
        "MaximumLength": 50.0
    }
}
```
