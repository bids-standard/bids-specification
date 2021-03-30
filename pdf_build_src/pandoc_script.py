"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
import pathlib
import subprocess


def build_pdf(filename):
    """Construct command with required pandoc flags and run using subprocess.

    Parameters
    ----------
    filename : str
        Name of the output file.

    """
    # Get all input files
    markdown_list = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith(".md") and file != 'index.md':
                markdown_list.append(os.path.join(root, file))
            elif file == 'index.md':
                index_page = os.path.join(root, file)

    # Prepare the command options
    cmd = [
        'pandoc',
        '--from=markdown_github',
        '--include-before-body=./cover.tex',
        '--toc',
        '--listings',
        '--include-in-header=./header.tex',
        '--include-in-header=./header_setup.tex',
        '-V documentclass=report',
        '-V linkcolor:blue',
        '--pdf-engine=xelatex',
        '--output={}'.format(filename),
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
    cmd += [str(root / i) for i in sorted(markdown_list)]

    # print and run
    print('running: \n\n' + '\n'.join(cmd))
    subprocess.run(cmd)


if __name__ == "__main__":
    build_pdf('bids-spec.pdf')
