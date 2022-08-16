"""Simple validation tests on schema rules."""
import pytest

from bidsschematools.schema import Namespace


def _dict_key_lookup(_dict, key, path=[]):
    """Look up any uses of a key in a nested dictionary.

    Adapted from https://stackoverflow.com/a/60377584/2589328.
    """
    results = []
    if isinstance(_dict, (dict, Namespace)):
        if key in _dict:
            results.append((path + [key], _dict[key]))

        for k, v in _dict.items():
            results.extend(_dict_key_lookup(v, key, path=path + [k]))

    elif isinstance(_dict, list):
        for index, item in enumerate(_dict):
            results.extend(_dict_key_lookup(item, key, path=path + [index]))

    return results


@pytest.mark.xfail
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
    object_types = list(schema_obj["objects"].keys())
    for object_type in object_types:
        type_instances_in_rules = _dict_key_lookup(schema_obj["rules"], object_type)
        if not type_instances_in_rules:
            continue

        for type_instance in type_instances_in_rules:
            path, instance = type_instance
            if isinstance(instance, dict):
                instance = list(instance.keys())

            for use in instance:
                # Skip derivatives folders, because the folder is treated as a "use" instead.
                if use == "derivatives":
                    continue

                assert use in schema_obj["objects"][object_type].keys(), path
