import os
import shutil

import pytest

from .conftest import BIDS_ERROR_SELECTION, BIDS_SELECTION


def test__add_entity():
    from bidsschematools.validator import _add_entity

    # Test empty input and directory creation and required entity
    regex_entities = ""
    entity = "subject"
    entity_shorthand = "sub"
    variable_field = "[0-9a-zA-Z]+"
    requirement_level = "required"

    _regex_entities = _add_entity(
        regex_entities,
        entity,
        entity_shorthand,
        variable_field,
        requirement_level,
    )

    assert _regex_entities == "sub-(?P=subject)"

    # Test append input and optional entity
    regex_entities = (
        "sub-(?P=subject)(|_ses-(?P=session))"
        "(|_task-(?P<task>[0-9a-zA-Z]+))(|_trc-(?P<tracer>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_run-(?P<run>[0-9a-zA-Z]+))"
    )
    entity = "recording"
    entity_shorthand = "recording"
    variable_field = "[0-9a-zA-Z]+"
    requirement_level = "optional"

    _regex_entities = _add_entity(
        regex_entities,
        entity,
        entity_shorthand,
        variable_field,
        requirement_level,
    )

    assert (
        _regex_entities == "sub-(?P=subject)(|_ses-(?P=session))"
        "(|_task-(?P<task>[0-9a-zA-Z]+))(|_trc-(?P<tracer>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_run-(?P<run>[0-9a-zA-Z]+))"
        "(|_recording-(?P<recording>[0-9a-zA-Z]+))"
    )


def test__add_extensions():
    from bidsschematools.validator import _add_extensions

    # Test single extension
    regex_string = (
        "sub-(?P=subject)(|_ses-(?P=session))"
        "_sample-(?P<sample>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))_photo"
    )
    variant = {
        "suffixes": ["photo"],
        "extensions": [".jpg"],
        "entities": {
            "subject": "required",
            "session": "optional",
            "sample": "required",
            "acquisition": "optional",
        },
    }
    _regex_string = _add_extensions(regex_string, variant)

    assert (
        _regex_string == "sub-(?P=subject)(|_ses-(?P=session))"
        "_sample-(?P<sample>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))_photo\\.jpg"
    )

    # Test multiple extensions
    regex_string = (
        "sub-(?P=subject)(|_ses-(?P=session))"
        "_sample-(?P<sample>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))_photo"
    )
    variant = {
        "suffixes": ["photo"],
        "extensions": [".jpg", ".png", ".tif"],
        "entities": {
            "subject": "required",
            "session": "optional",
            "sample": "required",
            "acquisition": "optional",
        },
    }
    _regex_string = _add_extensions(regex_string, variant)

    assert (
        _regex_string == "sub-(?P=subject)(|_ses-(?P=session))"
        "_sample-(?P<sample>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        "_photo(\\.jpg|\\.png|\\.tif)"
    )


def test__add_subdirs():
    from bidsschematools.validator import _add_subdirs

    regex_string = "sub-(?P=subject)_sessions\\.(tsv|json)"
    variant = {
        "suffixes": ["sessions"],
        "extensions": [".tsv", ".json"],
        "entities": {"subject": "required"},
    }
    datatype = "tabular_metadata"
    entity_definitions = {
        "acquisition": {
            "display_name": "Acquisition",
            "name": "acq",
            "type": "string",
            "format": "label",
        },
        "session": {
            "display_name": "Session",
            "name": "ses",
            "type": "string",
            "format": "label",
        },
        "subject": {
            "display_name": "Subject",
            "name": "sub",
            "type": "string",
            "format": "label",
        },
    }
    formats = {
        "label": {
            "pattern": "[0-9a-zA-Z]+",
        }
    }
    modality_datatypes = [
        "anat",
        "dwi",
        "fmap",
        "func",
        "perf",
        "eeg",
        "ieeg",
        "meg",
        "beh",
        "pet",
        "micr",
    ]
    _regex_string = _add_subdirs(
        regex_string, variant, datatype, entity_definitions, formats, modality_datatypes
    )

    assert _regex_string == "/sub-(?P<subject>[0-9a-zA-Z]+)/sub-(?P=subject)_sessions\\.(tsv|json)"


def test__add_suffixes():
    from bidsschematools.validator import _add_suffixes

    # Test single expansion
    regex_entities = "sub-(?P=subject)"
    variant = {
        "suffixes": ["sessions"],
        "extensions": [
            ".tsv",
            ".json",
        ],
        "entities": {"subject": "required"},
    }
    regex_string = "sub-(?P=subject)_sessions"

    _regex_string = _add_suffixes(regex_entities, variant)

    assert _regex_string == regex_string

    # Test multiple expansions
    regex_entities = (
        "sub-(?P=subject)(|_ses-(?P=session))"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_dir-(?P<direction>[0-9a-zA-Z]+))(|_run-(?P<run>[0-9a-zA-Z]+))"
        "(|_recording-(?P<recording>[0-9a-zA-Z]+))"
    )
    variant = {
        "suffixes": [
            "physio",
            "stim",
        ],
        "extensions": [
            ".tsv.gz",
            ".json",
        ],
        "entities": {
            "subject": "required",
            "session": "optional",
            "acquisition": "optional",
            "reconstruction": "optional",
            "direction": "optional",
            "run": "optional",
            "recording": "optional",
        },
    }
    regex_string = (
        "sub-(?P=subject)(|_ses-(?P=session))"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_dir-(?P<direction>[0-9a-zA-Z]+))(|_run-(?P<run>[0-9a-zA-Z]+))"
        "(|_recording-(?P<recording>[0-9a-zA-Z]+))"
        "_(physio|stim)"
    )

    _regex_string = _add_suffixes(regex_entities, variant)

    assert _regex_string == regex_string


@pytest.mark.parametrize("extension", ["bvec", "json", "tsv"])
def test__inheritance_expansion(extension):
    from bidsschematools.validator import _inheritance_expansion

    # test .json
    base_entry = (
        r".*?/sub-(?P<subject>[0-9a-zA-Z]+)/"
        r"(|ses-(?P<session>[0-9a-zA-Z]+)/)func/sub-(?P=subject)"
        r"(|_ses-(?P=session))_task-(?P<task>[0-9a-zA-Z]+)"
        r"(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        r"(|_ce-(?P<ceagent>[0-9a-zA-Z]+))"
        r"(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        r"(|_dir-(?P<direction>[0-9a-zA-Z]+))"
        r"(|_run-(?P<run>[0-9]*[1-9]+[0-9]*))"
        r"(|_echo-(?P<echo>[0-9]*[1-9]+[0-9]*))"
        r"_phase(\.nii\.gz|\.nii|\.{})$".format(extension)
    )
    expected_entries = [
        ".*?/sub-(?P<subject>[0-9a-zA-Z]+)/"
        "(|ses-(?P<session>[0-9a-zA-Z]+)/)sub-(?P=subject)"
        "(|_ses-(?P=session))_task-(?P<task>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        "(|_ce-(?P<ceagent>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_dir-(?P<direction>[0-9a-zA-Z]+))"
        "(|_run-(?P<run>[0-9]*[1-9]+[0-9]*))"
        "(|_echo-(?P<echo>[0-9]*[1-9]+[0-9]*))"
        "_phase(\\.nii\\.gz|\\.nii|\\.{})$".format(extension),
        ".*?/task-(?P<task>[0-9a-zA-Z]+)"
        "(|_acq-(?P<acquisition>[0-9a-zA-Z]+))"
        "(|_ce-(?P<ceagent>[0-9a-zA-Z]+))"
        "(|_rec-(?P<reconstruction>[0-9a-zA-Z]+))"
        "(|_dir-(?P<direction>[0-9a-zA-Z]+))"
        "(|_run-(?P<run>[0-9]*[1-9]+[0-9]*))"
        "(|_echo-(?P<echo>[0-9]*[1-9]+[0-9]*))"
        "_phase(\\.nii\\.gz|\\.nii|\\.{})$".format(extension),
    ]

    inheritance_expanded_entries = _inheritance_expansion(base_entry, datatype="func")
    assert inheritance_expanded_entries == expected_entries


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
        report_path=True,
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
