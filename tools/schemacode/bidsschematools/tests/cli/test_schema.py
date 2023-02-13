import json
import os
import subprocess


def test_export(tmp_path):
    out_file = os.path.join(tmp_path, "schema.json")
    # Does it work?
    subprocess.check_output(["bst", "export", out_file])
    # Does it produce a valid JSON file?
    with open(out_file) as f:
        _ = json.load(f)
