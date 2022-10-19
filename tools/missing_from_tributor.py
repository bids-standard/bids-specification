import pandas as pd
from rich import print

from utils import load_tributors, root_dir, add_to_tributors, add_to_allcontrib


tributors_file = root_dir().joinpath(".tributors")
allcontrib_file = root_dir().joinpath(".all-contributorsrc")

tributors = load_tributors(tributors_file)
tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

bids_contributors_old = pd.read_csv(
    "BIDS-contributor_emails.tsv", sep="\t", encoding="utf8"
)

print("\n[red]From email list and NOT IN .tributors FILE[/red]")
in_tributors = bids_contributors_old.Name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(f"{bids_contributors_old.Name[i]} {bids_contributors_old.Email[i]}")
        add_to_tributors(tributors_file, bids_contributors_old.Name[i])
        add_to_allcontrib(allcontrib_file, bids_contributors_old.Name[i])
print("\n")
