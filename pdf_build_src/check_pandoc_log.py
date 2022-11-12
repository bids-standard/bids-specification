"""Inspect the pandoc log for warnings that should be raised as errors."""

# %%
import json

# see pandoc_script.py
LOGFILE = "bids-spec_pandoc_log.json"

# read the log file
with open(LOGFILE, "r") as fin:
    logs = json.load(fin)

# go through the logs (list of dicts)
duplicate_link_refs = []
for log_dict in logs:

    # Check for DuplicateLinkReference
    logtype = log_dict.get("type", None)
    logverbosity = log_dict.get("verbosity", None)

    if logtype == "DuplicateLinkReference" and logverbosity == "WARNING":
        duplicate_link_refs.append(log_dict)

# raise errors if appropriate
if len(duplicate_link_refs) > 0:
    msg = "\n\nFound duplicate link references. Please make them unique.\n"
    for log_dict in duplicate_link_refs:
        msg += "\n" + json.dumps(log_dict, indent=4)
    raise RuntimeError(msg)
