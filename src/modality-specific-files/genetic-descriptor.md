# Genetic Descriptor

Support for genetic descriptors was developed as a
[BIDS Extension Proposal](../extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Genetic data are typically stored in dedicated repositories,
separate from imaging data.
A genetic descriptor links a BIDS dataset to associated genetic data,
potentially in a separate repository,
with details of where to find the genetic data and the type of data available.

!!! example "Example datasets"

    The following example dataset with genetics data have been formatted using this specification
    and can be used for practical guidance when curating a new dataset.

    -   [`UK biobank`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)

## Dataset Description

If information on associated genetic data is supplied as part of a BIDS dataset,
these "genetic descriptors" are encoded as an additional, REQUIRED entry in the
[`dataset_description.json`](../modality-agnostic-files.md#dataset_descriptionjson)
file.

Datasets linked to a genetic database entry include the following REQUIRED and OPTIONAL
keys in the `Genetics` sub-[object][] of `dataset_description.json`:

<!-- This block generates a table describing subfields within a metadata field.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_subobject_table("metadata.Genetics") }}

Example:

```JSON
{
  "Name": "Human Connectome Project",
  "BIDSVersion":  "1.3.0",
  "License": "CC0",
  "Authors": ["1st author", "2nd author"],
  "Funding": ["P41 EB015894/EB/NIBIB NIH HHS/United States"],
  "Genetics": {
     "Dataset": "https://www.ncbi.nlm.nih.gov/projects/gap/cgi-bin/study.cgi?study_id=phs001364.v1.p1",
     "Database": "https://www.ncbi.nlm.nih.gov/gap/",
     "Descriptors": ["doi:10.1016/j.neuroimage.2013.05.041"]
  }
}
```

## Subject naming and Participants file

If the same participants have different identifiers in the genetic and imaging datasets,
the column `genetic_id` SHOULD be added to the `participants.tsv` file to associate
the BIDS participant with a subject in the `Genetics.Dataset` referred to in the
`dataset_description.json` file.

Information about the presence/absence of specific genetic markers MAY be duplicated
in the `participants.tsv` file by adding optional columns (like `idh_mutation` in the
example below).
Note that optional columns MUST be further described in an accompanying
`participants.json` file as described in
[Tabular files](../common-principles.md#tabular-files).

`participants.tsv` example:

```tsv
participant_id	age	sex	group	genetic_id	idh_mutation
sub-control01	34	M	control	124587	yes
sub-control02	12	F	control	548936	yes
sub-patient01	33	F	patient	489634	no
```

## Genetic Information

Template:

```Text
genetic_info.json
```

The following fields are defined for genetic_info.json:

<!-- This block generates a description.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___render_text("objects.files.genetic_info.description") }}

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "GeneticLevel": "REQUIRED",
      "AnalyticalApproach": "OPTIONAL",
      "SampleOrigin": "REQUIRED",
      "TissueOrigin": "OPTIONAL",
      "BrainLocation": "OPTIONAL",
      "CellType": "OPTIONAL",
   }
) }}

To ensure dataset description consistency, we recommend following [Multi-omics approaches to disease](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-017-1215-1) by Hasin et al. 2017 to determine the `GeneticLevel:`

-   `Genetic`: data report on a single genetic location (typically directly in the `participants.tsv` file)
-   `Genomic`:  data link to participants' genome (multiple genetic locations)
-   `Epigenomic`: data link to participants' characterization of reversible modifications of DNA
-   `Transcriptomic`: data link to participants RNA levels
-   `Metabolomic`: data link to participants' products of cellular metabolic functions
-   `Proteomic`: data link to participants peptides and proteins quantification

`genetic_info.json` example:

```JSON
{
  "GeneticLevel": "Genomic",
  "AnalyticalApproach": ["Whole Genome Sequencing", "SNP/CNV Genotypes"],
  "SampleOrigin": "brain",
  "TissueOrigin": "gray matter",
  "CellType":  "neuron",
  "BrainLocation": "[-30 -15 10]"
}
```

<!-- Link Definitions -->

[object]: https://www.json.org/json-en.html
