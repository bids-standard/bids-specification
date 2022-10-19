import json

from pathlib import Path

from rich import print

from utils import write_tributors


def load_tributors(tributors_file):
    with open(tributors_file, "r", encoding="utf8") as tributors_file:
        return json.load(tributors_file)


def load_from_allcontrib(allcontrib_file):
    with open(allcontrib_file, "r", encoding="utf8") as input_file:
        return json.load(input_file)


def main():

    root_dir = Path(__file__).parent.joinpath("..").resolve()
    print(root_dir)

    tributors_file = root_dir.joinpath(".tributors")
    allcontrib_file = root_dir.joinpath(".all-contributorsrc")

    tributors = load_tributors(tributors_file)
    tributors_keys = list(tributors.keys())
    tributors_names = [tributors[x]["name"] for x in tributors]
    # print(tributors_keys)
    # print(tributors_names)

    allcontrib = load_from_allcontrib(allcontrib_file)
    allcontrib_names = [x["name"] for x in allcontrib["contributors"]]
    # print(allcontrib["contributors"])
    # print(allcontrib_names)

    for name in allcontrib_names:

        index_tributor = tributors_names.index(name)
        old_key_tributor = tributors_keys[index_tributor]

        index_allcontrib = allcontrib_names.index(name)
        new_key = allcontrib["contributors"][index_allcontrib]["login"]

        if new_key != old_key_tributor:
            tributors[new_key] = tributors.pop(old_key_tributor)
            print(f"\n[cyan]{name.upper()}[/cyan]")
            print(old_key_tributor)
            print(new_key)

    write_tributors(tributors_file, tributors)


if __name__ == "__main__":
    main()
