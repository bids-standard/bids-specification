"""Simple validation tests on schema rules."""

import warnings
from collections.abc import Mapping

import pytest


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
    their object portion.

    In the case of datatypes, the key and "value" field are always the same.

    Some other object types, such as associated_data, common_principles, formats, modalities,
    and top_level_files, are not checked in the rules at all.

    Additionally, this test only checks rules that fit the keys.
    """
    OBJECT_TYPE_MAPPER = {
        "metadata": "fields",  # metadata in objects is referred to as fields in rules
    }

    not_found = []  # A list of undefined, but referenced, objects
    for object_type in schema_obj.objects:
        # "files" is both an object name and a grouping of rules
        # The next line would be a false positive hit
        if object_type == "files":
            continue
        # Find all uses of a given object type in the schema rules
        type_instances_in_rules = _dict_key_lookup(
            schema_obj.rules,
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
                assert isinstance(use, str)
                if use == "derivatives":
                    # Skip derivatives dirs, because the dir is treated as a "use" instead.
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
                        value["value"] for value in schema_obj["objects"][object_type].values()
                    ]
                elif object_type in [
                    "columns",
                    "common_principles",
                    "datatypes",
                    "entities",
                    "enums",
                    "files",
                    "formats",
                    "metadata",
                    "metaentities",
                    "modalities",
                ]:
                    # But other object types are referenced via their keys
                    object_values = list(schema_obj["objects"][object_type].keys())
                else:
                    raise AssertionError(f"Object type {object_type} not implemented.")

                # Build a list of items mentioned in rules, but not found in objects.
                if use not in object_values:
                    temp_path = path[:]
                    if is_list:
                        temp_path[-1] += f"[{i_use}]"

                    not_found.append((temp_path, use))

    if not_found:
        not_found_string = "\n".join([f"{'.'.join(path)} == {val}" for path, val in not_found])
        raise AssertionError(f"Undefined objects found in rules: {not_found_string}")


@pytest.mark.validate_schema
def test_entity_order(schema_obj):
    """Check the order of the entities of the suffix group of each datatype
    and lists those that are out of order.
    """
    status_ok = True

    entities_order = schema_obj.rules.entities

    for key, group in schema_obj.rules.files.items(level=2):
        print(f"Checking {key}")
        entities = list(group.get("entities", ()))
        correct_order = sorted(entities, key=lambda x: entities_order.index(x))

        if entities != correct_order:
            status_ok = False
            warnings.warn(
                f"""\n\nfilename rule {key} has entities out-of-order:
                - got: {entities}
                - should be: {correct_order}
                """
            )

    if not status_ok:
        raise RuntimeError(
            "Some suffix groups have their entities out of order. See warnings above."
        )
