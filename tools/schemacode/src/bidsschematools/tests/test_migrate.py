"""Tests for BIDS dataset migration functionality."""

import json

import pytest

from bidsschematools.migrate import Migration, MigrationRegistry, load_json, save_json


class TestMigration:
    """Tests for Migration class."""

    def test_migration_creation(self):
        """Test creating a migration."""

        def dummy_func(dataset_path):
            return {"success": True, "modified_files": [], "message": "Done"}

        mig = Migration(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
            func=dummy_func,
        )

        assert mig.name == "test_migration"
        assert mig.version == "1.0.0"
        assert mig.description == "Test migration"
        assert callable(mig.func)

    def test_migration_call(self, tmp_path):
        """Test calling a migration."""

        def dummy_func(dataset_path, **kwargs):
            return {
                "success": True,
                "modified_files": ["test.json"],
                "message": f"Processed {dataset_path}",
            }

        mig = Migration(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
            func=dummy_func,
        )

        result = mig(tmp_path)
        assert result["success"] is True
        assert result["modified_files"] == ["test.json"]
        assert str(tmp_path) in result["message"]


class TestMigrationRegistry:
    """Tests for MigrationRegistry class."""

    def test_registry_creation(self):
        """Test creating a registry."""
        registry = MigrationRegistry()
        assert registry.list_migrations() == []

    def test_register_migration(self):
        """Test registering a migration."""
        registry = MigrationRegistry()

        @registry.register(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
        )
        def test_func(dataset_path):
            return {"success": True, "modified_files": [], "message": "Done"}

        migrations = registry.list_migrations()
        assert len(migrations) == 1
        assert migrations[0]["name"] == "test_migration"
        assert migrations[0]["version"] == "1.0.0"

    def test_get_migration(self):
        """Test getting a migration by name."""
        registry = MigrationRegistry()

        @registry.register(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
        )
        def test_func(dataset_path):
            return {"success": True, "modified_files": [], "message": "Done"}

        mig = registry.get("test_migration")
        assert mig is not None
        assert mig.name == "test_migration"

        mig = registry.get("nonexistent")
        assert mig is None

    def test_run_migration(self, tmp_path):
        """Test running a migration."""
        registry = MigrationRegistry()

        @registry.register(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
        )
        def test_func(dataset_path, **kwargs):
            return {
                "success": True,
                "modified_files": [],
                "message": "Migration completed",
            }

        result = registry.run("test_migration", tmp_path)
        assert result["success"] is True
        assert result["message"] == "Migration completed"

    def test_run_nonexistent_migration(self, tmp_path):
        """Test running a nonexistent migration raises error."""
        registry = MigrationRegistry()

        with pytest.raises(ValueError, match="Migration 'nonexistent' not found"):
            registry.run("nonexistent", tmp_path)

    def test_dry_run(self, tmp_path):
        """Test dry run mode."""
        registry = MigrationRegistry()

        @registry.register(
            name="test_migration",
            version="1.0.0",
            description="Test migration",
        )
        def test_func(dataset_path, dry_run=False):
            return {
                "success": True,
                "modified_files": [] if dry_run else ["test.json"],
                "message": "Dry run" if dry_run else "Modified files",
            }

        result = registry.run("test_migration", tmp_path, dry_run=True)
        assert result["success"] is True
        assert result["modified_files"] == []
        assert "Dry run" in result["message"]


class TestJsonHelpers:
    """Tests for JSON helper functions."""

    def test_load_json(self, tmp_path):
        """Test loading JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}

        with open(test_file, "w") as f:
            json.dump(test_data, f)

        loaded = load_json(test_file)
        assert loaded == test_data

    def test_load_json_nonexistent(self, tmp_path):
        """Test loading nonexistent JSON file returns None."""
        test_file = tmp_path / "nonexistent.json"
        loaded = load_json(test_file)
        assert loaded is None

    def test_load_json_invalid(self, tmp_path):
        """Test loading invalid JSON returns None."""
        test_file = tmp_path / "invalid.json"

        with open(test_file, "w") as f:
            f.write("not valid json{")

        loaded = load_json(test_file)
        assert loaded is None

    def test_save_json(self, tmp_path):
        """Test saving JSON file."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}

        result = save_json(test_file, test_data)
        assert result is True

        # Verify file contents
        with open(test_file) as f:
            loaded = json.load(f)
        assert loaded == test_data

    def test_save_json_with_indentation(self, tmp_path):
        """Test saving JSON file with custom indentation."""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value"}

        save_json(test_file, test_data, indent=4)

        # Check that file is properly indented
        with open(test_file) as f:
            content = f.read()
        assert "    " in content  # Should have 4-space indent
        assert content.endswith("\n")  # Should have trailing newline
