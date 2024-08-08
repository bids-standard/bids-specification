"""Test data module

.. autofunction:: load_test_data
"""

from ...data import Loader

__all__ = ("load_test_data",)

load_test_data = Loader(__package__)
