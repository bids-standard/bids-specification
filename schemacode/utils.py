"""
Utility functions for the bids-specification schema.
"""
import os.path as op


def get_schema_path():
    return op.abspath(
        op.join(
            op.dirname(op.dirname(__file__)),
            "src",
            "schema"
        ) + op.sep
    )
