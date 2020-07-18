# Genetic Descriptor

Support for genetic descriptors was developed as a [BIDS Extension
Proposal](../07-extensions.md#bids-extension-proposals).
The extension was primarily developed by Cyril Pernet and Clara Moreau with
contributions from Tom Nichols and Jessica Turner.

Genetic data are typically stored in dedicated repositories,
separate from imaging data.
A genetic descriptor links a BIDS dataset to associated genetic data,
potentially in a separate repository,
with details of where to find the genetic data and the type of data available.

## Dataset Description

Genetic descriptors are encoded as an additional, OPTIONAL entry in the
[`dataset_description.json`](../03-modality-agnostic-files.md#dataset_descriptionjson)
file.

Datasets linked to a genetic database entry include the following REQUIRED or OPTIONAL
`dataset_description.json` keys (a dot in the key name denotes a key in a subdictionary):

| Field name           | Definition                                                                     |
|----------------------|--------------------------------------------------------------------------------|
| Genetics.Dataset     | REQUIRED. URI where data can be retrieved.                                     |
| Genetics.Database    | OPTIONAL. URI of database where the dataset is hosted.                         |
| Genetics.Descriptors | OPTIONAL. List of relevant descriptors (*e.g.*, journal articles) for dataset. |

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
     "Descriptors": ["https://doi.org/10.1016/j.neuroimage.2013.05.041"]
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
[Tabular files](../02-common-principles.md#tabular-files).

`participants.tsv` example:

```Text
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

The `genetic_info.json` file describes the genetic information available in the
`participants.tsv` file and/or the genetic database described in
`dataset_description.json`.
Datasets containing the `Genetics` field in `dataset_description.json` or the
`genetic_id` column in `participants.tsv` MUST include this file with the following
fields:

| Field name                                                  | Definition                                                                                                                                                                                                                                                                               |
|-------------------------------------------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GeneticLevel                                                | REQUIRED. String. Describes the level of analysis. Values MUST be one of `Genetic`, `Genomic`, `Epigenomic`, `Transcriptomic`, `Metabolomic`, or `Proteomic`.                                                                                                                            |
| AnalyticalApproach                                          | OPTIONAL. String or list of strings. Methodology or methodologies used to analyse the GeneticLevel. Values MUST be taken from the [database of Genotypes and Phenotypes (dbGaP)][gapsolr] under /Study/Molecular Data Type, for instance `SNP Genotypes (Array)` or `Methylation (CpG)`. |
| SampleOrigin                                                | REQUIRED. String. Describes from which tissue the genetic information was extracted. Values MUST be one of `blood`, `saliva`, `brain`, `csf`, `breast milk`, `bile`, `amniotic fluid`, `other biospecimen`.                                                                              |
| TissueOrigin                                                | OPTIONAL. String. Describes the type of tissue analyzed for SampleOrigin `brain`. Values MUST be one of `gray matter`, `white matter`, `csf`, `meninges`, `macrovascular` or `microvascular`.                                                                                            |
| BrainLocation                                               | OPTIONAL. String. Refers to the location in space of the `TissueOrigin`. Values may be an MNI coordinate, a label taken from the [Allen Brain Atlas][allen], or layer to refer to layer-specific gene expression, which can also tie up with laminar fMRI.                               |
| CellType                                                    | OPTIONAL. String. Describes the type of cell analyzed. Values SHOULD come from the [cell ontology][ontology].                                                                                                                                                                            |

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

[allen]: http://atlas.brain-map.org/atlas?atlas=265297125&plate=112360888&structure=4392&x=40348.15104166667&y=46928.75&zoom=-7&resolution=206.60&z=3
[ontology]: http://obofoundry.org/ontology/cl.html
[gapsolr]: https://www.ncbi.nlm.nih.gov/gap/advanced_search/
