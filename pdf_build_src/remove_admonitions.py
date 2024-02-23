"""Script to remove all mkdocs admonition from the markdown files in a directory.

See the pdf_build_src/tests/data/input directory to see what admonitions look like.
"""

from __future__ import annotations

import shutil
from pathlib import Path

INDENT = "    "


def remove_admonitions(
    input_folder: str | Path, output_folder: str | Path, indent: str = None
):

    if indent is None:
        indent = INDENT

    md_files = Path(input_folder).glob("**/*.md")

    for file in md_files:

        with open(file, "r", encoding="utf8") as f:
            content = f.readlines()

        output_file = Path(output_folder) / file.relative_to(input_folder)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        print(f"processing: {file}\n to: {output_file}")

        with open(output_file, "w", encoding="utf8") as f:

            is_admonition = False
            counter = 0
            for line in content:

                if line.startswith("!!!"):
                    is_admonition = True
                    counter = 0
                    continue

                # skip first line after admonition
                if is_admonition and counter == 0:
                    counter += 1
                    continue

                if not line.startswith(indent):
                    is_admonition = False

                if is_admonition:
                    line = line.lstrip(indent)

                f.write(line)


if __name__ == "__main__":
    """If run as a script this will just run the main function on test data."""
    input_folder = Path(__file__).parent / "tests" / "data" / "input"
    output_folder = Path(__file__).parent / "tests" / "data" / "output"
    shutil.rmtree(output_folder)
    remove_admonitions(input_folder, output_folder)
