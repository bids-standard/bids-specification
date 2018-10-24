
# Contributing to the BIDS Specification

**Welcome to the BIDS Specification repository!**

*We're so excited you're here and want to contribute.*

We hope that these guidelines are designed to make it as easy as possible to get involved. If you have any questions that aren't discussed below, please let us know through one of the many ways to [get in touch](#get-in-touch).

## Table of contents

Been here before? Already know what you're looking for in this guide? Jump to the following sections:

*   [Joining the BIDS community](#joining-the-community)
*   [Get in touch](#get-in-touch)
*   [Contributing through GitHub](#contributing-through-github)
*   [Writing in markdown](#writing-in-markdown)
*   [Make a change with a pull request](#making-a-change-with-a-pull-request)
*   [Example pull request](#example-pull-request)
*   [Recognizing contributions](#recognizing-contributions)

## Joining the community

BIDS - the [Brain Imaging Data Structure](http://bids.neuroimaging.io/) - is a growing community of neuroimaging enthusiasts, and we want to make our resources accessible to and engaging for as many researchers as possible.

We therefore require that all contributions **adhere to our [Code of Conduct](CODE_OF_CONDUCT.md)**.

How do you know that you're a member of the BIDS community? You're here! You know that BIDS exists! You're officially a member of the community. It's THAT easy! Welcome!

## Get in touch

## Contributing through GitHub

[Git](https://git-scm.com/) is a really useful tool for version control. [GitHub](https://github.com/) sits on top of git and supports collaborative and distributed working.

We know that it can be daunting to start using git and GitHub if you haven't worked with them in the past, but the BIDS Specification maintainers are here to help you figure out any of the jargon or confusing instructions you encounter!

In order to contribute via GitHub you'll need to set up a free account and sign in. Here are some [instructions](https://help.github.com/articles/signing-up-for-a-new-github-account/) to help you get going. Remember that you can ask us any questions you need to along the way.

## Writing in markdown

The specification documents follow the [Markdown Style Guide](http://www.cirosantilli.com/markdown-style-guide/).

You
can validate your changes against the guide using [remark](https://github.com/remarkjs/remark-lint) which works as a
[standalone command line tool](https://github.com/remarkjs/remark/tree/master/packages/remark-cli) as well as [a plugin for various text editors](https://github.com/remarkjs/remark-lint#editor-integrations). Remark preserves consistent markdown styling across the contributions. Please ensure before submitting a contribution that you do not have any linter errors in your text editor.
You can also use [prettier](https://github.com/prettier/prettier) to automatically correct some of the style issuse that might be found in the proposed changes.

We have deployed a continous integrator ([circle CI](https://circleci.com/)) to further allow for integrating changes continously. The CI is testing that the changes are inline with our standard styling.

GitHub has a helpful page on [getting started with writing and formatting on GitHub](https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github).

## Building the specification using mkdocs

We are using mkdocs to render our specification. Please follow these instructions if you would like to build the specification locally.

#### 1. Install mkdocs

To begin please follow [this link](https://www.mkdocs.org/#installation) to install mkdocs locally.

#### 2. Download the BIDS specification [repository](https://github.com/bids-standard/bids-specification/tree/master) onto your computer

This can be done by clicking the green button on the right titled "Clone or download"

#### 3. Install our theme

Please go [here](https://squidfunk.github.io/mkdocs-material/) and install our theme - material. The terminal command is `pip install mkdocs-material`

#### 4. In the terminal (command line) navigate to your local version of the specification

This location will have the same files you see on our [main specification page](https://github.com/bids-standard/bids-specification). Note: A finder window may not show the hidden files (those that start with a period i.e. .remarkrc)

#### 5. Ready to build!

Using the terminal (command line) please enter `mkdocs serve`. This will allow you to see a local version of the specification. The local address will be `http://127.0.0.1:8000`. You may enter that into your browser and this will bring up the specification!

## Making a change with a pull request

We appreciate all contributions to the BIDS Specification. **THANK YOU** for helping us build this useful resource.

#### 1. Comment on an existing issue or open a new issue referencing your addition

This allows other members of the BIDS Specification team to confirm that you aren't overlapping with work that's currently underway and that everyone is on the same page with the goal of the work you're going to carry out.


#### 2. [Fork](https://help.github.com/articles/fork-a-repo/) [this repository](https://github.com/bids-standard/bids-specification) to your profile

This is now your own unique copy of the BIDS Specification. Changes here won't affect anyone else's work, so it's a safe space to explore edits to the specification!

Make sure to [keep your fork up to date](https://help.github.com/articles/syncing-a-fork/) with the master repository, otherwise you can end up with lots of dreaded [merge conflicts](https://help.github.com/articles/about-merge-conflicts/).

#### 3. Make the changes you've discussed

Try to keep the changes focused. If you submit a large amount of work in all in one go it will be much more work for whomever is reviewing your pull request. Please detail the changes you are attempting to make.

#### 4. Submit a [pull request](https://help.github.com/articles/about-pull-requests/)

A member of the BIDS Specification team will review your changes to confirm that they can be merged into the main codebase.

A [review](https://help.github.com/articles/about-pull-request-reviews/) will probably consist of a few questions to help clarify the work you've done. Keep an eye on your github notifications and be prepared to join in that conversation.

You can update your [fork](https://help.github.com/articles/about-forks/) of the BIDS Specification and the pull request will automatically update with those commits. You don't need to submit a new pull request when you make a change in response to a review.

GitHub has a [nice introduction](https://help.github.com/articles/github-flow/) to the pull request workflow, but please [get in touch](#get-in-touch) if you have any questions.

## Example pull request
<img align="right" src="https://i.imgur.com/s8yELfK.png" alt="Example-Contribution"/>

<br>

<br>

## Recognizing contributions

BIDS follows the [all-contributors](https://github.com/kentcdodds/all-contributors) specification, so we welcome and recognize all contributions from documentation to testing to code development. You can see a list of current contributors in the [BIDS specification](https://github.com/bids-standard/bids-specification/blob/master/src/99-appendices/01-contributors.md).

## Thank you!

You're awesome.
