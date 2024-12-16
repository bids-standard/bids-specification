# BIDS schema

The BIDS schema is a machine readable representation of the BIDS standard,
written in a custom YAML format.
The goal of the schema is to provide a single source for rendering the specification
and validating BIDS datasets, reducing the scope for inconsistencies.
Third party tools may also use the schema to write code that will adapt to additions
to the BIDS standard.

The BIDS schema is available in two machine readable formats:

-   as a set of [YAML](https://en.wikipedia.org/wiki/YAML) files in the [BIDS specification repository](https://github.com/bids-standard/bids-specification/tree/master/src/schema)
-   as a [single dereferencedJSONfile](https://bids-specification.readthedocs.io/en/stable/schema.json)

A didactic walkthrough of the schema can be found in the [BEP Guide](https://bids-extensions.readthedocs.io/en/latest/schema/),
and a complete description is available in the [`bidsschematools` documentation](https://bidsschematools.readthedocs.io/en/latest/).
[`bidsschematools`](https://pypi.org/project/bidsschematools/) is a Python package sourced
from the specification repository, and includes the necessary code to render the specification
and filename validation.
