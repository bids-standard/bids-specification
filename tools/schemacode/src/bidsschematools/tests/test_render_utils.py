from bidsschematools.render import utils


def test_combine_extensions():
    """A unit test for utils.combine_extensions."""
    test_extensions = ["nii.gz", "nii", "json"]
    target_combined = ["nii[.gz]", "json"]
    test_combined = utils.combine_extensions(test_extensions, pdf_format=True)
    assert test_combined == target_combined


def test_resolve_metadata_type():
    """A unit test for utils.resolve_metadata_type."""
    base_definition = {
        "name": "Term",
        "description": "A description",
    }

    # Basic string
    term_definition1 = base_definition.copy()
    term_definition1["type"] = "string"
    target_description = "[string](https://www.w3schools.com/js/js_json_datatypes.asp)"
    type_description = utils.resolve_metadata_type(term_definition1)
    assert target_description == type_description

    # When n/a is the only allowed value, the type should say "n/a"
    term_definition1["enum"] = ["n/a"]
    target_description = '`"n/a"`'
    type_description = utils.resolve_metadata_type(term_definition1)
    assert target_description == type_description
