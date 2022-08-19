--- PLEASE READ AND DELETE THE TEXT BELOW BEFORE OPENING THE PULL REQUEST ---

See the [CONTRIBUTING](https://github.com/bids-standard/bids-specification/blob/master/CONTRIBUTING.md) guide. Specifically:

- Please keep the title of your Pull Request (PR) short but informative - it will
  appear in the changelog.
- If you do **not** want a PR to appear in the changelog, it must receive the `exclude-from-changelog` label.
- Please ensure your name is credited on our [Contributors appendix](https://github.com/bids-standard/bids-specification/blob/master/src/99-appendices/01-contributors.md).
  To add your name, please edit our [Contributors wiki](https://github.com/bids-standard/bids-specification/wiki/Contributors) and add your name with the type of contribution.
  For assistance, please tag @bids-standard/maintainers.
- Use one of the following prefixes in the title of your PR:
  - `[ENH]` - enhancement of the specification that adds a new feature or
    support for a new data type
  - `[FIX]` - fix of a typo or language clarification
  - `[INFRA]` - changes to the infrastructure automating the specification
    release (for example building HTML docs)
  - `[SCHEMA]` - changes to the BIDS schema and/or related code
  - `[MISC]` - everything else including changes to the file listing
    contributors
- If you are opening a PR to obtain early feedback, but the changes
  are not ready to be merged (also known as a "Work in Progress" PR), please
  use a [Draft PR](https://github.blog/2019-02-14-introducing-draft-pull-requests/).
- After opening the PR, our continuous integration services will automatically check your contribution  for formatting errors and render a preview of the BIDS specification with your changes.
  To see the checks and preview, scroll down and click on the `show all checks` link.
  From the list, select the `Details` link of the `ci/circleci: build_docs artifact` check to see the preview of the BIDS specification.
- If you are updating the schema *and* you need to subsequently make changes to the bidsschematools code (validation, tests, rendering), this means your PR probably introduces a compatibility breaking change and you should increment the minor version (i.e. second number) in `bids-specification/src/schema/SCHEMA_VERSION`.

--- PLEASE READ AND DELETE THE TEXT ABOVE BEFORE OPENING THE PULL REQUEST ---
