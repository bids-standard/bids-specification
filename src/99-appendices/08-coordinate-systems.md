# Appendix VIII: Coordinate systems

## Introduction

To interpret a coordinate (x, y, z), it is required that you know (1) relative
to which origin the coordinate is expressed, (2) the interpretation of the
three axes, and (3) the units in which the numbers are expressed.
This information is sometimes called the coordinate system.

These letters help describe the coordinate system definition:

-   A/P means anterior/posterior
-   L/R means left/right
-   S/I means superior/inferior

For example: `RAS` means that the first dimension (X) points towards the right
hand side of the head, the second dimension (Y) points towards the Anterior
aspect of the head, and the third dimension (Z) points towards the top of the
head.
The directions are considered to be from the subject's perspective.
For example, in the `RAS` coordinate system, a point to the subject's left
will have a negative `x` value.

Besides coordinate systems, defined by their origin and direction of the axes,
BIDS defines "spaces" as an artificial frame of reference, created to describe
different anatomies in a unifying manner (see for example,
[doi:10.1016/j.neuroimage.2012.01.024](https://doi.org/10.1016/j.neuroimage.2012.01.024)).

The "space" and all coordinates expressed in this space are by design a
transformation of the real world geometry, and nearly always different from the
individual subject space that it stems from. An example is the
Talairach-Tournoux space, which is constructed by piecewise linear scaling of an
individual's brain to that of the Talairach-Tournoux 1988 atlas. In the
Talairach-Tournoux space, the origin of the coordinate system is at the AC and
units are expressed in mm.

The coordinate systems below all relate to neuroscience and therefore to the
head or brain coordinates. Please be aware that all data acquisition starts with
"device coordinates" (scanner), which does not have to be identical to the
initial "file format coordinates" (DICOM), which are again different from the
"head" coordinates (for example, NIFTI). Not only do device coordinate vary between
hardware manufacturers, but also the head coordinates differ, mostly due to
different conventions used in specific software packages developed by different
(commercial or academic) groups.

## Coordinate Systems applicable to MEG, EEG, and iEEG

Generally, across the MEG, EEG, and iEEG modalities, the first two pieces of
information for a coordinate system (origin and orientation) are specified in
`<datatype>CoordinateSystem`.
The third piece of information for a coordinate system (units) are specified in
`<datatype>CoordinateUnits`.
Here, `<datatype>` can be one of `MEG`, `EEG`, or `iEEG`, depending on the
modality that is being used.

Allowed values for the `<datatype>CoordinateSystem` field come from a list of
restricted keywords, as listed in the sections below.
If no value from the list of restricted keywords fits, there is always the
option to specify the value as follows:

-   `Other`: Use this for other coordinate systems and specify further details
    in the `<datatype>CoordinateSystemDescription` field

**If you believe a specific coordinate system should be added to the list
of restricted keywords for MEG, EEG, or iEEG, please open a new issue on the
[bids-standard/bids-specification GitHub repository](https://github.com/bids-standard/bids-specification/issues/new/choose).**

## MEG Specific Coordinate Systems

Restricted keywords for the `<datatype>CoordinateSystem` field in the
`coordinatesystem.json` file for MEG datasets:

-   `CTF`: ALS orientation and the origin between the ears
-   `ElektaNeuromag`: RAS orientation and the origin between the ears
-   `4DBti`: ALS orientation and the origin between the ears
-   `KitYokogawa`: ALS orientation and the origin between the ears
-   `ChietiItab`: RAS orientation and the origin between the ears

Note that the short descriptions above do not capture all details, There are
detailed extensive descriptions of these EEG coordinate systems on the
[FieldTrip toolbox web page](https://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)

## EEG Specific Coordinate Systems

Restricted keywords for the `<datatype>CoordinateSystem` field in the
`coordsystem.json` file for EEG datasets:

-   `CapTrak`: RAS orientation and the origin between the ears

Note that the short descriptions above do not capture all details, There are
detailed extensive descriptions of these EEG coordinate systems on the
[FieldTrip toolbox web page](https://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined).

## iEEG Specific Coordinate Systems

Restricted keywords for the `<datatype>CoordinateSystem` field in the
`coordsystem.json` file for iEEG datasets:

-   `Pixels`: If electrodes are localized in 2D space (only x and y are
    specified and z is n/a), then the positions in this file must correspond to
    the locations expressed in pixels on the photo/drawing/rendering of the
    electrodes on the brain. In this case, coordinates must be (row,column)
    pairs, with (0,0) corresponding to the upper left pixel and (N,0)
    corresponding to the lower left pixel.

-   `ACPC`: The origin of the coordinate system is at the Anterior Commissure
    and the negative y-axis is passing through the Posterior Commissure. The
    positive z-axis is passing through a mid-hemispheric point in the superior
    direction. The anatomical landmarks are determined in the individual's
    anatomical scan and no scaling or deformations have been applied to the
    individual's anatomical scan. For more information, see the
    [ACPC site](https://www.fieldtriptoolbox.org/faq/acpc/) on the FieldTrip
    toolbox wiki.

## Image-based Coordinate Systems

The transformation of the real world geometry to an artificial frame of
reference is described in `<datatype>CoordinateSystem`.
Unless otherwise specified below, the origin is at the AC and the orientation of
the axes is RAS.
Unless specified explicitly in the sidecar file in the
`<datatype>CoordinateUnits` field, the units are assumed to be mm.

### Standard template identifiers

| Coordinate System                   | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| ----------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ICBM452AirSpace                     | Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" with "linear transforms of the subjects into the atlas space using a 12-parameter affine transformation" [https://www.loni.usc.edu/research/atlases](https://www.loni.usc.edu/research/atlases)                                                                                                                                                                                                                          |
| ICBM452Warp5Space                   | Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" "based on a 5th order polynomial transformation into the atlas space" [https://www.loni.usc.edu/research/atlases](https://www.loni.usc.edu/research/atlases)                                                                                                                                                                                                                                                             |
| IXI549Space                         | Reference space defined by the average of the "549 (...) subjects from the IXI dataset" linearly transformed to ICBM MNI 452.Used by SPM12. [https://brain-development.org/](https://brain-development.org/)                                                                                                                                                                                                                                                                                                           |
| fsaverage                           | The `fsaverage` is a **dual template** providing both volumetric and surface coordinates references. The volumetric template corresponds to a FreeSurfer variant of `MNI305` space. The `fsaverage` atlas also defines a surface reference system (formerly described as fsaverage\[3\|4\|5\|6\|sym\]).                                                                                                                                                                                                                |
| fsaverageSym                        | The `fsaverage` is a **dual template** providing both volumetric and surface coordinates references. The volumetric template corresponds to a FreeSurfer variant of `MNI305` space. The `fsaverageSym` atlas also defines a symmetric surface reference system (formerly described as `fsaveragesym`).                                                                                                                                                                                                                 |
| fsLR                                | The `fsLR` is a **dual template** providing both volumetric and surface coordinates references. The volumetric template corresponds to `MNI152NLin6Asym`. Surface templates are given at several sampling densities: 164k (used by HCP pipelines for 3T and 7T anatomical analysis), 59k (used by HCP pipelines for 7T MRI bold and DWI analysis), 32k (used by HCP pipelines for 3T MRI bold and DWI analysis), or 4k (used by HCP pipelines for MEG analysis) fsaverage_LR surface reconstructed from the T1w image. |
| MNIColin27                          | Average of 27 T1 scans of a single subject [https://www.bic.mni.mcgill.ca/ServicesAtlases/Colin27Highres](https://www.bic.mni.mcgill.ca/ServicesAtlases/Colin27Highres)                                                                                                                                                                                                                                                                                                                                                |
| MNI152Lin                           | Also known as ICBM (version with linear coregistration) [https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152Lin](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152Lin)                                                                                                                                                                                                                                                                                                                                           |
| MNI152NLin2009\[a-c\]\[Sym\|Asym\]  | Also known as ICBM (non-linear coregistration with 40 iterations, released in 2009). It comes in either three different flavours each in symmetric or asymmetric version. [https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009)                                                                                                                                                                                                               |
| MNI152NLin6Sym                      | Also known as symmetric ICBM 6th generation (non-linear coregistration). Used by SPM99 - SPM8. [https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin6](https://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin6)                                                                                                                                                                                                                                                                                                |
| MNI152NLin6ASym                     | A variation of `MNI152NLin6Sym` built by A. Janke that is released as the *MNI template* of FSL. Volumetric templates included with [HCP-Pipelines](https://github.com/Washington-University/HCPpipelines/tree/master/global/templates) correspond to this template too. See [doi:10.1016/j.neuroimage.2012.01.024](https://doi.org/10.1016/j.neuroimage.2012.01.024).                                                                                                                                                 |
| MNI305                              | Also known as avg305.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| NIHPD                               | Pediatric templates generated from the NIHPD sample. Available for different age groups (4.5–18.5 y.o., 4.5–8.5 y.o., 7–11 y.o., 7.5–13.5 y.o., 10–14 y.o., 13–18.5 y.o. This template also comes in either -symmetric or -asymmetric flavor. [https://www.bic.mni.mcgill.ca/ServicesAtlases/NIHPD-obj1](https://www.bic.mni.mcgill.ca/ServicesAtlases/NIHPD-obj1)                                                                                                                                                     |
| OASIS30AntsOASISAnts                | [https://figshare.com/articles/ANTs_ANTsR_Brain_Templates/915436](https://figshare.com/articles/ANTs_ANTsR_Brain_Templates/915436)                                                                                                                                                                                                                                                                                                                                                                                     |
| OASIS30Atropos                      | [https://mindboggle.info/data.html](https://mindboggle.info/data.html)                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| Talairach                           | Piecewise linear scaling of the brain is implemented as described in TT88. [http://talairach.org/](http://talairach.org/)                                                                                                                                                                                                                                                                                                                                                                                              |
| UNCInfant                           | Infant Brain Atlases from Neonates to 1- and 2-year-olds. [https://www.nitrc.org/projects/pediatricatlas](https://www.nitrc.org/projects/pediatricatlas)                                                                                                                                                                                                                                                                                                                                                               |

The following template identifiers are retained for backwards compatibility
of BIDS implementations.
However, their use is [DEPRECATED][deprecated].

| Coordinate System                   | Description                                                                                                                                              | RECOMMENDED alternative identifier |
| ----------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------- |
| fsaverage\[3\|4\|5\|6\|sym\]        | Images were sampled to the FreeSurfer surface reconstructed from the subject’s T1w image, and registered to an fsaverage template                        | fsaverage\[Sym\]                   |
| UNCInfant\[0\|1\|2\]V\[21\|22\|23\] | Infant Brain Atlases from Neonates to 1- and 2-year-olds. [https://www.nitrc.org/projects/pediatricatlas](https://www.nitrc.org/projects/pediatricatlas) | UNCInfant                          |

### Nonstandard coordinate system identifiers

The following template identifiers are RECOMMENDED for individual- and study-specific reference
spaces.
In order for these spaces to be interpretable, `SpatialReference` metadata MUST be provided, as
described in [Common file level metadata fields][common file level metadata fields].

In the case of multiple study templates, additional names may need to be defined.

| Coordinate System | Description                                                                                                                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| individual        | Participant specific anatomical space (for example derived from T1w and/or T2w images). This coordinate system requires specifying an additional, participant-specific file to be fully defined. In context of surfaces this space has been refered to as `fsnative`. |
| study             | Custom space defined using a group/study-specific template. This coordinate system requires specifying an additional file to be fully defined.                                                                                                                        |

### Non-template coordinate system identifiers

The `scanner` coordinate system is implicit and assumed by default if the derivative filename does not define **any** `space-<label>`.
Please note that `space-scanner` SHOULD NOT be used, it is mentioned in this specification to make its existence explicit.

| Coordinate System | Description                                                                                                                                                                                                                                                           |
| ----------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| scanner           | The intrinsic coordinate system of the original image (the first entry of `RawSources`) after reconstruction and conversion to NIfTI or equivalent for the case of surfaces and dual volume/surface files.                                                            |

<!-- Link Definitions -->

[common file level metadata fields]: ../05-derivatives/02-common-data-types.md#common-file-level-metadata-fields
[deprecated]: ../02-common-principles.md#definitions
