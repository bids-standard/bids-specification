# Test inputs

This input directory contains data to use for testing the pdf build code of the BIDS specification.

For example the following admonition should be removed by `pdf_build_src/remove_admonitions.py`.

!!! note

    Lorem ipsum dolor sit amet, consectetur adipiscing elit.
    Nulla et euismod nulla.
    Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa,
    nec semper lorem quam in massa.

The `expected` directory should contain the documents
as they should look like after processing.
