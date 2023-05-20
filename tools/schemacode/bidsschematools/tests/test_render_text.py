"""Tests for the bidsschematools package."""
import os

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
    that rules are not mis-loaded as objects.
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
            assert any(line.startswith(f'<a name="objects.{i}') for i in object_files)
            # Are rules loaded incorrectly?
            assert not any(line.startswith(f'<a name="objects.{i}') for i in rules_only)


def test_make_filename_template(schema_obj):
    """
    Test whether:
        * the base hierarchy structure of mandatory subject and optional session is
        returned. This should be robust with respect to schema format.
        * each directory contains at least one possible pattern.
        This should be robust with respect to schema format.
        * all files under the datatype rules subdirectory have corresponding entries.
        This may need to be updated for schema hierarchy changes.
    """
    filename_template = text.make_filename_template("raw", schema_obj, pdf_format=True)

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
    datatype_level = False
    datatype_file_start = "            sub-<label>"
    datatype_bases_found = 0
    for line in filename_template.split("\n"):
        if datatype_level:
            # Is there at least one file pattern per datatype?
            assert line.startswith(datatype_file_start)
            datatype_level = False
        if line in datatype_bases:
            datatype_level = True
            datatype_bases_found += 1
    # Are all datatypes listed?
    assert datatype_bases_found == datatype_count


def test_make_filename_template_mutually_exclusive_extensions():
    """Extensions that are mutually exclusive appear on a single line.

    In this case mrk and sqd for MEG data.
    """
    filename_template = text.make_filename_template(
        "raw",
        datatypes=["meg"],
        suffixes=["markers"],
        pdf_format=True,
        include_legend=False,
    )
    print(filename_template)
    assert "legend" not in filename_template
    nb_lines = len(filename_template.split("\n"))
    assert nb_lines == 7


def test_make_filename_template_mutually_combine_extensions_when_too_many():
    """Combine extensions on a single line, there are too many extensions."""
    filename_template = text.make_filename_template(
        "raw",
        datatypes=["meg"],
        suffixes=["meg"],
        pdf_format=True,
        include_legend=False,
    )
    print(filename_template)
    nb_lines = len(filename_template.split("\n"))
    assert nb_lines == 10


def test_define_common_principles(schema_obj):
    """Ensure that define_common_principles returns a string."""
    common_principles_str = text.define_common_principles(schema_obj)
    # Must be a string
    assert isinstance(common_principles_str, str)
    # Must be fairly long
    assert len(common_principles_str) > 100


def test_append_filename_template_legend():
    """Check contents of generated string."""
    test_str = text._append_filename_template_legend("", pdf_format=False)
    assert isinstance(test_str, str)
    assert "follow the links" in test_str

    test_str = text._append_filename_template_legend("", pdf_format=True)
    assert isinstance(test_str, str)
    assert "follow the links" not in test_str


def test_define_allowed_top_directories(schema_obj):
    """smoke test for allowed top directories."""
    test_str = text.define_allowed_top_directories(schema_obj)
    assert isinstance(test_str, str)


@pytest.mark.parametrize(
    "extensions, expected, pdf_format",
    [
        (
            ["json"],
            ['<a href="SPEC_ROOT/glossary.html#extension-common_principles">json</a>'],
            False,
        ),
        (["nii.gz", "nii", "json"], ["nii[.gz]", "json"], True),
    ],
)
def test_extension_for_this_group(schema_obj, extensions, expected, pdf_format):
    extensions = text._combine_extensions_with_headings(
        schema_obj, extensions, pdf_format=pdf_format
    )
    assert extensions == expected


class Group:
    def __init__(self, extensions):
        self.extensions = extensions


@pytest.mark.parametrize("extensions, expected", [(["nii"], 1), (["nii", ["bar", "baz"]], 3)])
def test_nb_extensions(extensions, expected):
    group = Group(extensions=extensions)
    assert text._nb_extensions(group) == expected


@pytest.mark.parametrize(
    "extensions, expected", [(["nii"], ["nii"]), (["nii", ["bar", "baz"]], ["nii", "bar", "baz"])]
)
def test_listify_all_extensions(extensions, expected):
    assert text._listify_all_extensions(extensions) == expected
