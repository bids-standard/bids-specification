import logging
import tempfile
from collections.abc import Generator
from pathlib import Path
from subprocess import run

import pytest

from . import data

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
    "ds000248",  # .bidsignore
    "fnirs_automaticity",  # phenotypic
]
# Errors are described in the README of the respective datasets:
# https://github.com/bids-standard/bids-error-examples
BIDS_ERROR_SELECTION = [
    "invalid_asl003",
    "invalid_pet001",
]


@pytest.fixture(scope="session")
def tests_data_dir():
    try:
        this_file = Path(__file__)
    except NameError:
        return None

    data_dir = this_file.parent.parent.parent / "tests" / "data"

    if data_dir.exists():
        return data_dir


def get_gitrepo_fixture(url, whitelist):
    @pytest.fixture(scope="session")
    def fixture(tests_data_dir):
        if tests_data_dir is None:
            pytest.skip("No test data directory found; probably in an installed package")
        archive_name = url.rsplit("/", 1)[-1]
        archive_dir = tests_data_dir / archive_name
        if archive_dir.is_dir():
            lgr.info(
                f"Found static testdata archive under `{archive_dir}`. "
                "Not downloading latest data from version control."
            )
            yield archive_dir
        else:
            lgr.info(
                "No static testdata available under `%s`. "
                "Attempting to fetch live data from version control.",
                archive_dir,
            )
            with tempfile.TemporaryDirectory() as path:
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
def schema_dir() -> Generator[str, None, None]:
    """Path to the schema housed in the bids-specification repo."""
    with data.load.as_path("schema") as schema_path:
        if not schema_path.exists():
            pytest.skip("No schema found; probably in an installed package")
        yield str(schema_path)


@pytest.fixture(scope="session")
def schema_obj():
    """Schema object."""
    from bidsschematools import schema

    return schema.load_schema()


bids_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-examples",
    whitelist=BIDS_SELECTION,
)
bids_error_examples = get_gitrepo_fixture(
    "https://github.com/bids-standard/bids-error-examples",
    whitelist=BIDS_ERROR_SELECTION,
)
