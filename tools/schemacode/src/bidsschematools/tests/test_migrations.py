"""Tests for specific BIDS dataset migrations."""

import json

import pytest

from bidsschematools.migrations import (
    check_inheritance_overloading,
    check_tsv_entity_prefix,
    migrate_generatedby,
)


class TestMigrateGeneratedBy:
    """Tests for GeneratedBy migration."""

    @pytest.fixture
    def dataset_with_old_provenance(self, tmp_path):
        """Create a dataset with pre-standard provenance fields."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        # Create dataset_description.json with old-style provenance
        desc_data = {
            "Name": "Test Dataset",
            "BIDSVersion": "1.9.0",
            "Pipeline": {
                "Name": "fmriprep",
                "Version": "1.4.1",
            },
        }

        desc_file = dataset_path / "dataset_description.json"
        with open(desc_file, "w") as f:
            json.dump(desc_data, f, indent=2)

        return dataset_path

    @pytest.fixture
    def dataset_with_new_provenance(self, tmp_path):
        """Create a dataset with standard GeneratedBy field."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        desc_data = {
            "Name": "Test Dataset",
            "BIDSVersion": "1.10.0",
            "GeneratedBy": [
                {
                    "Name": "fmriprep",
                    "Version": "1.4.1",
                }
            ],
        }

        desc_file = dataset_path / "dataset_description.json"
        with open(desc_file, "w") as f:
            json.dump(desc_data, f, indent=2)

        return dataset_path

    def test_migrate_old_pipeline_field(self, dataset_with_old_provenance):
        """Test migrating old Pipeline field to GeneratedBy."""
        result = migrate_generatedby(dataset_with_old_provenance)

        assert result["success"] is True
        assert len(result["modified_files"]) == 1
        assert "dataset_description.json" in result["modified_files"][0]

        # Check that file was actually modified
        desc_file = dataset_with_old_provenance / "dataset_description.json"
        with open(desc_file) as f:
            data = json.load(f)

        assert "GeneratedBy" in data
        assert "Pipeline" not in data
        assert data["GeneratedBy"][0]["Name"] == "fmriprep"
        assert data["GeneratedBy"][0]["Version"] == "1.4.1"

    def test_skip_if_generatedby_exists(self, dataset_with_new_provenance):
        """Test that migration skips if GeneratedBy already exists."""
        result = migrate_generatedby(dataset_with_new_provenance)

        assert result["success"] is True
        assert len(result["modified_files"]) == 0
        assert "already exists" in result["message"] or "No pre-standard" in result["message"]

    def test_dry_run(self, dataset_with_old_provenance):
        """Test dry run mode doesn't modify files."""
        result = migrate_generatedby(dataset_with_old_provenance, dry_run=True)

        assert result["success"] is True
        assert len(result["modified_files"]) > 0
        assert "dry run" in result["modified_files"][0].lower()

        # Check that file was NOT modified
        desc_file = dataset_with_old_provenance / "dataset_description.json"
        with open(desc_file) as f:
            data = json.load(f)

        assert "Pipeline" in data
        assert "GeneratedBy" not in data

    def test_migrate_multiple_fields(self, tmp_path):
        """Test migrating multiple pre-standard fields."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        desc_data = {
            "Name": "Test Dataset",
            "BIDSVersion": "1.9.0",
            "Pipeline": "fmriprep",
            "Software": "SPM12",
        }

        desc_file = dataset_path / "dataset_description.json"
        with open(desc_file, "w") as f:
            json.dump(desc_data, f, indent=2)

        result = migrate_generatedby(dataset_path)

        assert result["success"] is True

        with open(desc_file) as f:
            data = json.load(f)

        assert "GeneratedBy" in data
        assert len(data["GeneratedBy"]) == 2
        assert "Pipeline" not in data
        assert "Software" not in data

    def test_no_dataset_description(self, tmp_path):
        """Test with no dataset_description.json file."""
        result = migrate_generatedby(tmp_path)

        assert result["success"] is True
        assert len(result["modified_files"]) == 0
        assert "No dataset_description.json" in result["message"]


class TestCheckInheritanceOverloading:
    """Tests for inheritance overloading check."""

    @pytest.fixture
    def dataset_with_overloading(self, tmp_path):
        """Create a dataset with inheritance overloading."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        # Create dataset-level metadata
        (dataset_path / "task-rest_bold.json").write_text(json.dumps({"RepetitionTime": 2.0}))

        # Create subject-level metadata with different value
        sub_dir = dataset_path / "sub-01"
        sub_dir.mkdir()
        (sub_dir / "task-rest_bold.json").write_text(json.dumps({"RepetitionTime": 1.5}))

        return dataset_path

    @pytest.fixture
    def dataset_without_overloading(self, tmp_path):
        """Create a dataset without inheritance overloading."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        # Create dataset-level metadata
        (dataset_path / "task-rest_bold.json").write_text(json.dumps({"TaskName": "rest"}))

        # Create subject-level metadata with same value
        sub_dir = dataset_path / "sub-01"
        sub_dir.mkdir()
        (sub_dir / "task-rest_bold.json").write_text(json.dumps({"TaskName": "rest"}))

        return dataset_path

    def test_detect_overloading(self, dataset_with_overloading):
        """Test detection of inheritance overloading."""
        result = check_inheritance_overloading(dataset_with_overloading)

        assert result["success"] is True
        assert len(result["warnings"]) > 0
        assert any("RepetitionTime" in w for w in result["warnings"])
        assert any("deprecated" in w for w in result["warnings"])

    def test_no_overloading(self, dataset_without_overloading):
        """Test dataset without overloading issues."""
        result = check_inheritance_overloading(dataset_without_overloading)

        assert result["success"] is True
        assert len(result.get("warnings", [])) == 0
        assert "No inheritance overloading" in result["message"]

    def test_empty_dataset(self, tmp_path):
        """Test with empty dataset."""
        result = check_inheritance_overloading(tmp_path)

        assert result["success"] is True
        assert "No JSON sidecar files" in result["message"]


class TestCheckTsvEntityPrefix:
    """Tests for TSV entity prefix check."""

    @pytest.fixture
    def dataset_with_participants(self, tmp_path):
        """Create a dataset with participants.tsv."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        # Create participants.tsv with correct prefix
        participants_file = dataset_path / "participants.tsv"
        participants_file.write_text("participant_id\tage\tsex\n01\t25\tF\n")

        return dataset_path

    @pytest.fixture
    def dataset_with_samples(self, tmp_path):
        """Create a dataset with samples.tsv without proper prefix."""
        dataset_path = tmp_path / "dataset"
        dataset_path.mkdir()

        # Create samples.tsv without proper prefix
        samples_file = dataset_path / "samples.tsv"
        samples_file.write_text("id\ttype\ttissue\n01\tblood\tWB\n")

        return dataset_path

    def test_correct_prefix(self, dataset_with_participants):
        """Test dataset with correct entity prefix."""
        result = check_tsv_entity_prefix(dataset_with_participants)

        assert result["success"] is True
        assert len(result.get("suggestions", [])) == 0
        assert "No entity prefix issues" in result["message"]

    def test_missing_prefix(self, dataset_with_samples):
        """Test dataset with missing entity prefix."""
        result = check_tsv_entity_prefix(dataset_with_samples)

        assert result["success"] is True
        assert len(result.get("suggestions", [])) > 0
        assert any("sample_" in s for s in result["suggestions"])

    def test_empty_dataset(self, tmp_path):
        """Test with empty dataset."""
        result = check_tsv_entity_prefix(tmp_path)

        assert result["success"] is True
        assert len(result.get("suggestions", [])) == 0
