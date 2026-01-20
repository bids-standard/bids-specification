"""Integration tests for the migrate CLI commands."""

import json
import subprocess


class TestMigrateCLI:
    """Test the bst migrate CLI commands."""

    def test_migrate_list_command(self):
        """Test that 'bst migrate list' works."""
        result = subprocess.run(
            ["bst", "migrate", "list"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "standardize_generatedby" in result.stdout
        assert "fix_inheritance_overloading" in result.stdout
        assert "fix_tsv_entity_prefix" in result.stdout
        assert "version" in result.stdout

    def test_migrate_run_command(self, tmp_path):
        """Test that 'bst migrate run' works on a real dataset."""
        # Create a test dataset
        dataset_path = tmp_path / "test_dataset"
        dataset_path.mkdir()

        desc_file = dataset_path / "dataset_description.json"
        desc_data = {"Name": "Test Dataset", "BIDSVersion": "1.9.0", "Pipeline": "my_pipeline"}

        with open(desc_file, "w") as f:
            json.dump(desc_data, f)

        # Run the migration
        result = subprocess.run(
            ["bst", "migrate", "run", "standardize_generatedby", str(dataset_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "Modified files" in result.stdout
        assert "dataset_description.json" in result.stdout

        # Verify the file was actually migrated
        with open(desc_file) as f:
            migrated_data = json.load(f)

        assert "GeneratedBy" in migrated_data
        assert "Pipeline" not in migrated_data

    def test_migrate_run_dry_run(self, tmp_path):
        """Test that 'bst migrate run --dry-run' doesn't modify files."""
        # Create a test dataset
        dataset_path = tmp_path / "test_dataset"
        dataset_path.mkdir()

        desc_file = dataset_path / "dataset_description.json"
        desc_data = {"Name": "Test Dataset", "BIDSVersion": "1.9.0", "Pipeline": "my_pipeline"}

        with open(desc_file, "w") as f:
            json.dump(desc_data, f)

        # Run the migration in dry-run mode
        result = subprocess.run(
            ["bst", "migrate", "run", "standardize_generatedby", str(dataset_path), "--dry-run"],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 0
        assert "dry run" in result.stdout.lower()

        # Verify the file was NOT modified
        with open(desc_file) as f:
            data = json.load(f)

        assert "Pipeline" in data
        assert "GeneratedBy" not in data

    def test_migrate_run_invalid_dataset(self, tmp_path):
        """Test that running migration on invalid dataset fails gracefully."""
        # Create empty directory (no dataset_description.json)
        dataset_path = tmp_path / "invalid_dataset"
        dataset_path.mkdir()

        result = subprocess.run(
            ["bst", "migrate", "run", "standardize_generatedby", str(dataset_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "dataset_description.json" in result.stderr.lower()

    def test_migrate_run_nonexistent_migration(self, tmp_path):
        """Test that running nonexistent migration fails gracefully."""
        # Create a valid dataset
        dataset_path = tmp_path / "test_dataset"
        dataset_path.mkdir()

        desc_file = dataset_path / "dataset_description.json"
        with open(desc_file, "w") as f:
            json.dump({"Name": "Test", "BIDSVersion": "1.0.0"}, f)

        result = subprocess.run(
            ["bst", "migrate", "run", "nonexistent_migration", str(dataset_path)],
            capture_output=True,
            text=True,
        )

        assert result.returncode == 1
        assert "not found" in result.stderr.lower()
