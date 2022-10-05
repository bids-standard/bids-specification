"""Tests for the bidsschematools package."""
import os
from collections.abc import Mapping

import pytest

from bidsschematools import __bids_version__, schema, types


def test__get_bids_version(tmp_path):
    # Is the version being read in correctly?
    schema_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        os.pardir,
        "data",
        "schema",
    )
    bids_version = schema._get_bids_version(schema_path)
    assert bids_version == __bids_version__

    # Does fallback to unknown development version work?
    expected_version = "1.2.3-dev"
    schema_path = os.path.join(tmp_path, "whatever", expected_version)
    bids_version = schema._get_bids_version(schema_path)
    assert bids_version == expected_version

    # Does fallback to path quoting work?
    schema_path = os.path.join(tmp_path, "whatever", "undocumented_schema_dir")
    bids_version = schema._get_bids_version(schema_path)
    assert bids_version == schema_path


def test_load_schema(schema_dir):
    """Smoke test for bidsschematools.schema.load_schema."""
    # Pointing to a nonexistent directory should raise a ValueError
    bad_path = "/path/to/nowhere"
    with pytest.raises(FileNotFoundError):
        schema.load_schema(bad_path)

    # Otherwise the function should return a dictionary
    schema_obj = schema.load_schema(schema_dir)
    assert isinstance(schema_obj, Mapping)

    # Check that it is fully dereferenced
    assert "$ref" not in str(schema_obj)


def test_object_definitions(schema_obj):
    """Ensure that object definitions in the schema contain required fields."""
    for obj_type, obj_type_def in schema_obj["objects"].items():
        for obj_key, obj_def in obj_type_def.items():
            # Private/inheritable definitions (ones starting with "_") do not need to conform to
            # the same rules as user-facing terms, so we skip them
            if obj_key.startswith("_"):
                continue

            assert "display_name" in obj_def, obj_key
            assert "description" in obj_def.keys(), obj_key
            if obj_type in ("columns", "entities", "metadata"):
                assert "name" in obj_def
            elif obj_type in ("datatypes", "extensions", "suffixes"):
                assert "value" in obj_def


def test_formats(schema_obj):
    """Test valid string patterns allowed by the specification."""
    import re

    # Check that valid strings match the search pattern.
    GOOD_PATTERNS = {
        "label": ["01", "test", "test01", "Test01"],
        "index": ["01", "1", "10000", "00001"],
        "string": ["any string is valid."],
        "integer": ["5", "10", "-5", "-10"],
        "number": [
            "5",  # integers are allowed
            "3.14",  # floats too
            "-5",  # they can be negative
            "-3.14",
            "1e3",  # scientific notation is allowed
            "-2.1E+5",
        ],
        "boolean": ["true", "false"],
        "date": ["2022-01-05", "2022-01-05UTC", "2022-50-50"],
        "datetime": [
            "2022-01-05T13:16:30",
            "2022-01-05T13:16:30.5",  # subsecond resolution is allowed
            "2022-01-05T13:16:30.000005",  # up to 6 decimal points
            "2022-01-05T13:16:30UTC",  # timezones are allowed
            "2022-01-05T13:16:30.05UTC",
        ],
        "time": [
            "13:16:30",
            "09:00:00",
            "9:00:00",  # leading zeros are not required for hours
        ],
        "unit": ["any string is valid."],
        "file_relative": [
            "file_in_same_directory.txt",
            "../../relative/path/file.txt",
            "sub-01/path/file.txt",
        ],
        "stimuli_relative": ["any/arbitrary/path/file.txt"],
        "dataset_relative": ["any/arbitrary/path/file.txt"],
        "participant_relative": ["any/arbitrary/path/file.txt"],
        "rrid": ["RRID:SCR_017398"],
        "uri": ["foo://example.com:8042/over/there?name=ferret#nose"],
        "bids_uri": [
            "bids::sub-01/fmap/sub-01_dir-AP_epi.nii.gz",
            "bids:ds000001:sub-02/anat/sub-02_T1w.nii.gz",
            "bids:myderivatives:sub-03/func/sub-03_task-rest_space-MNI152_bold.nii.gz",
        ],
    }
    for pattern, test_list in GOOD_PATTERNS.items():
        pattern_format = schema_obj["objects"]["formats"][pattern]["pattern"]
        search_pattern = "^" + pattern_format + "$"
        search = re.compile(search_pattern)
        for test_string in test_list:
            assert bool(
                search.fullmatch(test_string)
            ), f"'{test_string}' is not a valid match for the pattern '{search.pattern}'"

    # Check that invalid strings do not match the search pattern.
    BAD_PATTERNS = {
        "label": ["test_01", "!", "010101-", "01-01", "-01"],
        "index": ["test", "0.1", "0-1", "0_1"],
        "string": [],
        "integer": ["3.14", "-3.14", "1.", "-1.", "string", "s1", "1%", "one"],
        "number": ["string", "1%"],
        "boolean": ["True", "False", "T", "F"],
        "date": [
            "05-01-2022",  # MM-DD-YYYY or DD-MM-YYYY
            "05/01/2022",  # MM/DD/YYYY or DD/MM/YYYY
        ],
        "datetime": [
            "2022-01-05T13:16:30.1000005",  # too many decimal points
            "2022-01-05T13:16:30U",  # time zone too short
            "2022-01-05T13:16:30UTCUTC",  # time zone too long
            "2022-01-05T34:10:10",  # invalid time
        ],
        "time": [
            "34:10:10",  # invalid time
            "24:00:00",  # should be 00:00:00
            "00:60:00",  # should be 01:00:00
            "00:00:60",  # should be 00:01:00
            "01:23",  # lacks either hours or seconds
        ],
        "unit": [],
        "file_relative": [
            "/path/with/starting/slash/file.txt",
        ],
        "stimuli_relative": [
            "/path/with/starting/slash/file.txt",
            "stimuli/path/file.txt",
        ],
        "dataset_relative": [
            "/path/with/starting/slash/file.txt",
        ],
        "participant_relative": [
            "/path/with/starting/slash/file.txt",
            "sub-01/path/file.txt",
        ],
        "rrid": [
            "RRID:",  # empty one
        ],
        "uri": [
            # "ftp://",  # lacks anything but protocol. This should fail, but doesn't ATM.
        ],
        "bids_uri": [],
    }
    for pattern, test_list in BAD_PATTERNS.items():
        pattern_format = schema_obj["objects"]["formats"][pattern]["pattern"]
        search_pattern = f"^{pattern_format}$"
        search = re.compile(search_pattern)
        for test_string in test_list:
            assert not bool(
                search.fullmatch(test_string)
            ), f"'{test_string}' should not be a valid match for the pattern '{search.pattern}'"


def test_dereferencing():
    orig = {
        "ReferencedObject": {
            "Property1": "value1",
            "Property2": "value2",
        },
        "ReferencingObject": {
            "$ref": "ReferencedObject",
            "Property2": "value4",
        },
    }
    dereffed = schema.dereference(orig)
    assert dereffed == {
        "ReferencedObject": {
            "Property1": "value1",
            "Property2": "value2",
        },
        "ReferencingObject": {
            "Property1": "value1",
            "Property2": "value4",
        },
    }

    orig = {
        "raw.func": {
            "suffix": ["bold", "cbv"],
            "extensions": [".nii", ".nii.gz"],
            "datatype": ["func"],
            "entities": {
                "subject": "required",
                "session": "optional",
                "task": "required",
                "dir": "optional",
            },
        },
        "derived.func": {
            "$ref": "raw.func",
            "entities": {
                "$ref": "raw.func.entities",
                "space": "optional",
                "desc": "optional",
            },
        },
    }

    sch = types.Namespace.build(orig)
    dereffed = schema.dereference(sch)
    assert dereffed == {
        "raw": {
            "func": {
                "suffix": ["bold", "cbv"],
                "extensions": [".nii", ".nii.gz"],
                "datatype": ["func"],
                "entities": {
                    "subject": "required",
                    "session": "optional",
                    "task": "required",
                    "dir": "optional",
                },
            }
        },
        "derived": {
            "func": {
                "suffix": ["bold", "cbv"],
                "extensions": [".nii", ".nii.gz"],
                "datatype": ["func"],
                "entities": {
                    "subject": "required",
                    "session": "optional",
                    "task": "required",
                    "dir": "optional",
                    "space": "optional",
                    "desc": "optional",
                },
            }
        },
    }

    orig = {
        "_DERIV_ENTS": {
            "space": "optional",
            "desc": "optional",
        },
        "raw.func": {
            "suffix": ["bold", "cbv"],
            "extensions": [".nii", ".nii.gz"],
            "datatype": ["func"],
            "entities": {
                "subject": "required",
                "session": "optional",
                "task": "required",
                "dir": "optional",
            },
        },
        "derived.func": {
            "$ref": "raw.func",
            "entities": {
                "$ref": "_DERIV_ENTS",
            },
        },
    }

    sch = types.Namespace.build(orig)
    dereffed = schema.dereference(sch)
    assert dereffed == {
        "_DERIV_ENTS": {
            "space": "optional",
            "desc": "optional",
        },
        "raw": {
            "func": {
                "suffix": ["bold", "cbv"],
                "extensions": [".nii", ".nii.gz"],
                "datatype": ["func"],
                "entities": {
                    "subject": "required",
                    "session": "optional",
                    "task": "required",
                    "dir": "optional",
                },
            }
        },
        "derived": {
            "func": {
                "suffix": ["bold", "cbv"],
                "extensions": [".nii", ".nii.gz"],
                "datatype": ["func"],
                "entities": {
                    "space": "optional",
                    "desc": "optional",
                },
            }
        },
    }
