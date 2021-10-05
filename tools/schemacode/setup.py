#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" schemacode setup script """


def main():
    """ Install entry-point """
    import os.path as op
    from inspect import currentframe, getfile
    from io import open

    from setuptools import find_packages, setup

    import versioneer

    ver_file = op.join("schemacode", "info.py")
    with open(ver_file) as f:
        exec(f.read())
    vars = locals()

    root_dir = op.dirname(op.abspath(getfile(currentframe())))
    cmdclass = versioneer.get_cmdclass()

    pkg_data = {
        "schemacode": [
            "tests/data/*",
        ]
    }

    setup(
        name=vars["PACKAGENAME"],
        version=vars["VERSION"],
        description=vars["DESCRIPTION"],
        long_description=vars["LONGDESC"],
        long_description_content_type="text/markdown",
        author=vars["AUTHOR"],
        author_email=vars["EMAIL"],
        maintainer=vars["MAINTAINER"],
        maintainer_email=vars["EMAIL"],
        url=vars["URL"],
        license=vars["LICENSE"],
        classifiers=vars["CLASSIFIERS"],
        download_url=vars["DOWNLOAD_URL"],
        # Dependencies handling
        python_requires=vars["PYTHON_REQUIRES"],
        install_requires=vars["REQUIRES"],
        tests_require=vars["TESTS_REQUIRES"],
        extras_require=vars["EXTRA_REQUIRES"],
        entry_points=vars["ENTRY_POINTS"],
        packages=find_packages(exclude=("tests",)),
        zip_safe=False,
        cmdclass=cmdclass,
    )


if __name__ == "__main__":
    main()
