#!/usr/bin/env python3
"""Generate a Mermaid class diagram from the BIDS LinkML metaschema.

Uses PyYAML to parse bids_metaschema.yaml (since the schema uses draft
``extra_slots`` features not yet in the released linkml-runtime) and
produces a Mermaid ``classDiagram`` showing:

- Class inheritance hierarchy
- Key attributes for each class
- Enums with their permissible values
- Composition relationships (slots with class ranges)

Map wrapper classes (names ending in "Map") are excluded to keep the
diagram focused on the data model.

Usage::

    uv run python src/schema/gen_class_diagram.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

SCHEMA_PATH = Path(__file__).parent.parent / "bids_metaschema.yaml"
OUTPUT_PATH = Path(__file__).parent / "class_diagram.md"


def load_schema(path: Path) -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def is_map_wrapper(name: str) -> bool:
    """Return True for map wrapper classes we want to exclude."""
    return name.endswith("Map")


def resolve_map_value_type(map_class_name: str, all_classes: dict) -> str | None:
    """For a Map wrapper class, return the value type it wraps.

    Looks at extra_slots.range_expression.range to find what type
    the map values are.  Returns None if the map is open/untyped.
    """
    cls = all_classes.get(map_class_name, {})
    extra = cls.get("extra_slots", {})
    if not isinstance(extra, dict):
        return None
    range_expr = extra.get("range_expression", {})
    if isinstance(range_expr, dict):
        return range_expr.get("range")
    return None


def mermaid_type(range_val: str | None, default: str = "string") -> str:
    """Convert a LinkML range to a short Mermaid-friendly type string."""
    if range_val is None:
        return default
    # Simplify common LinkML built-in types
    simple = {
        "string": "string",
        "integer": "int",
        "float": "float",
        "boolean": "bool",
    }
    return simple.get(range_val, range_val)


def format_attr(name: str, attr: dict) -> str:
    """Format a single attribute line for a Mermaid class block."""
    range_val = mermaid_type(attr.get("range"))
    multivalued = attr.get("multivalued", False)
    required = attr.get("required", False)

    if multivalued:
        type_str = f"{range_val}[]"
    else:
        type_str = range_val

    # Use +/- for required/optional visibility
    visibility = "+" if required else "-"
    return f"    {visibility}{type_str} {name}"


def generate_diagram(schema: dict) -> str:
    classes = schema.get("classes", {})
    enums = schema.get("enums", {})

    lines: list[str] = []
    lines.append("classDiagram")
    lines.append("")

    # Separate data model classes from map wrappers
    data_classes = {
        name: cls for name, cls in classes.items() if not is_map_wrapper(name)
    }

    # --- Class blocks with attributes ---
    lines.append("    %% === Data model classes ===")
    lines.append("")

    for name, cls in data_classes.items():
        attrs = cls.get("attributes", {}) or {}
        # Also include slot_usage keys for display
        slot_usage = cls.get("slot_usage", {}) or {}

        lines.append(f"    class {name} {{")

        # Show description as a note if short enough
        desc = cls.get("description", "")
        if desc:
            # Truncate to first sentence
            first_sentence = desc.strip().split(". ")[0].rstrip(".")
            if len(first_sentence) <= 60:
                lines.append(f"        <<{first_sentence}>>")

        for attr_name, attr_def in attrs.items():
            if isinstance(attr_def, dict):
                range_val = attr_def.get("range", "")
                if isinstance(range_val, str) and is_map_wrapper(range_val):
                    # Resolve the map to its inner value type
                    inner = resolve_map_value_type(range_val, classes)
                    if inner and is_map_wrapper(inner):
                        # Nested map (e.g., GroupMap -> Map -> Type)
                        inner2 = resolve_map_value_type(inner, classes)
                        type_str = f"Map~Map~{inner2 or '?'}~~"
                    elif inner:
                        type_str = f"Map~{inner}~"
                    else:
                        type_str = "Map~any~"
                    lines.append(f"    -{type_str} {attr_name}")
                    continue
                lines.append(format_attr(attr_name, attr_def))

        # Show slot_usage overrides
        for su_name, su_def in slot_usage.items():
            if isinstance(su_def, dict) and su_def.get("required"):
                lines.append(f"    +* {su_name}")

        lines.append("    }")
        lines.append("")

    # --- Enum blocks ---
    lines.append("    %% === Enums ===")
    lines.append("")

    for enum_name, enum_def in enums.items():
        lines.append(f"    class {enum_name} {{")
        lines.append("        <<enumeration>>")
        pv = enum_def.get("permissible_values", {}) or {}
        for val_name in pv:
            lines.append(f"        {val_name}")
        lines.append("    }")
        lines.append("")

    # --- Inheritance relationships ---
    lines.append("    %% === Inheritance ===")
    lines.append("")

    for name, cls in data_classes.items():
        is_a = cls.get("is_a")
        if is_a and not is_map_wrapper(is_a):
            lines.append(f"    {is_a} <|-- {name}")

    lines.append("")

    # --- Composition relationships ---
    # For attributes whose range is a non-Map data class or enum
    lines.append("    %% === Composition relationships ===")
    lines.append("")

    for name, cls in data_classes.items():
        attrs = cls.get("attributes", {}) or {}
        for attr_name, attr_def in attrs.items():
            if not isinstance(attr_def, dict):
                continue
            range_val = attr_def.get("range", "")
            if not isinstance(range_val, str):
                continue
            # Skip basic types
            if range_val in ("string", "integer", "float", "boolean", ""):
                continue
            # If range is a data model class (not map wrapper)
            if range_val in data_classes:
                # Use composition for inlined, association otherwise
                inlined = attr_def.get("inlined", False)
                multivalued = attr_def.get("multivalued", False)
                card = '"*"' if multivalued else '"1"'
                if inlined:
                    lines.append(
                        f"    {name} *-- {card} {range_val} : {attr_name}"
                    )
                else:
                    lines.append(
                        f"    {name} --> {card} {range_val} : {attr_name}"
                    )
            # If range is an enum
            elif range_val in enums:
                lines.append(f"    {name} --> {range_val} : {attr_name}")

    lines.append("")

    return "\n".join(lines)


def main() -> None:
    schema = load_schema(SCHEMA_PATH)
    diagram = generate_diagram(schema)

    output = f"""\
# BIDS LinkML Metaschema — Class Diagram

Auto-generated from `bids_metaschema.yaml` by `gen_class_diagram.py`.

Map wrapper classes (29 classes ending in "Map") are excluded for clarity.

```mermaid
{diagram}
```
"""
    OUTPUT_PATH.write_text(output)
    print(f"Wrote {OUTPUT_PATH}")
    print(f"  Data model classes + enums visualized")
    print(f"  Map wrapper classes excluded")


if __name__ == "__main__":
    main()
