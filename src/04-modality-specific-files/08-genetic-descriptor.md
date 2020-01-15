# Genetic Descriptor

Support for genetic descriptors was developed as a [BIDS Extension
Proposal](../06-extensions.md#bids-extension-proposals).
The extension was primarily developped by Cyril Pernet and Clara Moreau with
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

`dataset_description.json` example:
```JSON
{
  "Name": "Human Connectom Project",
  "BIDSVersion":  "1.2.0",
  "License": "CC0",
  "Authors": ["1st author", "2nd author"],
  "Funding": "list your funding sources",
  "Genetics": {
     "Dataset": "dataset",
     "Database": "database",
     "Descriptors": "descriptors"
     }
}
```

## Subject naming and Participants file

If the same participants have different identifiers in the genetic and imaging datasets,
the column `GeneticID` SHOULD be added to the `participants.tsv` file to associate
the BIDS participant with a subject in the `Genetics.Dataset` referred to in the
`dataset_description.json` file.

Information about the presence/absence of specific genetic markers MAY be duplicated
in the `participants.tsv` file by adding optional columns.

`participants.tsv` example:

```Text
participant_id  age sex group GeneticID	IDH Mutation
sub-control01 34  M control 124587	yes
sub-control02 12  F control 548936	yes
sub-patient01 33  F patient 489634	no
```

## genetic_info.json

This file is the descriptor of the genetic information available either in the participant tsv file and/or the genetic database described in the dataset_description.json. The `GeneticLevel` and `SampleOrigin` are the only two mandatory fields.

| Field name         | Definition                                                                  | Values                                                                                                                                                                |
| :----------------- | :-------------------------------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| GeneticLevel       | MANDATORY Describes the level of analysis                                   | `Genetic`, `Genomic`, `Epigenomic`, `Transcriptomic`, `Metabolomic`, or `Proteomic`                                                                                   |
| AnalyticalApproach | OPTIONAL Methodology used to analyse the GeneticLevel                       | Value must be taken from [gapsolr] under /Study/Molecular Data Type, for instance `SNP Genotypes (Array)` or `Methylation (CpG)`                                      |
| SampleOrigin       | MANDATORY Describes from which tissue the genetic information was extracted | `blood`, `saliva`, `brain`, `csf`, `breast milk`, `bile`, `amniotic fluid`, `other biospecimen`                                                                       |
| TissueOrigin       | OPTIONAL Describes the type of tissue analyzed for SampleOrigin `brain`     | `gray matter`, `white matter`, `csf`, `meninges`, `macrovascular` or `microvascular`                                                                                  |
| BrainLocation      | OPTIONAL Refers to the location in space of the TissueOrigin                | `MNI coordinate` or a `label` taken from the [Allen Brain Atlas] possibly `layer` to refer to layer-specific gene expression, which can also tie up with laminar fMRI |
| CellType           | OPTIONAL Describes the type of cell analyzed                                | Value should come from the [cell ontology]                                                                                                                            |

`genetic_info.json` example:

```JSON
{
  "GeneticLevel": "Genetic",
  "AnalyticalApproach": "SNP Genotypes", "SampleOrigin": "brain",
  "TissueOrigin": "gray matter",
  "CellType":  "neuron",
  "BrainLocation": "[-30 -15 10]"
}
```

[Allen Brain Atlas]: http://atlas.brain-map.org/atlas?atlas=265297125&plate=112360888&structure=4392&x=40348.15104166667&y=46928.75&zoom=-7&resolution=206.60&z=3
[cell ontology]: http://obofoundry.org/ontology/cl.html
[gapsolr]: https://www.ncbi.nlm.nih.gov/projects/gapsolr/facets.html
