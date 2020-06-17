# Introduction

## Motivation

Neuroimaging experiments result in complicated data that can be arranged in many
different ways. So far there is no consensus how to organize and share data
obtained in neuroimaging experiments. Even two researchers working in the same
lab can opt to arrange their data in a different way. Lack of consensus (or a
standard) leads to misunderstandings and time wasted on rearranging data or
rewriting scripts expecting certain structure. Here we describe a simple and
easy-to-adopt way of organising neuroimaging and behavioral data. By using this
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

-   Validation tools such as the [BIDS Validator](https://github.com/bids-standard/bids-validator)
    can check your dataset integrity and help you easily spot missing values.

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
evolve over time. This is accomplished through community-driven BIDS Extension
Proposals (BEPs). For more information about the BEP process, see
[Extending the BIDS specification](07-extensions.md).

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
