import os

from bidsschematools import parse

from ..types import Namespace


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
    assert parse._entity_rule(rule, schema_obj) == {
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
    assert parse._entity_rule(rule, schema_obj) == {
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

    main, sidecar = parse._split_inheritance_rules(rule)
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
    (main2,) = parse._split_inheritance_rules(main)
    assert main2 == {
        "datatypes": ["anat"],
        "entities": {"subject": "required", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".nii"],
    }


def test_stem_rule():
    rule = Namespace.build({"stem": "README", "level": "required", "extensions": ["", ".md"]})
    assert parse._stem_rule(rule) == {
        "regex": r"README(?P<extension>|\.md)",
        "mandatory": True,
    }

    rule = Namespace.build(
        {"stem": "participants", "level": "optional", "extensions": [".tsv", ".json"]}
    )
    assert parse._stem_rule(rule) == {
        "regex": r"participants(?P<extension>\.tsv|\.json)",
        "mandatory": False,
    }


def test_path_rule():
    rule = Namespace.build({"path": "dataset_description.json", "level": "required"})
    assert parse._path_rule(rule) == {
        "regex": r"dataset_description\.json",
        "mandatory": True,
    }

    rule = Namespace.build({"path": "LICENSE", "level": "optional"})
    assert parse._path_rule(rule) == {"regex": "LICENSE", "mandatory": False}


def test_regexify_all():
    # schema_path = "/usr/share/bids-schema/1.7.0/"
    schema_path = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        os.pardir,
        "data",
        "schema",
    )
    schema_all, _ = parse.regexify_all(schema_path)

    # Check if expected keys are present in all entries
    for entry in schema_all:
        assert "regex" in list(entry.keys())
        assert "mandatory" in list(entry.keys())
