#!/usr/bin/env python3
import argparse
import json
import sys


def parse_file_tree(input_data, tab_width=4):
    """
    Parse a file tree hierarchy from an input stream and convert it to a nested dictionary.

    :param input_data: Input string or file-like object representing the file tree
    :param tab_width: Number of spaces to replace tabs with
    :return: A nested dictionary representing the file tree
    """
    # If input is a string, convert to a list of lines
    if isinstance(input_data, str):
        lines = input_data.splitlines()
    else:
        lines = [line.rstrip() for line in input_data.readlines()]

    def _parse_tree(lines):
        # Create main tree dictionary
        tree = {}

        # Stack to keep track of nested dictionaries and their indentation levels
        dict_stack = [(tree, -1)]

        for i, line in enumerate(lines):
            # Skip empty lines
            if not line.strip():
                continue

            # Replace tabs with specified number of spaces
            line = line.replace("\t", " " * tab_width).rstrip()

            # Compute indentation and clean name
            indent_level = len(line) - len(line.lstrip())
            current_name = line.strip()

            # Find the correct parent dictionary based on indentation
            while dict_stack and dict_stack[-1][1] >= indent_level:
                dict_stack.pop()

            # If stack is empty, something went wrong with indentation
            if not dict_stack:
                raise ValueError(f"Invalid indentation for line: {line}")

            # Get the current parent dictionary
            parent_dict, _ = dict_stack[-1]

            # Determine if it's a directory
            # 1. Explicitly marked with '/'
            # 2. Has children on next lines with more indentation
            is_dir = current_name.endswith("/") or (
                i < len(lines) - 1
                and len(lines[i + 1]) - len(lines[i + 1].lstrip()) > indent_level
            )

            # Normalize directory name
            if is_dir and not current_name.endswith("/"):
                current_name += "/"

            # Add item to the dictionary
            if is_dir:
                # Create a new nested dictionary for directories
                new_dict = {}
                parent_dict[current_name] = new_dict
                # Push new dictionary and its indentation to the stack
                dict_stack.append((new_dict, indent_level))
            else:
                # Add files with empty string value
                parent_dict[current_name] = ""

        return tree

    # Call the internal parsing function and return its result
    return _parse_tree(lines)


def decorate_output(output_str, decoration_type):
    """
    Decorate the output based on the specified decoration type

    :param output_str: JSON string to be decorated
    :param decoration_type: Type of decoration to apply
    :return: Decorated output string
    """
    if decoration_type == "bids-filetree":
        return f"{{{{ MACROS___make_filetree_example(\n\n{output_str}\n\n) }}}}"
    return output_str


def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Parse file tree hierarchy into a nested dictionary."
    )
    parser.add_argument(
        "input_file",
        nargs="?",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="Input file to parse (default: stdin)",
    )
    parser.add_argument(
        "--tab-width",
        type=int,
        default=4,
        help="Number of spaces to replace tabs with (default: 4)",
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default=None,
        help="Output file to write the parsed dictionary (default: stdout)",
    )
    parser.add_argument(
        "--indent", type=int, default=2, help="Indentation for JSON output (default: 2)"
    )
    parser.add_argument(
        "-D",
        "--decorate",
        type=str,
        choices=["bids-filetree"],
        default=None,
        help="Decorate the output with a specific format",
    )

    # Parse arguments
    args = parser.parse_args()

    # Parse the file tree
    result = parse_file_tree(args.input_file, args.tab_width)

    # Prepare output using json.dumps with specified indent
    output_str = json.dumps(result, indent=args.indent)

    # Decorate output if specified
    if args.decorate:
        output_str = decorate_output(output_str, args.decorate)

    # Determine output destination
    if args.output_file:
        # Write to file
        with open(args.output_file, "w") as f:
            f.write(output_str)
    else:
        # Print to stdout
        print(output_str)


def test_example1():
    """
    Test parsing a file tree with nested directories
    """
    input_tree = """file1
a.dat
sub-1
  subsub
    file.dat
  filehere
anotherfile"""

    expected_output = {
        "file1": "",
        "a.dat": "",
        "sub-1/": {"subsub/": {"file.dat": ""}, "filehere": ""},
        "anotherfile": "",
    }

    # Parse the input tree
    result = parse_file_tree(input_tree)

    # Use deep comparison to check the result
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_decorations():
    """
    Test the output decoration functionality
    """
    dummy_json = '{"test": "value"}'

    # Test bids-filetree decoration
    decorated = decorate_output(dummy_json, "bids-filetree")
    assert (
        decorated == '{{ MACROS___make_filetree_example(\n\n{"test": "value"}\n\n) }}'
    )

    # Test no decoration
    undecorated = decorate_output(dummy_json, None)
    assert undecorated == dummy_json


def test_more_complex_tree():
    """
    Test a more complex nested directory structure
    """
    input_tree = """root
  subdir1
    file1.txt
    subsubdir
      file2.txt
  subdir2
    file3.txt"""

    expected_output = {
        "root/": {
            "subdir1/": {"file1.txt": "", "subsubdir/": {"file2.txt": ""}},
            "subdir2/": {"file3.txt": ""},
        }
    }

    # Parse the input tree
    result = parse_file_tree(input_tree)

    # Use deep comparison to check the result
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


def test_neuroimaging_dataset():
    """
    Test parsing a complex neuroimaging dataset file structure
    """
    input_tree = """dataset_description.json
tasks.tsv
tasks.json
participants.tsv
sub-A/
  ses-20220101/
    ephys/
        sub-A_ses-20220101_task-nosepoke_ephys.nix
        sub-A_ses-20220101_task-nosepoke_ephys.json
        sub-A_ses-20220101_task-nosepoke_events.tsv
        sub-A_ses-20220101_task-rest_ephys.nix
        sub-A_ses-20220101_task-rest_ephys.json
        sub-A_ses-20220101_channels.tsv
        sub-A_ses-20220101_electrodes.tsv
        sub-A_ses-20220101_probes.tsv
  ses-20220102/
    ephys/
        sub-A_ses-20220102_task-rest_ephys.nix
        sub-A_ses-20220102_task-rest_ephys.json
        sub-A_ses-20220102_channels.tsv
        sub-A_ses-20220102_electrodes.tsv
        sub-A_ses-20220102_probes.tsv"""

    expected_output = {
        "dataset_description.json": "",
        "tasks.tsv": "",
        "tasks.json": "",
        "participants.tsv": "",
        "sub-A/": {
            "ses-20220101/": {
                "ephys/": {
                    "sub-A_ses-20220101_task-nosepoke_ephys.nix": "",
                    "sub-A_ses-20220101_task-nosepoke_ephys.json": "",
                    "sub-A_ses-20220101_task-nosepoke_events.tsv": "",
                    "sub-A_ses-20220101_task-rest_ephys.nix": "",
                    "sub-A_ses-20220101_task-rest_ephys.json": "",
                    "sub-A_ses-20220101_channels.tsv": "",
                    "sub-A_ses-20220101_electrodes.tsv": "",
                    "sub-A_ses-20220101_probes.tsv": "",
                }
            },
            "ses-20220102/": {
                "ephys/": {
                    "sub-A_ses-20220102_task-rest_ephys.nix": "",
                    "sub-A_ses-20220102_task-rest_ephys.json": "",
                    "sub-A_ses-20220102_channels.tsv": "",
                    "sub-A_ses-20220102_electrodes.tsv": "",
                    "sub-A_ses-20220102_probes.tsv": "",
                }
            },
        },
    }

    # Parse the input tree
    result = parse_file_tree(input_tree)

    # Use deep comparison to check the result
    assert result == expected_output, f"Expected {expected_output}, but got {result}"


if __name__ == "__main__":
    # If run directly, execute main
    main()
