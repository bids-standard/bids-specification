"""Specific BIDS dataset migrations.

This module contains individual migration functions for various BIDS version updates.
"""

import json
import logging
from pathlib import Path
from typing import Any

from .migrate import load_json, registry, save_json

lgr = logging.getLogger(__name__)


@registry.register(
    name="standardize_generatedby",
    version="1.10.0",
    description=(
        "Convert pre-standard provenance metadata to standardized GeneratedBy field. "
        "This migration helps adopt BEP028 conventions for dataset provenance tracking."
    ),
)
def migrate_generatedby(dataset_path: Path, dry_run: bool = False) -> dict[str, Any]:
    """Migrate pre-standard provenance to GeneratedBy field.

    This migration looks for common pre-standard provenance fields and converts
    them to the standardized GeneratedBy array format introduced in BEP028.

    Common pre-standard fields that may be migrated:
    - Provenance
    - Pipeline
    - ProcessingPipeline
    - Software

    Parameters
    ----------
    dataset_path : Path
        Path to the BIDS dataset root
    dry_run : bool, optional
        If True, don't actually modify files, default False

    Returns
    -------
    dict
        Migration result with success status, modified files, and message
    """
    modified_files = []
    issues = []

    # Look for dataset_description.json files (including in derivatives)
    desc_files = list(dataset_path.glob("dataset_description.json"))
    desc_files.extend(dataset_path.glob("derivatives/*/dataset_description.json"))
    desc_files.extend(dataset_path.glob("derivatives/*/*/dataset_description.json"))

    if not desc_files:
        return {
            "success": True,
            "modified_files": [],
            "message": "No dataset_description.json files found"
        }

    for desc_file in desc_files:
        data = load_json(desc_file)
        if data is None:
            issues.append(f"Could not load {desc_file}")
            continue

        # Check if GeneratedBy already exists
        if "GeneratedBy" in data:
            lgr.debug(f"GeneratedBy already exists in {desc_file}, skipping")
            continue

        # Look for pre-standard fields to migrate
        generated_by = []
        migrated_fields = []

        # Check for common pre-standard fields
        pre_standard_fields = {
            "Provenance": "provenance",
            "Pipeline": "pipeline",
            "ProcessingPipeline": "processing_pipeline",
            "Software": "software",
            "Tool": "tool",
        }

        for old_field, field_type in pre_standard_fields.items():
            if old_field in data:
                value = data[old_field]
                migrated_fields.append(old_field)

                # Convert to GeneratedBy format
                if isinstance(value, str):
                    # Simple string, create basic entry
                    entry = {
                        "Name": value,
                        "Description": f"Migrated from {old_field} field"
                    }
                    generated_by.append(entry)
                elif isinstance(value, dict):
                    # Already structured, try to map fields
                    entry = {}
                    if "Name" in value:
                        entry["Name"] = value["Name"]
                    elif "name" in value:
                        entry["Name"] = value["name"]
                    else:
                        entry["Name"] = old_field

                    if "Version" in value:
                        entry["Version"] = value["Version"]
                    elif "version" in value:
                        entry["Version"] = value["version"]

                    if "Description" in value:
                        entry["Description"] = value["Description"]
                    elif "description" in value:
                        entry["Description"] = value["description"]
                    else:
                        entry["Description"] = f"Migrated from {old_field} field"

                    # Handle container info if present
                    if "Container" in value or "container" in value:
                        entry["Container"] = value.get("Container", value.get("container"))

                    generated_by.append(entry)
                elif isinstance(value, list):
                    # List of entries
                    for item in value:
                        if isinstance(item, str):
                            generated_by.append({
                                "Name": item,
                                "Description": f"Migrated from {old_field} field"
                            })
                        elif isinstance(item, dict):
                            entry = {}
                            entry["Name"] = item.get("Name", item.get("name", old_field))
                            if "Version" in item or "version" in item:
                                entry["Version"] = item.get("Version", item.get("version"))
                            entry["Description"] = item.get(
                                "Description",
                                item.get("description", f"Migrated from {old_field} field")
                            )
                            if "Container" in item or "container" in item:
                                entry["Container"] = item.get("Container", item.get("container"))
                            generated_by.append(entry)

        if generated_by:
            if not dry_run:
                # Add GeneratedBy field
                data["GeneratedBy"] = generated_by

                # Remove old fields
                for field in migrated_fields:
                    del data[field]

                # Save updated file
                if save_json(desc_file, data):
                    modified_files.append(str(desc_file.relative_to(dataset_path)))
                    lgr.info(
                        f"Migrated {len(generated_by)} provenance entries in {desc_file.name}: "
                        f"removed fields {migrated_fields}"
                    )
                else:
                    issues.append(f"Failed to save {desc_file}")
            else:
                lgr.info(
                    f"[DRY RUN] Would migrate {len(generated_by)} provenance entries in "
                    f"{desc_file}: remove fields {migrated_fields}"
                )
                modified_files.append(f"{desc_file.relative_to(dataset_path)} (dry run)")

    if issues:
        message = f"Completed with issues: {'; '.join(issues)}"
        success = False
    elif modified_files:
        message = f"Migrated provenance in {len(modified_files)} file(s)"
        success = True
    else:
        message = "No pre-standard provenance fields found to migrate"
        success = True

    return {
        "success": success,
        "modified_files": modified_files,
        "message": message,
    }


@registry.register(
    name="fix_inheritance_overloading",
    version="1.10.1",
    description=(
        "Warn about deprecated inheritance overloading patterns. "
        "Per PR #1834, overloading metadata values in the inheritance principle "
        "will be deprecated in BIDS 2.0. This migration scans for potential issues."
    ),
)
def check_inheritance_overloading(dataset_path: Path, dry_run: bool = False) -> dict[str, Any]:
    """Check for inheritance overloading patterns that will be deprecated.

    This migration scans for cases where the inheritance principle is being
    used to overload values (e.g., using different values in different scopes
    for the same metadata field). This pattern is deprecated per PR #1834.

    Parameters
    ----------
    dataset_path : Path
        Path to the BIDS dataset root
    dry_run : bool, optional
        Not used for this check-only migration

    Returns
    -------
    dict
        Migration result with warnings about overloading patterns
    """
    warnings = []
    metadata_by_scope = {}

    # Find all JSON sidecar files
    json_files = list(dataset_path.rglob("*.json"))
    json_files = [f for f in json_files if f.name != "dataset_description.json"]

    if not json_files:
        return {
            "success": True,
            "modified_files": [],
            "message": "No JSON sidecar files found to check"
        }

    # Analyze metadata fields across different scopes
    for json_file in json_files:
        data = load_json(json_file)
        if data is None:
            continue

        # Determine scope level (dataset, subject, session, etc.)
        parts = json_file.relative_to(dataset_path).parts
        if len(parts) > 1 and parts[0].startswith("sub-"):
            if len(parts) > 2 and parts[1].startswith("ses-"):
                scope = f"subject-session ({parts[0]}/{parts[1]})"
            else:
                scope = f"subject ({parts[0]})"
        else:
            scope = "dataset"

        # Track metadata by field name
        for field, value in data.items():
            if field not in metadata_by_scope:
                metadata_by_scope[field] = {}

            if scope not in metadata_by_scope[field]:
                metadata_by_scope[field][scope] = []

            metadata_by_scope[field][scope].append({
                "file": str(json_file.relative_to(dataset_path)),
                "value": value,
            })

    # Check for overloading (same field with different values in different scopes)
    for field, scopes in metadata_by_scope.items():
        if len(scopes) > 1:
            # Get unique values across scopes
            all_values = []
            for scope_data in scopes.values():
                for item in scope_data:
                    value_str = json.dumps(item["value"], sort_keys=True)
                    if value_str not in all_values:
                        all_values.append(value_str)

            # If multiple different values, this is potential overloading
            if len(all_values) > 1:
                scope_summary = []
                for scope, items in scopes.items():
                    scope_summary.append(f"{scope}: {len(items)} file(s)")

                warnings.append(
                    f"Field '{field}' has different values across scopes "
                    f"({', '.join(scope_summary)}). This inheritance overloading pattern "
                    "is deprecated and will not be supported in BIDS 2.0. "
                    "Consider using separate metadata fields or entity labels instead."
                )

    if warnings:
        message = (
            f"Found {len(warnings)} potential inheritance overloading pattern(s). "
            "See warnings for details."
        )
        lgr.warning(message)
        for warning in warnings:
            lgr.warning(warning)
    else:
        message = "No inheritance overloading patterns detected"

    return {
        "success": True,
        "modified_files": [],
        "message": message,
        "warnings": warnings,
    }


@registry.register(
    name="fix_tsv_entity_prefix",
    version="1.10.1",
    description=(
        "Check for missing entity prefixes in TSV column headers. "
        "Per PR #2281, certain TSV files should use entity- prefix for their columns."
    ),
)
def check_tsv_entity_prefix(dataset_path: Path, dry_run: bool = False) -> dict[str, Any]:
    """Check for and optionally fix missing entity prefixes in TSV files.

    Some TSV files are expected to have entity prefixes (e.g., 'sample-' prefix
    in samples.tsv for columns that identify samples). This migration helps
    identify inconsistencies.

    Parameters
    ----------
    dataset_path : Path
        Path to the BIDS dataset root
    dry_run : bool, optional
        If True, don't actually modify files, default False

    Returns
    -------
    dict
        Migration result with findings about entity prefix consistency
    """
    issues = []
    suggestions = []

    # Files that should use entity prefixes
    # Format: {filename_pattern: expected_entity_prefix}
    expected_prefixes = {
        "samples.tsv": "sample",
        "participants.tsv": "participant",
    }

    for pattern, entity in expected_prefixes.items():
        tsv_files = list(dataset_path.glob(pattern))
        tsv_files.extend(dataset_path.glob(f"*/{pattern}"))

        for tsv_file in tsv_files:
            try:
                with open(tsv_file) as f:
                    header = f.readline().strip()
                    if not header:
                        continue

                    columns = header.split("\t")

                    # Check if first column lacks proper prefix
                    if columns and not columns[0].startswith(f"{entity}_"):
                        # Special case: participant_id is standard, don't flag it
                        if tsv_file.name == "participants.tsv" and columns[0] == "participant_id":
                            continue

                        suggestions.append(
                            f"{tsv_file.relative_to(dataset_path)}: "
                            f"Column '{columns[0]}' should likely be '{entity}_{columns[0]}'"
                        )
            except Exception as e:
                issues.append(f"Error reading {tsv_file}: {e}")

    if suggestions:
        message = (
            f"Found {len(suggestions)} TSV files with potential entity prefix issues. "
            "Manual review recommended."
        )
        lgr.info(message)
        for suggestion in suggestions:
            lgr.info(f"  - {suggestion}")
    else:
        message = "No entity prefix issues detected in TSV files"

    if issues:
        for issue in issues:
            lgr.warning(issue)

    return {
        "success": True,
        "modified_files": [],
        "message": message,
        "suggestions": suggestions,
        "issues": issues,
    }
