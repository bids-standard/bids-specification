"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
import subprocess


def build_pdf(filename):
    """Construct command with required pandoc flags and run using subprocess.

    Parameters
    ----------
    filename : str
        Name of the output file.

    """
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".md") and file != 'index.md':
                markdown_list.append(os.path.join(root, file))
            elif file == 'index.md':
                index_page = os.path.join(root, file)

    default_pandoc_cmd = "pandoc "

    # creates string of file paths in the order we'd like them to be appear
    # ordering is taken care of by the inherent file naming
    files_string = index_page + " " + " ".join(sorted(markdown_list))

    flags = (" -f markdown_github --include-before-body cover.tex --toc "
             "-V documentclass=report --listings -H listings_setup.tex "
             "-H header.tex -V linkcolor:blue -V geometry:a4paper "
             "-V geometry:margin=2cm --pdf-engine=xelatex -o ")
    output_filename = filename

    cmd = default_pandoc_cmd + files_string + flags + output_filename
    subprocess.run(cmd.split())


if __name__ == "__main__":
    build_pdf('bids-spec.pdf')