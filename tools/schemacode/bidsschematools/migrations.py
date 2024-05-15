import json
import os
import re
import subprocess
from functools import lru_cache
from itertools import chain
from pathlib import Path
from typing import Optional

import bidsschematools as bst
import bidsschematools.utils

lgr = bst.utils.get_logger()

TARGET_VERSION = "2.0.0"


class NotBIDSDatasetError(Exception):
    pass


def get_bids_version(dataset_path: Path) -> str:
    dataset_description = dataset_path / "dataset_description.json"
    if not dataset_description.exists():
        raise NotBIDSDatasetError(f"dataset_description.json not found in {dataset_path}")
    return json.loads(dataset_description.read_text())["BIDSVersion"]


def migrate_version(dataset_path: Path):
    """TODO: modify BIDSVersion in dataset_description.json

    Should do as a string manipulation not json to minimize
    the diff"""
    dataset_description = dataset_path / "dataset_description.json"
    # Read/write as bytes so we do not change Windows line endings
    content = dataset_description.read_bytes().decode()
    old_version = json.loads(content)["BIDSVersion"]
    migrated = re.sub(rf'("BIDSVersion":\s*)"{old_version}', r'\1"' + TARGET_VERSION, content)
    assert json.loads(migrated)["BIDSVersion"] == TARGET_VERSION
    dataset_description.write_bytes(migrated.encode())


def migrate_participants(dataset_path: Path):
    extensions = [".tsv", ".json"]

    for ext in extensions:
        old_file = dataset_path / f"participants{ext}"
        new_file = dataset_path / f"subjects{ext}"
        if old_file.exists():
            rename_path(old_file, new_file)
            lgr.info(f"   - renamed {old_file} to {new_file}")
            if ext == ".tsv":
                # Do manual .decode() and .encode() to avoid changing line endings
                migrated = (
                    new_file.read_bytes().decode().replace("participant_id", "subject_id", 1)
                )
                new_file.write_bytes(migrated.encode())
                lgr.info(f"   - migrated content in {new_file}")


def migrate_tsv_columns(dataset_path: Path):
    """
    Rename some columns in .tsv (and corresponding sidecar .json)
    """
    # TODO: ideally here we would not provide file_glob
    # but rather take schema and deduce which files could have
    # the column... alternatively - consider all .tsv files and
    # their .json files (note -- could be above and multiple given
    # inheritance principle)
    for col_from, col_to, file_glob in (
        # https://github.com/bids-standard/bids-2-devel/issues/78
        ("hplc_recovery_fractions", "hplc_recovery_fraction", "*_blood.*"),
        # https://github.com/bids-standard/bids-2-devel/issues/15
        ("units", "unit", "_channels.*"),  # dependency on migrate_participants
        # ??? Any other columns to rename for some reason?
    ):
        raise NotImplementedError()


def migrate_dataset(dataset_path):
    lgr.info(f"Migrating dataset at {dataset_path}")
    dataset_path = Path(dataset_path)
    try:
        if get_bids_version(dataset_path) == TARGET_VERSION:
            lgr.info(f"Dataset already at version {TARGET_VERSION}")
            return
    except NotBIDSDatasetError:
        lgr.warning("%s not a BIDS dataset, skipping", dataset_path)
        return
    # TODO: possibly add a check for BIDS version in dataset_description.json
    # and skip if already 2.0, although ideally transformations
    # should also be indepotent
    for migration in [
        migrate_participants,
        migrate_version,
        migrate_tsv_columns,  # depends on migrate_participants
    ]:
        lgr.info(f" - applying migration {migration.__name__}")
        migration(dataset_path)


@lru_cache
def path_has_git(path: Path) -> bool:
    return (path / ".git").exists()


def git_topdir(path: Path) -> Optional[Path]:
    """Return top-level directory of a git repository containing path,
    or None if not under git."""
    path = path.absolute()
    for p in chain([path] if path.is_dir() else [], path.parents):
        if path_has_git(p):
            return p
    return None


def rename_path(old_path: Path, new_path: Path):
    """git aware rename. If under git, use git mv, otherwise just os.rename."""
    # if under git, use git mv but ensure that on border
    # crossing (should just use DataLad and `mv` and it would do the right thing!)
    if (old_git_top := git_topdir(old_path)) != (new_git_top := git_topdir(new_path)):
        raise NotImplementedError(
            f"Did not implement moving across git repo boundaries {old_git_top} -> {new_git_top}"
        )
    if old_git_top:
        subprocess.run(["git", "mv", str(old_path), str(new_path)], check=True, cwd=old_git_top)
    else:
        os.rename(old_path, new_path)
