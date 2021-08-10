# Computational Models

## General principles

1.  **Short and intuitive filenames**: Computational models and corresponding simulation
results are typically characterised by a large number of different parameters.
Distinguishing files on the basis of all these parameters would lead to extremely long
filenames, which are not supported by operating systems and which are hard to parse
visually.
Therefore, instead of long lists of key-value pairs to disambiguate files, the defining
characteristic of each file (or file bundle) is given through the `desc` key-value pair
in free-form, while JSON and XML files are used to exhaustively specify parameters.
Every file that contains computational model simulation results MUST have an accompanying
JSON sidecar of the same name except the suffix.
In this JSON there MUST be links to the underlying model (`"ModelParam"`) and parameters
(`"ModelEq`) files.
Note that because simulation results are not necessarily dependent on a specific subject
or space the filename keys `subject` and `space` are OPTIONAL, while `desc` is REQUIRED.
1.  **Avoiding overspecialization and standard proliferation to increase
interoperability**: With standardization efforts there are risks of overspecialization
and standard proliferation: because they (apparently) do not accommodate every use case,
there is a tendency for competing standards or substandards to arise and after a while
the market for competing standards or substandards gets messy and hard to use such that
the problem (interoperability) that the standardization tried to solve comes back in a
different form (instead of no standard there is then a flood of standards or very complex
standards).
For example: when the key-value pairs of file names are tuned to a narrow
class of software or concepts then they often cannot be practically used outside of that
specific framework.
Problematically, neural simulators often have a dedicated file format
although the underlying information to describe neural models is often very similar or
even identical.
This is in contrast to the idea of BIDS of providing a generically interoperable
specification that is independent of a specific product, concept or framework.
Therefore, instead of interpreting computational model simulation results from the
conceptual vantage point of a specific product or framework and to converge towards a
common ground we introduce only highly **generic datatypes** to store computational models
and simulation results:
    - network graphs (`net/`)
    - mathematical equations with physical interpretation (`eq/`)
    - parameters used to produce a particular result (`param/`)
    - computer code (`code/`)
    - time series data (temporal objects) (`ts/`)
    - spatial objects data (`spatial/`)
    - coordinates (`coord/`) to align `ts/`, `spatial/` and `net/` in common reference
spaces

These data types can all be expressed with

-   tsv files
-   JSON sidecar files and
-   XML files for model equations and parameters using the
[**L**ow **E**ntropy **M**odel **S**pecification (LEMS)](http://lems.github.io/LEMS)
format.

In the following `n` refers to the number of nodes of a network graph, `t` to the number
of time points of a time series and `m` to the count of arbitrary entities like vertices,
faces, and so on.

## Generic metadata

These metadata keys MUST be used in all computational model JSON sidecar files.

{{ MACROS___make_metadata_table(
{
"NumberOfRows": "REQUIRED",
"NumberOfColumns": "REQUIRED",
"CoordsRows": "REQUIRED",
"CoordsColumns": "REQUIRED",
"Description": "REQUIRED",
}
) }}

## Network graphs (`net/`)

The folder `net/` stores the graph structure of computational network models.
Graphs are stored as adjacency matrices in `.tsv` files.
Rows and columns are sorted according to `coord/` files that are linked in the JSON
sidecar files using the keys `"NumberOfRows"`, `"NumberOfColumns"`, `"CoordsRows"`,
`"CoordsColumns"`.
The minimally required information for neural network modelling is the coupling `weights`
matrix.
Note that information in `distances`, `delays` and `speeds` matrices can be
redundant so it is best practice to supply only one of them to avoid potential
ambiguity problems.

{{ MACROS___make_filename_template(datatypes=["net"]) }}

Currently supported types of network graph files:

| **Name**           | `suffix`    | **Description**                       |
| ------------------ | ----------- | ------------------------------------- |
| coupling weights   | `weights`   | `nxn` matrix of connection weights.   |
| coupling distances | `distances` | `nxn` matrix of connection distances. |
| coupling delays    | `delays`    | `nxn` matrix of connection delays.    |
| coupling speeds    | `speeds`    | `nxn` matrix of connection speeds.    |
| node identifiers   | `labels`    | `nx1` vector of node names (strings). |

## Coordinates (`coord/`)

The files in the folder `coord/` define the spatial, respectively, the temporal
coordinates of the rows and columns in  `ts/`, `spatial/` and `net/` files.

{{ MACROS___make_filename_template(datatypes=["coord"]) }}

The sorting of coordinates refers to the sorting of, for example,

-   time points in time series, sampled at regular or irregular intervals (`ts/`)
-   locations of spatial objects (`spatial/`)
-   labels of network nodes (`net/`)

Units (for example: `"s"`, `"m"`, `"ms"`, `"degrees"`, `"radians"`, ...) are specified in
`coord/` sidecar files using the key `"Units"`. **The sorting of rows, respectively
columns, in a data file corresponds to the rows in the `coords/` files linked with the
keys `"CoordsColumns"`, respectively `"CoordsRows"`.**

Examples:

1.  The time steps in the first line (row 1) of a `ts/` file `<ts_example>_ts.tsv` happen
at the time specified in the first line (row 1) of a `coord/` file
`<ts_example>_times.tsv` that is linked from the field `"CoordsRows"` in the JSON sidecar
file `<coord_example>_ts.json`.
Furthermore, the labels of the nodes along columns in `<ts_example>_ts.tsv` may be
specified in an `<coord_example>_labels.tsv` file that is linked from the field
`"CoordsColumns"`.
1.  The location, respectively the label, of the node corresponding to column 247 in the
file `net/<example2>_weights.tsv` is specified in row 247 of the linked
`../coord/*_nodes.json`, respectively `../coord/*_labels.json`, that are linked via the
key `"CoordsColumns"`.

Example:
```json
    "CoordsColumns": [
                		"../coord/excoordsys_nodes.json",
                		"../coord/excoordsys_labels.json"
                	 ]
```
Currently supported types of coordinates:

| **Name**                             | `suffix`       | **Description**                                                                                                                                                                                |
| ------------------------------------ | -------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Time points of a time series         | `times`        | `nx1` vector of time points (default unit: s, seconds).  Both, sampling at regular and at irregular intervals is supported.                                                                    |
| Locations of network node centres    | `nodes`        | `nx3` matrix of cartesian coordinates.                                                                                                                                                         |
| Locations of surface vertices        | `vertices`     | `nx3` matrix of cartesian coordinates.                                                                                                                                                         |
| Indices of face vertices             | `faces`        | `nxm` matrix of vertex indices, referring to row indices (one-based numbering) in a corresponding `_vertices` file to form faces (triangles, rectangles, ...).                                 |
| Normal vectors of vertices           | `vnormals`     | `nx3` matrix of normal vectors, referring to row indices (one-based numbering) in a corresponding `_vertices` file.                                                                            |
| Normal vectors of faces              | `fnormals`     | `nx3` matrix of normal vectors, referring to row indices (one-based numbering) in a corresponding `_faces` file.                                                                               |
| Textual identifier labels            | `labels`       | `nxk` vector of strings to label the rows or columns of associated files.                                                                                                                      |
| Locations of sensors                 | `sensors`      | `nx3` matrix of cartesian coordinates.                                                                                                                                                         |
| Orientations of surfaces or vertices | `orientations` | `nx3` matrix of unit vectors.                                                                                                                                                                  |
| Mappings between coordinates         | `map`          | `nxm` matrix where the coordinates along rows are mapped to the coordinates along columns. The types of coordinates are specified in sidecar JSON fields `"CoordsRows"` and `"CoordsColumns"`. |
| Projection matrix                    | `conv`         | like a `map`, but applied as convolution matrix (that is, multiplied with a `ts` or `spatial` object).                                                                                         |
| spatial extends of 2d objects        | `areas`        | `nx1` matrix of areas (default unit: m<sup>2</sup>, square metre).                                                                                                                             |
| spaces enclosed by 3d objects        | `volumes`      | `nx1` matrix of volumes (default unit: m<sup>3</sup>, cubic metre).                                                                                                                            |
| Generic 2d cartesian coordinates     | `cartesian2d`  | `nx2` matrix of general purpose cartesian coordinates.                                                                                                                                         |
| Generic 3d cartesian coordinates     | `cartesian3d`  | `nx3` matrix of general purpose cartesian coordinates.                                                                                                                                         |
| Generic 2d polar coordinates         | `polar2d`      | `nx2` matrix of general purpose polar coordinates.                                                                                                                                             |
| Generic 3d polar coordinates         | `polar3d`      | `nx3` matrix of general purpose polar coordinates.                                                                                                                                             |

### `"coord""`-specific metadata

{{ MACROS___make_metadata_table(
{
"Units": "REQUIRED",
"AnatomicalLandmarkCoordinates": "RECOMMENDED",
"AnatomicalLandmarkCoordinateSystem": "RECOMMENDED",
"AnatomicalLandmarkCoordinateUnits": "RECOMMENDED",
"AnatomicalLandmarkCoordinateSystemDescription": "RECOMMENDED"
}
) }}

## Time series data (`ts/`)

The folder `ts/` stores time series.
For example, if a parameter space exploration was performed all resulting time series are
stored in this folder and their corresponding JSON sidecar files specify which `eq`,
`params`, `net` and `coord` files were used to produce the result.
The temporal dimension is always stored along rows and the temporally varying entities
along columns.
The corresponding time points are defined in a `coord/` file that is linked in a sidecar
JSON with the exact same name as the time series file except for the file type suffix.
Every `ts/*_desc-<label>*_<suffix>.tsv` time series file MUST have an accompanying
sidecar JSON `ts/*_desc-<label>*_<suffix>.json` that links to the LEMS XML files that
contain the underlying model equations (`eq/`) and parameters (`params/`) using the keys
`"ModelEq"` and `"ModelParam"`.

Both, `ts/` and `spatial/` files can be grouped into file bundles using the filename key
entity `series`. For example, a series of `ts` files can be used to store a longer,
discontinuous time series in smaller files:
```sh
    ts/desc_Stimulustest4_series_00001_stimuli.tsv,
    ts/desc_Stimulustest4_series_00002_stimuli.tsv,
    ts/desc_Stimulustest4_series_00003_stimuli.tsv,
    ...
    ts/desc_Stimulustest4_series_09876_stimuli.tsv
```
The coordinates of the series elements MUST be specified with the metadata key
`"CoordsSeries"`.

Note that the filetype `"spikes"` is the only data file filetype that allows jagged 2d
arrays: columns can have different lengths for efficient (sparse) storage of spike times.
Each row contains only the indices of the units that spiked at the times defined in the
linked `"CoordsRows"` file.
In contrast, the arrays in the filetype `"raster"` have a fixed dimensionality (that is,
no sparse storage).
A value of `0` in the array element `a<sub>ij</sub>` indicates no spike of unit `j` at
time index `i`, while a value of `1` indicates a spike by that unit at the indexed time
(the time can be obtained from the linked `coords/` file).

{{ MACROS___make_filename_template(datatypes=["ts"]) }}

Currently supported types of time series:

| **Name**                      | `suffix`  | **Description**                                                                                                                                                                                                                                            |
| ----------------------------- | --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Model simulation time series  | `vars`    | `txn` matrix of (state) variable time series. The labels in the `coord/*_labels.tsv` file linked in the sidecar `"CoordsColumns"` field MUST be identical to the name of the `StateVariable` / `DerivedVariable` in the corresponding LEMS XML model file. |
| Stimulation time series       | `stimuli` | `txn` matrix of stimulation time series.                                                                                                                                                                                                                   |
| Noise time series             | `noise`   | `txn` matrix of noise time series.                                                                                                                                                                                                                         |
| Spike timings                 | `spikes`  | `sparse` format for storing spikes. Variable number of columns in each row allowed.                                                                                                                                                                        |
| Spike raster                  | `raster`  | `txn` spike raster.                                                                                                                                                                                                                                        |
| Empirical timeseries          | `emp`     | `txn` matrix of empirical time series.                                                                                                                                                                                                                     |
| Generic time series container | `ts`      | `txn` matrix of generic time series.                                                                                                                                                                                                                       |
| Events, labels, annotations   | `events`  | `txn` matrix of strings to annotate time series.                                                                                                                                                                                                           |

### `"ts"`-specific metadata

While it is possible to use `coords/*_times.tsv` files to specify the time points of a
time series, it is often more convenient to just specify the
`"SamplingPeriod"` or the `"SamplingFrequency"` (works only for equidistant sampling).

{{ MACROS___make_metadata_table(
{
"ModelEq": "REQUIRED",
"ModelParam": "REQUIRED",
"SourceCode": "REQUIRED",
"SourceCodeVersion": "REQUIRED",
"SoftwareVersion": "REQUIRED",
"SoftwareName": "REQUIRED",
"SoftwareRepository": "REQUIRED",
"Network": "REQUIRED",
"SamplingPeriod": "RECOMMENDED",
"SamplingFrequency": "RECOMMENDED",
}
) }}

## Spatial data (`spatial/`)

The folder `spatial/` stores all kinds of spatial entities like

-   functional connectivity matrices and more generic
-   maps of values projected onto surfaces or network graphs.

The coordinates corresponding to rows and columns are defined in a `coord/` file,
linked in a sidecar JSON.
Every `spatial/*_desc-<label>*_<suffix>.tsv` data file MUST have an accompanying sidecar
JSON `spatial/*_desc-<label>*_<suffix>.json` that links to the LEMS XML files that
contain the underlying model equations (`eq/`) and parameters (`params/`) using the keys
`"ModelEq"` and `"ModelParam"`.

Both, `ts/` and `spatial/` files can be grouped into file bundles using the filename key
entity `series`. For example, a series of FC matrices can be used to store functional
connectivity dynamics matrices over time:
```sh
    spatial/desc_FCDtest1_series_00001_fc.tsv,
    spatial/desc_FCDtest1_series_00002_fc.tsv,
    spatial/desc_FCDtest1_series_00003_fc.tsv,
    ...
    spatial/desc_FCDtest1_series_00300_fc.tsv
```
The coordinates of the series elements MUST be specified with the metadata key
`"CoordsSeries"`.

{{ MACROS___make_filename_template(datatypes=["spatial"]) }}

Currently supported types of spatial objects:

| **Name**                                                  | `suffix` | **Description**                                                                      |
| --------------------------------------------------------- | -------- | ------------------------------------------------------------------------------------ |
| Values projected onto surfaces, volumes or network graphs | `map`    | `nxm` matrix of values. Rows/cols correspond to spatial objects defined by `/coords` |
| Functional connectivity matrix                            | `fc`     | `nxn` matrix                                                                         |

### `"spatial"`-specific metadata

{{ MACROS___make_metadata_table(
{
"ModelEq": "REQUIRED",
"ModelParam": "REQUIRED",
"SourceCode": "REQUIRED",
"SourceCodeVersion": "REQUIRED",
"SoftwareVersion": "REQUIRED",
"SoftwareName": "REQUIRED",
"SoftwareRepository": "REQUIRED",
"Network": "REQUIRED",
"CoordsSeries": "RECOMMENDED",
}
) }}

## Model equations (`eq/`)

Equation and parameter files have a special role among the used file formats, because
they belong to the only file type that uses XML syntax and a format that is defined
outside of BIDS.
Model equations and parameterizations MUST be specified using the
[LEMS](http://lems.github.io/LEMS) language.
LEMS provides a compact, minimally redundant, human-readable, human-writable, declarative
way of expressing models of physical systems.
[PyLEMS](https://github.com/LEMS/pylems) is a Python implementation of the LEMS language
that can both parse and simulate existing LEMS models and provides an API in Python for
reading, modifying and writing LEMS files.
See the
[original publication introducing LEMS](https://pubmed.ncbi.nlm.nih.gov/25309419/),
and its [repository](http://lems.github.io/LEMS) with examples for more information.

A basic principle of LEMS is to separate equations and parameters such that the equations
need only be stated once and can then be reused with different parameterizations.
Therefore, every `ts/` and `spatial/` object MUST reference the LEMS model XML(s) using
the keyword `"ModelEq"` and, furthermore, the LEMS XML that contains the parameters
that were used to produce the simulation result using the keyword `"ModelParam"`.

{{ MACROS___make_filename_template(datatypes=["eq"]) }}

### `"eq"`-specific metadata

{{ MACROS___make_metadata_table(
{
"SourceCode": "RECOMMENDED",
"SourceCodeVersion": "RECOMMENDED",
"SoftwareVersion": "RECOMMENDED",
"SoftwareName": "RECOMMENDED",
"SoftwareRepository": "RECOMMENDED",
}
) }}

## Model parameters (`param/`)

Every `ts/` and `spatial/` object MUST reference the LEMS model XML(s) using
the keyword `"ModelEq"` and, furthermore, the LEMS XML that contains the parameters
that were used to produce the simulation result using the keyword `"ModelParam"`.

{{ MACROS___make_filename_template(datatypes=["param"]) }}

### `"param"`-specific metadata

{{ MACROS___make_metadata_table(
{
"ModelEq": "REQUIRED",
"SourceCode": "RECOMMENDED",
"SourceCodeVersion": "RECOMMENDED",
"SoftwareVersion": "RECOMMENDED",
"SoftwareName": "RECOMMENDED",
"SoftwareRepository": "RECOMMENDED",
}
) }}

## Computer code (`code/`)

Computer code involves "source code" (human-readable standard programming language) and
"machine code" (executable program).
Every BIDS dataset that contains simulation results **MUST** either directly store the
**source code** that was used to produce the result in this folder or link to a long-term
repository where it is stored using the field `"SourceCode"`.
Code can be in an arbitrary language, but MUST be versioned.
Furthermore, the
**machine code**, that is, the executable deployment of that source code used to produce
the result **MUST** be linked using the fields `"SoftwareName"`, `"SoftwareVersion"` and
`"SoftwareRepository"`.
Like in the case of source code, machine code can be either provided in this folder or in
a publicly-accessible repository.
It is preferred that deployments of the code exist in the form of
platform-independent self-contained container images (including the entire necessary
computational environment).

{{ MACROS___make_filename_template(datatypes=["code"]) }}

### `"code"`-specific metadata

{{ MACROS___make_metadata_table(
{
"SourceCode": "RECOMMENDED",
"SourceCodeVersion": "RECOMMENDED",
"SoftwareVersion": "RECOMMENDED",
"SoftwareName": "RECOMMENDED",
"SoftwareRepository": "RECOMMENDED",
"ModelEq": "RECOMMENDED",
}
) }}
