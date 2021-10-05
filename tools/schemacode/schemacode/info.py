"""Base module variables."""
import importlib.util
import os.path as op
from pathlib import Path

# Get version
spec = importlib.util.spec_from_file_location(
    "_version", op.join(op.dirname(__file__), "schemacode/_version.py")
)
_version = importlib.util.module_from_spec(spec)
spec.loader.exec_module(_version)

VERSION = _version.get_versions()["version"]
del _version

# Get package description from README
# Since this file is executed from ../setup.py, the path to the README is determined by the
# location of setup.py.
readme_path = Path(__file__).parent.joinpath("README.md")
longdesc = readme_path.open().read()

# Fields
AUTHOR = "bids-standard developers"
COPYRIGHT = "Copyright 2021, bids-standard developers"
CREDITS = "bids-standard developers"
LICENSE = "LGPL 2.1"
MAINTAINER = ""
EMAIL = ""
STATUS = "Prototype"
URL = "https://github.com/bids-standard/schemacode"
PACKAGENAME = "schemacode"
DESCRIPTION = ""
LONGDESC = longdesc

DOWNLOAD_URL = "https://github.com/bids-standard/{name}/archive/{ver}.tar.gz".format(
    name=PACKAGENAME, ver=VERSION
)

REQUIRES = [
    "numpy",
    "pandas",
    "tabulate",
    "pyyaml",
]

TESTS_REQUIRES = [
    "codecov",
    "coverage<5.0",
    "flake8>=3.7",
    "flake8-black",
    "flake8-isort",
    "pytest",
    "pytest-cov",
]

EXTRA_REQUIRES = {
    "dev": ["versioneer"],
    "doc": [
        "sphinx>=1.5.3",
        "sphinx_rtd_theme",
    ],
    "tests": TESTS_REQUIRES,
}

ENTRY_POINTS = {}

# Enable a handle to install all extra dependencies at once
EXTRA_REQUIRES["all"] = list(set([v for deps in EXTRA_REQUIRES.values() for v in deps]))

# Supported Python versions using PEP 440 version specifiers
# Should match the same set of Python versions as classifiers
PYTHON_REQUIRES = ">=3.6"

# Package classifiers
CLASSIFIERS = [
    "Development Status :: 2 - Pre-Alpha",
    "Intended Audience :: Science/Research",
    "Topic :: Scientific/Engineering :: Information Analysis",
    "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]
