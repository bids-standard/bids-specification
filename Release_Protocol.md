# Release Procedure

When it is time to release, use a pull request to put the repository into a releasable state,
allowing testing and edits prior to merging to master.
The following procedure ensures a predictable release.

The protocol assumes that you have a [fork](https://help.github.com/en/articles/fork-a-repo)
of the bids-standard/bids-specification repository and have [cloned](https://help.github.com/en/articles/cloning-a-repository)
your fork locally to a directory called `bids-specification`.

### 0. Cleaning up the changelog

Before you start a release, you have to ensure that the automatically generated changelog is **up to date**.
See the relevant [section in CONTRIBUTING.md](CONTRIBUTING.md#how-is-the-changelog-generated) for further information.
In practice this means ensuring that the most recently merged pull request
was merged into the `master` branch using the "Merge commit" option.

![merge-commit](release_images/merge_commit.png.png "merge-commit")

### 1. Fetch the latest version of the [master branch of the BIDS-specification](https://github.com/bids-standard/bids-specification/tree/master)

You should have a remote, which we will call `upstream`, for the
[bids-standard/bids-specification](https://github.com/bids-standard/bids-specification/)
repository:

```Shell
git remote get-url upstream
git@github.com:bids-standard/bids-specification.git
```

If you do not, add it with:

```Shell
cd bids-specification
git remote add upstream git@github.com:bids-standard/bids-specification.git
```

Fetch the current repository state and create a new `rel/<version>` branch based on
`upstream/master`.
For example, if releasing version `1.2.0`:

```Shell
git fetch upstream
git checkout -b rel/1.2.0 upstream/master
```

### 2. Update the version, contributors list, previous version URLs, and the Changelog

#### 2.1 Update the version

Update the version in CITATION.cff.

Change the "Unreleased" heading in
[src/CHANGES.md](https://github.com/bids-standard/bids-specification/blob/master/src/CHANGES.md)
to `<version>`, and link to the target ReadTheDocs URL.
If the target release date is known, include the date in YYYY-MM-DD in parentheses after
the link.

```Diff
- ## Unreleased
+ ## [1.2.0](https://bids-specification.readthedocs.io/en/1.2.0/) (2019-03-04)
```

The date can be changed or added later, so accurate prediction is not necessary.

Remove the `-dev` from the version in
[mkdocs.yml](https://github.com/bids-standard/bids-specification/blob/master/mkdocs.yml)
configuration, so the title will be correct for the released specification.
If the version preceding the `-dev` is not the target version, update the version as well.
In the figure below, we update `1.2.0-dev` to `1.2.0`.
![dev-to-stable](release_images/site_name_release_1.2dev-1.2.png "dev-to-stable")

Additionally, implement the same change in the version name perform above in the `src/schema/BIDS_VERSION` file.

Note:
this will make our continuous integration ([CircleCI](https://circleci.com/)) fail.
This fails because the URL of the new ReadTheDocs rendering has not been generated at this time.
It will be generated once the GitHub release has been completed.

#### 2.2 Update the contributors list

We want to ensure that all contributors are duly credited.

To synchronize the
[Contributors appendix](https://github.com/bids-standard/bids-specification/blob/master/src/appendices/contributors.md)
with the
[Contributors wiki page](https://github.com/bids-standard/bids-specification/wiki/Recent-Contributors),
please follow these steps:

- be sure not to remove credits if both the contributors appendix AND
  the contributors wiki page have been edited (or the `.tributors` or `.all-contributorsrc` files)
- add new contributors info to the `tools/new_contributors.tsv` file.
- make sure that you have installed
  - all the python packages listed in `tools/requirements.txt`
  - the [allcontributors](https://allcontributors.org/docs/en/cli/installation) package
- run:

```bash
make update_contributors
```

- you may need to fix some errors in the contributions names in case of crash
- make sure to review the changes and not commit them blindly
- commit the changes

#### 2.3 Update the previous version URLs

In `src/CHANGES.md`,
please change the previous version links from GitHub to ReadTheDocs.
In the figure below, we update 1.2.2.
![github-to-rtd](release_images/GitHub_to_RTD_spec_rendering.png "github-to-rtd")

#### 2.4 Update the Changelog

Review `src/CHANGES.md` to ensure that the document produces a changelog that is useful to a
reader of the specification.
For example, several small PRs fixing typos might be merged into a single line-item, or less
important changes might be moved down the list to ensure that large changes are more prominent.
You can also make use of the `exclude-from-changelog` label.
Adding this label to PRs in the GitHub web interface will prevent the changelog generator from
considering this item for inclusion in the changelog.

### 3. Commit changes and push to upstream

By pushing `rel/` branches to the main repository, the chances of continuous integration
discrepancies is reduced.

```Shell
git add src/CHANGES.md mkdocs.yml src/appendices/contributors.md src/schema/BIDS_VERSION
git commit -m 'REL: 1.2.0'
git push -u upstream rel/1.2.0
```

### 4. Open a pull request against the master branch

**Important notes:**

1. The pull request title **must** be named "REL: X.Y.Z" (for example, "REL: 1.2.0")
1. The pull request **must** get a GitHub label called `exclude-from-changelog`

**This will open a period of discussion for 5 business days regarding if we are ready to release.**

Minor revisions may be made using GitHub's
[suggestion feature](https://help.github.com/en/articles/incorporating-feedback-in-your-pull-request).
For larger changes, pull requests should be made against `master`.

**Merging other pull requests during this period requires agreement among BIDS Maintainers.**

There are no hard-and-fast rules for what other pull requests might be merged, but the focus
should generally be on achieving a self-consistent, backwards-compatible document.
For example, if an inconsistency is noticed, a PR might be necessary to resolve it.
Merging an entire BEP would likely lead to greater uncertainty about self-consistency, and should
probably wait.

If `master` is updated, it should be merged into the `rel/<version>` branch:

```Shell
git fetch upstream
git checkout rel/1.2.0
git merge upstream/master
git push rel/1.2.0
```

### 5. Set release date and merge

On the day of release, please ensure the release branch aligns with the master branch.
The current date should be added to/updated in the changelog in the form
YYYY-MM-DD.
The date should be placed after the link to the versioned URL.
For example:

```Diff
- ## [1.2.0](https://bids-specification.readthedocs.io/en/1.2.0/)
+ ## [1.2.0](https://bids-specification.readthedocs.io/en/1.2.0/) (2019-03-04)
```

Verify that the pull request title matches "REL: X.Y.Z" and merge the pull request.

### 6. Get the built PDF and `CITATION.cff` file

Upon each commit to the `master` branch, CircleCI builds a PDF version of the
specification (see `.circleci/config.yml` and the `pdf_build_src` directory).

So after merging the new "stable" version into `master`, wait for the CircleCI
jobs to finish and then check the built PDF using the following steps:

1. Go to the [list of recent commits](https://github.com/bids-standard/bids-specification/commits/master)
1. Click on the "CI checks" for the most recent commit (should be a green checkmark)
1. From the list of CI checks, click on the one called: `Check the rendered PDF version here!`
1. Download the PDF and check that the date and version on the first page are as expected
1. Hold the PDF ready for upload to our Zenodo archive (see the *Uploading the stable PDF to Zenodo* step below)

Furthermore, **copy the `CITATION.cff`** file in its current state from the root of the repository
and hold it ready for facilitating the upload of the PDF to our Zenodo archive.

### 7. Tag the release

GitHub's release mechanism does not have all of the features we need, so manually tag the release
in your local repository.
To do this, `fetch` the current state of `upstream` (see step 1), tag `upstream/master`, and
`push` the tag to `upstream`.

```Shell
git fetch upstream
git tag -a -m "1.2.0 (2019-03-04)" 1.2.0 upstream/master
git push upstream 1.2.0
```

There are four components to the tag command:

1. `-a-` indicates that we want to use an
   [annotated tag](https://git-scm.com/book/en/v2/Git-Basics-Tagging#_creating_tags), which will
   ensure that [`git describe`](https://git-scm.com/docs/git-describe) works nicely with the
   repository.
2. `-m <message>` is the message that will be saved with the tag.
3. `v<version>` is the name of the release and the tag.
4. `upstream/master` instructs `git` to tag the most recent commit on the `master` branch of the
   `upstream` remote.

### 8. Create a GitHub release

Some GitHub processes may only trigger on a GitHub release, rather than a tag push.
To make a GitHub release, go to the
[Releases](https://github.com/bids-standard/bids-specification/releases) page:
![GH-release-1](release_images/GH-release_1.png "GH-release-1")

Click [Draft a new release](https://github.com/bids-standard/bids-specification/releases/new):

![GH-release-2](release_images/GH-release_2.png "GH-release-2")

Set the tag version and release title to "X.Y.Z", and paste the current changelog as the
description:

![GH-release-3](release_images/GH-release_3.png "GH-release-3")

Click "Publish release".

Verify ReadTheDocs builds complete and publish. If needed, manually
trigger [builds](https://readthedocs.org/projects/bids-specification/builds/)
for `stable` and the most recent tag.

### 9. Edit the mkdocs.yml file site_name to set a new development version

Please open a pull request and create a merge commit to `master` with the title `REL: <version>-dev`.

![merge-commit](release_images/merge_commit.png.png "merge-commit")

This should be the first commit in the new version.

This will reset the URLs that were [manually changed before in step 2.3](#2.3-update-the-previous-version-URLs).

This process is illustrated below.

![stable-to-dev](release_images/site_name_release_1.2-1.3dev.png "stable-to-dev")

Note that the development version number should be larger than the last release, with the
version of the next *intended* release, followed by `-dev`.
For example, after the 1.3.0 release, either `1.3.1-dev` or `1.4.0-dev` would be reasonable, based
on the expected next version.

Additionally, the same version name set above in `mkdocs.yaml` should be set in the `src/schema/BIDS_VERSION` schema version file.

Similarly update the version in CITATION.cff with a `dev` suffix.

### 10. Uploading the stable PDF to Zenodo

1. In a previous step you have secured a PDF version of the BIDS specification and the corresponding `CITATION.cff` file.
1. Follow the steps described here: https://github.com/bids-standard/bids-specification-pdf-releases#release-instructions

### 11. Update the BIDS website data

Update the following files in the BIDS website repository (https://github.com/bids-standard/bids-website) if applicable:

- `tools/timeline.csv`
- `_data/beps.yml`
- `_data/beps_completed.yml`
- `_data/beps_other.yml`

### 12. Sharing news of the release

Please share news of the release on the [identified platforms](https://docs.google.com/spreadsheets/d/16SAGK3zG93WM2EWuoZDcRIC7ygPc5b7PDNGpFyC3obA/edit#gid=0).
Please use our previous release posts as a guide.
