from math import nan

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
)

UPDATE_AVATARS = False


def transfer_contribution(tributors: dict, allcontrib: dict) -> dict:
    """transfer contribution list from tributors to allcontrib"""

    tributors_keys = list(tributors.keys())
    tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]

    for name in tributors_names:

        index_allcontrib = allcontrib_names.index(name)

        index_tributor = tributors_names.index(name)
        key_tributor = tributors_keys[index_tributor]

        contributions = tributors[key_tributor].get("contributions", ["doc"])
        allcontrib["contributors"][index_allcontrib]["contributions"] = contributions

    return allcontrib


def rename_columns(df):
    df.rename(
        columns={
            "Name  For example: Jane Smith": "name",
            "Primary affiliation  Please include:  Institution, Department, City, (State), Zip Code, Country": "affiliation",
            "ORCID number  For example:  https://orcid.org/0000-0002-1535-9777": "orcid",
            "Github username  For example:   https://github.com/Jane-Smith": "github",
            "I agree to have my email address on the github repository of the BIDS specification": "consent",
            "Email address": "email",
            "Added to .tributors file in repo": "added",
        },
        inplace=True,
    )
    return df


def return_this_contributor(tsv, name: str):

    name = name.strip()

    github = tsv[tsv.name == name].github.values[0]
    if github in ["nan"] or isinstance(github, (float)):
        github = None

    github_username = None
    if github is not None:
        github_username = github.replace("https://github.com/", "").rstrip(" ")

    website = tsv[tsv.name == name].Website.values[0]
    if website == "nan" or isinstance(website, (float)):
        website = github

    affiliation = tsv[tsv.name == name].affiliation.values[0]
    if affiliation == "nan" or isinstance(affiliation, (float)):
        affiliation = None

    orcid = tsv[tsv.name == name].orcid.values[0]
    if orcid == "nan" or isinstance(orcid, (float)):
        orcid = None
    if orcid is not None:
        orcid = orcid.replace("http://", "https://")

    add_email = tsv[tsv.name == name].consent.values[0]
    add_email = add_email not in ["nan", "No"] and not isinstance(add_email, (float))

    email = tsv[tsv.name == name].email.values[0]
    if email == "nan" or isinstance(email, (float)):
        email = None
    if not add_email:
        email = None

    return {
        "name": name,
        "github": github,
        "github_username": github_username,
        "website": website,
        "affiliation": affiliation,
        "orcid": orcid,
        "publish_email": add_email,
        "email": email,
    }


def main():

    TOKEN = "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"

    tributors_file = root_dir().joinpath(".tributors")
    allcontrib_file = root_dir().joinpath(".all-contributorsrc")
    citation_file = root_dir().joinpath("CITATION.cff")

    tsv = pd.read_csv("contributors.tsv", sep="\t", encoding="utf8")
    tsv = rename_columns(tsv)
    # print(tsv.head())

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

            this_contributor = return_this_contributor(tsv, name)

            index_tributor = tributors_names.index(name)
            key_tributor = tributors_keys[index_tributor]

            index_allcontrib = allcontrib_names.index(name)

            assert allcontrib["contributors"][index_allcontrib]["name"] == name
            assert tributors[key_tributor]["name"] == name

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

            # print(f"\n[cyan]{name.upper()}[/cyan]")
            # print(this_contributor)
            # print(tributors[key_tributor])
            # print(allcontrib["contributors"][index_allcontrib])

    for i, this_contributor in enumerate(allcontrib["contributors"]):

        if UPDATE_AVATARS and this_contributor.get("avatar_url") is None:
            avatar_url = get_gh_avatar(this_contributor["login"], "Remi-Gau", TOKEN)
            if avatar_url is not None:
                allcontrib["contributors"][i]["avatar_url"] = avatar_url

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


if __name__ == "__main__":
    main()
