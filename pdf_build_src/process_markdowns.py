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