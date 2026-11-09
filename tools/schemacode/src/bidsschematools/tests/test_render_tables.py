"""Tests for the bidsschematools package."""

from bidsschematools.render import tables
from bidsschematools.render.utils import normalize_requirements


def test_make_entity_table(schema_obj):
    """
    Test whether expected entities are present and listed correctly.
    This should be robust with respect to schema format.
    """
    entity_table = tables.make_entity_table(schema_obj)

    # Non-exhaustive list covering both value and index formats
    expected_entities = [
        "[`acq-<label>`](./appendices/entities.md#acq)",
        "[`ses-<label>`](./appendices/entities.md#ses)",
        "[`sample-<label>`](./appendices/entities.md#sample)",
        "[`task-<label>`](./appendices/entities.md#task)",
        "[`acq-<label>`](./appendices/entities.md#acq)",
        "[`ce-<label>`](./appendices/entities.md#ce)",
        "[`trc-<label>`](./appendices/entities.md#trc)",
        "[`stain-<label>`](./appendices/entities.md#stain)",
        "[`rec-<label>`](./appendices/entities.md#rec)",
        "[`dir-<label>`](./appendices/entities.md#dir)",
        "[`run-<index>`](./appendices/entities.md#run)",
    ]

    for expected_entity in expected_entities:
        assert expected_entity in entity_table


def test_make_suffix_table(schema_obj):
    """
    Test whether expected suffixes are present and listed with correct names.
    Values are hard-coded from the present YAML, but should nevertheless be robust
    with respect to schema format, other than case changes for the names.
    """
    target_suffixes = [
        "beh",
        "cbv",
        "dwi",
    ]
    suffix_table = tables.make_suffix_table(schema_obj, target_suffixes)

    expected_names = [
        "Behavioral recording",
        "Cerebral blood volume image",
        "Diffusion-weighted image",
    ]

    for expected_name in expected_names:
        assert expected_name in suffix_table


def test_make_sidecar_table(schema_obj):
    """
    Test whether expected metadata fields are present and the requirement level is
    applied correctly.
    This should be robust with respect to schema format.
    """
    # mri.MRISpatialEncoding selected for having some level and description addenda
    rendered_table = tables.make_sidecar_table(schema_obj, "mri.MRISpatialEncoding").split("\n")

    assert rendered_table[0].startswith("| **Key name**")
    assert rendered_table[1].startswith("|-------------")

    fields = schema_obj.rules.sidecars.mri.MRISpatialEncoding.fields
    assert len(rendered_table) == len(fields) + 2

    for field, render_row in zip(fields, rendered_table[2:]):
        assert render_row.startswith(f"| [{field}](")
        spec = fields[field]
        if isinstance(spec, str):
            level = normalize_requirements(spec)
            level_addendum = ""
            description_addendum = ""
        else:
            level = normalize_requirements(spec["level"])
            level_addendum = normalize_requirements(spec.get("level_addendum", ""))
            description_addendum = spec.get("description_addendum", "")

        assert f"| {level}" in render_row
        assert level_addendum.split("\n")[0] in render_row
        assert description_addendum.split("\n")[0] in render_row


def test_make_metadata_table(schema_obj):
    """
    Test whether expected metadata fields are present and the requirement level is
    applied correctly.
    This should be robust with respect to schema format.
    """
    target_metadata = {
        "Authors": "required",
        "BIDSVersion": "required",
        "DatasetDOI": "optional",
    }
    metadata_table = tables.make_metadata_table(schema_obj, target_metadata).split("\n")

    metadata_tracking = list(target_metadata.keys())

    for line in metadata_table:
        for i in metadata_tracking:
            if i in line:
                # Is the requirement level displayed correctly?
                assert target_metadata[i].upper() in line
                # Mark found
                metadata_tracking.remove(i)

    # Have we found all fields?
    assert len(metadata_tracking) == 0


def test_make_columns_table(schema_obj):
    """
    Test whether expected columns are present and the requirement level is
    applied correctly.
    This should be robust with respect to schema format.
    """
    # mri.MRISpatialEncoding selected for having some level and description addenda
    rendered_table = tables.make_columns_table(
        schema_obj,
        "modality_agnostic.Participants",
    ).split("\n")

    assert rendered_table[0].startswith("| **Column name**")
    assert rendered_table[1].startswith("|----------------")

    fields = schema_obj.rules.tabular_data.modality_agnostic.Participants.columns
    assert len(rendered_table) == len(fields) + 3  # header + orientation + add. cols. row

    for field, render_row in zip(fields, rendered_table[2:-1]):
        assert render_row.startswith(f"| [{field}](")
        spec = fields[field]
        if isinstance(spec, str):
            level = spec
            level_addendum = ""
            description_addendum = ""
        else:
            level = spec["level"]
            level_addendum = spec.get("level_addendum", "").replace("required", "REQUIRED")
            description_addendum = spec.get("description_addendum", "")

        assert level.upper() in render_row
        assert level_addendum.split("\n")[0] in render_row
        assert description_addendum.split("\n")[0] in render_row
