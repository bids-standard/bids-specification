File Format specification
=========================

All parts of a BIDS filename are considered case-sensitive. Thus `task-xyz_acq-test1_run-1_bold.json` and `task-xyz_acq-Test1_run-2_bold.json` will
be treated as having different acquisition labels by a BIDS validator or
should be treated as different by bids-aware libraries.
