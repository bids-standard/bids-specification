#!/usr/bin/env python3
"""Post-process LinkML-generated JSON Schema for BIDS metaschema.

LinkML does not natively support maps with arbitrary string keys and
typed values (JSON Schema additionalProperties / patternProperties).
This script patches the generated JSON Schema to add those constraints,
producing a metaschema that can validate the compiled BIDS schema.

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

    # --- Patch map slots to use additionalProperties ---
    # Each entry: (class_name, slot_name, value_ref_or_type)
    map_patches: list[tuple[str, str, dict[str, Any]]] = [
        # MetaSection
        ("MetaSection", "associations", {"$ref": "#/$defs/Association"}),
        ("MetaSection", "context", {"type": "object"}),
        ("MetaSection", "templates", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/Template"},
            },
        }),
        # ObjectsSection - each sub-namespace is a map of name -> typed object
        ("ObjectsSection", "columns", {"$ref": "#/$defs/Column"}),
        ("ObjectsSection", "common_principles", {"$ref": "#/$defs/GeneralTerm"}),
        ("ObjectsSection", "datatypes", {"$ref": "#/$defs/Datatype"}),
        ("ObjectsSection", "entities", {"$ref": "#/$defs/Entity"}),
        ("ObjectsSection", "enums", {}),  # mixed EnumValue / PrivateEnum, allow any
        ("ObjectsSection", "extensions", {"$ref": "#/$defs/Extension"}),
        ("ObjectsSection", "files", {"$ref": "#/$defs/FileObject"}),
        ("ObjectsSection", "formats", {"$ref": "#/$defs/Format"}),
        ("ObjectsSection", "metadata", {"$ref": "#/$defs/MetadataField"}),
        ("ObjectsSection", "metaentities", {"$ref": "#/$defs/GeneralTerm"}),
        ("ObjectsSection", "modalities", {"$ref": "#/$defs/GeneralTerm"}),
        ("ObjectsSection", "suffixes", {"$ref": "#/$defs/Suffix"}),
        # RulesSection
        ("RulesSection", "checks", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/CheckRule"},
            },
        }),
        ("RulesSection", "dataset_metadata", {"$ref": "#/$defs/SidecarRule"}),
        ("RulesSection", "directories", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/DirectoryEntry"},
            },
        }),
        ("RulesSection", "errors", {"$ref": "#/$defs/ErrorDefinition"}),
        ("RulesSection", "json", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/SidecarRule"},
            },
        }),
        ("RulesSection", "modalities", {"$ref": "#/$defs/ModalityMapping"}),
        ("RulesSection", "sidecars", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/SidecarRule"},
            },
        }),
        ("RulesSection", "tabular_data", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/TabularDataRule"},
            },
        }),
        # FileRulesSection
        ("FileRulesSection", "common", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {},
            },
        }),
        ("FileRulesSection", "raw", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/SuffixRule"},
            },
        }),
        ("FileRulesSection", "deriv", {
            "type": "object",
            "additionalProperties": {
                "type": "object",
                "additionalProperties": {"$ref": "#/$defs/SuffixRule"},
            },
        }),
    ]

    for class_name, slot_name, value_schema in map_patches:
        cls: dict[str, Any] = defs.get(class_name, {})
        props: dict[str, Any] = cls.get("properties", {})
        if slot_name in props:
            if "$ref" in value_schema or "type" not in value_schema:
                # Simple map: object with additionalProperties
                props[slot_name] = {
                    "description": props[slot_name].get("description", ""),
                    "type": "object",
                    "additionalProperties": value_schema if value_schema else True,
                }
            else:
                # Complex nested type (already fully specified)
                desc = props[slot_name].get("description", "")
                value_schema["description"] = desc
                props[slot_name] = value_schema

    # --- Patch SidecarRule.fields and TabularDataRule.columns ---
    # These are maps from name -> RequirementLevel string | FieldSpec object
    field_spec = {
        "anyOf": [
            {"$ref": "#/$defs/RequirementLevel"},
            {"$ref": "#/$defs/FieldSpec"},
        ]
    }
    for class_name, slot_name in [
        ("SidecarRule", "fields"),
        ("TabularDataRule", "columns"),
    ]:
        cls = defs.get(class_name, {})
        props = cls.get("properties", {})
        if slot_name in props:
            props[slot_name] = {
                "description": props[slot_name].get("description", ""),
                "type": "object",
                "additionalProperties": field_spec,
            }

    # --- Patch SuffixRule.entities ---
    # Map from entity name -> RequirementLevel string | EntityOverride object
    entity_spec = {
        "anyOf": [
            {"$ref": "#/$defs/RequirementLevel"},
            {"$ref": "#/$defs/EntityOverride"},
        ]
    }
    suffix_rule = defs.get("SuffixRule", {})
    suffix_props = suffix_rule.get("properties", {})
    if "entities" in suffix_props:
        suffix_props["entities"] = {
            "description": suffix_props["entities"].get("description", ""),
            "type": "object",
            "additionalProperties": entity_spec,
        }

    # --- Patch Template.entities ---
    template = defs.get("Template", {})
    template_props = template.get("properties", {})
    if "entities" in template_props:
        template_props["entities"] = {
            "description": template_props["entities"].get("description", ""),
            "type": "object",
            "additionalProperties": {"$ref": "#/$defs/RequirementLevel"},
        }

    # --- Patch AssociationTarget.extension to allow string or array ---
    assoc_target = defs.get("AssociationTarget", {})
    at_props = assoc_target.get("properties", {})
    if "extension" in at_props:
        at_props["extension"] = {
            "description": at_props["extension"].get("description", ""),
            "anyOf": [
                {"type": "string"},
                {"type": "array", "items": {"type": "string"}},
            ],
        }

    # --- Patch ExpressionTest.result to allow any value ---
    expr_test = defs.get("ExpressionTest", {})
    et_props = expr_test.get("properties", {})
    if "result" in et_props:
        et_props["result"] = {
            "description": et_props["result"].get("description", ""),
        }

    # --- Patch JsonSchema to allow any object ---
    if "JsonSchema" in defs:
        defs["JsonSchema"] = {
            "description": defs["JsonSchema"].get("description", ""),
        }

    # --- Patch DirectoryEntry.subdirs to allow objects (oneOf) ---
    dir_entry = defs.get("DirectoryEntry", {})
    de_props = dir_entry.get("properties", {})
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

    # --- Patch sidecars/tabular_data to handle the 'derivatives'
    #     sub-group which nests one more level ---
    sidecar_rule_map = {
        "type": "object",
        "additionalProperties": {"$ref": "#/$defs/SidecarRule"},
    }
    tabular_rule_map = {
        "type": "object",
        "additionalProperties": {"$ref": "#/$defs/TabularDataRule"},
    }
    rules_section = defs.get("RulesSection", {})
    rules_props = rules_section.get("properties", {})
    if "sidecars" in rules_props:
        rules_props["sidecars"] = {
            "description": rules_props["sidecars"].get("description", ""),
            "type": "object",
            "additionalProperties": {
                "anyOf": [
                    sidecar_rule_map,  # direct group: {RuleName: SidecarRule}
                    {  # nested group like derivatives: {SubGroup: {RuleName: SidecarRule}}
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
                    tabular_rule_map,  # direct group
                    {  # nested group like derivatives
                        "type": "object",
                        "additionalProperties": tabular_rule_map,
                    },
                ],
            },
        }

    # --- Remove additionalProperties: false from classes that need
    #     to accept JSON Schema fields (metadata, columns) ---
    for class_name in [
        "MetadataField", "Column", "NameValueTerm",
        "Suffix", "EnumValue", "ValueTerm",
        "DirectoryEntry", "Template",
    ]:
        cls = defs.get(class_name, {})
        cls.pop("additionalProperties", None)

    # --- Set the root $ref to BidsSchema ---
    schema["$ref"] = "#/$defs/BidsSchema"

    return schema


if __name__ == "__main__":
    raw = json.load(sys.stdin)
    patched = patch(raw)
    json.dump(patched, sys.stdout, indent=2)
    sys.stdout.write("\n")
