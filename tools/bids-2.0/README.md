This directory to contain various little helpers which would script desired
automated changes (where possible) for migrating specification (not datasets)
to BIDS 2.0.  Ideally scripts should have some header pointing to the
underlying issue they are addressing.

## `apply_all`

`apply_all` script goes through `patches/` in a (numeric) sorted order
and applies those "patches".

"patches" could be of two types:

- an executable -- a script to be executed which introduces the changes.
- `.patch` - a regular patch which needs to be applied using `patch -p1`

Typically for the same leading index (e.g. `01`) there would be a script and
then a patch to possibly manually tune up remaining changes.

`apply_all` could also take an index -- then it would stop applying patches
having applied patches up to that index.
