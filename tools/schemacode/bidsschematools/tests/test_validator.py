import os
import shutil

import pytest

from .. import validator
from ..types import Namespace
from .conftest import BIDS_ERROR_SELECTION, BIDS_SELECTION


def test_path_rule():
    rule = Namespace.build({"path": "dataset_description.json", "level": "required"})
    assert validator._path_rule(rule) == {
        "regex": r"dataset_description\.json",
        "mandatory": True,
    }

    rule = Namespace.build({"path": "LICENSE", "level": "optional"})
    assert validator._path_rule(rule) == {"regex": "LICENSE", "mandatory": False}


def test_stem_rule():
    rule = Namespace.build({"stem": "README", "level": "required", "extensions": ["", ".md"]})
    assert validator._stem_rule(rule) == {
        "regex": r"README(?P<extension>|\.md)",
        "mandatory": True,
    }

    rule = Namespace.build(
        {"stem": "participants", "level": "optional", "extensions": [".tsv", ".json"]}
    )
    assert validator._stem_rule(rule) == {
        "regex": r"participants(?P<extension>\.tsv|\.json)",
        "mandatory": False,
    }


def test_entity_rule(schema_obj):
    # Simple
    rule = Namespace.build(
        {
            "datatypes": ["anat"],
            "entities": {"subject": "required", "session": "optional"},
            "suffixes": ["T1w"],
            "extensions": [".nii"],
        }
    )
    assert validator._entity_rule(rule, schema_obj) == {
        "regex": (
            r"sub-(?P<subject>[0-9a-zA-Z]+)/"
            r"(?:ses-(?P<session>[0-9a-zA-Z]+)/)?"
            r"(?P<datatype>anat)/"
            r"sub-(?P=subject)_"
            r"(?:ses-(?P=session)_)?"
            r"(?P<suffix>T1w)"
            r"(?P<extension>\.nii)"
        ),
        "mandatory": False,
    }

    # Sidecar entities are optional
    rule = Namespace.build(
        {
            "datatypes": ["anat", ""],
            "entities": {"subject": "optional", "session": "optional"},
            "suffixes": ["T1w"],
            "extensions": [".json"],
        }
    )
    assert validator._entity_rule(rule, schema_obj) == {
        "regex": (
            r"(?:sub-(?P<subject>[0-9a-zA-Z]+)/)?"
            r"(?:ses-(?P<session>[0-9a-zA-Z]+)/)?"
            r"(?:(?P<datatype>anat)/)?"
            r"(?:sub-(?P=subject)_)?"
            r"(?:ses-(?P=session)_)?"
            r"(?P<suffix>T1w)"
            r"(?P<extension>\.json)"
        ),
        "mandatory": False,
    }


def test_split_inheritance_rules():
    rule = {
        "datatypes": ["anat"],
        "entities": {"subject": "required", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".nii", ".json"],
    }

    main, sidecar = validator.split_inheritance_rules(rule)
    assert main == {
        "datatypes": ["anat"],
        "entities": {"subject": "required", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".nii"],
    }
    assert sidecar == {
        "datatypes": ["", "anat"],
        "entities": {"subject": "optional", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".json"],
    }

    # Can't split again
    (main2,) = validator.split_inheritance_rules(main)
    assert main2 == {
        "datatypes": ["anat"],
        "entities": {"subject": "required", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".nii"],
    }


def test_inheritance_examples():
    from bidsschematools.validator import validate_bids

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
        accept_dummy_paths=True,
    )

    assert result["path_tracking"] == incorrect_inheritance


def test_load_all():
    from bidsschematools.validator import load_all

    # schema_path = "/usr/share/bids-schema/1.7.0/"
    schema_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        os.pardir,
        "data",
        "schema",
    )
    schema_all, _ = load_all(schema_path)

    # Check if expected keys are present in all entries
    for entry in schema_all:
        assert "regex" in list(entry.keys())
        assert "mandatory" in list(entry.keys())


def test_write_report(tmp_path):
    from bidsschematools.validator import write_report

    validation_result = {}

    validation_result["schema_tracking"] = [
        {
            "regex": ".*?/sub-(?P<subject>[0-9a-zA-Z]+)/"
            "(|ses-(?P<session>[0-9a-zA-Z]+)/)anat/sub-(?P=subject)"
            "(|_ses-(?P=session))(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
            "(|_ce-(?P<ceagent>[0-9a-zA-Z]+))"
            "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
            "(|_run-(?P<run>[0-9a-zA-Z]+))"
            "(|_part-(?P<part>(mag|phase|real|imag)))"
            "_(T1w|T2w|PDw|T2starw|FLAIR|inplaneT1|inplaneT2|PDT2|angio|T2star)"
            "\\.(nii.gz|nii|json)$",
            "mandatory": False,
        }
    ]
    validation_result["schema_listing"] = [
        {
            "regex": ".*?/sub-(?P<subject>[0-9a-zA-Z]+)/"
            "(|ses-(?P<session>[0-9a-zA-Z]+)/)anat/sub-(?P=subject)"
            "(|_ses-(?P=session))(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
            "(|_ce-(?P<ceagent>[0-9a-zA-Z]+))"
            "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
            "(|_run-(?P<run>[0-9a-zA-Z]+))"
            "(|_part-(?P<part>(mag|phase|real|imag)))"
            "_(T1w|T2w|PDw|T2starw|FLAIR|inplaneT1|inplaneT2|PDT2|angio|T2star)"
            "\\.(nii.gz|nii|json)$",
            "mandatory": False,
        }
    ]
    validation_result["path_tracking"] = [
        "/home/chymera/.data2/datalad/000026/"
        "rawdata/sub-EXC022/anat/sub-EXC022_ses-MRI_flip-1_VFA.nii.gz"
    ]
    validation_result["path_listing"] = [
        "/home/chymera/.data2/datalad/000026/"
        "rawdata/sub-EXC022/anat/sub-EXC022_ses-MRI_flip-1_VFA.nii.gz"
    ]

    report_path = os.path.join(
        tmp_path,
        "output_bids_validator_xs_write.log",
    )
    expected_report_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "data/expected_bids_validator_xs_write.log",
    )
    write_report(validation_result, report_path=report_path)
    with open(report_path, "r") as f:
        report_text = f.read()
    with open(expected_report_path, "r") as f:
        expected_report_text = f.read()
    assert report_text == expected_report_text


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
@pytest.mark.parametrize("dataset", BIDS_SELECTION)
def test_bids_datasets(bids_examples, tmp_path, dataset):
    from bidsschematools.validator import validate_bids

    schema_path = "{module_path}/data/schema/"

    # Validate per dataset:
    target = os.path.join(bids_examples, dataset)
    result = validate_bids(
        target,
        schema_version=schema_path,
    )
    # Have all files been validated?
    assert len(result["path_tracking"]) == 0


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_validate_bids(bids_examples, tmp_path):
    from bidsschematools.validator import validate_bids

    schema_path = "{module_path}/data/schema/"

    # Create input for file list based validation
    selected_dir = os.path.join(bids_examples, BIDS_SELECTION[0])
    selected_paths = []
    for root, dirs, files in os.walk(selected_dir, topdown=False):
        for f in files:
            selected_path = os.path.join(root, f)
            selected_paths.append(selected_path)
    # Do version fallback work?
    result = validate_bids(selected_paths, schema_version=None)
    # Does default log path specification work?
    result = validate_bids(selected_paths, schema_version=schema_path, report_path=True)

    # Does custom log path specification work?
    result = validate_bids(
        selected_paths,
        schema_version=schema_path,
        report_path=os.path.join(tmp_path, "test_bids.log"),
    )
    # Have all files been validated?
    assert len(result["path_tracking"]) == 0

    # Is the schema version recorded correctly?
    schema_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        os.pardir,
        "data",
        "schema",
    )
    with open(os.path.join(schema_path, "BIDS_VERSION")) as f:
        expected_version = f.readline().rstrip()
    assert result["bids_version"] == expected_version


@pytest.mark.skipif(
    os.environ.get("SCHEMACODE_TESTS_NONETWORK") is not None,
    reason="no network",
)
def test_broken_json_dataset(bids_examples, tmp_path):
    """Perhaps this can be integrated into
    https://github.com/bids-standard/bids-error-examples ."""
    from bidsschematools.validator import validate_bids

    dataset = "asl003"
    dataset_path = os.path.join(bids_examples, dataset)
    dataset_json = os.path.join(dataset_path, "dataset_description.json")

    broken_json = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        "data/broken_dataset_description.json",
    )
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
@pytest.mark.parametrize("dataset", BIDS_ERROR_SELECTION)
def test_error_datasets(bids_error_examples, dataset):
    from bidsschematools.validator import validate_bids

    schema_path = "{module_path}/data/schema/"

    target = os.path.join(bids_error_examples, dataset)
    result = validate_bids(
        target,
        schema_version=schema_path,
        report_path=True,
    )
    # Are there non-validated files?
    assert len(result["path_tracking"]) != 0


def test_gitdir(bids_examples, tmp_path):
    """Maybe better handled in example data?"""
    from distutils.dir_util import copy_tree

    from bidsschematools.validator import validate_bids

    selected_dir = os.path.join(bids_examples, BIDS_SELECTION[0])
    tmp_path = str(tmp_path)
    copy_tree(selected_dir, tmp_path)

    os.makedirs(os.path.join(tmp_path, ".git"))
    with open(os.path.join(tmp_path, ".git", "config"), "w") as temp_file:
        temp_file.write("")
    result = validate_bids(tmp_path)
    assert len(result["path_tracking"]) == 0
