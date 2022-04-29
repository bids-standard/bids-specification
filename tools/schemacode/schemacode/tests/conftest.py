import pytest

from schemacode import schema, utils


@pytest.fixture(scope="session")
def schema_dir():
    """Path to the schema housed in the bids-specification repo."""
    bids_schema = utils.get_schema_path()
    return bids_schema


@pytest.fixture(scope="session")
def schema_obj(schema_dir):
    """Schema object."""
    return schema.load_schema(schema_dir)
