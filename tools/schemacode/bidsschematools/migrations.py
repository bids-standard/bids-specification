import json
import os
import re
from pathlib import Path

import bidsschematools as bst
import bidsschematools.utils

lgr = bst.utils.get_logger()

TARGET_VERSION = "2.0.0"


def get_bids_version(dataset_path: Path) -> str:
    dataset_description = dataset_path / "dataset_description.json"
    if not dataset_description.exists():
        raise ValueError(f"dataset_description.json not found in {dataset_path}")
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
            os.rename(old_file, new_file)
            lgr.info(f"   - renamed {old_file} to {new_file}")
            if ext == ".tsv":
                # Do manual .decode() and .encode() to avoid changing line endings
                migrated = (
                    new_file.read_bytes().decode().replace("participant_id", "subject_id", 1)
                )
                new_file.write_bytes(migrated.encode())
                lgr.info(f"   - migrated content in {new_file}")


def migrate_dataset(dataset_path):
    lgr.info(f"Migrating dataset at {dataset_path}")
    dataset_path = Path(dataset_path)
    if get_bids_version(dataset_path) == TARGET_VERSION:
        lgr.info(f"Dataset already at version {TARGET_VERSION}")
        return
    # TODO: possibly add a check for BIDS version in dataset_description.json
    # and skip if already 2.0, although ideally transformations
    # should also be indepotent
    for migration in [
        migrate_participants,
        migrate_version,
    ]:
        lgr.info(f" - applying migration {migration.__name__}")
        migration(dataset_path)
