"""Tests for the stimulus file rules."""

import re

import pytest

from bidsschematools import rules

SUBJECT_DATATYPES = {"beh", "eeg", "emg", "func", "ieeg", "meg", "motion", "nirs"}
MEDIA_SUFFIXES = ("audio", "image", "video", "audiovideo")


@pytest.fixture(scope="module")
def raw_regexes(schema_obj):
    return [
        entry["regex"]
        for entry in rules.regexify_filename_rules(schema_obj.rules.files.raw, schema_obj, level=2)
    ]


def _matches(regexes, path):
    return any(re.match(regex, path) for regex in regexes)


def test_subject_stimulus_rules(schema_obj):
    """Subject-level stimulus rules mirror the /stimuli rules and require stim and task."""
    stimuli_rules = schema_obj.rules.files.raw.stimuli
    for suffix in MEDIA_SUFFIXES:
        root_rule = stimuli_rules[f"stimulus_{suffix}"]
        subject_rule = stimuli_rules[f"subject_stimulus_{suffix}"]
        assert set(root_rule.datatypes) == {"stimuli"}
        assert set(subject_rule.datatypes) == SUBJECT_DATATYPES
        assert subject_rule.suffixes == root_rule.suffixes == [suffix]
        assert subject_rule.extensions == root_rule.extensions
        for entity in ("subject", "task", "stimulus"):
            assert subject_rule.entities[entity] == "required"


def test_stimulus_entity_order(schema_obj):
    """stim follows task in subject-level names, and part precedes annot."""
    order = list(schema_obj.rules.entities)
    assert order.index("stimulus") == order.index("task") + 1
    assert order.index("part") < order.index("annotation")


def test_stimulus_selectors_use_short_entity_names(schema_obj):
    """Validators key context.entities by the short entity name (stim, annot)."""
    short_names = {entity.name for entity in schema_obj.objects.entities.values()}
    selectors = " ".join(
        selector
        for rule in schema_obj.rules.sidecars.stimuli.values()
        for selector in rule.get("selectors", [])
    )
    used = set(re.findall(r"entities\.([a-z]+)", selectors))
    assert used == {"stim", "annot"}
    assert used <= short_names
    assert "entities.stim == null" in schema_obj.rules.checks.events.EventsMissing.selectors


def test_stimulus_check_selectors(schema_obj):
    """Stimulus checks stay off non-stimulus events and datasets without /stimuli."""
    stim_presentation = schema_obj.rules.sidecars.events.StimulusPresentation.selectors
    assert 'datatype != "stimuli"' in stim_presentation
    stimuli_tsv_missing = schema_obj.rules.checks.stimuli.StimuliTsvForStimId.selectors
    assert 'exists("stimuli", "dataset") == 1' in stimuli_tsv_missing


def test_part_enum_on_mri_rules(schema_obj):
    """Every non-stimulus rule with a part entity keeps the MRI enum."""
    mri_parts = ["mag", "phase", "real", "imag"]
    checked = 0
    for group in (schema_obj.rules.files.raw, schema_obj.rules.files.deriv):
        for rule in group.values(level=2):
            if "part" not in rule.get("entities", {}) or "stimulus" in rule.entities:
                continue
            assert list(rule.entities.part.enum) == mri_parts
            checked += 1
    # anat, fmap, func, and derivative imaging rules
    assert checked > 20


def test_part_labels(schema_obj, raw_regexes):
    """MRI rules restrict part to complex-signal components; stimulus rules do not."""
    assert "enum" not in schema_obj.objects.entities.part
    assert _matches(raw_regexes, "sub-01/anat/sub-01_part-mag_T1w.nii.gz")
    assert not _matches(raw_regexes, "sub-01/anat/sub-01_part-chapter1_T1w.nii.gz")
    # Sidecar regexes relax entity levels but keep per-rule enums
    assert _matches(raw_regexes, "sub-01/anat/sub-01_part-mag_T1w.json")
    assert not _matches(raw_regexes, "sub-01/anat/sub-01_part-chapter1_T1w.json")
    assert not _matches(raw_regexes, "sub-01/func/sub-01_task-rest_part-chapter1_bold.json")
    assert _matches(raw_regexes, "stimuli/stim-movie01_part-1_audiovideo.mp4")
    assert _matches(
        raw_regexes,
        "sub-01/func/sub-01_task-movie_stim-movie01_run-1_part-chapter1_audiovideo.mkv",
    )


@pytest.mark.parametrize(
    ("path", "valid"),
    [
        ("stimuli/stim-face01_image.jpeg", True),
        ("stimuli/stim-movie01_annot-action_events.tsv", True),
        ("stimuli/stim-movie01_annotations.tsv", True),
        ("sub-01/beh/sub-01_task-dyad_stim-partner_audio.wav", True),
        ("sub-01/ses-01/eeg/sub-01_ses-01_task-view_stim-face01_acq-cam_image.png", True),
        ("sub-01/beh/sub-01_stim-partner_task-dyad_audio.wav", False),
        ("sub-01/beh/sub-01_task-dyad_audio.wav", False),
        ("sub-01/beh/sub-01_stim-partner_audio.wav", False),
        ("sub-01/anat/sub-01_task-view_stim-face01_image.png", False),
    ],
)
def test_stimulus_filenames(raw_regexes, path, valid):
    """Stimulus file names are accepted only in the documented layout."""
    assert _matches(raw_regexes, path) is valid
