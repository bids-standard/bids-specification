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
    copy_cmd = "cp -a "+src_path+" "+target_path
    run_shell_cmd(copy_cmd)


def copy_bids_logo():
    """Copy BIDS_logo.jpg from the BIDS_logo dir in the root of the repo."""
    run_shell_cmd("cp ../BIDS_logo/BIDS_logo.jpg src_copy/images/")


def copy_images(root_path):
    """Copy images.

    Will be done from images directory of subdirectories to images directory
    in the src directory
    """
    subdir_list = []

    # walk through the src directory to find subdirectories named 'images'
    # and copy contents to the 'images' directory in the duplicate src directory
    for root, dirs, files in os.walk(root_path):
        if 'images' in dirs:
            subdir_list.append(root)

    for each in subdir_list:
        if each != root_path:
            run_shell_cmd("cp -a "+each+"/images/"+" "+root_path+"/images/")


def extract_header_string():
    """Extract the latest release's version number and date from CHANGES.md."""
    released_versions = []

    for i, line in enumerate(open('src_copy/CHANGES.md')):

        match_list = re.findall(r'^##\s\[v.+\]', line)

        if len(match_list) > 0:
            wordlist = line.split()
            released_versions.append([match_list[0].split()[1], wordlist[2]])

    version_number = released_versions[0][0].strip('[]')
    version_date = released_versions[0][1].strip('()')

    return version_number, version_date


def add_header():
    """Add the header string extracted from changelog to header.tex file."""
    version_number, version_date = extract_header_string()

    # creating a header string with latest version number and date
    header_string = ("\chead{Brain Imaging Data Structure " +
                     version_number + " " + version_date + "}")

    with open('header.tex', 'r') as file:
        data = file.readlines()

    # now change the last but 2nd line, note that you have to add a newline
    data[-2] = header_string+'\n'

    # re-write header.tex file with new header string
    with open('header.tex', 'w') as file:
        file.writelines(data)


def remove_internal_links(root_path, link_type):
    """Find and replace all cross and same markdown internal links.

    The links will be replaced with plain text associated with the link.
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
    with open('src_copy/CHANGES.md', 'r') as file:
        data = file.readlines()

    data[0] = "# Changelog"

    with open('src_copy/CHANGES.md', 'w') as file:
        file.writelines(data)


def edit_titlepage():
    """Add title and version number of the specification to the titlepage."""
    version_number, version_date = extract_header_string()

    with open('cover.tex', 'r') as file:
        data = file.readlines()

    data[-1] = ("\\textsc{\large "+version_number+"}" +
                "\\\\[0.5cm]" +
                "{\large " +
                version_date +
                "}" +
                "\\\\[2cm]" +
                "\\vfill" +
                "\\end{titlepage}")

    with open('cover.tex', 'w') as file:
        data = file.writelines(data)


if __name__ == '__main__':

    duplicated_src_dir_path = 'src_copy'

    # Step 1: make a copy of the src directory in the current directory
    copy_src()

    # Step 2: copy BIDS_logo to images directory of the src_copy directory
    copy_bids_logo()

    # Step 3: copy images from subdirectories of src_copy directory
    copy_images(duplicated_src_dir_path)

    # Step 4: extract the latest version number and date
    extract_header_string()
    add_header()

    edit_titlepage()

    modify_changelog()

    # Step 5: remove all internal links
    remove_internal_links(duplicated_src_dir_path, 'cross')
    remove_internal_links(duplicated_src_dir_path, 'same')