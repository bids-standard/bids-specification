# Dataset description

Templates:

-   `dataset_description.json`
-   `README[.md|.rst|.txt]`
-   `CITATION.cff`
-   `datacite.yml`
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
{{ MACROS___make_json_table('dataset_metadata.dataset_description') }}

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
  "BIDSVersion": "1.10.1",
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
  "HEDVersion": "8.4.0",
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

## Structured citation files

BIDS permits structured citation files that may improve interoperability with
dataset indexing utilities or afford higher precision than fields in
`dataset_description.json`.

If these files are used, fields that provide information that is redundant with
`dataset_description.json` fields SHOULD be preferred to those in `dataset_description.json`.

To avoid inconsistency, metadata present in one of the following files SHOULD NOT be
be included in `dataset_description.json`, with the exception of `Name` and
`DatasetDOI`, to ensure that tools that are only aware of `dataset_description.json`
can generate references to the dataset.

In particular, if a structured citation file is present,
the `"Authors"` field of `dataset_description.json` MUST be omitted.

### `CITATION.cff`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.CITATION.description") }}

If `CITATION.cff` is present,
the `"HowToAcknowledge"`, `"License"` and `"ReferencesAndLinks"` fields SHOULD be omitted
from `dataset_description.json` in favor of the `CITATION.cff` fields
`message`/`preferred-citation`, `license` and `references`.

### `datacite.yml`

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.datacite.description") }}

If `datacite.yml` is present, the `"License"` field SHOULD be omitted
from `dataset_description.json` in favor of the `datacite.yml` field `rightsList`.

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
