import os


def test_make_archive(bids_examples, bids_error_examples, tmp_path):
    """
    ATTENTION! This is not a test!
    Creates a static testdata directory containing only the bidsschematools whitelist of reference datasets.

    Notes
    -----
    * Due to intricacies arising from:
        (1) fixtures not working outside of pytest
        (2) implicit teardown leveraging tempdata removal (while held open by yield)
        (3) wrappers evaluating the yield statement
        (4) the desire to not download testdata twice for archive creation
        testdata archive creation is now inconspicuously posing as a test.
    """

    import shutil

    archive_path = os.path.join(tmp_path, "testdata")
    try:
        os.mkdir(archive_path)
    except FileExistsError:
        pass
    shutil.copytree(bids_examples, os.path.join(archive_path, "bids-examples"))
    shutil.copytree(bids_error_examples, os.path.join(archive_path, "bids-error-examples"))
