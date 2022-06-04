import json
import yaml

with open("../.all-contributorsrc", "r") as allcontrib_file:
    allcontrib = json.load(allcontrib_file)

    with open("../CITATION.cff", "r") as citation_file:
        citation = yaml.load(citation_file, Loader=yaml.FullLoader)

        author_list = []

        for contrib in allcontrib["contributors"]:
            name = contrib["name"]
            given_names = name.split()[0]
            family_names = " ".join(name.split()[1:])

            website = contrib["profile"]

            print(family_names)
            print(given_names)
            print(website)

            author_list.append(
                {
                    "family-names": family_names,
                    "given-names": given_names,
                    "website": website,
                }
            )

        citation["authors"] = author_list

        with open("../CITATION_new.cff", "w") as new_citation_file:
            yaml.dump(citation, new_citation_file)
