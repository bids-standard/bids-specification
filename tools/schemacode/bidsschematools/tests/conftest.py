import logging
import shutil
import tempfile
from subprocess import run

import pytest

from bidsschematools import schema, utils

lgr = logging.getLogger()

BIDS_SELECTION = [
    "asl003",
    "eeg_cbm",
    "hcp_example_bids",
    "micr_SEM",
    "micr_SPIM",
    "pet001",
    "pet003",
    "qmri_tb1tfl",
]


@pytest.mark.no_network
def get_gitrepo_fixture(url, whitelist):
    @pytest.fixture(scope="session")
    def fixture():
        path = tempfile.mktemp()  # not using pytest's tmpdir fixture to not
        # collide in different scopes etc. But we
        # would need to remove it ourselves
        lgr.debug("Cloning %r into %r", url, path)
        try:
            runout = run(
                [
                    "git",
                    "clone",
                    "--depth=1",
                    "--filter=blob:none",
                    "--sparse",
                    url,
                    path,
                ]
            )
            if runout.returncode:
                raise RuntimeError(f"Failed to clone {url} into {path}")
            # cwd specification is VERY important, not only to achieve the correct
            # effects, but also to avoid dropping files from your repository if you
            # were to run `git sparse-checkout` inside the software repo.
            run_init = run(["git", "sparse-checkout", "init", "--cone"], cwd=path)
            run_checkout = run(["git", "sparse-checkout", "set"] + whitelist, cwd=path)
            yield path
        finally:
            try:
                shutil.rmtree(path)
            except BaseException as exc:
                lgr.warning("Failed to remove %s - using Windows?: %s", path, exc)

    return fixture


bids_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-examples",
    whitelist=BIDS_SELECTION,
)


@pytest.fixture(scope="session")
def schema_dir():
    """Path to the schema housed in the bids-specification repo."""
    bids_schema = utils.get_schema_path()
    return bids_schema


@pytest.fixture(scope="session")
def schema_obj(schema_dir):
    """Schema object."""
    return schema.load_schema(schema_dir)
