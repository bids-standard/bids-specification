"""Simple validation tests on schema rules."""
import warnings
from collections.abc import Mapping

import pytest

TYPES = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


@pytest.mark.validate_schema
def test_object_definitions(schema_obj):
    """Ensure that all object definitions follow the appropriate type definition."""
    for type_name, type_objects in schema_obj["objects"].items():
        type_obj = schema_obj["meta"]["types"][type_name]
        type_def = type_obj["definition"]

        for obj, obj_def in type_objects.items():
            if "type" in type_def.keys():
                valid_types = [
                    thing if isinstance(thing, str) else list(thing.keys())[0]
                    for thing in type_def["type"]
                ]
                assert "type" in obj_def.keys(), f"{type_name}, {obj}"
                assert obj_def["type"] in valid_types

            for field, value in obj_def.items():
                if field not in type_def.keys():
                    pass


def _dict_key_lookup(_dict, key, path=[]):
    """Look up any uses of a key in a nested dictionary.

    Adapted from https://stackoverflow.com/a/60377584/2589328.
    """
    results = []
    if isinstance(_dict, Mapping):
        if key in _dict:
            results.append((path + [key], _dict[key]))

        for k, v in _dict.items():
            results.extend(_dict_key_lookup(v, key, path=path + [k]))

    elif isinstance(_dict, list):
        for index, item in enumerate(_dict):
            results.extend(_dict_key_lookup(item, key, path=path + [index]))

    return results


@pytest.mark.validate_schema
def test_rule_objects(schema_obj):
    """Ensure that all objects referenced in the schema rules are defined in
    its object portion.

    This test currently fails because rules files reference object keys for some object types,
    including entities, columns, and metadata fields,
    but reference "name" or "value" elements of the object definitions for other object types,
    including suffixes and extensions.
    In the case of datatypes, the key and "value" field are always the same.

    Some other object types, such as associated_data, common_principles, formats, modalities,
    and top_level_files, are not checked in the rules at all.

    Additionally, this test only checks rules that fit the keys.
    """
    OBJECT_TYPE_MAPPER = {
        "metadata": "fields",  # metadata in objects is referred to as fields in rules
    }

    not_found = []  # A list of undefined, but referenced, objects
    object_types = list(schema_obj["objects"].keys())
    for object_type in object_types:
        # Find all uses of a given object type in the schema rules
        type_instances_in_rules = _dict_key_lookup(
            schema_obj["rules"],
            OBJECT_TYPE_MAPPER.get(object_type, object_type),
        )
        if not type_instances_in_rules:
            continue

        for type_instance in type_instances_in_rules:
            path, instance = type_instance
            is_list = True
            if isinstance(instance, Mapping):
                instance = list(instance)
                is_list = False

            for i_use, use in enumerate(instance):
                if use == "derivatives":
                    # Skip derivatives folders, because the folder is treated as a "use" instead.
                    continue
                elif "[]" in use:
                    # Rules may reference metadata fields with lists.
                    # This test can't handle this yet, so skip.
                    continue
                elif "{}" in use:
                    # Rules may reference sub-dictionaries in metadata fields.
                    # This test can't handle this yet, so skip.
                    continue

                if object_type in ["extensions", "suffixes"]:
                    # Some object types are referenced via their "value" fields in the rules
                    object_values = [
                        schema_obj["objects"][object_type][k]["value"]
                        for k in schema_obj["objects"][object_type].keys()
                    ]
                else:
                    # But other object types are referenced via their keys
                    object_values = list(schema_obj["objects"][object_type].keys())

                # Build a list of items mentioned in rules, but not found in objects.
                if use not in object_values:
                    temp_path = path[:]
                    if is_list:
                        temp_path[-1] += f"[{i_use}]"

                    not_found.append((temp_path, use))

    if not_found:
        not_found_string = "\n".join([f"{'.'.join(path)} == {val}" for path, val in not_found])
        raise ValueError(not_found_string)


@pytest.mark.validate_schema
def test_entity_order(schema_obj):
    """Check the order of the entities of the suffix group of each datatype
    and lists those that are out of order.
    """
    status_ok = True

    entities_order = schema_obj["rules"]["entities"]
    datatypes_schema_obj = schema_obj["rules"]["datatypes"]

    for datatype, datatype_schema_obj in datatypes_schema_obj.items():

        print(f"Checking: {datatype}")
        # Skip over derivatives folders nested in regular folders
        if datatype == "derivatives":
            continue

        for suffix_group, suffix_group_obj in datatype_schema_obj.items():
            entities = list(suffix_group_obj["entities"].keys())
            correct_order = sorted(entities, key=lambda x: entities_order.index(x))

            if entities != correct_order:
                status_ok = False
                warnings.warn(
                    f"""
                \nsuffix group {suffix_group} in {datatype} is out of order:
                - got: {entities}
                - should be: {correct_order}
                """
                )

    if not status_ok:
        raise RuntimeError(
            "Some suffix groups have their entities out of order. See warnings above."
        )
