1 Dataset description
---------------------

Template: `dataset_description.json` `README` `CHANGES`

### 8.1.1 `dataset_description.json`

The file dataset_description.json is a JSON file describing the dataset. Every dataset MUST include this file with the following fields:

| Field name         | Definition                                              |
|:-------------------|:--------------------------------------------------------|
| Name               | REQUIRED. Name of the dataset.                          |
| BIDSVersion        | REQUIRED. The version of the BIDS standard that was used. |
| License            | RECOMMENDED. What license is this dataset distributed under? The use of license name abbreviations is suggested for specifying a license. A list of common licenses with suggested abbreviations can be found in Appendix II. |
| Authors            | OPTIONAL. List of individuals who contributed to the creation/curation of the dataset. |
| Acknowledgements   | OPTIONAL. Text acknowledging contributions of individuals or institutions  beyond those listed in Authors or Funding. |
| HowToAcknowledge   | OPTIONAL. Instructions how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset. |
| Funding            | OPTIONAL. List of sources of funding (grant numbers)    |
| ReferencesAndLinks | OPTIONAL. List of references to publication that contain information on the dataset, or links. |
| DatasetDOI         | OPTIONAL. The Document Object Identifier of the dataset (not the corresponding paper). |

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.0.1",
  "License": "CC0",
  "Authors": [
    "Paul Broca",
    "Carl Wernicke"
  ],
  "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
  "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
  "Funding": [
    "National Institute of Neuroscience Grant F378236MFH1",
    "National Institute of Neuroscience Grant 5RMZ0023106"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. http://doi.org/1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "10.0.2.3/dfjj.10"
}
```

### 8.1.2 `README`

In addition a free form text file (`README`) describing the dataset in more details SHOULD be provided.

### 8.1.3 `CHANGES`

Version history of the dataset (describing changes, updates and corrections) MAY be provided in the form of a `CHANGES` text file. This file MUST follow the CPAN Changelog convention: [http://search.cpan.org/~haarg/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod](https://metacpan.org/pod/release/HAARG/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod). `README` and `CHANGES` files MUST be either in ASCII or UTF-8 encoding.

Example:

```
1.0.1 2015-08-27
 - Fixed slice timing information.

1.0.0 2015-08-17
 - Initial release.
```
