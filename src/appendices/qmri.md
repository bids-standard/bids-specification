# Quantitative MRI

Quantitative MRI (qMRI) is a collection of methods aiming at generating parametric maps
that can characterize underlying tissue properties.
Unlike those of conventional MR images (for example, `T1w` or `T2w`),
intensity values of quantitative maps are not represented in an arbitrary range.
Instead, these maps are represented either in absolute physical units
(for example, `seconds` for `T1map`),
or within an application dependent range of arbitrary units
(for example, myelin water fraction `MWFmap` in brain).

## Organization of qMRI data in BIDS

Unlike conventional MR images, quantitative maps are not immediate products of the image reconstruction step
(from k-space data to structural images).
Intensity values of qMRI maps are calculated by fitting a collection of parametrically
linked images to a biophysical model or to an MRI signal representation.
This processing is typically carried out in the image domain.
There are two main ways to obtain a quantitative map:

1.  Pre-generated qMRI maps: The qMRI maps are generated right after the reconstruction
    of required input images and made available to the user at the scanner console.
    The acquisition scenarios may include (a) vendor pipelines or (b) open-source pipelines
    deployed at the scanner site.

1.  Post-generated qMRI maps: The qMRI maps are generated from a collection of input
    data after they are exported from the scanner site.
    This type of processing is commonly carried out using an open-source software such as
    [hMRI toolbox](https://github.com/hMRI-group/hMRI-toolbox),
    [mrQ](https://github.com/mezera/mrQ),
    [PyQMRI](https://github.com/IMTtugraz/PyQMRI),
    [qmap](https://web.archive.org/web/20220201201633/https://www.medphysics.wisc.edu/~samsonov/qmap/doc/qmap.html),
    [qMRLab](https://github.com/qmrlab/qmrlab),
    and [QUIT](https://github.com/spinicist/QUIT).

### Inputs are file collections

The common concept of [entity-linked file collections](../common-principles.md#entity-linked-file-collections) enables the description of a qMRI
application by creating logical groups of input files through `suffix` and certain entities
representing acquisition parameters (`echo`, `flip`, `inv`, `mt`) or file parts (`part`).

If a qMRI file collection is intended for creating structural quantitative maps (for example, `T1map`),
files belonging to that collection are stored in the `anat` subdirectory.

List of currently supported collections:

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
         "MESE",
         "MEGRE",
         "VFA",
         "IRT1",
         "MP2RAGE",
         "MPM",
         "MTS",
         "MTR",
      ]
   )
}}

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template("raw", datatypes=["anat"], suffixes=[
         "MESE",
         "MEGRE",
         "VFA",
         "IRT1",
         "MP2RAGE",
         "MPM",
         "MTS",
         "MTR",
      ])
}}

Below is an example file collection for `MP2RAGE`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "anat": {
            "sub-01_inv-1_part-mag_MP2RAGE.nii.gz":"",
            "sub-01_inv-1_part-phase_MP2RAGE.nii.gz":"",
            "sub-01_inv-1_MP2RAGE.json":"",
            "sub-01_inv-2_part-mag_MP2RAGE.nii.gz":"",
            "sub-01_inv-2_part-phase_MP2RAGE.nii.gz":"",
            "sub-01_inv-2_MP2RAGE.json":"",
            },
        },
}
) }}

Commonly, RF fieldmaps (`B1+` and `B1-` maps) are used for the correction of structural quantitative maps.
As these images do not convey substantial structural information,
respective file collections of RF fieldmaps are stored in the `fmap` subdirectory.
Below is an example file collection for RF transmit field map `TB1EPI`:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "fmap": {
            "sub-01_echo-1_flip-1_TB1EPI.nii.gz": "",
            "sub-01_echo-1_flip-1_TB1EPI.json": "",
            "sub-01_echo-2_flip-1_TB1EPI.nii.gz": "",
            "sub-01_echo-2_flip-1_TB1EPI.json": "",
            "sub-01_echo-1_flip-2_TB1EPI.nii.gz": "",
            "sub-01_echo-1_flip-2_TB1EPI.json": "",
            "sub-01_echo-2_flip-2_TB1EPI.nii.gz": "",
            "sub-01_echo-2_flip-2_TB1EPI.json": "",
            },
        },
   }
) }}

Please visit the [file collections appendix](./file-collections.md#magnetic-resonance-imaging) to see the list of currently supported qMRI applications.

### Outputs are quantitative maps

qMRI maps are stored differently depending on the process that generated them.
Pre-generated qMRI maps MAY be stored as part of a raw BIDS dataset,
whereas they MUST be stored in a derivative BIDS dataset if they were post-generated.

See the example below of a `T1map` generated from an `MP2RAGE` file collection using either option.

If the map is post-generated:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "ds-example": {
        "derivatives": {
            "qMRI-software-name": {
                "sub-01": {
                    "anat": {
                        "sub-01_T1map.nii.gz": " # --> T1 map in a derivative dataset",
                        "sub-01_T1map.json": "",
                        "sub-01_UNIT1.nii.gz": " # --> UNI T1 in a derivative dataset",
                        "sub-01_UNIT1.json": "",
                    },
                },
            },
        },
        "sub-01": {
            "anat": {
                "sub-01_inv-1_part-mag_MP2RAGE.nii.gz":"",
                "sub-01_inv-1_part-phase_MP2RAGE.nii.gz":"",
                "sub-01_inv-1_MP2RAGE.json":"",
                "sub-01_inv-2_part-mag_MP2RAGE.nii.gz":"",
                "sub-01_inv-2_part-phase_MP2RAGE.nii.gz":"",
                "sub-01_inv-2_MP2RAGE.json":"",
            },
        },
    },
   }
) }}

If the map is pre-generated, for example, by a Siemens scanner:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "ds-example": {
        "sub-01": {
            "anat": {
                "sub-01_inv-1_part-mag_MP2RAGE.nii.gz":"",
                "sub-01_inv-1_part-phase_MP2RAGE.nii.gz":"",
                "sub-01_inv-1_MP2RAGE.json":"",
                "sub-01_inv-2_part-mag_MP2RAGE.nii.gz":"",
                "sub-01_inv-2_part-phase_MP2RAGE.nii.gz":"",
                "sub-01_inv-2_MP2RAGE.json":"",
                "sub-01_T1map.nii.gz": " # --> T1 map in a raw dataset",
                "sub-01_T1map.json": "",
                "sub-01_UNIT1.nii.gz": " # --> UNI T1 in a raw dataset",
                "sub-01_UNIT1.json": "",
            },
        },
    }
   }
) }}

!!! note "Sharing of vendor outputs"

    Even though the process from which pre-generated qMRI maps are obtained (vendor pipelines) is not known,
    vendors generally allow exporting of the corresponding input data.
    It is RECOMMENDED to share them along with the vendor outputs,
    whenever possible for a qMRI method supported by BIDS.

### Example datasets

You can find example file collections and qMRI maps organized according to BIDS
in the [BIDS examples](https://bids-standard.github.io/bids-examples/#qmri).

## Metadata requirements for qMRI data

The table of required entities for qMRI file collections are provided in the [entity table](./entity-table.md).
However, viability of a qMRI file collection is determined not only by the naming and organization of the input files,
but also by which metadata fields are provided in accompanyingJSONfiles.

### Method-specific priority levels for qMRI file collections

#### Anatomy imaging data

| **File collection**  | **REQUIRED metadata**                                                                                                        | **OPTIONAL metadata**      |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------- | -------------------------- |
| VFA                  | `FlipAngle`, `PulseSequenceType`, `RepetitionTimeExcitation`                                                                 | `SpoilingRFPhaseIncrement` |
| IRT1                 | `InversionTime`                                                                                                              |                            |
| MP2RAGE<sup>\*</sup> | `FlipAngle`, `InversionTime`, `RepetitionTimeExcitation`, `RepetitionTimePreparation`, `NumberShots`,`MagneticFieldStrength` | `EchoTime`                 |
| MESE                 | `EchoTime`                                                                                                                   |                            |
| MEGRE                | `EchoTime`                                                                                                                   |                            |
| MTR                  | `MTState`                                                                                                                    |                            |
| MTS                  | `FlipAngle`, `MTState`, `RepetitionTimeExcitation`                                                                           |                            |
| MPM                  | `FlipAngle`, `MTState`, `RepetitionTimeExcitation`                                                                           | `EchoTime`                 |

<sup>\*</sup> Please see MP2RAGE-specific notes for the calculation of `NumberShots` and regarding the
organization of `UNIT1` image.

Explanation of the table:

-   The metadata fields listed in the REQUIRED column are needed to perform a minimum viable qMRI processing for the corresponding `file collection`.

-   Note that some of the metadata fields may be constant across different files in a file collection,
    yet still required as an input (for example, `NumberShots` in `MP2RAGE`).
    Such metadata fields MUST be provided in the accompanying JSON files.

-   The metadata fields listed in the OPTIONAL column can be used to form different flavors of an existing file collection suffix,
    dispensing with the need for introducing a new suffix.
    See [deriving the intended qMRI application from an ambiguous file collection](#deriving-the-intended-qmri-application-from-an-ambiguous-file-collection)
    for details.

#### Field maps

<!--
This block generates a suffix table.
The definitions of these fields can be found in
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_suffix_table(
      [
        "TB1DAM",
        "TB1EPI",
        "TB1AFI",
        "TB1TFL",
        "TB1RFM",
        "RB1COR",
        "TB1SRGE",
        "TB1map",
        "RB1map",
      ]
   )
}}

<!--
This block generates a filename templates.
The inputs for this macro can be found in the directory
  src/schema/rules/files/raw
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filename_template(
   "raw",
   datatypes=["fmap"],
   suffixes=[
    "TB1DAM",
    "TB1EPI",
    "TB1AFI",
    "TB1TFL",
    "TB1RFM",
    "RB1COR",
    "TB1SRGE",
    "TB1map",
    "RB1map",
    ])
}}

| **File collection**  | **REQUIRED metadata**                                                                                |
| -------------------- | ---------------------------------------------------------------------------------------------------- |
| TB1DAM               | `FlipAngle`                                                                                          |
| TB1EPI               | `EchoTime`, `FlipAngle`, `TotalReadoutTime`, `MixingTime`                                            |
| TB1AFI               | `RepetitionTime`                                                                                     |
| TB1TFL               |                                                                                                      |
| TB1RFM               |                                                                                                      |
| TB1SRGE<sup>\*</sup> | `FlipAngle`, `InversionTime`, `RepetitionTimeExcitation`, `RepetitionTimePreperation`, `NumberShots` |
| RB1COR               |                                                                                                      |

<sup>\*</sup> Please see TB1SRGE-specific notes for the calculation of `NumberShots`.

### Metadata requirements for qMRI maps

As qMRI maps are stored as derivatives, they are subjected to the metadata requirements of
[derived datasets](../modality-agnostic-files.md#derived-dataset-and-pipeline-description).

An example `dataset_description.json` for a qMRI map derivatives directory:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "ds-example": {
        "derivatives": {
            "qMRLab": {
                "dataset_description.json": "",
                "sub-01": {
                    "anat": {
                        "sub-01_T1map.nii.gz": "",
                        "sub-01_T1map.json": "",
                        "sub-01_M0map.nii.gz": "",
                        "sub-01_M0map.json": "",
                        },
                    },
                },
            },
        },
   }
) }}

`dataset_description.json`:

```json
{
  "Name": "qMRLab Outputs",
  "BIDSVersion": "1.5.0",
  "DatasetType": "derivative",
  "GeneratedBy": [
    {
      "Name": "qMRLab",
      "Version": "2.4.1",
      "Container": {
        "Type": "docker",
        "Tag": "qmrlab/minimal:2.4.1"
        }
    },
    {
      "Name": "Manual",
      "Description": "Generated example T1map outputs"
    }
  ],
  "SourceDatasets": [
    {
      "DOI": "doi:10.17605/OSF.IO/K4BS5",
      "URL": "https://osf.io/k4bs5/",
      "Version": "1"
    }
  ]
}
```

In addition to the metadata fields provided in the `dataset_description.json`,
qMRI maps are RECOMMENDED to be accompanied by sidecar JSON files that contain further information about the quantified maps.
Although this may not be the generic case for common derivative outputs,
a proper interpretation of qMRI maps may critically depend on some metadata fields.
For example, without the information of `MagneticFieldStrength`, white-matter T1 values in a `T1map` become elusive.

-   All the acquisition parameters that are constant across the files in a file collection are RECOMMENDED
    to be added to the sidecarJSONof the qMRI maps.

-   Relevant acquisition parameters that vary across files in a qMRI file collection are RECOMMENDED
    to be added to the sidecarJSONof the qMRI map **in array form**.

-   The JSON file accompanying a qMRI map which is obtained by using open-source software is RECOMMENDED
    to include additional metadata fields listed in the following table:

<!-- This block generates a metadata table.
The definitions of these fields can be found in
  src/schema/objects/metadata.yaml
and a guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_metadata_table(
   {
      "Sources": "RECOMMENDED",
      "EstimationReference": "RECOMMENDED",
      "EstimationAlgorithm": "RECOMMENDED",
      "Units": "RECOMMENDED",
      "BasedOn": "DEPRECATED",
   }
) }}

Example:

```text
sub-01_T1map.nii.gz
sub-01_T1map.json
```

sub-01_T1map.json:

```text
{

<<Parameter injected by the software/pipeline>>

"Sources":["bids:raw:sub-01/anat/sub-01_flip-1_VFA.nii.gz",
           "bids:raw:sub-01/anat/sub-01_flip-2_VFA.nii.gz",
           "bids:raw:sub-01/anat/sub-01_flip-3_VFA.nii.gz",
           "bids:raw:sub-01/anat/sub-01_flip-4_VFA.nii.gz",
           "bids:raw:sub-01/fmap/sub-01_TB1map.nii.gz"],
"EstimationPaper":"Deoni et. al.MRM, 2015",
"EstimationAlgorithm":"Linear",
"Units": "second",

<<Parameters that are constant across files in the (parent) file collection>>

"MagneticFieldStrength": "3",
"Manufacturer": "Siemens",
"ManufacturerModelName": "TrioTim",
"InstitutionName": "xxx",
"PulseSequenceType": "SPGR",
"PulseSequenceDetails": "Information beyond the sequence type that identifies
 specific pulse sequence used (VB version, if not standard, Siemens WIP XXX
 ersion ### sequence written by xx using a version compiled on mm/dd/yyyy/)",
"RepetitionTimeExcitation": "35",
"EchoTime": "2.86",
"SliceThickness": "5",

<<Relevant parameters that vary across the linking entity of the (parent) file collection>>

"FlipAngle": ["5","10","15","20"]

}
```

## Deriving the intended qMRI application from an ambiguous file collection

Certain file collection suffixes may refer to a generic data collection regime such as variable flip angle (VFA),
rather than a more specific acquisition, for example, magnetization prepared two gradient echoes (MP2RAGE).
Such generic acquisitions can serve as a basis to derive various qMRI applications by changes to the acquisition sequence
(for example, readout) type or by varying additional scan parameters.

If such an inheritance relationship is applicable between an already existing file collection
and a new qMRI application to be included in the specification,
the inheritor qMRI method is listed in the table below instead of introducing a new file collection suffix.
This approach aims at:

-   preventing the list of available suffixes from over-proliferation,
-   providing qMRI-focused BIDS applications with a set of meta-data driven rules to infer possible fitting options,
-   keeping an inheritance track of the qMRI methods described within the specification.

| **File-collection suffix** | **If REQUIRED metadata == Value** | **OPTIONAL metadata (`entity`/`fixed`)** | **Derived application name (NOT a suffix)** |
| -------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------------- |
| VFA                        | `PulseSequenceType` == `SPGR`     |                                          | DESPOT1                                     |
| VFA                        | `PulseSequenceType` == `SSFP`     | `SpoilingRFPhaseIncrement` (`fixed`)     | DESPOT2                                     |
| MP2RAGE                    |                                   | `EchoTime` (`echo`)                      | MP2RAGE-ME                                  |
| MPM                        |                                   | `EchoTime` (`echo`)                      | MPM-ME                                      |

In this table, (`entity`/`fixed`) denotes whether the OPTIONAL metadata that forms a new
flavor of qMRI application for the respective suffix varies across files of a file collection
(which calls for using a linking entity) or fixed. If former is the case, the entity is to be
added to the files in that file collection. Note that this addition MUST be allowed by the
priority levels given for that suffix in the [`entity table`](./entity-table.md). If latter (`fixed`) is the case,
filenames will remain the same; however, the optional metadata (third column) may
define the flavor of the application (fourth column) along with the conditional value of a
required metadata field (second column).

A derived qMRI application becomes available if all the optional metadata fields
listed for the respective file collection suffix are provided for the data. In addition,
conditional rules based on the value of a given required metadata field can be set
for the description of a derived qMRI application. Note that the value of this
required metadata is fixed across constituent images of a file collection and defined
in [Method-specific priority levels for qMRI file collections](#method-specific-priority-levels-for-qmri-file-collections).

For example, if the optional metadata field of `PulseSequenceType` is SPGR
for a collection of anatomical images listed by the `VFA` suffix, the data
qualifies for `DESPOT1` T1 fitting. For the same suffix, if the `PulseSequenceType`
metadata field has the value of `SSFP`, and the `SpoilingRFPhaseIncrement` is
provided as a metadata field, then the dataset becomes eligible for `DESPOT2`
T2 fitting application.

Please note that optional metadata fields listed in the
[deriving the intended qMRI application from an ambiguous file collection table](#deriving-the-intended-qmri-application-from-an-ambiguous-file-collection)
are included in the optional (third) column of
[the priority levels table](#method-specific-priority-levels-for-qmri-file-collections)
for the consistency of this appendix.

## Introducing a new qMRI file collection

If a qMRI application cannot be interpreted as a subtype of an already existing suffix
of a qMRI-related file collection, we RECOMMEND adhering to the following principles to
introduce a new suffix:

-   All qMRI-relevant file collection suffixes are capitalized.

-   Unless the pulse sequence is exclusively associated with a specific qMRI application
    (for example, `MP2RAGE`), sequence names are not used as suffixes.

-   File collection suffixes for qMRI applications attain a clear description of the qMRI method that they relate to in the
    [file collections appendix](./file-collections.md#magnetic-resonance-imaging).

-   Hyperlinks to example applications and reference method articles are encouraged whenever possible.

-   If it is possible to derive a qMRI application from an already existing file collection suffix
    by defining a set of logical conditions over the metadata fields, the tables of the
    [deriving the intended qMRI application from an ambiguous file collection](#deriving-the-intended-qmri-application-from-an-ambiguous-file-collection)
    and the
    [anatomy data priority levels](#anatomy-imaging-data)
    sections are extended instead of introducing a new suffix.

## Application-specific notes for qMRI file collections

### Anatomy imaging data

General notes:

-   Some BIDS metadata field values are calculated based on the values of other metadata fields that are not listed as required fields.
    These fields include: `NumberShots`.
    The calculation of the values may depend on the type of the acquisition.
    These acquisitions include: `MP2RAGE` and `TB1SRGE`.

#### `MP2RAGE` specific notes

##### `UNIT1` images

Although the `UNIT1` image is provided as an output by the acquisition sequence, it is used
as an input to offline calculation of a `T1map` using a dictionary lookup approach. However,
`complex` data is needed for an accurate calculation of the `UNIT1` image, which is not commonly
provided by the stock sequence. Instead, the `magnitude` and `phase` images are exported. Please
see the relevant discussion at [qMRLab issue #255](https://github.com/qMRLab/qMRLab/issues/255).

Therefore, the `UNIT1` image provided by the scanner
SHOULD be stored under the `anat` in a raw BIDS dataset
along with the `MP2RAGE` file collection
and to be used as the primary input for quantifying a `T1map`.

If an additional `UNIT1` image is calculated offline,
then the output MUST be stored in a derivative BIDS dataset with necessary provenance information.

##### `NumberShots` metadata field

Note that the type of `NumberShots` field can be either a `number` or an `array of numbers`.

-   If a single `number` is provided, this should correspond to the number of `SlicesPerSlab` or `ReconMatrixPE`.
    However, in this case, `SlicePartialFourier` or `PartialFourierPE` fraction is needed
    to calculate the number of partitions `before` and `after` of the k-space center to calculate a T1 map.

-   If `before/after` calculation is performed during the BIDS conversion of the `MP2RAGE` data,
    then the value of `NumberShots` metadata field can be given as a 1X2 array,
    with first entry corresponding to `before` and the second to the `after`.

Formula:

If NumberShots is an array of numbers such that `"NumberShots": [before, after]`,
the values of `before` and `after` are calculated as follows:

```text
before = SlicesPerSlab*(SlicePartialFourier - 0.5)
after  = SlicesPerSlab/2
```

See this [reference implementation](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/a405df30ac2c617d29d8b1b16025aaa911e86370/func/bids_T1B1correct.m#L16).

##### Other metadata fields

The value of the `RepetitionTimeExcitation` field is not commonly found in the DICOM files.
When accessible, the value of `EchoSpacing` corresponds to this metadata.
When not accessible, `2 X EchoTime` can be used as a surrogate.

Further information about other `MP2RAGE` qMRI protocol fields can be found in the
[qMRLab documentation](https://qmrlab.readthedocs.io/en/master/protocols.html#mp2rage).

#### `TB1SRGE` specific notes

Calculation of `before` and `after` entries for `NumberShots` metadata field of `TB1SRGE` is more involved than that of `MP2RAGE`.
The formula can be found in a
[reference implementation](https://github.com/JosePMarques/MP2RAGE-related-scripts/blob/a405df30ac2c617d29d8b1b16025aaa911e86370/DemoForR1Correction.m#L17),
which requires information about `BaseResolution` (that is, image matrix size in PE direction),
partial Fourier fraction in the PE direction, number of reference lines for parallel imaging acceleration,
and the parallel imaging acceleration factor in PE direction.

### Radiofrequency (RF) field mapping

Some RF file collections call for the use of special notations that cannot be resolved by
by entities that can generalize to other applications.
Instead of introducing an entity that is exclusive to a single application,
method developers who commonly use these file collections for the `MPM` application reached
the consensus on the use of `acq` entity to distinguish individual files.
These suffixes include: `TB1AFI`, `TB1TFL`, `TB1RFM`, and `RB1COR`.

#### `TB1EPI` specific notes

The `flip` and `echo` entities MUST be used to distinguish images with this suffix.
The use of `flip` follows the default convention. However, this suffix defines a
specific use case for the `echo` entity:

| **`echo-1`**         | **`echo-2`**                |
| -------------------- | --------------------------- |
| Lower `EchoTime`     | Higher `EchoTime`           |
| Spin Echo (SE) image | Stimulated Echo (STE) image |

At each `FlipAngle`, the `TB1EPI` suffix lists two images acquired at two echo times.
The first echo is a spin echo (SE) formed by the pulses alpha-2alpha. However, the
second echo in this method is generated in a different fashion compared to a typical
MESE acquisition. The second echo is a stimulated echo (STE) that is formed by an
additional alpha pulse (that is, alpha-2alpha-alpha).

The `FlipAngle` value corresponds to the nominal flip angle value of the STE pulse.
The nominal FA value of the SE pulse is twice this value.

Note that the following metadata fields MUST be defined in the accompanying JSON
files:

<!-- This block generates a metadata table.
These tables are defined in
  src/schema/rules/sidecars
The definitions of the fields specified in these tables may be found in
  src/schema/objects/metadata.yaml
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_sidecar_table("fmap.TB1EPI") }}

To properly identify constituents of this particular method, values of the `echo`
entity MUST index the images as follows:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "fmap": {
            "sub-01_echo-1_flip-1_TB1EPI.nii.gz": "# SE",
            "sub-01_echo-1_flip-1_TB1EPI.json":   "",
            "sub-01_echo-2_flip-1_TB1EPI.nii.gz": "# STE",
            "sub-01_echo-2_flip-1_TB1EPI.json":   "",
            "sub-01_echo-1_flip-2_TB1EPI.nii.gz": "# SE",
            "sub-01_echo-1_flip_2_TB1EPI.json":   "",
            "sub-01_echo-2_flip-2_TB1EPI.nii.gz": "# STE",
            "sub-01_echo-2_flip-2_TB1EPI.json":   "",
            },
        },
   }
) }}

#### `TB1AFI` specific notes

This method calculates a B1<sup>+</sup> map from two images acquired at two interleaved excitation repetition times (TR).
Note that there is no entity for the TR that can be used to label the files corresponding to the two
repetition times and the definition of repetition time depends on the modality
(`functional` or `anatomical`) in the specification.

Therefore, to properly identify constituents of this particular method,
values of the `acq` entity SHOULD begin with either `tr1` (lower TR) or `tr2` (higher TR)
and MAY be followed by freeform entries:

| **First `TR`**   | **Second `TR`**  | **Use case**         |
| ---------------- | ---------------- | -------------------- |
| `_acq-tr1`       | `_acq-tr2`       | Single acquisition   |
| `_acq-tr1Test`   | `_acq-tr2Test`   | Acquisition `Test`   |
| `_acq-tr1Retest` | `_acq-tr2Retest` | Acquisition `Retest` |

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "fmap": {
            "sub-01_acq-tr1_TB1AFI.nii.gz": "",
            "sub-01_acq-tr1_TB1AFI.json": "",
            "sub-01_acq-tr2_TB1AFI.nii.gz": "",
            "sub-01_acq-tr2_TB1AFI.json": "",
            },
        },
   }
) }}

#### `TB1TFL` and `TB1RFM` specific notes

These suffixes describe two outputs generated by Siemens `tfl_b1_map` and `rf_map` product sequences, respectively.
Both sequences output two images.
The first image appears like an anatomical image and the second output is a scaled flip angle map.

To properly identify files of this particular file collection,
values of the `acq` entity SHOULD begin with either `anat` or `famp` and MAY be followed by freeform entries:

| **Anatomical (like) image** | **Scaled flip angle map** | **Use case**         |
| --------------------------- | ------------------------- | -------------------- |
| `_acq-anat`                 | `_acq-famp`               | Single acquisition   |
| `_acq-anatTest`             | `_acq-fampTest`           | Acquisition `Test`   |
| `_acq-anatRetest`           | `_acq-fampRetest`         | Acquisition `Retest` |

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "fmap": {
            "sub-01_acq-anat_TB1TFL.nii.gz": "",
            "sub-01_acq-anat_TB1TFL.json": "",
            "sub-01_acq-famp_TB1TFL.nii.gz": "",
            "sub-01_acq-famp_TB1TFL.json": "",
            },
        },
   }
) }}

The example above applies to the `TB1RFM` suffix as well.

#### `RB1COR` specific notes

This method generates a receive sensitivity map by combining two low resolution images
collected sequentially by two different RF coils in receive mode (the body and the head coil)
with otherwise identical acquisition parameters.
To correct for dynamic changes in the receive sensitivity over time due to, for example,
subject motion, separate receive sensitivity maps may be acquired for each anatomical
acquisition in a file collection.

To properly identify constituents of this particular method, values of the `acq`
entity SHOULD begin with either `body` or `head` and MAY be followed by freeform
entries:

| **Body coil**  | **Head coil**  | **Use case**       |
| -------------- | -------------- | ------------------ |
| `_acq-body`    | `_acq-head`    | Single acquisition |
| `_acq-bodyMTw` | `_acq-headMTw` | `MTw` for `MPM`    |
| `_acq-bodyPDw` | `_acq-headPDw` | `PDw` for `MPM`    |
| `_acq-bodyT1w` | `_acq-headT1w` | `T1w` for `MPM`    |

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "fmap": {
            "sub-01_acq-body_RB1COR.nii.gz": "# Body coil",
            "sub-01_acq-body_RB1COR.json": "",
            "sub-01_acq-head_RB1COR.nii.gz": "# Head coil",
            "sub-01_acq-head_RB1COR.json": "",
            },
        },
   }
) }}
