"""Process the markdown files.

The purpose of the script is to create a duplicate src directory within which
all of the markdown files are processed to match the specifications of building
a pdf from multiple markdown files using the pandoc library (***add link to
pandoc library documentation***) with pdf specific text rendering in mind as
well.
"""

import json
import os
import posixpath
import re
import subprocess
import sys
from pathlib import Path
from datetime import datetime

import numpy as np
import pandas as pd

from remove_admonitions import remove_admonitions

sys.path.append("../tools/")
# functions from module macros are called by eval() later on
from mkdocs_macros_bids import macros  # noqa: F401


def run_shell_cmd(command):
    """Run shell/bash commands passed as a string using subprocess module."""
    process = subprocess.Popen(
        command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    output = process.stdout.read()

    return output.decode("utf-8")


def copy_src():
    """Duplicate src directory to a new but temp directory named 'src_copy'."""
    # source and target directories
    src_path = "../src/"
    target_path = "src_copy"

    # make new directory
    mkdir_cmd = "mkdir " + target_path
    run_shell_cmd(mkdir_cmd)

    # copy contents of src directory
    copy_cmd = "cp -R " + src_path + " " + target_path
    run_shell_cmd(copy_cmd)


def copy_bids_logo():
    """Copy BIDS_logo.jpg from the BIDS_logo dir in the root of the repo."""
    run_shell_cmd("cp ../BIDS_logo/BIDS_logo.jpg src_copy/src/images/")


def copy_images(root_path):
    """Copy images.

    Will be done from images directory of subdirectories to images directory
    in the src directory
    """
    subdir_list = []

    # walk through the src directory to find subdirectories named 'images'
    # and copy contents to the 'images' directory in the duplicate src
    # directory
    for root, dirs, files in sorted(os.walk(root_path)):
        if "images" in dirs:
            subdir_list.append(root)

    for each in subdir_list:
        if each != root_path:
            run_shell_cmd("cp -R " + each + "/images" + " " + root_path + "/images/")


def extract_header_string():
    """Extract the latest release's version number and date from CHANGES.md."""
    run_shell_cmd("cp ../mkdocs.yml src_copy/")

    with open(
        os.path.join(os.path.dirname(__file__), "src_copy/mkdocs.yml"), "r"
    ) as file:
        data = file.readlines()

    header_string = data[0].split(": ")[1]

    title = " ".join(header_string.split()[0:4])
    version_number = header_string.split()[-1]
    build_date = datetime.today().strftime("%Y-%m-%d")

    return title, version_number, build_date


def add_header():
    """Add the header string extracted from changelog to header.tex file."""
    title, version_number, build_date = extract_header_string()
    header = " ".join([title, version_number, build_date])

    # creating a header string with latest version number and date
    header_string = r"\fancyhead[L]{ " + header + " }"

    with open("header.tex", "r") as file:
        data = file.readlines()

    # insert the header, note that you have to add a newline
    data[4] = header_string + "\n"

    # re-write header.tex file with new header string
    with open("header.tex", "w") as file:
        file.writelines(data)


def remove_internal_links_reference(root_path):
    """Find and replace internal "reference-style" links.

    Works on all ".md" files in `root_path`.
    The links will be replaced with plain text associated with it.
    See https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links

    - `[reference-style links][some-ref]`, if "some-ref" points to a local ref
    - `[some-ref][]`, if "some-ref" points to a local ref

    For "reference-style links" we also need to remove the reference itself,
    which we assume to be put at the bottom of the markdown document,
    below a comment: `<!-- Link Definitions -->`.
    These references look like this:

    - `[some-ref]: #some-heading`
    - `[some-ref]: ./some_section.md#some-heading`

    "reference style links" of the form `[this is my link]`, where at the
    bottom of the document a declaration
    `[this is my link]: ./some_section#some-heading` is present,
    MUST be written with a trailing pair of empty brackets:
    `[this is my link][]`.
    """
    # match anything starting on a new line with "[" until you find "]"
    # (this is important to not also match pictures, which
    # start with "![")
    # then, we expect a ": "
    # then, if a "(" is present,
    # check that the following does not continue with "http"
    # (assuming that all links that start with http are external,
    # and all remaining links are internal)
    # if it doesn't, match anything until you find ")" and the end of
    # the line
    # if all of this works out, we found something
    pattern_ref = re.compile(r"^\[([^\]]+)\]:\s((?!http).+)$")

    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            links_to_remove = []
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as markdown:
                    data = markdown.readlines()

                # first find, which links need to be remove by scanning the
                # references, and remove the reference
                for ind, line in enumerate(data):

                    match = pattern_ref.search(line)

                    if match:
                        links_to_remove.append(match.groups()[0])
                        data[ind] = "\n"

                # Now remove the links for the references we found (& removed)
                for link in links_to_remove:
                    # match as in pattern_ref above, except that:
                    # line start and end don't matter(^ and $)
                    # no ": " in between bracket parts
                    # second bracket part uses square brackets
                    # part within second bracket part MUST match a particular
                    # link
                    pattern = re.compile(r"\[([^\]]+)\]\[" + f"{link}" + r"\]")
                    for ind, line in enumerate(data):

                        match = pattern.search(line)

                        if match:
                            line = re.sub(pattern, match.groups()[0], line)

                        data[ind] = line

                # Now write the changed data back to file
                with open(os.path.join(root, file), "w") as markdown:
                    markdown.writelines(data)


def remove_internal_links_inline(root_path):
    """Find and replace internal "inline-style" links.

    Works on all ".md" files in `root_path`.
    The links will be replaced with plain text associated with it.
    See https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#links

    We need to remove the following types of links:

    - `[inline-style links](#some-heading)`
    - `[inline-style links](./some_section.md#some-heading)`
    """
    # match anything starting with " [" or "[" until you find "]"
    # (this is important to not also match pictures, which
    # start with "![")
    # then, if a "(" is present,
    # check that the following does not continue with "http"
    # (assuming that all links that start with http are external,
    # and all remaining links are internal)
    # if it doesn't, match anything until you find ")"
    # if all of this works out, we found something
    pattern_inline = re.compile(r"(\s|^)+\[([^\]]+)\]\((?!http)([^\)]+)\)")

    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as markdown:
                    data = markdown.readlines()

                for ind, line in enumerate(data):
                    match = pattern_inline.search(line)

                    if match:
                        line = re.sub(pattern_inline, f" {match.groups()[1]}", line)

                    data[ind] = line

                with open(os.path.join(root, file), "w") as markdown:
                    markdown.writelines(data)


def assert_no_multiline_links(root_path):
    """Check that markdown links are defined on single lines.

    Works on all ".md" files in `root_path`.
    This "style" is important for link removal/replacement to work
    properly.

    Links like this are not accepted: `some stuff [start of link
    continues](http://ends-here.com)`

    See Also
    --------
    remove_internal_links_reference
    remove_internal_links_inline
    """
    pattern = re.compile(r"(\s|^)+\[([^\]]+)$")

    problems = dict()
    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), "r") as markdown:
                    data = markdown.readlines()

                code_context = False
                macro_context = False
                for ind, line in enumerate(data):

                    # do not check "code blocks" or "macros"
                    if line.strip().startswith("```"):
                        code_context = not code_context

                    if (not macro_context) and line.strip().startswith("{{"):
                        macro_context = True

                    if macro_context and line.strip().endswith("}}"):
                        macro_context = False

                    if code_context or macro_context:
                        continue

                    match = pattern.search(line)

                    if match:
                        problems[file] = problems.get(file, []) + [(ind, line)]

    if len(problems) > 0:
        msg = (
            "Found multiline markdown links! Please reformat as single"
            " line links.\n\n"
        )
        msg += json.dumps(problems, indent=4)
        raise AssertionError(msg)


def modify_changelog():
    """Change first line of the changelog to markdown Heading 1.

    This modification makes sure that in the pdf build, changelog is a new
    chapter.
    """
    with open("src_copy/src/CHANGES.md", "r") as file:
        data = file.readlines()

    data[0] = "# Changelog"

    with open("src_copy/src/CHANGES.md", "w") as file:
        file.writelines(data)


def read_table_from_tsv(input_file: Path, output_file : Path | None = None):
    """Inject table in markdown document from a tsv file.

    :param input_file: path to input markdown file

    :param output_file: path to output markdown file
                        defaults to writing to the input file if None is passed.
    """

    if output_file is None:
        output_file = input_file

    with open(input_file, "r", encoding="utf8") as f:
        content = f.readlines()

    with open(output_file, "w", encoding="utf8") as f:

        for line in content:

            if not line.startswith("{{ read_table('"):
                f.write(line)
                continue

            table = line.split("(")[1].split(",")[0].replace("'", '').replace('"', '')
            table_to_read = input_file.parent / table
            assert table_to_read.exists(), f"This file does not exist\n:{table_to_read}"

            df = pd.read_csv(table_to_read, sep="\t")
            df_as_md = df.to_markdown(index=False)
            f.write(df_as_md)
            f.write("\n")

            continue


def correct_table(table, offset=[0.0, 0.0], debug=False):
    """Create the corrected table.

    Compute the number of characters maximal in each table column and reformat each
    row in the table to make sure the first and second rows of the table have enough
    dashes (in proportion) and that fences are correctly aligned
    for correct rendering in the generated PDF.

    Parameters
    ----------
    table : list of list of str
        Table content extracted from the markdown file.
    offset : list of int
        Offset that is used to adjust the correction of number of dashes
        in the first (offset[0]) and
        second (offset[1]) columns by the number specified in percentage.
        Defaults to [0.0, 0.0].
    debug : bool
        If True, print debugging information. Defaults to False.

    Returns
    -------
    new_table : list of list of str
        List of corrected lines of the input table
        with corrected number of dashes and aligned fences.
        To be later joined with pipe characters (``|``).
    corrected : bool
        Whether or not the table was corrected.
    """
    corrected = True

    # nb_of_rows = len(table)
    nb_of_cols = len(table[0]) - 2

    nb_of_chars = []
    for i, row in enumerate(table):
        # Ignore number of dashes in the count of characters
        if i != 1:
            nb_of_chars.append([len(elem) for elem in row])

    # sanity check: nb_of_chars is list of list, all nested lists must be of equal length
    if not len(set([len(i) for i in nb_of_chars])) == 1:
        print('    - ERROR for current table ... "nb_of_chars" is misaligned, see:\n')
        print(nb_of_chars)
        print("\n    - Skipping formatting of this table.")
        corrected = False
        return table, corrected

    # Convert the list to a numpy array and computes the maximum number of chars for each column
    nb_of_chars_arr = np.array(nb_of_chars)
    max_chars_in_cols = nb_of_chars_arr.max(axis=0)
    max_chars = max_chars_in_cols.max()

    # Computes an equal number of dashes per column based
    # on the maximal number of characters over the columns
    nb_of_dashes = max_chars
    prop_of_dashes = 1.0 / nb_of_cols

    # Adjust number of characters in first and second column based  offset parameter
    first_column_width = int(offset[0] * nb_of_dashes) + nb_of_dashes
    second_column_width = int(offset[1] * nb_of_dashes) + nb_of_dashes

    if debug:
        print("    - Number of chars in table cells: {}".format(max_chars_in_cols))
        print("    - Number of dashes (per column): {}".format(nb_of_dashes))
        print("    - Proportion of dashes (per column): {}".format(prop_of_dashes))
        print(
            "    - Final number of chars in first column: {}".format(first_column_width)
        )
        print(
            "    - Final number of chars in second column: {}".format(
                second_column_width
            )
        )

    # Format the lines with correct number of dashes or whitespaces and
    # correct alignment of fences and populate the new table (A List of str)
    new_table = []
    for i, row in enumerate(table):

        if i == 1:
            str_format = " {:-{align}{width}} "
        else:
            str_format = " {:{align}{width}} "

        row_content = []
        for j, elem in enumerate(row):
            # Set the column width
            column_width = nb_of_dashes
            if j == 1:
                column_width = first_column_width
            elif j == 2:
                column_width = second_column_width

            if j == 0 or j == len(row) - 1:
                row_content.append(elem)
            else:
                # Handles alignment descriptors in pipe tables
                if "-:" in elem and ":-" in elem:
                    str_format = " {:-{align}{width}}: "
                    row_content.append(
                        str_format.format(":-", align="<", width=(column_width))
                    )
                elif "-:" not in elem and ":-" in elem:
                    str_format = " {:-{align}{width}} "
                    row_content.append(
                        str_format.format(":-", align="<", width=(column_width))
                    )
                elif "-:" in elem and ":-" not in elem:
                    str_format = " {:-{align}{width}}: "
                    row_content.append(
                        str_format.format("-", align="<", width=(column_width))
                    )
                elif i == 1 and "-:" not in elem and ":-" not in elem:
                    str_format = " {:-{align}{width}} "
                    row_content.append(
                        str_format.format("-", align="<", width=(column_width))
                    )
                else:
                    row_content.append(
                        str_format.format(elem, align="<", width=(column_width))
                    )

        new_table.append(row_content)

    return new_table, corrected


def _contains_table_start(line, debug=False):
    """Check if line is start of a md table."""
    is_table = False

    nb_of_pipes = line.count("|")
    nb_of_escaped_pipes = line.count(r"\|")
    nb_of_pipes = nb_of_pipes - nb_of_escaped_pipes
    nb_of_dashes = line.count("--")

    if debug:
        print("Number of dashes / pipes : {} / {}".format(nb_of_dashes, nb_of_pipes))

    if nb_of_pipes > 2 and nb_of_dashes > 2:
        is_table = True

    return is_table


def correct_tables(root_path, debug=False):
    """Change tables in markdown files for correct rendering in PDF.

    This modification makes sure that the proportion and number of dashes (-) are
    sufficient enough for correct PDF rendering and fences (|) are correctly aligned.


    Parameters
    ----------
    root_path : str
        Path to the root directory containing the markdown files
    debug : bool
        If True, print debugging information. Defaults to False.

    Notes
    -----
    This function MUST respect escaped pipes (i.e., pipes preceded by a backslash),
    and not interpret them as table delimiters. Here this is implemented with a regex
    split and a negative lookbehind assertion [1]_.

    References
    ----------
    .. [1] https://stackoverflow.com/a/21107911/5201771
    """
    exclude_files = ["index.md", "01-contributors.md"]
    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            if file.endswith(".md") and file not in exclude_files:
                print("Check tables in {}".format(os.path.join(root, file)))

                # Load lines of the markdown file
                with open(os.path.join(root, file), "r") as f:
                    content = f.readlines()

                table_mode = False
                start_line = 0
                new_content = []
                for line_nb, line in enumerate(content):
                    # Use dashes to detect where a table start and
                    # extract the header and the dashes lines
                    if not table_mode and _contains_table_start(line, debug):
                        # Initialize a list to store table rows
                        table = []

                        # Set table_mode to True such that the next lines
                        # will be append to the table list
                        table_mode = True

                        # Keep track of the line number where the table starts
                        start_line = line_nb - 1

                        print("  * Detected table starting line {}".format(start_line))
                        # Extract for each row (header and the one containing dashes)
                        # the content of each column and strip to remove extra whitespace
                        header_row = [
                            c.strip()
                            for c in re.split(r"(?<!\\)\|", content[line_nb - 1])
                        ]
                        row = [c.strip() for c in re.split(r"(?<!\\)\|", line)]

                        # Add the two lines to the table row list
                        table.append(header_row)
                        table.append(row)

                    elif table_mode:
                        # Extract from the line string the content of each column
                        # and strip them to remove extra whitespace
                        row = [c.strip() for c in re.split(r"(?<!\\)\|", line)]

                        # Detect if this is the end of the table and add the row if not empty.
                        # The end of the table is reached when:
                        #  * the row is empty (len(row) <= 1)
                        #  * or the successive row is empty (len(content[line_nb]) > 1)
                        is_end_of_table = False
                        if len(row) > 1:
                            table.append(row)
                            if line_nb < len(content) - 1:
                                if not len(content[line_nb]) > 1:
                                    is_end_of_table = True
                                    end_line = line_nb
                            elif line_nb == len(content) - 1:
                                is_end_of_table = True
                                end_line = line_nb
                        else:
                            is_end_of_table = True
                            end_line = line_nb - 1

                        # If the end of the table is reached, correct the table and
                        # append each corrected row (line)
                        # to the content of the new markdown content
                        if is_end_of_table:
                            print(
                                "    - End of table detected after line {}".format(
                                    end_line
                                )
                            )

                            # Set table_mode to False such that the script will look
                            # for a new table start at the next markdown line
                            table_mode = False

                            # Correct the given table
                            table, corrected = correct_table(table, debug=debug)
                            if corrected:
                                print("    - Table corrected")
                            if debug:
                                print(table)

                            # Update the corresponding lines in
                            # the markdown with the corrected table
                            count = 0
                            for i, new_line in enumerate(content):
                                if i == start_line:
                                    new_content.pop()
                                if i >= start_line and i < end_line:
                                    new_content.append("|".join(table[count]) + " \n")
                                    count += 1
                                elif i == end_line:
                                    new_content.append("|".join(table[count]) + " \n\n")
                                    count += 1
                            if corrected:
                                print(
                                    "    - Appended corrected table lines to new markdown content"
                                )
                    else:
                        new_content.append(line)

                    line_nb += 1

                # Overwrite with the new markdown content
                with open(os.path.join(root, file), "w") as f:
                    f.writelines(new_content)


def edit_titlepage():
    """Add title and version number of the specification to the titlepage."""
    title, version_number, build_date = extract_header_string()

    with open("cover.tex", "r") as file:
        data = file.readlines()

    data[-1] = (
        rf"\textsc{{\large {version_number}}}"
        r"\\[0.5cm]"
        rf"{{\large {build_date}}}"
        r"\\[2cm]"
        r"\vfill"
        r"\end{titlepage}"
    )

    with open("cover.tex", "w") as file:
        file.writelines(data)


class MockPage:
    pass


class MockFile:
    pass


def process_macros(duplicated_src_dir_path):
    """Search for mkdocs macros in the specification, run the embedded
    functions, and replace the macros with their outputs.

    Parameters
    ----------
    duplicated_src_dir_path : str
        Location of the files from the specification.

    Notes
    -----
    Macros are embedded snippets of Python code that are run as part of the
    mkdocs build, when generating the website version of the specification.

    Warning
    -------
    This function searches specifically for the mkdocs macros plugin's
    delimiters ("{{" and "}}"). Therefore, those characters should not be used
    in the specification for any purposes other than running macros.
    """
    re_code_snippets = re.compile("({{.*?}})", re.DOTALL)

    for root, dirs, files in os.walk(duplicated_src_dir_path):
        for name in files:
            # Only edit markdown files
            if not name.lower().endswith(".md"):
                continue

            filename = os.path.join(root, name)

            read_table_from_tsv(Path(filename))

            with open(filename, "r") as fo:
                contents = fo.read()

            # Create a mock MkDocs Page object that has a "file" attribute,
            # which is a mock MkDocs File object with a str "src_path" attribute
            # The src_path
            mock_file = MockFile()
            mock_file.src_path = posixpath.sep.join(filename.split(os.sep)[1:])

            page = MockPage()
            page.file = mock_file

            _Context__self = {"page": page}  # noqa: F841

            # Replace code snippets in the text with their outputs
            matches = re.findall(re_code_snippets, contents)
            for m in matches:
                # Remove macro delimiters to get *just* the function call
                function_string = m.strip("{} ")
                # Replace prefix with module name
                function_string = function_string.replace("MACROS___", "macros.")
                # switch "use_pipe" flag OFF to render examples
                if "make_filetree_example" in function_string:
                    function_string = function_string.replace(
                        ")",
                        ", False)",
                    )

                # switch "pdf_format" ON to render filename templates
                if "make_filename_template" in function_string:
                    function_string = function_string.replace(")", ", pdf_format=True)")

                # Run the function to get the output
                new = eval(function_string)
                # Replace the code snippet with the function output
                contents = contents.replace(m, new)

            with open(filename, "w") as fo:
                fo.write(contents)


if __name__ == "__main__":

    duplicated_src_dir_path = "src_copy/src"

    # make a copy of the src directory in the current directory
    copy_src()

    # run mkdocs macros embedded in markdown files
    process_macros(duplicated_src_dir_path)

    # remove mkdocs admonition
    remove_admonitions(
        input_folder=duplicated_src_dir_path, output_folder=duplicated_src_dir_path
    )

    # copy BIDS_logo to images directory of the src_copy directory
    copy_bids_logo()

    # copy images from subdirectories of src_copy directory
    copy_images(duplicated_src_dir_path)
    subprocess.call("mv src_copy/src/images/images/* src_copy/src/images/", shell=True)

    # extract the latest version number, date and title
    extract_header_string()
    add_header()

    edit_titlepage()

    # modify changelog to be a level 1 heading to facilitate section
    # separation
    modify_changelog()

    # remove all internal links
    assert_no_multiline_links(duplicated_src_dir_path)
    remove_internal_links_inline(duplicated_src_dir_path)
    remove_internal_links_reference(duplicated_src_dir_path)

    # correct number of dashes and fences alignment for rendering tables in PDF
    correct_tables(duplicated_src_dir_path)
