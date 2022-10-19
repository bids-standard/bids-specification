"""Replace author field of CITATION.CFF with content from .tributors"""

import json
import ruamel.yaml

from rich import print

from utils import load_citation, root_dir, write_citation


yaml = ruamel.yaml.YAML()

citation_file = root_dir().joinpath("CITATION.cff")
tributors_file = root_dir().joinpath(".tributors")


def main():

    with open(tributors_file, "r", encoding="utf8") as input_file:
        tributors = json.load(input_file)

    author_list = []

    for count, tributor in enumerate(tributors, start=1):

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

        # print(count)
        # print(new_contrib)

        author_list.append(new_contrib)

    citation = load_citation(citation_file)
    citation["authors"] = author_list

    write_citation(citation_file, citation)


if __name__ == "__main__":
    main()
