import pandas as pd
from cffconvert.cli.create_citation import create_citation
from cffconvert.cli.validate_or_write_output import validate_or_write_output
from rich import print
from utils import (
    add_to_allcontrib,
    add_to_tributors,
    load_allcontrib,
    load_citation,
    load_tributors,
    return_author_list_for_cff,
    return_missing_from_tributors,
    root_dir,
    transfer_contribution,
    write_allcontrib,
    write_citation,
    write_tributors,
)

UPDATE_AVATARS = False


def main():
    tributors_file = root_dir().joinpath(".tributors")
    allcontrib_file = root_dir().joinpath(".all-contributorsrc")
    citation_file = root_dir().joinpath("CITATION.cff")

    tsv = pd.read_csv("contributors.tsv", sep="\t", encoding="utf8")

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
    tributors_keys = list(tributors.keys())
    tributors_names = [tributors[x]["name"].rstrip() for x in tributors]
    # print(tributors_keys)
    # print(tributors_names)

    allcontrib = load_allcontrib(allcontrib_file)
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    # print(allcontrib["contributors"])
    # print(allcontrib_names)

    for name in tsv.name:
        if name in tributors_names:
            index_tributor = tributors_names.index(name)
            key_tributor = tributors_keys[index_tributor]

            index_allcontrib = allcontrib_names.index(name)

            assert allcontrib["contributors"][index_allcontrib]["name"] == name
            assert tributors[key_tributor]["name"] == name

            this_contributor = "foo"

            # update some contributor info with data from .tributor
            if (
                this_contributor["website"] is None
                and "blog" in tributors[key_tributor]
                and tributors[key_tributor]["blog"] is not None
            ):
                this_contributor["website"] = tributors[key_tributor]["blog"]

            if (
                this_contributor["github_username"] is None
                and allcontrib["contributors"][index_allcontrib]["login"] is not None
            ):
                this_contributor["github_username"] = allcontrib["contributors"][
                    index_allcontrib
                ]["login"]

            if this_contributor["website"] is not None:
                allcontrib["contributors"][index_allcontrib][
                    "profile"
                ] = this_contributor["website"]
                tributors[key_tributor]["blog"] = this_contributor["website"]

            if this_contributor["github_username"] is not None:
                allcontrib["contributors"][index_allcontrib][
                    "login"
                ] = this_contributor["github_username"]

            """
            update .tributor
            """
            tributors[key_tributor]["publish_email"] = this_contributor["publish_email"]
            if (
                tributors[key_tributor]["publish_email"] is True
                and this_contributor["email"] is not None
            ):
                tributors[key_tributor]["email"] = this_contributor["email"]

            if this_contributor["affiliation"] is not None:
                tributors[key_tributor]["affiliation"] = this_contributor["affiliation"]

            if this_contributor["orcid"] is not None:
                tributors[key_tributor]["orcid"] = this_contributor["orcid"].replace(
                    "https://orcid.org/", ""
                )

    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    tributors_names = [tributors[x]["name"] for x in tributors]

    # sanity checks
    print(set(tributors_names) - set(allcontrib_names))
    print(set(allcontrib_names) - set(tributors_names))

    assert len(tributors_names) == len(set(tributors_names))
    assert len(allcontrib_names) == len(set(allcontrib_names))
    assert len(tributors_names) == len(allcontrib_names)

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
