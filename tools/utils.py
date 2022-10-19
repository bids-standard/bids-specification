from pathlib import Path
import json
import ruamel.yaml
import emoji
from rich import print


def root_dir():
    return Path(__file__).parent.parent


def load_tributors(tributors_file):
    with open(tributors_file, "r", encoding="utf8") as tributors_file:
        return json.load(tributors_file)


def load_from_allcontrib(allcontrib_file):
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


def load_citation(citation_file):
    yaml = ruamel.yaml.YAML()
    with open(citation_file, "r", encoding="utf8") as input_file:
        return yaml.load(input_file)


def emoji_map():
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


def return_missing_from_tributors(tributors_file, names: list[str]) -> list[str]:
    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"].strip() for x in tributors]
    for i, name in enumerate(names):
        names[i] = name.strip()
    missing_from_tributors = set(names) - set(tributors_names)
    return sorted(list(missing_from_tributors))


def add_to_tributors(tributors_file, user: str):
    user = user.strip()
    tributors = load_tributors(tributors_file)
    tributors_names = [tributors[x]["name"].strip() for x in tributors]
    if user not in tributors_names:
        print(f"adding {user} to {tributors_file}")
        user_login = user.lower().replace(" ", "_")
        tributors[user_login] = {"name": user}
        with open(tributors_file, "w", encoding="utf8") as output_file:
            json.dump(tributors, output_file, indent=4, ensure_ascii=False)


def add_to_allcontrib(allcontrib_file, user: str):
    user = user.strip()
    allcontrib = load_from_allcontrib(allcontrib_file)
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
        with open(allcontrib_file, "w", encoding="utf8") as output_file:
            json.dump(allcontrib, output_file, indent=4, ensure_ascii=False)
