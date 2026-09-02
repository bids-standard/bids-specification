#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pytest>=8",
#     "gql[aiohttp]",
# ]
# ///

# Tests for tools/announce_release.py.
#
# Run with:
#   tools/tests/test_announce_release.py              # via uv-run shebang
#   uv run --with pytest pytest tools/tests/test_announce_release.py
#
# Covers the pure-logic units:
#   - TAG_RE tag filter
#   - comment-body / release-link formatting
#   - prs_in_range commit-subject parsing
#   - release_tags filter
#   - CLI argparse validation
#
# The GraphQL/REST functions (get_pr_info, has_comment, post_comment) are
# exercised end-to-end via the dry-run on the real repo's git history; they
# are not unit-tested here to avoid baking the GitHub GraphQL schema into the
# test fixtures.
import importlib.util
import subprocess as sp
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SCRIPT = HERE.parent / "announce_release.py"
_spec = importlib.util.spec_from_file_location("announce_release", SCRIPT)
ann = importlib.util.module_from_spec(_spec)
sys.modules["announce_release"] = ann
_spec.loader.exec_module(ann)


# ---------- TAG_RE -----------------------------------------------------------

@pytest.mark.parametrize("tag", ["v1.0.0", "v10.20.30", "v1.11.1", "v0.0.1"])
def test_tag_regex_accepts(tag):
    assert ann.TAG_RE.match(tag), tag


@pytest.mark.parametrize(
    "tag",
    [
        "1.0.0",            # missing v
        "v1.0",             # missing patch
        "schema-1.2.3",     # schema tag
        "v1.0.0-dev",       # pre-release suffix
        "v1.0.0.post1",     # post-release suffix
        "v.1.1.2",          # bogus historical tag in this repo
    ],
)
def test_tag_regex_rejects(tag):
    assert not ann.TAG_RE.match(tag), tag


# ---------- formatting ------------------------------------------------------

def test_release_link_format():
    link = ann.release_link("v1.11.1")
    assert "[`v1.11.1`]" in link
    assert "https://github.com/bids-standard/bids-specification/releases/tag/v1.11.1" in link


def test_pr_and_issue_comment_bodies_differ_and_contain_tag():
    pr = ann.pr_comment_body("v1.0.0")
    iss = ann.issue_comment_body("v1.0.0")
    assert pr != iss
    assert "v1.0.0" in pr and "v1.0.0" in iss
    assert pr.startswith("PR released in ")
    assert iss.startswith("Issue fixed in ")


# ---------- prs_in_range ----------------------------------------------------

def test_prs_in_range_squash_and_merge(monkeypatch):
    """Parses both squash-merge `... (#NNN)` and `Merge pull request #NNN` subjects.

    Skips REL: subject (no PR ref) and dedupes repeated PR numbers (insertion-order).
    """
    fake_log = "\n".join(
        [
            "REL: Version 1.11.1",                                       # no PR ref, skip
            "[FIX] Add emg to timeseries rule (#2346)",                   # squash
            "fix: Allow mkdocs to render links in glossary (#2345)",      # squash
            "Merge pull request #2189 from bids-standard/rel/1.10.1",     # merge
            "chore: commit with no PR ref",                               # skip
            "another (#2346)",                                            # duplicate
            "tail #1234 in middle, not at end",                           # skip (not (#))
        ]
    )
    monkeypatch.setattr(ann, "git", lambda *a: fake_log)
    assert ann.prs_in_range("v1.10.0", "v1.11.0") == [2346, 2345, 2189]


def test_prs_in_range_handles_no_prev_tag(monkeypatch):
    monkeypatch.setattr(ann, "git", lambda *a: "Initial commit\nfeat: x (#1)\n")
    assert ann.prs_in_range(None, "v1.0.0") == [1]


def test_prs_in_range_empty(monkeypatch):
    monkeypatch.setattr(ann, "git", lambda *a: "")
    assert ann.prs_in_range("v1.0.0", "v1.0.1") == []


# ---------- release_tags ---------------------------------------------------

def test_release_tags_filters_and_preserves_order(monkeypatch):
    raw = "\n".join(
        [
            "schema-1.2.3",
            "v.1.1.2",        # malformed
            "v1.1.2",
            "v1.10.0",
            "v1.10.1",
            "v1.11.0",
            "v1.11.1-dev",    # pre-release
            "v1.11.1",
        ]
    )
    monkeypatch.setattr(ann, "git", lambda *a: raw)
    assert ann.release_tags() == [
        "v1.1.2", "v1.10.0", "v1.10.1", "v1.11.0", "v1.11.1"
    ]


# ---------- CLI argparse validation ----------------------------------------

def _run_script(*argv):
    """Run the script as a subprocess, returning (returncode, stderr)."""
    proc = sp.run(
        [sys.executable, str(SCRIPT), *argv],
        capture_output=True,
        text=True,
    )
    return proc.returncode, proc.stderr


def test_cli_rejects_tag_with_retroactive():
    rc, err = _run_script("v1.11.1", "--retroactive")
    assert rc != 0
    assert "--retroactive" in err


def test_cli_rejects_since_without_retroactive():
    rc, err = _run_script("--since", "v1.10.0")
    assert rc != 0
    assert "--since" in err


def test_cli_missing_token(monkeypatch):
    """Without GITHUB_TOKEN, the script exits 1 with a clear message."""
    import os
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
    proc = sp.run(
        [sys.executable, str(SCRIPT), "v1.11.1"],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(HERE.parent.parent),  # repo root
    )
    assert proc.returncode == 1
    assert "GITHUB_TOKEN" in proc.stderr


def test_cli_help_without_token():
    """`--help` must work even without GITHUB_TOKEN (argparse short-circuits)."""
    import os
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
    proc = sp.run(
        [sys.executable, str(SCRIPT), "--help"],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(HERE.parent.parent),
    )
    assert proc.returncode == 0
    assert "usage:" in proc.stdout
    assert "--retroactive" in proc.stdout


def test_cli_unknown_tag_message_before_token():
    """Invalid tag is reported before the token check (so e.g. a typo doesn't
    surface as a confusing 'GITHUB_TOKEN not set'). Important for the
    `uv run script -- --help` pattern, which makes argparse see `--help`
    as a positional tag."""
    import os
    env = {k: v for k, v in os.environ.items() if k != "GITHUB_TOKEN"}
    proc = sp.run(
        [sys.executable, str(SCRIPT), "v9.99.99"],
        capture_output=True,
        text=True,
        env=env,
        cwd=str(HERE.parent.parent),
    )
    assert proc.returncode == 1
    assert "not a known release tag" in proc.stderr
    assert "GITHUB_TOKEN" not in proc.stderr


# ---------- select_tags ----------------------------------------------------

def _ns(**kw):
    """Build an argparse.Namespace with sensible defaults."""
    import argparse
    return argparse.Namespace(
        tag=kw.get("tag"),
        retroactive=kw.get("retroactive", False),
        since=kw.get("since"),
        post=kw.get("post", False),
    )


def test_select_tags_default_picks_latest():
    tags = ["v1.0.0", "v1.1.0", "v1.2.0"]
    assert ann.select_tags(_ns(), tags) == ["v1.2.0"]


def test_select_tags_explicit_tag():
    tags = ["v1.0.0", "v1.1.0", "v1.2.0"]
    assert ann.select_tags(_ns(tag="v1.1.0"), tags) == ["v1.1.0"]


def test_select_tags_explicit_unknown(capsys):
    assert ann.select_tags(_ns(tag="v9.9.9"), ["v1.0.0"]) is None
    assert "not a known release tag" in capsys.readouterr().err


def test_select_tags_retroactive_full():
    tags = ["v1.0.0", "v1.1.0", "v1.2.0"]
    assert ann.select_tags(_ns(retroactive=True), tags) == tags


def test_select_tags_retroactive_since():
    tags = ["v1.0.0", "v1.1.0", "v1.2.0"]
    assert ann.select_tags(_ns(retroactive=True, since="v1.1.0"), tags) == ["v1.1.0", "v1.2.0"]


def test_select_tags_retroactive_since_unknown(capsys):
    assert ann.select_tags(_ns(retroactive=True, since="v9.9.9"), ["v1.0.0"]) is None
    assert "--since" in capsys.readouterr().err


def test_select_tags_no_tags(capsys):
    assert ann.select_tags(_ns(), []) is None
    assert "No vX.Y.Z release tags" in capsys.readouterr().err


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
