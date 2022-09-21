import pandas as pd
from rich import print

from utils import load_tributors, root_dir


tributors_file = root_dir().joinpath(".tributors")


tsv = pd.read_csv("bids_contributors_old.tsv", sep="\t", encoding="utf8")

tributors = load_tributors(tributors_file)
tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

print("\n[red]NOT IN .tributors FILE[/red]")
in_tributors = tsv.name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(tsv.name[i])
print("\n")
