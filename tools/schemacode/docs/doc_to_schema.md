---
jupytext:
  formats: md:myst
  text_representation:
    extension: .md
    format_name: myst
    format_version: 0.13
    jupytext_version: 1.17.2
kernelspec:
  name: python3
  display_name: Python 3 (ipykernel)
  language: python
---

+++ {"editable": true, "slideshow": {"slide_type": "slide"}}

# Translating a BEP Document into Schema Code

One of the most important steps of a BEP is translating it from a plain text (google/microsoft document) as
a yaml schema.

Following this step one will be able to:

1) render the spec into its [ultimate markdown form](https://bids-specification.readthedocs.io/en/stable/)
2) apply and validate the new rules and requirements introduced by the BEP
3) merge their BEP into the BIDS Spec

For the purpose of this guide we'll be referencing a completed BEP starting from its initial Google doc form
and finishing with it's translation into schema.

## The Google Doc

blah