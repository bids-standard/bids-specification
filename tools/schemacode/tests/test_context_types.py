from bidsschematools.types import context


def test_import():
    "Verify that the module contains the generated content."
    assert context.__doc__.splitlines()[0].startswith("BIDS validation context")
    assert "Context" in context.__all__

    assert isinstance(context.Context, type)
