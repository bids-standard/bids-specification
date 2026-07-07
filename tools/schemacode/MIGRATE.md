# BIDS Dataset Migration Tools

The BIDS Schema Tools package includes a `migrate` command to help dataset maintainers adopt new standardized conventions introduced in BIDS specification updates.

## Overview

As the BIDS specification evolves, new conventions and metadata fields are introduced. The migration tools help you upgrade existing datasets to use these new standards without manual editing.

## Usage

### List Available Migrations

To see all available migrations:

```bash
bst migrate list
```

This will display:
- Migration name
- BIDS version when it was introduced
- Description of what the migration does

### Run a Specific Migration

To run a single migration on a dataset:

```bash
bst migrate run MIGRATION_NAME /path/to/dataset
```

For example:
```bash
bst migrate run standardize_generatedby /data/my_bids_dataset
```

### Dry Run Mode

To preview what would be changed without modifying files:

```bash
bst migrate run MIGRATION_NAME /path/to/dataset --dry-run
```

### Run All Migrations

To run all available migrations on a dataset:

```bash
bst migrate all /path/to/dataset
```

Skip specific migrations:

```bash
bst migrate all /path/to/dataset --skip standardize_generatedby --skip another_migration
```

## Available Migrations

### standardize_generatedby (version 1.10.0)

**Purpose:** Convert pre-standard provenance metadata to the standardized `GeneratedBy` field introduced in BEP028.

**What it does:**
- Looks for legacy provenance fields: `Pipeline`, `ProcessingPipeline`, `Software`, `Tool`, `Provenance`
- Converts them to the standard `GeneratedBy` array format
- Removes the legacy fields after migration

**Example:**

Before migration:
```json
{
  "Name": "My Dataset",
  "BIDSVersion": "1.9.0",
  "Pipeline": {
    "Name": "fmriprep",
    "Version": "1.4.1"
  },
  "Software": "SPM12"
}
```

After migration:
```json
{
  "Name": "My Dataset",
  "BIDSVersion": "1.9.0",
  "GeneratedBy": [
    {
      "Name": "fmriprep",
      "Version": "1.4.1",
      "Description": "Migrated from Pipeline field"
    },
    {
      "Name": "SPM12",
      "Description": "Migrated from Software field"
    }
  ]
}
```

### fix_inheritance_overloading (version 1.10.1)

**Purpose:** Check for deprecated inheritance overloading patterns (PR #1834).

**What it does:**
- Scans JSON sidecar files across different inheritance scopes
- Identifies fields that have different values at different levels (dataset, subject, session)
- Reports warnings about this deprecated pattern
- Does not modify files (check-only migration)

**Background:** Using different values for the same metadata field at different inheritance levels will not be supported in BIDS 2.0. This migration helps identify such cases so they can be addressed.

### fix_tsv_entity_prefix (version 1.10.1)

**Purpose:** Check for missing entity prefixes in TSV column headers (PR #2281).

**What it does:**
- Checks TSV files that should use entity prefixes (e.g., `samples.tsv`, `participants.tsv`)
- Identifies columns that lack proper entity prefixes
- Provides suggestions for corrections
- Does not modify files (check-only migration)

**Example issue:**
In `samples.tsv`, a column named `id` should be `sample_id`.

## Creating New Migrations

Migrations are registered using a decorator pattern. To add a new migration:

```python
from bidsschematools.migrate import registry

@registry.register(
    name="my_migration",
    version="1.11.0",
    description="Description of what this migration does"
)
def my_migration(dataset_path, dry_run=False):
    """
    Perform the migration.
    
    Parameters
    ----------
    dataset_path : Path
        Path to the BIDS dataset root
    dry_run : bool
        If True, don't modify files
        
    Returns
    -------
    dict
        Result with keys: success, modified_files, message
    """
    # Migration implementation
    modified_files = []
    
    # ... your migration code ...
    
    return {
        "success": True,
        "modified_files": modified_files,
        "message": "Migration completed"
    }
```

Add your migration to `bidsschematools/migrations.py` and it will automatically be available through the CLI.

## Migration Best Practices

1. **Always use dry-run first:** Preview changes before applying them
   ```bash
   bst migrate run MIGRATION_NAME /path/to/dataset --dry-run
   ```

2. **Backup your data:** While migrations are designed to be safe, always backup important datasets before running migrations

3. **Version control:** If your dataset is in git, commit before running migrations so you can review and revert if needed

4. **Review output:** Check the list of modified files and review changes to ensure they are correct

5. **Check-only migrations:** Some migrations only report issues without making changes. Review their output and make manual corrections as needed

## Exit Codes

- `0`: Success
- `1`: Migration failed or encountered errors
- `2`: Invalid usage (e.g., no dataset_description.json found)

## Logging

Use `-v` for verbose output:
```bash
bst -v migrate run MIGRATION_NAME /path/to/dataset
```

Use `-vv` for even more detailed logging:
```bash
bst -vv migrate run MIGRATION_NAME /path/to/dataset
```

## Related Resources

- [BIDS Specification](https://bids-specification.readthedocs.io/)
- [BEP028 (Provenance)](https://bids.neuroimaging.io/bep028)
- [PR #1834 (Inheritance Overloading)](https://github.com/bids-standard/bids-specification/pull/1834)
- [PR #2281 (Entity Prefixes)](https://github.com/bids-standard/bids-specification/pull/2281)
