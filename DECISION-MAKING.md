# Decision-making rules
## Introduction
The Brain Imaging Data Structure (BIDS) community set out the following 
decision-making rules with the intention to:

- Strive for consensus.
- Promote open discussions.
- Minimize the administrative burden.
- Provide a path for when consensus cannot be made.
- Grow the community.
- Maximize the [bus factor](https://en.wikipedia.org/wiki/Bus_factor) of the 
  project.

The rules outlined below are inspired by the [lazy consensus system used in the Apache Foundation](https://www.apache.org/foundation/voting.html) 
and heavily depends on [GitHub Pull Request Review system](https://help.github.com/articles/about-pull-requests/).

## Definitions
**Repository** - [https://github.com/bids-standard/bids-specification](https://github.com/bids-standard/bids-specification)
**Contributor** - a person listed in the Appendix I: Contributors. The 
community decides on the content of this file using the same process as any 
other change to the Repository (see below) allowing the meaning of "Contributor"
to evolve independently of the Decision-making rules.

## Rules
1. Every modification of the specification (including a correction of a typo, 
   adding a new Contributor, an extension adding support for a new data type, or
   others) or proposal to release a new version needs to be done via a Pull 
   Request (PR) to the Repository.
1. Anyone can open a PR (this action is not limited to Contributors).
1. A PR is eligible to be merged if and only if these conditions are met:
   1. The last commit is at least 5 working days old to allow the community to 
      evaluate it.
   1. The PR features at least one [Review that Approves](https://help.github.com/articles/about-pull-request-reviews/#about-pull-request-reviews) 
      the PR from a Contributor that is not an author of the PR. The review 
      needs to be made after the last commit in the PR (equivalent to 
      [Stale review dismissal](https://help.github.com/articles/enabling-required-reviews-for-pull-requests/)
      option on GitHub).
   1. Does not feature any [Reviews that Request changes](https://help.github.com/articles/about-required-reviews-for-pull-requests/).
   1. Does not feature "WIP" in the title (Work in Progress).
   1. Passes all automated tests.
1. Any Contributor can Review a PR and Request changes. If a Contributor 
   Request changes they need to provide an explanation what changes 
   should be added and justification of their importance. Reviews requesting 
   changes can also be used to request more time to review a PR.
1. A Contributor that Requested changes can Dismiss their own review or Approve 
   changes added by the Contributor who opened the PR.
1. If the author of a PR and Contributor who provided Review that Requests 
   changes cannot find a solution that would lead to the Contributor dismissing 
   their review or accepting the changes the Review can be Dismissed with a 
   vote. Rules governing voting:
   1. A Vote can be triggered by any Contributor, but only after 5 working days 
      from the time a Review Requesting Changes has been raised and in case a 
      Vote has been triggered previously no sooner than 15 working days since 
      its conclusion.
   1. Only Contributors can vote, each contributor gets one vote.
   1. A Vote ends after 5 working days or when all Contributors have voted 
      (whichever comes first).
   1. A Vote freezes the PR - no new commits or Reviews Requesting changes can 
      be added to it while a vote is ongoing. If a commit is accidentally made 
      during that period it should be reverted.
   1. The quorum for a Vote is 30% of all Contributors.
   1. The outcome of the vote is decided based on a simple majority.

## Comments

1. There are no restrictions on how the content of the PR is prepared. For 
   example it is perfectly fine for a PR to consist of content developed by a 
   group of experts over an extended period of time via in person meetings and 
   online collaborations using a Google Document.
1. To facilitate triaging of incoming PR you can subscribe to 
   notifications for new PRs proposing changes to specific files. To do this
   add your Github name next to the file you want to subscribe to in the 
   [CODEOWNERS](CODEOWNERS). This way you will be ask to review each relevant
   PR. Please mind that lack of your review will not prevent the PR from being
   merged so if you think the PR needs your attention, please review it 
   promptly or request more time via Request changes.
1. Releases are triggered the same way as any other change - via a PR.


