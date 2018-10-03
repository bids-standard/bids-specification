Units
=====

All units SHOULD be specified as per International System of Units (abbreviated as SI, from the French Système international (d'unités)) and can be SI units or SI derived units. In case there are valid reasons to deviate from  SI units or SI derived units, the units MUST be specified in the sidecar JSON file. In case data is expressed in SI units or SI derived units,  the units MAY be specified in the sidecar JSON file.  In case prefixes are added to SI or non-SI units (e.g. mm), the prefixed units MUST be specified in the JSON file (see Appendix V: Units).  In particular:

-   Elapsed time SHOULD be expressed in seconds. Please note that some DICOM parameters have been traditionally expressed in milliseconds. Those need to be converted to seconds.
-   Frequency SHOULD be expressed in Hertz.

Describing dates and timestamps:

-   Date time information MUST be expressed in the following format `YYYY-MM-DDThh:mm:ss` (one of the [ISO8601](https://en.wikipedia.org/wiki/ISO_8601) date-time formats). For example: `2009-06-15T13:45:30`
-   Time stamp information MUST be expressed in the following format: `13:45:30`
-   Dates can be shifted by a random number of days for privacy protection reasons. To distinguish real dates from shifted dates always use year 1900 or earlier when including shifted years. For longitudinal studies please remember to shift dates within one subject by the same number of days to maintain the interval information. Example: `1867-06-15T13:45:30`
-   Age SHOULD be given as the number of years since birth at the time of scanning (or first scan in case of multi session datasets). Using higher accuracy (weeks) should in general be avoided due to privacy protection, unless when appropriate given the study goals, e.g., when scanning babies.
