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

from __future__ import annotations

import json
import logging
from collections import OrderedDict
from pathlib import Path
from typing import Optional

import emoji
import pandas as pd
import requests
import ruamel.yaml
from cffconvert.cli.create_citation import create_citation
from cffconvert.cli.validate_or_write_output import validate_or_write_output
from rich.logging import RichHandler
from rich.traceback import install

yaml = ruamel.yaml.YAML()
yaml.indent(mapping=2, sequence=4, offset=2)

UPDATE_AVATARS = False

GH_USERNAME = "Remi-Gau"

TOKEN_FILE = None

INPUT_FILE = Path(__file__).parent / "new_contributors.tsv"

LOG_LEVEL = "DEBUG"  # 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'


def logger(log_level="INFO") -> logging.Logger:
    """Create log."""
    # let rich print the traceback
    install(show_locals=True)
    FORMAT = "%(asctime)s - %(message)s"
    logging.basicConfig(
        level=log_level, format=FORMAT, datefmt="[%X]", handlers=[RichHandler()]
    )
    return logging.getLogger("rich")


log = logger(log_level=LOG_LEVEL)


def root_dir() -> Path:
    return Path(__file__).parent.parent


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


def return_this_contributor(
    df: pd.DataFrame, name: str, contribution_needed=True
) -> dict[str, Optional[str]]:
    """Get and validate the data for a given contributor from a panda dataframe"""
    name = name.strip()

    mask = df.name == name

    github = df[mask].github.values[0]
    if pd.isna(github) or not isinstance(github, (str)):
        github = None

    github_username = None
    if github is not None:
        github_username = github.replace("https://github.com/", "")
    if github_username is None:
        github_username = name.lower().replace(" ", "_")

    contributions = df[mask].contributions.values[0]
    log.debug(f"contributions for {name}: '{contributions}'")
    if pd.isna(contributions):
        contributions is None
    if contribution_needed and contributions is None:
        raise ValueError(f"Contributions for {name} not defined in input file.")
    if contributions is not None:
        contributions = listify_contributions(contributions)
        validate_contributions(contributions, name)
        contributions = canonicalize_contributions(contributions)
    log.debug(f"kept contributions for {name}: {contributions}")

    orcid = df[mask].orcid.values[0]
    if pd.isna(orcid) or not isinstance(orcid, (str)):
        orcid = None
    if orcid is not None:
        orcid = orcid.replace("http://", "https://")

    website = df[mask].website.values[0]
    affiliation = df[mask].affiliation.values[0]
    email = df[mask].email.values[0]

    this_contributor = {
        "name": name,
        "github": github,
        "github_username": github_username,
        "blog": website,
        "affiliation": affiliation,
        "orcid": orcid,
        "email": email,
        "contributions": contributions,
    }

    # light validation / clean up
    for key, value in this_contributor.items():
        if value is None:
            continue
        elif not isinstance(this_contributor[key], (list)) and pd.isna(
            this_contributor[key]
        ):
            this_contributor[key] = None
        elif isinstance(this_contributor[key], (str)):
            this_contributor[key] = this_contributor[key].strip()
        elif all(pd.isna(x) for x in this_contributor[key]):
            this_contributor[key] = None

    return this_contributor


def listify_contributions(contributions: str):
    contributions = [x.strip() for x in contributions.split(",")]
    tmp = []
    for contribution_ in contributions:
        tmp.extend(iter(contribution_.split(" ")))
    return tmp


def validate_contributions(contributions: list, name: str):
    allowed_contributions = list(emoji_map().keys())
    allowed_emojis = [emoji.emojize(x) for x in list(emoji_map().values())]
    allowed_contributions += allowed_emojis
    allowed_contributions.extend(x.replace(":", "") for x in list(emoji_map().values()))
    if any(x for x in contributions if x.replace(":", "") not in allowed_contributions):
        raise ValueError(
            f"Contributions must be one of {allowed_contributions}.\n"
            f" Got '{contributions}' for {name}."
        )


def canonicalize_contributions(contributions: list) -> list:
    allowed_emojis = [emoji.emojize(x) for x in list(emoji_map().values())]
    for contribution_ in contributions:
        if contribution_ in allowed_emojis:
            contributions[contributions.index(contribution_)] = emoji.demojize(
                contribution_
            ).replace(":", "")
    for contribution_ in contributions:
        contributions[contributions.index(contribution_)] = contribution_.replace(
            ":", ""
        )
    contributions = sorted(list(set(contributions)))

    return contributions


def update_key(
    contributor: dict[str, str], key: str, value: str | None
) -> dict[str, str]:
    """Update a key in a contributor dict if the value is not None."""
    if value is None:
        return contributor
    log.info(f"updating {contributor['name']} - {key}")
    contributor[key] = value
    return contributor


"""TRIBUTORS"""


def load_tributors(tributors_file: Path) -> dict:
    """Load .tributors file."""
    with open(tributors_file, "r", encoding="utf8") as tributors_file:
        return json.load(tributors_file)


def write_tributors(tributors_file: Path, tributors: dict[str, dict]) -> None:
    """Write .tributors file."""
    tributors = sort_tributors(tributors)
    with open(tributors_file, "w", encoding="utf8") as output_file:
        json.dump(tributors, output_file, indent=4, ensure_ascii=False)


def return_missing_from_tributors(tributors_file: Path, names: list[str]) -> list[str]:
    """Return list of names that are in the input file but not in the .tributors file."""
    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"] for x in tributors]
    for i, name in enumerate(names):
        names[i] = name.strip()
    missing_from_tributors = set(names) - set(tributors_names)
    return sorted(list(missing_from_tributors))


def sort_tributors(tributors: dict[str, dict]) -> dict[str, dict]:
    """Sort tributors alphabetically by name of contributor."""
    for key in tributors:
        tributors[key] = dict(OrderedDict(sorted(tributors[key].items())))
    return dict(sorted(tributors.items(), key=lambda item: item[1]["name"]))


def add_to_tributors(
    tributors: dict[str, dict], this_contributor: dict[str, str]
) -> dict[str, dict]:
    """Add contributor to .tributors"""
    name = this_contributor.get("name")

    tributors_names = [tributors[x]["name"] for x in tributors]
    if name in tributors_names:
        return tributors

    log.info(f"adding {name}")

    user_login = this_contributor.get("github_username")
    this_contributor.pop("github_username", None)

    tributors[user_login] = this_contributor
    return tributors


def update_tributors(
    tributors: dict[str, dict], this_contributor: dict[str, str]
) -> dict[str, dict]:
    tributors_names = [tributors[x]["name"] for x in tributors]

    name = this_contributor["name"]

    if name not in tributors_names:
        return tributors

    index_tributor = tributors_names.index(this_contributor["name"])
    tributors_keys = list(tributors.keys())
    key_tributor = tributors_keys[index_tributor]

    for key, value in this_contributor.items():
        if key == "github_username" or value is None:
            continue

        if key not in tributors[key_tributor]:
            tributors[key_tributor] = update_key(
                contributor=tributors[key_tributor],
                key=key,
                value=value,
            )

        if tributors[key_tributor][key] != value:
            tributors[key_tributor] = update_key(
                contributor=tributors[key_tributor],
                key=key,
                value=value,
            )

    return tributors


"""ALCONTRIB"""


def load_allcontrib(allcontrib_file: Path) -> None:
    """Load .all-contributorsrc file."""
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


def write_allcontrib(allcontrib_file: Path, allcontrib: dict) -> None:
    """Write .all-contributorsrc file."""
    allcontrib = sort_all_contrib(allcontrib)
    with open(allcontrib_file, "w", encoding="utf8") as output_file:
        json.dump(allcontrib, output_file, indent=4, ensure_ascii=False)


def sort_all_contrib(allcontrib: dict) -> dict:
    """Sort .all-contributorsrc file alphabetically by name of contributor."""
    for i, contrib in enumerate(allcontrib["contributors"]):
        allcontrib["contributors"][i] = dict(OrderedDict(sorted(contrib.items())))
    allcontrib["contributors"] = sorted(
        allcontrib["contributors"], key=lambda x: x["name"]
    )
    return allcontrib


def update_allcontrib(allcontrib: dict, this_contributor: dict[str, str]) -> dict:
    """Add a contributor if not in .all-contributorsrc, or update if already in."""
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]

    if this_contributor["name"] not in allcontrib_names:
        log.info(f"adding {this_contributor['name']}")
        allcontrib["contributors"].append(this_contributor)
        return allcontrib

    index_allcontrib = allcontrib_names.index(this_contributor["name"])

    for key, value in this_contributor.items():
        if key not in allcontrib["contributors"][index_allcontrib]:
            allcontrib["contributors"][index_allcontrib] = update_key(
                contributor=allcontrib["contributors"][index_allcontrib],
                key=key,
                value=value,
            )

        if allcontrib["contributors"][index_allcontrib][key] != value:
            allcontrib["contributors"][index_allcontrib] = update_key(
                contributor=allcontrib["contributors"][index_allcontrib],
                key=key,
                value=value,
            )

    return allcontrib


def get_gh_avatar(gh_username: str, auth_username: str, auth_token: str) -> str:
    """Return url of github avatar."""
    avatar_url = None

    if gh_username is None:
        return avatar_url

    log.info(f"getting avatar: {gh_username}")
    url = f"https://api.github.com/users/{gh_username}"
    response = requests.get(url, auth=(auth_username, auth_token))
    if response.status_code == 200:
        avatar_url = response.json()["avatar_url"]

    return avatar_url


def rename_keys_for_allcontrib(this_contributor: dict[str, str]) -> dict[str, str]:
    """Rename some keys to adapt to all-contributors."""
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


"""CITATION.CFF"""


def load_citation(citation_file: Path) -> dict:
    """Load CITATION.CFF file."""
    with open(citation_file, "r", encoding="utf8") as input_file:
        return yaml.load(input_file)


def write_citation(citation_file: Path, citation: dict) -> None:
    """Write CITATION.CFF file."""
    with open(citation_file, "w", encoding="utf8") as output_file:
        return yaml.dump(citation, output_file)


def return_author_list_for_cff(tributors_file: Path) -> list[dict[str, str]]:
    """Create an dict to be used for the authors in the CITATION.CFF file."""
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

        if this_tributor.get("website") is not None:
            new_contrib["website"] = this_tributor["blog"]

        if this_tributor.get("orcid") is not None:
            new_contrib["orcid"] = "https://orcid.org/" + this_tributor["orcid"]

        if this_tributor.get("affiliation") is not None:
            new_contrib["affiliation"] = this_tributor["affiliation"]

        if this_tributor.get("email") is not None:
            new_contrib["email"] = this_tributor["email"]

        author_list.append(new_contrib)

    return author_list


"""MAIN"""


def main():
    token = None
    if TOKEN_FILE is not None:
        with open(Path(TOKEN_FILE)) as f:
            token = f.read().strip()

    log.debug(f"Reading: {INPUT_FILE}")
    df = pd.read_csv(INPUT_FILE, sep="\t", encoding="utf8")
    log.debug(f"\n{df.head()}")

    tributors_file = root_dir() / ".tributors"
    allcontrib_file = root_dir() / ".all-contributorsrc"
    citation_file = root_dir() / "CITATION.cff"

    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"] for x in tributors]

    allcontrib = load_allcontrib(allcontrib_file)
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]

    citation = load_citation(citation_file)

    # sanity checks to make sure no contributor was added manually
    assert len(tributors_names) == len(set(tributors_names))
    assert len(allcontrib_names) == len(set(allcontrib_names))
    assert len(tributors_names) == len(allcontrib_names)
    assert len(tributors_names) == len(citation["authors"])

    new_contrib_names = df.name.to_list()
    missing_from_tributors = return_missing_from_tributors(
        tributors_file, new_contrib_names
    )
    if len(missing_from_tributors) != 0:
        log.info("ADDING TO .tributors")
        for name in missing_from_tributors:
            this_contributor = return_this_contributor(df, name)
            add_to_tributors(tributors, this_contributor)

    contributors_to_update = set(new_contrib_names) - set(missing_from_tributors)
    if len(contributors_to_update) != 0:
        log.info("UPDATING .tributors")
        for name in contributors_to_update:
            this_contributor = return_this_contributor(
                df=df, name=name, contribution_needed=False
            )
            tributors = update_tributors(tributors, this_contributor)

    write_tributors(tributors_file, tributors)

    log.info("UPDATING .all-contributorsrc")
    for github_username in tributors:
        this_contributor = tributors[github_username]
        this_contributor["login"] = github_username
        this_contributor = rename_keys_for_allcontrib(this_contributor)

        if UPDATE_AVATARS:
            avatar_url = get_gh_avatar(
                this_contributor["github_username"], GH_USERNAME, token
            )
            this_contributor["avatar_url"] = avatar_url

        allcontrib = update_allcontrib(allcontrib, this_contributor)

    write_allcontrib(allcontrib_file, allcontrib)

    log.info("UPDATING CITATION.cff")
    citation = load_citation(citation_file)
    citation["authors"] = return_author_list_for_cff(tributors_file)
    write_citation(citation_file, citation)

    log.info("VALIDATING CITATION.cff")
    citation = create_citation(infile=citation_file, url=None)
    validate_or_write_output(
        outfile=None, outputformat=None, validate_only=True, citation=citation
    )


if __name__ == "__main__":
    main()
