import logging
import os
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
    "micr_SEMzarr",  # micr, SEM, OME-ZARR
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


def get_gitrepo_fixture(url, whitelist):
    @pytest.fixture(scope="session")
    def fixture():
        archive_name = url.rsplit("/", 1)[-1]
        testdata_archive = os.path.join(os.getcwd(), "testdata", archive_name)
        if os.path.isdir(testdata_archive):
            lgr.info(
                "Found static testdata archive under `%s`. "
                "Not downloading latest data from version control.",
                testdata_archive,
            )
            yield testdata_archive
        else:
            lgr.info(
                "No static testdata available under `%s`. "
                "Attempting to fetch live data from version control.",
                testdata_archive,
            )
            with tempfile.TemporaryDirectory() as path:
                assert os.path.exists(path)
                lgr.debug("Cloning %r into %r", url, path)
                runout = run(
                    [
                        "git",
                        "clone",
                        "--depth=1",
                        "--filter=blob:none",
                        "--sparse",
                        url,
                        path,
                    ],
                    capture_output=True,
                )
                if runout.returncode:
                    raise RuntimeError(f"Failed to clone {url} into {path}")
                # cwd specification is VERY important, not only to achieve the correct
                # effects, but also to avoid dropping files from your repository if you
                # were to run `git sparse-checkout` inside the software repo.
                _ = run(["git", "sparse-checkout", "init", "--cone"], cwd=path)
                _ = run(["git", "sparse-checkout", "set"] + whitelist, cwd=path)
                yield path

    return fixture


@pytest.fixture(scope="session")
def schema_dir():
    """Path to the schema housed in the bids-specification repo."""
    bids_schema = utils.get_schema_path()
    return bids_schema


@pytest.fixture(scope="session")
def schema_obj(schema_dir):
    """Schema object."""
    return schema.load_schema(schema_dir)


bids_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-examples",
    whitelist=BIDS_SELECTION,
)
bids_error_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-error-examples",
    whitelist=BIDS_ERROR_SELECTION,
)
