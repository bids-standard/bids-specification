import re

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
    nii_rule = rules._entity_rule(rule, schema_obj)
    assert nii_rule == {
        "regex": (
            r"sub-(?P<subject>[0-9a-zA-Z+]+)/"
            r"(?:ses-(?P<session>[0-9a-zA-Z+]+)/)?"
            r"(?P<datatype>anat)/"
            r"(?(subject)sub-(?P=subject)_)"
            r"(?(session)ses-(?P=session)_)"
            r"(?P<suffix>T1w)"
            r"(?P<extension>\.nii)\Z"
        ),
        "mandatory": False,
    }

    assert re.match(nii_rule["regex"], "sub-01/anat/sub-01_T1w.nii")
    assert re.match(nii_rule["regex"], "sub-01/ses-01/anat/sub-01_ses-01_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01/anat/sub-02_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01/sub-01_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01/ses-01/anat/sub-01_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01/anat/sub-01_ses-01_T1w.nii")
    assert not re.match(nii_rule["regex"], "sub-01/ses-01/anat/sub-01_ses-02_T1w.nii")

    # Sidecar entities are optional
    rule = Namespace.build(
        {
            "datatypes": ["anat", ""],
            "entities": {"subject": "optional", "session": "optional"},
            "suffixes": ["T1w"],
            "extensions": [".json"],
        }
    )
    json_rule = rules._entity_rule(rule, schema_obj)
    assert json_rule == {
        "regex": (
            r"(?:sub-(?P<subject>[0-9a-zA-Z+]+)/)?"
            r"(?:ses-(?P<session>[0-9a-zA-Z+]+)/)?"
            r"(?:(?P<datatype>anat)/)?"
            r"(?(subject)sub-(?P=subject)_)"
            r"(?(session)ses-(?P=session)_)"
            r"(?P<suffix>T1w)"
            r"(?P<extension>\.json)\Z"
        ),
        "mandatory": False,
    }
    assert re.match(json_rule["regex"], "sub-01/anat/sub-01_T1w.json")
    assert re.match(json_rule["regex"], "sub-01/sub-01_T1w.json")
    assert re.match(json_rule["regex"], "T1w.json")
    assert re.match(json_rule["regex"], "sub-01/ses-01/anat/sub-01_ses-01_T1w.json")
    assert re.match(json_rule["regex"], "sub-01/ses-01/sub-01_ses-01_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01/anat/sub-02_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01_T1w.json")
    assert not re.match(json_rule["regex"], "ses-01_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01/ses-01/anat/sub-01_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01/anat/sub-01_ses-01_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01/ses-01/ses-01_T1w.json")
    assert not re.match(json_rule["regex"], "sub-01/ses-01/anat/sub-01_ses-02_T1w.json")


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
        "regex": r"(?P<stem>(?s:README))(?P<extension>|\.md)\Z",
        "mandatory": True,
    }

    rule = Namespace.build(
        {"stem": "participants", "level": "optional", "extensions": [".tsv", ".json"]}
    )
    assert rules._stem_rule(rule) == {
        "regex": r"(?P<stem>(?s:participants))(?P<extension>\.tsv|\.json)\Z",
        "mandatory": False,
    }

    # Wildcard stem, with datatype
    rule = Namespace.build(
        {
            "stem": "*",
            "datatypes": ["phenotype"],
            "level": "optional",
            "extensions": [".tsv", ".json"],
        }
    )
    assert rules._stem_rule(rule) == {
        "regex": r"(?P<datatype>phenotype)/(?P<stem>(?s:.*))(?P<extension>\.tsv|\.json)\Z",
        "mandatory": False,
    }


def test_path_rule():
    rule = Namespace.build({"path": "dataset_description.json", "level": "required"})
    assert rules._path_rule(rule) == {
        "regex": r"(?P<path>dataset_description\.json)(?:/.*)?\Z",
        "mandatory": True,
    }

    rule = Namespace.build({"path": "LICENSE", "level": "optional"})
    assert rules._path_rule(rule) == {"regex": r"(?P<path>LICENSE)(?:/.*)?\Z", "mandatory": False}


def test_regexify_all():
    schema_all, _ = rules.regexify_all()

    # Check if expected keys are present in all entries
    for entry in schema_all:
        assert "regex" in entry
        assert "mandatory" in entry
