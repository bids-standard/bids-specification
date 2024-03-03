from bidsschematools import rules

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
    assert rules._entity_rule(rule, schema_obj) == {
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
    assert rules._entity_rule(rule, schema_obj) == {
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

    main, sidecar = rules._split_inheritance_rules(rule)
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
    (main2,) = rules._split_inheritance_rules(main)
    assert main2 == {
        "datatypes": ["anat"],
        "entities": {"subject": "required", "session": "optional"},
        "suffixes": ["T1w"],
        "extensions": [".nii"],
    }


def test_stem_rule():
    rule = Namespace.build({"stem": "README", "level": "required", "extensions": ["", ".md"]})
    assert rules._stem_rule(rule) == {
        "regex": r"README(?P<extension>|\.md)",
        "mandatory": True,
    }

    rule = Namespace.build(
        {"stem": "participants", "level": "optional", "extensions": [".tsv", ".json"]}
    )
    assert rules._stem_rule(rule) == {
        "regex": r"participants(?P<extension>\.tsv|\.json)",
        "mandatory": False,
    }


def test_path_rule():
    rule = Namespace.build({"path": "dataset_description.json", "level": "required"})
    assert rules._path_rule(rule) == {
        "regex": r"dataset_description\.json",
        "mandatory": True,
    }

    rule = Namespace.build({"path": "LICENSE", "level": "optional"})
    assert rules._path_rule(rule) == {"regex": "LICENSE", "mandatory": False}


def test_regexify_all():
    schema_all, _ = rules.regexify_all()

    # Check if expected keys are present in all entries
    for entry in schema_all:
        assert "regex" in entry
        assert "mandatory" in entry
