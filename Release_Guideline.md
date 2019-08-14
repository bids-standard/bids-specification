# Release Guidelines

This document captures guidelines to follow when considering a new release of the BIDS specification.

## Background
BIDS has generally followed a semantic versioning (semver) approach.
The canonical semver text can be found at https://semver.org/, and an adaptation to documents can be found at https://semverdoc.org/.
A specification falls somewhere between these two, as documentation does not require
backwards compatibility, while software has notions of bugs and features which do not
map to the reasons for updating a specification.

In both cases, edition numbers are specified as MAJOR.MINOR.PATCH, and the difference is in the rules for incrementing each edition number.

In BIDS, we have considered a major release version (the next being 2.0.0) to indicate
backwards-incompatible changes, while minor and patch releases must be backwards compatible.

## Guidelines

Once a decision for a release has been established, the rules of [decision-making](DECISION-MAKING.md)
govern the mechanism of doing the release, *i.e.*, waiting 5 business days and obtaining
the approval of at least one maintainer before merging.

### Minor (1.X.0) releases

A minor release should be made when a BEP (BIDS Extension Proposal) has been merged into the
specification.
The BIDS Maintainers have discretion to identify other cases justifying a minor release.

### Patch (1.X.Y) releases

Patch releases will generally be more frequent, and indicate less significant changes to the specification.
The following is a non-exhaustive set of justifications for a patch release:

- A modality field has changed and the [bids-validator](https://github.com/bids-standard/bids-validator) has been updated to reflect this change.
- Links or information in the specification are no longer accurate, *e.g.* if a BEP document is added or moved
- The rendering of the [specification](https://bids-specification.readthedocs.io/en/stable/) has changed
- A metadata field or file type is added at the request of a curator attempting to release BIDS-compliant data

Ultimately, all releases are a matter of maintainer discretion, but patch release frequency should
balance community needs for stability and responsiveness.
