#!/usr/bin/env python
"""Check that embedded JSON examples in Markdown files are valid.

This validates JSON code blocks (```JSON or ```json) in Markdown files
to catch issues like trailing commas that are invalid in JSON.
"""

import argparse
import json
import os
import re
import sys

SCRIPT_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.dirname(SCRIPT_DIR)


def parse_args():
    """Construct command line interface."""
    parser = argparse.ArgumentParser(
        description="Check for valid JSON in Markdown files."
    )

    parser.add_argument(
        "files",
        nargs="*",
        help="Markdown files to check. If none provided, checks all .md files in src/",
    )

    return parser.parse_args()


def extract_json_blocks(text):
    """Extract JSON code blocks from Markdown text.

    Arguments:
        text {string} -- The Markdown text to search

    Returns:
        {list} -- List of tuples (line_number, json_content)
    """
    # Pattern matches ```JSON or ```json followed by content until ```
    pattern = r"```[Jj][Ss][Oo][Nn]\n(.*?)```"
    blocks = []

    for match in re.finditer(pattern, text, re.DOTALL):
        # Calculate line number where the JSON block starts
        line_num = text[: match.start()].count("\n") + 1
        blocks.append((line_num, match.group(1)))

    return blocks


def validate_json_blocks(filename, blocks):
    """Validate JSON blocks and return errors.

    Arguments:
        filename {string} -- The file being checked
        blocks {list} -- List of (line_number, json_content) tuples

    Returns:
        {list} -- List of error dictionaries
    """
    errors = []

    for line_num, content in blocks:
        try:
            json.loads(content)
        except json.JSONDecodeError as e:
            errors.append(
                {
                    "file": filename,
                    "line": line_num,
                    "error": str(e),
                    "preview": content[:100].replace("\n", " ") + "...",
                }
            )

    return errors


def check_file(filepath):
    """Check a single file for JSON validity.

    Arguments:
        filepath {string} -- Path to the file to check

    Returns:
        {list} -- List of error dictionaries
    """
    try:
        with open(filepath, encoding="utf8") as f:
            text = f.read()
    except (FileNotFoundError, IOError):
        return []

    blocks = extract_json_blocks(text)
    if not blocks:
        return []

    return validate_json_blocks(filepath, blocks)


def get_all_markdown_files(directory=None):
    """Get all Markdown files to check.

    Keyword Arguments:
        directory {string} -- Directory to search (default: src/)

    Returns:
        {list} -- List of file paths
    """
    if directory is None:
        directory = os.path.join(REPO_ROOT, "src")

    files = []

    for rootdir, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(".md"):
                files.append(os.path.join(rootdir, filename))

    return files


def construct_error_message(errors):
    """Construct an error message from validation errors.

    Arguments:
        errors {list} -- List of error dictionaries

    Returns:
        {string} -- Formatted error message
    """
    lines = ["Invalid JSON found in the following files:\n"]

    for error in errors:
        lines.append(f"{error['file']}:{error['line']}: {error['error']}")
        lines.append(f"  Preview: {error['preview']}\n")

    return "\n".join(lines)


def main():
    """Main function."""
    args = parse_args()

    if args.files:
        files = [f for f in args.files if f.endswith(".md")]
    else:
        files = get_all_markdown_files()

    all_errors = []
    for filepath in files:
        errors = check_file(filepath)
        all_errors.extend(errors)

    print(f"Checked {len(files)} files. {len(all_errors)} JSON errors found.")

    if all_errors:
        error_message = construct_error_message(all_errors)
        print(error_message, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
