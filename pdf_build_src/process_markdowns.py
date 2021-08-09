"""Process the markdown files.

The purpose of the script is to create a duplicate src directory within which
all of the markdown files are processed to match the specifications of building
a pdf from multiple markdown files using the pandoc library (***add link to
pandoc library documentation***) with pdf specific text rendering in mind as
well.
"""

import os
import re
import subprocess
import sys
from datetime import datetime

import numpy as np

sys.path.append("../tools/")
from schemacode import macros


def run_shell_cmd(command):
    """Run shell/bash commands passed as a string using subprocess module."""
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE)
    output = process.stdout.read()

    return output.decode('utf-8')


def copy_src():
    """Duplicate src directory to a new but temp directory named 'src_copy'."""
    # source and target directories
    src_path = "../src/"
    target_path = "src_copy"

    # make new directory
    mkdir_cmd = "mkdir "+target_path
    run_shell_cmd(mkdir_cmd)

    # copy contents of src directory
    copy_cmd = "cp -R "+src_path+" "+target_path
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
        if 'images' in dirs:
            subdir_list.append(root)

    for each in subdir_list:
        if each != root_path:
            run_shell_cmd("cp -R "+each+"/images"+" "+root_path+"/images/")


def extract_header_string():
    """Extract the latest release's version number and date from CHANGES.md."""
    run_shell_cmd("cp ../mkdocs.yml src_copy/")

    with open(os.path.join(os.path.dirname(__file__), 'src_copy/mkdocs.yml'), 'r') as file:
        data = file.readlines()

    header_string = data[0].split(": ")[1]

    title = " ".join(header_string.split()[0:4])
    version_number = header_string.split()[-1]
    build_date = datetime.today().strftime('%Y-%m-%d')

    return title, version_number, build_date


def add_header():
    """Add the header string extracted from changelog to header.tex file."""
    title, version_number, build_date = extract_header_string()
    header = " ".join([title, version_number, build_date])

    # creating a header string with latest version number and date
    header_string = (r"\fancyhead[L]{ " + header + " }")

    with open('header.tex', 'r') as file:
        data = file.readlines()

    # insert the header, note that you have to add a newline
    data[4] = header_string+'\n'

    # re-write header.tex file with new header string
    with open('header.tex', 'w') as file:
        file.writelines(data)


def remove_internal_links(root_path, link_type):
    """Find and replace all cross and same markdown internal links.

    The links will be replaced with plain text associated with it.
    """
    if link_type == 'cross':
        # regex that matches cross markdown links within a file
        # TODO: add more documentation explaining regex
        primary_pattern = re.compile(r'\[((?!http).[\w\s.\(\)`*/–]+)\]\(((?!http).+(\.md|\.yml|\.md#[\w\-\w]+))\)')  # noqa: E501
    elif link_type == 'same':
        # regex that matches references sections within the same markdown
        primary_pattern = re.compile(r'\[([\w\s.\(\)`*/–]+)\]\(([#\w\-._\w]+)\)')

    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            if file.endswith(".md"):
                with open(os.path.join(root, file), 'r') as markdown:
                    data = markdown.readlines()

                for ind, line in enumerate(data):
                    match = primary_pattern.search(line)

                    if match:
                        line = re.sub(primary_pattern,
                                      match.group().split('](')[0][1:], line)

                    data[ind] = line

                with open(os.path.join(root, file), 'w') as markdown:
                    markdown.writelines(data)


def modify_changelog():
    """Change first line of the changelog to markdown Heading 1.

    This modification makes sure that in the pdf build, changelog is a new
    chapter.
    """
    with open('src_copy/src/CHANGES.md', 'r') as file:
        data = file.readlines()

    data[0] = "# Changelog"

    with open('src_copy/src/CHANGES.md', 'w') as file:
        file.writelines(data)


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
        Offset that is used to adjust the correction of number of dashes in the first (offset[0]) and
        second (offset[1]) columns by the number specified in percentage. Defaults to [0.0, 0.0].
    debug : bool
        If True, print debugging information. Defaults to False.

    Returns
    -------
    new_table : list of list of str
        List of corrected lines of the input table with corrected number of dashes and aligned fences.
        To be later joined with pipe characters (``|``).
    """
    # nb_of_rows = len(table)
    nb_of_cols = len(table[0]) - 2

    nb_of_chars = []
    for i, row in enumerate(table):
        # Ignore number of dashes in the count of characters
        if i != 1:
            nb_of_chars.append([len(elem) for elem in row])

    # sanity check: nb_of_chars is list of list, all nested lists must be of equal length
    if not len(set([len(i) for i in nb_of_chars])) == 1:
        print('ERROR for current table ... "nb_of_chars" is misaligned, see:\n')
        print(nb_of_chars)
        print('\nSkipping formatting of this table.\n')
        return table

    # Convert the list to a numpy array and computes the maximum number of chars for each column
    nb_of_chars_arr = np.array(nb_of_chars)
    max_chars_in_cols = nb_of_chars_arr.max(axis=0)
    max_chars = max_chars_in_cols.max()

    # Computes an equal number of dashes per column based on the maximal number of characters over the columns
    nb_of_dashes = max_chars
    prop_of_dashes = 1.0 / nb_of_cols

    # Adjust number of characters in first and second column based  offset parameter
    first_column_width = int(offset[0] * nb_of_dashes) + nb_of_dashes
    second_column_width = int(offset[1] * nb_of_dashes) + nb_of_dashes

    if debug:
        print('    - Number of chars in table cells: {}'.format(max_chars_in_cols))
        print('    - Number of dashes (per column): {}'.format(nb_of_dashes))
        print('    - Proportion of dashes (per column): {}'.format(prop_of_dashes))
        print('    - Final number of chars in first column: {}'.format(first_column_width))
        print('    - Final number of chars in second column: {}'.format(second_column_width))

    # Format the lines with correct number of dashes or whitespaces and
    # correct alignment of fences and populate the new table (A List of str)
    new_table = []
    for i, row in enumerate(table):

        if i == 1:
            str_format = ' {:-{align}{width}} '
        else:
            str_format = ' {:{align}{width}} '

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
                if '-:' in elem and ':-' in elem:
                    str_format = ' {:-{align}{width}}: '
                    row_content.append(str_format.format(':-', align='<', width=(column_width)))
                elif '-:' not in elem and ':-' in elem:
                    str_format = ' {:-{align}{width}} '
                    row_content.append(str_format.format(':-', align='<', width=(column_width)))
                elif '-:' in elem and ':-'not in elem:
                    str_format = ' {:-{align}{width}}: '
                    row_content.append(str_format.format('-', align='<', width=(column_width)))
                elif i == 1 and '-:' not in elem and ':-' not in elem:
                    str_format = ' {:-{align}{width}} '
                    row_content.append(str_format.format('-', align='<', width=(column_width)))
                else:
                    row_content.append(str_format.format(elem, align='<', width=(column_width)))

        new_table.append(row_content)

    return new_table


def _contains_table_start(line, debug=False):
    """Check if line is start of a md table."""
    is_table = False

    nb_of_pipes = line.count('|')
    nb_of_escaped_pipes = line.count(r'\|')
    nb_of_pipes = nb_of_pipes - nb_of_escaped_pipes
    nb_of_dashes = line.count('-')

    if debug:
        print('Number of dashes / pipes : {} / {}'.format(nb_of_dashes, nb_of_pipes))

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
    exclude_files = ['index.md', '01-contributors.md']
    for root, dirs, files in sorted(os.walk(root_path)):
        for file in files:
            if file.endswith(".md") and file not in exclude_files:
                print('Check tables in {}'.format(os.path.join(root, file)))

                # Load lines of the markdown file
                with open(os.path.join(root, file), 'r') as f:
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
                        start_line = line_nb-1

                        print('  * Detected table starting line {}'.format(start_line))
                        # Extract for each row (header and the one containing dashes)
                        # the content of each column and strip to remove extra whitespace
                        header_row = [c.strip() for c in re.split(r'(?<!\\)\|', content[line_nb-1])]
                        row = [c.strip() for c in re.split(r'(?<!\\)\|', line)]

                        # Add the two lines to the table row list
                        table.append(header_row)
                        table.append(row)

                    elif table_mode:
                        # Extract from the line string the content of each column
                        # and strip them to remove extra whitespace
                        row = [c.strip() for c in re.split(r'(?<!\\)\|', line)]

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
                        # append each corrected row (line) to the content of the new markdown content
                        if is_end_of_table:
                            print('    - End of table detected after line {}'.format(end_line))

                            # Set table_mode to False such that the script will look
                            # for a new table start at the next markdown line
                            table_mode = False

                            # Correct the given table
                            table = correct_table(table, debug=debug)
                            print('    - Table corrected')
                            if debug:
                                print(table)

                            # Update the corresponding lines in
                            # the markdown with the corrected table
                            count = 0
                            for i, new_line in enumerate(content):
                                if i == start_line:
                                    new_content.pop()
                                if i >= start_line and i < end_line:
                                    new_content.append('|'.join(table[count])+' \n')
                                    count += 1
                                elif i == end_line:
                                    new_content.append('|'.join(table[count])+' \n\n')
                                    count += 1
                            print('    - Appended corrected table lines to the new markdown content')
                    else:
                        new_content.append(line)

                    line_nb += 1

                # Overwrite with the new markdown content
                with open(os.path.join(root, file), 'w') as f:
                    f.writelines(new_content)


def edit_titlepage():
    """Add title and version number of the specification to the titlepage."""
    title, version_number, build_date = extract_header_string()

    with open('cover.tex', 'r') as file:
        data = file.readlines()

    data[-1] = ("\\textsc{\large "+version_number+"}" +
                "\\\\[0.5cm]" +
                "{\large " +
                build_date +
                "}" +
                "\\\\[2cm]" +
                "\\vfill" +
                "\\end{titlepage}")

    with open('cover.tex', 'w') as file:
        data = file.writelines(data)


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
    for root, dirs, files in os.walk(duplicated_src_dir_path):
        for name in files:
            # Only edit markdown files
            if not name.lower().endswith(".md"):
                continue

            filename = os.path.join(root, name)
            with open(filename, "r") as fo:
                contents = fo.read()

            # Replace code snippets in the text with their outputs
            matches = re.findall("({{.*?}})", contents)
            matches = re.findall(re.compile("({{.*?}})", re.DOTALL), contents)
            for m in matches:
                # Remove macro delimiters to get *just* the function call
                function_string = m.strip("{} ")
                # Replace prefix with module name
                function_string = function_string.replace(
                    "MACROS___",
                    "macros."
                )
                # switch "use_pipe" flag OFF to render examples
                if "make_filetree_example" in function_string:
                    function_string = function_string.replace(
                    ")",
                    ", False)"
                    )
                # Run the function to get the output
                new = eval(function_string)
                # Replace the code snippet with the function output
                contents = contents.replace(m, new)

            with open(filename, "w") as fo:
                fo.write(contents)


if __name__ == '__main__':

    duplicated_src_dir_path = 'src_copy/src'

    # Step 1: make a copy of the src directory in the current directory
    copy_src()

    # Step 2: run mkdocs macros embedded in markdown files
    process_macros(duplicated_src_dir_path)

    # Step 3: copy BIDS_logo to images directory of the src_copy directory
    copy_bids_logo()

    # Step 4: copy images from subdirectories of src_copy directory
    copy_images(duplicated_src_dir_path)
    subprocess.call("mv src_copy/src/images/images/* src_copy/src/images/",
                    shell=True)

    # Step 5: extract the latest version number, date and title
    extract_header_string()
    add_header()

    edit_titlepage()

    # Step 6: modify changelog to be a level 1 heading to facilitate section
    # separation
    modify_changelog()

    # Step 7: remove all internal links
    remove_internal_links(duplicated_src_dir_path, 'cross')
    remove_internal_links(duplicated_src_dir_path, 'same')

    # Step 8: correct number of dashes and fences alignment for rendering tables in PDF
    correct_tables(duplicated_src_dir_path)
