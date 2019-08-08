# Genetic Descriptor

The extension was primarily developped by Cyril Pernet and Clara Moreau with contributions from Tom Nichols and Jessica Turner.

The goal of the genetic descriptor is to link imaging and genetic data by providing minimal information about i) where to find genetic information associated with the imaging data and ii) what type of genetic information is available. This is necessary as genetic data are typically stored in dedicated repositories, separately from the imaging data.

## dataset_description.json

Two additional keys related to the genetic data can be added. The Key `GeneticDataBase` (MANDATORY) links to the name of the database and web address. The key `GeneticDescriptor` (OPTIONAL) refers to the descriptor (e.g. journal article) of the genetic data.

`dataset_description.json` example:

{  
  "Name": "xxxxx",  
  "BIDSVersion":  "xxxxx",  
  "License": "CC0",  
  "Authors": ["1st author", "2nd author"],  
  "Funding": "list your funding sources",  
  "GeneticDataBase": ["Name", "www",],  
  "GeneticDescriptor": ["data paper", "10.0.2.3/dfjj.10"]  
}

## Subject naming and Participants file

One issue with having two repositories (one for imaging, one for genetics) is naming of subjects. A simple solution is to use the same ID in both datasets. Alternatively, one can encode the name used in the genetic database in the participant.tsv file. The column `GeneticID` (OPTIONAL) encodes the ID used for the same subject in the `GeneticDataBase` referred to in the dataset_description.json file.

Information about the presence/absence of specific genetic markers can be and should be shared simply in the participants.tsv file adding optopnal columns.

`participants.tsv` example:

```Text
participant_id  age sex group GeneticID	IDH Mutation
sub-control01 34  M control 124587	yes
sub-control02 12  F control 548936	yes
sub-patient01 33  F patient 489634	no
```

## genetic_info.json

This file is the descriptor of the genetic information available either in the participant tsv file and/or the genetic database described in the dataset_description.json. The 'GeneticLevel' and 'SampleOrigin' are the only two mandatory fields.

| Field name   | Definition | Values |
| :----------- | :--------- | :------|
| GeneticLevel | MANDATORY Describes the level of analysis | `Genetic`, `Genomic`, `Epigenomic`, `Transcriptomic`, `Metabolomic`, or `Proteomic` |
| AnalyticalApproach | OPTIONAL Methodology used to analyse the GeneticLevel | Value must be taken from [gapsolr](https://www.ncbi.nlm.nih.gov/projects/gapsolr/facets.html) under /Study/Molecular Data Type, for instance `SNP Genotypes (Array)` or `Methylation (CpG)` |
| SampleOrigin | MANDATORY Describes from which tissue the genetic information was extracted from | `blood`, `saliva`, `brain`, `csf`, `breast milk`, `bile`, `amniotic fluid`, `other biospecimen` |
| TissueOrigin | OPTIONAL Describes the type of tissue analyzed for SampleOrigin `brain` | `gray matter`, `white matter`, `csf`, `meninges`, `macrovascular` or `microvascular` |
| BrainLocation | OPTIONAL Refers to the location in space of the TissueOrigin | `MNI coordinate` or a `label` taken from the [Allen Brain Atlas](http://atlas.brain-map.org/atlas?atlas=265297125#atlas=265297125&plate=112360888&structure=4392&x=40348.15104166667&y=46928.75&zoom=-7&resolution=206.60&z=3) possibly `layer` to refer to layer-specific gene expression, which can also tie up with laminar fMRI |
| CellType | OPTIONAL Describes the type of cell analyzed | Value should come from the [cell ontology](http://obofoundry.org/ontology/cl.html) |

`genetic_info.json` example:

{  
  "GeneticLevel": "Genetic",  
  "AnalyticalApproach": "SNP Genotypes",  
  "SampleOrigin": "brain",  
  "TissueOrigin": "gray matter",  
  "CellType":  "neuron",  
  "BrainLocation": "[-30 -15 10]"  
}
