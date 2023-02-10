import os
import subprocess

import pytest

from ..conftest import BIDS_ERROR_SELECTION, BIDS_SELECTION


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_validate_bids(bids_examples, tmp_path):
    selected_dir = os.path.join(bids_examples, BIDS_SELECTION[0])

    subprocess.check_output(["bst", "validate", selected_dir])


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_validate_bids_error(bids_error_examples, tmp_path):
    import ast

    selected_dir = os.path.join(bids_error_examples, BIDS_ERROR_SELECTION[0])

    p = subprocess.run(["bst", "validate", selected_dir], stdout=subprocess.PIPE)
    # Ideally we would do this by capturing the logging, since that's what the CLI actually
    # produces.
    output = ast.literal_eval(p.stdout.decode("utf-8"))
    assert len(output["path_tracking"]) > 0
