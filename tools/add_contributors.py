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

import json
from collections import OrderedDict
from pathlib import Path

import pandas as pd
import requests
import ruamel.yaml
from cffconvert.cli.create_citation import create_citation
from cffconvert.cli.validate_or_write_output import validate_or_write_output
from rich import print

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

UPDATE_AVATARS = False

GH_USERNAME = "Remi-Gau"

TOKEN_FILE = None

INPUT_FILE = Path(__file__).parent / "new_contributors.tsv"


def updating_allcontrib(allcontrib: dict, this_contributor: dict[str, str]) -> dict:
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]

    if this_contributor["name"] not in allcontrib_names:
        print(f"adding {this_contributor['name']}")
        allcontrib["contributors"].append(this_contributor)
        return allcontrib

    else:
        index_allcontrib = allcontrib_names.index(this_contributor["name"])

        for key, value in this_contributor.items():
            if key not in allcontrib["contributors"][index_allcontrib]:
                update_allcontrib_key(
                    contributor=allcontrib["contributors"][index_allcontrib],
                    key=key,
                    value=value,
                )

            if allcontrib["contributors"][index_allcontrib][key] != value:
                update_allcontrib_key(
                    contributor=allcontrib["contributors"][index_allcontrib],
                    key=key,
                    value=value,
                )

    return allcontrib


def update_allcontrib_key(contributor: dict, key: str, value: str):
    print(f"updating {contributor['name']} - {key}")
    contributor[key] = value


def root_dir():
    return Path(__file__).parent.parent


def load_tributors(tributors_file: Path):
    """Load .tributors file."""
    with open(tributors_file, "r", encoding="utf8") as tributors_file:
        return json.load(tributors_file)


def write_tributors(tributors_file: Path, tributors):
    """Write .tributors file."""
    tributors = sort_tributors(tributors)
    with open(tributors_file, "w", encoding="utf8") as output_file:
        json.dump(tributors, output_file, indent=4, ensure_ascii=False)


def load_allcontrib(allcontrib_file: Path):
    """Load .all-contributorsrc file."""
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


def write_allcontrib(allcontrib_file: Path, allcontrib):
    """Write .all-contributorsrc file."""
    allcontrib = sort_all_contrib(allcontrib)
    with open(allcontrib_file, "w", encoding="utf8") as output_file:
        json.dump(allcontrib, output_file, indent=4, ensure_ascii=False)


def load_citation(citation_file: Path):
    """Load CITATION.CFF file."""
    with open(citation_file, "r", encoding="utf8") as input_file:
        return yaml.load(input_file)


def write_citation(citation_file: Path, citation):
    """Write CITATION.CFF file."""
    with open(citation_file, "w", encoding="utf8") as output_file:
        return yaml.dump(citation, output_file)


def emoji_map() -> dict[str, str]:
    # https://allcontributors.org/docs/en/emoji-key
    return {
        "code": ":laptop:",
        "doc": ":open_book:",
        "ideas": ":thinking_face:",
        "bug": ":bug:",
        "example": ":light_bulb:",
        "question": ":speech_balloon:",
        "review": ":eyes:",
        "plugin": ":electric_plug:",
        "fundingFinding": ":magnifying_glass_tilted_left:",
        "talk": ":loudspeaker:",
        "design": ":artist_palette:",
        "data": ":input_symbols:",
        "tool": ":wrench:",
        "projectManagement": ":tear-off_calendar:",
        "test": ":warning:",
        "eventOrganizing": ":clipboard:",
        "infra": ":metro:",
        "userTesting": ":notebook:",
        "video": ":video_camera:",
        "blog": ":memo:",
        "content": ":fountain_pen:",
        "tutorial": ":check_mark_button:",
        "maintenance": ":construction:",
        "financial": ":dollar_banknote:",
    }


def transfer_contribution(tributors: dict, allcontrib: dict) -> dict:
    """Transfer contribution list from tributors to allcontrib."""

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


def get_gh_avatar(gh_username: str, auth_username: str, auth_token: str):
    """Return url of github avatar."""

    avatar_url = None

    if gh_username is not None:
        print(f"getting avatar: {gh_username}")
        url = f"https://api.github.com/users/{gh_username}"
        response = requests.get(url, auth=(auth_username, auth_token))
        if response.status_code == 200:
            avatar_url = response.json()["avatar_url"]

    return avatar_url


def return_missing_from_tributors(tributors_file: Path, names: list[str]) -> list[str]:
    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"].strip() for x in tributors]
    for i, name in enumerate(names):
        names[i] = name.strip()
    missing_from_tributors = set(names) - set(tributors_names)
    return sorted(list(missing_from_tributors))


def sort_tributors(tributors) -> dict:
    for key in tributors:
        tributors[key] = dict(OrderedDict(sorted(tributors[key].items())))
    return dict(sorted(tributors.items(), key=lambda item: item[1]["name"]))


def add_to_tributors(tributors, this_contributor: str):
    name = this_contributor.get("name").strip()

    tributors_names = [tributors[x]["name"].strip() for x in tributors]
    if name in tributors_names:
        return tributors

    print(f"adding {name}")

    user_login = this_contributor.get("github_username")
    this_contributor.pop("github_username", None)

    tributors[user_login] = this_contributor
    return tributors


def sort_all_contrib(allcontrib):
    for i, contrib in enumerate(allcontrib["contributors"]):
        allcontrib["contributors"][i] = dict(OrderedDict(sorted(contrib.items())))
    allcontrib["contributors"] = sorted(
        allcontrib["contributors"], key=lambda x: x["name"]
    )
    return allcontrib


def add_to_allcontrib(allcontrib_file, user: str):
    user = user.strip()
    allcontrib = load_allcontrib(allcontrib_file)
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    if user not in allcontrib_names:
        print(f"adding {user} to {allcontrib_file}")
        user_login = user.lower().replace(" ", "_")
        allcontrib["contributors"].append(
            {
                "name": user,
                "login": user_login,
                "contributions": [
                    "doc",
                ],
            }
        )
        write_allcontrib(allcontrib_file, allcontrib)


def return_author_list_for_cff(tributors_file):
    tributors = load_tributors(tributors_file)

    author_list = []

    for _, tributor in enumerate(tributors, start=1):
        this_tributor = tributors[tributor]

        name = this_tributor["name"]

        # take as given name the first part of the name and anything ending with a dot
        # suboptimal for people with multiple given names
        given_names = name.split()[0]
        str_index = 1
        while str_index < len(name.split()) and name.split()[str_index].endswith("."):
            given_names += f" {name.split()[str_index]}"
            str_index += 1

        new_contrib = {
            "given-names": given_names,
        }

        if family_names := " ".join(name.split()[str_index:]):
            new_contrib["family-names"] = family_names

        if "blog" in this_tributor:
            new_contrib["website"] = this_tributor["blog"]

        if "orcid" in this_tributor:
            new_contrib["orcid"] = "https://orcid.org/" + this_tributor["orcid"]

        if "affiliation" in this_tributor:
            new_contrib["affiliation"] = this_tributor["affiliation"]

        if "email" in this_tributor:
            new_contrib["email"] = this_tributor["email"]

        author_list.append(new_contrib)

    return author_list


def return_this_contributor(tsv: pd.DataFrame, name: str):
    name = name.strip()

    mask = tsv.name == name

    github = tsv[mask].github.values[0]
    if pd.isna(github) or not isinstance(github, (str)):
        github = None

    github_username = None
    if github is not None:
        github_username = github.replace("https://github.com/", "").strip(" ")
    if github_username is None:
        github_username = name.lower().replace(" ", "_")

    contributions = tsv[mask].contributions[0]
    if pd.isna(contributions) or contributions is None:
        raise ValueError(f"Contributions for {name} not defined in input file.")
    allowed_contributions = list(emoji_map().keys())[0]
    if any(x for x in contributions if x not in allowed_contributions):
        raise ValueError(
            f"Contributions must be one of {allowed_contributions}."
            f" Got '{contributions}' for {name}."
        )

    website = tsv[mask].website.values[0]
    if pd.isna(website) or not isinstance(website, (str)):
        website = github

    affiliation = tsv[mask].affiliation.values[0]
    if pd.isna(affiliation) or not isinstance(affiliation, (str)):
        affiliation = None

    orcid = tsv[mask].orcid.values[0]
    if pd.isna(orcid) or not isinstance(orcid, (str)):
        orcid = None
    if orcid is not None:
        orcid = orcid.replace("http://", "https://")

    email = tsv[mask].email.values[0]
    if pd.isna(email) or not isinstance(email, (str)):
        email = None

    return {
        "name": name,
        "github": github,
        "github_username": github_username,
        "blog": website,
        "affiliation": affiliation,
        "orcid": orcid,
        "email": email,
    }


def rename_keys_for_allcontrib(this_contributor):
    renaming_map = {
        "name": "name",
        "avatar_url": "avatar_url",
        "github_username": "login",
        "login": "login",
        "blog": "profile",
        "contributions": "contributions",
    }

    renamed = {
        renaming_map[key]: this_contributor[key]
        for key in this_contributor
        if key in renaming_map
    }
    return renamed


def main():
    token = None
    if TOKEN_FILE is not None:
        with open(Path(TOKEN_FILE)) as f:
            token = f.read().strip()

    df = pd.read_csv(INPUT_FILE, sep="\t", encoding="utf8")
    print(df.head())

    tributors_file = root_dir() / ".tributors"
    allcontrib_file = root_dir() / ".all-contributorsrc"
    citation_file = root_dir() / "CITATION.cff"

    print("\n[red]NOT IN .tributors FILE[/red]")
    new_contrib_names = df.name.to_list()
    missing_from_tributors = return_missing_from_tributors(
        tributors_file, new_contrib_names
    )
    print(missing_from_tributors)

    tributors = load_tributors(tributors_file)
    allcontrib = load_allcontrib(allcontrib_file)
    citation = load_citation(citation_file)

    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    tributors_names = [tributors[x]["name"] for x in tributors]

    # sanity checks
    assert len(tributors_names) == len(set(tributors_names))
    assert len(allcontrib_names) == len(set(allcontrib_names))
    assert len(tributors_names) == len(allcontrib_names)
    assert len(tributors_names) == len(citation["authors"])

    print("\n[green]ADDING TO .tributors[/green]")
    for name in missing_from_tributors:
        this_contributor = return_this_contributor(df, name)
        add_to_tributors(tributors, this_contributor)

    write_tributors(tributors_file, tributors)

    print("\n[green]UPDATING .all-contributorsrc[/green]")
    for github_username in tributors:
        this_contributor = tributors[github_username]
        if UPDATE_AVATARS:
            avatar_url = get_gh_avatar(
                this_contributor["github_username"], GH_USERNAME, token
            )
            this_contributor["avatar_url"] = avatar_url
        this_contributor["login"] = github_username
        this_contributor = rename_keys_for_allcontrib(this_contributor)

        allcontrib = updating_allcontrib(allcontrib, this_contributor)

    write_allcontrib(allcontrib_file, allcontrib)

    print("\n[green]UPDATING CITATION.CFF[/green]")
    citation = load_citation(citation_file)
    citation["authors"] = return_author_list_for_cff(tributors_file)
    write_citation(citation_file, citation)

    citation = create_citation(infile=citation_file, url=None)
    validate_or_write_output(
        outfile=None, outputformat=None, validate_only=True, citation=citation
    )


if __name__ == "__main__":
    main()
