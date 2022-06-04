import json
import ruamel.yaml

yaml = ruamel.yaml.YAML()

citation_file = "/home/remi/github/BIDS-specification/CITATION.cff"

def load_citation(citation_file):
    with open(citation_file, "r", encoding="utf8") as input_file:
        return yaml.load(input_file)

with open("../.tributors", "r", encoding="utf8") as tributors_file:
    tributors = json.load(tributors_file)

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
