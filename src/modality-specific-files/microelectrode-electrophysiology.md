# Microelectrode Electrophysiology

Support for Microelectrode Electrophysiology was developed as a [BIDS Extension Proposal](../extensions.md#bids-extension-proposals) [BEP032: Animal electrophysiology (ephys)](https://bids.neuroimaging.io/bep032).

Please see [Citing BIDS](../introduction.md#citing-bids) on how to appropriately credit this extension
when referring to it in the context of the academic literature.

This BEP has been initiated by members of the INCF Working Group on Standardized Data Structures,
that was initiated in 2020 to develop a set of specifications and tools
that would allow the standardization of a directory structure for experimental data recorded
with animal models in neuroscience, and its associated metadata.

Please consider joining this working group if you would like to contribute to this effort.
You can also reach the moderators of this BEP through our [main discussion forum](https://github.com/INCF/neuroscience-data-structure/issues), where you can participate in existing discussions or raise new questions / issues.

Most core principles of the original BIDS and particulars of BIDS-iEEG specification are adopted
for this modality as well, though some special considerations and additional fields were added.

Several [example Microelectrode Electrophysiology datasets](https://bids-standard.github.io/bids-examples/#microephys)
have been formatted using this specification and can be used for practical guidance when curating a new dataset.

## Primary data file formats

Unprocessed microelectrode electrophysiology (`icephys` and `ecephys` modalities) data must be stored in an [open file format](https://en.wikipedia.org/wiki/Open_format),
while the native format, if different, can be stored in an optional  `sourcedata/` directory.
The native file format is used in case conversion elicits the loss of crucial metadata specific to manufacturers and specific acquisition systems.
Metadata should be included alongside the data in the `.json` and `.tsv` files.
The current list of allowed data file formats:

| **Format**                                                                          | **Extension(s)** | **Description**                                                                                                                                                                                                      |
--------------------------------------------------------------------------------------|------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| [Neuroscience Information Exchange Format](https://nixio.readthedocs.io/en/latest/) | `.nix`           | A generic and open  framework with an hdf5 backend and a defined interface to many ephys formats via the [Neo library](https://neo.readthedocs.io/en/latest/). The `.nix` file has to contain a valid Neo structure. |
| [Neurodata Without Borders](https://www.nwb.org)                                    | `.nwb`           | BRAIN Initiative Data Standard based on an hdf5 backend ...                                                                                                                                                          |

Both of these formats can also store essential metadata of the datasets.
Some of these need to be duplicated in BIDS `.tsv` and `.json` sidecar files.
Even though the duplication requires additional effort to ensure the consistency of the data, it provides a number of advantages:
-   Making the dataset easier for humans to scan as essential information is easily accessible without loading the data files
-   The dataset follows the BIDS standard and can benefit from tools building on top of this standard, starting with [bids-validator](https://github.com/bids-standard/bids-validator).
-   It simplifies the separation of data and basic metadata, for example to publish a dataset in a light-weight fashion with access to the data files on request (as implemented by [DataLad](https://www.datalad.org)).

##

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "raw",
   datatypes=["ecephys", "icephys"],
   suffixes=["ecephys", "icephys", "events", "channels", "electrodes","scans"]
)
}}

<!-- Link Definitions -->

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["icephys"],
   suffixes=["icephys", "events", "channels", "electrodes","scans"]
)
}}

{{ MACROS___make_filename_template(
   "raw",
   datatypes=["ecephys"],
   suffixes=["ecephys", "events", "channels", "electrodes","scans"]
)
}}
