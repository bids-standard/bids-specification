# Contributing to the BIDS Specification

**Welcome to the BIDS Specification repository!**

_We're so excited you're here and want to contribute._

We hope that these guidelines are designed to make it as easy as possible to get
involved. 
If you have any questions that aren't discussed below, please let us know 
by [opening an issue](#understanding-issues).

## Table of contents

Been here before? 
Already know what you're looking for in this guide? 
Jump to the following sections:

-   [Joining the BIDS community](#joining-the-community)
-   [Contributing through GitHub](#contributing-through-github)
-   [Understanding issues](#understanding-issues)
-   [Writing in markdown](#writing-in-markdown)
-   [Fixing Remark errors from Travis](#fixing-travis-remark-errors)
-   [Making a change with a pull request](#making-a-change-with-a-pull-request)
-   [Example pull request](#example-pull-request)
-   [Commenting on a pull request](#commenting-on-a-pull-request)
-   [Accepting suggestion from a review](#accepting-suggestion-from-a-review)
-   [Updating the specification schema](#updating-the-schema)
-   [Recognizing contributions](#recognizing-contributions)

## Joining the community

BIDS - the [Brain Imaging Data Structure](https://bids.neuroimaging.io/) - is a
growing community of neuroimaging enthusiasts, and we want to make our resources
accessible to and engaging for as many researchers as possible.

How do you know that you're a member of the BIDS community? 
You're here! 
You know that BIDS exists! 
You're officially a member of the community. 
It's THAT easy! Welcome!

Most of our discussions take place here in
[GitHub issues](#understanding-issues). 
We also have a
[bids-discussion](https://groups.google.com/forum/#!forum/bids-discussion)
Google Group, although this is largely now an archive of previous conversations.

Moving forward, we encourage all members to contribute here on
[GitHub](https://github.com/bids-standard/bids-specification) or on the
[NeuroStars](https://neurostars.org/tags/bids) Discourse Forum, under the `bids`
tag.

To keep on top of new posts, please see this guide for setting your
[topic notifications](https://meta.discourse.org/t/discourse-new-user-guide/96331#heading--topic-notifications).

As a reminder, we expect that all contributions adhere to our
[Code of Conduct](CODE_OF_CONDUCT.md).

## Contributing through GitHub

[Git](https://git-scm.com/) is a really useful tool for version control.
[GitHub](https://github.com/) sits on top of git and supports collaborative and
distributed working.

We know that it can be daunting to start using git and GitHub if you haven't
worked with them in the past, but the BIDS Specification maintainers are here to
help you figure out any of the jargon or confusing instructions you encounter!

In order to contribute via GitHub you'll need to set up a free account and sign
in. 
Here are some
[instructions](https://help.github.com/articles/signing-up-for-a-new-github-account/)
to help you get going. 
Remember that you can ask us any questions you need to along the way.

## Understanding issues

Every project on GitHub uses
[issues](https://github.com/bids-standard/bids-specification/issues) slightly
differently.

The following outlines how BIDS developers think about communicating through
issues.

**Issues** are individual pieces of work that need to be completed or decisions
that need to be made to move the project forwards. 
A general guideline: if you find yourself tempted to write a great big issue 
that is difficult to describe as one unit of work, please consider splitting it 
into two or more issues.

Issues are assigned [labels](#issue-labels) which explain how they relate to the
overall project's goals and immediate next steps.

### Issue labels

The current list of labels are
[here](https://github.com/bids-standard/bids-specification/labels) and include:

-   [![Help wanted](https://img.shields.io/badge/-help%20wanted-159818.svg)](https://github.com/bids-standard/bids-specification/labels/help%20wanted)
    _These issues contain a task that a member of the team has determined we
    need additional help with._

    If you feel that you can contribute to one of these issues, we especially
    encourage you to do so!

-   [![Opinions wanted](https://img.shields.io/badge/-opinions%20wanted-84b6eb.svg)](https://github.com/bids-standard/bids-specification/labels/opinions%20wanted)
    _These issues hold discussions where we're especially eager for feedback._

    Ongoing discussions benefit from broad feedback. 
    This label is used to highlight issues where decisions are being considered, 
    so please join the conversation!

-   [![Community](https://img.shields.io/badge/-community-%23ddcc5f.svg)](https://github.com/bids-standard/bids-specification/labels/community)
    _These issues are related to building and supporting the BIDS community._

    In addition to the specification itself, we are dedicated to creating a
    healthy community. 
    These issues highlight pieces of work or discussions
    around how we can support our members and make it easier to contribute.

## Writing in markdown

The specification documents follow the
[Markdown Style Guide](http://www.cirosantilli.com/markdown-style-guide/).

You can validate your changes against the guide using
[remark](https://github.com/remarkjs/remark-lint) which works as a
[standalone command line tool](https://github.com/remarkjs/remark/tree/master/packages/remark-cli)
as well as
[a plugin for various text editors](https://github.com/remarkjs/remark-lint#editor-integrations).
Remark preserves consistent markdown styling across the contributions. 
Please ensure before submitting a contribution that you do not have any linter errors
in your text editor. 
You can also use [prettier](https://github.com/prettier/prettier) to 
automatically correct some of the style issues that might be found 
in the proposed changes.

We have deployed a continuous integrator ([circle CI](https://circleci.com/)) to
further allow for integrating changes continuously. 
The CI is testing that the changes are inline with our standard styling.

GitHub has a helpful page on
[getting started with writing and formatting on GitHub](https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github).

## Building the specification using mkdocs

We are using mkdocs to render our specification. 
Please follow these instructions if you would like to build the specification locally.

#### 1. Install mkdocs

To begin please follow [this link](https://www.mkdocs.org/#installation) to
install mkdocs locally.

#### 2. Download the BIDS specification [repository](https://github.com/bids-standard/bids-specification/tree/master) onto your computer

This can be done by clicking the green button on the right titled "Clone or
download"

#### 3. Install our theme

Please go [here](https://squidfunk.github.io/mkdocs-material/) and install our
theme - material. 
The terminal command is `pip install mkdocs-material`

#### 4. In the terminal (command line) navigate to your local version of the specification

This location will have the same files you see on our
[main specification page](https://github.com/bids-standard/bids-specification).
Note: A finder window may not show the hidden files (those that start with a
period, like `.remarkrc`)

#### 5. Ready to build!

Using the terminal (command line) please enter `mkdocs serve`. 
This will allow you to see a local version of the specification. 
The local address will be `http://127.0.0.1:8000`. 
You may enter that into your browser and this will bring up the specification!

## Fixing Travis Remark errors

We use a linter called [Remarkjs](https://github.com/remarkjs/remark-lint) to
ensure all of our Markdown documents are consistent and well-styled. 
This commonly produces errors, which are flagged by [Travis CI](https://travis-ci.org/), 
a continuous integration service. 
When Travis returns an error, use the following process to resolve the issue:

#### 1. Install NodeJS / npm

We use a markdown linter written in Javascript. To run command Javascript tools
on the command line, please [download and install](https://nodejs.org/en/download/) 
NodeJS.

#### 2. Install Remark-CLI and our style guide

Remark-CLI can be installed via [npm](https://www.npmjs.com/), which is part of
the NodeJS distribution.

To install the packages we use for our style guide, the following command will
work on most command lines:

```
npm install `cat npm-requirements.txt`
```

The equivalent command on PowerShell is:

```
npm install @(cat npm-requirements.txt)
```

#### 3. Fix the flagged document

Please go to the directory where the flagged file is and run remark like this:

```
remark flagged_file.md -o flagged_file_fixed.md
```

Please confirm this has fixed the file. To do this, please run this:

```
remark flagged_file_fixed.md --frail
```

This command will indicate whether this file now conforms to the style guide. 
If it passes, replace `flagged_file.md` with the contents of
`flagged_file_fixed.md`, add and commit the change:

```
mv flagged_file_fixed.md flagged_file.md
git add flagged_file.md
git commit -m 'STY: Fixed Markdown style'
```

## Making a change with a pull request

We appreciate all contributions to the BIDS Specification. **THANK YOU** for
helping us build this useful resource.

#### 1. Comment on an existing issue or open a new issue referencing your addition

This allows other members of the BIDS Specification team to confirm that you
aren't overlapping with work that's currently underway and that everyone is on
the same page with the goal of the work you're going to carry out.

#### 2. [Fork](https://help.github.com/articles/fork-a-repo/) [this repository](https://github.com/bids-standard/bids-specification) to your profile

This is now your own unique copy of the BIDS Specification. 
Changes here won't affect anyone else's work, so it's a safe space to explore edits to the
specification!

Make sure to
[keep your fork up to date](https://help.github.com/articles/syncing-a-fork/)
with the master repository, otherwise you can end up with lots of dreaded
[merge conflicts](https://help.github.com/articles/about-merge-conflicts/).

#### 3. Make the changes you've discussed

Try to keep the changes focused. 
If you submit a large amount of work in all in one go it will be much more work 
for whomever is reviewing your pull request.
Please detail the changes you are attempting to make.

#### 4. Submit a [pull request](https://help.github.com/articles/about-pull-requests/)

Please keep the title of your pull request short but informative - it will
appear in the [changelog](src/CHANGES.md).

Use one of the following prefixes in the title of your pull request:

-   `[ENH]` - enhancement of the specification that adds a new feature or
    support for a new data type
-   `[FIX]` - fix of a typo or language clarification
-   `[INFRA]` - changes to the infrastructure automating the specification
    release (for example, building HTML docs)
-   `[MISC]` - everything else including changes to the file listing
    contributors

If you are opening a pull request to obtain early feedback, but the changes are
not ready to be merged (also known as a "work in progress" pull request, sometimes abbreviated by `WIP`)
please use a
[draft pull request](https://github.blog/2019-02-14-introducing-draft-pull-requests/).

A member of the BIDS Specification team will review your changes to confirm that
they can be merged into the main codebase.

A [review](https://help.github.com/articles/about-pull-request-reviews/) will
usually consist of a few questions to help clarify the work you've done. 
Keep an eye on your GitHub notifications and be prepared to join in that
conversation.

You can update your [fork](https://help.github.com/articles/about-forks/) of the
BIDS Specification and the pull request will automatically update with those
commits. 
You don't need to submit a new pull request when you make a change in
response to a review.

GitHub has a [nice introduction](https://help.github.com/articles/github-flow/)
to the pull request workflow, but please [get in touch](#get-in-touch) if you
have any questions.

## Example pull request

<img align="center" src="https://i.imgur.com/s8yELfK.png" alt="Example-Contribution" width="800"/>

## Commenting on a pull request

Our primary method of adding to or enhancing BIDS occurs in the form of
[pull requests](https://help.github.com/articles/about-pull-requests/). 
BIDS Extension Proposals
([BEPs](https://docs.google.com/document/d/1pWmEEY-1-WuwBPNy5tDAxVJYQ9Een4hZJM06tQZg8X4/))
are submitted as pull requests, and commenting on pull requests is an important
way of participating in the BIDS community.

This section outlines how to comment on a pull request.

### Navigating to open pull requests

The list of pull requests can be found by clicking on the "Pull requests" tab in
the
[BIDS-Specification repository](https://github.com/bids-standard/bids-specification).

![BIDS-mainpage](commenting_images/BIDS_GitHub_mainpage.png "BIDS_GitHub_mainpage")

### Selecting an open pull request

In this example we will be navigating to our
[BIDS common derivatives pull request](https://github.com/bids-standard/bids-specification/pull/265).

![BIDS-pr-list](commenting_images/BIDS_pr_list.png "BIDS_pr_list")

### Pull request description

Upon opening the pull request we see a detailed description of what this pull
request is seeking to address. 
Descriptions are important for reviewers and the community to gain context into 
what the pull request is achieving.

![BIDS-pr](commenting_images/BIDS_pr.png "BIDS_pr")

### Generally commenting on a pull request

At the bottom of the pull request page, a comment box is provided for general
comments and questions.

![BIDS-comment](commenting_images/BIDS_comment.png "BIDS-comment")

### Specific comments on a pull request

The proposed changes to the text of the specification can be seen in the "Files
changed" tab. 
Proposed additions are displayed on a green background with a `+`
before each added line. 
Proposed deletions are displayed on a red background with a `-` before each removed line. 
To comment on a specific line, hover over it, and click the blue plus sign (pictured below). 
Multiple lines can be selected by clicking and dragging the plus sign.

![BIDS-specific-comment](commenting_images/BIDS_file_comment.png "BIDS-specific-comment")

#### Suggesting text

Comments on lines can contain "suggestions", which allow you to propose specific
wording for consideration. To make a suggestion, click the plus/minus (±) icon
in the comment box (pictured below).

![BIDS-suggest-box](commenting_images/BIDS_suggest.png "BIDS-suggest")

Once the button is clicked the highlighted text will be copied into the comment
box and formatted as a
[Markdown code block](https://help.github.com/en/github/writing-on-github/creating-and-highlighting-code-blocks).

![BIDS-suggest-text](commenting_images/BIDS_suggest_text.png "BIDS-suggest-box")

The "Preview" tab in the comment box will show your suggestion as it will be
rendered. The "Suggested change" box will highlight the differences between the
original text and your suggestion.

![BIDS-suggest-change](commenting_images/BIDS_suggest_change.png "BIDS-suggest-change")

A comment may be submitted on its own by clicking "Add single comment". Several
comments may be grouped by clicking "Start a review". As more comments are
written, accept them with "Add review comment", and submit your review comments
as a batch by clicking the "Finish your review" button.

## Accepting suggestion from a review

When others are making [suggestions to your pull request](#suggesting-text), you
have the possibility to accept directly the changes suggested during the review
through the github interface. This can often be faster and more convenient than
make the changes locally and then pushing those changes to update your pull
request. Moreover it gives the opportunity to give credit to the reviewers for
their contribution.

To do this, you must click on the `Files changed` tab at the top of the page of
a pull request.

![BIDS_pr_files_changed](commenting_images/BIDS_pr_files_changed.png "BIDS_pr_files_changed")

From there you can browse the different files changed and the 'diff' for each of
them (what line was changed and what the change consist of). You can also see
comments and directly change suggestions made by reviewers.

You can add each suggestion one by one or group them together in a batch.

![BIDS_pr_accept_comment](commenting_images/BIDS_pr_accept_comment.png "BIDS_pr_accept_comment")

If you decide to batch the suggestions to add several of them at once, you must
scroll back to the top of the 'Files changed' page and the `commit suggestions`
button will let you add all those suggestions as a single commit.

![BIDS_pr_commit_batch](commenting_images/BIDS_pr_commit_batch.png "BIDS_pr_commit_batch")

Once those suggestions are committed the commit information should mention the
reviewer as a co-author.

![BIDS_pr_reviewer_credit](commenting_images/BIDS_pr_reviewer_credit.png "BIDS_pr_reviewer_credit")

## Updating the schema

Portions of the BIDS specification are defined using YAML files, in order to
make the specification machine-readable. 
Currently, the only portion of the specification that relies on this schema is 
the Entity Table, but any changes to the specification should be mirrored in the schema.

### The format of the schema

The schema reflects the files and objects in the specification, as well as
associations between these objects. 
Here is a list of the files and subfolders of the schema, roughly in order of importance:

-   `datatypes/*.yaml`: Data types supported by the specification. Each datatype
    may support many suffixes. 
    These suffixes are divided into groups based on what extensions and entities 
    are allowed for each. 
    Data types correspond to subfolders (for example, `anat`, `func`) in the BIDS structure.
-   `auxdatatypes/*.yaml`: Auxiliary (not directly imaging or data-containing)
    data types supported by the specification. 
    Each auxiliary data type is associated with a set of data types, 
    and these auxiliary data types are grouped based on what data types, 
    extensions, and entities are allowed for each. 
    Examples of auxiliary data types include `channels`, `electrodes`, and
    `photo`.
-   `entities.yaml`: A list of entities (key/value pairs in folder and
    filenames) with associated descriptions and formatting rules. 
    The order of the entities in the file determines the order in which entities 
    must appear in filenames.
-   `top_level_files.yaml`: Modality-agnostic files stored at the top level of a
    BIDS dataset. 
    The schema specifies whether these files are required or optional, 
    as well as acceptable extensions for each.
-   `modalities.yaml`: Modalities supported by the specification, along with a
    list of associated data types. 
    Modalities are not reflected directly in the BIDS structure, 
    but data types are modality-specific.
-   `associated_data.yaml`: Folders that are commonly contained within the same
    folder as a BIDS dataset, but which do not follow the BIDS structure
    internally, such as `code` or `sourcedata`. 
    The schema specifies which folders are accepted and whether they are required 
    or optional.

### Making a change to the schema

#### 1. Ensure that changes to the specification are matched in the schema

The schema formalizes the rules described in the specification text, so you must
ensure that any changes which impact the rules of the specification (including,
but not limited to, adding new entities, suffixes, datatypes, modalities) are
reflected in the schema as well.

#### 2. Generate an updated entity table before pushing your changes

Run the Python script `tools/bids_schema.py`:

```bash
python tools/bids_schema.py entity src/schema/ src/99-appendices/04-entity-table.md
```

#### 3. Push your changes

For more information on making general changes with a pull request, please
review
[Making a change with a pull request](#making-a-change-with-a-pull-request).

## How the decision to merge a pull request is made?

The decision-making rules are outlined in
[DECISION-MAKING.md](DECISION-MAKING.md).

## Recognizing contributions

BIDS follows the
[all-contributors](https://github.com/kentcdodds/all-contributors)
specification, so we welcome and recognize all contributions from documentation
to testing to code development. 
You can see a list of current contributors in the
[BIDS specification](https://github.com/bids-standard/bids-specification/blob/master/src/99-appendices/01-contributors.md).

If you have made any type of contributions to the BIDS specifications, you can
either make a change to the
[contributors document](./src/99-appendices/01-contributors.md) and commit as
part of a pull request or you can edit this
[page](https://github.com/bids-standard/bids-specification/wiki/Recent-Contributors)
of the specification WIKI. 
The WIKI is then synced with the specification with evert new release of the specifications.

## Thank you!

You're awesome.
