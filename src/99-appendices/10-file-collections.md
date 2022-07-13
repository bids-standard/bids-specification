# Appendix X: File collections

Here, some concrete use-cases of [entity-linked file collections](../02-common-principles.md#file-name-structure) are listed using descriptive tables, organized by modality.

The tables in this appendix catalog applications where the use of
a file collection is REQUIRED.

Certain entities interlink the files in a file collection through a metadata field.
Unlike other common entities (for example `run`), they require an iteration over different
values of the metadata fields they represent.
Please keep the following list of linking entities up-to-date with the file collections
included in this appendix:

-   Magnetic Resonance Imaging
    -   [`echo`](./09-entities.md#echo)
    -   [`flip`](./09-entities.md#flip)
    -   [`inv`](./09-entities.md#inv)
    -   [`mt`](./09-entities.md#mt)
    -   [`part`](./09-entities.md#part)

## Magnetic Resonance Imaging

### Anatomy imaging data

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
    datatypes=["anat"],
    suffixes=[
        "VFA",
        "IRT1",
        "MP2RAGE",
        "MESE",
        "MEGRE",
        "MTR",
        "MTS",
        "MPM",
    ])
}}

| **Suffix** | **Linking entities**  | **Application**                            | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                     |
|------------|-----------------------|--------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| VFA        | flip                  | Variable flip angle                        | The VFA method involves at least two spoiled gradient echo (SPGR) of steady-state free precession (SSFP) images acquired at different flip angles. Depending on the provided metadata fields and the sequence type, data may be eligible for DESPOT1, DESPOT2 and their variants ([Deoni et al. 2005](https://doi.org/10.1002/mrm.20314)).                                                                                          |
| IRT1       | inv, part             | Inversion recovery T1 mapping              | The IRT1 method involves multiple inversion recovery spin-echo images acquired at different inversion times ([Barral et al. 2010](https://doi.org/10.1002/mrm.22497)).                                                                                                                                                                                                                                                              |
| MP2RAGE    | flip, inv, echo, part | Magnetization prepared two gradient echoes | The MP2RAGE method is a special protocol that collects several images at different flip angles and inversion times to create a parametric T1map by combining the magnitude and phase images ([Marques et al. 2010](https://doi.org/10.1016/j.neuroimage.2009.10.002)).                                                                                                                                                              |
| MESE       | echo                  | Multi-echo spin-echo                       | The MESE method involves multiple spin echo images acquired at different echo times and is primarily used for T2 mapping. Please note that this suffix is not intended for the logical grouping of images acquired using an Echo Planar Imaging (EPI) readout.                                                                                                                                                                      |
| MEGRE      | echo                  | Multi-echo gradient-echo                   | Anatomical gradient echo images acquired at different echo times. Please note that this suffix is not intended for the logical grouping of images acquired using an Echo Planar Imaging (EPI) readout.                                                                                                                                                                                                                              |
| MTR        | mt                    | Magnetization transfer ratio               | This method is to calculate a semi-quantitative magnetization transfer ratio map.                                                                                                                                                                                                                                                                                                                                                   |
| MTS        | flip, mt              | Magnetization transfer saturation          | This method is to calculate a semi-quantitative magnetization transfer saturation index map. The MTS method involves three sets of anatomical images that differ in terms of application of a magnetization transfer RF pulse (MTon or MToff) and flip angle ([Helms et al. 2008](https://doi.org/10.1002/mrm.21732)).                                                                                                              |
| MPM        | flip, mt, echo, part  | Multi-parametric mapping                   | The MPM approaches (a.k.a hMRI) involves the acquisition of highly-similar anatomical images that differ in terms of application of a magnetization transfer RF pulse (MTon or MToff), flip angle and (optionally) echo time and magnitue/phase parts ([Weiskopf et al. 2013](https://doi.org/10.3389/fnins.2013.00095)). See [here](https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ) for suggested MPM acquisition protocols. |

### Fieldmap data

<!--
This block generates a filename templates.
The inputs for this macro can be found in the folder
  src/schema/rules/datatypes
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
    datatypes=["fmap"],
    suffixes=[
        "TB1DAM",
        "TB1EPI",
        "TB1AFI",
        "TB1TFL",
        "TB1RFM",
        "TB1SRGE",
        "RB1COR",
    ])
}}

| **Suffix** | **Meta-data relevant entity**                                | **Application**                    | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|------------|--------------------------------------------------------------|------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TB1DAM     | flip                                                         | Double-angle B1+ mapping           | The double-angle B1<sup>+</sup> method ([Insko and Bolinger 1993](https://doi.org/10.1006/jmra.1993.1133)) is based on the calculation of the actual angles from signal ratios, collected by two acquisitions at different nominal excitation flip angles. Common sequence types for this application include spin echo and echo planar imaging.                                                                                                        |
| TB1EPI     | flip, echo                                                   | B1<sup>+</sup> mapping with 3D EPI | This B1<sup>+</sup> mapping method ([Jiru and Klose 2006](https://doi.org/10.1002/mrm.21083)) is based on two EPI readouts to acquire spin echo (SE) and stimulated echo (STE) images at multiple flip angles in one sequence, used in the calculation of deviations from the nominal flip angle.                                                                                                                                                       |
| TB1AFI     | Please see the [qMRI appendix](../99-appendices/11-qmri.md). | Actual Flip Angle Imaging (AFI)    | This method ([Yarnykh 2007](https://doi.org/10.1002/mrm.21120)) calculates a B1<sup>+</sup> map from two images acquired at interleaved (two) TRs with identical RF pulses using a steady-state sequence.                                                                                                                                                                                                                                               |
| TB1TFL     | Please see the [qMRI appendix](../99-appendices/11-qmri.md). | Siemens `tfl_b1_map`               | B1<sup>+</sup> data acquired using `tfl_b1_map` product sequence by Siemens based on the method by [Chung et al. (2010)](https://doi.org/10.1002/mrm.22423). The sequence generates one anatomical image and one scaled flip angle map.                                                                                                                                                                                                                 |
| TB1RFM     | Please see the [qMRI appendix](../99-appendices/11-qmri.md). | Siemens `rf_map`                   | B1<sup>+</sup> data acquired using `rf_map` product sequence by Siemens.                                                                                                                                                                                                                                                                                                                                                                                |
| TB1SRGE    | `flip`, `inv`                                                | SA2RAGE                            | Saturation-prepared with 2 rapid gradient echoes (SA2RAGE) uses a ratio of two saturation recovery images with different time delays, and a simulated look-up table to estimate B1+ ([Eggenschwiler et al. 2011](https://doi.org/10.1002/mrm.23145)). This sequence can also be used in conjunction with MP2RAGE T1 mapping to iteratively improve B1+ and T1 map estimation ([Marques & Gruetter 2013](https://doi.org/10.1371/journal.pone.0069294)). |
| RB1COR     | Please see the [qMRI appendix](../99-appendices/11-qmri.md). | B1<sup>-</sup> field correction    | Low resolution images acquired by the body coil (in the gantry of the scanner) and the head coil using identical acquisition parameters to generate a combined sensitivity map as described in [Papp et al. (2016)](https://doi.org/10.1002/mrm.26058).                                                                                                                                                                                                 |
