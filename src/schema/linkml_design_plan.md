# LinkML Metaschema Conversion — Plan

## Current State

| Layer | Current approach |
|-------|-----------------|
| **Metaschema** | `src/metaschema.json` — 742 lines of JSON Schema defining the shape of the BIDS schema |
| **Schema data** | ~90 YAML files under `src/schema/` organized as `meta/`, `objects/`, `rules/` |
| **Validation** | `bidsschematools.schema.get_schema_validator()` validates compiled schema against metaschema via `jsonschema` |
| **Python types** | `Namespace` dict-like wrapper — no real classes, no type safety |
| **TypeScript** | `jsr-dist` orphan branch uses `json-schema-to-typescript` to auto-generate types from JSON Schema |
| **LinkML tools** | Local repos at `/home/yoh/proj/misc/linkml/` for reference; install from PyPI via `uv pip install linkml` |

## Scope

**We are only replacing the metaschema** (`src/metaschema.json` → LinkML).
The BIDS schema YAML files under `src/schema/` themselves are not being modified.
The `$ref` conventions, expression DSL, and overall schema structure stay as-is.

## Key Challenges

1. **The BIDS metaschema isn't a typical data model.** It describes a schema-about-schemas. Some parts (e.g., `objects.metadata`, `objects.columns`) embed inline JSON Schema fragments (`type`, `anyOf`, `items`, `properties`, `additionalProperties`). LinkML will need to model this without losing expressiveness.

2. **No `$ref` in scope.** The BIDS schema YAML files use a custom `$ref` convention, but these are fully dereferenced during compilation (`bst export`). The metaschema validates the **compiled** JSON output, which contains no `$ref` fields. The LinkML metaschema has no need to model `$ref` at all.

3. **Expressions language.** `selectors` and `checks` are string-based DSL expressions. These are opaque strings from the metaschema's perspective — LinkML just needs to declare them as string lists, but long-term there may be value in formalizing them.

4. **Heterogeneous rule shapes.** File rules (`pathRule`, `stemRule`, `suffixRule`), sidecar rules, tabular data rules, and check rules all have different shapes. These map well to LinkML classes with inheritance.

## Phase 1: Modeling — Create the LinkML schema (`bids_metaschema.yaml`)

The core work. Translate the concepts in `metaschema.json` into LinkML:

- **Top-level class**: `BidsSchema` (with slots for `meta`, `objects`, `rules`, `bids_version`, `schema_version`)

- **Object term types** as a class hierarchy:
  - `GeneralTerm` (base: `display_name`, `description`)
  - `NameValueTerm` extends `GeneralTerm` (adds `name`, `type`, `format`, `enum`, etc.)
    - **`Entity`** — NameValueTerm with required `format` (label/index)
    - **`MetadataField`** — NameValueTerm with JSON Schema value constraints, `unit`, `recommended`
    - **`Column`** — NameValueTerm with optional `definition` (JSON object), `unit`, `format`
  - `ValueTerm` extends `GeneralTerm` (adds `value`)
    - **`Suffix`** — ValueTerm with optional `unit`, `anyOf`, `maxValue`, `minValue`
    - **`Datatype`** — plain ValueTerm
    - **`Extension`** — plain ValueTerm
  - Independent classes (not subclasses of NameValue/Value):
    - **`Format`** — GeneralTerm + required `pattern`
    - **`FileObject`** — GeneralTerm + required `file_type`
    - **`EnumValue`** — GeneralTerm + `value` + optional `tags`

- **Rule types** as another hierarchy:
  - `FileRule` (base for `PathRule`, `StemRule`, `SuffixRule`)
  - `SidecarRule`, `TabularDataRule`, `CheckRule`
  - `Issue`, `RequirementLevel` (enum)

- **Meta types**: `Association`, `Context` (can remain as embedded JSON Schema)

## Why the generated JSON Schema needs post-processing

LinkML's JSON Schema generator (`gen-json-schema`) produces valid JSON Schema from the
LinkML model, but the BIDS metaschema relies heavily on a pattern that LinkML does not
natively express: **maps with arbitrary string keys and typed values**.
In JSON Schema this is `"additionalProperties": {"$ref": "#/$defs/SomeClass"}`.

The post-processing script `patch_metaschema.py` bridges this gap.
The 43 patches fall into six categories:

### Category 1: Simple typed maps (16 patches)

Pattern: a slot whose value is `{arbitrary_key: TypedValue}`.

Example: `ObjectsSection.entities` is a JSON object where every key is an entity name
(like `"subject"`, `"session"`) and every value conforms to the `Entity` class.
LinkML generates `"type": ["string", "null"]` for the slot (since it has no explicit range);
the patch replaces this with `"type": "object", "additionalProperties": {"$ref": "#/$defs/Entity"}`.

Affected slots: `ObjectsSection.columns`, `.datatypes`, `.entities`, `.enums`, `.extensions`,
`.files`, `.formats`, `.metadata`, `.metaentities`, `.modalities`, `.suffixes`,
`.common_principles`; `RulesSection.dataset_metadata`, `.errors`, `.modalities`;
`MetaSection.associations`.

### Category 2: Nested maps (9 patches)

Pattern: two levels of arbitrary keys, `{groupName: {ruleName: TypedValue}}`.

Example: `rules.checks` is `{anat: {T1wFileWithTooManyDimensions: CheckRule, ...}, ...}`.
The patch builds nested `additionalProperties`.

Affected: `MetaSection.templates`, `RulesSection.checks`, `.directories`, `.json`,
`.sidecars`, `.tabular_data`; `FileRulesSection.common`, `.raw`, `.deriv`.

### Category 3: Union-valued maps (4 patches)

Pattern: a map where values can be either a plain string enum or an object.

Example: `SuffixRule.entities` maps entity names to either a `RequirementLevel` string
(`"required"`, `"optional"`) or an `EntityOverride` object (`{level: "required", enum: [...]}`).
The patch uses `anyOf` in the `additionalProperties`.

Affected: `SuffixRule.entities`, `SidecarRule.fields`, `TabularDataRule.columns`,
`Template.entities`.

### Category 4: Open classes (8 patches)

LinkML generates `"additionalProperties": false` by default, but some BIDS classes embed
arbitrary JSON Schema properties (for example, `MetadataField` can have `items`, `properties`,
`additionalProperties`, and other JSON Schema keywords not enumerated in the class definition).
The patch removes the `"additionalProperties": false` constraint from these classes.

Affected: `MetadataField`, `Column`, `NameValueTerm`, `Suffix`, `EnumValue`, `ValueTerm`,
`DirectoryEntry`, `Template`.

### Category 5: Slot type coercions (5 patches)

Individual slots that need type flexibility beyond what LinkML expresses:

- `MetaSection.context` — the value is an arbitrary JSON Schema object (the context definition)
- `AssociationTarget.extension` — can be a string or an array of strings
- `ExpressionTest.result` — can be any JSON value (string, number, null, boolean, etc.)
- `DirectoryEntry.subdirs` — array items can be strings or objects (with `oneOf`)
- `JsonSchema` — the entire class is an open container for any JSON Schema fragment

### Category 6: Root reference (1 patch)

Sets `$ref` to `BidsSchema` so the schema validates the top-level object.
This is already handled by `tree_root: true` in the LinkML model, but `gen-json-schema`
does not emit a top-level `$ref` currently.

### LinkML `extra_slots` — implemented using PR 2940

LinkML's [`extra_slots`](https://linkml.io/linkml-model/dev/docs/extra_slots/) feature
maps to JSON Schema `additionalProperties`.
Using the draft implementation from linkml/linkml#2940
(`sneakers-the-rat/linkml@jsonschema-extra`), we have adopted `extra_slots` throughout
the BIDS metaschema:

```yaml
# Generates: "additionalProperties": {"anyOf": [{"$ref": "#/$defs/Entity"}, {"type": "null"}]}
EntityMap:
  extra_slots:
    range_expression:
      range: Entity

# Generates: "additionalProperties": true
MetadataField:
  extra_slots:
    allowed: true

# Generates: "additionalProperties": {"anyOf": [{$ref: RequirementLevel}, {$ref: EntityOverride}, ...]}
EntityRequirementMap:
  extra_slots:
    range_expression:
      any_of:
        - range: RequirementLevel
        - range: EntityOverride
```

**Results**: The patch script has been reduced from **43 patches to 8**:
- Categories 1-4 (35 patches) are fully handled by `extra_slots`
- Category 5 (5 slot-level type coercions) still requires patches
- Category 6 (root `$ref`) still requires a patch
- Special: sidecars/tabular_data derivatives nesting (2 patches) — heterogeneous
  depth that cannot be expressed with simple `extra_slots`

**29 wrapper classes** were added to model the typed maps:
- 13 simple map classes (Category 1): `EntityMap`, `ColumnMap`, etc.
- 12 nested map classes (Category 2): `CheckRuleGroupMap` → `CheckRuleMap`, etc.
- 3 union map classes (Category 3): `EntityRequirementMap`, `FieldRequirementMap`, `TemplateEntityMap`
- 1 open map class: `EnumMap` (mixed EnumValue/PrivateEnum values)

### Divergences to report against PR 2940

1. **Spurious `{type: null}` in `additionalProperties`**: When `extra_slots` has a
   `range_expression` pointing to a class, the generated `additionalProperties` wraps
   the reference in `anyOf: [{$ref: X}, {type: null}]`. The null alternative is incorrect
   for map values — it means map values can be null, which is not the intent. The fix
   would be to call `get_subschema_for_slot(..., include_null=False)` in
   `get_additional_properties()` (line 714 of `jsonschemagen.py`).

   This does NOT cause validation failures (the BIDS schema has no null map values),
   but it makes the schema less strict than intended.

2. **No issue with `allowed: true`**: Classes using `extra_slots: {allowed: true}` correctly
   generate `additionalProperties: true`.

3. **`any_of` in `range_expression` works correctly**: Union-valued maps like
   `EntityRequirementMap` generate the expected `anyOf` with all alternatives, plus
   the spurious null from issue #1.

## Phase 2: Validation continuity — Generate JSON Schema from LinkML

- Use `gen-json-schema bids_metaschema.yaml | python patch_metaschema.py` to produce
  the final JSON Schema
- Verify it validates the compiled BIDS schema. The existing tooling already has what we need:
  - `check-jsonschema` (already a test dependency) can validate `schema.json` against a schema file
  - `bidsschematools` uses `jsonschema` library with `get_schema_validator()` — we just swap the metaschema source
  - Concretely: `uv run bst export > /tmp/schema.json && check-jsonschema --schemafile generated_metaschema.json /tmp/schema.json`
- Compare coverage/strictness with current `metaschema.json`
- Iterate on the LinkML model until parity is achieved

## Phase 3: Python code generation

- Use `linkml gen-python` (or `gen-pydantic`) to produce typed Python classes
- Integrate into `bidsschematools` — replace the `Namespace` dict approach with proper dataclass loading
- **Namespace boundary consideration**: The `Namespace` class (`tools/schemacode/.../types/namespace.py`) provides recursive `.attribute` access during compilation/dereferencing. The generated typed classes need to either:
  - Support the same attribute-style access (Pydantic models and dataclasses do this natively), or
  - Serve as the "outer shell" with `Namespace` still used internally for the parts of the schema not described by the metaschema (e.g., the free-form JSON Schema fragments inside `objects.metadata` values)
- The schema loading path (`load_schema()` → dereference → validate) would return typed objects instead of nested dicts

## Phase 4: TypeScript code generation

- Use `linkml gen-typescript` to produce TypeScript interfaces
- Replace the current `json-schema-to-typescript` approach in `jsr-dist`
- No runtime library needed — the generated interfaces are pure type definitions with zero runtime dependencies, which is exactly what `jsr-dist` needs to type the compiled `schema.json`

## Phase 5: CI and documentation

- Replace `check-metaschema` pre-commit hook with LinkML-based validation
- Update `src/schema/README.md` (note: this README is part of the Sphinx docs for bidsschematools, so updates need to be consistent with that documentation build)
- Ensure `bst export-metaschema` outputs the generated JSON Schema for backwards compatibility

## Class Hierarchy Diagram

A Mermaid class diagram visualizing the 35 data model classes, 3 enums,
inheritance, and composition relationships is available in
[`class_diagram.md`](class_diagram.md).

It is auto-generated from `bids_metaschema.yaml` by running:

```bash
uv run python src/schema/gen_class_diagram.py
```

The diagram excludes the 29 map wrapper classes (names ending in "Map")
for clarity.  Map-typed attributes are shown using `Map~ValueType~` notation
(e.g., `Map~Entity~` for a map with Entity values, `Map~Map~SuffixRule~~`
for a nested two-level map).

## Suggested Starting Point

Phase 1 is the critical path. Start with a minimal LinkML schema that models just the `objects.entities` and `objects.suffixes` sub-namespaces (they're the simplest — `GeneralTerm` + `NameValueTerm` / `ValueTerm`), then progressively add the more complex parts (`objects.metadata` with its embedded JSON Schema, then `rules.*`).
