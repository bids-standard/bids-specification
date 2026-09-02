#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "gql[aiohttp]",
# ]
# ///

# How to use this script:
# 1. Provide a GitHub token via the GITHUB_TOKEN environment variable. The
#    quickest way if you have the `gh` CLI authenticated is:
#        GITHUB_TOKEN=$(gh auth token) tools/announce_release.py ...
#    Otherwise generate a PAT at https://github.com/settings/tokens with
#    `public_repo` scope (write access is needed for --post).
# 2. Run from a checkout of bids-standard/bids-specification — the script
#    uses `git log` between tags to discover PRs included in each release.
#
# Examples (all default to dry-run; add --post to actually comment):
#   GITHUB_TOKEN=$(gh auth token) tools/announce_release.py v1.11.0
#   GITHUB_TOKEN=$(gh auth token) tools/announce_release.py            # latest tag
#   GITHUB_TOKEN=$(gh auth token) tools/announce_release.py --retroactive --since v1.10.0
#   GITHUB_TOKEN=$(gh auth token) tools/announce_release.py --post v1.11.1
#
# Idempotent: skips PRs/issues that already have an identical comment.
#
# Modeled after datalad/release-action's `make_release_comments`:
#   https://github.com/datalad/release-action/blob/master/datalad_release_action/client.py
import argparse
import asyncio
import os
import re
import subprocess as sp
import sys
from dataclasses import dataclass

import aiohttp
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

REPO = "bids-standard/bids-specification"
TAG_RE = re.compile(r"^v\d+\.\d+\.\d+$")

PR_INFO_QUERY = gql("""\
query($owner: String!, $name: String!, $number: Int!, $issue_cursor: String) {
  repository(owner: $owner, name: $name) {
    pullRequest(number: $number) {
      title
      closingIssuesReferences(first: 50, after: $issue_cursor) {
        nodes { number repository { nameWithOwner } }
        pageInfo { endCursor hasNextPage }
      }
    }
  }
}
""")

COMMENTS_QUERY = gql("""\
query($owner: String!, $name: String!, $number: Int!, $after: String) {
  repository(owner: $owner, name: $name) {
    issueOrPullRequest(number: $number) {
      ... on Issue {
        comments(first: 100, after: $after) {
          nodes { body }
          pageInfo { endCursor hasNextPage }
        }
      }
      ... on PullRequest {
        comments(first: 100, after: $after) {
          nodes { body }
          pageInfo { endCursor hasNextPage }
        }
      }
    }
  }
}
""")


@dataclass
class PRInfo:
    number: int
    title: str
    closing_issues: list[int]


def git(*args: str) -> str:
    return sp.run(
        ["git", *args], capture_output=True, check=True, text=True
    ).stdout.strip()


def release_tags() -> list[str]:
    """Version tags (vX.Y.Z) ordered oldest-first."""
    out = git("tag", "--sort=version:refname")
    return [t for t in out.splitlines() if TAG_RE.match(t)]


def prs_in_range(prev_tag: str | None, tag: str) -> list[int]:
    """Find PR numbers in commits between prev_tag and tag (first-parent).

    Recognizes both squash-merge `... (#NNN)` and `Merge pull request #NNN ...`
    commit subject styles.
    """
    rev = f"{prev_tag}..{tag}" if prev_tag else tag
    out = git("log", rev, "--first-parent", "--pretty=%s")
    seen: dict[int, None] = {}  # dict preserves insertion order, dedupes
    for line in out.splitlines():
        if m := re.search(r"\(#(\d+)\)\s*$", line):
            seen[int(m.group(1))] = None
        elif m := re.match(r"Merge pull request #(\d+)", line):
            seen[int(m.group(1))] = None
    return list(seen)


def release_link(tag: str) -> str:
    return f"[`{tag}`](https://github.com/{REPO}/releases/tag/{tag})"


def pr_comment_body(tag: str) -> str:
    return f"PR released in {release_link(tag)}"


def issue_comment_body(tag: str) -> str:
    return f"Issue fixed in {release_link(tag)}"


async def get_pr_info(client: Client, number: int) -> PRInfo | None:
    owner, name = REPO.split("/")
    closing: list[int] = []
    title = ""
    cursor: str | None = None
    while True:
        result = await client.execute_async(
            PR_INFO_QUERY,
            variable_values={
                "owner": owner,
                "name": name,
                "number": number,
                "issue_cursor": cursor,
            },
        )
        pr = result["repository"]["pullRequest"]
        if pr is None:
            return None
        title = pr["title"]
        page = pr["closingIssuesReferences"]
        for n in page["nodes"]:
            if n["repository"]["nameWithOwner"] == REPO:
                closing.append(n["number"])
        if not page["pageInfo"]["hasNextPage"]:
            return PRInfo(number=number, title=title, closing_issues=closing)
        cursor = page["pageInfo"]["endCursor"]


async def has_comment(client: Client, number: int, body: str) -> bool:
    owner, name = REPO.split("/")
    target = body.strip()
    cursor: str | None = None
    while True:
        result = await client.execute_async(
            COMMENTS_QUERY,
            variable_values={
                "owner": owner,
                "name": name,
                "number": number,
                "after": cursor,
            },
        )
        node = result["repository"]["issueOrPullRequest"]
        if node is None:
            return False
        comments = node["comments"]
        for c in comments["nodes"]:
            if c["body"].strip() == target:
                return True
        if not comments["pageInfo"]["hasNextPage"]:
            return False
        cursor = comments["pageInfo"]["endCursor"]


async def post_comment(
    session: aiohttp.ClientSession, token: str, number: int, body: str
) -> None:
    url = f"https://api.github.com/repos/{REPO}/issues/{number}/comments"
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    async with session.post(url, json={"body": body}, headers=headers) as resp:
        if resp.status not in (200, 201):
            text = await resp.text()
            raise RuntimeError(f"POST {url}: HTTP {resp.status} - {text}")


async def annotate_release(
    client: Client,
    session: aiohttp.ClientSession,
    token: str,
    tag: str,
    prev_tag: str | None,
    *,
    post: bool,
) -> None:
    print(f"\n=== Release {tag} (prev: {prev_tag or 'initial'}) ===")
    pr_numbers = prs_in_range(prev_tag, tag)
    if not pr_numbers:
        print("  (no PRs found in commit range)")
        return
    print(f"  {len(pr_numbers)} PR(s) in this release")
    pr_body = pr_comment_body(tag)
    iss_body = issue_comment_body(tag)
    for pr_num in pr_numbers:
        pr_url = f"https://github.com/{REPO}/pull/{pr_num}"
        pr = await get_pr_info(client, pr_num)
        if pr is None:
            print(f"  - PR #{pr_num} {pr_url} — not found via API; skipping")
            continue
        marker = "POST" if post else "DRY"
        if await has_comment(client, pr.number, pr_body):
            status = "comment already exists, skip"
        else:
            status = f"[{marker}] comment on PR"
            if post:
                await post_comment(session, token, pr.number, pr_body)
        print(f"  - PR #{pr.number} {pr_url} — {status} — {pr.title!r}")
        for issue_num in pr.closing_issues:
            issue_url = f"https://github.com/{REPO}/issues/{issue_num}"
            if await has_comment(client, issue_num, iss_body):
                status = "comment already exists, skip"
            else:
                status = f"[{marker}] comment on issue"
                if post:
                    await post_comment(session, token, issue_num, iss_body)
            print(f"      issue #{issue_num} {issue_url} — {status}")


def select_tags(args: argparse.Namespace, tags: list[str]) -> list[str] | None:
    """Return the list of release tags to process, or None on a validation error
    (the error message is printed to stderr).
    """
    if not tags:
        print("No vX.Y.Z release tags found.", file=sys.stderr)
        return None
    if args.retroactive:
        start = 0
        if args.since:
            if args.since not in tags:
                print(
                    f"--since {args.since!r} is not a known release tag.",
                    file=sys.stderr,
                )
                return None
            start = tags.index(args.since)
        return tags[start:]
    if args.tag:
        if args.tag not in tags:
            print(f"{args.tag!r} is not a known release tag.", file=sys.stderr)
            return None
        return [args.tag]
    return [tags[-1]]


async def main_async(args: argparse.Namespace, selected: list[str], tags: list[str]) -> int:
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        print("GITHUB_TOKEN environment variable is not set.", file=sys.stderr)
        return 1
    transport = AIOHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"Bearer {token}"},
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)
    async with aiohttp.ClientSession() as session:
        for tag in selected:
            idx = tags.index(tag)
            prev = tags[idx - 1] if idx > 0 else None
            await annotate_release(
                client, session, token, tag, prev, post=args.post
            )
    return 0


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Post 'PR released in vX.Y.Z' / 'Issue fixed in vX.Y.Z' comments "
            "on the PRs included in a release and the issues those PRs close."
        )
    )
    parser.add_argument(
        "tag",
        nargs="?",
        help="Release tag, e.g. v1.11.1. Defaults to the most recent vX.Y.Z tag.",
    )
    parser.add_argument(
        "--retroactive",
        action="store_true",
        help="Process all historical releases (oldest first).",
    )
    parser.add_argument(
        "--since",
        metavar="TAG",
        help="With --retroactive: start at this tag (inclusive).",
    )
    parser.add_argument(
        "--post",
        action="store_true",
        help="Actually post comments. Default is dry-run.",
    )
    args = parser.parse_args()
    if args.tag and args.retroactive:
        parser.error("Cannot combine a single TAG argument with --retroactive.")
    if args.since and not args.retroactive:
        parser.error("--since only makes sense with --retroactive.")
    # Resolve and validate tag selection (uses git, no network needed) BEFORE
    # requiring GITHUB_TOKEN, so e.g. typos / `-- --help` invocation patterns
    # fail with a clear message instead of the token error.
    tags = release_tags()
    selected = select_tags(args, tags)
    if selected is None:
        sys.exit(1)
    sys.exit(asyncio.run(main_async(args, selected, tags)))


if __name__ == "__main__":
    main()
