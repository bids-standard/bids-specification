from pathlib import Path

import emoji

from utils import emoji_map
from utils import load_allcontrib, root_dir

tmp_file = Path(__file__).parent.joinpath("tmp.md")


def contributor_table_header(max_name_length, max_contrib_length):
    return f"""# Contributors

Legend (source:
<https://allcontributors.org/docs/en/emoji-key>)

The following individuals have contributed to the Brain Imaging Data Structure
ecosystem (in alphabetical order).
If you contributed to the BIDS ecosystem and your name is not listed, please add it.

|name{" " * (max_name_length-4)}|contributions{" " * (max_contrib_length-13)}|
|{"-" * max_name_length}|{"-"*max_contrib_length}|
"""


def create_line_contributor(contributor, max_name_length, max_contrib_length):
    # TODO add link to contributor blog? or orcid?
    name = contributor["name"]

    line = f"| {name}{' '*(max_name_length-len(name)-1)}|"

    nb_contrib = len(contributor["contributions"]) * 2
    for contrib in contributor["contributions"]:
        line += emoji.emojize(emoji_map()[contrib])

    line += f"{' '*(max_contrib_length-nb_contrib)}|\n"

    return line


def main():

    allcontrib_file = root_dir().joinpath(".all-contributorsrc")
    allcontrib = load_allcontrib(allcontrib_file)

    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    sorted_allcontrib_names = sorted(allcontrib_names)

    max_name_length = len(max(allcontrib_names, key=len))

    max_contrib_length = (
        max(len(x["contributions"]) for x in allcontrib["contributors"]) * 2
    )

    with open(tmp_file, "w", encoding="utf8") as output_file:
        output_file.write(contributor_table_header(max_name_length, max_contrib_length))

        for name in sorted_allcontrib_names:
            index_allcontrib = allcontrib_names.index(name)
            this_contrib = allcontrib["contributors"][index_allcontrib]
            output_file.write(
                create_line_contributor(
                    this_contrib, max_name_length, max_contrib_length
                )
            )


if __name__ == "__main__":
    main()
