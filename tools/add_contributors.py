import pandas as pd

from rich import print

from utils import (
    add_to_tributors,
    add_to_allcontrib,
    get_gh_avatar,
    load_citation,
    load_allcontrib,
    load_tributors,
    root_dir,
    return_author_list_for_cff,
    return_missing_from_tributors,
    write_citation,
    write_allcontrib,
    write_tributors,
    transfer_contribution,
)


def main():

    tsv = pd.read_csv("new_contributors.tsv", sep="\t", encoding="utf8")
    print(tsv.head())

    tributors_file = root_dir().joinpath(".tributors")
    allcontrib_file = root_dir().joinpath(".all-contributorsrc")
    citation_file = root_dir().joinpath("CITATION.cff")

    print("\n[red]NOT IN .tributors FILE[/red]")
    new_contrib_names = tsv.name.to_list()
    missing_from_tributors = return_missing_from_tributors(
        tributors_file, new_contrib_names
    )
    print(missing_from_tributors)
    print("\n")

    for name in missing_from_tributors:
        add_to_tributors(tributors_file, name)
        add_to_allcontrib(allcontrib_file, name)

    tributors = load_tributors(tributors_file)

    for gh_usernames in tributors:
        if tributors[gh_usernames].get("contributions") is None:
            tributors[gh_usernames]["contributions"] = ["doc"]

    allcontrib = load_allcontrib(allcontrib_file)
    allcontrib = transfer_contribution(tributors, allcontrib)

    write_allcontrib(allcontrib_file, allcontrib)

    write_tributors(tributors_file, tributors)

    citation = load_citation(citation_file)
    citation["authors"] = return_author_list_for_cff(tributors_file)
    write_citation(citation_file, citation)


if __name__ == "__main__":
    main()
