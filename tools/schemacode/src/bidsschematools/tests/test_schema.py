"""Tests for the bidsschematools package."""

import json
import os
import subprocess
from collections.abc import Mapping

import pytest
from jsonschema.exceptions import ValidationError

from bidsschematools import __bids_version__, schema, types

from ..data import load


def test__get_bids_version(schema_dir):
    # Is the version being read in correctly?
    bids_version = schema._get_bids_version(schema_dir)
    assert bids_version == __bids_version__


def test__get_bids_version_fallback(tmp_path):
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
            "2022-01-05T13:16:30Z",  # UTC indicator is allowed
            "2022-01-05T13:16:30.05Z",
            "2022-01-05T13:16:30+01:00",  # integral offsets are allowed
            "2022-01-05T13:16:30-05:00",
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
            assert bool(search.fullmatch(test_string)), (
                f"'{test_string}' is not a valid match for the pattern '{search.pattern}'"
            )

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
            "2022-01-05T13:16:30U",  # Only Z is permitted
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
            assert not bool(search.fullmatch(test_string)), (
                f"'{test_string}' should not be a valid match for the pattern '{search.pattern}'"
            )


def test_format_consistency(schema_obj):
    """Test that the "Format" field is consistent with objects.formats."""
    assert set(schema_obj.objects.metadata.Format.enum) == schema_obj.objects.formats.keys()


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

    orig = {
        "objects": {
            "enums": {
                "left": {"value": "L"},
                "right": {"value": "R"},
            },
            "entities.hemisphere": {
                "name": "hemi",
                "enum": [
                    {"$ref": "objects.enums.left.value"},
                    {"$ref": "objects.enums.right.value"},
                ],
            },
        },
    }

    sch = types.Namespace.build(orig)
    dereffed = schema.dereference(sch)
    assert dereffed == {
        "objects": {
            "enums": {
                "left": {"value": "L"},
                "right": {"value": "R"},
            },
            "entities": {
                "hemisphere": {
                    "name": "hemi",
                    "enum": ["L", "R"],
                },
            },
        },
    }


def test_namespace_to_dict():
    def check_for_namespaces(obj):
        if isinstance(obj, dict):
            [check_for_namespaces(val) for val in obj.values()]
        elif isinstance(obj, list):
            [check_for_namespaces(val) for val in obj]
        elif isinstance(obj, types.Namespace):
            raise ValueError("Namespace object found in dict")

    check_for_namespaces(schema.load_schema().to_dict())


def test_valid_schema():
    """Test that a valid schema does not raise an error."""
    namespace = schema.load_schema()
    schema.validate_schema(namespace)


@pytest.mark.parametrize("regex_variant", ["default", "nonunicode", "python"])
def test_valid_schema_with_check_jsonschema(tmp_path, regex_variant):
    """
    Test that the BIDS schema is valid against the metaschema when validation is done
    using the `check-jsonschema` CLI
    """
    bids_schema = schema.load_schema().to_dict()
    metaschema_path = str(load.readable("metaschema.json"))

    # Save BIDS schema to a temporary file
    bids_schema_path = tmp_path / "bids_schema.json"
    bids_schema_path.write_text(json.dumps(bids_schema))

    # Invoke the check-jsonschema to validate the BIDS schema
    try:
        subprocess.run(
            [
                "check-jsonschema",
                "--regex-variant",
                regex_variant,
                "--schemafile",
                metaschema_path,
                str(bids_schema_path),
            ],
            stdout=subprocess.PIPE,  # Capture stdout
            stderr=subprocess.STDOUT,  # Set stderr to into stdout
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        pytest.fail(
            f"check-jsonschema failed with code {e.returncode}:\n{e.stdout}", pytrace=False
        )


def test_add_legal_field():
    """Test that adding a legal field does not raise an error."""
    namespace = schema.load_schema()
    namespace["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "optional"
    schema.validate_schema(namespace)


def test_invalid_value():
    """Test that an invalid value raises an error."""
    namespace = schema.load_schema()
    namespace["rules"]["files"]["deriv"]["preprocessed_data"]["anat_nonparametric_common"][
        "entities"
    ]["density"] = "invalid"
    with pytest.raises(ValidationError) as e:
        schema.validate_schema(namespace)
    print(e.value)
    assert "invalid" in str(e.value)
