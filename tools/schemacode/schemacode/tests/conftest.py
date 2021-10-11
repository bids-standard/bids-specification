from pathlib import Path

import pytest


@pytest.fixture(scope="session")
def schema_dir():
    """Path to the schema housed in the bids-specification repo."""
    bids_schema = Path(__file__).parent.parent.parent.parent.parent / "src" / "schema"
    return bids_schema
