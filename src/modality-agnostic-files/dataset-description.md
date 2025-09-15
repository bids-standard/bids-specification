# Dataset description

Templates:

-   `dataset_description.json`
-   `README[.md|.rst|.txt]`
-   `CITATION.cff`
-   `CHANGES`
-   `LICENSE[.md|.rst|.txt]`

## `dataset_description.json`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.dataset_description.description") }}

Every dataset MUST include this file with the following fields:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Name": "REQUIRED",
      "BIDSVersion": "REQUIRED",
      "HEDVersion": "RECOMMENDED",
      "DatasetLinks": "REQUIRED if [BIDS URIs][] are used",
      "DatasetType": "RECOMMENDED",
      "License": "RECOMMENDED",
      "Authors": "RECOMMENDED if CITATION.cff is not present",
      "Keywords": "OPTIONAL",
      "Acknowledgements": "OPTIONAL",
      "HowToAcknowledge": "OPTIONAL",
      "Funding": "OPTIONAL",
      "EthicsApprovals": "OPTIONAL",
      "ReferencesAndLinks": "OPTIONAL",
      "DatasetDOI": "OPTIONAL",
      "GeneratedBy": "RECOMMENDED",
      "SourceDatasets": "RECOMMENDED",
   }
) }}

Each object in the `GeneratedBy` array includes the following REQUIRED, RECOMMENDED
and OPTIONAL keys:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.GeneratedBy.items") }}

Example:

```JSON
{
  "Name": "The mother of all experiments",
  "BIDSVersion": "1.6.0",
  "DatasetType": "raw",
  "License": "CC0",
  "Authors": [
    "Paul Broca",
    "Carl Wernicke"
  ],
  "Keywords": [
    "neuroscience",
    "language",
    "brain"
  ],
  "Acknowledgements": "Special thanks to Korbinian Brodmann for help in formatting this dataset in BIDS. We thank Alan Lloyd Hodgkin and Andrew Huxley for helpful comments and discussions about the experiment and manuscript; Hermann Ludwig Helmholtz for administrative support; and Claudius Galenus for providing data for the medial-to-lateral index analysis.",
  "HowToAcknowledge": "Please cite this paper: https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
  "Funding": [
    "National Institute of Neuroscience Grant F378236MFH1",
    "National Institute of Neuroscience Grant 5RMZ0023106"
  ],
  "EthicsApprovals": [
    "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. doi:1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "doi:10.0.2.3/dfjj.10",
  "HEDVersion": "8.0.0",
  "GeneratedBy": [
    {
      "Name": "reproin",
      "Version": "0.6.0",
      "Container": {
        "Type": "docker",
        "Tag": "repronim/reproin:0.6.0"
      }
    }
  ],
  "SourceDatasets": [
    {
      "URL": "s3://dicoms/studies/correlates",
      "Version": "April 11 2011"
    }
  ]
}
```

### Derived dataset and pipeline description

As for any BIDS dataset, a `dataset_description.json` file MUST be found at the
top level of every derived dataset:
`<dataset>/derivatives/<pipeline-name>/dataset_description.json`.

In contrast to raw BIDS datasets, derived BIDS datasets MUST include a
`GeneratedBy` key:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneratedBy": "REQUIRED"
   }
) }}

If a derived dataset is stored as a subdirectory of the raw dataset, then the `Name` field
of the first `GeneratedBy` object MUST be a substring of the derived dataset directory name.
That is, in a directory `<dataset>/derivatives/<pipeline-name>[-<variant>]/`, the first
`GeneratedBy` object should have a `Name` of `<pipeline-name>`.

Example:

```JSON
{
  "Name": "FMRIPREP Outputs",
  "BIDSVersion": "1.6.0",
  "DatasetType": "derivative",
  "GeneratedBy": [
    {
      "Name": "fmriprep",
      "Version": "1.4.1",
      "Container": {
        "Type": "docker",
        "Tag": "poldracklab/fmriprep:1.4.1"
        }
    },
    {
      "Name": "Manual",
      "Description": "Re-added RepetitionTime metadata to bold.json files"
    }
  ],
  "SourceDatasets": [
    {
      "DOI": "doi:10.18112/openneuro.ds000114.v1.0.1",
      "URL": "https://openneuro.org/datasets/ds000114/versions/1.0.1",
      "Version": "1.0.1"
    }
  ]
}
```

## `README`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.README.description") }}

## `CITATION.cff`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.CITATION.description") }}

For most redundant fields between `CITATION.cff` and `dataset_description.json`,
the `CITATION.cff` SHOULD take precedence.
To avoid inconsistency, metadata present in `CITATION.cff` SHOULD NOT be
be included in `dataset_description.json`, with the exception of `Name` and
`DatasetDOI`, to ensure that `CITATION.cff`-unaware tools can generate
references to the dataset.
In particular, if `CITATION.cff` is present,
the `"Authors"` field of `dataset_description.json` MUST be omitted,
and the `"HowToAcknowledge"`, `"License"` and `"ReferencesAndLinks"` SHOULD be omitted
in favor of the `CITATION.cff` fields `message`/`preferred-citation`, `license` and
`references`.

## `CHANGES`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.CHANGES.description") }}

Example:

```Text
1.0.1 2015-08-27
  - Fixed slice timing information.

1.0.0 2015-08-17
  - Initial release.
```

## `LICENSE`

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.LICENSE.description") }}

<!-- Link Definitions -->

[bids uris]: ../common-principles.md#bids-uri
