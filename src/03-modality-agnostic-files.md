# Modality agnostic files

## Dataset description

Templates:

-   `dataset_description.json`
-   `README`
-   `CHANGES`

### `dataset_description.json`

The file dataset_description.json is a JSON file describing the dataset. Every
dataset MUST include this file with the following fields:

| Field name         | Definition                                                                                                                                                                                                                           |
| ------------------------------------------------------------------------------| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Name               | REQUIRED. Name of the dataset.                                                                                                                                                                                                       |
| BIDSVersion        | REQUIRED. The version of the BIDS standard that was used.                                                                                                                                                                            |
| License            | RECOMMENDED. What license is this dataset distributed under? The use of license name abbreviations is suggested for specifying a license. A list of common licenses with suggested abbreviations can be found in Appendix II.        |
| Authors            | OPTIONAL. List of individuals who contributed to the creation/curation of the dataset.                                                                                                                                               |
| Acknowledgements   | OPTIONAL. Text acknowledging contributions of individuals or institutions beyond those listed in Authors or Funding.                                                                                                                 |
| HowToAcknowledge   | OPTIONAL. Text containing instructions on how researchers using this dataset should acknowledge the original authors. This field can also be used to define a publication that should be cited in publications that use the dataset. |
| Funding            | OPTIONAL. List of sources of funding (grant numbers).                                                                                                                                                                                |
| EthicsApprovals    | OPTIONAL. List of ethics committee approvals of the research protocols and/or protocol identifiers.                                                                                                                                  |                                                                                                                |
| ReferencesAndLinks | OPTIONAL. List of references to publication that contain information on the dataset, or links.                                                                                                                                       |
| DatasetDOI         | OPTIONAL. The Document Object Identifier of the dataset (not the corresponding paper).                                                                                                                                               |

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
  "EthicsApprovals": [
    "Army Human Research Protections Office (Protocol ARL-20098-10051, ARL 12-040, and ARL 12-041)"
  ],
  "ReferencesAndLinks": [
    "https://www.ncbi.nlm.nih.gov/pubmed/001012092119281",
    "Alzheimer A., & Kraepelin, E. (2015). Neural correlates of presenile dementia in humans. Journal of Neuroscientific Data, 2, 234001. http://doi.org/1920.8/jndata.2015.7"
  ],
  "DatasetDOI": "10.0.2.3/dfjj.10"
}
```

### `README`

In addition a free form text file (`README`) describing the dataset in more
details SHOULD be provided. The `README` file MUST be either in ASCII or UTF-8
encoding.

### `CHANGES`

Version history of the dataset (describing changes, updates and corrections) MAY
be provided in the form of a `CHANGES` text file. This file MUST follow the CPAN
Changelog convention:
[http://search.cpan.org/~haarg/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod](https://metacpan.org/pod/release/HAARG/CPAN-Changes-0.400002/lib/CPAN/Changes/Spec.pod).
The `CHANGES` file MUST be either in ASCII or UTF-8 encoding.

Example:

```Text
1.0.1 2015-08-27
  - Fixed slice timing information.

1.0.0 2015-08-17
  - Initial release.
```

## Participants file

Template:

```Text
participants.tsv
participants.json
```

The purpose of this RECOMMENDED file is to describe properties of participants
such as age, sex, handedness etc.
In case of single-session studies, this file has one compulsory column
`participant_id` that consists of `sub-<label>`, followed by a list of optional
columns describing participants.
Each participant MUST be described by one and only one row.

Commonly used *optional* columns in `participant.tsv` files are `age`, `sex`,
and `handedness`. We RECOMMEND to make use of these columns, and
in case that you do use them, we RECOMMEND to use the following values
for them:

-   `age`: numeric value in years (float or integer value)

-   `sex`: string value indicating phenotypical sex, one of "male", "female",
    "other"

    -   for "male", use one of these values: `male`, `m`, `M`, `MALE`, `Male`

    -   for "female", use one of these values: `female`, `f`, `F`, `FEMALE`,
      ` Female`

    -   for "other", use one of these values: `other`, `o`, `O`, `OTHER`,
        `Other`

-   `handedness`: string value indicating one of "left", "right",
    "ambidextrous"

    -   for "left", use one of these values: `left`, `l`, `L`, `LEFT`, `Left`

    -   for "right", use one of these values: `right`, `r`, `R`, `RIGHT`,
        `Right`

    -   for "ambidextrous", use one of these values: `ambidextrous`, `a`, `A`,
        `AMBIDEXTROUS`, `Ambidextrous`

Throughout BIDS you can indicate missing values with `n/a` (i.e., "not
available").

`participants.tsv` example:

```Text
participant_id age sex handedness group
sub-01 34 M right read
sub-02 12 F right write
sub-03 33 F n/a read
```

It is RECOMMENDED to accompany each `participants.tsv` file with a sidecar
`participants.json` file to describe the TSV column names and properties of their values (see also
the [section on tabular files](02-common-principles.md#tabular-files)).
Such sidecar files are needed to interpret the data, especially so when
optional columns are defined beyond `age`, `sex`, and `handedness`, such as
`group` in this example, or when a different age unit is needed (e.g., gestational weeks).
If no `units` is provided for age, it will be assumed to be in years relative to date of birth. 

`participants.json` example:

```JSON
{
    "age": {
        "Description": "age of the participant",
        "Units": "years"
    },
    "sex": {
        "Description": "sex of the participant as reported by the participant",
        "Levels": {
            "M": "male",
            "F": "female"
        }
    },    
    "handedness": {
        "Description": "handedness of the participant as reported by the participant",
        "Levels": {
            "left": "left",
            "right": "right"
        }
    },
    "group": {
        "Description": "experimental group the participant belonged to",
        "Levels": {
            "read": "participants who read an inspirational text before the experiment",
            "write": "participants who wrote an inspirational text before the experiment"
        }
    }
}
```

## Phenotypic and assessment data

Template:

```Text
phenotype/<measurement_tool_name>.tsv
phenotype/<measurement_tool_name>.json
```

Optional: Yes

If the dataset includes multiple sets of participant level measurements (for
example responses from multiple questionnaires) they can be split into
individual files separate from `participants.tsv`.

Each of the measurement files MUST be kept in a `/phenotype` directory placed
at the root of the BIDS dataset and MUST end with the `.tsv` extension.
File names SHOULD be chosen to reflect the contents of the file.
For example, the "Adult ADHD Clinical Diagnostic Scale" could be saved in a file
called `/phenotype/acds_adult.tsv`.

The files can include an arbitrary set of columns, but one of them MUST be
`participant_id` and the entries of that column MUST correspond to the subjects
in the BIDS dataset and `participants.tsv` file.

As with all other tabular data, the additional phenotypic information files
MAY be accompanied by a JSON file describing the columns in detail
(see [Tabular files](02-common-principles.md#tabular-files)).
In addition to the column description, a section describing the measurement tool
(as a whole) MAY be added under the name `MeasurementToolMetadata`.
This section consists of two keys:

  - `Description`: A free text description of the measurement tool
  - `TermURL`: A link to an entity in an ontology corresponding to this tool.

As an example, consider the contents of a file called
`phenotype/acds_adult.json`:

```JSON
{
  "MeasurementToolMetadata": {
    "Description": "Adult ADHD Clinical Diagnostic Scale V1.2",
    "TermURL": "http://www.cognitiveatlas.org/task/id/trm_5586ff878155d"
  },
  "adhd_b": {
    "Description": "B. CHILDHOOD ONSET OF ADHD (PRIOR TO AGE 7)",
    "Levels": {
      "1": "YES",
      "2": "NO"
    }
  },
  "adhd_c_dx": {
    "Description": "As child met A, B, C, D, E and F diagnostic criteria",
    "Levels": {
      "1": "YES",
      "2": "NO"
    }
  }
}
```

Please note that in this example `MeasurementToolMetadata` includes information
about the questionnaire and `adhd_b` and `adhd_c_dx` correspond to individual
columns.

In addition to the keys available to describe columns in all tabular files
(`LongName`, `Description`, `Levels`, `Units`, and `TermURL`) the
`participants.json` file as well as phenotypic files can also include column
descriptions with a `Derivative` field that, when set to true, indicates that
values in the corresponding column is a transformation of values from other
columns (for example a summary score based on a subset of items in a
questionnaire).

## Scans file

Template:

```Text
sub-<label>/[ses-<label>/]
    sub-<label>[_ses-<label>]_scans.tsv
```

Optional: Yes

The purpose of this file is to describe timing and other properties of each
imaging acquisition sequence (each run `.nii[.gz]` file) within one session.
Each `.nii[.gz]` file should be described by at most one row. Relative paths to
files should be used under a compulsory `filename` header. If acquisition time
is included it should be under `acq_time` header. Datetime should be expressed
in the following format `2009-06-15T13:45:30` (year, month, day, hour (24h),
minute, second; this is equivalent to the RFC3339 "date-time" format, time zone
is always assumed as local time). For anonymization purposes all dates within
one subject should be shifted by a randomly chosen (but common across all runs
etc.) number of days. This way relative timing would be preserved, but chances
of identifying a person based on the date and time of their scan would be
decreased. Dates that are shifted for anonymization purposes should be set to a
year 1925 or earlier to clearly distinguish them from unmodified data. Shifting
dates is RECOMMENDED, but not required.

Additional fields can include external behavioral measures relevant to the
scan. For example vigilance questionnaire score administered after a resting
state scan.

Example:

```Text
filename  acq_time
func/sub-control01_task-nback_bold.nii.gz 1877-06-15T13:45:30
func/sub-control01_task-motor_bold.nii.gz 1877-06-15T13:55:33
```

## Code

Template: `code/*`

Source code of scripts that were used to prepare the dataset (for example if it
was anonymized or defaced) MAY be stored here.<sup>1</sup> Extra care should be
taken to avoid including original IDs or any identifiable information with the
source code. There are no limitations or recommendations on the language and/or
code organization of these scripts at the moment.

<sup>1</sup>Storing actual source files with the data is preferred over links to
external source repositories to maximize long term preservation (which would
suffer if an external repository would not be available anymore).

## Provenance of BIDS datasets, files, and derivatives

Template:

```Text
- [Dataset level] prov.jsonld
- [File level] sub-<label>/[ses-<label>/]sub-<label>[_ses-<label>]_prov.jsonld
```

Optional: Yes

### Rationale
Interpreting and comparing scientific results and enabling reusable data and 
analysis output require understanding provenance, i.e. how the data were 
generated and processed. To be useful, the provenance must be understandable, 
easily communicated, and captured automatically in machine accessible form. 
Provenance records are thus used to encode transformations between 
digital objects. 

*Note:* Detailed provenance can be complex and imposing sufficiency will be 
use-case dependent. In this document, we will encode different levels of 
provenance requirements that a software can support.

Provenance can be captured using different mechanisms, but independent of 
encoding, always reflects transformations by either humans or software. The 
interpretability of provenance records requires a consistent vocabulary 
for provenance as well as an expectation for a consistent terminology 
for the objects being encoded. 

### Encoding Provenance In BIDS

i. Provenance information SHOULD be included in a BIDS dataset when possible.

ii. Provenance records MUST use the [PROV model](https://www.w3.org/TR/prov-o/) 
ontology and SHOULD be augmented by terms curated in the BIDS specification, 
the [NIDM](http://nidm.nidash.org/) model, and future enhancements to these models.

iii. If provenance records are included, these records of provenance of a dataset 
or a file MUST be described using a `[&lt;prefix>_]prov.jsonld` file. 
Since these [jsonld](https://json-ld.org/) documents are graph objects,
 they can be aggregated without the need to apply any inheritance principle. 

iv. The provenance file MAY be used to reflect the _provenance of a dataset, 
a collection of files or a specific file at any level_of the bids hierarchy. 

v. Provenance information SHOULD be anonymized/de-identified as necessary. 

### Examples of provenance in BIDS. 

1. The raw conversion from DICOM images or other instrument native formats 
to BIDS structure, details of stimulus presentation and cognitive paradigms, 
and clinical and neuropsychiatric assessments, each come with their 
own details of provenance.
   ```
    { "identifier": "sub-01/anat/..._T1.nii.gz",
      "type": "NIfTIGZ",
      "checksum": {"type": "sha512",
                   "value": "21231221ab4534..."
                  },
      "derivedFrom": ["sourcedata/12345-1.dcm", "sourcedata/12345-2.dcm"],
      "generatedBy": {"started": 2019-01-10T10:00:00"
                      "associatedWith": {"type": "softwareAgent",
                                         "name": "dcm2niix",
                                         "version": "2.0.0"},
                      "commandLine": "dcm2niix ..."
                      }
    }
   ```
2. In BIDS derivatives, the consideration of outputs requires knowledge of 
which inputs from the BIDS dataset were used together with what software was 
run in what environment and with what parameters.
   ```
    { "identifier": "derivatives/freesurfer/sub-01/mri/orig/001.mgz",
      "type": "MGZ",
      "checksum": {"type": "sha512",
                   "value": "121231221ab4534..."
                  },
      "derivedFrom": "sub-01/anat/..._T1.nii.gz",
      "generatedBy": {"started": 2019-01-10T10:00:00"
                      "associatedWith": {"type": "softwareAgent",
                                         "name": "FreeSurfer",
                                         "uri": "RRID:SCR_001847",
                                         "version": "6.0.0"},
                      "commandLine": "mri_convert ..."
                      }
    }
   ```
3. Provenance can involve information about people and institutions 
involved in a study.
   ```
    {
      "@context": "https://some/url/to/bids_context.jsonld",
      "identifier": "http://example.org/ds00000X",
      "generatedBy": {
        "type": "Project",
        "uri": "https://banda.mit.edu/",
        "startedAt": "2016-09-01T10:00:00",
        "wasAssociatedWith": { 
          "type": "Organization",
          "uri": "NIH",
          "role": "Funding"},
        },
      "wasAttributedTo": { 
         "type": "Person",
         "name": "Prof. Smith",
         "uri": "ORCID:0123",
         "role": "PI"}
       }
    }
   ```
4. Provenance records can highlight reuse of datasets while providing 
appropriate attribution to the original dataset generators as well as 
future transformers.  
5. For datasets and derivatives, provenance can also include details of 
why the data were collected in the first place covering hypotheses, claims, 
and prior publications. Provenance can encode support for which claims were 
supported by future analyses.

### Justification for Separating Provenance from file JSON

Provenance is information about a file, including any metadata that is relevant 
to the file itself. Thus any BIDS data file and its associated JSON sidecar
metadata together constitute a unique entity. As such, one may want to record 
the provenance of the JSON file as much as the provenance of the BIDS file. 
In addition, separating the provenance as a separate file for now, allows 
this to be an OPTIONAL component, and by encoding provenance as a JSON-LD 
document allows capturing the provenance as an individual record or 
multiple records distributed throughout the dataset.

### Possible places to encode provenance

**Dataset level provenance.** At the dataset level, provenance could be about 
the dataset itself, or about any entity in the dataset. This provenance may 
evolve as new data are added, which may include sourcedata, BIDS data, and 
BIDS derived data. One option is to make use of 
[named-graphs](https://www.w3.org/TR/json-ld11/#named-graphs).

In this example, with this `prov.jsonld` file we encode that the T1.mgz file 
was generated by version 6 of the FreeSurfer software.

```json
{
  "@context": "https://some/url/to/bids_context.jsonld",
  "identifier": "http://example.org/ds00000X",
  "generatedAt": "2020-01-10T10:00:00",
  "generatedBy": {
      "type": "Project",
      "uri": "https://banda.mit.edu/",
      "startedAt": "2016-09-01T10:00:00",
      "wasAssociatedWith": { "type": "Organization",
                             "uri": "NIH",
                             "role": "Funding"
                           }
    },
  "records": [
    { "identifier": "derivatives/freesurfer/sub-01/mri/orig/001.mgz",
      "type": "MGZ",
      "checksum": {"type": "sha512",
                   "value": "121231221ab4534..."
                  },
      "derivedFrom": "sub-01/anat/..._T1.nii.gz",
      "generatedBy": {"started": 2019-01-10T10:00:00"
                      "associatedWith": {"type": "softwareAgent",
                                         "name": "FreeSurfer",
                                         "uri": "RRID:SCR_001847",
                                         "version": "6.0.0"},
                      "commandLine": "mri_convert ..."
                      }
    }
  ]
}
```

**File level provenance.** This follows some of the same concepts at the dataset 
level, but is specifically about the current file under consideration.

```bash
sub-01/ 
    func/
        sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
        sub-01_task-xyz_acq-test1_run-1_prov.jsonld
...
```
```json
{
  "@context": "https://some/url/to/bids_context.jsonld",
  "generatedAt": "2020-01-10T10:00:00",
  "sha512": "1001231221ab4534...",
  "derivedFrom": "../../../sourcedata/sub-01/...dcm",
  "attributedTo": {
    "@type": "SoftwareAgent",
    "version": "1.3.0",
    "RRID": "RRID:SCR_017427",
    "label": "SPM",
    "description": "If this is a custom script, treat this as a methods section",
  }
}
```

The NIDM extensions (nidash.org)  to the PROV model would allow one to 
incorporate many aspects of the neuroimaging research workflow from data to 
results. This includes capturing who performed data collection, 
what software were used, what analyses were run, and what hardware and 
software resources (e.g., operating system and dependencies) were used.

### BIDS JSON-LD context

For most developers and users, the context will appear in the jsonld file as:

```json
{

  "@context": "https://some/url/to/bids_context.jsonld",`
  ...
}
```

Details of the context, will encode terminology that is consistent across BIDS 
and may itself involve separate context files. 
so `"https://some/url/to/bids_context.jsonld"` could look like:

```json
{

  "@context": ["https://some/url/to/bids_common_context.jsonld",
              "https://some/url/to/bids_derivates_context.jsonld",
              "https://some/url/to/bids_provenance_context.jsonld",
              ...
            ]
}
```

Contexts are created at the BIDS organization level, and only if necessary 
extended by a dataset. Thus most dataset creators will be able to reuse 
existing contexts. For terms, many of these are already in BIDS, with 
additional ones being curated by the NIDM-terms grant. Additionally, terms can 
and should be re-used from schema.org, bioschemas, and other ontologies and 
vocabularies whenever possible.

Example context: Common

[https://some/url/to/bids_common_context.jsonld]()
```json
{ 
  "@context": {
    "RepetitionTime": {
      "@id": "http://.../bids/RepetitionTime",
      "@type": "xsd:float",
      "hasUnit": "s"
    },
    ...
  }
}
```

Example context: Provenance

[https://some/url/to/bids_provenance_context.jsonld]()
```json
{ 
  "@context": {
    "generatedAt": {
      "@id": "http://www.w3.org/ns/prov#generatedAtTime",
      "@type": "http://www.w3.org/2001/XMLSchema#dateTime"
    },
    "attributedTo": {
      "@id": "http://www.w3.org/ns/prov#wasAttributedTo",
      "@type": "@id"
    },
    "derivedFrom": {
      "@id": "http://www.w3.org/ns/prov#wasDerivedFrom",
      "@type": "@id"
    },
    "RRID": {"@id": "https://schema.org/identifier", "@type": "@id"}
    "sha512": {"@id": "http://id.loc.gov/vocabulary/preservation/cryptographicHashFunctions/sha512", "@type": "@id"}
  },
    ...
}
```
<!----- Conversion time: 1.344 seconds.


Using this Markdown file:

1. Cut and paste this output into your source file.
2. See the notes and action items below regarding this conversion run.
3. Check the rendered output (headings, lists, code blocks, tables) for proper
   formatting and use a linkchecker before you publish this page.

Conversion notes:

* Docs to Markdown version 1.0β20
* Tue Mar 24 2020 09:07:42 GMT-0700 (PDT)
* Source doc: BIDS Extension Proposal XX (BEP0XX): Provenance
----->