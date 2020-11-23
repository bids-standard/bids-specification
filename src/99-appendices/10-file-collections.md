# Appendix X: File collections

To give context to the use of [entity-linked file collections](./02-common-principles.md#file-name-structure), applications concerned with this
common principle are listed by descriptive tables under their respective modalities.

Note that the tables in this appendix catolog applications where the use of 
a file collection is REQUIRED.

Certain entitites interlink the files in a file collection through a metadata field.
Unlike other common entities (e.g. `run`), they require an iteration over different
values of the metadata fields they represent.
Please keep the following list of linking entities up-to-date with the file collections
included in this appendix:

* Magnetic Resonance Imaging 
    * [`echo`](./99-appendices/09-entities.md#echo) 
    * `flip` (to be added)
    * `inv`  (to be added)
    * `mt`   (to be added) 
    * `part` (to be added)

## Magnetic Resonance Imaging 

### Anatomy imaging data 

| Suffix  | Linking entities | Application                                | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
|---------|---------------------------|--------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| VFA     | flip                      | Variable flip angle                        | The VFA method involves at least two spoiled gradient echo (SPGR) of steady-state free precession (SSFP) images acquired at different flip angles. Depending on the provided metadata fields and the sequence type, data may be eligible for DESPOT1, DESPOT2 and their variants ([Deoni et al. 2005](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.20314)).                             |
| IRT1    | inv, part                       | Inversion recovery T1 mapping              | The IRT1 method involves multiple inversion recovery spin-echo images acquired at different inversion times ([Barral et al. 2010](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.22497)).                                                                                                                                                                                                                                                               |
| MP2RAGE | flip, inv, echo, part                 | Magnetization prepared two gradient echoes | The MP2RAGE method is a special protocol that collects several images at different flip angles and inversion times to create a parametric T1map by combining the magnitude and phase images ([Marques et al. 2010](https://www.sciencedirect.com/science/article/pii/S1053811909010738?casa_token=u_CYBx4hi7IAAAAA:3w0cMTyU5jA1BdFs0s5oVcQeqF2tZho0iJ9d4N1kExfaX27v9-JnWacF6mbEp_lMKZ64CvoTl8k)                                                               |
| MESE    | echo                      | Multi-echo spin-echo                       | The MESE method involves multiple spin echo images acquired at different echo times and is primarily used for T2 mapping. Please note that this suffix is not intended for the logical grouping of images acquired using an Echo Planar Imaging (EPI) readout.                                                                                                                                                                                                |
| MEGRE   | echo                      | Multi-echo gradient-echo                   | Anatomical gradient echo images acquired at different echo times. Please note that this suffix is not intended for the logical grouping of images acquired using an Echo Planar Imaging (EPI) readout.                                                                                                                                                                                                                                                        |
| MTR     | mt                        | Magnetization transfer ratio               | This method is to calculate a semi-quantitative magnetization transfer ratio map.                                                                                                                                                                                                                                                                                                                                                                             |
| MTS     | flip, mt                  | Magnetization transfer saturation          | This method is to calculate a semi-quantitative magnetization transfer saturation index map. The MTS method involves three sets of anatomical images that differ in terms of application of a magnetization transfer RF pulse (MTon or MToff) and flip angle ([Helms et al. 2008](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.21732)).                                                                                                               |
| MPM     | flip, mt, echo, part                  | Multi-parametric mapping                   | The MPM approaches (a.k.a hMRI) involves the acquisition of highly-similar anatomical images that differ in terms of application of a magnetization transfer RF pulse (MTon or MToff), flip angle and (optionally) echo time and magnitue/phase parts ([Weiskopf et al. 2013](https://www.frontiersin.org/articles/10.3389/fnins.2013.00095/full)). See [here](https://owncloud.gwdg.de/index.php/s/iv2TOQwGy4FGDDZ) for suggested MPM acquisition protocols. |

### Fieldmap data

| Suffix | Meta-data relevant entity     | Application                        | Description                                                                                                                                                                                                                                                                                                                                                                       |
|--------|-------------------------------|------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| TB1DAM | flip                          | Double-angle B1+ mapping           | The double-angle B1<sup>+</sup> method ([Insko and Bolinger 1993](https://www.sciencedirect.com/science/article/abs/pii/S1064185883711332)) is based on the calculation of the actual angles from signal ratios, collected by two acquisitions at different nominal excitation flip angles. Common sequence types for this application include spin echo and echo planar imaging. |
| TB1EPI | flip, echo                    | B1<sup>+</sup> mapping with 3D EPI | This B1<sup>+</sup> mapping method ([Jiru and Klose 2006](https://dx.doi.org/10.1002/mrm.21083)) is based on two EPI readouts to acquire spin echo (SE) and stimulated echo (STE) images at multiple flip angles in one sequence, used in the calculation of deviations from the nominal flip angle.                                                                              |
| TB1AFI | flip, inv                     | Actual Flip Angle Imaging (AFI)    | This method ([Yarnykh 2007](https://dx.doi.org/10.1002/mrm.21120)) calculates a B1<sup>+</sup> map from two images acquired at interleaved (two) TRs with identical RF pulses using a steady-state sequence                                                                                                                                                                       |
| TB1TFL | Please see the qMRI appendix* | Siemens `tfl_b1_map`               | B1<sup>+</sup> data acquired using `tfl_b1_map` product sequence by Siemens based on the method by [Chung et al. (2010)](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.22423). The sequence generates one ~anatomical image and one scaled flip angle map.                                                                                                                 |
| TB1RMF | Please see the qMRI appendix* | Siemens `rf_map`                   | B1<sup>+</sup> data acquired using `rf_map` product sequence by Siemens                                                                                                                                                                                                                                                                                                           |
| RB1COR | Please see the qMRI appendix* | B1<sup>-</sup> field correction    | Low resolution images acquired by the body coil (in the gantry of the scanner) and the head coil using identical acquisition parameters to generate a combined sensitivity map as described in [Papp et al. (2016)](https://onlinelibrary.wiley.com/doi/full/10.1002/mrm.26058)                                                                                                   |

\* These file collections call for the use of special notations that cannot
be resolved by entities that can generalize to other applications. Instead of
introducing an entity that is exclusive to a single application, method developers 
who commonly use these file collections for the `MPM` application reached the consensus 
on the use of `acq` entity to distinguish individual files. Please visit the qMRI 
appendix for further details.