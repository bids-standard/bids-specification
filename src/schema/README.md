# BIDS-schema

Portions of the BIDS specification are defined using YAML files, in order to
make the specification machine-readable.

Currently, the portions of the specification that rely on this schema are
the entity tables, entity definitions, filename templates, and metadata tables.
Any changes to the specification should be mirrored in the schema.

## The format of the schema

The schema is divided into two parts: the object definitions and the rules.

The object definitions (files in `objects/`) describe attributes of individual
objects or data types in the specification.
Common information in these files includes full names, descriptions, and
constraints on valid values.
These files **do not** describe how objects of different types
(for example file suffixes and file entities) interact with one another, or
whether objects are required in a given dataset or file.

The rules (files in `rules/`) describe how objects related to one another,
as well as their requirement levels.

## Object files

The types of objects currently supported in the schema are:

-   modalities,
-   datatypes,
-   entities,
-   suffixes,
-   metadata,
-   top-level files,
-   and non-BIDS associated directories.

Each of these object types has a single file in the `objects/` directory.

-   `modalities.yaml`: The modalities, or types of technology, used to acquire data in a BIDS dataset.
    These modalities are not reflected directly in the specification.
    For example, while both fMRI and DWI data are acquired with an MRI,
    in a BIDS dataset they are stored in different directories reflecting the two different `datatypes`.

-   `datatypes.yaml`: Data types supported by the specification.
    The only information provided in the file is:

    1.  a full list of valid BIDS datatypes
    1.  each datatype's full name
    1.  a free text description of the datatype.

-   `entities.yaml`: Entities (key/value pairs in directory and filenames).

-   `metadata.yaml`: All valid metadata fields that are explicitly supported in BIDS sidecar JSON files.

-   `columns.yaml`: All valid columns that are explicitly supported in BIDS TSV files.

-   `suffixes.yaml`: Valid file suffixes.

-   `top_level_files.yaml`: Valid top-level files which may appear in a BIDS dataset.

-   `associated_data.yaml`: Directories that may appear within a dataset directory without following BIDS rules.

### On re-used objects with different definitions

If an object may mean something different depending on where it is used within the specification,
then this must be reflected in the schema.
Specifically, each version of the object must have its own definition within the relevant file.
However, since object files are organized as dictionaries, each object must have a unique key.
Thus, we append a suffix to each re-used object's key in order to make it unique.
For objects with `CamelCase` names (for example, metadata fields), the suffix will start with a single underscore (`_`).
For objects with `snake_case` names, two underscores must be used.

There should also be a comment near the object definition in the YAML file describing the nature of the different objects.

For example, the TSV column `"reference"` means different things when used for EEG data, as compared to iEEG data.
As such, there are two definitions in `columns.yaml` for the `"reference"` column: `"reference__eeg"` and `"reference_ieeg"`.

```yaml
# reference column for channels.tsv files for EEG data
reference__eeg:
  name: reference
  description: |
    Name of the reference electrode(s).
    This column is not needed when it is common to all channels.
    In that case the reference electrode(s) can be specified in `*_eeg.json` as `EEGReference`).
  type: string
# reference column for channels.tsv files for iEEG data
reference__ieeg:
  name: reference
  description: |
    Specification of the reference (for example, 'mastoid', 'ElectrodeName01', 'intracranial', 'CAR', 'other', 'n/a').
    If the channel is not an electrode channel (for example, a microphone channel) use `n/a`.
  anyOf:
  - type: string
  - type: string
    enum:
    - n/a
```

When adding new object definitions to the schema,
every effort should be made to find a shared, common definition for the term, should it already exist.
If the differences between two versions of the same object are subtle or driven by context,
then you can generally _append_ additional text to the object definition within the associated rendered table in the specification,
rather than creating a separate entry in the schema.

### `modalities.yaml`

This file contains a dictionary in which each modality is defined.
Keys are modality abbreviations (for example, `mri` for magnetic resonance imaging),
and each associated value is a dictionary with two keys: `name` and `description`.

The `name` field is the full name of the modality.
The `description` field is a freeform description of the modality.

### `datatypes.yaml`

This file contains a dictionary in which each datatype is defined.
Keys are the directory names associated with each datatype (for example, `anat` for anatomical MRI),
and each associated value is a dictionary with two keys: `name` and `description`.

The `name` field is the full name of the datatype.
The `description` field is a freeform description of the datatype.

### `entities.yaml`

This file contains a dictionary in which each entity (key/value pair in filenames) is defined.
Keys are long-form versions of the entities, which are distinct from both the entities as
they appear in filenames _and_ their full names.
For example, the key for the "Contrast Enhancing Agent" entity, which appears in filenames as `ce-<label>`,
is `ceagent`.
These keys are also the recommended variable names for their associated entities in BIDS-compliant code,
since many entities (such as `ce`) have very short filename elements.
Each key's associated value is a dictionary with five keys:

-   `name`,
-   `entity`,
-   `description`,
-   `type`,
-   and either `format` or `enum`.

The `name` field is the full name of the entity. For example, the `name` for `ceagent` is "Contrast Enhancing Agent".

The `entity` field is the entity as it appears in filenames. For example, the `entity` for `ceagent` is `ce`.

The `description` field is a freeform description of the entity.
The description should apply to _all_ uses of the entity,
so if there is some additional information about the entity that applies specifically to a subset of suffixes or datatypes,
then that information should be provided in the specification, rather than the schema.

The `type` field defines the representation type for the value associated with the entity.
Given that all entities appear in filenames, they should all be strings and the `type` field should always be `string`.
This is true of both alphanumeric entities (such as `acq-desc`) and numeric ones (such as `run-1`).

The `format` field defines the specific format the value should take.
Entities are broadly divided into either `label` or `index` types.

When `format` is `index`, then the entity's associated value should be a non-zero integer, optionally with leading zeros.
For example, `run` should have an index, so a valid key-value pair in a filename would be `run-01`.

When `format` is `label`, then the value should be an alphanumeric string.
Beyond limitations on which characters are allowed, labels have few restrictions.
For example, `acq` should have a label, so a valid key-value pair might be `acq-someLabel`.

For a small number of entities, only certain labels are allowed.
In those cases, instead of a `format` field, there will be an `enum` field, which will provide a list of allowed values.

### `metadata.yaml`

This file contains definitions for all metadata fields (fields which may appear in sidecar JSON files)
currently supported in BIDS.

Entries in this file contain, at minimum, the following fields: `name`,
`description`, and a set of fields for describing the field's data type.

The data types include:

-   `type`, which MUST have a value of `array`,
-   `string`,
-   `integer`,
-   `number`,
-   `object`,
-   or `boolean`.

There are additional fields which may define rules that apply to a given type.

-   `array`: If `type` is `array`, then there MUST be an `items` field at
    the same level as `type`. `items` describes the data type and rules that
    apply to the individual items in the array. The same rules that apply to
    describing data types for the field itself apply to `items`.
    Additionally, there may be any of the following fields at the same level
    as `type`: `minItems`, `maxItems`.
    Here is an example of a field that MUST have three `integer` items:
    ```yaml
    ExampleField:
        name: ExampleField
        description: |
            The description of "ExampleField".
        type: array
        minItems: 3
        maxItems: 3
        items:
            type: integer
    ```

-   `string`: If `type` is `string`, then there MAY be any of the following
    fields at the same level as `type`: `pattern`, `format`, and `enum`.

    -   `pattern` defines a regular expression for valid string names.

    -   `format` defines the format for the string at the same level as `type`.
        Valid values for `format` include:

       -   `uri` (uniform resource identifiers),

       -   `date` (date-times),

       -   `unit` (standard units),

       -   `dataset_relative` (relative paths from dataset root),

       -   `participant_relative` (relative paths from participant directory).

    -   `enum` defines a list of valid values for the field.
        The minimum string length (`minLength`) defaults to 1.
        Here is an example of a field with a restricted set of possible values:
        ```yaml
        ExampleField:
            name: ExampleField
            description: |
                The description of "ExampleField".
            type: string
            enum:
                - PossibleValue1
                - PossibleValue2
        ```

-   `integer`: If `type` is `integer`, then there MAY be any of the
    following fields at the same level as `type`: `unit`,
    `minimum` (inclusive minimum), `maximum` (inclusive maximum),
    `exclusiveMinimum`, `exclusiveMaximum`.
    Here is an example of a field with a minimum value of 0:
    ```yaml
    ExampleField:
        name: ExampleField
        description: |
            The description of "ExampleField".
        type: integer
        minimum: 0
    ```

-   `number`: If `type` is `number`, then there MAY be any of the following
    fields at the same level as `type`: `unit`,
    `minimum` (inclusive minimum), `maximum` (inclusive maximum),
    `exclusiveMinimum`, `exclusiveMaximum`.
    Here is an example of a field with a minimum of 0, in units of
    kilometers per second:
    ```yaml
    ExampleField:
        name: ExampleField
        description: |
            The description of "ExampleField".
        type: number
        minimum: 0
        # k stands for "kilo", m stands for "meter", "/" means "per", and
        # s stands for "seconds"
        unit: km/s
    ```

-   `object`: If `type` is `object`, then there MAY be any of the following
    fields at the same level as `type`: `additionalProperties`,
    `properties`.
    Objects are defined as sets of key/value pairs.
    Keys MUST be strings, while values may have specific attributes,
    which is what `additionalProperties` describes.
    Here is an example of a field which MUST be an object,
    with one optional field named "OptionalField" that MUST be a `string`
    and any number of additional optional fields that MUST be `number`s.
    ```yaml
    ExampleField:
        name: ExampleField
        description: |
            The description of "ExampleField".
        type: object
        properties:
            OptionalField:
                type: string
        additionalProperties:
            type: number
    ```

-   `boolean`: If `type` is `boolean`, then the field's value MUST be one
    of: `true`, `false`. Here is an example:
    ```yaml
    ExampleField:
        name: ExampleField
        description: |
            The description of "ExampleField".
        type: boolean
    ```

Additionally, if multiple data types are possible for a given field
(for example, if a field may be a `number` or an `array` of `number`s),
then an `anyOf` field MUST be used, in which an array of data type
descriptions MUST be defined.
Here is an example of one such case:
```yaml
ExampleField:
    name: ExampleField
    description: |
        The description of "ExampleField".
    anyOf:
        - type: number
        - type: array
            items:
            type: number
```

Furthermore, if the data type description of a field is reused across fields,
then it may be defined in a separate field and referenced in each target field with the `$ref` keyword.
Here is an example of a field definition using `$ref`:
```yaml
ExampleField:
    name: ExampleField
    description: |
        The description of "ExampleField".
    $ref: _ReferenceField
```
The target field (`_ReferenceField` in this case) MUST be located in
the metadata YAML file, and MUST contain all information
that would be used to describe the field's data type otherwise.

Here is an example of a reference field:
```yaml
_ReferenceField:
    name: _ReferenceField
    description: |
        Description of "_ReferenceField".
    type: string
    enum:
        - PossibleValue1
        - PossibleValue2
```

The result of including `$ref` makes the `ExampleField` above equivalent to the following format:
```yaml
ExampleField:
    name: ExampleField
    description: |
        The description of "ExampleField".
    type: string
    enum:
        - PossibleValue1
        - PossibleValue2
```

### `columns.yaml`

This file contains definitions for all TSV columns currently supported in BIDS.

Entries in this file follow the same rules as `metadata.yaml`,
although column names appear in `snake_case`, rather than `CamelCase`.

### `suffixes.yaml`

This file contains a dictionary in which each suffix is defined.
Keys are the suffixes (for example, `T1w` for a T1-weighted image),
and each associated value is a dictionary with three keys: `name`, `description`, and (optionally) `unit`.

The `name` field is the full name of the suffix.
The `description` field is a freeform description of the type of data stored in files with the suffix.

The `unit` field describes units in which the data may appear.
When no `unit` field is present, data with that suffix is assumed to be in arbitrary units.
The `unit` field may use an `anyOf` keyword if multiple valid units are possible.

These entries may also, rarely, include fields defining the range or types of values that are valid for
files with the suffix.
For example, `MTRmap` files must have values between 0 and 100, since they represent percentages.

### `top_level_files.yaml`

This file contains a dictionary in which each top-level file is defined.
Keys are the filenames (without file extensions),
and each associated value is a dictionary with two keys: `name` and `description`.

The `name` field is the full name of the file.
The `description` field is a freeform description of the file.

### `associated_data.yaml`

This file contains a dictionary in which each non-BIDS directory is defined.
Keys are directory names, and each associated value is a dictionary with two keys: `name` and `description`.

The `name` field is the full name of the directory.
The `description` field is a freeform description of the directory.

## Rule files

The files in the `rules/` directory are less standardized than the files in `objects/`,
because rules governing how different object types interact in a valid dataset are more variable
than the object definitions.

-   `modalities.yaml`: This file simply groups `datatypes` under their associated modality.

-   `datatypes/*.yaml`: Files in the `datatypes` directory contain information about valid filenames within a given datatype.
    Specifically, each datatype's YAML file contains a list of dictionaries.
    Each dictionary contains a list of suffixes, entities, and file extensions which may constitute a valid BIDS filename.

-   `entities.yaml`: This file simply defines the order in which entities, when present, MUST appear in filenames.

-   `top_level_files.yaml`: Requirement levels and valid file extensions of top-level files.

-   `associated_data.yaml`: Requirement levels of associated non-BIDS directories.

### `modalities.yaml`

This file contains a dictionary in which each key is a modality abbreviation and the value is a dictionary with one key: `datatypes`.
The `datatypes` dictionary contains a list of datatypes that fall under that modality.

### `datatypes/*.yaml`

The files in this directory are currently the least standardized of any part of the schema.

Each file corresponds to a single `datatype`.
Within the file is a list of dictionaries.
Each dictionary corresponds to a group of suffixes that have the same rules regarding filenames.

The dictionaries have three keys: `suffixes`, `extensions`, and `entities`.

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
- suffixes:
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

- suffixes:
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
