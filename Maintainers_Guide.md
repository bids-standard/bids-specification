# BIDS Maintainers Group Guide

The BIDS Maintainers are a key group of members that ensure that the BIDS infrastructure is kept up.
The maintainers have wide-ranging responsibilities that enable BIDS to continue to grow and succeed.
As furthermore detailed in the [DECISION-MAKING document](DECISION-MAKING.md),
maintainers have a set of rights that go beyond those of a contributor.

The following guide draws heavily on a related [blog post](https://matthewrocklin.com/blog/2019/05/18/maintainer)
on "The Role of a Maintainer" by Matthew Rocklin,
which is a recommended reading in conjunction with this guide.

## Current BIDS Maintainers

See also: [BIDS governance](https://bids.neuroimaging.io/governance.html#bids-maintainers-group)

| Name                                                                      | Time commitment | Scope                                 | Joined   |
| ------------------------------------------------------------------------- | --------------- | ------------------------------------- | -------- |
| Stefan Appelhoff ([@sappelhoff](https://github.com/sappelhoff))           | 1h/week         |                                       | Mar 2020 |
| Chris Markiewicz ([@effigies](https://github.com/effigies))               | 5h/week         |                                       | Mar 2020 |
| Ross Blair ([@rwblair](https://github.com/rwblair))                       |                 | Maintainer of the bids-validator      | Mar 2020 |
| Taylor Salo ([@tsalo](https://github.com/tsalo))                          | 3h/week         | MRI                                   | Sep 2020 |
| Remi Gau ([@Remi-Gau](https://github.com/Remi-Gau))                       | 3h/week         | Community development, MRI            | Oct 2020 |
| Anthony Galassi  ([@bendhouseart](https://github.com/bendhouseart))       | 3h/week         | PET, Community development            | Sep 2021 |
| Eric Earl ([@ericearl](https://github.com/ericearl))                      | 2h/week         |                                       | Dec 2021 |
| Christine Rogers ([@christinerogers](https://github.com/christinerogers)) | 2h/month        | Interoperability, EEG and multi-modal | Apr 2023 |
| Nell Hardcastle ([@nellh](https://github.com/nellh))                      | 2h/week         |                                       | Jul 2023 |
| Kimberly Ray ([@KimberlyLRay](https://github.com/KimberlyLRay))           | 1h/week         |                                       | Nov 2022 |

In addition to the [BIDS Governance](https://bids.neuroimaging.io/governance.html#bids-maintainers-group)
classification of a maintainer, maintainers may declare a limited scope of responsibility.
Such a scope can range from maintaining a modality supported in the specification to nurturing a
welcoming BIDS community.
Any number of scopes can be chosen by the maintainer and agreed upon by the Maintainers Group.
A maintainer is primarily responsible for issues within their chosen scope(s), although
contributions elsewhere are welcome, as well.

### Lead Maintainer

The role of the "lead maintainer", that is, the BIDS maintainer currently representing the maintainers group,
is rotating among current maintainers.

## Past BIDS Maintainers

See also: [BIDS governance](https://bids.neuroimaging.io/governance.html#bids-maintainers-group)

| Name                                                                           | Duration            |
| ------------------------------------------------------------------------------ | ------------------- |
| Franklin Feingold ([@franklin-feingold](https://github.com/franklin-feingold)) | Mar 2020 - Jul 2022 |

## Why become a maintainer?

As a BIDS maintainer you may get the chance to:

* Learn to work as a team
* Bring your expertise to the BIDS maintainers group and cover technical blind spots it may have
* Improving your technical writing skills (for example documentation)
* Learn to work with continuous integration and deployment
* Advise and participate in the development of BIDS extensions that are most commonly associated with a publication

## Responsibilities

* Maintainers need to be loosely aware of the entire project
  and use their knowledge to facilitate and initiate interactions
  between different nodes of the project
  and determine a reasonable and timely order for features to be added and issues to be resolved.
* Maintainers direct other BIDS contributors in reviewing PRs,
  writing clarifications to the specification, or other contributions.
* Maintainers ensure that all contributors maintain a friendly and welcoming tone
  to encourage productive conversations.
* If no work team is suitable or available,
  the final responsibility of getting the work done lies with the maintainers.
* The development of each BIDS extension proposal should be "followed"
  by at least one maintainer who acts as a preferential point of contact
  between the BIDS maintainers and the BEP leads.

Apart from these abstract and general responsibilities,
maintainers within the BIDS community also need to ensure that the following tasks get done:

* Keeping the
  [Contributors wiki](https://github.com/bids-standard/bids-specification/wiki/Recent-Contributors)
  up to date and assisting new contributors with adding their credits,
  and performing community inquiries to ensure contributors are credited in the
  [Contributors appendix](https://bids-specification.readthedocs.io/en/stable/appendices/contributors.html)
    * Deciding what constitutes a contribution worth adding to the "Contributors list"
* Preparing a monthly report to the BIDS Steering Group.
  The monthly report is in the form of milestones, issues addressed,
  and open issues raised in the past month and goals/plans for the next month.
  The BIDS Steering Group may ask for additional information or propose a meeting to further discuss report items.
  The report format and meetings are at the discretion of the BIDS Steering Group.

Maintainers are not expected to individually be responsible for all the responsibilities listed.
Rather, the responsibilities are distributed amongst the entire group.

## Organization

* The group of maintainers are a group of people with the above mentioned responsibilities,
  who commit to convene bi-weekly meetings to discuss the project.
* One lead maintainer represents the group to other BIDS Groups, mediates disagreement among members,
  and casts deciding votes when needed (tie break).
  Note that the maintainers will always strive for consensus decision making, and will try to avoid resorting to voting.
    * The lead maintainer may delegate any of their duties to another maintainer.
    * The lead maintainer is appointed collectively by the group of maintainers, preferably through consensus.
    * If no one else does, the lead maintainer sets the schedule for the maintainers meeting.
* Additions to and departures from the group are negotiated collectively between the lead maintainer
  and the new/departing members, as they involve the redistribution of duties.
    * If a maintainer wishes to serve for a limited term, that can be arranged at the start. Otherwise, due notice is expected.
    * See also "How to become a maintainer?" below

## How to become a maintainer?

If you are interested in becoming a BIDS maintainer,
please get in contact with an active BIDS maintainer
(for example via opening a GitHub issue on bids-standard/bids-specification and tagging `@bids-standard/maintainers`).
In that initial contact, it would be great if you could outline previous experience with BIDS (if any)
and your motivation to become a maintainer, as well as particular interests for work that you would like to do.
The BIDS maintainers will then invite you to one of the biweekly maintainers meetings (online)
to discuss further steps and point you to the onboarding documentation (things to do).

We would be happy to hear from you!

## Crediting BIDS maintainers in work submissions

If you prepare a submission of work related to BIDS, and would like to credit the BIDS maintainers
in that submission, please get in touch.

It is for example possible to include BIDS maintainers as a consortium author,
through using the following OSF account: [https://osf.io/y48x9/](https://osf.io/y48x9/)

We are furthermore preparing more guidelines on this topic, see this work in progress:
https://docs.google.com/document/d/1yQdYOw7WMpkcFgT4tNalOjKuH34nhmRqg4luI4V9uhE/

## Notes

As detailed in the [BIDS governance](https://bids.neuroimaging.io/governance.html),
this guide is subject to change and to amendment by the BIDS Steering Group.
