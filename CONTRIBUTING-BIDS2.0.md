# HOWTO for BIDS 2.0 development branch

## References

- Current PR: https://github.com/bids-standard/bids-specification/pull/1775
- BIDS 2.0 Project: https://github.com/orgs/bids-standard/projects/10
- Full list of issues to consider: https://github.com/bids-standard/bids-2-devel/issues
- https://github.com/bids-standard/bids-2-devel/issues/57

## Instructions

- **Minimization of "persistent" comments: Do not comment in the main thread of this PR to avoid flooding it**
  - Ideally: initiate PR from a feature branch with desired changes so we could concentrate discussion on the topic there
  - If needed: start discussion as a comment attached to pertinent location in [diff view](https://github.com/bids-standard/bids-specification/pull/1775/files) so we could eventually resolve it to collapse
- **To contribute to this PR -- submit a PR against the `bids-2.0` branch**
  - If you host that feature branch in this repository, it is RECOMMENDED to name it with `bids-2.0-` prefix.
  - **WARNING**: this PR can rebase or otherwise modify its set of commits (squash etc), so it is recommended to keep your feature branch also succinct to just few commits so it would be obvious what to rebase on top of rebased [bids-2.0].
  - When changes accepted they would be incorporated without Merge commit and might undergo squashing into just few commits to reflect that change.
  - Where relevant do not forget to reference or close an issue from [bids-2-devel/issues](https://github.com/bids-standard/bids-2-devel/issues)
- **Minimization of commits/diff**. To make it manageable to review, diff in this PR should avoid mass changes which could be scripted.
  - For scripted changes there would be scripts and "fix up patches" collected (in this PR) under `tools/bids-2.0/` directory. See [tools/bids-2.0/README.md](https://github.com/bids-standard/bids-specification/pull/1775/files) and files under the [tools/bids-2.0/patches/] for more details and example(s).
  - Those scripts will be applied on CI and changes pushed to [bids-2.0-patched](https://github.com/bids-standard/bids-specification/tree/bids-2.0) branch.
    - you can review [diff bids-2.0..bids-2.0-patched](https://github.com/bids-standard/bids-specification/compare/bids-2.0..bids-2.0-patched) to see if scripts or fixup patches need to be adjusted
    - that [bids-2.0-patched] is pushed by `validate-datasets` workflow
    - rendered: https://bids-specification.readthedocs.io/en/bids-2.0-patched/
    - if fixes spotted needed on top of [bids-2.0-patched] - they should be committed on top and `git format-patch` and added to `tools/bids-2.0/patches/` or absorbed into already existing patches there in.

[tools/bids-2.0/README.md]: https://github.com/bids-standard/bids-specification/pull/1775/files
[bids-2.0]: https://github.com/bids-standard/bids-specification/tree/bids-2.0
[bids-2.0-patched]: https://github.com/bids-standard/bids-specification/tree/bids-2.0-patched
[tools/bids-2.0/]: https://github.com/bids-standard/bids-specification/tree/bids-2.0/tools/bids-2.0/
[tools/bids-2.0/README.md]: https://github.com/bids-standard/bids-specification/tree/bids-2.0/tools/bids-2.0/README.md
[tools/bids-2.0/patches/]: https://github.com/bids-standard/bids-specification/tree/bids-2.0/tools/bids-2.0/patches
