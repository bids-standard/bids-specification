# pdf-version of BIDS specification 

The `pdf_build_src` directory contains the scripts and tex files required to build a pdf document of the BIDS specification from multiple markdown files using the pandoc library. 

Pandoc is command line tool which is also a Haskell library that converts files from one markup format to another. More here: https://pandoc.org/index.html

## Requirements

For the pdf build to be successful, the following need to be installed: 

- Python 3.x 
- pandoc 
- Latest version of LaTeX: By default, Pandoc creates PDFs using LaTeX. Because a full MacTeX installation uses four gigabytes of disk space, pandoc recommends BasicTeX or TinyTeX and using the tlmgr tool to install additional packages as needed. 

Installation instructions for both pandoc and LaTeX: https://pandoc.org/installing.html

## Building pdf document

Run the `build_pdf.sh` from the `pdf_build_src` with the command `sh build_pdf.sh` from the command line terminal 

List of warnings are for missing characters like emojis while converting from markdown to pdf. Except for losing those characters in the final document, it doesn't affect the formatting or contents and therefore, can be ignored.

## Technical Overview

Pandoc comes with a plethora of options to format the resulting document. For building a pdf from multiple markdowns, a consolidated intermediate tex file is first built, which is then converted to a pdf document. To achieve the desired formatting in the final pdf, additional tex files are used with options offered by pandoc. 

### Formatting files

`listings_setup.tex` -  Listings is a LaTeX package used for typestting programming code in TeX. This file sets up the listings package to suit our needs and is used with the `--listings` option. 

`cover.tex` - BIDS Logo is used as a cover page for the document. `cover.tex` is used with the option `--include-before-body`

`header.tex` - Header tex file that's updated with the latest version number and date when `build_pdf.sh` is run. Used with the `-H` header option. 

### Scripts

`process_markdowns.py` - Script that processes markdown files in the `src` directory that are duplicated and modified for the needs of the pdf. 

`pandoc_script.py` - Prepares and runs the final pandoc command through the `build_pdf.sh` script

`build_pdf.sh` - Shell script that organizes the directory structure and runs the above two python scripts
