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
