import os
import shutil

import pytest


def require_env(var):
    env = os.environ.get(var)
    return pytest.mark.skipif(
        not env, reason=f"To activate this test/feature `export {var}=1` and re-run."
    )


@require_env("BIDSSCHEMATOOLS_RELEASE")
def test_make_archive(tests_data_dir, bids_examples, bids_error_examples):
    """
    ATTENTION! This is not a test!
    Create static testdata archive containing the bidsschematools data reference whitelist.

    Notes
    -----
    Due to intricacies arising from:

    (1) fixtures not working outside of pytest
    (2) implicit teardown leveraging tempdata removal (while held open by yield)
    (3) wrappers evaluating the yield statement
    (4) the desire to not download testdata twice for archive creation

    testdata archive creation is now inconspicuously posing as a test.
    """

    ignore_git = shutil.ignore_patterns(".git*")
    target_examples = tests_data_dir / "bids-examples"
    target_error_examples = tests_data_dir / "bids-error-examples"
    if bids_examples != target_examples:
        shutil.copytree(bids_examples, target_examples, ignore=ignore_git)
    if bids_error_examples != target_error_examples:
        shutil.copytree(bids_error_examples, target_error_examples, ignore=ignore_git)
