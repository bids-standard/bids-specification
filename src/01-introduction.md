# Introduction

## Motivation

Neuroimaging experiments result in complicated data that can be arranged in many
different ways. So far there is no consensus how to organize and share data
obtained in neuroimaging experiments. Even two researchers working in the same
lab can opt to arrange their data in a different way. Lack of consensus (or a
standard) leads to misunderstandings and time wasted on rearranging data or
rewriting scripts expecting certain structure. Here we describe a simple and
easy-to-adopt way of organising neuroimaging and behavioural data. By using this
standard you will benefit in the following ways:

-   It will be easy for another researcher to work on your data. To understand
    the organisation of the files and their format you will only need to refer
    them to this document. This is especially important if you are running your
    own lab and anticipate more than one person working on the same data over
    time. By using BIDS you will save time trying to understand and reuse data
    acquired by a graduate student or postdoc that has already left the lab.

-   There are a growing number of data analysis software packages that can
    understand data organised according to BIDS (see
    [http://bids.neuroimaging.io](http://bids.neuroimaging.io) for the most up
    to date list).

-   Databases such as OpenNeuro.org accept datasets organised according to BIDS.
    If you ever plan to share your data publicly (nowadays some journals require
    this) you can minimize the additional time and energy spent on publication,
    and speed up the curation process by using BIDS to structure and describe
    your data right after acquisition.

-   There are [validation tools](https://github.com/Squishymedia/BIDS-Validator)
    that can check your dataset integrity and let you easily spot missing
    values.

BIDS is heavily inspired by the format used internally by OpenfMRI.org and has
been supported by the International Neuroinformatics Coordinating Facility and
the Neuroimaging Data Sharing Task Force. While working on BIDS we consulted
many neuroscientists to make sure it covers most common experiments, but at the
same time is intuitive and easy to adopt. The specification is intentionally
based on simple file formats and folder structures to reflect current lab
practices and make it accessible to a wide range of scientists coming from
different backgrounds.

## Extensions

The BIDS specification can be extended in a backwards compatible way and will
evolve over time. A number of extensions are currently being worked on:

| Extension label                                                                           | Title                                                                                                                                                                                         | Moderators/leads                                               |
| :---------------------------------------------------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------- |
| [BEP001](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg) | [Structural acquisitions that include multiple contrasts (multi echo, flip angle, inversion time) sequences](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg) | Gilles de Hollander                                            |
| [BEP002](https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M) | [The BIDS Models Specification](https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M)                                                                              | Tal Yarkoni                                                    |
| [BEP003](https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4) | [Common Derivatives](https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4)                                                                                         | Chris Gorgolewski                                              |
| [BEP004](https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc) | [Susceptibility Weighted Imaging (SWI)](https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc)                                                                      | Fidel Alfaro Almagro                                           |
| [BEP005](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c) | [Arterial Spin Labeling (ASL)](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c)                                                                               | Henk-Jan Mutsaerts and Michael Chappell                        |
| [BEP006](https://docs.google.com/document/d/1ArMZ9Y_quTKXC-jNXZksnedK2VHHoKP3HCeO5HPcgLE) | [Electroencephalography (EEG)](https://docs.google.com/document/d/1ArMZ9Y_quTKXC-jNXZksnedK2VHHoKP3HCeO5HPcgLE)                                                                               | Cyril R Pernet, Robert Oostenveld, Stefan Appelhoff            |
| [BEP009](https://docs.google.com/document/d/1mqMLnxVdLwZjDd4ZiWFqjEAmOmfcModA_R535v3eQs0) | [Positron Emission Tomography (PET)](https://docs.google.com/document/d/1mqMLnxVdLwZjDd4ZiWFqjEAmOmfcModA_R535v3eQs0)                                                                         | Melanie Ganz                                                   |
| [BEP010](https://docs.google.com/document/d/1qMUkoaXzRMlJuOcfTYNr3fTsrl4SewWjffjMD5Ew6GY) | [intracranial Electroencephalography (iEEG)](https://docs.google.com/document/d/1qMUkoaXzRMlJuOcfTYNr3fTsrl4SewWjffjMD5Ew6GY)                                                                 | Dora Hermes and Chris Holdgraf                                 |
| [BEP011](https://docs.google.com/document/d/1YG2g4UkEio4t_STIBOqYOwneLEs1emHIXbGKynx7V0Y) | [The structural preprocessing derivatives](https://docs.google.com/document/d/1YG2g4UkEio4t_STIBOqYOwneLEs1emHIXbGKynx7V0Y)                                                                   | Andrew Hoopes                                                  |
| [BEP012](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU) | [The functional preprocessing derivatives](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU)                                                                   | Camille Maumet and Chris Markiewicz                            |
| [BEP013](https://docs.google.com/document/d/1qBNQimDx6CuvHjbDvuFyBIrf2WRFUOJ-u50canWjjaw) | [The resting state fMRI derivatives](https://docs.google.com/document/d/1qBNQimDx6CuvHjbDvuFyBIrf2WRFUOJ-u50canWjjaw)                                                                         | Steven Giavasis                                                |
| [BEP014](https://docs.google.com/document/d/11gCzXOPUbYyuQx8fErtMO9tnOKC3kTWiL9axWkkILNE) | [The affine transformations and nonlinear field warps](https://docs.google.com/document/d/11gCzXOPUbYyuQx8fErtMO9tnOKC3kTWiL9axWkkILNE)                                                       | Oscar Esteban                                                  |
| [BEP015](https://docs.google.com/document/d/1WYOTXDB7GzlHoWqLjd45I3uGBgPxXddST-NTqBnroJE) | [Mapping file](https://docs.google.com/document/d/1WYOTXDB7GzlHoWqLjd45I3uGBgPxXddST-NTqBnroJE)                                                                                               | Eric Earl, Camille Maumet, and Vasudev Raguram                 |
| [BEP016](https://docs.google.com/document/d/1cQYBvToU7tUEtWMLMwXUCB_T8gebCotE1OczUpMYW60) | [The diffusion weighted imaging derivatives](https://docs.google.com/document/d/1cQYBvToU7tUEtWMLMwXUCB_T8gebCotE1OczUpMYW60)                                                                 | Franco Pestilli and Oscar Esteban                              |
| [BEP017](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA) | [Generic BIDS connectivity data schema](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA)                                                                      | Eugene Duff and Paul McCarthy                                  |
| [BEP018](https://docs.google.com/document/d/1uRkgyzESLKuGjXi98Z97Wh6vt-iLN5nOAb9TG16CjUs) | [Genetic information](https://docs.google.com/document/d/1uRkgyzESLKuGjXi98Z97Wh6vt-iLN5nOAb9TG16CjUs)                                                                                        | Cyril R Pernet, Clara Moreau, and Thomas Nichols               |
| [BEP019](https://docs.google.com/document/d/1FqJI791ycXr0bfRg2qyLqAf0RpVttJ2cInOgMWrKsNU) | [DICOM Metadata](https://docs.google.com/document/d/1FqJI791ycXr0bfRg2qyLqAf0RpVttJ2cInOgMWrKsNU)                                                                                             | Satrajit Ghosh                                                 |
| [BEP020](https://docs.google.com/document/d/1eggzTCzSHG3AEKhtnEDbcdk-2avXN6I94X8aUPEBVsw) | [Eye Tracking including Gaze Position and Pupil Size(ET)](https://docs.google.com/document/d/1eggzTCzSHG3AEKhtnEDbcdk-2avXN6I94X8aUPEBVsw)                                                    | Benjamin Gagl and Dejan Draschkow                              |
| [BEP021](https://docs.google.com/document/d/1PmcVs7vg7Th-cGC-UrX8rAhKUHIzOI-uIOh69_mvdlw) | [Common Electrophysiological Derivatives](https://docs.google.com/document/d/1PmcVs7vg7Th-cGC-UrX8rAhKUHIzOI-uIOh69_mvdlw)                                                                    | Stefan Appelhoff, Cyril Pernet, Robert Oostenveld, Teon Brooks |

When an extension reaches maturity it is merged into the main body of the
specification. If you would like to contribute to BIDS please consult the
[BIDS Contributor Guide](https://docs.google.com/document/d/1pWmEEY-1-WuwBPNy5tDAxVJYQ9Een4hZJM06tQZg8X4/edit?usp%3Dsharing&sa=D&ust=1537468908724000)
All of the ideas that are not backwards compatible and thus will have to wait
for BIDS 2.0 are listed
[here](https://docs.google.com/document/d/1LEgsMiisGDe1Gv-hBp1EcLmoz7AlKj6VYULUgDD3Zdw)

## Citing BIDS

When referring to BIDS in context of academic literature please cite:

> Gorgolewski, K.J., Auer, T., Calhoun, V.D., Craddock, R.C., Das, S., Duff,
> E.P., Flandin, G., Ghosh, S.S., Glatard, T., Halchenko, Y.O., Handwerker,
> D.A., Hanke, M., Keator, D., Li, X., Michael, Z., Maumet, C., Nichols, B.N.,
> Nichols, T.E., Pellman, J., Poline, J.-B., Rokem, A., Schaefer, G., Sochat,
> V., Triplett, W., Turner, J.A., Varoquaux, G., Poldrack, R.A., 2016.
> [The brain imaging data structure, a format for organizing and describing outputs of neuroimaging experiments](https://www.nature.com/articles/sdata201644).
> Sci Data 3, 160044.

as well as other papers describing specific BIDS extensions (see below).

BIDS has also a
[Research Resource Identifier (RRID)](https://www.force11.org/group/resource-identification-initiative)
- `RRID:SCR_016124` - which you can also include in your manuscript in addition
to citing the paper.
