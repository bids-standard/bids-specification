# BIDS schema description

Portions of the BIDS specification are defined using YAML files in order to
make the specification machine-readable.

Currently the portions of the specification that rely on this schema are:
-   the entity tables,
-   entity definitions,
-   filename templates,
-   metadata tables.

Any changes to the specification should be mirrored in the schema.

## Organization and syntax

At the time of this writing, the schema has the following file layout:

```plain
├── meta
│   ├── ...
│   └── versions.yaml
├── objects
│   ├── ...
│   └── suffixes.yaml
├── rules
│   ├── checks
│   │   ├── ...
│   │   └── references.yaml
│   ├── files
│   │   ├── common
│   │   │   ├── core.yaml
│   │   │   └── tables.yaml
│   │   ├── deriv
│   │   │   ├── imaging.yaml
│   │   │   └── preprocessed_data.yaml
│   │   └── raw
│   │       ├── ...
│   │       └── task.yaml
│   ├── sidecars
│   │   ├── derivatives
│   │   │   └── common_derivatives.yaml
│   │   ├── ...
│   │   └── pet.yaml
│   ├── tabular_data
│   │   ├── derivatives
│   │   │   └── common_derivatives.yaml
│   │   ├── ...
│   │   └── task.yaml
│   ├── ...
│   └── modalities.yaml
├── BIDS_VERSION
└── SCHEMA_VERSION
```

The top-level organization includes `objects`, where terms are defined;
`rules`, where constraints (such as valid filenames or required metadata fields)
are defined;
and `meta`, where definitions useful for interpreting the schema are defined.

Each file is made up of YAML data, most often an *object*.
For example, the file `rules/checks/mri.yaml` contains the contents:

```YAML
PhasePartUnits:
  issue:
    code: PHASE_UNITS
    message: |
      Phase images (with the `part-phase` entity) must have units
      "rad" or "arbitrary".
    level: error
  selectors:
    - modality == "mri"
    - entities.part == "phase"
    - '"Units" in sidecar'
  checks:
    - intersects([sidecar.Units], ["rad", "arbitrary"])
```

When we wish to refer to a file we might write `rules/checks/mri.yaml`.
Alternately, we can use `rules.checks.mri` to refer to the object contained by the
file.
Using this notation, the *qualified name*, the contents of an entire directory or a
portion of a file can be referred to unambiguously.
For example, the entire `rules/checks/` directory is referred to as `rules.checks`,
and `rules.checks.mri.PhasePartUnits.issue` refers to the object:

```JSON
{
  "code": "PHASE_UNITS",
  "message": "Phase images (with the `part-phase` [...]\n\"rad\" or \"arbitrary\".\n",
  "level": "error"
}
```

These qualified names may be used in this README, as well as in *references* and
*expressions*.

### Description formatting

Many objects throughout the schema have a `description` field,
which will typically be rendered somewhere in the specification.
Because the specification is written in [Markdown](https://en.wikipedia.org/wiki/Markdown),
these `description` fields may also contain Markdown,
including links to other locations in the specification.

Because the same description may be used in multiple locations,
a mechanism is needed to ensure that the correct path is discovered
to render the description in each location.
To do this, the path should follow the form `SPEC_ROOT/path/within/source.md#anchor`.
For example, to link to the
[Definitions](https://bids-specification.readthedocs.io/en/stable/common-principles.html#definitions)
section of
[Common principles](https://bids-specification.readthedocs.io/en/stable/common-principles.html),
use the path `SPEC_ROOT/common-principles.md#definitions`:

```Markdown
[Common principles - Definitions](SPEC_ROOT/common-principles.md#definitions)
```

Note that the Markdown extension `.md` MUST be used for this to render correctly.

For more information please see the following pull request and linked discussions:
[#1096](https://github.com/bids-standard/bids-specification/pull/1096)

### References

Some schema entries take the form:

```YAML
ObjectName:
  $ref: objects.metadata.OtherObjectName
```

This object may be *dereferenced* by replacing the `$ref` entry
with the object being referenced.
The following two prototypical examples are presented to clarify the semantics of
references (the cases in which they are used will be presented later):

1.  In `objects.enums`:
    ```YAML
    _GeneticLevelEnum:
      type: string
      enum:
        - $ref: objects.enums.Genetic.value
        - $ref: objects.enums.Genomic.value
        - $ref: objects.enums.Epigenomic.value
        - $ref: objects.enums.Transcriptomic.value
        - $ref: objects.enums.Metabolomic.value
        - $ref: objects.enums.Proteomic.value
    ```
    and in `objects.metadata`:
    ```YAML
    GeneticLevel:
      name: GeneticLevel
      display_name: Genetic Level
      description: |
        Describes the level of analysis.
        Values MUST be one of `"Genetic"`, `"Genomic"`, `"Epigenomic"`,
        `"Transcriptomic"`, `"Metabolomic"`, or `"Proteomic"`.
      anyOf:
        - $ref: objects.enums._GeneticLevelEnum
        - type: array
          items:
            $ref: objects.enums._GeneticLevelEnum
    ```
    Here `_GeneticLevelEnum` is used to describe the valid values of `GeneticLevel`,
    (which are in turn references to individual values), and the references inside `GeneticLevel.anyOf` indicate that there may be a single
    such value or a list of values.

1.  In [`rules.files.deriv.preprocessed_data`](./rules/files/deriv/preprocessed_data.yaml):
    ```YAML
    anat_nonparametric_common:
      $ref: rules.files.raw.anat.nonparametric
      entities:
        $ref: rules.files.raw.anat.nonparametric.entities
        space: optional
        description: optional
    ```
    Here, the derivative datatype rule starts by copying the raw datatype rule
    `rules.files.raw.anat.nonparametric`.
    It then *overrides* the `entities` portion of that rule with a new object.
    To *extend* the original `entities`, it again begins
    by referencing `rules.files.raw.anat.nonparametric.entities`,
    and adding the new entities `space` and `description`.

### Expressions

Rules definitions make use of a limited language of expressions that always evaluate to `true` or `false`.
These expressions may be used as `selectors`, determining whether a rule applies,
or `checks`, determining whether a rule is satisfied.

Re-examining `rules.checks.mri.PhasePartUnits` from above:

```YAML
PhasePartUnits:
  issue:
    code: PHASE_UNITS
    message: |
      Phase images (with the `part-phase` entity) must have units
      "rad" or "arbitrary".
    level: error
  selectors:
    - modality == "mri"
    - entities.part == "phase"
    - '"Units" in sidecar'
  checks:
    - intersects([sidecar.Units], ["rad", "arbitrary"])
```

We see expressions may contain:

-   fields such as `modality`, `entities` (which has a `.part` subfield), `sidecar`
-   String literals such as `"mri"`, `"Units"` or `"rad"`
-   Lists containing fields or strings
-   Comparison operators such as `==` (equality) or `in` (subfield exists in field)
-   Functions such as `intersects()`

In fact, the full list of fields is defined in the `meta.context` object,
which (currently) contains at the top level:

-   `schema`: access to the schema itself
-   `dataset`: attributes of the whole dataset
-   `subject`: attributes of the current subject
-   `path`: the full path of the current file (relative to dataset root)
-   `entities`: an object of entities parsed from the path
-   `datatype`: the datatype, parsed from the path
-   `suffix`: the suffix, parsed from the path
-   `extension`: the file extension
-   `modality`: the file modality, determined by datatype
-   `sidecar`: the metadata values, accumulated by the inheritance principle
-   `associations`: associated files, discovered by the inheritance principle
-   `columns`: the columns in the current TSV file
-   `json`: the contents of the current JSON file
-   `gzip`: the contents of the current file GZIP header
-   `nifti_header`: selected contents of the current NIfTI file's header
-   `ome`: the contents of the current OME-XML metadata
-   `tiff`: the contents of the current TIFF file's header

Some of these are strings, while others are nested objects.
These are to be populated by an *interpreter* of the schema,
and provide the *namespace* in which expressions are evaluated.

The following operators should be defined by an interpreter:

| Operator    | Definition                                                    | Example                                       |
| ----------- | ------------------------------------------------------------- | --------------------------------------------- |
| `==`        | equality                                                      | `suffix == "T1w"`                             |
| `!=`        | inequality                                                    | `entities.task != "rest"`                     |
| `<`/`>`     | less-than / greater-than                                      | `sidecar.EchoTime < 0.5`                      |
| `<=`/`>=`   | less-than-or-equal / greater-than-or-equal                    | `0 <= 4`                                      |
| `in`        | object lookup, true if RHS is a subfield of LHS               | `"Units" in sidecar`                          |
| `!`         | negation, true if the following value is false, or vice versa | `!true == false`                              |
| `&&`        | conjunction, true if both RHS and LHS are true                | `"Units" in sidecar && sidecar.Units == "mm"` |
| `\|\|`      | disjunction, true if either RHS or LHS is true                | `a < mn \|\| a > mx`                          |
| `.`         | object query, returns value of subfield                       | `sidecar.Units`                               |
| `[]`        | array/string index, returns value of Nth element (0-indexed)  | `columns.participant_label[0]`                |
| `+`         | numeric addition / string concatenation                       | `x + 1`, `stem + "suffix"`                    |
| `-`/`*`/`/` | numeric operators (division coerces to float)                 | `length(array) - 2`, `x * 2`, `1 / 2 == 0.5`  |

The following functions should be defined by an interpreter:

| Function                                        | Definition                                                                                                                                | Example                                                | Note                                                                           |
| ----------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `count(arg: array, val: any) -> int`            | Number of elements in an array equal to `val`                                                                                             | `count(columns.type, "EEG")`                           | The number of times "EEG" appears in the column "type" of the current TSV file |
| `exists(arg: str \| array, rule: str) -> int`   | Count of files in an array that exist in the dataset. String is array with length 1. See following section for the meanings of rules.     | `exists(sidecar.IntendedFor, "subject")`               | True if all files in `IntendedFor` exist, relative to the subject directory.   |
| `index(arg: array, val: any) -> int`            | Index of first element in an array equal to `val`, `null` if not found                                                                    | `index(["i", "j", "k"], axis)`                         | The number, from 0-2 corresponding to the string `axis`                        |
| `intersects(a: array, b: array) -> bool`        | `true` if arguments contain any shared elements                                                                                           | `intersects(dataset.modalities, ["pet", "mri"])`       | True if either PET or MRI data is found in dataset                             |
| `allequal(a: array, b: array) -> bool`          | `true` if arrays have the same length and paired elements are equal                                                                       | `intersects(dataset.modalities, ["pet", "mri"])`       | True if either PET or MRI data is found in dataset                             |
| `length(arg: array) -> int`                     | Number of elements in an array                                                                                                            | `length(columns.onset) > 0`                            | True if there is at least one value in the onset column                        |
| `match(arg: str, pattern: str) -> bool`         | `true` if `arg` matches the regular expression `pattern` (anywhere in string)                                                             | `match(extension, ".gz$")`                             | True if the file extension ends with `.gz`                                     |
| `max(arg: array) -> number`                     | The largest non-`n/a` value in an array                                                                                                   | `max(columns.onset)`                                   | The time of the last onset in an events.tsv file                               |
| `min(arg: array) -> number`                     | The smallest non-`n/a` value in an array                                                                                                  | `min(sidecar.SliceTiming) == 0`                        | A check that the onset of the first slice is 0s                                |
| `sorted(arg: array, method: str) -> array`      | The sorted values of the input array; defaults to type-determined sort. If method is "lexical", or "numeric" use lexical or numeric sort. | `sorted(sidecar.VolumeTiming) == sidecar.VolumeTiming` | True if `sidecar.VolumeTiming` is sorted                                       |
| `substr(arg: str, start: int, end: int) -> str` | The portion of the input string spanning from start position to end position                                                              | `substr(path, 0, length(path) - 3)`                    | `path` with the last three characters dropped                                  |
| `type(arg: Any) -> str`                         | The name of the type, including `"array"`, `"object"`, `"null"`                                                                           | `type(datatypes)`                                      | Returns `"array"`                                                              |

#### The `exists()` function

In various places, BIDS datasets may declare links between files.
In order to validate these links,
the `exists()` function returns a count of files that can be found within the dataset.
To accommodate the various ways of declaring these links,
the following rules are defined:

| `rule`       | Definition                                                                                                | Example                                                                               |
| ------------ | --------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------- |
| `"dataset"`  | A path relative to the root of the dataset.                                                               | `exists('participants.tsv', 'dataset')`                                               |
| `"subject"`  | A path relative to the current subject directory.                                                         | `exists('ses-1/anat/sub-01_ses-1_T1w.nii.gz', 'subject')`                             |
| `"stimuli"`  | A path relative to the `/stimuli` directory.                                                              | For `events.tsv`: `exists(columns.stim_file, 'stimuli') == length(columns.stim_file)` |
| `"file"`     | A path relative to the directory containing the current file.                                             | For `scans.tsv`: `exists(columns.filename, 'file') == length(columns.stim_file)`      |
| `"bids-uri"` | A URI of the form `bids:<dataset>:<relative-path>`. If `<dataset>` is empty, the current dataset is used. | `exists('bids::participants.tsv', 'bids-uri')`                                        |

#### The special value `null`

Missing values in the context object have the special value `null`.
This value propagates through all of the above operations in a fully-defined,
hopefully intuitive way.
Most operations involving `null` simply resolve to `null`:

| Operation                  | Result |
| -------------------------- | ------ |
| `sidecar.MissingValue`     | `null` |
| `null.anything`            | `null` |
| `null[0]`                  | `null` |
| `null && true`             | `null` |
| `null \|\| true`           | `null` |
| `!null`                    | `null` |
| `null + 1`                 | `null` |
| `null - 1`                 | `null` |
| `null * 1`                 | `null` |
| `null / 1`                 | `null` |
| `match(null, pattern)`     | `null` |
| `intersects(list, null)`   | `null` |
| `intersects(null, list)`   | `null` |
| `allequal(list, null)`     | `null` |
| `allequal(null, list)`     | `null` |
| `substr(null, 0, 1)`       | `null` |
| `substr(str, null, 1)`     | `null` |
| `substr(str, 0, null)`     | `null` |
| `length(null)`             | `null` |
| `count(null, val)`         | `null` |
| `count(list, null)`        | `null` |
| `index(null, val)`         | `null` |
| `index([0], null)`         | `null` |
| `index([], val)`           | `null` |
| `min(null)`                | `null` |
| `max(null)`                | `null` |
| `exists(null, "bids-uri")` | `null` |
| `exists("/path", null)`    | `null` |

The following operators have boolean results:

| Operation                | Result  | Comment                      |
| ------------------------ | ------- | ---------------------------- |
| `null == false`          | `false` |                              |
| `null == true`           | `false` |                              |
| `null != false`          | `true`  |                              |
| `null != true`           | `true`  |                              |
| `null == null`           | `true`  |                              |
| `null == 1`              | `false` | Also `<`, `>`, `<=` and `>=` |
| `"VolumeTiming" in null` | `false` |                              |

The `type()` function returns a string:

| Operation    | Result   |
| ------------ | -------- |
| `type(null)` | `"null"` |

Finally, if an expression (selector or check) evaluates to `null`,
the `null` will be interpreted equivalent to `false`.
That is, a `null` selector will not apply the current rule, and a `null`
check will fail.

## Object files

Object files define "objects" or "terms", which are semantic descriptions of
concepts used in BIDS. These reside under the `object.*` namespace in the schema.
These files **do not** describe how objects of different types
(for example file suffixes and file entities) interact with one another,
or whether objects are required in a given dataset or file.

### Overview

There are currently 12 sub-namespaces, which fall into five rough categories.

The namespaces are:

| Namespace                   | Description                                                                         | Group            |
| --------------------------- | ----------------------------------------------------------------------------------- | ---------------- |
| `objects.common_principles` | Terms that are used throughout BIDS                                                 | General terms    |
| `objects.modalities`        | Broad categories of data represented in BIDS, roughly matching recording instrument | General terms    |
| `objects.entities`          | Name-value pairs appearing in filenames                                             | Name/value terms |
| `objects.metadata`          | Name-value pairs appearing in JSON files                                            | Name/value terms |
| `objects.columns`           | Column headings and values appearing in TSV files                                   | Name/value terms |
| `objects.datatypes`         | Subdirectories that organize files by type (such as `anat`, `eeg`)                  | Value terms      |
| `objects.suffixes`          | Filename suffixes that describe the contents of the file                            | Value terms      |
| `objects.extensions`        | Filename component that describe the format of the file                             | Value terms      |
| `objects.formats`           | Terms that define the forms values (for example, in metadata) might take            | Formats          |
| `objects.files`             | Files and directories that may appear at the root of a dataset                      | Files            |
| `objects.enums`             | Full descriptions of enumerated values used in other sub-namespaces                 | Value terms      |

Because these objects vary, the contents of each namespace can vary.

Common fields to all objects:

| Field          | Description                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `description`  | A description of the term that can be understood that should not depend on particular surrounding text; may contain markdown for rendering |
| `display_name` | A human-friendly name, for tools to display; may include spaces                                                                            |

The name/value terms groups (`entities`, `metadata` and `columns`) define terms where
a name, when present, has a given meaning, and its value may be restricted.

These objects additionally have the field:

| Field    | Description                                                                                                                                                                                                     |
| -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | For terms that can take on multiple values (such as entities, metadata fields), the name of the term as it appears in the specification and in a dataset; must be alphanumeric; mutually exclusive with `value` |
| `type`   | The type (such as `string`, `integer`, `object`) of values the term describes                                                                                                                                   |
| `format` | The format of the term (defined in `objects.formats`)                                                                                                                                                           |

Value terms groups (`datatypes`, `suffixes`, `extensions`) define terms where a field
can take on multiple values.
For example, a file has one datatype, as compared to a collection of entities.

These objects may have the fields:

| Field   | Description                                                                                                      |
| ------- | ---------------------------------------------------------------------------------------------------------------- |
| `value` | For terms that cannot take on multiple values (for example suffixes or extensions), the string value of the term |

The `formats` terms provide one additional field:

| Field     | Description                                                 |
| --------- | ----------------------------------------------------------- |
| `pattern` | Regular expression validating a string rendering of a value |

#### Value constraints

For name/value terms, the `type` and `format` fields allow constraints to be placed on
the values described by the names.

Additional fields may apply to further constrain the type:

| Field                                  | Description                                   |
| -------------------------------------- | --------------------------------------------- |
| `maximum`/`minimum`/`exclusiveMinimum` | Value ranges for `integer` and `number` types |
| `maxValue`/`minValue`                  | Value ranges for `integer` and `number` types |
| `maxItems`/`minItems`                  | Size ranges for `array` types                 |
| `enum`                                 | List of accepted values for `string` types    |

Some values may be more flexible, allowing multiple possible values, or may be
arrays or objects:

| Field                  | Description                                                                                   |
| ---------------------- | --------------------------------------------------------------------------------------------- |
| `anyOf`                | A list of constraints, any of which could apply                                               |
| `items`                | The array described contains values whose types are constrained                               |
| `properties`           | The object described has a given set of fields; the values of these fields may be constrained |
| `additionalProperties` | The object described has constraints on its values, but not the names                         |

### On reused objects with different definitions

In a few cases, two objects with the same name appear multiple times in the specification.
When this happens, it is preferred to find a common definition, and clarify it in the rules (see below).
However, in some cases, the object description and permissible values differ, and it needs to be defined
as two separate objects.

Consider the following examples:

```yaml
# reference column for channels.tsv files for EEG data
reference__eeg:
  name: reference
  display_name: Electrode reference
  description: |
    Name of the reference electrode(s).
    This column is not needed when it is common to all channels.
    In that case the reference electrode(s) can be specified in `*_eeg.json` as `EEGReference`).
  type: string
# reference column for channels.tsv files for iEEG data
reference__ieeg:
  name: reference
  display_name: Electrode reference
  description: |
    Specification of the reference (for example, `mastoid`, `ElectrodeName01`, `intracranial`, `CAR`, `other`, `n/a`).
    If the channel is not an electrode channel (for example, a microphone channel) use `n/a`.
  anyOf:
    - type: string
    - type: string
      enum:
        - n/a
```

Here, the TSV column `"reference"` means different things when used for EEG data,
as compared to iEEG data, so two definitions are needed.
Because columns use `snake_case` (meaning they can be expected to contain underscores),
two underscores are needed to separate the column name from the string that indicates the use of the term.

The convention can be summed up in the following rules:

1.  Each specific term takes on the form `<term>_<context>`, where `<term>` is the common name that
    the two (or more) terms share, `<context>` indicates when the specific term applies.

1.  If the `<term>` appears in `snake_case` then `<context>` begins with an extra `_`.

#### Valid fields for definitions by sub-namespace

-   `objects.common_principles`
    | Field          | Description         |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

-   `objects.modalities`
    | Field          | Description         |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

-   `objects.entities`

    | Field          | Description                                             |
    | -------------- | ------------------------------------------------------- |
    | `display_name` | Human-friendly name                                     |
    | `description`  | Term definition                                         |
    | `name`         | Key of entity, such as `sub` or `ses`                   |
    | `type`         | Type of value (always `string`)                         |
    | `format`       | Permissible format of values, either `label` or `index` |
    | `enum`         | Exclusive list of valid values, if present              |

    Note that descriptions should apply to *all* uses of the entity; if additional information
    applies in certain contexts, that should be written in the specification, and not the schema.

-   `objects.metadata`
    | Field          | Description                                                                          |
    | -------------- | ------------------------------------------------------------------------------------ |
    | `display_name` | Human-friendly name                                                                  |
    | `description`  | Term definition                                                                      |
    | `name`         | Name of field in JSON object (in `CamelCase`)                                        |
    | `unit`         | Interpretation of numeric values                                                     |
    | `type`         | Type of value (one of `array`, `string`, `integer`, `number`, `object` or `boolean`) |
    | `format`       | Permissible format of values, from definitions in `objects.formats`                  |
    | `enum`         | Exclusive list of valid values, if present                                           |
    | `maximum`      | Maximum for numeric values                                                           |
    | `minimum`      | Minimum for numeric values                                                           |
    | `*`            | JSON-schema fields to further constrain values                                       |

-   `objects.columns`
    | Field          | Description                                                         |
    | -------------- | ------------------------------------------------------------------- |
    | `display_name` | Human-friendly name                                                 |
    | `description`  | Term definition                                                     |
    | `name`         | Name of column in TSV file (in `snake_case`)                        |
    | `unit`         | Interpretation of numeric values                                    |
    | `type`         | Type of value                                                       |
    | `format`       | Permissible format of values, from definitions in `objects.formats` |
    | `pattern`      | Regular expression constraining string values                       |
    | `enum`         | Exclusive list of valid values, if present                          |
    | `maximum`      | Maximum for numeric values                                          |
    | `minimum`      | Minimum for numeric values                                          |
    | `*`            | JSON-schema fields to further constrain values                      |

-   `objects.datatypes`
    | Field          | Description                |
    | -------------- | -------------------------- |
    | `display_name` | Human-friendly name        |
    | `description`  | Term definition            |
    | `value`        | String value of `datatype` |

-   `objects.suffixes`
    | Field          | Description                                                    |
    | -------------- | -------------------------------------------------------------- |
    | `display_name` | Human-friendly name                                            |
    | `description`  | Term definition                                                |
    | `value`        | String value of `suffix`                                       |
    | `unit`         | Interpretation of values in a data file with the given suffix  |
    | `maxValue`     | Maximum permissible value in a data file with the given suffix |
    | `minValue`     | Minimum permissible value in a data file with the given suffix |
    | `anyOf`        | Used to describe multiple permissible units                    |

-   `objects.extensions`
    | Field          | Description                 |
    | -------------- | --------------------------- |
    | `display_name` | Human-friendly name         |
    | `description`  | Term definition             |
    | `value`        | String value of `extension` |

-   `objects.formats`
    | Field          | Description                        |
    | -------------- | ---------------------------------- |
    | `display_name` | Human-friendly name                |
    | `description`  | Term definition                    |
    | `pattern`      | Regular expression defining format |

-   `objects.files`
    | Field          | Description                                                                          |
    | -------------- | ------------------------------------------------------------------------------------ |
    | `display_name` | Human-friendly name                                                                  |
    | `description`  | Term definition                                                                      |
    | `file_type`    | Indicator that the file is a regular file (`"regular"`) or directory (`"directory"`) |

-   `objects.enums`
    | Field          | Description            |
    | -------------- | ---------------------- |
    | `display_name` | Human-friendly name    |
    | `description`  | Term definition        |
    | `value`        | String value of `enum` |

## Rule files

The `rules.*` namespace contains most of the validatable content of the schema,
apart from value constraints that can be encoded in `objects`.

There are several types of rule, and this section is subject to reconsolidation as
patterns are found.

### Core concepts

Core concepts are [expressions](#expressions) (defined above), requirement levels and issues.

#### Requirement levels and severity

BIDS follows RFC 2119 and has three requirement levels: OPTIONAL, RECOMMENDED and REQUIRED.
In the schema, we use `optional`, `recommended` and `required`.

A rule interpreter (validator) is expected to treat:
-   missing REQUIRED data/metadata as an error,
-   missing RECOMMENDED data/metadata as a warning,
-   and silently pass over missing OPTIONAL data.

BIDS also defines a level `DEPRECATED`, rendered in the schema as `deprecated`,
and corresponding to a warning if the data/metadata is present.

#### Issues

Issues are messages intended to be communicated to a dataset curator to indicate an issue
with their dataset.

They have a code and severity as well:

| Field     | Description                                    |
| --------- | ---------------------------------------------- |
| `code`    | Issue identifier, such as `EVENTS_TSV_MISSING` |
| `level`   | Issue severity (`warning` or `error`)          |
| `message` | Message for display to a user                  |

A level of `warning` corresponds to a rule in the specification that is RECOMMENDED,
while a level of `error` corresponds to a rule that is REQUIRED.

In some cases, an issue is contained next to a `level: required` or `level: recommended`
as part of a larger rule.
In these cases, the `level` field should be omitted from the issue
to avoid duplication or conflict.

### Filename construction rules

A significant portion of BIDS is devoted to the naming of files,
and almost all filenames consist of entities, a suffix, an extension, and a data type.
Exceptions will be noted below.

`rules.files` contains the following subdivisions.

| Namespace                   | Description                                                                               |
| --------------------------- | ----------------------------------------------------------------------------------------- |
| `rules.files.common.core`   | Files and directories that reside at the top level of datasets                            |
| `rules.files.common.tables` | Tabular metadata files that associate metadata with entities                              |
| `rules.files.raw.*`         | Raw data and metadata files that have entities, suffixes, datatypes and extensions        |
| `rules.files.deriv.*`       | Derivative data and metadata files that have entities, suffixes, datatypes and extensions |

#### Core files and directories

`rules.files.common.core` describes files that have little-to-no variability in their form.
These either have a single `path` field, or a `stem` field and a list of `extensions`:

| Field        | Description                                                                                                   |
| ------------ | ------------------------------------------------------------------------------------------------------------- |
| `level`      | Requirement level of file, one of (`optional`, `recommended`, `required`, `deprecated`)                       |
| `path`       | Location of file, relative to dataset root; mutually exclusive with `stem` and `extensions`                   |
| `stem`       | Name of file, relative to dataset root, up to but not including the extension; mutually exclusive with `path` |
| `extensions` | List of valid extension strings, including the initial dot (`.`); mutually exclusive with `path`              |

These are the entries for `dataset_description.json` and `README`:

```YAML
dataset_description:
  level: required
  path: dataset_description.json
README:
  level: required
  stem: README
  extensions:
    - ''
    - .md
    - .rst
    - .txt
```

Here, `README` and `README.md` are both valid, while only `dataset_description.json` is permitted.

#### Tabular metadata files

`rules.files.common.tables` describes TSV files and their associated metadata,
including `participants.tsv`, `samples.tsv`, `*_sessions.tsv` and `*_scans.tsv`.
The first two use the `stem` field, while the latter two specify the entities used
to construct the filename.

The valid fields are:

| Field        | Description                                                                                                       |
| ------------ | ----------------------------------------------------------------------------------------------------------------- |
| `level`      | Requirement level of file, one of (`optional`, `recommended`, `required`, `deprecated`)                           |
| `stem`       | Name of file, relative to dataset root, up to but not including the extension; mutually exclusive with `entities` |
| `entities`   | Object where the keys are entries in `objects.entities`. The value is a requirement level.                        |
| `extensions` | List of valid extension strings, including the initial dot (`.`)                                                  |

For example:

```YAML
participants:
  level: optional
  stem: participants
  extensions:
    - .tsv
    - .json
sessions:
  suffixes:
    - sessions
  extensions:
    - .tsv
    - .json
  entities:
    subject: required
```

Note that these files do not have a `datatype`, but otherwise follow the same rules as above.

#### BIDS filenames

`rules.files.raw` and `rules.files.deriv` contain series of related rules.
These are largely grouped by datatype, but file types that appear in multiple locations may be grouped together.

The files described take the form:

```plain
[sub-<label>/][ses-<label>/]<datatype>/<entities>_<suffix><extension>
```

Rules have the following fields:

| Field        | Description                                                                                                                                     |
| ------------ | ----------------------------------------------------------------------------------------------------------------------------------------------- |
| `suffixes`   | List of suffixes found in `objects.suffixes`                                                                                                    |
| `extensions` | List of valid extension strings, including initial dot (`.`)                                                                                    |
| `datatypes`  | List of datatypes found in `objects.datatypes`                                                                                                  |
| `entities`   | Object where the keys are entries in `objects.entities`. The value is either a requirement level or an object described by the following table. |

| Field    | Requirement level | Description                                                                              |
| -------- | ----------------- | ---------------------------------------------------------------------------------------- |
| `level`  | REQUIRED          | Requirement level of field, one of (`optional`, `recommended`, `required`, `deprecated`) |
| `format` | OPTIONAL          | Override of entity field - Permissible format of values, either `label` or `index`       |
| `enum`   | OPTIONAL          | Override of entity field - Exclusive list of valid values, if present                    |

As an example, let us look at a (modified) part of `meg.yaml`:

```yaml
meg:
  suffixes:
    - meg
  extensions:
    - .fif
  datatypes:
    - meg
  entities:
    subject: required
    session: optional
    task: required
    acquisition: optional
    run: optional
    processing: optional
    split: optional

crosstalk:
  suffixes:
    - meg
  extensions:
    - .fif
  datatypes:
    - meg
  entities:
    subject: required
    session: optional
    acquisition:
      level: required
      enum:
        - crosstalk
```

In this case, the first group has one suffix: `meg`.
The second group has the same suffix (`meg`), but describes different rules for files with that suffix.
While the valid extension is the same for both groups (`.fif`), the entities are not.

Specifically, files in the first group may have `task`, `run`, `processing`, and `split` entities,
while files in the second group may not.
Also, when files in the second group have the `acq` entity, the associated value MUST be `crosstalk`.

A common derivatives type is preprocessed data, where the type of the generated data is the same
as the input data.
BIDS Derivatives specifies that these files may be distinguished from raw data
with the new entities `space-<label>` or `desc-<label>`.

This rule is encoded:

```yaml
meg_meg_common:
  $ref: rules.files.raw.meg.meg
  entities:
    $ref: rules.files.raw.meg.meg.entities
    space: optional
    description: optional
```

When expanded, this becomes:

```yaml
meg_meg_common:
  suffixes:
    - meg
  extensions:
    - .fif
  datatypes:
    - meg
  entities:
    subject: required
    session: optional
    task: required
    acquisition: optional
    run: optional
    processing: optional
    split: optional
    space: optional
    description: optional
```

### Sidecar and tabular data rules

Tabular data and JSON sidecar files follow a similar pattern:

|      | Name          | Value         |
| ---- | ------------- | ------------- |
| JSON | field         | value         |
| TSV  | column header | column values |

In the specification, groups of fields/columns are described together in a table
that includes the name of the field/column, the requirement level and a description.
The definitions, including name and description, appear in `objects.metadata`,
and the columns appear in `objects.columns`.

Here, we define YAML "tables" that can be rendered in the specification. These
take the form:

```YAML
RuleName:
  selectors:
    - expression1
    - expression2
  fields:
    - FieldName1:
        level: recommended
        level_addendum: required if XYZ
        description_addendum: Additional text following object description.
    - FieldName2: optional

RuleNameReq:
  selectors:
    - expression1
    - expression2
    - expression3
  fields:
    - FieldName1:
        level: required
        issue:
          code: ISSUE_NAME
          message: A description of the problem for a user
```

Here we show an example of two fields, one that is RECOMMENDED in most cases
but REQUIRED in another, the other of which is OPTIONAL.

`selectors` indicate whether the current rule applies to a given file.
This is not rendered in the text, but may be used by a validator.
`fields` is an object with keys that appear in `objects.metadata`/`objects.columns`.
If the value is a string, then it is a requirement level.
If it is an object, then the it has the following fields

| Field                  | Requirement level | Description                                                                              |
| ---------------------- | ----------------- | ---------------------------------------------------------------------------------------- |
| `level`                | REQUIRED          | Requirement level of field, one of (`optional`, `recommended`, `required`, `deprecated`) |
| `level_addendum`       | OPTIONAL          | Additional text to describe cases where requirement level changes                        |
| `description_addendum` | OPTIONAL          | Additional text to follow the `objects.metadata.<fieldname>.description`                 |
| `issue`                | OPTIONAL          | [issue object](#issues), if additional communication is warranted                        |

The second table implements the change in the first table's `level_addendum`.
The `expression3` selector indicates the additional case where the more stringent
rule is applied.

#### Valid fields for definitions

1.  `rules.sidecars.*`

    | Field       | Description                                                                                              |
    | ----------- | -------------------------------------------------------------------------------------------------------- |
    | `selectors` | List of expressions; any evaluating false indicate rule does not apply                                   |
    | `fields`    | Object with keys that may be found in `objects.metadata`, values either a requirement level or an object |

1.  `rules.tabular_data.*`

    | Field                | Description                                                                                                    |
    | -------------------- | -------------------------------------------------------------------------------------------------------------- |
    | `selectors`          | List of expressions; any evaluating false indicate rule does not apply                                         |
    | `columns`            | Object with keys that may be found in `objects.columns`, values either a requirement level or an object        |
    | `initial_columns`    | An optional list of columns that must be the first N columns of a file                                         |
    | `index_columns`      | An optional list of columns that uniquely identify a row.                                                      |
    | `additional_columns` | Indicates whether additional columns may be defined. One of `allowed`, `allowed_if_defined` and `not_allowed`. |

The following tables demonstrate how mutual exclusive, required fields,
may be set in `rules.sidecars.*`:

```YAML
MRIFuncRepetitionTime:
  selectors:
    - modality == "mri"
    - datatype == "func"
    - '!("VolumeTiming" in sidecar)'
    - match(extension, "^\.nii(\.gz)?$")
  fields:
    RepetitionTime:
      level: required
      level_addendum: mutually exclusive with `VolumeTiming`

MRIFuncVolumeTiming:
  selectors:
    - modality == "mri"
    - datatype == "func"
    - '!("RepetitionTime" in sidecar)'
    - match(extension, "^\.nii(\.gz)?$")
  fields:
    VolumeTiming:
      level: required
      level_addendum: mutually exclusive with `RepetitionTime`
```

An additional check will be required to assert that both are not present,
but these tables may be combined for rendering purposes.

Here we present an example rule in `rules.tabular_data.eeg`:

```YAML
EEGChannels:
  selectors:
  - datatype == "eeg"
  - suffix == "channels"
  - extension == ".tsv"
  initial_columns:
  - name__channels
  - type__channels
  - units
  columns:
    name__channels: required
    type__channels: required
    units: required
    description: optional
    sampling_frequency: optional
    reference: optional
    low_cutoff: optional
    high_cutoff: optional
    notch: optional
    status: optional
    status_descriptions: optional
  additional_columns: allowed_if_defined
```

### Checks

`rules.checks` can contain more complex rules. Structurally, these are similar to sidecar rules,
in that they have selectors.
They additionally have a `checks` list, and an explicit issue.

| Field       | Description                                                                                    |
| ----------- | ---------------------------------------------------------------------------------------------- |
| `issue`     | Issue code object (see [Issues](#issues)                                                       |
| `selectors` | List of expressions; any evaluating false indicate rule does not apply                         |
| `checks`    | List of expressions; any evaluating false indicate rule is violated and issue should be raised |

```YAML
EventsMissing:
  issue:
    code: EVENTS_TSV_MISSING
    message: |
      Task scans should have a corresponding events.tsv file.
      If this is a resting state scan you can ignore this warning or rename the task to include the word "rest".
    level: warning # could be an error with the proper selectors, I think
  selectors:
    - '"task" in entities'
    - '!match(entities.task, "rest")'
    - suffix != "events"
  checks:
    - '"events" in associations'
```

### Ordering rules

-   `rules.entities` - This file contains a list of keys into `objects.entities` and
    simply defines the order in which entities, when present, MUST appear in filenames

-   `rules.common_principles` - This file contains a list of terms that appear in `objects.common_principles`
    that determines the order they appear in the specification

### One-off rules

-   `rules.modalities` - The keys in this file are the modalities, the values objects with the following field:

    | Field       | Description                           |
    | ----------- | ------------------------------------- |
    | `datatypes` | List of datatypes mapping to modality |

-   `rules.dataset_metadata` - These are similar to `rules.sidecars.*`, for JSON files at the root level.
    This is likely to go away in favor of other approaches.

-   `rules.errors` - This file describes errors that cannot be expressed in the schema. This provides common
    codes and language that implementing validators can use to ensure the same problems are reported to
    users in the same way.

## Version of the schema

File `SCHEMA_VERSION` in the top of the directory contains a semantic
version (`MAJOR.MINOR.PATCH`) for the schema (how it is organized).
Note that while in `0.` series, breaking changes are
permitted without changing the `MAJOR` (leading) component of the version.
Going forward, the 2nd, `MINOR` indicator should be
incremented whenever schema organization introduces "breaking changes":
changes which would cause existing tools reading schema to
adjust their code to be able to read it again.
Additions of new components to the schema should increment the last,
`PATCH`, component of the version so that tools could selectively
enable/disable loading specific components of the schema.
With the release of `1.0.0` version of the schema,
we expect that the `MAJOR` component
will be incremented whenever schema organization introduces "breaking changes",
`MINOR` - when adding new components to the schema,
and `PATCH` - when fixing errors in existing components.

## Schema publication

The BIDS Schema is compiled into a single, dereferenced object during
the ReadTheDocs build of the specification.
This object is published as a JSON document that can be found at `/schema.json`
at the root of the specification.
For example, the schema used to construct the 1.8.0 release of BIDS can be found at
<https://bids-specification.readthedocs.io/en/v1.8.0/schema.json>,
and the latest version that includes unreleased changes to BIDS and the schema may
be found at <https://bids-specification.readthedocs.io/en/latest/schema.json>.

The JSON version of the schema contains `schema_version` and `bids_version` keys
that identify the state of both the schema and the specification at the time it was
compiled.

## Metaschema

The `metaschema.json` file is a meta-schema that uses the JSON Schema language to
formalize the allowable directories, files, fields and values of the BIDS schema,
ensuring consistency across the entire schema directory. Validation of the schema is
incorporated into the CI, so any changes that are inconsistent will be flagged before
inclusion.
