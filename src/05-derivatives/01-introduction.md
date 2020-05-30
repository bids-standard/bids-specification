# BIDS Derivatives

Derivatives are outputs of common processing pipelines, capturing data and
meta-data sufficient for a researcher to understand and (critically) reuse those
outputs in subsequent processing.
Standardizing derivatives is motivated by use cases where formalized
machine-readable access to processed data enables higher level processing.

The following sections cover additions to and divergences from "raw" BIDS.
Placement and naming conventions for derived datasets are addressed in
[Storage of derived datasets][storage], and dataset-level metadata is included
in [Derived dataset and pipeline description][derived-dataset-description].

## Metadata conventions

-   Unless specified otherwise, individual sidecar JSON files and all metadata
    fields within are OPTIONAL. However, the appropriate use of these files and
    pertinent fields is very valuable and thus encouraged. Moreover, for some
    types of files, there may be one or more required metadata fields, in which
    case at least one metadata file containing that field must be located
    somewhere within the file’s hierarchy (per [the Inheritance
    Principle](../02-common-principles.md#the-inheritance-principle)).

-   When chaining derivative pipelines, any JSON fields that were specified as
    mandatory in the input files SHOULD be propagated forward in the output
    file’s JSON provided they remain valid. Non-required JSON fields MAY be
    propagated, and are highly useful, but it is the pipeline’s responsibility
    to ensure that the values are still relevant and appropriate to the type of
    output data.

## File naming conventions

-   Filenames that are permissible for a raw BIDS data type have a privileged
    status. Any modification of raw files must use a modified filename that does
    not conflict with the raw filename. Further, any files created as part of a
    derivative dataset must not match a permissible filename of a valid raw
    dataset. Stated equivalently, if any filename in a derivative dataset has a
    name permissible for a raw BIDS data, then that file must be an identical
    copy of that raw file.

-   Each Derivatives filename MUST be of the form:
    `<source_entities>[_keyword-<value>]_<suffix>.<ext>`
    (where `<value>` could either be an `<index>` or a `<label>` depending on
    the keyword; see [Definitions][definitions])

-   When the derivatives chain involves outputs derived from a single raw input,
    `source_entities` MUST be the entire source filename, with the omission of
    the source suffix and extension. One exception to this rule is filename
    entities that are no longer relevant. Depending on the nature of the
    derivative file, the suffix can either be the same as the source file if
    that suffix is still appropriate, or a new appropriate value selected from
    the controlled list.

-   There is no prohibition against identical filenames in different derived
    datasets, although users should be aware of the potential ambiguity this can
    create and use the sidecar JSON files to detail the specifics of individual
    files.

-   When necessary to distinguish two files that do not otherwise have a
    distinguishing entity, the `_desc-<label>` keyword-value SHOULD be used.
    This includes the cases of needing to distinguish both differing inputs and
    differing outputs (for example, `_desc-T1w` and `_desc-T2w` to distinguish
    brain mask files derived from T1w and T2w images;
    or `_desc-sm4` and `_desc-sm8` to distinguish between outputs generated with
    two different levels of smoothing).

-   When naming files that are not yet standardized, it is RECOMMENDED to use
    names consistent with BIDS conventions where those conventions apply.
    For example, if a summary statistic is derived from a given task, the file
    name SHOULD contain `_task-<label>`.

[]: <> (################)
[]: <> (Link definitions)
[]: <> (################)

[definitions]: ../02-common-principles.md#definitions
[storage]: ../02-common-principles.md#storage-of-derived-datasets
[derived-dataset-description]: ../03-modality-agnostic-files.md#derived-dataset-and-pipeline-description
