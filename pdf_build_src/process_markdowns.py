"""Process the markdown files.
The purpose of the script is to create a duplicate src directory within which
all of the markdown files are processed to match the specifications of building
a pdf from multiple markdown files using the pandoc library (***add link to
pandoc library documentation***) with pdf specific text rendering in mind as
well.
"""

import os
import subprocess
import re
from datetime import datetime


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
    for root, dirs, files in os.walk(root_path):
        if 'images' in dirs:
            subdir_list.append(root)

    for each in subdir_list:
        if each != root_path:
            run_shell_cmd("cp -R "+each+"/images"+" "+root_path+"/images/")


def extract_header_string():
    """Extract the latest release's version number and date from CHANGES.md."""
    released_versions = []
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
    header_string = ("\chead{ " + header + " }")

    with open('header.tex', 'r') as file:
        data = file.readlines()

    # now change the last but 2nd line, note that you have to add a newline
    data[-2] = header_string+'\n'

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

    for root, dirs, files in os.walk(root_path):
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


"""Number of chars maximal in one line approximated from a line of the PDF"""
NB_CHARS_LINE_PDF = 100

def correct_table(table):
    """Compute the max number of characters and dashes for each column and create the corrected table

    Parameters
    ----------
    table : List of List of str
        Table content extracted from the markdown file.

    Returns
    -------
    new_table : List of List of str
        List of corrected lines of the input table with corrected number of dashes and aligned fences.
        To be later join with |'s
    """
    import numpy as np
    
    nb_of_rows = len(table)
    nb_of_cols = len(table[0])

    nb_of_chars = []
    for i, row in enumerate(table):
         # Ignore number of dashes in the count of characters
        if i != 1:
            nb_of_chars.append([len(elem) for elem in row])

    # Convert the list to a numpy array and computes the maximum number of chars for each column
    nb_of_chars_arr = np.array(nb_of_chars)
    max_chars_in_cols = nb_of_chars_arr.max(axis=0)

    # Computes number of dashes based on the maximal number of characters in each column
    nb_of_dashes = max_chars_in_cols
    prop_of_dashes = nb_of_dashes / nb_of_dashes.sum()
    nb_of_chars_in_pdf = prop_of_dashes * int(NB_CHARS_LINE_PDF)

    # print('    - Number of chars in table cells: {}'.format(max_chars_in_cols))
    # print('    - Number of dashes (per column): {}'.format(nb_of_dashes))
    # print('    - Proportion of dashes (per column): {}'.format(prop_of_dashes))
    # print('    - Number of chars max in column (PDF): {}'.format(nb_of_chars_in_pdf))

    # Offset that can be used to ajust the correction of number of dashes in the first and 
    # second columns by the number specified
    offset = [15, 0]
    
    # Computes the corrected number of dashes. An offset can be used to extend 
    for i, (value, prop) in enumerate(zip(max_chars_in_cols,prop_of_dashes)):
        # Correction for first column
        if i == 1:
            if int(value) < int(NB_CHARS_LINE_PDF) and prop < 0.5:
                first_column_width = int(nb_of_dashes.sum() * (value / int(NB_CHARS_LINE_PDF)) + offset[0])
            else:
                first_column_width = int(value)
            # print('    - Final number of chars in first column: {}'.format(first_column_width))
        # Correction for second column
        elif i == 2:
            if int(value) < int(NB_CHARS_LINE_PDF) and prop < 0.5:
                second_column_width = int(nb_of_dashes.sum() * (value / int(NB_CHARS_LINE_PDF)) + offset[1])
            else:
                second_column_width = int(value)
            # print('    - Final number of chars in second column: {}'.format(second_column_width))

    # Format the lines with correct number of dashes or whitespaces and correct alignment of fences and
    # populate the new table (A List of str)
    new_table = []
    for i, row in enumerate(table):
        row_content = []
        for j, elem in enumerate(row):
            if j == 0 or j == len(row) - 1:
                row_content.append(elem)
            else:
                if i == 1:
                    if j == 1:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(first_column_width)))
                    elif j == 2:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(second_column_width)))
                    else:
                        row_content.append('{:-{align}{width}}'.format(elem, align='<', width=(max_chars_in_cols[j])))
                else:
                    if j == 1:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(first_column_width)))
                    elif j == 2:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(second_column_width)))
                    else:
                        row_content.append('{:{align}{width}}'.format(elem, align='<', width=(max_chars_in_cols[j])))
        new_table.append(row_content)
        #print(row_content)
    return new_table


def correct_tables(root_path):
    """Make sure that:
    * proportion and number of dashes (---) are sufficiently enough for PDF generation, and 
    * fences (|) are corrected aligned
    """
    markdown_list = []
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if file.endswith(".md") and file != 'index.md' and file != '01-contributors.md' and file != '04-entity-table.md':
                print('Check tables in {}'.format(os.path.join(root, file)))
                markdown_list.append(os.path.join(root, file))
                with open(os.path.join(root, file),'r') as f:
                    content = f.readlines()
                tables = []
                table_mode = False
                start_line = 0
                new_content = []
                for line_nb, line in enumerate(content):
                    if line:
                        # Use dashes to detect where a table start and extract the header and the dashes lines
                        if '--' in line and not table_mode:
                            table_mode = True
                            start_line = line_nb-1
                            print('  * Detected table starting line {}'.format(start_line))
                            table = []
                            header_row = [c.strip() for c in content[line_nb-1].split('|')]
                            row = [c.strip() for c in line.split('|')]
                            table.append(header_row)
                            table.append(row)
                        elif table_mode:
                            row = [c.strip() for c in line.split('|')]
                            # Add row to table if this is not the end of the table
                            if row != ['']:
                                table.append(row)
                            else:
                                end_line = line_nb-1
                                table_mode = False
                                
                                # Correct the given table
                                table = correct_table(table)

                                # Update the corresponding lines in the markdown with the corrected table
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
                        else:
                            new_content.append(line)

                    line_nb += 1

                # Overwrite with the new markdown content
                with open(os.path.join(root, file),'w') as f:
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


if __name__ == '__main__':

    duplicated_src_dir_path = 'src_copy/src'

    # Step 1: make a copy of the src directory in the current directory
    copy_src()

    # Step 2: copy BIDS_logo to images directory of the src_copy directory
    copy_bids_logo()

    # Step 3: copy images from subdirectories of src_copy directory
    copy_images(duplicated_src_dir_path)
    subprocess.call("mv src_copy/src/images/images/* src_copy/src/images/", 
                    shell=True)

    # Step 4: extract the latest version number, date and title
    extract_header_string()
    add_header()

    edit_titlepage()

    # Step 5: modify changelog to be a level 1 heading to facilitate section 
    # separation
    modify_changelog()

    # Step 6: remove all internal links
    remove_internal_links(duplicated_src_dir_path, 'cross')
    remove_internal_links(duplicated_src_dir_path, 'same')

    # Step 7: correct number of dashes and fences alignment for rendering tables in PDF
    correct_tables(duplicated_src_dir_path) 