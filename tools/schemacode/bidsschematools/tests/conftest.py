import logging
import shutil
import tempfile
from subprocess import run

import pytest

from bidsschematools import schema, utils

lgr = logging.getLogger()

# This selects a subset of the bids-examples collection to run the test suite on.
# Generally it's best to avoid adding large datasets to this list, but ideally a
# good proportion modalities would be represented, as well as datasets exemplifying
# tricky edge-cases, such as directory pseudo-files.
BIDS_SELECTION = [
    "asl003",  # anat, perf, _asl, _T1w
    "eeg_cbm",  # eeg
    "hcp_example_bids",  # anat, fmap
    "micr_SEM",  # micr, SEM
    "micr_SPIM",  # micr, SPIM, .ome.tif
    "pet003",  # pet, anat
    "qmri_tb1tfl",  # fmap, _TB1TFL
    "qmri_vfa",  # derivatives
]
# Errors are described in the README of the respective datasets:
# https://github.com/bids-standard/bids-error-examples
BIDS_ERROR_SELECTION = [
    "invalid_asl003",
    "invalid_pet001",
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
            _ = run(["git", "sparse-checkout", "init", "--cone"], cwd=path)
            _ = run(["git", "sparse-checkout", "set"] + whitelist, cwd=path)
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
bids_error_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-error-examples",
    whitelist=BIDS_ERROR_SELECTION,
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
