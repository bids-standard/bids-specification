import os
from pathlib import Path

import bidsschematools as bst
import bidsschematools.utils

lgr = bst.utils.get_logger()


def migrate_version(dataset_path: Path):
    """TODO: modify BIDSVersion in dataset_description.json

    Should do as a string manipulation not json to minimize
    the diff"""
    pass


def migrate_participants(dataset_path: Path):
    extensions = [".tsv", ".json"]

    for ext in extensions:
        old_file = Path(dataset_path) / f"participants{ext}"
        new_file = Path(dataset_path) / f"subjects{ext}"
        if old_file.exists():
            os.rename(old_file, new_file)
            lgr.info(f"   - renamed {old_file} to {new_file}")
            if ext == ".tsv":
                migrated = new_file.read_text().replace("participant_id", "subject_id", 1)
                new_file.write_text(migrated)
                lgr.info(f"   - migrated content in {new_file}")


def migrate_dataset(dataset_path):
    lgr.info(f"Migrating dataset at {dataset_path}")

    # TODO: possibly add a check for BIDS version in dataset_description.json
    # and skip if already 2.0, although ideally transformations
    # should also be indepotent
    for migration in [migrate_participants, migrate_version]:
        lgr.info(f" - applying migration {migration.__name__}")
        migration(dataset_path)
