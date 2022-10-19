import pandas as pd
from rich import print

from utils import load_tributors, root_dir


tributors_file = root_dir().joinpath(".tributors")

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
print("\n")

bids_contributors_old = pd.read_csv(
    "bids_contributors_old.tsv", sep="\t", encoding="utf8"
)
bids_contributors_old_emails_names = [x.strip() for x in bids_contributors_old.name]
