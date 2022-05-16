import pytest
import tempfile
import logging
from subprocess import run

from schemacode import schema, utils

lgr = logging.getLogger()

@pytest.mark.no_network
def get_gitrepo_fixture(url):
    @pytest.fixture(scope="session")
    def fixture():
        path = tempfile.mktemp()  # not using pytest's tmpdir fixture to not
        # collide in different scopes etc. But we
        # would need to remove it ourselves
        lgr.debug("Cloning %r into %r", url, path)
        try:
            runout = run(["git", "clone", "--depth=1", url, path])
            if runout.returncode:
                raise RuntimeError(f"Failed to clone {url} into {path}")
            yield path
        finally:
            try:
                shutil.rmtree(path)
            except BaseException as exc:
                lgr.warning("Failed to remove %s - using Windows?: %s", path, exc)

    return fixture

bids_examples = get_gitrepo_fixture("https://github.com/bids-standard/bids-examples")

@pytest.fixture(scope="session")
def schema_dir():
    """Path to the schema housed in the bids-specification repo."""
    bids_schema = utils.get_schema_path()
    return bids_schema


@pytest.fixture(scope="session")
def schema_obj(schema_dir):
    """Schema object."""
    return schema.load_schema(schema_dir)

