"""Tests for the bidsschematools package."""

import os

import pytest

from bidsschematools.render import text
from bidsschematools.types import Namespace


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

    assert "**Definition**: A person or animal participating in the study." in schema_text
    # Each allowed value gets its own code span
    assert "**Allowed values**: `on`, `off`" in schema_text


def test_make_entity_definitions_snapshot():
    """Check the exact markdown rendered for a minimal schema."""
    schema = Namespace.build(
        {
            "objects": {
                "entities": {
                    "foo": {"name": "foo", "display_name": "Foo", "description": "A foo."},
                    "bar": {
                        "name": "bar",
                        "display_name": "Bar",
                        "format": "index",
                        "enum": ["a", {"name": "b"}],
                        "description": "See [x](SPEC_ROOT/x.md).",
                    },
                }
            },
            "rules": {"entities": ["foo", "bar"]},
        }
    )
    assert text.make_entity_definitions(schema) == (
        "\n## foo\n\n"
        "**Full name**: Foo\n\n"
        "**Format**: `foo-<label>`\n\n"
        "**Definition**: A foo."
        "\n## bar\n\n"
        "**Full name**: Bar\n\n"
        "**Format**: `bar-<index>`\n\n"
        "**Allowed values**: `a`, `b`\n\n"
        "**Definition**: See [x](./x.md)."
    )


def test_make_glossary(schema_obj, schema_dir):
    """
    Test whether files under the schema objects subdirectory correspond to entries, and
    that rules are not misloaded as objects.
    This may need to be updated for schema hierarchy changes.
    """
    # Test consistency
    object_files = []
    for root, _, files in os.walk(schema_dir, topdown=False):
        if "objects" in root:
            for object_file in files:
                object_base, _ = os.path.splitext(object_file)
                object_files.append(object_base)
    rule_files = []
    for root, _, files in os.walk(schema_dir, topdown=False):
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

    # Each object is rendered exactly once
    headers = [line for line in glossary.split("\n") if line.startswith("## ")]
    assert len(headers) == len(set(headers))

    # Multi-sense objects get an extra anchor without the sense suffix
    assert '<a name="objects.columns.acq_time"></a>' in glossary
    assert '<a name="objects.columns.acq_time__scans"></a>' in glossary


def test_make_glossary_snapshot():
    """Check the exact markdown rendered for a minimal schema."""
    schema = Namespace.build(
        {
            "objects": {
                "suffixes": {
                    "bold": {
                        "value": "bold",
                        "display_name": "BOLD",
                        "description": (
                            "Line one\\\ncontinued.\n\n"
                            "Example:\n\n```Text\na\nb\n```\n\n"
                            "Types:\n\n    1.  `x`\n\n    2.  `y`\n"
                        ),
                    },
                },
                "columns": {
                    "kind": {
                        "name": "kind",
                        "display_name": "Kind",
                        "description": "A kind.",
                        "definition": {"Levels": {"x": "X", "y": "Y"}},
                        "type": "string",
                    },
                },
            }
        }
    )
    assert text.make_glossary(schema) == (
        '\n<a name="objects.suffixes.bold"></a>\n'
        "## bold (suffixes)\n\n"
        "**Name**: BOLD\n\n"
        "**Type**: Suffix\n\n"
        "**Format**: `<entities>_bold.<extension>`\n\n"
        "**Description**:\nLine onecontinued.\n\n"
        # code fences survive
        "Example:\n\n```Text\na\nb\n```\n\n"
        # lists indented to nest in the common principles are not code blocks here
        "Types:\n\n1.  `x`\n\n2.  `y`\n\n"
        '\n<a name="objects.columns.kind"></a>\n'
        "## kind (columns)\n\n"
        "**Name**: Kind\n\n"
        "**Type**: Column\n\n"
        "**Allowed values**: `x`, `y`\n\n"
        "**Description**:\nA kind.\n\n"
        "**Schema information**:\n```yaml\ntype: string\n\n```"
    )


@pytest.mark.parametrize(
    ("desc", "expected"),
    [
        # orphan indented list is dedented
        ("Intro:\n\n    1. a\n\n    2. b\n\nOutro.", "Intro:\n\n1. a\n\n2. b\n\nOutro."),
        # nested list keeps its indentation
        ("- a\n    - b\n\n    continued", "- a\n    - b\n\n    continued"),
        # code fences are left alone
        ("```\n    code\n```", "```\n    code\n```"),
    ],
)
def test_dedent_orphan_blocks(desc, expected):
    assert text._dedent_orphan_blocks(desc) == expected


def test_define_common_principles_snapshot():
    """Check the exact markdown rendered for a minimal schema."""
    schema = {
        "objects": {
            "common_principles": {
                "a": {"display_name": "A", "description": "First."},
                "b": {"display_name": "B", "description": "Second."},
            }
        },
        "rules": {"common_principles": ["b", "a"]},
    }
    assert text.define_common_principles(schema) == "1. **B** - Second.\n\n2. **A** - First."


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
