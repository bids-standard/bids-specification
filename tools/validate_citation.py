# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "pyyaml",
#     "flask",
#     "idutils",
#     "marshmallow",
#     "marshmallow_utils",
#     "flask_resources",
#     "invenio_records",
#     "invenio_db",
#     "zenodo-legacy",
#     "zenodo-rdm",
# ]
#
# [tool.uv.sources]
# zenodo-rdm = { git = "https://github.com/zenodo/zenodo-rdm.git", subdirectory = "site", rev = "v21.0.2" }
# zenodo-legacy = { git = "https://github.com/zenodo/zenodo-rdm.git", subdirectory = "legacy", rev = "v21.0.2" }
# ///

# This script checks whether Zenodo will accept a CITATION.cff file
from pathlib import Path

import yaml
from zenodo_rdm.github.schemas import CitationMetadataSchema
from zenodo_rdm.legacy.deserializers.schemas import LegacySchema


def main() -> None:
    contents = Path("CITATION.cff").read_text()
    data = yaml.safe_load(contents)
    legacy_data = {"metadata": CitationMetadataSchema().load(data)}
    rdm_data = LegacySchema().load(legacy_data)
    print(rdm_data["metadata"])


if __name__ == "__main__":
    main()
