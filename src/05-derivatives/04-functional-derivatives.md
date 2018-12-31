# Functional derivatives

## Functional derivatives maps

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func/
            <source_keywords>[_referencemap-<referencemap>][_desc-<label>]_<suffix>.nii[.gz]
            <source_keywords>[_referencemap-<referencemap>][_desc-<label>]_<suffix>.json
```

for example:

```Text
pipeline1/
    sub-001/
        func/
            sub-001_task-rest_run-1_space-MNI305_mean.nii.gz
            sub-001_task-rest_run-1_space-MNI305_mean.json
```

The following table lists allowed suffixes and their corresponding measures:

| `<suffix>`       | Measure                                                          |
| ---------------- | ---------------------------------------------------------------- |
| `mean`           | Mean across the temporal/4th dimension of the data               |
| `std`            | Standard deviation across the temporal/4th dimension of the data |
| `tsnr`           | Temporal SNR (i.e. mean / std)                                   |
| `sfs`            | Signal fluctuation sensitivity                                   |
| `alff`           | Amplitude low frequency fluctuations                             |
| `falff`          | Fractional amplitude of low frequency fluctuations               |
| `reho`           | Regional homogeneity (voxelwise only)                            |
| `dcb`, `dcw`     | Voxelwise degree centrality binary and weighted                  |
| `ecb`, `ecw`     | Voxelwise eigenvector centrality binary and weighted             |
| `lfcdb`, `lfcdw` | Local functional connectivity density                            |
| `vmhc`           | Voxel mirrored homotopic connectivity                            |

The following metadata JSON fields are valid for derivative maps:

| Key name       | Description                                                               | Required for suffix        |
| -------------- | ------------------------------------------------------------------------- | -------------------------- |
| BandpassFilter | String describing all relevant parameters of the applied bandpass filter. | `alff`, `falff`            |
| Neighborhood   | String describing neighborhood for regional measures.                     | `reho`                     |
| Threshold      | String describing threshold used for determining graph edges.             | `dcb`, `dcw`, `ecb`, `ecw` |
| Method         | String describing method used to calculate measure.                       | `dcb`, `dcw`, `ecb`, `ecw` |

## Time series and regressors

For the purposes of this section, a time series or regressor is a numeric series
of values corresponding to volumes in a BOLD series. Time series is specifically
used to indicate an aggregate time series within an ROI, while regressor is used
as a more general term indicating series that may be derived from other sources,
such as head motion estimates or physiological recordings.

Regressors will generally be stored as tables, with a row of column headers
indicating the name of the regressor. In the case where every voxel has a
regressor, then the data should be stored in a 4D NIfTI file.

Tabular regressor files MUST be accompanied by a data dictionary in JSON format,
consistent with the format described in
[Common princioples](../02-common-principles.md).

Volumetric regressor files MAY be accompanied by a data dictionary in JSON
format, with OPTIONAL `LongName`, `Description`, `Levels`, `Units`, and
`TermURL` fields.

### General time series and regressors

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func/
	        <source_keywords>[_desc-<label>]_regressors.tsv
	        <source_keywords>[_desc-<label>]_regressors.json
```

for example:

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_desc-confounds_regressors.tsv
        sub-001_task-rest_run-1_desc-confounds_regressors.json
```

Any time series or regressor with one value per BOLD volume may be stored in a
regressors file. If a column is specified in another sub-section, then any
additional required metadata MUST be stored in the JSON description of the
column.

#### Column names

Column names are unique alphanumeric values that are defined in a relevant JSON
sidecar file. For a series of related columns, it is RECOMMENDED to use
zero-based indexing as a suffix. For example, the first six aCompCor components
may be named `a_comp_cor_00` ... `a_comp_cor_05`. Custom column names must not
conflict with reserved names specified in this document.

Reserved names are specified in the remaining subsections.

#### Time series transformations

Any column may have the following suffixes appended to indicate transformations
applied to the original time series data:

| Transformation | Description                                                                 |
| -------------- | --------------------------------------------------------------------------- |
| `_shift_back`  | The time series has been lagged by one TR. `x_shift_back[i] = x[i-1]`       |
| `_dt`          | The discrete first derivative of the time series. `x_dt[i] = x[i+1] - x[i]` |
| `_sq`          | The square of the time series                                               |
| `_var_norm`    | The time series has been variance normalized                                |
| `_centered`    | The time series has had its mean subtracted                                 |

For example, `rot_z_shift_back_sq` means the square of the lagged version of the
Z rotation (see Motion-related regressors).

### ROI-based time series extraction

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func/
            <source_keywords>[_atlas-<atlas_label>][_desc-<label>]_timeseries.<tsv|nii.gz>
            <source_keywords>[_atlas-<atlas_label>][_desc-<label>]_timeseries.json
```

for example:

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_atlas-AAL_timeseries.tsv
        sub-001_task-rest_run-1_atlas-AAL_timeseries.json
        sub-001_task-rest_run-1_desc-anaticor_timeseries.nii.gz
        sub-001_task-rest_run-1_desc-anaticor_timeseries.json
```

Time series will generally be stored as tables, with a row of column headers
indicating the name of the time series. In the case where every voxel has a time
series (i.e., voxel-wise regressors, as in ANATICOR), then the time series
should be saved as a NIfTI file.

#### Column metadata special fields

Atlas (optional) - A label indicating an atlas that defines a region or set of
regions in the volume. An atlas may be three- or four-dimensional, which affects
the interpretation of the roi index.

ROI (optional) - For 3D atlases, the ROI label should be numeric, corresponding
to the value of the voxels in the ROI. For 4D atlases, the ROI label should be
numeric, corresponding to the volume index containing the ROI mask. The
following special labels correspond to common ROIs that may be defined by many
atlases or segmentation algorithms:

| ROI Value      | Description                                                                            |
| -------------- | -------------------------------------------------------------------------------------- |
| WhiteMatter    | Signal derived from white matter ROI.                                                  |
| CSF            | Signal derived from cerebro-spinal fluid ROI.                                          |
| Background     | Signal derived from background (out of brain) ROI.                                     |
| GreyMatter     | Signal derived from grey matter ROI.                                                   |
| Ventricles     | Signal derived from ventricles ROI.                                                    |
| CircleOfWillis | Signal derived from circle of Willis ROI.                                              |
| GlobalSignal   | Vector of mean values within the brain mask. Can be used for Global Signal Regression. |

#### Column names

Column names are unique alphanumeric values that are defined in a relevant JSON
sidecar file. A naming convention might be to concatenate the atlas, ROI index,
summarization method (defined below) and transformations (see Time series
transformations, above) using snake case. For example,
`harvard_oxford_cortical_4_PC` could indicate ROI 4 of the Harvard-Oxford
cortical atlas, summarized by taking the first principal component.

#### Summarization methods

To indicate the summarization method applied to construct a single time series
for an ROI, the following column suffixes are defined:

| Column suffix | Description of the transformation                                                                                                                       |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `_mean`       | The mean of voxel time series                                                                                                                           |
| `_median`     | The median of voxel time series                                                                                                                         |
| `_pc[_<x>]`   | The ith eigenvariate from principal component analysis, where `x` is 0 indexed. If `x` is not specified, the first component is implied (i.e., `pc_0`). |
| `_spat_reg`   | Spatial regression                                                                                                                                      |

Example:

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_timeseries.tsv
```

```Text
white_matter_mean global_signal_mean ventricles_mean
12                98                 11
11                34                 53
54                34                 34
```

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_timeseries.json
```

```JSON
{
    "white_matter_mean": {
        "ROI": "WhiteMatter"
    },
    "global_signal_mean": {
        "ROI": "GlobalSignal"
    },
    "ventricles_mean": {
        "ROI": "Ventricles"
    }
}
```

### Motion-related regressors

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
    func/
        <source_keywords>[_desc-<label>]_motion.tsv
        <source_keywords>[_desc-<label>]_motion.json
```

#### Column names

The six basic motion parameters derived from motion correction have the
following names and units:

| Column name                     | Units   | Description            |
| ------------------------------- | ------- | ---------------------- |
| `trans_x`, `trans_y`, `trans_z` | mm      | Translation parameters |
| `rot_x`, `rot_y`, `rot_z`       | radians | Rotation parameters    |

Transformations (see Transformations) of motion parameters may be included in
the same file. For example, rot_z_shift_back_sq means square of the lagged
version of Z rotation.

The following columns indicate summarized motion, as defined in the
corresponding references:

| Column name              | Units | Description                                                         |
| ------------------------ | ----- | ------------------------------------------------------------------- |
| `framewise_displacement` | mm    | Framewise displacement (Power, et al., 2012)                        |
| `rmsd`                   | mm    | Root mean square deviation (Jenkinson, 1999)                        |
| `rms`                    | mm    | Root mean square of translation parameters (Van Dijk, et al., 2012) |

### Temporal outlier masks

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func/
	        <source_keywords>[_desc-<label>]_outliers.tsv
            <source_keywords>[_desc-<label>]_outliers.json
```

Outlier masks are columns of zeros (0), with ones (1) indicating volumes that
have been identified as outliers by some method.

#### Column names

Column names for outliers correspond to the type of outlier or method for
identifying the outlier. Column names should take the form `method[XX]`, where
`XX` is an optional index.

For example, if a BOLD series included two initial dummy scans,
`non_steady_state` may be a column with a 1 for the first two volumes, or
`non_steady_state_00` and `non_steady_state_01` may be columns with a 1 in the
first and second position, respectively.

The following methods are defined as reserved words:

| Column name            | Description                                              |
| ---------------------- | -------------------------------------------------------- |
| `non_steady_state_<x>` | Initial non-steady-state volumes. One column per volume. |

### Other time series and regressors

Time series and regressors that are not otherwise specified should be placed in
a regressors.tsv file (see General time series and regressors).

#### Column names

The following regressors are defined as reserved words:

| Column name    | Description                                           |
| -------------- | ----------------------------------------------------- |
| `dvars`        | Change in variance (Brett, 2006, Power, et al., 2012) |
| `std_dvars`    | Standardized DVARS (Nichols, 2013)                    |
| `cosine_<X>`   | Discrete cosine basis vectors                         |
| `legendre_<X>` | Legendre polynomial basis vectors                     |

### Spatiotemporal decompositions

Template:

```Text
<pipeline_name>/
    sub-<participant_label>/
        func/
            <source_keywords>[_desc-<label>]_<mixing|components>.tsv
            <source_keywords>[_desc-<label>]_<mixing|components>.nii.gz
            <source_keywords>[_desc-<label>]_decomposition.json
```

for example:

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_desc-MELODIC_components.nii.gz
        sub-001_task-rest_run-1_desc-MELODIC_mixing.tsv
        sub-001_task-rest_run-1_desc-MELODIC_decomposition.json
```

```Text
sub-001/
    func/
        sub-001_task-rest_run-1_desc-tICA_mixing.nii.gz
        sub-001_task-rest_run-1_desc-tICA_components.tsv
        sub-001_task-rest_run-1_desc-tICA_decomposition.json
```

Spatiotemporal decompositions produce either spatial or temporal components,
along with conjugate mixing matrices that can be represented as time series and
spatial maps, respectively. The combination of suffix and extension indicates
which class of algorithm produced the outputs.

Mixing matrices may be omitted for algorithms that are temporal decompositions
with no spatial component, such as CompCor variants.

Spatiotemporal decomposition files MUST be accompanied by a data dictionary in
JSON format, consistent with Raw-BIDS section 4.2, which describes metadata for
each column name. In addition to column names, the following MANDATORY field is
added:

| Key name | Description                                           |
| -------- | ----------------------------------------------------- |
| Method   | REQUIRED. Algorithm name and (if applicable) version. |

#### Column names

Column names in spatiotemporal decompositions take the form of
`<decomposition>_<index>`, where `<decomposition>` is the name of the
decomposition algorithm, and `<index>` is a numeric identifier. Indices SHOULD
start at 0. If there is a natural ordering, indices should reflect that
ordering. For example, the aCompCor component which explains the most variance
should be named `a_comp_cor_00`.

The following reserved words indicate common algorithms:

| Column name              | Description                                                                                                                                                                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `[a|t|w|c]_comp_cor_<x>` | CompCor (Behzadi, et al., 2007) calculated with voxels chosen based on: `a`: anatomically derived ROIs (white matter and CSF), `t`: temporal variance, `w`: white matter voxels only, `c`: CSF voxels only |
| `melodic_<x>`            | Columns from the mixing matrix in FSL MELODIC                                                                                                                                                              |
