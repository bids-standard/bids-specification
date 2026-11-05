"""Tests for the bidsschematools package."""

import os
import re

import pytest

from bidsschematools.render import text


def test_make_entity_definitions(schema_obj):
    """
    Test whether expected format strings are present.
    This should be stable with respect to schema format.
    """
    schema_text = text.make_entity_definitions(schema_obj)
    expected_formats = [
        "**Format**: `sub-<label>`",
        "**Format**: `ses-<label>`",
        "**Format**: `sample-<label>`",
        "**Format**: `task-<label>`",
        "**Format**: `acq-<label>`",
        "**Format**: `ce-<label>`",
        "**Format**: `trc-<label>`",
        "**Format**: `stain-<label>`",
        "**Format**: `rec-<label>`",
        "**Format**: `dir-<label>`",
        "**Format**: `run-<index>`",
        "**Format**: `mod-<label>`",
        "**Format**: `echo-<index>`",
        "**Format**: `flip-<index>`",
        "**Format**: `inv-<index>`",
        "**Format**: `mt-<label>`",
    ]
    for expected_format in expected_formats:
        assert expected_format in schema_text


def test_make_glossary(schema_obj, schema_dir):
    """
    Test whether files under the schema objects subdirectory correspond to entries, and
    that rules are not misloaded as objects.
    This may need to be updated for schema hierarchy changes.
    """
    # Test consistency
    object_files = []
    for root, dirs, files in os.walk(schema_dir, topdown=False):
        if "objects" in root:
            for object_file in files:
                object_base, _ = os.path.splitext(object_file)
                object_files.append(object_base)
    rule_files = []
    for root, dirs, files in os.walk(schema_dir, topdown=False):
        if "rules" in root:
            for rule_file in files:
                rule_base, _ = os.path.splitext(rule_file)
                rule_files.append(rule_base)
    rules_only = list(filter(lambda a: a not in object_files, rule_files))

    glossary = text.make_glossary(schema_obj)
    for line in glossary.split("\n"):
        if line.startswith('<a name="objects.'):
            # Are all objects objects?
            assert any(line.startswith(f'<a name="objects.{i}.') for i in object_files)
            # Are rules loaded incorrectly?
            assert not any(line.startswith(f'<a name="objects.{i}.') for i in rules_only)


@pytest.mark.parametrize("placeholders", [True, False])
def test_make_filename_template(schema_obj, schema_dir, placeholders):
    """
    Test whether:

    * The base hierarchy structure of mandatory subject and optional session is
      returned. This should be robust with respect to schema format.
    * Each directory contains at least one possible pattern.
      This should be robust with respect to schema format.
    * All files under the datatype rules subdirectory have corresponding entries.
      This may need to be updated for schema hierarchy changes.
    """
    filename_template = text.make_filename_template(
        "raw", schema_obj, placeholders=placeholders, pdf_format=True
    )

    # Test predefined substrings
    expected_template_part = """
sub-<label>/
    [ses-<label>/]
        anat/
    """
    assert expected_template_part in filename_template

    # Test consistency
    datatypes = {
        datatype
        for rule in schema_obj.rules.files.raw.values(level=2)
        for datatype in rule.datatypes
    }
    # Datatypes in named directories at the dataset root (for example, stimuli)
    # are not rendered under sub-<label>/[ses-<label>/]
    layout = schema_obj.rules.directories.raw
    root_dirs = {layout[key].name for key in layout.root.subdirs if "name" in layout[key]}
    assert "stimuli" in datatypes & root_dirs
    assert "        stimuli/" not in filename_template.split("\n")
    datatypes -= root_dirs

    datatype_count = len(datatypes)
    datatype_bases = [f"        {i}/" for i in datatypes]
    datatype_file_start = (
        "            sub-<label>" if not placeholders else "            <matches>_"
    )
    datatype_bases_found = 0
    template_started = False
    for line in filename_template.split("\n"):
        if "```" in line:
            if template_started:
                break

            template_started = True
            continue

        if not template_started:
            continue

        if line.startswith("sub-<label>"):
            continue
        if line.startswith("    [ses-<label>/]"):
            continue

        if line in datatype_bases:
            datatype_bases_found += 1
        else:
            assert line.startswith(datatype_file_start)

    # Are all datatypes listed?
    assert datatype_bases_found == datatype_count

    # Restrict (a little) the datatype bases
    filename_template = text.make_filename_template(
        "raw",
        schema_obj,
        suffixes=["events"],
        placeholders=placeholders,
        empty_dirs=False,
        pdf_format=True,
    )

    datatype_bases_found = 0
    template_started = False
    for line in filename_template.split("\n"):
        if "```" in line:
            if template_started:
                break

            template_started = True
            continue

        if not template_started:
            continue

        if line.startswith("sub-<label>"):
            continue
        if line.startswith("    [ses-<label>/]"):
            continue

        if line in datatype_bases:
            datatype_bases_found += 1
        else:
            assert line.startswith(datatype_file_start)

    # In this case events is not defined for all datatypes
    assert datatype_bases_found < datatype_count


def _template_lines(schema_obj, pdf_format, **kwargs):
    """Render a raw filename template and return its lines without HTML markup."""
    template = text.make_filename_template("raw", schema_obj, pdf_format=pdf_format, **kwargs)
    if not pdf_format:
        # HTML output escapes placeholders and wraps names in links
        template = re.sub(r"<[^>]+>", "", template).replace("&lt;", "<").replace("&gt;", ">")
    return template.split("\n")


@pytest.mark.parametrize("pdf_format", [True, False])
def test_make_filename_template_root_datatype(schema_obj, pdf_format):
    """Root-level datatype directories render at the dataset root when requested."""
    lines = _template_lines(schema_obj, pdf_format, datatypes=["stimuli"])
    assert "stimuli/" in lines
    assert not any(line.startswith("sub-<label>") for line in lines)
    # Dataset-level tables come from the common rules and precede the stimulus files
    audio = "    stim-<label>[_part-<label>]_audio.json"
    assert lines.index("    stimuli.tsv") < lines.index(audio)
    assert "    annotations.tsv" in lines
    assert "    stim-<label>[_part-<label>]_annot-<label>_events.tsv" in lines
    # No other common stem rules (such as phenotype's "*") are picked up
    assert not any(line.startswith("    *") for line in lines)

    # Mixed with a subject-level datatype, both trees are shown, the root one last
    lines = _template_lines(schema_obj, pdf_format, datatypes=["stimuli", "eeg"])
    assert lines.index("sub-<label>/") < lines.index("        eeg/") < lines.index("stimuli/")

    # The catalog tables have no suffix, so a suffix filter leaves them out
    lines = _template_lines(schema_obj, pdf_format, datatypes=["stimuli"], suffixes=["audio"])
    assert "stimuli/" in lines
    assert "    stimuli.tsv" not in lines

    # Root-level directories are not shown unless requested
    lines = _template_lines(schema_obj, pdf_format, datatypes=["eeg"])
    assert "stimuli/" not in lines


def test_define_common_principles(schema_obj):
    """Ensure that define_common_principles returns a string."""
    common_principles_str = text.define_common_principles(schema_obj)
    # Must be a string
    assert isinstance(common_principles_str, str)
    # Must be fairly long
    assert len(common_principles_str) > 100


def test_append_filename_template_legend():
    """Check contents of generated string."""
    test_str = text.append_filename_template_legend("", pdf_format=False)
    assert isinstance(test_str, str)
    assert "follow the links" in test_str

    test_str = text.append_filename_template_legend("", pdf_format=True)
    assert isinstance(test_str, str)
    assert "follow the links" not in test_str


def test_define_allowed_top_directories(schema_obj):
    """smoke test for allowed top directories."""
    test_str = text.define_allowed_top_directories(schema_obj)
    assert isinstance(test_str, str)


def test_render_text(schema_obj):
    test_str = text.render_text(
        schema_obj, key="objects.files.dataset_description.description", src_path=None
    )
    assert (
        test_str == "The file `dataset_description.json` is a JSON file describing the dataset.\n"
    )


def test_render_text_errors(schema_obj):
    with pytest.raises(ValueError, match="does not refer to a text field"):
        text.render_text(schema_obj, key="dataset_description", src_path=None)
