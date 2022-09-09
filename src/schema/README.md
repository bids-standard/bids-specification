# BIDS-schema

Portions of the BIDS specification are defined using YAML files in order to
make the specification machine-readable.

Currently the portions of the specification that rely on this schema are
the entity tables, entity definitions, filename templates, and metadata tables.
Any changes to the specification should be mirrored in the schema.

## Organization and syntax

At the time of this writing, the schema has the following file layout:

    src/schema
    ├── BIDS_VERSION
    ├── meta
    │   └── context.yaml
    ├── objects
    │   ├── associated_data.yaml
    │   ├── ...
    │   └── top_level_files.yaml
    ├── rules
    │   ├── associated_data.yaml
    │   ├── checks
    │   │   ├── asl.yaml
    │   │   ├── ...
    │   │   └── mri.yaml
    │   ├── ...
    │   └── top_level_files.yaml
    └── SCHEMA_VERSION

The top-level organization includes `objects`, where terms are defined;
`rules`, where constraints (such as valid filenames or required metadata fields)
are defined;
and `meta`, where definitions useful for interpreting the schema are defined.

Each file is a YAML structure, most often an *object*.
To take an example, the file `rules/checks/mri.yaml` contains the contents:

```YAML
---
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

When we wish to refer to a file, we might write `rules/checks/mri.yaml`.
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

Many objects throughout the schema have `description` fields, which will typically be
rendered somewhere in the specification. Because the specification is written in
[Markdown](https://en.wikipedia.org/wiki/Markdown), these description fields may also
contain Markdown, including links to other locations in the specification.

Because the same description may be used in multiple locations, a mechanism is needed
to ensure that the correct path is discovered to render the description in each location.
To do this, the path should follow the form `SPEC_ROOT/path/within/source.md#anchor`.
For example, to link to the
[Definitions](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#definitions)
section of
[Common principles](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html),
use the path `SPEC_ROOT/02-common-principles.md#definitions`, e.g.,

    [Common principles - Definitions](SPEC_ROOT/02-common-principles.md#definitions)

Note that the Markdown extension `.md` MUST be used for this to render correctly.

For more information please see the following pull request and linked discussions:
[#1096](https://github.com/bids-standard/bids-specification/pull/1096)

### References

Some schema entries take the form:

    ObjectName:
      $ref: objects.metadata.OtherObjectName

This object may be *dereferenced* by replacing the `$ref` entry with the object being
referenced.
The following two prototypical examples are presented to clarify the semantics of
references (the cases in which they are used will be presented later):

1.  In `objects.metadata`:
    ```YAML
    _GeneticLevelEnum:
      type: string
      enum:
        - Genetic
        - Genomic
        - Epigenomic
        - Transcriptomic
        - Metabolomic
        - Proteomic

    GeneticLevel:
      name: GeneticLevel
      display_name: Genetic Level
      description: |
        Describes the level of analysis.
        Values MUST be one of `"Genetic"`, `"Genomic"`, `"Epigenomic"`,
        `"Transcriptomic"`, `"Metabolomic"`, or `"Proteomic"`.
      anyOf:
        - $ref: objects.metadata._GeneticLevelEnum
        - type: array
          items:
            $ref: objects.metadata._GeneticLevelEnum
    ```
    Here `_GeneticLevelEnum` is used to describe the valid values of `GeneticLevel`,
    and the references inside `GeneticLevel.anyOf` indicate that there may be a single
    such value or a list of values.

2.  In `rules.datatypes.derivatives.common_derivatives`:
    ```YAML
    anat_nonparametric_common:
      $ref: rules.datatypes.anat.nonparametric
      entities:
        $ref: rules.datatypes.anat.nonparametric.entities
        space: optional
        description: optional
    ```
    Here, the derivative datatype rule starts by copying the raw datatype rule
    `rules.datatypes.anat.nonparametric`. It then *overrides* the `entities` portion
    of that rule with a new object. To *extend* the original `entities`, it again
    begins by referencing `rules.datatypes.anat.nonparametric.entities`, and adding
    the new entities `space` and `description`.

### Expressions

In order to define a rule, we describe a limited language for boolean expressions,
that is, having values of `true` or `false`.
These expressions may be used as `selectors`, determining whether a rule applies,
or `checks`, determining whether a rule is satisfied.

Re-examining `rules.checks.mri.PhasePartUnits` from above:

```YAML
---
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

*   fields such as `modality`, `entities` (which has a `.part` subfield), `sidecar`
*   String literals such as `"mri"`, `"Units"` or `"rad"`
*   Lists containing fields or strings
*   Comparison operators such as `==` (equality) or `in` (subfield exists in field)
*   Functions such as `intersects()`

In fact, the full list of fields is defined in the `meta.context.context` object,
which (currently) contains at the top level:

*   `schema`: access to the schema itself
*   `dataset`: attributes of the whole dataset
*   `subject`: attributes of the current subject
*   `path`: the full path of the current file (relative to dataset root)
*   `entities`: an object of entities parsed from the path
*   `datatype`: the datatype, parsed from the path
*   `suffix`: the suffix, parsed from the path
*   `extension`: the file extension
*   `modality`: the file modality, determined by datatype
*   `sidecar`: the metadata values, accumulated by the inheritance principle
*   `associations`: associated files, discovered by the inheritance principle
*   `columns`: the columns in the current TSV file
*   `json`: the contents of the current JSON file
*   `nifti_header`: selected contents of the current NIfTI file's header

Some of these are strings, while others are nested objects.
These are to be populated by an *interpreter* of the schema, and provide the
*namespace* in which expressions are evaluated.

The following operators should be defined by an interpreter:

| Operator  | Definition                                                    | Example                                       |
| --------- | ------------------------------------------------------------- | --------------------------------------------- |
| `==`      | equality                                                      | `suffix == "T1w"`                             |
| `!=`      | inequality                                                    | `entities.task != "rest"`                     |
| `<`/`>`   | less-than / greater-than                                      | `sidecar.EchoTime < 0.5`                      |
| `<=`/`>=` | less-than-or-equal / greater-than-or-equal                    | `0 <= 4`                                      |
| `in`      | object lookup, true if RHS is a subfield of LHS               | `"Units" in sidecar`                          |
| `!`       | negation, true if the following value is false, or vice versa | `!true == false`                              |
| `&&`      | conjunction, true if both RHS and LHS are true                | `"Units" in sidecar && sidecar.Units == "mm"` |
| `\|\|`    | disjunction, true if either RHS or LHS is true                | `a < mn \|\| a > mx`                          |
| `.`       | object query, returns value of subfield                       | `sidecar.Units`                               |
| `[]`      | array index, returns value of Nth element (0-indexed) of list | `columns.participant_label[0]`                |

The following functions should be defined by an interpreter:

| Function                                 | Definition                                                                    | Example                                          | Note                                                                           |
| ---------------------------------------- | ----------------------------------------------------------------------------- | ------------------------------------------------ | ------------------------------------------------------------------------------ |
| `match(arg: str, pattern: str) -> bool`  | `true` if `arg` matches the regular expression `pattern` (anywhere in string) | `match(extension, ".gz$")`                       | True if the file extension ends with `.gz`                                     |
| `type(arg: Any) -> str`                  | The name of the type, including `"array"`, `"object"`, `"null"`               | `type(datatypes)`                                | Returns `"array"`                                                              |
| `intersects(a: array, b: array) -> bool` | `true` if arguments contain any shared elements                               | `intersects(dataset.modalities, ["pet", "mri"])` | True if either PET or MRI data is found in dataset                             |
| `length(arg: array) -> int`              | Number of elements in an array                                                | `length(columns.onset) > 0`                      | True if there is at least one value in the onset column                        |
| `count(arg: array, val: any)`            | Number of elements in an array equal to `val`                                 | `count(columns.type, "EEG")`                     | The number of times "EEG" appears in the column "type" of the current TSV file |
| `min(arg: array)`                        | The smallest non-`n/a` value in an array                                      | `min(sidecar.SliceTiming) == 0`                  | A check that the onset of the first slice is 0s                                |
| `max(arg: array)`                        | The largest non-`n/a` value in an array                                       | `max(columns.onset)`                             | The time of the last onset in an events.tsv file                               |

#### The special value `null`

Missing values in the context object have the special value `null`.
This value propagates through all of the above operations in a fully-defined,
hopefully intuitive way.
Most operations involving `null` simply resolve to `null`:

| Operation                | Result |
| ------------------------ | ------ |
| `sidecar.MissingValue`   | `null` |
| `null.anything`          | `null` |
| `null[0]`                | `null` |
| `null && true`           | `null` |
| `null \|\| true`         | `null` |
| `!null`                  | `null` |
| `match(null, pattern)`   | `null` |
| `intersects(list, null)` | `null` |
| `length(null)`           | `null` |
| `count(null, val)`       | `null` |
| `count(list, null)`      | `null` |
| `min(null)`              | `null` |
| `max(null)`              | `null` |

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
(for example file suffixes and file entities) interact with one another, or
whether objects are required in a given dataset or file.

### Overview

There are currently 11 sub-namespaces, which fall into five rough categories.
The namespaces are:

| Namespace                   | Description                                                                         | Group            |
| --------------------------- | ----------------------------------------------------------------------------------- | ---------------- |
| `objects.common_principles` | Terms that are used throughout BIDS                                                 | General terms    |
| `objects.modalities`        | Broad categories of data represented in BIDS, roughly matching recording instrument | General terms    |
| `objects.entities`          | Name-value pairs appearing in file names                                            | Name/value terms |
| `objects.metadata`          | Name-value pairs appearing in JSON files                                            | Name/value terms |
| `objects.columns`           | Column headings and values appearing in TSV files                                   | Name/value terms |
| `objects.datatypes`         | Subdirectories that organize files by type (e.g., `anat`, `eeg`)                    | Value terms      |
| `objects.suffixes`          | Filename suffixes that describe the contents of the file                            | Value terms      |
| `objects.extensions`        | Filename component that describe the format of the file                             | Value terms      |
| `objects.formats`           | Terms that define the forms values (for example, in metadata) might take            | Formats          |
| `objects.associated_data`   | Directories that may appear at the root of a dataset                                | Files            |
| `objects.top_level_files`   | Files that may appear at the root of a dataset                                      | Files            |

Because these objects vary, the contents of each namespace can vary.
Common fields to all objects:

| Field          | Description                                                                                                                                |
| -------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `display_name` | A human-friendly name, for tools to display; may include spaces                                                                            |
| `description`  | A description of the term that can be understood that should not depend on particular surrounding text; may contain markdown for rendering |

The name/value terms groups (`entities`, `metadata` and `columns`) define terms where
a name, when present, has a given meaning, and its value may be restricted. These objects
additionally have the field:

| Field    | Description                                                                                                                                                                                                   |
| -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `name`   | For terms that can take on multiple values (e.g., entities, metadata fields), the name of the term as it appears in the specification and in a dataset; must be alphanumeric; mutually exclusive with `value` |
| `type`   | The type (e.g., `string`, `integer`, `object`) of values the term describes                                                                                                                                   |
| `format` | The format of the term (defined in `objects.formats`)                                                                                                                                                         |

Value terms groups (`datatypes`, `suffixes`, `extensions`) define terms where a field
can take on multiple values. For example, a file has one datatype, as compared to a
collection of entities. These objects may have the fields:

| Field   | Description                                                                                              |
| ------- | -------------------------------------------------------------------------------------------------------- |
| `value` | For terms that cannot take on multiple values (e.g., suffixes, extensions), the string value of the term |

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

### On re-used objects with different definitions

In a few cases, two objects with the same name appear multiple times in the specification.
When this happens, it is preferred to find a common definition, and clarify it in the rules (see below).
However, in some cases, the object description and permissible values differ, and it needs to be defined
as two separate objects.
The following conventions are used:

1.  Each specific term takes on the form `<term>_<context>`, where `<term>` is the common name that
    the two (or more) terms share, `<context>` indicates when the specific term applies.
2.  If the `<term>` appears in `snake_case` (meaning it or similar objects may contain underscores),
    then `<context>` begins with an extra `_`.

For example, the TSV column `"reference"` means different things when used for EEG data, as compared to iEEG data.
As such, there are two definitions in `columns.yaml` for the `"reference"` column: `"reference__eeg"` and `"reference__ieeg"`.

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

#### Valid fields for definitions

1.  `objects.common_principles`
    | Field          | Description         |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

2.  `objects.modalities`
    | Field          |                     |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

3.  `objects.entities`

    | Field          |                                                         |
    | -------------- | ------------------------------------------------------- |
    | `display_name` | Human-friendly name                                     |
    | `description`  | Term definition                                         |
    | `name`         | Key of entity, such as `sub` or `ses`                   |
    | `type`         | Type of value (always `string`)                         |
    | `format`       | Permissible format of values, either `label` or `index` |
    | `enum`         | Exclusive list of valid values, if present              |

    Note that descriptions should apply to *all* uses of the entity; if additional information
    applies in certain contexts, that should be written in the specification, and not the schema.

4.  `objects.metadata`
    | Field          |                                                                                      |
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

5.  `objects.columns`
    | Field          |                                                                     |
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

6.  `objects.datatypes`
    | Field          |                            |
    | -------------- | -------------------------- |
    | `display_name` | Human-friendly name        |
    | `description`  | Term definition            |
    | `value`        | String value of `datatype` |

7.  `objects.suffixes`
    | Field          |                                                                |
    | -------------- | -------------------------------------------------------------- |
    | `display_name` | Human-friendly name                                            |
    | `description`  | Term definition                                                |
    | `value`        | String value of `suffix`                                       |
    | `unit`         | Interpretation of values in a data file with the given suffix  |
    | `maxValue`     | Maximum permissible value in a data file with the given suffix |
    | `minValue`     | Minimum permissible value in a data file with the given suffix |
    | `anyOf`        | Used to describe multiple permissible units                    |

8.  `objects.extensions`
    | Field          |                             |
    | -------------- | --------------------------- |
    | `display_name` | Human-friendly name         |
    | `description`  | Term definition             |
    | `value`        | String value of `extension` |

9.  `objects.formats`
    | Field          |                                    |
    | -------------- | ---------------------------------- |
    | `display_name` | Human-friendly name                |
    | `description`  | Term definition                    |
    | `pattern`      | Regular expression defining format |

10. `objects.associated_data`
    | Field          |                     |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

11. `objects.top_level_files`
    | Field          |                     |
    | -------------- | ------------------- |
    | `display_name` | Human-friendly name |
    | `description`  | Term definition     |

## Rule files

The files in the `rules/` directory are less standardized than the files in `objects/`,
because rules governing how different object types interact in a valid dataset are more variable
than the object definitions.

-   `modalities.yaml`: This file simply groups `datatypes` under their associated modality.

-   `datatypes/*.yaml`: Files in the `datatypes` directory contain information about valid filenames within a given datatype.
    Specifically, each datatype's YAML file contains a list of dictionaries.
    Each dictionary contains a list of suffixes, entities, and file extensions which may constitute a valid BIDS filename.

-   `sidecars/*.yaml`: Files in the `sidecars` directory contain information about valid JSON
    sidecar entries for files within a datatype.

-   `checks/*.yaml`: Files in the `checks` directory contain assertions on data, organized
    broadly by datatype, but not constrained.

-   `entities.yaml`: This file simply defines the order in which entities, when present, MUST appear in filenames.

-   `top_level_files.yaml`: Requirement levels and valid file extensions of top-level files.

-   `associated_data.yaml`: Requirement levels of associated non-BIDS directories.

### `modalities.yaml`

This file contains a dictionary in which each key is a modality abbreviation and the value is a dictionary with one key: `datatypes`.
The `datatypes` dictionary contains a list of datatypes that fall under that modality.

### `datatypes/*.yaml`

The files in this directory are currently the least standardized of any part of the schema.

Each file corresponds to a single `datatype`.
Within the file is a dictionary.
Each dictionary entry corresponds to a group of suffixes that have the same rules regarding filenames.
The key to each entry is a unique identifier for the group of suffixes, such as `meg` for general MEG-related suffixes.
The entry's corresponding value is a dictionary with four keys: `suffixes`, `extensions`, `datatypes`, and `entities`.

The `suffixes` entry is a list of file suffixes for which all of the extensions in the `extensions` entry
and all of the entity rules in the `entities` entry apply.

The `extensions` entry is a list of valid file extensions.

The `entities` entry is a dictionary in which the keys are entity names and the values are whether the entity is
required or optional for that suffix.
Any entities that are not present in this dictionary are not allowed in files with any of the suffixes in the group.
In rare occasions, there are restrictions on valid entity values
(for example, some suffixes may only allow an `acq` value of `calibration`).
In those cases, the entity's value will be another object, rather than a string indicating the requirement level.
This object will contain at least two keys: "requirement" and "type".

**NOTE**: The order in which entities appear in these dictionaries does not reflect how they should appear in filenames.
That information is present in `rules/entities.yaml`.

As an example, let us look at part of `meg.yaml`:

```yaml
meg:
  suffixes:
  - meg
  extensions:
  - .fif
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
  entities:
    subject: required
    session: optional
    acquisition:
      requirement: required
      type: string
      enum:
      - crosstalk
```

In this case, the first group has one suffix: `meg`.
The second group has the same suffix (`meg`), but describes different rules for files with that suffix.
While the valid extension is the same for both groups (`.fif`), the entities are not.

Specifically, files in the first group may have `task`, `run`, `processing`, and `split` entities,
while files in the second group may not.
Also, when files in the second group have the `acq` entity, the associated value MUST be `crosstalk`.

### `sidecars/*.yaml`

Sidecar files introduce the idea of "selectors" to determine whether a set of fields is added
to the sidecar schema that will be applied to the sidecar.
From here, the `fields` property lists will be accumulated to set requirement levels.
Rules that show up later in the document can override the rules that come before.
By default, fields take a requirement level, but the object can be expanded to include
level, additional level and description text for rendering the field in a table, and
issue codes and messages if more specific error messages are warranted.

```YAML
RuleName:
  selectors:
  - datatype == "anat"
  fields:
    MyField1: required
    MyField2:
      level: recommended
      level_addendum: Text to be added to the requirement level field.
      description_addendum: Text to be added to the description field.
      issue:
        code: ISSUE_CODE_STRING
        message: |
          Common message text users will see if the field is missing.

RuleNameOverride:
  selectors:
  - datatype == "anat"
  - suffix == "T1w"
  fields:
    MyField2:
      level: required
      issue:
        code: DIFFERENT_ISSUE_STRING
        message: |
          T1w images require MyField to be defined, so override
```

### `checks/*.yaml`

Check rules are similar to sidecar rules with selectors. These allow the issue field to
be placed at the top level, and introduce a list of `checks` or assertions that cause the
issue to fail if any evaluate to `False`.

```YAML
EventsMissing:
  issue:
    code: EVENTS_TSV_MISSING
    message: |
      Task scans should have a corresponding events.tsv file.
      If this is a resting state scan you can ignore this warning or rename the task to include the word "rest".
    severity: warning
  selectors:
  - entities contains "task"
  - not(entities.task contains "rest")  # Alternative for including the word "rest"
  checks:
  - associations contains "events"
```

Note that because we do not have requirement levels, severity must be explicitly specified.

Selectors and checks use the same expression syntax. The difference is that selectors determine
whether the rule is applied while checks determine whether it passes.

### `tabular_data/*.yaml`

Tabular data rules are essentially identical to sidecar rules, except that in place of fields
there are columns. Additional properties include `initial_columns` that shows a required
set (and order) of columns that should be the first in a table. The `additional_columns`
property can take values of `allowed`, `allowed_if_defined` and `not_allowed`.

```YAML
EEGChannels:
  selectors:
  - datatype == "eeg"
  - suffix == "channels"
  - extension == ".tsv"
  initial_columns:
  - name__channels
  - type__eeg_channels
  - units
  columns:
    name__channels: required
    type__eeg_channels: required
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

### `entities.yaml`

This file contains a list of entities in the order in which they must appear in filenames.

### `top_level_files.yaml`

This file contains a dictionary in which each key is a top-level file and the value is a dictionary with two keys:
`required` and `extensions`.
The `required` entry contains a boolean value (true or false) to indicate if that top-level file is required for BIDS datasets or not.
The `extensions` entry contains a list of valid file extensions for the file.

In cases where there is a data file and a metadata file, the `.json` extension for metadata file is included.

### `associated_data.yaml`

This file contains a dictionary in which each key is a directory and the value is a dictionary with one key: `required`.
The `required` entry contains a boolean value to indicate if that directory is required for BIDS datasets or not.

## Using links from a schema entry to places within the specification

Sometimes a particular metadata entry will refer to other concepts within the
BIDS specification using a link.
Currently, in order for these links to get properly rendered with the MkDocs structure,
they must be relative to the `src` directory of the bids-specification repository and
 need to be prefixed with `SPEC_ROOT`. Furthermore, they must point to the Markdown document;
that is, ending with `.md`, **not** `.html`.

For more information please see the following pull request and linked discussions:
[#1096](https://github.com/bids-standard/bids-specification/pull/1096)

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
