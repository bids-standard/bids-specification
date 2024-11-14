"""Module containing data files, including the schema source files

.. autofunction:: load_resource
"""

import atexit
import os
from contextlib import ExitStack
from functools import cached_property
from pathlib import Path
from types import ModuleType
from typing import Union

try:
    from functools import cache
except ImportError:  # PY38
    from functools import lru_cache as cache

try:  # Prefer backport to leave consistency to dependency spec
    from importlib_resources import as_file, files
except ImportError:
    from importlib.resources import as_file, files  # type: ignore

__all__ = ["load_resource"]


class Loader:
    """A loader for package files relative to a module

    This class wraps :mod:`importlib.resources` to provide a getter
    function with an interpreter-lifetime scope. For typical packages
    it simply passes through filesystem paths as :class:`~pathlib.Path`
    objects. For zipped distributions, it will unpack the files into
    a temporary directory that is cleaned up on interpreter exit.

    This loader accepts a fully-qualified module name or a module
    object.

    Expected usage::

        '''Data package

        .. autofunction:: load_data
        '''

        from bidsschematools.data import Loader

        load_data = Loader(__package__)

    :class:`~Loader` objects implement the :func:`callable` interface
    and generate a docstring, and are intended to be treated and documented
    as functions.
    """

    def __init__(self, anchor: Union[str, ModuleType]):
        self._anchor = anchor
        self.files = files(anchor)
        self.exit_stack = ExitStack()
        atexit.register(self.exit_stack.close)
        # Allow class to have a different docstring from instances
        self.__doc__ = self._doc

    @cached_property
    def _doc(self):
        """Construct docstring for instances

        Lists the public top-level paths inside the location, where
        non-public means has a `.` or `_` prefix or is a 'tests'
        directory.
        """
        top_level = sorted(
            os.path.relpath(p, self.files) + "/"[: p.is_dir()]
            for p in self.files.iterdir()
            if p.name[0] not in (".", "_") and p.name != "tests"
        )
        doclines = [
            f"Load package files relative to ``{self._anchor}``.",
            "",
            "This package contains the following (top-level) files/directories:",
            "",
            *(f"* ``{path}``" for path in top_level),
        ]

        return "\n".join(doclines)

    @cache
    def __call__(self, *segments) -> Path:
        """Ensure data is available as a :class:`~pathlib.Path`.

        Any temporary files that are created remain available throughout
        the duration of the program, and are deleted when Python exits.

        Results are cached so that multiple calls do not unpack the same
        data multiple times, but the cache is sensitive to the specific
        argument(s) passed.
        """
        return self.exit_stack.enter_context(as_file(self.files.joinpath(*segments)))


load_resource = Loader(__package__)
