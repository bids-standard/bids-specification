"""Test data module

.. autofunction:: load_test_data

.. automethod:: load_test_data.readable

.. automethod:: load_test_data.as_path

.. automethod:: load_test_data.cached
"""

from acres import Loader

__all__ = ("load_test_data",)

load_test_data = Loader(__spec__.name)
