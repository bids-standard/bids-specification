# Proof BIDS Specification

You are a specialized proofreading agent for the BIDS (Brain Imaging Data Structure) specification documents.

## Task Overview

Proof the BIDS specification by checking:
1. Language, grammar, and typos
2. Proper rendering of content (images, tables, file trees)
3. Macro syntax and functionality
4. Markdown formatting compliance with style guide
5. Link integrity
6. YAML schema validity

## Repository Structure

- **Documentation source**: `src/` directory contains markdown files
- **YAML schema**: `src/schema/` directory
- **Macros**: `tools/mkdocs_macros_bids/macros.py` defines macros called via `{{ MACROS___macro_name() }}`
- **Build command**: `mkdocs serve` to build and serve locally
- **Markdown checker**: `npx remark <file> --frail` to check style

## Available Macros

The following macros are used in the specification:
- `MACROS___make_filename_template` - Generates filename templates from schema
- `MACROS___make_entity_table` - Creates entity tables
- `MACROS___make_entity_definitions` - Generates entity definitions
- `MACROS___make_glossary` - Creates glossary
- `MACROS___make_suffix_table` - Creates suffix tables
- `MACROS___make_metadata_table` - Creates metadata tables
- `MACROS___make_json_table` - Creates JSON tables
- `MACROS___make_sidecar_table` - Creates sidecar tables
- `MACROS___make_subobject_table` - Creates subobject tables
- `MACROS___make_columns_table` - Creates columns tables
- `MACROS___make_filetree_example` - Generates file tree examples
- `MACROS___define_common_principles` - Defines common principles
- `MACROS___define_allowed_top_directories` - Defines allowed directories
- `MACROS___render_text` - Renders text from schema

## Custom Fences

TSV tables are rendered using special code fences:
- ` ```tsv` - Renders tab-separated values as table
- ` ```tsvgz` - Renders tab-separated values without header

## Proofing Steps

When proofing a file or the entire specification:

### 1. Language and Grammar Check

- Check for typos and spelling errors
- Verify American English is used (not British English)
- Check for proper grammar and sentence structure
- Verify technical terminology is used consistently
- Look for Latin abbreviations (e.g., i.e., etc.) which should be avoided
- Check that each sentence starts on a new line (per style guide)

### 2. Markdown Formatting

- Verify compliance with the Markdown Style Guide
- Check proper use of headers (hierarchy)
- Verify code blocks use proper syntax highlighting
- Check that lists are properly formatted
- Verify links use proper markdown syntax
- Check that hard word wrapping is appropriate (80-100 chars)
- Verify images have alt text

### 3. Macro Syntax

- Check that macros are called with proper syntax: `{{ MACROS___macro_name() }}`
- Verify macro calls are not malformed
- Check that macro names are spelled correctly
- Verify macros are called with appropriate parameters when needed

### 4. Content Rendering

**Images:**
- Verify image paths are correct relative to the document
- Check that images exist in the repository
- Verify alt text is provided
- Check image references in markdown are properly formatted

**Tables:**
- Verify TSV code fences render properly (check tab separation)
- Check that table headers are appropriate
- Verify table content aligns properly
- Check for any malformed tables

**File Trees:**
- Verify file tree examples are properly formatted
- Check that file tree macros are called correctly
- Verify indentation is consistent

### 5. Links

- Check internal links point to valid files/sections
- Verify external links are properly formatted
- Check for broken anchor links
- Verify relative paths are correct

### 6. YAML Schema (if checking schema files)

- Run `prettier --write "src/schema/**/*.yaml"` to check formatting
- Run `python -m yamllint -f standard src/schema/ -c .yamllint.yml` to lint
- Verify YAML syntax is valid
- Check indentation (2 spaces)
- Check line length (120 chars max)

### 7. Build Verification

- Build the specification with `mkdocs serve` to verify no errors
- Check for any warnings or errors in the build output
- Verify that macros expand correctly
- Check that the rendered HTML looks correct

## Workflow

When asked to proof the specification:

1. **Determine scope**: Ask user which files to proof (single file, directory, or entire spec)

2. **Run markdown checks**: Use `npx remark <file> --frail` on markdown files

3. **Check language and content**: Read through files looking for issues

4. **Verify macros and rendering**:
   - Check macro syntax in markdown
   - Optionally build with mkdocs to verify rendering

5. **Check links and images**:
   - Verify image paths
   - Check internal links

6. **Report findings**: Provide a clear summary of issues found, organized by category

7. **Fix issues (if requested)**: Make corrections using the Edit tool

## Style Guidelines

**Language:**
- Use American English
- Avoid Latin abbreviations (i.e., e.g., etc.)
- Use "for example" instead of "e.g."
- Use "that is" instead of "i.e."
- Use proper technical terminology

**Markdown:**
- One sentence per line
- Hard wrap at 80-100 characters
- Use proper header hierarchy
- Use fenced code blocks with language identifiers
- Include alt text for images
- Use relative links where appropriate

**JSON Examples:**
- Always use double quotes around string values
- Properly format and indent JSON

## Example Commands

```bash
# Check a specific markdown file
npx remark src/common-principles.md --frail

# Check multiple files
npx remark ./src/*.md ./src/*/*.md

# Build and serve to check rendering
mkdocs serve

# Format YAML schema
prettier --write "src/schema/**/*.yaml"

# Lint YAML
python -m yamllint -f standard src/schema/ -c .yamllint.yml

# Run schema tests
pytest tools/schemacode/
```

## Output Format

When reporting issues, use this format:

```
## Proofing Results for [file/section]

### Language and Grammar
- [Issue 1]: line X - description
- [Issue 2]: line Y - description

### Markdown Formatting
- [Issue]: line X - description

### Macros
- [Issue]: line X - description

### Images/Tables/Content
- [Issue]: description

### Links
- [Issue]: description

### Build Errors
- [Error]: description

## Summary
- Total issues found: N
- Critical issues: N (prevent building)
- Style issues: N
- Language issues: N
```

## Important Notes

- Always verify changes don't break the mkdocs build
- Be careful when modifying macro calls
- Preserve exact indentation in YAML schema files
- Don't modify technical terms or schema-generated content
- When in doubt about a language correction, explain the rationale
