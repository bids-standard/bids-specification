"""Use the pandoc library as a final step to build the pdf.

This is done once the duplicate src directory is processed.
"""
import os
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

    def _flatten_values(lst):
        """Flatten a list of dicts of lists to a list of values."""
        for val in (obj.values() for obj in lst):
            if isinstance(val, str):
                yield val
            else:
                yield from _flatten_values(val)

      # Find mkdocs.yml in some parent directory of this script
      fname_mkdocs_yml = next(
          path / "mkdocs.yml"
          for path in pathlib.Path(__file__).absolute().parents
          if Path.isfile(path / "mkdocs.yml")
      )
    with open(fname_mkdocs_yml, "r") as stream:
        mkdocs_yml = yaml.safe_load(stream)

    sections = mkdocs_yml["nav"][0]["The BIDS Specification"]

    # special files
    index_page = "./index.md"
    pandoc_metadata = pathlib.Path(__file__).with_name("metadata.yml")

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
    cmd += [str(root / md) for md in _flatten_values(sections)]

    # print and run
    print("pandoc command being run: \n\n" + "\n".join(cmd))
    subprocess.run(cmd)


if __name__ == "__main__":
    build_pdf()
