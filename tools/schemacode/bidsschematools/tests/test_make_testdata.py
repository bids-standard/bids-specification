import os
import shutil
import tarfile
import tempfile

import pytest

from .. import __version__


def require_env(var):
    env = os.environ.get(var)
    return pytest.mark.skipif(
        not env,
        reason=f"To activate this test/feature `export {var}=1` and re-run."
    )


@require_env("BIDSSCHEMATOOLS_RELEASE")
def test_make_archive(bids_examples, bids_error_examples):
    """
    ATTENTION! This is not a test!
    Create static testdata archive containing the bidsschematools data reference whitelist.

    Notes
    -----
    * Due to intricacies arising from:
        (1) fixtures not working outside of pytest
        (2) implicit teardown leveraging tempdata removal (while held open by yield)
        (3) wrappers evaluating the yield statement
        (4) the desire to not download testdata twice for archive creation
        testdata archive creation is now inconspicuously posing as a test.
    * Archives will be generated under `/tmp/bidsschematools-testdata-SCHEMA_VERSION.tar.gz`
    """

    archive_name = f"bidsschematools-testdata-{__version__}"
    archive_path = f"/tmp/{archive_name}.tar.gz"

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(bids_examples, arcname=f"{archive_name}/bids-examples")
        tar.add(bids_error_examples, arcname=f"{archive_name}/bids-examples")
