# Appendix XV: The Inheritance Principle

The [Inheritance Principle](#inheritance-principle) specifies how it is
not strictly necessary to have data and metadata files with identical names
apart from the [file extension](#definitions).
It is possible to have a single metadata file with its contents applicable
to multiple data files;
it is additionally possible to have one data file where there are multiple
metadata files from which metadata are applicable.
This Appendix provides the precise definition of how this principle operates
and the consequences of such,
as reference for both software implementations and advanced BIDS users.

## Rules

1.  Any metadata file (such as `.json`, `.bvec` or `.tsv`) MAY be defined at any directory level.

1.  For a given data file, any metadata file is applicable to that data file if:
    1.  It is stored at the same directory level or higher;
    1.  The metadata and the data filenames possess the same suffix;
    1.  The metadata filename does not include any entity absent from the data filename.

1.  A metadata file MUST NOT have a filename that would be otherwise applicable
    to some data file based on rules 2.b and 2.c but is made inapplicable based on its
    location in the directory structure as per rule 2.a.

1.  If, for a given data file, multiple metadata files satisfy criteria 2.a-c above:

    1.  The set of applicable metadata files is ordered as follows:

        1.  Within each level of the filesystem hierarchy:

            1.  Obtain the list of applicable metadata files within that directory.

            1.  Sort this list in order of fewest to most entities.

            1.  There MUST NOT be multiple applicable metadata files that
                possess the same number of entities.

            1.  The set of entities in any filename within this list MUST be a
                strict superset of those present in the filename that precedes
                it within this list.

        1.  These lists are concatenated in order of highest to lowest level in the
            filesystem hierarchy.

    1.  For [tabular files](#tabular-files) and other simple metadata files
        (for instance, [`bvec` / `bval` files for diffusion MRI](#bvec-bval),
        accessing metadata associated with a data file MUST consider only the
        last file in the order established by rule 4.a.

    1.  For [JSON files](#json-files), key-values MUST be loaded
        from applicable files sequentially in the order established by rule 4.a,
        overwriting any existing key-values when doing so.

### Corollaries

1.  As per rule 3, metadata files applicable only to a specific participant / session
    MUST be defined in or below the directory corresponding to that participant / session;
    similarly, a metadata file that is applicable to multiple participants / sessions
    MUST NOT be placed within a directory corresponding to only one such participant / session.

1.  It is permissible for a single metadata file to be applicable to multiple data files.
    Where such metadata content is consistent across multiple data files,
    it is RECOMMENDED to store metadata in this way,
    rather than duplicating that metadata content across multiple metadata files.

1.  Where multiple applicable [JSON files](#json-files) are loaded
    for one data file as per rules 4.a and 4.c:

    1.  Where the same key is present in multiple applicable metadata files,
        the final value associated with that key will be that of the file latest in
        the order in which that key is defined;
        any values associated with that key earlier in the ordering are overridden
        (though it is RECOMMENDED to minimize the extent of such overrides).

    1.  The requirement that applicable metadata files follow a strict ordering according to
        addition of entities applies individually within each level of the filesystem hierarchy;
        it is not necessary for the complete ordered set of all applicable metadata files
        across all filesystem levels to demonstrate strict addition of entities between
        sequential filenames.

    1.  A key-value being present in a metadata file earlier in the ordering but absent in
        any file later in the ordering does not imply the "unsetting" of that key-value.

    1.  Removal of key-values present in files earlier in the ordering based on the content
        of files later in the ordering is not possible.

## Advanced examples

### Example 1: Complex inheritance scenario

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filetree_example(
    {
    "bold.json": "",
    "sub-01": {
        "ses-01": {
            "func": {
                "sub-01_ses-01_bold.json": "",
                "sub-01_ses-01_task-ovg_bold.json": "",
                "sub-01_ses-01_task-ovg_run-1_bold.nii.gz": "",
                "sub-01_ses-01_task-ovg_run-2_bold.nii.gz": "",
                "sub-01_ses-01_task-ovg_run-2_bold.json": "",
                "sub-01_ses-01_task-rest_bold.nii.gz": "",
                "sub-01_ses-01_task-rest_bold.json": "",
                }
            },
        "ses-02": {
            "func": {
                "sub-01_ses-02_task-ovg_bold.nii.gz": "",
                "sub-01_ses-02_task-rest_bold.nii.gz": "",
                }
            },
        "sub-01_bold.json": "",
        },
    "sub-02": {
        "ses-01": {
            "func": {
                "sub-02_ses-01_task-rest_bold.nii.gz": "",
                "sub-02_ses-01_task-rest_bold.json": "",
                }
            }
        },
    "task-ovg_bold.json": "",
    "task-rest_bold.json": "",
    }
) }}

### Applicable data files per metadata file

For each metadata file, the set of data files to which its contents are
applicable is as follows:

-   `bold.json`:
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-ovg_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-rest_bold.nii.gz`
    -   `sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.nii.gz`

-   `task-ovg_bold.json`:
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-ovg_bold.nii.gz`

-   `task-rest_bold.json`:
    -   `sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-rest_bold.nii.gz`
    -   `sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.nii.gz`

-   `sub-01/sub-01_bold.json`:
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-ovg_bold.nii.gz`
    -   `sub-01/ses-02/func/sub-01_ses-02_task-rest_bold.nii.gz`

-   `sub-01/ses-01/sub-01_ses-01_bold.json`:
    -   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`
    -   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`
    -   `sub-01/ses-01/sub-01_ses-01_task-rest_bold.nii.gz`

-   `sub-01/ses-01/sub-01_ses-01_task-ovg_bold.json`:
    -   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`
    -   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`

-   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-2_bold.json`:
    -   `sub-01/ses-01/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`

-   `sub-01/ses-01/sub-01_ses-01_task-rest_bold.json`:
    -   `sub-01/ses-01/sub-01_ses-01_task-rest_bold.nii.gz`

-   `sub-02/ses-01/sub-02_ses-01_task-rest_bold.json`:
    -   `sub-02/ses-01/sub-02_ses-01_task-rest_bold.nii.gz`

### Applicable metadata files per data file

For each data file, the order in which the set of applicable metadata
files would be loaded is as follows:

-   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-1_bold.nii.gz`:
    -   `bold.json`
    -   `task-ovg_bold.json`
    -   `sub-01/sub-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_bold.json`

-   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-2_bold.nii.gz`:
    -   `bold.json`
    -   `task-ovg_bold.json`
    -   `sub-01/sub-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-ovg_run-2_bold.json`

-   `sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.nii.gz`:
    -   `bold.json`
    -   `task-rest_bold.json`
    -   `sub-01/sub-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_bold.json`
    -   `sub-01/ses-01/func/sub-01_ses-01_task-rest_bold.json`

-   `sub-01/ses-02/func/sub-01_ses-02_task-ovg_bold.nii.gz`:
    -   `bold.json`
    -   `task-ovg_bold.json`
    -   `sub-01/sub-01_bold.json`

-   `sub-01/ses-02/func/sub-01_ses-02_task-rest_bold.nii.gz`:
    -   `bold.json`
    -   `task-rest_bold.json`
    -   `sub-01/sub-01_bold.json`

-   `sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.nii.gz`:
    -   `bold.json`
    -   `task-rest_bold.json`
    -   `sub-02/ses-01/func/sub-02_ses-01_task-rest_bold.json`

### Example 2: Violation due to order ambiguity

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->

{{ MACROS___make_filetree_example(
    {
    "sub-01": {
        "func": {
            "sub-01_acq-highres_bold.json": "",
            "sub-01_acq-lowres_bold.json": "",
            "sub-01_bold.json": "",
            "sub-01_task-ovg_bold.json": "",
            "sub-01_task-ovg_acq-highres_bold.nii.gz": "",
            "sub-01_task-ovg_acq-lowres_bold.nii.gz": "",
            "sub-01_task-rest_bold.json": "",
            "sub-01_task-rest_acq-highres_bold.nii.gz": "",
            "sub-01_task-rest_acq-lowres_bold.nii.gz": "",
            }
        }
    }
) }}

Data file `sub-01_ses-01_task-ovg_acq-highres_bold.nii.gz` has three metadata
files deemed applicable according to rule 2, all residing within the same directory: (
`sub-01_bold.json`,
`sub-01_task-ovg_bold.json`,
`sub-01_acq-highres_bold.json`).
It is however impossible to determine a unique ordering of these files that
satisfies rule 4.a. The metadata contents to be associated with this data file
would be ambiguous if files `sub-01_task-ovg_bold.json` and `sub-01_acq-highres_bold.json`
were to contain differing values for the same key, as the ambiguous order in which
they were loaded would determine those contents.

<!-- Link Definitions -->

[bvec-bval]: 04-modality-specific-files/01-magnetic-resonance-imaging#required-gradient-orientation-information

[definitions]: 02-common-principles.md#definitions

[inheritance-principle]: 02-common-principles.md#the-inheritance-principle

[json-files]: 02-common-principles.md#key-value-files-dictionaries

[tabular-files]: 02-common-principles.md#tabular-files
