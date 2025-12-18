"""BIDS dataset migration utilities.

This module provides functionality to migrate BIDS datasets from older versions
to newer standardized forms, helping users adopt new conventions and metadata fields.
"""

import json
import logging
from pathlib import Path
from typing import Any, Callable, Optional

lgr = logging.getLogger(__name__)


class Migration:
    """Represents a single migration operation.

    Attributes
    ----------
    name : str
        Human-readable name of the migration
    version : str
        BIDS version when this migration applies (e.g., "1.10.0")
    description : str
        Description of what this migration does
    func : Callable
        The function that performs the migration
    """

    def __init__(
        self,
        name: str,
        version: str,
        description: str,
        func: Callable[[Path], dict[str, Any]],
    ):
        """Initialize a migration.

        Parameters
        ----------
        name : str
            Human-readable name of the migration
        version : str
            BIDS version when this migration applies
        description : str
            Description of what this migration does
        func : Callable
            The function that performs the migration, takes dataset path
            and returns a dict with 'success', 'modified_files', and 'message' keys
        """
        self.name = name
        self.version = version
        self.description = description
        self.func = func

    def __call__(self, dataset_path: Path, **kwargs) -> dict[str, Any]:
        """Execute the migration.

        Parameters
        ----------
        dataset_path : Path
            Path to the BIDS dataset root
        **kwargs
            Additional keyword arguments for the migration function

        Returns
        -------
        dict
            Result of the migration with keys:
            - success: bool indicating if migration succeeded
            - modified_files: list of modified file paths
            - message: str with details about the migration
        """
        return self.func(dataset_path, **kwargs)


class MigrationRegistry:
    """Registry for BIDS dataset migrations."""

    def __init__(self):
        """Initialize the migration registry."""
        self._migrations: dict[str, Migration] = {}

    def register(
        self,
        name: str,
        version: str,
        description: str,
    ) -> Callable:
        """Decorator to register a migration function.

        Parameters
        ----------
        name : str
            Human-readable name of the migration
        version : str
            BIDS version when this migration applies
        description : str
            Description of what this migration does

        Returns
        -------
        Callable
            Decorator function

        Examples
        --------
        >>> registry = MigrationRegistry()
        >>> @registry.register(
        ...     name="standardize_generatedby",
        ...     version="1.10.0",
        ...     description="Convert pre-standard provenance to GeneratedBy field"
        ... )
        ... def migrate_generatedby(dataset_path):
        ...     # migration code here
        ...     return {"success": True, "modified_files": [], "message": "Done"}
        """

        def decorator(func: Callable) -> Migration:
            migration = Migration(name, version, description, func)
            self._migrations[name] = migration
            lgr.debug(f"Registered migration: {name} (version {version})")
            return migration

        return decorator

    def get(self, name: str) -> Optional[Migration]:
        """Get a migration by name.

        Parameters
        ----------
        name : str
            Name of the migration

        Returns
        -------
        Migration or None
            The migration if found, None otherwise
        """
        return self._migrations.get(name)

    def list_migrations(self) -> list[dict[str, str]]:
        """List all registered migrations.

        Returns
        -------
        list of dict
            List of migration metadata with name, version, and description
        """
        return [
            {
                "name": mig.name,
                "version": mig.version,
                "description": mig.description,
            }
            for mig in self._migrations.values()
        ]

    def run(
        self,
        name: str,
        dataset_path: Path,
        dry_run: bool = False,
        **kwargs,
    ) -> dict[str, Any]:
        """Run a specific migration.

        Parameters
        ----------
        name : str
            Name of the migration to run
        dataset_path : Path
            Path to the BIDS dataset root
        dry_run : bool, optional
            If True, don't actually modify files, default False
        **kwargs
            Additional keyword arguments for the migration

        Returns
        -------
        dict
            Result of the migration

        Raises
        ------
        ValueError
            If migration not found
        """
        migration = self.get(name)
        if migration is None:
            raise ValueError(f"Migration '{name}' not found")

        lgr.info(f"Running migration: {migration.name} (version {migration.version})")
        lgr.info(f"Description: {migration.description}")

        if dry_run:
            lgr.info("DRY RUN: No files will be modified")
            kwargs["dry_run"] = True

        result = migration(dataset_path, **kwargs)

        if result.get("success"):
            lgr.info(f"Migration completed successfully: {result.get('message', '')}")
        else:
            lgr.warning(f"Migration failed or had issues: {result.get('message', '')}")

        return result


# Global registry instance
registry = MigrationRegistry()


def load_json(filepath: Path) -> Optional[dict]:
    """Load JSON file safely.

    Parameters
    ----------
    filepath : Path
        Path to JSON file

    Returns
    -------
    dict or None
        Loaded JSON data, or None if error
    """
    try:
        with open(filepath) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        lgr.error(f"Error loading {filepath}: {e}")
        return None


def save_json(filepath: Path, data: dict, indent: int = 2) -> bool:
    """Save JSON file safely.

    Parameters
    ----------
    filepath : Path
        Path to JSON file
    data : dict
        Data to save
    indent : int, optional
        JSON indentation, default 2

    Returns
    -------
    bool
        True if successful, False otherwise
    """
    try:
        with open(filepath, "w") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.write("\n")  # Add newline at end of file
        return True
    except Exception as e:
        lgr.error(f"Error saving {filepath}: {e}")
        return False
