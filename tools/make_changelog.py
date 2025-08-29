#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gql[aiohttp]",
# ]
# ///

# How to use this script:
# 1. Generate a GitHub token at https://github.com/settings/tokens with `public_repo` scope.
#    Set the `GITHUB_TOKEN` environment variable to the token.
# 2. Run this script with `uv run`, `pipx run`, `pip run` or similar. Or run with Python,
#    but you will need to install `gql[aiohttp]`.
#
# This will update src/CHANGES.md with the PRs that are not excluded from the changelog.
import asyncio
import os
import re
import subprocess as sp
from dataclasses import dataclass
from datetime import date, datetime, timedelta, UTC
from pathlib import Path

from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

SEARCH_MERGED_PRS_QUERY = gql("""\
query SearchMergedPullRequests($query: String!, $after: String) {
  search(query: $query, type: ISSUE, first: 100, after: $after) {
    pageInfo {
      hasNextPage
      endCursor
    }
    nodes {
      ... on PullRequest {
        title
        mergedAt
        number
        url
        author {
          login
          url
        }
      }
    }
  }
}
""")


@dataclass
class PR:
    title: str
    number: int
    url: str
    merged_date: datetime
    author: str
    author_url: str

    @property
    def category(self) -> str:
        if match := re.match(r"^\[[^\]]+\]", self.title):
            return match.group()
        return ""

    def __str__(self):
        return f"-   \\{self.title} [#{self.number}]({self.url}) ([{self.author}]({self.author_url}))"


def git(*args: str) -> str:
    return (
        sp.run(["git", *args], capture_output=True, check=True).stdout.decode().strip()
    )


def get_repo() -> Path:
    return Path(git("rev-parse", "--show-toplevel"))


def previous_tag() -> str:
    return git("describe", "--match=v*", "--abbrev=0")


def tag_date(tag: str) -> date:
    short_date = git("log", "-n1", tag, "--pretty=%as")
    return date.fromisoformat(short_date)


def load_changes(repo: Path, tag: str) -> str:
    with open(repo / "src/CHANGES.md") as changelog:
        for line in changelog:
            if line.startswith(f"## [{tag}]"):
                break
        return line + changelog.read()


async def get_merged_prs(
    client: Client, repository: str, merged_after: date
) -> list[PR]:
    prs = []

    cursor = None
    has_next_page = True

    search_query = f"repo:{repository} is:pr is:merged base:master merged:>={merged_after:%Y-%m-%d} -label:exclude-from-changelog"

    now = datetime.now(UTC)

    while has_next_page:
        variable_values = {"query": search_query, "after": cursor}
        result = await client.execute_async(
            SEARCH_MERGED_PRS_QUERY, variable_values=variable_values
        )

        search_results = result["search"]
        page_info = search_results["pageInfo"]
        cursor = page_info["endCursor"]
        has_next_page = page_info["hasNextPage"]

        for pr in search_results["nodes"]:
            if not pr:
                continue

            merged_date = datetime.fromisoformat(pr["mergedAt"].replace("Z", "+00:00"))

            prs.append(
                PR(
                    title=pr["title"],
                    number=pr["number"],
                    url=pr["url"],
                    merged_date=merged_date,
                    author=pr["author"]["login"],
                    author_url=pr["author"]["url"],
                )
            )

    # Sort by category, and then descending by merge date
    return sorted(prs, key=lambda x: (x.category, now - x.merged_date))


async def main() -> None:
    github_token = os.getenv("GITHUB_TOKEN")
    transport = AIOHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {github_token}"},
    )
    client = Client(transport=transport, fetch_schema_from_transport=True)

    tag = previous_tag()
    start_date = tag_date(tag) + timedelta(days=1)
    repo = get_repo()
    changes = load_changes(repo, tag)

    prs = await get_merged_prs(
        client, repository="bids-standard/bids-specification", merged_after=start_date
    )

    with open(repo / "src/CHANGES.md", "w") as changelog:
        changelog.write("# Changelog\n\n## Upcoming\n\n")
        changelog.write("\n".join([*map(str, prs), "", changes]))


if __name__ == "__main__":
    asyncio.run(main())
