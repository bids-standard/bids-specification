import pandas as pd
from rich import print

from utils import load_tributors, root_dir


tributors_file = root_dir().joinpath(".tributors")


tributors = load_tributors(tributors_file)
tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

tsv = pd.read_csv("bids_contributors_old.tsv", sep="\t", encoding="utf8")

print("\n[red]From old contributors and NOT IN .tributors FILE[/red]")
in_tributors = tsv.name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(tsv.name[i])
print("\n")

tsv = pd.read_csv("BIDS-contributor_emails.tsv", sep="\t", encoding="utf8")

print("\n[red]From email list and NOT IN .tributors FILE[/red]")
in_tributors = tsv.Name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(tsv.Name[i])
print("\n")
