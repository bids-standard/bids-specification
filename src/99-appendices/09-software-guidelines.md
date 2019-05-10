# Appendix IX: BIDS software development guidelines 

This section RECOMMENDS some practices which could be adopted while developing
BIDS compatible software.

## Be consist with BIDS terminology

[Common Principles: Definitions](../02-common-principles.md#definitions) and
[Appendix IV: Entity table](04-entity-table.md) define some definitions and 
terms which ideally be used in the UI of the tools to make tools easier to use
by BIDS-aware users.
 
## Be resilient and future-proofing

BIDS is an evolving standard, and although we strive to clearly and unambiguously
describe all entities and filenames convention, retain backward compatibility, 
and version every release of the specification, some aspects could remain not
clarified and open for interpretation or future change.  E.g., the set of 
allowed characters in `<label>` might eventually change [ISSUE-226] or 
[inheritance principle](../02-common-principles.md#the-inheritance-principle)
could be further formalized (see [ISSUE-102]).
It is RECOMMENDED that BIDS supporting applications are coded adhering 
to [Postel's principle](https://en.wikipedia.org/wiki/Robustness_principle)
which is driving TCP implementations to *"be conservative in what you do, be 
liberal in what you accept from others."*


[ISSUE-226]: https://github.com/bids-standard/bids-specification/issues/226
[ISSUE-102]: https://github.com/bids-standard/bids-specification/issues/102