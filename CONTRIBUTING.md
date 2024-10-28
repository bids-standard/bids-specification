# Contributing to the BIDS Specification

**Welcome to the BIDS Specification repository!**

_We're so excited you're here and want to contribute._

We hope that these guidelines are designed to make it as easy as possible to get involved.
If you have any questions that aren't discussed below, please let us know
by [opening an issue](https://github.com/bids-standard/bids-specification/issues/new).

If you are not familiar with Git ansd GitHub,
check our [generic contributing guidelines](https://bids-website.readthedocs.io/en/latest/collaboration/bids_github/CONTRIBUTING.html).

If you want to contribute to the BIDS website,
make sure you also read the instructions below.

## Table of contents

Been here before?
Already know what you're looking for in this guide?
Jump to the following sections:

## Writing in Markdown

The specification documents follow the
[Markdown Style Guide](http://www.cirosantilli.com/markdown-style-guide/).

You can validate your changes against the guide using
[remark](https://github.com/remarkjs/remark-lint) which works as a
[standalone command line tool](https://github.com/remarkjs/remark/tree/master/packages/remark-cli)
as well as
[a plugin for various text editors](https://github.com/remarkjs/remark-lint#editor-integrations).
Remark preserves consistent Markdown styling across the contributions.
Please ensure before submitting a contribution that you do not have any linter errors
in your text editor.

We have deployed a continuous integrator ([circle CI](https://circleci.com/)) to
further allow for integrating changes continuously.
The CI is testing that the changes are inline with our standard styling.

GitHub has a helpful page on
[getting started with writing and formatting on GitHub](https://help.github.com/articles/getting-started-with-writing-and-formatting-on-github).

### Style guide

There are certain style rules we are trying to follow in the way the specifications are written.

Many of those styling issues can fixed automatically using a linter: see
the section [Fixing Remark errors from Travis](#fixing-travis-remark-errors).

Some others need to fixed manually:

- Do not use Latin abbreviations like `"e.g"`, `"i.e"`, `"etc"` that can be confusing
  to some readers and try to replace them by common English equivalents such as
  `"for example"`, `"that is"`, `"and so on"`.

The BIDS specification is written in American English.

#### Soft rules

We follow certain "soft rules" in the way we format the specification in Markdown.

These rules are sometimes for internal consistency in terms of styling and esthetics,
but several of them are also there because they help the workflow of
tracking changes, reviewing them on GitHub, and making code suggestions.

They are "soft" rules because they will not be a reason to reject a contribution
but if they are followed they will definitely make the lives of many people easier.

- Start every sentence on a new line.
  This then makes it easier to track with git where a change happened in the text.

- Similarly try to use "hard word wrapping": if a sentence gets long and extends
  a line length beyond 80-100 characters, continue the sentence on the next line.

**Example**

Don't do this:

```Markdown
Unprocessed MEG data MUST be stored in the native file format of the MEG instrument with which the data was collected. With the MEG specification of BIDS, we wish to promote the adoption of good practices in the management of scientific data.
```

But do this:

```Markdown
Unprocessed MEG data MUST be stored in the native file format of the MEG instrument
with which the data was collected.
With the MEG specification of BIDS, we wish to promote the adoption of good practices
in the management of scientific data.
```

- when providing a string example for a specific JSON key name make sure that this
  example appears with double quotes as it would in the real JSON file.

**Example**

Don't do this:

```Markdown
| **Key name** | **Description**                                          |
| ------------ | -------------------------------------------------------- |
| Manufacturer | Manufacturer of the equipment, for example (`Siemens`)   |
```

That would look like this:

| **Key name** | **Description**                                          |
| ------------ | -------------------------------------------------------- |
| Manufacturer | Manufacturer of the equipment, for example (`Siemens`)   |

But do this instead:

```Markdown
| **Key name** | **Description**                                          |
| ------------ | -------------------------------------------------------- |
| Manufacturer | Manufacturer of the equipment, for example (`"Siemens"`) |
```

That would look like this:

| **Key name** | **Description**                                          |
| ------------ | -------------------------------------------------------- |
| Manufacturer | Manufacturer of the equipment, for example (`"Siemens"`) |


### MkDocs admonitions

It is possible to use [Mkdocs admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#inline-blocks-inline-end)
to highlight certain aspect of the specification.

Admonitions are written like this:

````
!!! note "displayed heading is preceded by a keyword and 3 `!`"

    Body of the admonition
    can be written on several lines,
    but must be always preceded by 4 spaces.
````

The keyword for the heading must be one of the following:

- note
- abstract
- info
- tip
- success
- question
- warning
- failure: octicons
- danger
- bug
- example
- quote

Do not put [macros](#using-macros) in admonitions,
as this will likely not give the output you expect.

## Using macros

We use [mkdocs-macros](https://mkdocs-macros-plugin.readthedocs.io/en/latest/)
to standardize how some aspects of the BIDS specification are rendered in HTML.

We have dedicated documentation for this, see the [macros_doc.ms](./macros_doc.md) file.

## Building the specification using MkDocs

We are using MkDocs to render our specification.
Please follow these instructions if you would like to build the specification locally.

### 1. Download the BIDS specification [repository](https://github.com/bids-standard/bids-specification/tree/master) onto your computer

This can be done by clicking the green button on the right titled "Clone or
download"
or using [this link](https://github.com/bids-standard/bids-specification/archive/master.zip).

Or you can use the following `git` command in a terminal:

```bash
git clone https://github.com/bids-standard/bids-specification.git
```

### 2. In the terminal (command line) navigate to your local version of the specification

This location will have the same files you see on our
[main specification page](https://github.com/bids-standard/bids-specification).
Note that a file browser window may not show the hidden files
(those that start with a period, like `.remarkrc`).

If you cloned the repository using the `git` command above, you can then just do:

```bash
cd bids-specification
```

Enter all commands below from the command line prompt located at the root of the local version of the specification.

### 3. Install MkDocs, the Material theme and the required extensions

In the following links, you can find more information about

- [MkDocs](https://www.mkdocs.org/#installation) and how to install it locally,
- [the Material theme](https://squidfunk.github.io/mkdocs-material/) we use.

You will also need several other MkDocs plugins, like `branchcustomization` and `macros`.

To install all of this make sure you have a recent version of Python on your computer.
The [DataLad Handbook](http://handbook.datalad.org/en/latest/intro/installation.html#python-3-all-operating-systems) provides helpful instructions for setting up Python.

In general, we strongly recommend that you install all dependencies in an isolated Python environment.
For example using `conda`, as described in this [Geohackweek tutorial](https://geohackweek.github.io/Introductory/01-conda-tutorial/).

```bash
conda create --name bids-spec
conda activate bids-spec
```

Or alternatively using `venv`, as described in this [Real Python tutorial](https://realpython.com/python-virtual-environments-a-primer/).

A short version of the commands needed to create and activate your `venv` virtual environment would look like:

```bash
python -m venv env
source env/bin/activate
```

Note that this will create a local directory called `env` within the bids-specification directory
but that its content will not be tracked by `git` because it is listed in the `.gitignore` file.

Once you have activated your isolated Python environment,
an easy way to install the correct version of MkDocs and all the other required extensions
is to use the `requirements.txt` file contained in this repository as follows:

```bash
pip install -U pip
pip install -r requirements.txt
```

The first command ensures you are using an up to date version of `pip`,
and the second command installs all dependencies.
The third command ensures to install the BIDS schema code as an "editable" install,
so that if you make changes to the schema files,
these are automatically reflected in the sourcecode.

Note that if you need to work on the some of the Python code
that is used to render the specification,
you will probably have to also run:

```bash
pip install -e tools/schemacode[render]
```

This installs the `bidsschemacode` package in "editable" mode,
so that any changes you make to the code will be reflected when you use it,
such as when you build the documentation locally.

### 4. Ready to build!

Using the terminal (command line) please enter `mkdocs serve`.
This will allow you to see a local version of the specification.
The local address will be `http://127.0.0.1:8000`.
You may enter that into your browser and this will bring up the specification!

## Fixing Markdown style errors

We use a linter called [Remarkjs](https://github.com/remarkjs/remark-lint) to
ensure all of our Markdown documents are consistent and well-styled.
This commonly produces errors, which are flagged by [GitHub Actions](https://github.com/features/actions),
a continuous integration service.
When GitHub Actions returns an error, use the following process to resolve the issue:

### 1. Install NodeJS / npm

We use a Markdown linter written in Javascript. To run command Javascript tools
on the command line, please [download and install](https://nodejs.org/en/download/)
NodeJS.

### 2. Install Remark-CLI and our style guide

Remark-CLI can be installed via [npm](https://www.npmjs.com/), which is part of
the NodeJS distribution.

To install the packages we use for our style guide, the following command will
work on most command lines:

```shell
npm install `cat npm-requirements.txt`
```

The equivalent command on PowerShell is:

```shell
npm install @(cat npm-requirements.txt)
```

### 3. Find documents that are failing the check

Run the following from the root directory of `bids-specification`:

```shell
npx remark ./src/*.md ./src/*/*.md
```

### 4. Fix the flagged document

Please go to the directory where the flagged file is and run remark like this:

```shell
npx remark flagged_file.md -o flagged_file_fixed.md
```

Please confirm this has fixed the file. To do this, please run this:

```shell
npx remark flagged_file_fixed.md --frail
```

This command will indicate whether this file now conforms to the style guide.
If it passes, replace `flagged_file.md` with the contents of
`flagged_file_fixed.md`, add and commit the change:

```shell
mv flagged_file_fixed.md flagged_file.md
git add flagged_file.md
git commit -m 'STY: Fixed Markdown style'
```

NOTE:

Using `remark` to fix some linting errors might introduce some additional changes:

- changing unordered list from using `-` to using `*`
- changing ordered list from using `1.` to actually using the number of the item
- changes literal hyperlinks URLs from `[URL](URL)` to `<URL>`
- in some instances, it will "escape" all `_` and `&` with a `\` in all the URLs.

You might have to revert those or use [interactive staging](https://git-scm.com/book/en/v2/Git-Tools-Interactive-Staging) to make sure you only commit the right chunks of code.

## Adding a figure to the specifications

> A figure is worth a 1000 words!

If you think that a figure or a picture can help summarize several aspects or notions of the
specification, do not hesitate to make a suggestion by showing a draft in a GitHub issue.

After discussion and approval by the community, you can then submit your image
in a pull request.

Images should be added to an `images` directory that is at the same level as the Markdown file
where your image will be added. For example if you want to add a figure `figure01.png` to
`src/05-derivatives/01-introduction.md` then your image should go to
`src/05-derivatives/images/figure01.png`.

Figures can be inserted in a Markdown like this (see also
[Markdown-Cheatsheet](https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet#images)):

```Markdown
![text to show if image does not load](relative_path_to_file "text to show when hovering over image")
```

### Recommendations for figures

1. Try to keep the file size of your figure relatively small (smaller than 500 Kb)
to keep the repository light and reduce the load time of the specs
for people who do not necessarily have broad-band internet.

1. Figures in the main part of the specification should aim to be very "comprehensive"
but "smaller" figures can find their home in the appendices or the BIDS-starter-kit.

1. If you are adding a figure (and not picture) make sure to also supply a vector format
of that figure (ideally as an `.svg` file) as this makes it easier to edit it in the
future.

1. Try to include a README file that details where the figure / image came from
and how it can be reproduced. Preferably with a link to the file that generated the figure
if relevant.

## Making a change to the BIDS-schema

Several aspects of the specification are defined in a set of YAML files in the
`src/schema` directory. The content of those files is described in a dedicated
[README file](./src/schema/README.md).

### 1. Ensure that changes to the specification are matched in the schema

The schema formalizes the rules described in the specification text, so you must
ensure that any changes which impact the rules of the specification (including,
but not limited to, adding new entities, suffixes, datatypes, modalities) are
reflected in the schema as well.

### 2. Ensure that changes to the schema are matched in auto-generated sections of the specification

The schema is used to generate a number of elements in the specification text, including:

- Filename format templates
- Entity tables
- Entity definitions

As such, you need to ensure that the functions used throughout the specification to render these elements are appropriately referencing the schema.
In essence, please make sure, if your changes do impact how functions should be called, that you also update how the function are called.

### 3. Render the specification with `mkdocs` to check your changes

Run `mkdocs serve` and open `localhost:8000` to browse the rendered specification.
Make sure that all filename format templates, entity tables, and entity definitions are correct
and that the code that generates these elements is not broken by your changes.

While the continuous integration run on pull requests by the repository will render the specification,
it is crucial to manually review the rendered changes to ensure that the code not only successfully runs,
but also that the rendered changes appear as expected.

## How is the decision to merge a pull request made?

The decision-making rules are outlined in
[DECISION-MAKING.md](DECISION-MAKING.md).

## How is the changelog generated?

The changelog (see `src/CHANGES.md`) is generated automatically using
[github-changelog-generator](https://github.com/github-changelog-generator/github-changelog-generator).
You can see the workflow in the following GitHub Actions configuration file: `.github/workflows/changelog_generator.yml`.

This workflow is triggered for every commit to `master` that contains string `[build changelog]` in its commit message.
If you push several commits at once, you need to make sure that the "youngest commit" (the HEAD commit) contains that string.
The workflow will then open a Pull Request to incorporate the updated changelog.
Check the proposed changes and merge the Pull Request at will.

To exclude pull requests from showing up in the changelog, they have to be labeled with
the "exclude-from-changelog" label.

## Thank you!

You're awesome.
