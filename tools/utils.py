import json
from collections import OrderedDict
from pathlib import Path

import requests
import ruamel.yaml
from rich import print

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


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


def add_to_tributors(tributors_file, user: str):
    user = user.strip()
    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"].strip() for x in tributors]
    if user not in tributors_names:
        print(f"adding {user} to {tributors_file}")
        user_login = user.lower().replace(" ", "_")
        tributors[user_login] = {"name": user}
        write_tributors(tributors_file, tributors)


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


def return_this_contributor(tsv, name: str):
    name = name.strip()

    mask = tsv.name == name

    github = tsv[mask].github.values[0]
    if not isinstance(github, (str)):
        github = None

    github_username = None
    if github is not None:
        github_username = github.replace("https://github.com/", "").strip(" ")

    website = tsv[mask].website.values[0]
    if not isinstance(website, (str)):
        website = github

    affiliation = tsv[mask].affiliation.values[0]
    if not isinstance(affiliation, (str)):
        affiliation = None

    orcid = tsv[mask].orcid.values[0]
    if not isinstance(orcid, (str)):
        orcid = None
    if orcid is not None:
        orcid = orcid.replace("http://", "https://")

    email = tsv[mask].email.values[0]
    if not isinstance(email, (str)):
        email = None

    return {
        "name": name,
        "github": github,
        "github_username": github_username,
        "website": website,
        "affiliation": affiliation,
        "orcid": orcid,
        "email": email,
    }
