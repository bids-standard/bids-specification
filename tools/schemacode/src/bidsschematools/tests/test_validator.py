import os
import shutil

import pytest

from bidsschematools.conftest import BIDS_ERROR_SELECTION, BIDS_SELECTION
from bidsschematools.validator import select_schema_path, validate_bids

from ..data import load
from .data import load_test_data


def test_inheritance_examples():
    correct_inheritance = [
        "/lala/sub-01/ses-test/sub-01_ses-test_task-sometask_bold.json",
        "/lala/sub-01/sub-01_task-sometask_bold.json",
        "/lala/task-sometask_bold.json",
    ]
    incorrect_inheritance = [
        "/lala/sub-01/sub-01_ses-test_task-sometask_bold.json",
        "/lala/ses-test_task-sometask.json",
    ]

    result = validate_bids(
        correct_inheritance + incorrect_inheritance,
        dummy_paths=True,
    )

    assert result["path_tracking"] == incorrect_inheritance


def test_regression_examples():
    """Tests that failed on pybids when switching to bst-regex-based validation"""
    examples = [
        "/sub-01/ses-ses/sub-01_dwi.bval",  # redundant dir /ses-ses/
        "/sub-01/01_dwi.bvec",  # missed subject suffix
        "/sub-01/sub_dwi.json",  # missed subject id
        "/sub-01/sub-01_23_run-01_dwi.bval",  # wrong _23_
        "/sub-01/sub-01_run-01_dwi.vec",  # wrong extension
        "/sub-01/sub-01_run-01_dwi.jsn",  # wrong extension
        "/sub-01/sub-01_acq_dwi.bval",  # missed suffix value
        "/sub-01/sub-01_acq-23-singleband_dwi.bvec",  # redundant -23-
        "/sub-01/anat/sub-01_acq-singleband_dwi.json",  # redundant /anat/
        "/sub-01/sub-01_recrod-record_acq-singleband_run-01_dwi.bval",  # redundant record-record_
        "/sub_01/sub-01_acq-singleband_run-01_dwi.bvec",  # wrong /sub_01/
        "/sub-01/sub-01_acq-singleband__run-01_dwi.json",  # wrong __
        "/sub-01/ses-test/sub-01_ses_test_dwi.bval",  # wrong ses_test
        "/sub-01/ses-test/sb-01_ses-test_dwi.bvec",  # wrong sb-01
        "/sub-01/ses-test/sub-01_ses-test_dw.json",  # wrong modality
        "/sub-01/ses-test/sub-01_ses-test_run-01_dwi.val",  # wrong extension
        "/sub-01/ses-test/sub-01_run-01_dwi.bvec",  # missed session in the filename
        # This validator adds a .*/ to the regex, so this will be a false negative
        # If I cared about this validator, I would dig into it, but it doesn't seem worth it.
        # -cjm 2024.08.14
        # "/sub-01/ses-test/ses-test_run-01_dwi.json",  # missed subject in the filename
        "/sub-01/ses-test/sub-01_ses-test_acq-singleband.bval",  # missed modality
        "/sub-01/ses-test/sub-01_ses-test_acq-singleband_dwi",  # missed extension
        "/ses-test/sub-01/sub-01_ses-test_acq-singleband_dwi.json",  # wrong dirs order
        "/sub-01/ses-test/sub-02_ses-test_acq-singleband_run-01_dwi.bval",  # wrong sub id
        "/sub-01/sub-01_ses-test_acq-singleband_run-01_dwi.bvec",  # ses dir missed
        "/ses-test/sub-01_ses-test_acq-singleband_run-01_dwi.json",  # sub id dir missed
    ]

    result = validate_bids(examples, dummy_paths=True)
    assert result["path_tracking"] == examples


def test_write_report(tmp_path):
    from bidsschematools.validator import write_report

    validation_result = {}

    validation_result["schema_tracking"] = [
        {
            "regex": ".*?/sub-(?P<subject>[0-9a-zA-Z+]+)/"
            "(|ses-(?P<session>[0-9a-zA-Z+]+)/)anat/sub-(?P=subject)"
            "(|_ses-(?P=session))(|_acq-(?P<acquisition>[0-9a-zA-Z+]+))"
            "(|_ce-(?P<ceagent>[0-9a-zA-Z+]+))"
            "(|_rec-(?P<reconstruction>[0-9a-zA-Z+]+))"
            "(|_run-(?P<run>[0-9a-zA-Z+]+))"
            "(|_part-(?P<part>(mag|phase|real|imag)))"
            "_(T1w|T2w|PDw|T2starw|FLAIR|inplaneT1|inplaneT2|PDT2|angio|T2star)"
            "\\.(nii.gz|nii|json)$",
            "mandatory": False,
        }
    ]
    validation_result["schema_listing"] = [
        {
            "regex": ".*?/sub-(?P<subject>[0-9a-zA-Z+]+)/"
            "(|ses-(?P<session>[0-9a-zA-Z+]+)/)anat/sub-(?P=subject)"
            "(|_ses-(?P=session))(|_acq-(?P<acquisition>[0-9a-zA-Z+]+))"
            "(|_ce-(?P<ceagent>[0-9a-zA-Z+]+))"
            "(|_rec-(?P<reconstruction>[0-9a-zA-Z+]+))"
            "(|_run-(?P<run>[0-9]+))"
            "(|_part-(?P<part>(mag|phase|real|imag)))"
            "_(T1w|T2w|PDw|T2starw|FLAIR|inplaneT1|inplaneT2|PDT2|angio|T2star)"
            "\\.(nii.gz|nii|json)$",
            "mandatory": False,
        }
    ]
    validation_result["path_tracking"] = [
        "/home/chymera/.data2/datalad/000026/"
        "noncompliant/sub-EXC022/anat/sub-EXC022_ses-MRI_flip-1_VFA.nii.gz"
    ]
    validation_result["path_listing"] = [
        "/home/chymera/.data2/datalad/000026/"
        "noncompliant/sub-EXC022/anat/sub-EXC022_ses-MRI_flip-1_VFA.nii.gz"
    ]

    report_path = tmp_path / "output_bids_validator_xs_write.log"
    write_report(validation_result, report_path=str(report_path))

    expected_report_path = load_test_data("expected_bids_validator_xs_write.log")
    assert report_path.read_text() == expected_report_path.read_text()


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
@pytest.mark.parametrize("dataset", BIDS_SELECTION)
def test_bids_datasets(bids_examples, tmp_path, dataset):
    # Validate per dataset:
    target = os.path.join(bids_examples, dataset)
    result = validate_bids(
        target,
    )
    # Have all files been validated?
    assert len(result["path_tracking"]) == 0


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_validate_bids(bids_examples, tmp_path):
    # Create input for file list based validation
    selected_dir = os.path.join(bids_examples, BIDS_SELECTION[0])
    selected_paths = []
    for root, dirs, files in os.walk(selected_dir, topdown=False):
        for f in files:
            selected_path = os.path.join(root, f)
            selected_paths.append(selected_path)
    # Does version fallback work?
    result = validate_bids(selected_paths, schema_path=False)
    # Does default log path specification work?
    result = validate_bids(selected_paths, report_path=True)

    # Does custom log path specification work?
    result = validate_bids(
        selected_paths,
        report_path=os.path.join(tmp_path, "test_bids.log"),
    )
    # Have all files been validated?
    assert len(result["path_tracking"]) == 0

    # Is the schema version recorded correctly?
    schema_path = load.readable("schema")
    expected_version = schema_path.joinpath("BIDS_VERSION").read_text().rstrip()
    assert result["bids_version"] == expected_version


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_broken_json_dataset(bids_examples, tmp_path):
    """Perhaps this can be integrated into
    https://github.com/bids-standard/bids-error-examples ."""

    dataset = "asl003"
    dataset_path = os.path.join(bids_examples, dataset)
    dataset_json = os.path.join(dataset_path, "dataset_description.json")

    broken_json = load_test_data("broken_dataset_description.json")
    shutil.copyfile(broken_json, dataset_json)

    # No assert, will simply raise JSON reader error if not catching it properly.
    _ = validate_bids(
        dataset_path,
        report_path=True,
    )


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_exclude_files(bids_examples, tmp_path):
    from bidsschematools.validator import validate_bids

    dataset = "asl003"
    dataset_reference = os.path.join(bids_examples, dataset)
    tmp_path = str(tmp_path)
    shutil.copytree(dataset_reference, tmp_path, dirs_exist_ok=True)

    # Create non-BIDS non-dotfile
    archive_file_name = "dandiset.yaml"
    archive_file_path = os.path.join(tmp_path, archive_file_name)
    with open(archive_file_path, "w") as f:
        f.write(" \n")

    # Does it fail, as it should (more like a failsafe assertion)
    result = validate_bids(tmp_path)
    assert len(result["path_tracking"]) == 1

    # Does the parameter work?
    result = validate_bids(tmp_path, exclude_files=[archive_file_name])
    assert len(result["path_tracking"]) == 0


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_accept_non_bids_dir(bids_examples, tmp_path):
    from bidsschematools.validator import validate_bids

    dataset = "asl003"
    dataset_reference = os.path.join(bids_examples, dataset)
    tmp_path = str(tmp_path)
    shutil.copytree(dataset_reference, tmp_path, dirs_exist_ok=True)

    # remove `dataset_description.json`
    os.remove(os.path.join(tmp_path, "dataset_description.json"))

    # Does it fail, as it should (more like a failsafe assertion)
    with pytest.raises(
        ValueError,
        match="None of the files in the input list are part of a BIDS dataset. Aborting.",
    ):
        _ = validate_bids(tmp_path)

    # Does the parameter work?
    result = validate_bids(tmp_path, accept_non_bids_dir=True)
    assert len(result["path_tracking"]) == 0


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
@pytest.mark.parametrize("dataset", BIDS_ERROR_SELECTION)
def test_error_datasets(bids_error_examples, dataset):
    target = os.path.join(bids_error_examples, dataset)
    result = validate_bids(
        target,
        report_path=True,
    )
    # Are there non-validated files?
    assert len(result["path_tracking"]) != 0


def test_gitdir(bids_examples, tmp_path):
    """Maybe better handled in example data?"""

    selected_dir = os.path.join(bids_examples, BIDS_SELECTION[0])
    tmp_path = str(tmp_path)
    shutil.copytree(selected_dir, tmp_path, dirs_exist_ok=True)

    os.makedirs(os.path.join(tmp_path, ".git"))
    with open(os.path.join(tmp_path, ".git", "config"), "w") as temp_file:
        temp_file.write("")
    result = validate_bids(tmp_path)
    assert len(result["path_tracking"]) == 0


def test_select_schema_path(bids_examples, tmp_path):
    dataset = "asl003"
    dataset_path = os.path.join(bids_examples, dataset)

    # Does fallback to None work without any `raise`?
    schema_path = select_schema_path(dataset_path)
    assert schema_path is None


def test_bids_schema_versioncheck(monkeypatch, schema_dir):
    """Test incompatible version."""
    import bidsschematools as bst

    schema_dir = bst.data.load.readable("schema")
    assert bst.validator._bids_schema_versioncheck(schema_dir)
    monkeypatch.setattr(bst, "__version__", "99.99.99")
    assert not bst.validator._bids_schema_versioncheck(schema_dir)
