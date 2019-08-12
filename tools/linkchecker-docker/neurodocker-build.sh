#!/bin/bash

# A script to build docker image with desired patched linkchecker
# using neurodocker

# TODOs:
#   - minimize image (currently >500MB) using reprozip
#     see https://github.com/kaczmarj/neurodocker/#minimize-existing-docker-image
#     for instructions

# tag for patched linkchecker -- will also serve our image version
version="9.4.0.anchorfix1"
# docker image build
build=1

neurodocker generate docker \
    --base neurodebian:nd100 \
    --pkg-manager apt \
    --install python-pip python-requests python-dnspython python-setuptools python-wheel \
    --run "sed -e 's,^deb ,deb-src ,g' /etc/apt/sources.list > /etc/apt/sources.list.d/deb-sources.list \
    && apt-get update \
    && apt-get build-dep -y linkchecker \
    && pip install pyxdg https://github.com/yarikoptic/linkchecker/archive/$version.zip \
    && mkdir ~/.linkchecker && echo '[AnchorCheck]' > ~/.linkchecker/linkcheckerrc \
    " \
    --entrypoint /usr/local/bin/linkchecker \
| docker build -t yarikoptic/linkchecker:$version-$build -
