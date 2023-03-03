"""Add new contributors listed in new_contributors.tsv to .tributors file

The tributor file is then used to update
- the CITATION.cff file
- the .all-contributorsrc file
- TODO: the table of contributors in the appendix of the spec

Contrary to the typical .tributors file,
the one here also centralizes the contributions
that would otherwise be listed in the .all-contributorsrc file.

This can also be used to update all files if new_contributors.tsv is empty.
"""

# TODO: handle the following cases
# - ORCID
# - affiliation
# - getting avatars

from pathlib import Path

import pandas as pd
from cffconvert.cli.create_citation import create_citation
from cffconvert.cli.validate_or_write_output import validate_or_write_output
from rich import print
from utils import (
    add_to_allcontrib,
    add_to_tributors,
    get_gh_avatar,
    load_allcontrib,
    load_citation,
    load_tributors,
    return_author_list_for_cff,
    return_missing_from_tributors,
    return_this_contributor,
    root_dir,
    transfer_contribution,
    write_allcontrib,
    write_citation,
    write_tributors,
)

UPDATE_AVATARS = False

GH_USERNAME = "Remi-Gau"

TOKEN_FILE = None

INPUT_FILE = Path(__file__).parent / "new_contributors.tsv"


def main():
    token = None
    if TOKEN_FILE is not None:
        with open(Path(TOKEN_FILE)) as f:
            token = f.read().strip()

    tsv = pd.read_csv(INPUT_FILE, sep="\t", encoding="utf8")
    print(tsv.head())

    tributors_file = root_dir() / ".tributors"
    allcontrib_file = root_dir() / ".all-contributorsrc"
    citation_file = root_dir() / "CITATION.cff"

    print("\n[red]NOT IN .tributors FILE[/red]")
    new_contrib_names = tsv.name.to_list()
    missing_from_tributors = return_missing_from_tributors(
        tributors_file, new_contrib_names
    )
    print(missing_from_tributors)
    print("\n")

    for name in missing_from_tributors:
        this_contributor = return_this_contributor(tsv, name)
        add_to_tributors(tributors_file, name)
        if UPDATE_AVATARS:
            avatar_url = get_gh_avatar(
                this_contributor["github_username"], GH_USERNAME, token
            )
            this_contributor["avatar_url"] = avatar_url
        add_to_allcontrib(allcontrib_file, name)

    tributors = load_tributors(tributors_file)

    for gh_usernames in tributors:
        if tributors[gh_usernames].get("contributions") is None:
            tributors[gh_usernames]["contributions"] = ["doc"]
        for key in tributors[gh_usernames]:
            if isinstance(tributors[gh_usernames][key], (str)):
                tributors[gh_usernames][key] = tributors[gh_usernames][key].strip()

    allcontrib = load_allcontrib(allcontrib_file)
    allcontrib = transfer_contribution(tributors, allcontrib)

    write_allcontrib(allcontrib_file, allcontrib)

    write_tributors(tributors_file, tributors)

    citation = load_citation(citation_file)
    citation["authors"] = return_author_list_for_cff(tributors_file)
    write_citation(citation_file, citation)

    citation = create_citation(infile=citation_file, url=None)
    validate_or_write_output(
        outfile=None, outputformat=None, validate_only=True, citation=citation
    )


if __name__ == "__main__":
    main()
