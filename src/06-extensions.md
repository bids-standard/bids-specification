# Contributing to and extending the BIDS specification

This page lists some ways that you can get involved with the BIDS community.

## Contributing to BIDS

There are many ways to get involved with the BIDS community!

### The BIDS Starter Kit
If you're new to the BIDS community and you'd like to learn a bit more, we
recommend checking out the [BIDS Starter Kit](https://github.com/bids-standard/bids-starter-kit/blob/master/README.md).
This has introductory information about the BIDS specification, tools in the
BIDS ecosystem, and how you can get involved.

### The BIDS Contributor guide

If you'd like to get involved more heavily in helping extend the BIDS
specification or develop tools for it, see the [BIDS Contributor Guide](https://docs.google.com/document/d/1pWmEEY-1-WuwBPNy5tDAxVJYQ9Een4hZJM06tQZg8X4).
It contains more in-depth information for getting involved with the BIDS
community.

## BIDS Extension Proposals

The BIDS specification can be extended in a backwards compatible way and will
evolve over time. These are accomplished with BIDS Extension Proposals (BEPs),
which are community-driven processes.

Below is a table of currently-active BEPs. The "Extension label" column
provides a direct link to the documentation.

| Extension label                                                                           | Title                                                                                                      | Moderators/leads                                                           |
| :---------------------------------------------------------------------------------------- | :--------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------- |
| [BEP001](https://docs.google.com/document/d/1QwfHyBzOyFWOLO4u_kkojLpUhW0-4_M7Ubafu9Gf4Gg) | Structural acquisitions that include multiple contrasts (multi echo, flip angle, inversion time) sequences | Gilles de Hollander                                                        |
| [BEP002](https://docs.google.com/document/d/1bq5eNDHTb6Nkx3WUiOBgKvLNnaa5OMcGtD0AZ9yms2M) | The BIDS Models Specification                                                                              | Tal Yarkoni                                                                |
| [BEP003](https://docs.google.com/document/d/1Wwc4A6Mow4ZPPszDIWfCUCRNstn7d_zzaWPcfcHmgI4) | Common Derivatives                                                                                         | Chris Gorgolewski                                                          |
| [BEP004](https://docs.google.com/document/d/1kyw9mGgacNqeMbp4xZet3RnDhcMmf4_BmRgKaOkO2Sc) | Susceptibility Weighted Imaging (SWI)                                                                      | Fidel Alfaro Almagro                                                       |
| [BEP005](https://docs.google.com/document/d/15tnn5F10KpgHypaQJNNGiNKsni9035GtDqJzWqkkP6c) | Arterial Spin Labeling (ASL)                                                                               | Henk-Jan Mutsaerts and Michael Chappell                                    |
| [BEP009](https://docs.google.com/document/d/1mqMLnxVdLwZjDd4ZiWFqjEAmOmfcModA_R535v3eQs0) | Positron Emission Tomography (PET)                                                                         | Melanie Ganz                                                               |
| [BEP011](https://docs.google.com/document/d/1YG2g4UkEio4t_STIBOqYOwneLEs1emHIXbGKynx7V0Y) | The structural preprocessing derivatives                                                                   | Andrew Hoopes                                                              |
| [BEP012](https://docs.google.com/document/d/16CvBwVMAs0IMhdoKmlmcm3W8254dQmNARo-7HhE-lJU) | The functional preprocessing derivatives                                                                   | Camille Maumet and Chris Markiewicz                                        |
| [BEP013](https://docs.google.com/document/d/1qBNQimDx6CuvHjbDvuFyBIrf2WRFUOJ-u50canWjjaw) | The resting state fMRI derivatives                                                                         | Steven Giavasis                                                            |
| [BEP014](https://docs.google.com/document/d/11gCzXOPUbYyuQx8fErtMO9tnOKC3kTWiL9axWkkILNE) | The affine transformations and nonlinear field warps                                                       | Oscar Esteban                                                              |
| [BEP015](https://docs.google.com/document/d/1WYOTXDB7GzlHoWqLjd45I3uGBgPxXddST-NTqBnroJE) | Mapping file                                                                                               | Eric Earl, Camille Maumet, and Vasudev Raguram                             |
| [BEP016](https://docs.google.com/document/d/1cQYBvToU7tUEtWMLMwXUCB_T8gebCotE1OczUpMYW60) | The diffusion weighted imaging derivatives                                                                 | Franco Pestilli and Oscar Esteban                                          |
| [BEP017](https://docs.google.com/document/d/1ugBdUF6dhElXdj3u9vw0iWjE6f_Bibsro3ah7sRV0GA) | Generic BIDS connectivity data schema                                                                      | Eugene Duff and Paul McCarthy                                              |
| [BEP018](https://docs.google.com/document/d/1uRkgyzESLKuGjXi98Z97Wh6vt-iLN5nOAb9TG16CjUs) | Genetic information                                                                                        | Cyril R Pernet, Clara Moreau, and Thomas Nichols                           |
| [BEP019](https://docs.google.com/document/d/1FqJI791ycXr0bfRg2qyLqAf0RpVttJ2cInOgMWrKsNU) | DICOM Metadata                                                                                             | Satrajit Ghosh                                                             |
| [BEP020](https://docs.google.com/document/d/1eggzTCzSHG3AEKhtnEDbcdk-2avXN6I94X8aUPEBVsw) | Eye Tracking including Gaze Position and Pupil Size(ET)                                                    | Benjamin Gagl and Dejan Draschkow                                          |
| [BEP021](https://docs.google.com/document/d/1PmcVs7vg7Th-cGC-UrX8rAhKUHIzOI-uIOh69_mvdlw) | Common Electrophysiological Derivatives                                                                    | Mainak Jas, Stefan Appelhoff, Cyril Pernet, Robert Oostenveld, Teon Brooks |
| [BEP022](https://docs.google.com/document/d/1pWCb02YNv5W-UZZja24fZrdXLm4X7knXMiZI7E2z7mY) | Magnetic Resonance Spectroscopy (MRS)                                                                      | Dickson Wong                                                               |
| [BEP023](https://docs.google.com/document/d/1yzsd1J9GT-aA0DWhdlgNr5LCu6_gvbjLyfvYq2FuxlY) | PET Preprocessing derivatives                                                                              | Martin Noergaard, Graham Searle, Melanie Ganz                              |
| [BEP024](https://docs.google.com/document/d/1fqnJZ18x5LJC8jiJ8yvPHUGFzNBZ6gW2kywYrUKWtuo) | Computed Tomography scan (CT)                                                                              | Hugo Boniface                                                              |
| [BEP025](https://docs.google.com/document/d/1chZv7vAPE-ebPDxMktfI9i1OkLNR2FELIfpVYsaZPr4) | Medical Population Imaging Data structure (MIDS)                                                           | Jose Manuel Saborit Torres, Maria de la Iglesia Vayá                                                 |
| [BEP026](https://docs.google.com/document/d/14KC1d5-Lx-7ZSMtwS7pVAAvz-2WR_uoo5FvsNirzqJw) | Microelectrode Recordings (MER)                                                                            | Greydon Gilmore                                                            |

When an extension reaches maturity it is merged into the main body of the
specification.  Below is a table of BEPs that have been merged in the main body
of the specification.

| Extension label                                                                           | Title                                      | Moderators/leads                                  |
| :---------------------------------------------------------------------------------------- | :----------------------------------------- | :------------------------------------------------ |
| [BEP006](https://docs.google.com/document/d/1ArMZ9Y_quTKXC-jNXZksnedK2VHHoKP3HCeO5HPcgLE) | Electroencephalograpgy (EEG)               | Cyril Pernet, Stefan Appelhoff, Robert Oostenveld |
| [BEP008](https://docs.google.com/document/d/1FWex_kSPWVh_f4rKgd5rxJmxlboAPtQlmBc1gyZlRZM) | Magnetoencephalography (MEG)               | Guiomar Niso                                      |
| [BEP010](https://docs.google.com/document/d/1qMUkoaXzRMlJuOcfTYNr3fTsrl4SewWjffjMD5Ew6GY) | intracranial Electroencephalograpgy (iEEG) | Chris Holdgraf, Dora Hermes                       |

All of the extension ideas that are not backwards compatible and thus
will have to wait for BIDS 2.0 are listed
[here](https://docs.google.com/document/d/1LEgsMiisGDe1Gv-hBp1EcLmoz7AlKj6VYULUgDD3Zdw).
