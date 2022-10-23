#!/bin/bash
# Shell script that runs process_markdowns.py and pandoc_script.py in sequence to build the pdf document

set -eu

# prepare the copied src directory
echo "Running: process_markdowns.py"
python3 process_markdowns.py

# copy pandoc_script into the temp src_copy directory
echo "Running: copying files to src_copy/src"
cp pandoc_script.py header.tex cover.tex header_setup.tex src_copy/src

# run pandoc_script from src_copy directory
echo "Running: cd to src_copy/src and run pandoc_script.py"
pushd src_copy/src
python3 pandoc_script.py

echo "Running: Moving built spec PDF and log JSON to pdf_build_src"
mv bids-spec.pdf ../..
mv bids-spec_pandoc_log.json ../..
popd

# Do a check on the pandoc log file
echo "Running: check_pandoc_log.py"
python3 check_pandoc_log.py

# delete the duplicated src directory
echo "Running: remove unneeded src_copy directory"
rm -rf src_copy
