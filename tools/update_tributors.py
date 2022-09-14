import json
from math import isnan, nan
from multiprocessing import allow_connection_pickling
import ruamel.yaml
import pandas as pd

from rich import print

from pathlib import Path

root_dir = Path(__file__).parent.parent

yaml = ruamel.yaml.YAML()

tributors_file = root_dir.joinpath(".tributors")
allcontrib_file = root_dir.joinpath(".all-contributorsrc")


def load_tributors(tributors_file):
    with open(tributors_file, "r", encoding="utf8") as tributors_file:
        return json.load(tributors_file)


def load_from_allcontrib(allcontrib_file):
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


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


def return_this_contributor(tsv, name):
    github = tsv[tsv.name == name].github.values[0]
    if github in ["nan"] or isinstance(github, (float)):
        github = None

    github_username = None
    if github is not None:
        github_username = github.replace("https://github.com/", "")

    website = tsv[tsv.name == name].Website.values[0]
    if website == "nan" or isinstance(website, (float)):
        website = github

    affiliation = tsv[tsv.name == name].affiliation.values[0]
    if affiliation == "nan" or isinstance(affiliation, (float)):
        affiliation = None

    orcid = tsv[tsv.name == name].orcid.values[0]
    if orcid == "nan" or isinstance(orcid, (float)):
        orcid = None

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
        "add_email": add_email,
        "email": email,
    }


tsv = pd.read_csv("contributors.tsv", sep="\t", encoding="utf8")
tsv = rename_columns(tsv)
# print(tsv.head())

tributors = load_tributors(tributors_file)
tributors_keys = list(tributors.keys())
tributors_names = [tributors[x]["name"] for x in tributors]
# print(tributors_keys)
# print(tributors_names)

allcontrib = load_from_allcontrib(allcontrib_file)
allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
# print(allcontrib["contributors"])
# print(allcontrib_names)

print("\n[red]NOT IN .tributors FILE[/red]")
in_tributors = tsv.name.isin(tributors_names).to_list()
# print(in_tributors)
for i, value in enumerate(in_tributors):
    if not value:
        print(tsv.name[i])
print("\n")

for name in tsv.name:

    if name in tributors_names:

        this_contributor = return_this_contributor(tsv, name)

        index_tributor = tributors_names.index(name)
        key_tributor = tributors_keys[index_tributor]

        index_allcontrib = allcontrib_names.index(name)

        assert allcontrib["contributors"][index_allcontrib]["name"] == name
        assert tributors[key_tributor]["name"] == name

        if this_contributor["github_username"] is not None:
            allcontrib["contributors"][index_allcontrib]["profile"] = this_contributor[
                "website"
            ]

        if this_contributor["website"] is not None:
            allcontrib["contributors"][index_allcontrib]["login"] = this_contributor[
                "github_username"
            ]
            tributors[key_tributor]["blog"] = this_contributor["website"]

        if this_contributor["add_email"]:
            tributors[key_tributor]["email"] = this_contributor["email"]

        if this_contributor["affiliation"] is not None:
            tributors[key_tributor]["affiliation"] = this_contributor["affiliation"]

        if this_contributor["orcid"] is not None:
            tributors[key_tributor]["orcid"] = this_contributor["orcid"].replace("https://orcid.org/", "")


        print("\n")
        print(this_contributor)
        print(tributors[key_tributor])
        print(allcontrib["contributors"][index_allcontrib])
