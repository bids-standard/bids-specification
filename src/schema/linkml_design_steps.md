# Phase 1 Implementation Steps

## Step 1.1: Scaffold the LinkML schema with enums and base types

Create `src/schema/bids_metaschema.yaml` with:
- Prefixes and schema metadata (id, name, license)
- `RequirementLevel` enum: `required`, `recommended`, `optional`, `deprecated`
- `FormatType` enum: all 17 values from current metaschema
- `IssueSeverity` enum: `error`, `warning`
- `GeneralTerm` class: slots `display_name` (required string), `description` (required string)

## Step 1.2: Model the `objects.*` sub-namespaces

- `ValueTerm` (extends `GeneralTerm`): add `value` (required string) — covers `datatypes`, `extensions`
- `Suffix` (extends `GeneralTerm` + `value`): add optional `unit`, `anyOf`, `maxValue`, `minValue`
- `NameValueTerm` (extends `GeneralTerm`): add `name` (required string), `type`, `format`, `enum`
  with JSON Schema constraint fields (`maximum`, `minimum`, `anyOf`, `items`, `properties`, `additionalProperties`)
- `Entity`: NameValueTerm with required `format`
- `MetadataField`: NameValueTerm + `unit`, `recommended`
- `Column`: NameValueTerm + optional `definition` object, `unit`
- `Format`: GeneralTerm + required `pattern`
- `FileObject`: GeneralTerm + required `file_type`
- `EnumValue`: GeneralTerm + `value` + optional `tags`
- Container classes: `ObjectsCollection` tying them together with keyed maps

## Step 1.3: Model the `rules.*` types

- `Issue`: `code` (string), `message` (string), optional `level` (IssueSeverity)
- `SuffixRule`: `suffixes`, `extensions`, `entities` (map of entity to requirement), optional `datatypes`, `level`, `selectors`
- `PathRule`: `path`, `level`
- `StemRule`: `stem`, `extensions`, `level`, optional `datatypes`, `selectors`
- `SidecarRule`: `selectors`, `fields` (map of field name to requirement level or object with level/addendum/issue)
- `TabularDataRule`: `selectors`, `columns`, `additional_columns`, optional `initial_columns`, `index_columns`
- `CheckRule`: `selectors`, `checks`, `issue`
- Container classes for `rules.files`, `rules.sidecars`, `rules.tabular_data`, `rules.checks`

## Step 1.4: Model the `meta.*` types

- `Association`: `target` (with `entities`, `suffix`, `extension`), optional `selectors`, `inherit`
- `Context`: keep as free-form (JSON Schema embedded)
- `ExpressionTest`: `expression` (string), `result` (any)
- Ordering lists (`rules.entities`, `rules.common_principles`, `rules.metaentities`): string arrays

## Step 1.5: Wire up the top-level `BidsSchema` class

- Slots: `meta`, `objects`, `rules`, `bids_version` (string), `schema_version` (string)

## Step 1.6: Validate round-trip

- `linkml gen-json-schema bids_metaschema.yaml > /tmp/generated_metaschema.json`
- `uv run bst export > /tmp/schema.json`
- `check-jsonschema --schemafile /tmp/generated_metaschema.json /tmp/schema.json`
- Compare against `check-jsonschema --schemafile src/metaschema.json /tmp/schema.json`
- Iterate until parity
