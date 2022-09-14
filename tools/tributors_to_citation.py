"""Replace author field of CITATION.CFF with content from .tributors"""

import json
import ruamel.yaml

from rich import print

from pathlib import Path

yaml = ruamel.yaml.YAML()

root_dir = Path(__file__).parent.parent

citation_file = root_dir.joinpath("CITATION.cff")
tributors_file = root_dir.joinpath(".tributors")


def load_citation(citation_file):
    with open(citation_file, "r", encoding="utf8") as input_file:
        return yaml.load(input_file)


def main():

    with open(tributors_file, "r", encoding="utf8") as input_file:
        tributors = json.load(input_file)

    author_list = []

    for count, tributor in enumerate(tributors, start=1):

        print(count)

        this_tributor = tributors[tributor]

        name = this_tributor["name"]

        given_names = name.split()[0]

        new_contrib = {
            "given-names": given_names,
        }

        if family_names := " ".join(name.split()[1:]):
            new_contrib["family-names"] = family_names

        if "blog" in this_tributor:
            new_contrib["website"] = this_tributor["blog"]

        if "orcid" in this_tributor:
            new_contrib["orcid"] = "https://orcid.org/" + this_tributor["orcid"]

        if "affiliation" in this_tributor:
            new_contrib["affiliation"] = this_tributor["affiliation"]

        if "email" in this_tributor:
            new_contrib["email"] = this_tributor["email"]

        print(new_contrib)

        author_list.append(new_contrib)

    citation = load_citation(citation_file)
    citation["authors"] = author_list

    with open(citation_file, "w") as output_file:
        yaml.dump(citation, output_file)


if __name__ == "__main__":
    main()
