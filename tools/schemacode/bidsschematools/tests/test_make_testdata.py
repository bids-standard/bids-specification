import os
import shutil
import tarfile
import pytest

from .. import version_file


def require_env(var):
    env = os.environ.get(var)
    return pytest.mark.skipif(
        not env,
        reason=f"Release mode is not activated. Not generating static testdata archive. "
		"In order to force testdata archive generation run: "
		"`export BIDSSCHEMATOOLS_RELEASE_MODE_ACTIVATED=1`."
    )

@require_env("BIDSSCHEMATOOLS_RELEASE_MODE_ACTIVATED")
def test_make_archive(bids_examples, bids_error_examples, tmp_path):
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
    """

    bst_version = open(version_file).read().rstrip("\n")
    archive_name = f"bidsschematools-testdata-{bst_version}"
    data_path = os.path.join(tmp_path, archive_name)
    archive_path = f"{data_path}.tar.gz"

    try:
        os.mkdir(data_path)
    except FileExistsError:
        pass
    shutil.copytree(bids_examples, os.path.join(data_path, "bids-examples"))
    shutil.copytree(bids_error_examples, os.path.join(data_path, "bids-error-examples"))

    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(data_path, arcname=os.path.basename(data_path))
