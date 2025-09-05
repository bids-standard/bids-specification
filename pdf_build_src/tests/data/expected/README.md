# Test inputs

This input directory contains data to use for testing the pdf build code of the BIDS specification.

For example the following admonition should be removed by `pdf_build_src/remove_admonitions.py`.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Nulla et euismod nulla.
Curabitur feugiat, tortor non consequat finibus, justo purus auctor massa,
nec semper lorem quam in massa.

The `expected` directory should contain the documents
as they should look like after processing.

[Mkdocs admonitions](https://squidfunk.github.io/mkdocs-material/reference/admonitions/#inline-blocks-inline-end)
come in different type. In aaddtion of the classical admonitions show above you have also:

Collapsible admonitions start with 3 questions marks (`???`).

Collapsible admonitions that will be shown as expanded
start with 3 questions marks and a plus sign (`???+`).



Let's see

-   [`UK biobank`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)
-   foo bar [`UK biobank`](https://github.com/bids-standard/bids-examples/tree/master/genetics_ukbb)

More of the admonition

And here we resume normal thing.
