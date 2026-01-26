#!python
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pandas>=2.3.3",
# ]
# ///
#
# Script to parse new contributors from wiki text and add to new_contributors.tsv
#
# This aims for simplicity over robustness, so you may need to edit the text and try again.
# Or fix this script or add_contributors.py to make it more robust.
#
# Example input:
#
# ### 1
# - name: Alice
# - contributions: 📖
# - email (optional): alice@gmail.com
# - github (optional): alice
# - affiliation (optional):
# - orcid (optional): 0000-0001-2345-6789
# - bio (optional):
# - website (optional):
#
# ### 2
# ...

import sys
from pathlib import Path

import pandas as pd


def main() -> None:
    if sys.argv[1:]:
        out_file = sys.argv[1]
    else:
        out_file = (
            input("Output TSV file [new_contributors.tsv]: ").strip()
            or "new_contributors.tsv"
        )
    text = input("Paste new contributors from wiki:\n").strip()
    entries = text.split("### ")[1:]
    records = [
        {
            key[2:]: stripped
            for key, val in (
                line.split(": ", 1) for line in entry.splitlines() if ": " in line
            )
            if (stripped := val.strip())
        }
        for entry in entries
    ]
    df = pd.DataFrame.from_records(records)
    df.columns = [col.removesuffix(" (optional)") for col in df.columns]

    Path(out_file).write_text(df.to_csv(sep="\t", index=False, na_rep=""))


if __name__ == "__main__":
    main()
