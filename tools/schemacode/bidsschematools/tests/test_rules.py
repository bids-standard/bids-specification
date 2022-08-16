"""Simple validation tests on schema rules."""
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


def test_rule_objects(schema_obj):
    """Ensure that all objects referenced in the schema rules are defined in
    its object portion.
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
                assert use in schema_obj["objects"][object_type].keys(), path
