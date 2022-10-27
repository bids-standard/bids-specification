"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import pathlib
import subprocess
import yaml


def build_pdf(filename="bids-spec.pdf", logfile="bids-spec_pandoc_log.json"):
    """Construct command with required pandoc flags and run using subprocess.

    Parameters
    ----------
    filename : str
        Name of the output file. Defaults to "bids-spec.pdf".
    logfile : str
        Name of the log file. Defaults to "bids-spec_pandoc_log.json".
    """
    # location of this file: This is also the working directory when
    # the pdf is being built using `cd build_pdf_src` and then
    # `bash build_pdf.sh`
    root = pathlib.Path(__file__).parent.absolute()

    # Parse content files from mkdocs.yml file
    def _unpack(sections):
        """Flatten a list of dicts of lists."""
        sections_flat = []
        for i in sections:
            if isinstance(list(i.values())[0], str):
                sections_flat.append(i)
            elif isinstance(list(i.values())[0], list):
                for j in list(i.values())[0]:
                    sections_flat.append(j)
        return sections_flat

    def _has_only_str2str(sections):
        """Check list of dict has only str to str mappings."""
        for i in sections:
            if not isinstance(list(i.values())[0], str):
                return False
        return True

    fname_mkdocs_yml = [
        i for i in list(root.parents) if str(i).endswith("bids-specification")
    ][0] / "mkdocs.yml"
    with open(fname_mkdocs_yml, "r") as stream:
        mkdocs_yml = yaml.safe_load(stream)

    sections = mkdocs_yml["nav"][0]["The BIDS Specification"]
    while not _has_only_str2str(sections):
        sections = _unpack(sections)

    markdown_list = [list(i.values())[0] for i in sections]

    # special files
    index_page = "./index.md"
    pandoc_metadata = (
        [i for i in list(root.parents) if str(i).endswith("bids-specification")][0]
        / "pdf_build_src"
        / "metadata.yml"
    )

    # Prepare the command options
    cmd = [
        "pandoc",
        "--from=markdown_github+yaml_metadata_block",
        "--include-before-body=./cover.tex",
        "--include-in-header=./header.tex",
        "--include-in-header=./header_setup.tex",
        "--pdf-engine=xelatex",
        f"--log={logfile}",
        f"--output={filename}",
    ]

    # Resources are searched relative to the working directory, but
    # we can add additional search paths using <path>:<another path>, ...
    # When in one of the appendices/ files there is a reference to
    # "../04-modality-specific-files/images/...", then we need to use
    # appendices/ as a resource-path so that the relative files can
    # be found.
    cmd += [f'--resource-path=.:{str(root / "appendices")}']

    # Add input files to command
    # The filenames in `markdown_list` will ensure correct order when sorted
    cmd += [str(root / index_page)]
    cmd += [str(pandoc_metadata)]
    cmd += [str(root / i) for i in markdown_list]

    # print and run
    print("pandoc command being run: \n\n" + "\n".join(cmd))
    subprocess.run(cmd)


if __name__ == "__main__":
    build_pdf()
