from rich import print

from utils import (
    add_to_tributors,
    add_to_allcontrib,
    get_gh_avatar,
    load_citation,
    load_from_allcontrib,
    load_tributors,
    root_dir,
    return_author_list_for_cff,
    return_missing_from_tributors,
    write_citation,
    write_from_allcontrib,
    write_tributors,
)

tributors_file = root_dir().joinpath(".tributors")
allcontrib_file = root_dir().joinpath(".all-contributorsrc")

tributors = load_tributors(tributors_file)
tributors_keys = list(tributors.keys())
tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

allcontrib = load_from_allcontrib(allcontrib_file)
allcontrib_names = [x["name"] for x in allcontrib["contributors"]]

for name in allcontrib_names:
    index_allcontrib = allcontrib_names.index(name)
    print("\n")
    print(allcontrib["contributors"][index_allcontrib])

    index_tributor = tributors_names.index(name)
    key_tributor = tributors_keys[index_tributor]

    tributors[key_tributor]["contributions"] = allcontrib["contributors"][
        index_allcontrib
    ]["contributions"]
    print(tributors[key_tributor])

write_tributors(tributors_file, tributors)
