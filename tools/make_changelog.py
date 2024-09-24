#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "httpx",
# ]
# ///

# How to use this script:
# 1. Go to https://github.com/bids-standard/bids-specification/releases/new and
#    generate a new changelog. Do not release. Paste the contents into `auto-changelog.txt`.
# 2. Generate a GitHub token at https://github.com/settings/tokens with `public_repo` scope.
#    Set the `GITHUB_TOKEN` environment variable to the token.
# 3. Run this script with `uv run`, `pipx run`, `pip run` or similar. Or run with Python,
#    but you will need to install httpx into your environment.
#
# This will output to stdout the PRs that are not excluded from the changelog.
#
# Future versions could modify the changelog file in place, but this is the limit of my
# interest for now.

import asyncio
import os
import re
import sys
from pathlib import Path

import httpx

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO_OWNER = "bids-standard"
REPO_NAME = "bids-specification"

if not GITHUB_TOKEN:
    raise ValueError("Please set the GITHUB_TOKEN environment variable")

auto_changelog = Path("auto-changelog.txt")

if not auto_changelog.exists():
    raise FileNotFoundError("auto-changelog.txt not found")

pr_numbers = reversed(
    [line.split("/")[-1] for line in auto_changelog.read_text().splitlines()]
)

headers = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
    "Accept": "application/vnd.github.v3+json",
}


async def get_pr_details(client, pr_number):
    url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/pulls/{pr_number}"

    response = await client.get(url)

    if response.status_code == 200:
        pr_data = response.json()
        labels = [label["name"] for label in pr_data.get("labels", [])]

        if "exclude-from-changelog" not in labels:
            return (
                pr_data.get("title"),
                pr_data.get("html_url"),
                pr_data["user"]["login"],
                pr_data["user"]["html_url"],
            )
    else:
        print(
            f"Failed to fetch PR #{pr_number}: {response.status_code}", file=sys.stderr
        )
    return (None, None, None, None)


async def main():
    cat = re.compile(r"^\[[^\]]+\]")
    async with httpx.AsyncClient(headers=headers) as client:
        pr_summaries = {}
        for pr_number in pr_numbers:
            title, pr_url, username, user_url = await get_pr_details(client, pr_number)
            if title:
                category = cat.match(title).group()
                pr_summaries.setdefault(category, []).append(
                    f"- {title} [{pr_number}]({pr_url}) ([{username}]({user_url}))"
                )

    for category in sorted(pr_summaries):
        for pr_summary in pr_summaries[category]:
            print(pr_summary)


if __name__ == "__main__":
    asyncio.run(main())
