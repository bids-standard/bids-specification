# BIDS-schema

Portions of the BIDS specification are defined using YAML files, in order to
make the specification machine-readable.

Currently, the portions of the specification that rely on this schema are
the entity tables, entity definitions, filename templates, and metadata tables.
Any changes to the specification should be mirrored in the schema.

## The format of the schema

The schema reflects the files and objects in the specification, as well as
associations between these objects. Here is a list of the files and subfolders
of the schema, roughly in order of importance:

-   `datatypes/*.yaml`: Data types supported by the specification. Each datatype
    may support many suffixes. These suffixes are divided into groups based on
    what extensions and entities are allowed for each. Data types correspond to
    subfolders (for example, `anat`, `func`) in the BIDS structure.

-   `entities.yaml`: A list of entities (key/value pairs in folder and
    filenames) with associated descriptions and formatting rules. The order of
    the entities in the file determines the order in which entities must appear
    in filenames.

-   `top_level_files.yaml`: Modality-agnostic files stored at the top level of a
    BIDS dataset. The schema specifies whether these files are required or
    optional, as well as acceptable extensions for each.

-   `modalities.yaml`: Modalities supported by the specification, along with a
    list of associated data types. Modalities are not reflected directly in the
    BIDS structure, but data types are modality-specific.

-   `associated_data.yaml`: Folders that are commonly contained within the same
    folder as a BIDS dataset, but which do not follow the BIDS structure
    internally, such as `code` or `sourcedata`. The schema specifies which
    folders are accepted and whether they are required or optional.

-   `metadata/*.yaml`: Valid fields for sidecar metadata json files.
    These files contain, at minimum, the following fields: `name`,
    `description`, and a set of fields for describing the field's data type.

    The data types include `type`, which MUST have a value of
    `array`, `string`, `integer`, `number`, `object`, or `boolean`.
    There are additional fields which may define rules that apply to a given
    type.

    -   `array`: If `type` is `array`, then there MUST be an `items` field at
        the same level as `type`. `items` describes the data type and rules that
        apply to the individual items in the array. The same rules that apply to
        describing data types for the field itself apply to `items`.
        Additionally, there may be any of the following fields at the same level
        as `type`: `minItems`, `maxItems`.
        The minimum number of items (`minItems`) defaults to 1.
        Here is an example of a field that MUST have three `integer` items:
        ```yaml
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
        `pattern` defines a regular expression for valid string names.
        `format` defines the format for the string at the same level as `type`.
        Valid values for `format` include: `uri` (uniform resource
        identifiers), `date` (date-times), `unit` (standard units),
        `dataset_relative` (relative paths from dataset root),
        `participant_relative` (relative paths from participant folder).
        `enum` defines a list of valid values for the field.
        The minimum string length (`minLength`) defaults to 1.
        Here is an example of a field with a restricted set of possible values:
        ```yaml
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
    name: ExampleField
    description: |
        The description of "ExampleField".
    anyOf:
        - type: number
        - type: array
          items:
            type: number
    ```

    Finally, if the data type description of a field is reused across fields,
    then it may be defined in a separate file and referenced in the field's YAML
    file, with the `$ref` keyword.
    Here is an example of a field definition using `$ref`:
    ```yaml
    name: ExampleField
    description: |
        The description of "ExampleField".
    $ref: _ReferenceFile.yaml
    ```
    The target file (`_ReferenceFile.yaml` in this case) MUST be located in
    the same folder as the metadata YAML file, and MUST contain all information
    that would be used to describe the field's data type otherwise.

    Here is an example of a reference file:
    ```yaml
    name: _ReferenceFile
    description: |
        Description of "_ReferenceFile".
    type: string
    enum:
        - PossibleValue1
        - PossibleValue2
    ```

    The result of including `$ref` makes the `ExampleField` above equivalent
    to the following format:
    ```yaml
    name: ExampleField
    description: |
        The description of "ExampleField".
    type: string
    enum:
        - PossibleValue1
        - PossibleValue2
    ```
