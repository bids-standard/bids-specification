# Introduction

## Motivation

Neuroimaging experiments result in complicated data that can be arranged in many
different ways. So far there is no consensus how to organize and share data
obtained in neuroimaging experiments. Even two researchers working in the same
lab can opt to arrange their data in a different way. Lack of consensus (or a
standard) leads to misunderstandings and time wasted on rearranging data or
rewriting scripts expecting certain structure. Here we describe a simple and
easy-to-adopt way of organizing neuroimaging and behavioral data. By using this
standard you will benefit in the following ways:

-   It will be easy for another researcher to work on your data. To understand
    the organization of the files and their format you will only need to refer
    them to this document. This is especially important if you are running your
    own lab and anticipate more than one person working on the same data over
    time. By using BIDS you will save time trying to understand and reuse data
    acquired by a graduate student or postdoc that has already left the lab.

-   There are a growing number of data analysis software packages that can
    understand data organized according to BIDS (see the
    [up to date list](https://bids.neuroimaging.io/benefits.html)).

-   Databases such as [OpenNeuro.org](https://openneuro.org/) accept datasets
    organized according to BIDS.
    If you ever plan to share your data publicly (nowadays some journals require
    this) you can minimize the additional time and energy spent on publication,
    and speed up the curation process by using BIDS to structure and describe
    your data right after acquisition.

-   Validation tools such as the [BIDS Validator](https://github.com/bids-standard/bids-validator)
    can check your dataset integrity and help you easily spot missing values.

BIDS was heavily inspired by the format used internally by the OpenfMRI repository
that is now known as [OpenNeuro.org](https://openneuro.org/),
and has been supported by the International Neuroinformatics Coordinating Facility
([INCF](https://www.incf.org/))
and the INCF Neuroimaging Data Sharing (NIDASH) Task Force.
While working on BIDS we consulted
many neuroscientists to make sure it covers most common experiments, but at the
same time is intuitive and easy to adopt. The specification is intentionally
based on simple file formats and directory structures to reflect current lab
practices and make it accessible to a wide range of scientists coming from
different backgrounds.

## Extensions

The BIDS specification can be extended in a backwards compatible way and will
evolve over time. This is accomplished through community-driven BIDS Extension
Proposals (BEPs). For more information about the BEP process, see
[Extending the BIDS specification](extensions.md).

## Citing BIDS

When referring to BIDS in context of academic literature, please cite one or
more of the publications listed below.
We RECOMMEND that you cite the original publication on BIDS and *additionally*
the publication regarding the datatype you were using
(for example, EEG, MEG, iEEG, if available).

For example:

> The data used in the study were organized using the
> Brain Imaging Data Structure (Gorgolewski, K., Auer, T., Calhoun, V. et al., 2016)
> with the extension for EEG data (Pernet, C.R., Appelhoff, S., Gorgolewski, K.J. et al., 2019).

### Original publication

-   Gorgolewski, K.J., Auer, T., Calhoun, V.D., Craddock, R.C., Das, S., Duff,
    E.P., Flandin, G., Ghosh, S.S., Glatard, T., Halchenko, Y.O., Handwerker,
    D.A., Hanke, M., Keator, D., Li, X., Michael, Z., Maumet, C., Nichols, B.N.,
    Nichols, T.E., Pellman, J., Poline, J.-B., Rokem, A., Schaefer, G., Sochat,
    V., Triplett, W., Turner, J.A., Varoquaux, G., Poldrack, R.A. (2016).
    **The brain imaging data structure,**
    **a format for organizing and describing outputs of neuroimaging experiments**.
    Scientific Data, 3 (160044).
    [doi:10.1038/sdata.2016.44](https://doi.org/10.1038/sdata.2016.44)

### Datatype specific publications

#### EEG

-   Pernet, C. R., Appelhoff, S., Gorgolewski, K.J., Flandin, G., Phillips, C.,
    Delorme, A., Oostenveld, R. (2019).
    **EEG-BIDS, an extension to the brain imaging data structure for electroencephalography**.
    Scientific data, 6 (103).
    [doi:10.1038/s41597-019-0104-8](https://doi.org/10.1038/s41597-019-0104-8)

#### iEEG

-   Holdgraf, C., Appelhoff, S., Bickel, S., Bouchard, K., D'Ambrosio, S.,
    David, O., Devinsky, O., Dichter, B., Flinker, A., Foster, B. L.,
    Gorgolewski, K. J., Groen, I., Groppe, D., Gunduz, A., Hamilton, L.,
    Honey, C. J., Jas, M., Knight, R., Lauchaux, J.-P., Lau, J. C.,
    Lee-Messer, C., Lundstrom, B. N., Miller, K. J., Ojemann, J. G.,
    Oostenveld, R., Petridou, N., Piantoni, G., Pigorini, A., Pouratian, N.,
    Ramsey, N. F., Stolk, A., Swann, N. C., Tadel, F., Voytek, B., Wandell, B. A.,
    Winawer, J., Whitaker, K., Zehl, L., Hermes, D. (2019).
    **iEEG-BIDS, extending the Brain Imaging Data Structure specification to**
    **human intracranial electrophysiology**.
    Scientific data, 6 (102).
    [doi:10.1038/s41597-019-0105-7](https://doi.org/10.1038/s41597-019-0105-7)

#### MEG

-   Niso Galan, J.G., Gorgolewski, K.J., Bock, E., Brooks, T.L., Flandin, G.,
    Gramfort, A., Henson, R.N., Jas, M., Litvak, V., Moreau, J., Oostenveld, R.,
    Schoffelen, J.-M., Tadel, F., Wexler, J., Baillet, S. (2018).
    **MEG-BIDS, the brain imaging data structure extended to magnetoencephalography**.
    Scientific Data, 5 (180110).
    [doi:10.1038/sdata.2018.110](https://doi.org/10.1038/sdata.2018.110)

#### PET

-   Norgaard, M., Matheson, G.J., Hansen, H.D., Thomas, A., Searle, G., Rizzo, G.,
    Veronese, M., Giacomel, A., Yaqub, M., Tonietto, M., Funck, T., Gillman, A., Boniface,
    H., Routier, A., Dalenberg, J.R.., Betthauser, T., Feingold, F., Markiewicz, C.J.,
    Gorgolewski, K.J., Blair, R.W., Appelhoff, S., Gau, R., Salo, T., Niso, G., Pernet, C.,
    Phillips, C., Oostenveld, R., Gallezot, J-D., Carson, R.E., Knudsen, G.M.,
    Innis R.B. & Ganz M. (2021).
    **PET-BIDS, an extension to the brain imaging data structure for positron emission tomography**.
    Scientific Data, 9 (65).
    [doi:10.1038/s41597-022-01164-1](https://doi.org/10.1038/s41597-022-01164-1)

-   Knudsen GM, Ganz M, Appelhoff S, Boellaard R, Bormans G, Carson RE, Catana C,
    Doudet D, Gee AD, Greve DN, Gunn RN, Halldin C, Herscovitch P, Huang H, Keller SH,
    Lammertsma AA, Lanzenberger R, Liow JS, Lohith TG, Lubberink M, Lyoo CH, Mann JJ,
    Matheson GJ, Nichols TE, Nørgaard M, Ogden T, Parsey R, Pike VW, Price J, Rizzo G,
    Rosa-Neto P, Schain M, Scott PJH, Searle G, Slifstein M, Suhara T, Talbot PS, Thomas A,
    Veronese M, Wong DF, Yaqub M, Zanderigo F, Zoghbi S, Innis RB. (2020).
    **Guidelines for Content and Format of PET Brain Data in Publications and in Archives: A Consensus Paper**.
    Journal of Cerebral Blood Flow and Metabolism, 2020 Aug; 40(8): 1576-1585.
    [doi:10.1177/0271678X20905433](https://doi.org/10.1177/0271678X20905433)

#### Genetics

-   Clara Moreau, Martineau Jean-Louis, Ross Blair, Christopher Markiewicz, Jessica Turner,
    Vince Calhoun, Thomas Nichols, Cyril Pernet (2020).
    **The genetics-BIDS extension: Easing the search for genetic data associated with human brain imaging**.
    GigaScience, 9 (10).
    [doi:10.1093/gigascience/giaa104](https://doi.org/10.1093/gigascience/giaa104)

#### Microscopy

-   Bourget M.-H., Kamentsky L., Ghosh S.S., Mazzamuto G., Lazari A., Markiewicz C.J., Oostenveld R.,
    Niso G., Halchenko Y.O., Lipp I., Takerkart S., Toussaint P.-J., Khan A.R., Nilsonne G.,
    Castelli F.M., The BIDS Maintainers and Cohen-Adad J. (2022).
    **Microscopy-BIDS: An Extension to the Brain Imaging Data Structure for Microscopy Data**.
    Frontiers in Neuroscience, 16 (871228).
    [doi:10.3389/fnins.2022.871228](https://doi.org/10.3389/fnins.2022.871228)

#### qMRI

-   Karakuzu, A., Appelhoff, S., Auer, T., Boudreau M., Feingold F., Khan A.R., Lazari A., Markiewicz C.J.,
    Mulder M., Phillips C., Salo T., Stikov N., Whitaker K. and de Hollander G. (2022).
    **qMRI-BIDS: An extension to the brain imaging data structure for quantitative magnetic resonance imaging data**.
    Scientific Data 9, (517).
    [doi:10.1038/s41597-022-01571-4](https://doi.org/10.1038/s41597-022-01571-4)

#### ASL

-   Clement P., Castellaro M., Okell T. W., Thomas D. L., Vandemaele P., Elgayar S., Oliver-Taylor A.,
    Kirk T., Woods J. G., Vos S. B., Kuijer J. P. A., Achten E., van Osch M. J. P., BIDS maintainers,
    Detre J. A., Lu H., Alsop D. C., Chappell M. A., Hernandez-Garcia L., Petr J. & Mutsaerts H. J. M. M. (2022)
    **ASL-BIDS, the brain imaging data structure extension for arterial spin labeling**.
    Scientific Data 9, (543).
    [doi:10.1038/s41597-022-01615-9](https://doi.org/10.1038/s41597-022-01615-9)

#### NIRS

-   Luke, R., Oostenveld, R., Cockx, H., Niso, G., Shader, M., Orihuela-Espina, F.,
    Innes-Brown, H., Tucker, S., Boas, D., Gau, R., Salo, T., Appelhoff, S., Markiewicz, C
    McAlpine, D., BIDS maintainers, Pollonini, L. (2023).
    **fNIRS-BIDS, the Brain Imaging Data Structure Extended to Functional Near-Infrared Spectroscopy**.
    PsyArXiv.
    [doi:10.31219/osf.io/7nmcp](https://doi.org/10.31219/osf.io/7nmcp)

#### Motion

-   Jeung, S., Cockx, H., Appelhoff, S., Berg, T., Gramann, K., Grothkopp, S., Warmerdam, E., Hansen, C.,
    Oostenveld, R., BIDS maintainers, Welzel, J. (2023).
    **Motion-BIDS: extending the Brain Imaging Data Structure specification to organize motion data for reproducible research**.
    PsyArXiv.
    [doi:10.31234/osf.io/w6z79](https://doi.org/10.31234/osf.io/w6z79)

#### MRS

-   (publication forthcoming)

### Research Resource Identifier (RRID)

BIDS has also a
[Research Resource Identifier (RRID)](https://force11.org/group/resource-identification-initiative),
which you can also include in your citations in addition to relevant publications (see above):

-   [`RRID:SCR_016124`](https://rrid.site/data/record/nlx_144509-1/SCR_016124/resolver?q=SCR_016124)
