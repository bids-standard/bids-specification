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

## Phase 2: Validation continuity — Generate JSON Schema from LinkML

- Use `linkml gen-json-schema` to produce a JSON Schema from the LinkML model
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

## Suggested Starting Point

Phase 1 is the critical path. Start with a minimal LinkML schema that models just the `objects.entities` and `objects.suffixes` sub-namespaces (they're the simplest — `GeneralTerm` + `NameValueTerm` / `ValueTerm`), then progressively add the more complex parts (`objects.metadata` with its embedded JSON Schema, then `rules.*`).
