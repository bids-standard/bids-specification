#!/usr/bin/env python3
"""Post-process LinkML-generated JSON Schema for BIDS metaschema.

With the adoption of LinkML's extra_slots feature (PR linkml/linkml#2940),
the number of patches has been reduced from ~43 to ~6.

The remaining patches cover:
  - Category 5: Slot-level type coercions that extra_slots cannot express
  - Category 6: Root $ref for the top-level schema object
  - Special: sidecars/tabular_data derivatives nesting override

Usage:
    gen-json-schema bids_metaschema.yaml | python patch_metaschema.py > metaschema.json
"""

from __future__ import annotations

import json
import sys
from typing import Any


def patch(schema: dict[str, Any]) -> dict[str, Any]:
    """Apply patches to generated JSON Schema."""
    defs: dict[str, Any] = schema.get("$defs", {})

    # --- Categories 1-4 are now handled by extra_slots in the LinkML schema ---
    # Category 1 (simple typed maps): wrapper classes with range_expression
    # Category 2 (nested maps): nested wrapper classes
    # Category 3 (union-valued maps): wrapper classes with any_of
    # Category 4 (open classes): extra_slots: {allowed: true}

    # --- Category 5: Slot-level type coercions ---

    # MetaSection.context is an arbitrary JSON Schema object
    meta = defs.get("MetaSection", {})
    meta_props: dict[str, Any] = meta.get("properties", {})
    if "context" in meta_props:
        meta_props["context"] = {
            "description": meta_props["context"].get("description", ""),
            "type": "object",
        }

    # AssociationTarget.extension can be a string or an array of strings
    assoc_target = defs.get("AssociationTarget", {})
    at_props: dict[str, Any] = assoc_target.get("properties", {})
    if "extension" in at_props:
        at_props["extension"] = {
            "description": at_props["extension"].get("description", ""),
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ],
        }

    # ExpressionTest.result can be any JSON value
    expr_test = defs.get("ExpressionTest", {})
    et_props: dict[str, Any] = expr_test.get("properties", {})
    if "result" in et_props:
        et_props["result"] = {
            "description": et_props["result"].get("description", ""),
        }

    # JsonSchema is an open container for any JSON Schema fragment
    if "JsonSchema" in defs:
        defs["JsonSchema"] = {
            "description": defs["JsonSchema"].get("description", ""),
        }

    # DirectoryEntry.subdirs items can be strings or objects
    dir_entry = defs.get("DirectoryEntry", {})
    de_props: dict[str, Any] = dir_entry.get("properties", {})
    if "subdirs" in de_props:
        de_props["subdirs"] = {
            "description": de_props["subdirs"].get("description", ""),
            "type": "array",
            "items": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "object"},
                ]
            },
        }

    # --- Special: sidecars/tabular_data derivatives nesting ---
    # The derivatives sub-group nests one more level than the regular
    # groups. Override the generated schema with anyOf to accept both
    # {RuleName: Rule} and {SubGroup: {RuleName: Rule}} at each group.
    sidecar_rule_map: dict[str, Any] = {
        "type": "object",
        "additionalProperties": {"$ref": "#/$defs/SidecarRule"},
    }
    tabular_rule_map: dict[str, Any] = {
        "type": "object",
        "additionalProperties": {"$ref": "#/$defs/TabularDataRule"},
    }
    rules_section = defs.get("RulesSection", {})
    rules_props: dict[str, Any] = rules_section.get("properties", {})
    if "sidecars" in rules_props:
        rules_props["sidecars"] = {
            "description": rules_props["sidecars"].get("description", ""),
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    sidecar_rule_map,
                    {
                        "type": "object",
                        "additionalProperties": sidecar_rule_map,
                    },
                ],
            },
        }
    if "tabular_data" in rules_props:
        rules_props["tabular_data"] = {
            "description": rules_props["tabular_data"].get("description", ""),
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    tabular_rule_map,
                    {
                        "type": "object",
                        "additionalProperties": tabular_rule_map,
                    },
                ],
            },
        }

    # --- Category 6: Root $ref ---
    schema["$ref"] = "#/$defs/BidsSchema"

    return schema


if __name__ == "__main__":
    raw = json.load(sys.stdin)
    patched = patch(raw)
    json.dump(patched, sys.stdout, indent=2)
    sys.stdout.write("\n")
