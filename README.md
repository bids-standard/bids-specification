# BIDS Schema

The BIDS Schema is the canonical reference for terms and rules associated with
the [Brain Imaging Data Structure](https://bids.neuroimaging.io) standard.

The schema itself is a collection of YAML files that are compiled into a JSON object
using the [bidsschematools](https://bidsschematools.readthedocs.io/en/latest/) Python
package bundled with the specification.

This package provides ready import for Javascript and Typescript projects.

## Usage

```typescript
import type { Schema, Context } from 'jsr:@bids/schema'
import { schema } from 'jsr:@bids/schema'

const metadataFields = schema.objects.metadata
const filenameRules = schema.rules.files
```
