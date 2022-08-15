"""Simple validation tests on schema rules."""
TYPES = {
    "string": str,
    "number": float,
    "integer": int,
    "boolean": bool,
    "object": dict,
    "array": list,
}


def test_object_definitions(schema_obj):
    """Ensure that all object definitions follow the appropriate type definition."""
    for type_name, type_objects in schema_obj["objects"].items():
        type_obj = schema_obj["meta"]["types"][type_name]
        type_def = type_obj["definition"]

        for obj, obj_def in type_objects.items():
            print(obj)
            print(obj_def)

        for field in type_def.keys():
            ...

    raise Exception()
