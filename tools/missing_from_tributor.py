import pandas as pd
from rich import print

from utils import load_tributors, root_dir

def rename_columns(df):
    df.rename(
        columns={
            "Name  For example: Jane Smith": "name",
            "Primary affiliation  Please include:  Institution, Department, City, (State), Zip Code, Country": "affiliation",
            "ORCID number  For example:  https://orcid.org/0000-0002-1535-9777": "orcid",
            "Github username  For example:   https://github.com/Jane-Smith": "github",
            "I agree to have my email address on the github repository of the BIDS specification": "consent",
            "Email address": "email",
            "Added to .tributors file in repo": "added",
        },
        inplace=True,
    )
    return df

tributors_file = root_dir().joinpath(".tributors")


tributors = load_tributors(tributors_file)
tributors_names = [tributors[x]["name"].rstrip() for x in tributors]

bids_contributors_old = pd.read_csv("bids_contributors_old.tsv", sep="\t", encoding="utf8")

print("\n[red]From old contributors and NOT IN .tributors FILE[/red]")
in_tributors = bids_contributors_old.name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(bids_contributors_old.name[i])
print("\n")

bids_contributors_old_emails = pd.read_csv("BIDS-contributor_emails.tsv", sep="\t", encoding="utf8")

print("\n[red]From email list and NOT IN .tributors FILE[/red]")
in_tributors = bids_contributors_old_emails.Name.isin(tributors_names).to_list()
for i, value in enumerate(in_tributors):
    if not value:
        print(bids_contributors_old_emails.Name[i])
print("\n")

bids_contributors_old_emails_names = [x.strip() for x in bids_contributors_old.name]

bids_contributors_new_emails = pd.read_csv("contributors.tsv", sep="\t", encoding="utf8")
bids_contributors_new_emails = rename_columns(bids_contributors_new_emails)
bids_contributors_new_emails_names = [x.strip() for x in bids_contributors_new_emails.name]

print("\n[red]From new email list and not in old email list[/red]")
new_ones = set(bids_contributors_new_emails_names) - set(bids_contributors_old_emails_names)
print(new_ones)

for i in new_ones:
    y = bids_contributors_new_emails[bids_contributors_new_emails.name == i]
    print(f"{y['name'].values[0]}, {y['email'].values[0]}")
    z = bids_contributors_old_emails[bids_contributors_old_emails.Name == i]
    print(f"{z['Name'].values[0]}, {z['Email'].values[0]}")
