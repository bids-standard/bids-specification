# Provenance

## Overview

### Goals

Interpreting and comparing scientific results and enabling reusable data and analysis output require understanding provenance, i.e. how the data were generated and processed. To be useful, the provenance must be comprehensive, understandable, easily communicated, and captured automatically in machine accessible form. Provenance records are thus used to encode transformations between digital objects.

This part of the BIDS specification -referred as BIDS-Prov in the following- is aimed at describing the provenance of a BIDS dataset. This description is retrospective, i.e. it describes a set of steps that were executed in order to obtain the dataset (this is different from prospective descriptions of workflows that could for instance list all sets of steps that can be run on this dataset).

### Which type of provenance is covered in BIDS ?

Provenance comes up in many different contexts in BIDS. This specification focuses on representing the processings that were applied to a dataset. These could be for instance:

1. The raw conversion from DICOM images or other instrument native formats to BIDS layout, details of stimulus presentation and cognitive paradigms, and clinical and neuropsychiatric assessments, each come with their own details of provenance.
2. In BIDS derivatives, the consideration of outputs requires knowledge of which inputs from the BIDS dataset were used together with what software was run in what environment and with what parameters.

But provenance comes up in other contexts as well, which might be addressed at a later stage:

3. For datasets and derivatives, provenance can also include details of why the data were collected in the first place covering hypotheses, claims, and prior publications. Provenance can encode support for which claims were supported by future analyses.
4. Provenance can involve information about people and institutions involved in a study.
5. Provenance records can highlight reuse of datasets while providing appropriate attribution to the original dataset generators as well as future transformers.

Provenance can be captured using different mechanisms, but independent of encoding, always reflects transformations by either humans or software. The interpretability of provenance records requires a consistent vocabulary for provenance as well as an expectation for a consistent terminology for the objects being encoded.

### Principles for encoding provenance in BIDS

1. Provenance information SHOULD be included in a BIDS dataset when possible.
2. If provenance records are included, these MUST be described using the conventions detailed by this specification.
3. Provenance records MAY be used to reflect the provenance of a dataset, a collection of files or a specific file at any level of the BIDS hierarchy.
4. Provenance information SHOULD be anonymized/de-identified as necessary.

### Provenance format

Provenance metadata is written in JSON or JSON-LD. JSON-LD is a specific type of JSON that allows encoding graph-like structures with the [Resource Description Framework](https://www.w3.org/TR/json-ld11/#basic-concepts).

Provenance records use the [PROV model ontology](http://www.w3.org/TR/prov-o/), augmented by terms curated in this specification, and defined in the [BIDS-Prov context](/context.json).

![](/images/prov_w3c.svg)

A skeleton for a BIDS-Prov JSON-LD file looks like this:
```
{
    "@context": "https://purl.org/nidash/bidsprov/context.json",
    "BIDSProvVersion": "0.0.1",
    "Records": {
        "Agent": [
            {
                    <...Agent 1...>
            },
            {
                    <...Agent 2...>
            }
        ],
        "Activity": [
            {
                    <...Activity 1...>
            },
            {
                    <...Activity 2...>
            }
        ],
        "Entity": [
            {
                    <...Entity 1...>
            },
            {
                    <...Entity 2...>
            }
        ],
        "Environment": [
            {
                    <...Environment 1...>
            },
            {
                    <...Environment 2...>
            }
        ]
  }
}
```

<table>
  <tr>
   <td><strong>Key name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>@context</code>
   </td>
   <td>REQUIRED. A URL to the BIDS-Prov json context. Value must be <code>"https://purl.org/nidash/bidsprov/context.json"</code>
   </td>
  </tr>
  <tr>
   <td><code>BIDSProvVersion</code>
   </td>
   <td>REQUIRED. A string identifying the version of the specification adhered to.
   </td>
  </tr>
  <tr>
   <td><code>Records</code>
   </td>
   <td>REQUIRED. A list of provenance records (Activity, Entity, Agent, Environment), describing the provenance (see the <a href="#provenance-records">Provenance records</a> section below).
   </td>
  </tr>
</table>

BIDS-Prov allows this skeleton to be split into several *JSON* files. This is described in sections [Suffixes](#suffixes)
and [Provenance description levels](#provenance-description-levels).

Using tools provided by BIDS-Prov ([Tools](#tools)), these JSON contents can be merged back to a structured JSON-LD as described above.

!!! note
    Since the JSON-LD documents are graph objects, they can be aggregated using RDF tools without the need to apply the inheritance principle.

!!! warning
    A group of provenance records MUST be described:
     * either in several `.json` files ;
     * or in several `.jsonld` files.

!!! bug
    TODO: the schema cited below does not exist

A complete schema for the model file to facilitate specification and validation is available from [https://github.com/bids-standard/BEP028_BIDSprov](https://github.com/bids-standard/BEP028_BIDSprov). In the event of disagreements between the schema and the specification, the specification is authoritative.

## Provenance records

BIDS-Prov metadata consists in a set or records. There are 4 types of records: `Activity`, `Entity`, `Agent`, and `Environment`.

Activities represent the transformations that have been applied to the data. Each Activity can use Entities as inputs and outputs. The Agent specifies the software package. Environments specify the software environment in which the provenance record was obtained.

![](/images/prov_records.svg)

### Activity
Each Activity record is a JSON Object with the following fields:

!!! bug
    TODO: AssociatedWith and Used can also entirely describe the Agent (resp. Entity)
    TODO: Can an Activity represent a group of command lines ? If so, Command can be a list

<table>
  <tr>
   <td><strong>Key name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>Id</code>
   </td>
   <td>REQUIRED. Unique URIs (for example a UUID). Identifier for the  activity.
   </td>
  </tr>
  <tr>
   <td><code>Label</code>
   </td>
   <td>REQUIRED. String. Name of the tool, script, or function used (e.g. “bet”, "recon-all", "myFunc", "docker").
   </td>
  </tr>
  <tr>
   <td><code>Command</code>
   </td>
   <td>REQUIRED. String. Command used to run the tool, including all parameters.
   </td>
  </tr>
  <tr>
   <td><code>AssociatedWith</code>
   </td>
   <td>OPTIONAL. UUID (or List of UUIDs). Identifier(s) of the software package(s) used to compute this activity. The corresponding Agent must be defined with its own Agent record).
   </td>
  </tr>
  <tr>
   <td><code>Used</code>
   </td>
   <td>OPTIONAL. UUID (or List of UUIDs). Identifier(s) of entitie(s) or environment(s) used by this activity. The corresponding Entities (resp. Environments) must be defined with their own Entity (resp. Environment) record.
   </td>
  </tr>
  <tr>
   <td><code>Type</code>
   </td>
   <td>OPTIONAL. URI. A term from a controlled vocabulary that more specifically describes the Activity.
   </td>
  </tr>
  <tr>
   <td><code>StartedAtTime</code>
   </td>
   <td>OPTIONAL. xsd:<em>dateTime. </em>A timestamp tracking when this activity started
   </td>
  </tr>
  <tr>
   <td><code>EndedAtTime</code>
   </td>
   <td>OPTIONAL. xsd:<em>dateTime. </em>A timestamp tracking when this activity ended
   </td>
  </tr>
</table>

Here is an example of an Activity record:
```JSON
{
    "Id": "bids::prov/#conversion-00f3a18f",
    "Label": "Dicom to Nifti conversion",
    "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
    "AssociatedWith": "bids::prov/#dcm2niix-khhkm7u1",
    "Used": [
        "bids::prov/#fedora-uldfv058",
        "bids::sourcedata/dicoms"
    ],
    "Type": "Activity",
    "StartedAtTime": "2025-03-13T10:26:00",
    "EndedAtTime": "2025-03-13T10:26:05"
}
```

### Entity
Each Entity record is a JSON Object with the following fields:

!!! bug
    TODO: GeneratedBy can also entirely describe the Activity

<table>
  <tr>
   <td><strong>Key name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>Id</code>
   </td>
   <td>REQUIRED. Unique URIs (for example a UUID). Identifier for the entity.
   </td>
  </tr>
  <tr>
   <td><code>Label</code>
   </td>
   <td>REQUIRED. String. A name for the entity.
   </td>
  </tr>
  <tr>
   <td><code>AtLocation</code>
   </td>
   <td>OPTIONAL. String. For input files, this is the relative path to the file on disk.
   </td>
  </tr>
  <tr>
   <td><code>GeneratedBy</code>
   </td>
   <td>OPTIONAL. UUID (or List of UUIDs). Identifier(s) of the Activity(ies) which generated this Entity. The corresponding Activity must be defined with its own Activity record.
   </td>
  </tr>
  <tr>
   <td><code>Type</code>
   </td>
   <td>OPTIONAL. URI. A term from a controlled vocabulary that more specifically describes the Entity.
   </td>
  </tr>
  <tr>
   <td><code>Digest</code>
   </td>
   <td>RECOMMENDED. Dict. For files, this would include checksums of files. It would take the form {"<checksum-name>": "value"}.
   </td>
  </tr>
</table>

Here is an example of an Entity record:
```JSON
{
    "Id": "bids::sub-02/anat/sub-02_T1w.nii",
    "Label": "sub-02_T1w.nii",
    "AtLocation": "sub-02/anat/sub-02_T1w.nii",
    "GeneratedBy": "bids::prov/#conversion-00f3a18f",
    "Type": "Activity",
    "Digest": {
        "SHA-256": "42d8faeaa6d4988a9233a95860ef3f481fb0daccce4c81bc2c1634ea8cf89e52"
    }
}
```

### Agent (Optional)
Agent records are OPTIONAL. If included, each Agent record is a JSON Object with the following fields:

!!! bug
    TODO: do we need a Type field for Agent?
    TODO: shall we use `Software`, `Agent`, `SoftwareAgent` ?

<table>
  <tr>
   <td><strong>Key name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>Id</code>
   </td>
   <td>REQUIRED. A unique identifier like a UUID that will be used to associate activities with this software (e.g., urn:1264-1233-11231-12312, "urn:bet-o1ef4rt"
   </td>
  </tr>
  <tr>
   <td><code>AltIdentifier</code>
   </td>
   <td>OPTIONAL. URI. URI of the RRID for this software package (cf. <a href="https://scicrunch.org/resources/about/Getting%20Started">scicrunch</a>).
   </td>
  </tr>
  <tr>
   <td><code>Label</code>
   </td>
   <td>REQUIRED. String. Name of the software.
   </td>
  </tr>
  <tr>
   <td><code>Version</code>
   </td>
   <td>REQUIRED. String. Version of the software.
   </td>
  </tr>
</table>

Here is an example of an Agent record:
```JSON
{
    "Id": "bids::prov/#dcm2niix-khhkm7u1",
    "AltIdentifier": "RRID:SCR_023517",
    "Label": "dcm2niix",
    "Version": "v1.0.20220720"
}
```

### Environment (Optional)
Environment records are OPTIONAL. If included, each Environment record is a JSON Object with the following fields:

!!! bug
    TODO: do we need a Type field for Environment?
    TODO: Environment not currently defined in the BIDS-Prov context

<table>
  <tr>
   <td><strong>Key name</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>
  <tr>
   <td><code>Id</code>
   </td>
   <td>REQUIRED. Unique URIs (for example a UUID). Identifier for the environment (this identifier will be used to associated activities with this environment).
   </td>
  </tr>
  <tr>
   <td><code>Label</code>
   </td>
   <td>REQUIRED. String. Name of the software.
   </td>
  </tr>
  <tr>
   <td><code>EnvVars</code>
   </td>
   <td>OPTIONAL. Dict. A dictionary defining the environment variables as key-value pairs.
   </td>
  </tr>
  <tr>
   <td><code>OperatingSystem</code>
   </td>
   <td>OPTIONAL. String. Name of the operating system.
   </td>
  </tr>
  <tr>
   <td><code>Dependencies</code>
   </td>
   <td>OPTIONAL. Dict. A dictionary defining the software used and their versions as key-value pairs.
   </td>
  </tr>
</table>

Here is an example of an Environment record:
```JSON
{
    "Id": "bids::prov/#fedora-uldfv058",
    "Label": "Fedora release 36 (Thirty Six)",
    "OperatingSystem": "GNU/Linux 6.2.15-100.fc36.x86_64"
}
```

## File naming

This section describes additions to the BIDS naming conventions for BIDS-Prov files.

For further information about naming conventions, please consult the BIDS specification ([https://bids-specification.readthedocs.io](https://bids-specification.readthedocs.io)). Until these conventions are established in BIDS, it is RECOMMENDED to use the following.

### Extensions

BIDS-Prov files contain JSON or JSON-LD data, hence having either a `.json` or a `.jsonld` extension.

When using a `.jsonld` extension, the contents of the file must be JSON-LD.

As JSON-LD is JSON, `*.jsonld` files can contain JSON.

### The `prov` entity

BIDS-Prov introduces the following entity:

`prov`
* Full name: Provenance records
* Format: `prov-<label>`
* Definition: A grouping of provenance records. Defining multiple provenance records groups is appropriate when several processings have been performed on data.

In the following example, two separated processings (`conversion` and `smoothing`) were performed on the data, resulting in two groups of provenance records.
```
└─ dataset
   └─ prov/
      ├─ prov-conversion_all.jsonld
      ├─ prov-smoothing_base.json
      ├─ prov-smoothing_soft.json
      ├─ prov-smoothing_ent.json
      └─ ...
```

### Suffixes

The following BIDS suffixes specify the contents of a provenance file.

!!! bug
    TODO: these suffixes might not be explicit enough.
    TODO: especially the `all`

<table>
  <tr>
   <td><strong>Suffix</strong>
   </td>
   <td><strong>File contents</strong>
   </td>
   <td><strong>File extension</strong>
   </td>
  </tr>
  <tr>
   <td><code>act</code>
   </td>
   <td>Activity records for the group of provenance
   </td>
   <td><code>.json</code>
   </td>
  </tr>
  <tr>
   <td><code>ent</code>
   </td>
   <td>Agent records for the group of provenance
   </td>
   <td><code>.json</code>
   </td>
  </tr>
  <tr>
   <td><code>env</code>
   </td>
   <td>Entity records for the group of provenance
   </td>
   <td><code>.json</code>
   </td>
  </tr>
  <tr>
   <td><code>soft</code>
   </td>
   <td>Software records for the group of provenance
   </td>
   <td><code>.json</code>
   </td>
  </tr>
  <tr>
   <td><code>base</code>
   </td>
   <td>Common parameters for the group of provenance (<code>BIDSProvVersion</code> and <code>@context</code>).
   <td><code>.json</code>
   </td>
   </td>
  </tr>
  <tr>
   <td><code>all</code>
   </td>
   <td>All records for the group of provenance records.
   </td>
   <td><code>.jsonld</code>
   </td>
  </tr>
</table>

## Provenance description levels

This section describes the places where BIDS-Prov metadata can be stored.

For further information about organization conventions, please consult the BIDS specification ([https://bids-specification.readthedocs.io](https://bids-specification.readthedocs.io)). Until these conventions are established in BIDS, it is RECOMMENDED to use the following.

BIDS-Prov metadata can be stored in different places:
* inside a top-level `prov/` directory;
* inside sidecar JSON files;
* inside the `dataset_description.json` file.

### `prov/` directory

BIDS-Prov files can be stored in a `prov/` directory immediately below the BIDS dataset (or BIDS-Derivatives dataset) root. At the dataset level, provenance can be about any BIDS file in the dataset.

Each BIDS-Prov file MUST meet the following naming convention. The `label` of the `prov` entity is arbitrary, `suffix` is one of listed in [Suffixes](#suffixes), and `extension` is either `json` or `jsonld`

```
prov/
  [<subdirectories>/]
    prov-<label>_<suffix>.<extension>
```

Here is an example:
```
└─ dataset
   ├─ prov/
   │  ├─ dcm2niix/
   │  │  └─ prov-dcm2niix_base.jsonld
   │  ├─ prov-preprocessing_base.json
   │  ├─ prov-preprocessing_soft.json
   │  └─ ...
   ├─ sub-001/
   ├─ sub-002/
   ├─ sub-003/
   ├─ ...
   └─ dataset_description.json
```

!!! warning
    When using `.json` files, the `@context` and `BIDSProvVersion` fields MUST be defined inside a `*_base.json` file, e.g.:
    ```JSON
    {
     "@context": "https://purl.org/nidash/bidsprov/context.json",
     "BIDSProvVersion": "0.0.1"
    }
    ```

### File level provenance

BIDS-Prov provenance metadata can be stored inside the sidecar JSON of any BIDS file (or BIDS-Derivatives file) it applies to.
In this case, the BIDS-Prov content only refers to the associated data file.

The sidecar JSON naming convention is already defined by BIDS. Here is an example dataset tree:
```
└─ example_dataset
   ├─ prov/
   │  └─ prov-dcm2niix_base.json
   ├─ sub-001/
   │  └─ ses-01/
   │     └─ anat/
   │        ├─ sub-001_ses-01_T1w.nii.gz
   │        └─ sub-001_ses-01_T1w.json
   ├─ sub-002/
   │  └─ ses-01/
   │     └─ anat/
   │        ├─ sub-002_ses-01_T1w.nii.gz
   │        └─ sub-002_ses-01_T1w.json
   ├─ ...
   └─ dataset_description.json
```

Inside the sidecar JSON, the `GenearatedBy` field must describe the `Activity` that generated the data file, with a reference to an existing `Id`:

```JSON
{
    "GeneratedBy": "bids::prov#conversion-00f3a18f",
}
```

Based on the same principle, the `SidecarGenearatedBy` field can be defined to describe the `Activity` that generated the sidecar JSON file.
If the `SidecarGenearatedBy` field is not defined, BIDS-Prov assumes that the sidecar JSON was generated by the `Activity` described in the `GenearatedBy` field.

No other field is allowed to describe provenance inside sidecar JSONs.

!!! warning
    When using sidecar JSON files to describe provenance, the `@context` and `BIDSProvVersion` fields MUST be defined inside a `prov/prov-<label>_base.json` file, e.g.:
    ```JSON
    {
     "@context": "https://purl.org/nidash/bidsprov/context.json",
     "BIDSProvVersion": "0.0.1"
    }
    ```

### Dataset level provenance - `dataset_description.json` file

!!! bug
    TODO: how do we know to which provenance group belongs the records in the `dataset_description.json`? (As no `prov` entity is used)

In the current version of the BIDS specification (1.10.0), the [`GeneratedBy`](https://bids-specification.readthedocs.io/en/stable/glossary.html#generatedby-metadata) field of the `dataset_description.json` files allows to specify provenance of the dataset.

BEP028 proposes that the following description replaces the `GeneratedBy` field as part of a major revision of the BIDS specification. Until this happens, BIDS-Prov provenance records can be stored in a `GeneratedByProv` field.

Here is an example of a `GeneratedByProv` field containing a complete description of an `Activity`:

```JSON
{
    "GeneratedByProv": {
        "Id": "bids::prov#conversion-00f3a18f",
        "Label": "Dicom to Nifti conversion",
        "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
        "AssociatedWith": {
            "Id": "bids::#dcm2niix-khhkm7u1",
            "AltIdentifier": "RRID:SCR_023517",
            "Label": "dcm2niix",
            "Version": "v1.0.20220720",
            "Used": {
                "Id": "bids::#fedora-uldfv058",
                "Label": "Fedora release 36 (Thirty Six)",
                "OperatingSystem": "GNU/Linux 6.2.15-100.fc36.x86_64"
            }
        }
    }
}
```

Here is an example of a `GeneratedByProv` field containing the IRI of an `Entity` described in another BIDS-Prov file:

```JSON
{
    "GeneratedByProv": "bids::prov#conversion-00f3a18f"
}
```

!!! warning
    When using provenance in `dataset_description.json` files, the `@context` and `BIDSProvVersion` fields MUST be defined inside a `*_base.json` file, e.g.:
    ```JSON
    {
     "@context": "https://purl.org/nidash/bidsprov/context.json",
     "BIDSProvVersion": "0.0.1"
    }
    ```

## Consistency of IRIs

BIDS-Prov recommends the following conventions in order to have consistent, human readable, and explicit [IRIs](https://www.w3.org/TR/json-ld11/#iris) as `Id` for provenance records objects. These principles also allow to identify where a record is described.

IRIs identifying `Activity`, `Agent`, and `Environment` provenance records inside files stored in a directory `<directory>` relatively to a BIDS dataset `<dataset>` SHOULD have the following form, where `<label>` is a human readable label for the record and `<uid>` is a unique group of chars:

```
bids:<dataset>:prov#<name>-<uid>
```

Here are a few naming examples:
* `bids:ds001734:prov#conversion-xfMMbHK1`: an `Activity` described inside the `ds001734` dataset;
* `bids::prov#fedora-uldfv058"`: an `Environment` described inside the current dataset.

IRI identifying `Entity` provenance records for a file `<file>` relatively to a BIDS dataset `<dataset>` SHOULD have the following form:

```
bids:<dataset>:<file>
```

Here are a few naming examples:
* `bids:ds001734:sub-002/anat/sub-02_T1w.nii`: an `Entity` describing a T1w file for subject `sub-002` in the `ds001734` dataset ;
* `bids:derivatives:fmriprep/sub-001/func/sub-001_task-MGT_run-01_bold_space-MNI152NLin2009cAsym_preproc.nii.gz`: an `Entity` describing a bold file for subject `sub-001` in the `derivatives` dataset.

Here is another example that considers the following dataset:

```
└─ dataset/
   ├─ sourcedata/
   │  └─ dicoms/
   │     └─ ...
   ├─ sub-001/
   │  └─ anat/
   │     ├─ sub-001_T1w.nii.gz
   │     └─ sub-001_T1w.json
   ├─ ...
   └─ prov/
      ├─ prov-dcm2niix_act.json
      ├─ prov-dcm2niix_base.json
      └─ prov-dcm2niix_soft.json
```

IRIs of provenance records defined in `prov/prov-dcm2niix_soft.json` should start with `bids:dataset:prov#` or `bids::prov#`.

```JSON
{
    "bids:dataset:prov#dcm2niix-70ug8pl5": {
        "Label": "dcm2niix",
        "Version": "v1.1.3"
    }
}
```

The previously described `Agent` can be referred to in the `prov/prov-dcm2niix_act.json` file:

```JSON
{
    "bids:dataset:prov#conversion-00f3a18f": {
        "Label": "Conversion",
        "Command": "dcm2niix -o . -f sub-%i/anat/sub-%i_T1w sourcedata/dicoms",
        "AssociatedWith": "bids:dataset:prov#dcm2niix-70ug8pl5"
    }
}
```

The previously described `Activity` can be referred to in the `sub-001/anat/sub-001_T1w.json` sidecar JSON file:

```JSON
{
    "GeneratedBy":"bids:dataset:prov#conversion-00f3a18f"
}
```

## Examples

A list of examples for BIDS-Prov are available in https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples

!!! bug
    TODO: merge to BIDS examples to bids-examples, and update links (or completely remove this part)

<table>
  <tr>
   <td><strong>Location</strong>
   </td>
   <td><strong>Description</strong>
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/simple_example/">simple_example/</a>
   </td>
   <td>A simple example describing the downsampling of EEG data using EEGLAB.
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/from_parsers/afni/">from_parsers/afni/</a>
   </td>
   <td>A set of examples for fMRI processing using AFNI. These where generated generated from ...
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/from_parsers/fsl/">from_parsers/fsl/</a>
   </td>
   <td>A set of examples for fMRI processing using FSL. These where generated generated from ...
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/from_parsers/spm/">from_parsers/spm/</a>
   </td>
   <td>A set of examples for fMRI processing using SPM. These where generated generated from ...
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/dcm2niix/">dcm2niix/</a>
   </td>
   <td>A set of examples describing dicom to nifti conversion using dcm2niix. These aim at showing different ways to organise the exact same provenance records inside a dataset:
    <ul>
        <li><code>dcm2niix_1</code>: all provenance records inside one JSON-LD file at dataset level.</li>
        <li><code>dcm2niix_4</code>: all provenance records inside several JSON files at dataset level, sidecar JSON use references to these files.</li>
    </ul>
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/heudiconv/">heudiconv/</a>
   </td>
   <td>An example describing dicom to nifti conversion using heudiconv.
   </td>
  </tr>

  <tr>
   <td><a href="https://github.com/bids-standard/BEP028_BIDSprov/tree/master/examples/nipype/">nipype/</a>
   </td>
   <td>An example describing simple processings on anatomical MRI using FSL through Nipype.
   </td>
  </tr>

</table>
