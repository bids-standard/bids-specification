"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
import pathlib
import subprocess


def build_pdf(filename="bids-spec.pdf", logfile="bids-spec_pandoc_log.json"):
    """Construct command with required pandoc flags and run using subprocess.

    Parameters
    ----------
    filename : str
        Name of the output file. Defaults to "bids-spec.pdf".
    logfile : str
        Name of the log file. Defaults to "bids-spec_pandoc_log.json".
    """
    # Files that are not supposed to be built into the PDF
    EXCLUDE = ["./index.md", "./schema/README.md", "./pregh-changes.md"]

    # Get all input files
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            fpath = os.path.join(root, file)
            if fpath.endswith(".md") and fpath not in EXCLUDE:
                markdown_list.append(fpath)
            elif fpath.endswith('index.md'):
                # Special role for index.md
                index_page = fpath

    # Prepare the command options
    cmd = [
        'pandoc',
        '--from=markdown_github+yaml_metadata_block',
        '--include-before-body=./cover.tex',
        '--include-in-header=./header.tex',
        '--include-in-header=./header_setup.tex',
        '--pdf-engine=xelatex',
        f'--log={logfile}',
        f'--output={filename}',
    ]

    # location of this file: This is also the working directory when
    # the pdf is being built using `cd build_pdf_src` and then
    # `bash build_pdf.sh`
    root = pathlib.Path(__file__).parent.absolute()

    # Resources are searched relative to the working directory, but
    # we can add additional search paths using <path>:<another path>, ...
    # When in one of the 99-appendices/ files there is a reference to
    # "../04-modality-specific-files/images/...", then we need to use
    # 99-appendices/ as a resource-path so that the relative files can
    # be found.
    cmd += [f'--resource-path=.:{str(root / "99-appendices")}']

    # Add input files to command
    # The filenames in `markdown_list` will ensure correct order when sorted
    cmd += [str(root / index_page)]
    cmd += [str(root / i) for i in ["../../metadata.yml"] + sorted(markdown_list)]

    # print and run
    print('running: \n\n' + '\n'.join(cmd))
    subprocess.run(cmd)


if __name__ == "__main__":
    build_pdf()
