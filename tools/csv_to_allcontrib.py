import pandas as pd
import emoji
import re
import json
from rich import print

contributor = []

# https://allcontributors.org/docs/en/emoji-key
emoji_map = {
    ":laptop:": "code,",
    ":open_book:": "doc,",
    ":thinking_face:": "ideas,",
    ":bug:": "bug,",
    ":light_bulb:": "example,",
    ":speech_balloon:": "question,",
    ":eyes:": "review,",
    ":electric_plug:": "plugin,",
    ":magnifying_glass_tilted_left:": "fundingFinding,",
    ":loudspeaker:": "talk,",
    ":artist_palette:": "design,",
    ":input_symbols:": "data,",
    ":wrench:": "tool,",
    ":tear-off_calendar:": "projectManagement,",
    ":warning:": "test,",
    ":clipboard:": "eventOrganizing,",
    ":metro:": "infra,",
    ":notebook:": "userTesting,",
    ":video_camera:": "video,",
    ":memo:": "blog,",
    ":fountain_pen:": "content,",
    ":check_mark_button:": "tutorial,",
    ":construction:": "maintenance,",
    ":dollar_banknote:": "financial,",
}


df = pd.read_csv("bids_contributors_no_email.csv", encoding="utf8")

# print(df)

contributors = df.Name

contributors_list = []

allcontrib_file = "/home/remi/github/BIDS-specification/.all-contributorsrc"


def load_from_allcontrib(allcontrib_file):
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


# sourcery skip: use-named-expression
allcontrib = load_from_allcontrib(allcontrib_file)

for contrib in contributors:

    x = contrib.split()

    """parse contributions
    """
    contributions = x[-1]
    # print(contributions)

    contributions_text = emoji.replace_emoji(
        contributions, replace=lambda chars, data_dict: data_dict["en"]
    )

    for key, value in emoji_map.items():
        contributions_text = re.sub(key, value, contributions_text)

    contributions_text = contributions_text.split(sep=",")
    contributions_text[:] = [x for x in contributions_text if x]
    # print(contributions_text)

    """update contributors
    """
    name = " ".join(x[:-1])

    tmp = list(filter(lambda item: item["name"] == name, allcontrib["contributors"]))

    if tmp:
        tmp[0]["contributions"] = contributions_text
        contributors_list.append(tmp[0])
    else:

        # create temporary login place holder
        login = name.lower()
        login = re.sub("[. -']", "_", login)
        login = re.sub("__", "_", login)
        login = "TMP_" + login

        contributors_list.append(
            {
                "name": name,
                "login": login,
                "contributions": contributions_text,
            }
        )

"""
append the ones that were not in the CSV
most likely duplicates that will have to be cleaned up manually
"""
contributors_name_list = [x["name"] for x in contributors_list]

for contrib in allcontrib["contributors"]:

    name = contrib["name"]
    if name not in contributors_name_list:
        # print(name)
        contributors_list.append(contrib)


# sort alphabetically
contributors_list = sorted(contributors_list, key=lambda i: i["name"])

print(contributors_list)

print(len(contributors_list))

allcontrib["contributors"] = contributors_list

with open(allcontrib_file, "w", encoding="utf8") as output_file:

    json.dump(allcontrib, output_file, indent=4, ensure_ascii=False)
