# Appendix VI: MEG file formats

Each MEG system brand has specific file organization and data formats.
RECOMMENDED values for `manufacturer_specific_extensions`:

| **Value**                                           | **Description**                                                                       |
| --------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [`ctf`](06-meg-file-formats.md#ctf)                 | CTF (directory with `.ds` extension)                                                  |
| [`fif`](06-meg-file-formats.md#neuromagelektamegin) | Neuromag / Elekta / MEGIN and BabyMEG (file with extension `.fif`)                    |
| [`4d`](06-meg-file-formats.md#bti4d-neuroimaging)   | BTi / 4D Neuroimaging (directory containing multiple files without extensions)        |
| [`kit`](06-meg-file-formats.md#kityokogawaricoh)    | KIT / Yokogawa / Ricoh (file with extension `.sqd`, `.con`, `.raw`, `.ave` or `.mrk`) |
| [`kdf`](06-meg-file-formats.md#kriss)               | KRISS (file with extension `.kdf`)                                                    |
| [`itab`](06-meg-file-formats.md#itab)               | Chieti system (file with extension `.raw` and `.mhd`)                                 |

Below are specifications for each system brand.

## CTF

Each experimental run with a CTF system yields a directory with a `.ds` extension,
containing several files. The OPTIONAL digitized positions of the head points
are usually stored in a separate `.pos` file, not necessarily within the `.ds`
directory.

```Text
[sub-<label>[_ses-<label>]_headshape.pos]
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.ds>
```

CTF's data storage is therefore via directories containing multiple files. The
files contained within a `.ds` directory are named such that they match the
parent directory, but preserve the original file extension (for example, `.meg4`,
`.res4`).
The renaming of CTF datasets SHOULD be done with a specialized software
such as the CTF newDs command-line application or
[MNE-BIDS](https://github.com/mne-tools/mne-bids).

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001": {
            "sub-control01_ses-001_scans.tsv": "",
            "meg": {
                "sub-control01_ses-001_coordsystem.json": "",
                "sub-control01_ses-001_headshape.pos": "",
                "sub-control01_ses-001_task-rest_run-01_meg.ds": {},
                "sub-control01_ses-001_task-rest_run-01_meg.json": "",
                "sub-control01_ses-001_task-rest_run-01_channels.tsv": "",
                },
            },
        }
   }
) }}

To learn more about CTF’s data organization:
[https://www.fieldtriptoolbox.org/getting_started/ctf](https://www.fieldtriptoolbox.org/getting_started/ctf)

## Neuromag/Elekta/MEGIN

Neuromag/Elekta/MEGIN and Tristan Technologies BabyMEG data is stored as
FIFF files with the extension `.fif`. The digitized positions of the head
points are saved inside the FIFF file along with the MEG data, with typically no
`_headshape` file.

```Text
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.fif
```

### Cross-talk and fine-calibration files

In case internal active shielding (IAS) was used during acquisition, raw FIFF
files need to be processed using Maxwell filtering
(signal-space separation, SSS) to make the data usable.
To this end, two specific files are needed:
The *cross-talk* file, and the *fine-calibration* file,
both of which are produced by the MaxFilter software
and the work of the Neuromag/Elekta/MEGIN engineers during maintenance of the MEG acquisition system.
Both files are thus specific to the site of recording and may change in the
process of regular system maintenance.

In BIDS, the cross-talk and fine-calibration files are shared unmodified,
including their original extensions (`.fif` for cross-talk and `.dat` for
fine-calibration), but with BIDS file naming convention and by using the `acq`
entity.

-   cross-talk file template: `sub-<label>[_ses-<label>]_acq-crosstalk_meg.fif`
-   fine-calibration file template: `sub-<label>[_ses-<label>]_acq-calibration_meg.dat`

Note that cross-talk files MUST be denoted using `acq-crosstalk` and
fine-calibration files MUST be denoted using `acq-calibration`.

The cross-talk and fine-calibration data MUST be stored in the subject-level `meg` directory,
which may be nested inside a `ses-<label>` directory, as shown in the following examples.

#### Example with single session (omitted session directory)

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "meg": {
            "sub-01_coordsystem.json": "",
            "sub-01_task-rest_meg.fif": "",
            "sub-01_task-rest_meg.json": "",
            "sub-01_task-rest_channels.tsv": "",
            "sub-01_acq-crosstalk_meg.fif": "",
            "sub-01_acq-calibration_meg.dat": "",
            },
        },
    "sub-02": {
        "meg": {
            "sub-02_coordsystem.json": "",
            "sub-02_task-rest_meg.fif": "",
            "sub-02_task-rest_meg.json": "",
            "sub-02_task-rest_channels.tsv": "",
            "sub-02_acq-crosstalk_meg.fif": "",
            "sub-02_acq-calibration_meg.dat": "",
            },
        }
   }
) }}

#### Example with multiple sessions

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-01": {
        "ses-01":{
            "sub-01_ses-01_scans.tsv": "",
            "meg": {
                "sub-01_ses-01_coordsystem.json": "",
                "sub-01_ses-01_task-rest_run-01_meg.fif": "",
                "sub-01_ses-01_task-rest_run-01_meg.json": "",
                "sub-01_ses-01_task-rest_run-01_channels.tsv": "",
                "sub-01_ses-01_acq-crosstalk_meg.fif": "",
                "sub-01_ses-01_acq-calibration_meg.dat": "",
                },
            },
        "ses-02":{
            "sub-01_ses-02_scans.tsv": "",
            "meg": {
                "sub-01_ses-02_coordsystem.json": "",
                "sub-01_ses-02_task-rest_run-01_meg.fif": "",
                "sub-01_ses-02_task-rest_run-01_meg.json": "",
                "sub-01_ses-02_task-rest_run-01_channels.tsv": "",
                "sub-01_ses-02_acq-crosstalk_meg.fif": "",
                "sub-01_ses-02_acq-calibration_meg.dat": "",
                },
            },
        },
   }
) }}

### Sharing FIFF data after signal-space separation (SSS)

After applying SSS (for example, by using the MaxFilter software),
files SHOULD be renamed with the corresponding label (for example, `proc-sss`)
and placed in a `derivatives` subdirectory.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "meg": {
                "sub-control01_ses-001_task-rest_run-01_proc-sss_meg.fif": "",
                "sub-control01_ses-001_task-rest_run-01_proc-sss_meg.json": "",
                },
            },
        }
   }
) }}

### Split files

In the case of long data recordings that exceed a file size of 2Gb, the `.fif`
files are conventionally split into multiple parts.
For example:

```Text
some_file.fif
some_file-1.fif
```

Each of these files has an internal pointer to the next file.
This is important when renaming these split recordings to the BIDS convention.
Instead of a simple renaming, files should be read in and saved under their new
names with dedicated tools like [MNE](https://mne.tools), which will ensure
that not only the filenames, but also the internal file pointers will be
updated.

It is RECOMMENDED that FIFF files with multiple parts use the `split-<index>`
entity to indicate each part.

If there are multiple parts of a recording and the optional `scans.tsv` is provided,
remember to list all files separately in `scans.tsv` and that the entries
for the `acq_time` column in `scans.tsv` MUST all be identical, as described in
[Scans file](../03-modality-agnostic-files.md#scans-file).

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "meg": {
                "sub-control01_ses-001_task-rest_run-01_split-01_meg.fif": "",
                "sub-control01_ses-001_task-rest_run-01_split-02_meg.fif": "",
                },
            },
        }
   }
) }}

More information can be found under the following links:

-   [Neuromag/Elekta/MEGIN data organization](https://www.fieldtriptoolbox.org/getting_started/neuromag)
-   [BabyMEG](https://www.fieldtriptoolbox.org/getting_started/babysquid)

### Recording dates in `.fif` files

It is important to note that recording dates in `.fif` files are represented
as `int32` format seconds since (or before) [*the Epoch*](https://en.wikipedia.org/wiki/Unix_time)
(`1970-01-01T00:00:00.000000` UTC).
Integers in `int32` format can encode values from -2,147,483,647 to +2,147,483,647.
Due to this representation, the Neuromag/Elekta/MEGIN file format for MEG (`.fif`) does *not*
support recording dates earlier than `1901-12-13T08:45:53.000000` UTC or later than
`2038-01-19T03:14:07.000000` UTC.

## BTi/4D neuroimaging

Each experimental run on a 4D neuroimaging/BTi system results in a directory
containing multiple files without extensions.

```Text
[sub-<label>[_ses-<label>]_headshape.pos]
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg>
```

One SHOULD rename/create a parent run-specific directory and keep the original
files for each run inside (for example, `c,rfhp0.1Hz`, `config` and `hs_file`).

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "sub-control01_ses-001_scans.tsv": "",
            "meg": {
                "sub-control01_ses-001_coordsystem.json": "",
                "sub-control01_ses-001_headshape.pos": "",
                "sub-control01_ses-001_task-rest_run-01_meg": {},
                "sub-control01_ses-001_task-rest_run-01_meg.json": "",
                "sub-control01_ses-001_task-rest_run-01_channels.tsv": "",
                },
            },
        },
   }
) }}

Where:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01_ses-001_task-rest_run-01_meg": {
        "config": "",
        "hs_file": "",
        "e,rfhp1.0Hz.COH": "",
        "c,rfDC": "",
        },
   }
) }}

More about the 4D neuroimaging/BTi data organization at:
[https://www.fieldtriptoolbox.org/getting_started/bti](https://www.fieldtriptoolbox.org/getting_started/bti)

## KIT/Yokogawa/Ricoh

Each experimental run on a KIT/Yokogawa/Ricoh system yields a raw file with either
`.sqd` or `.con` extension,
and with its associated marker coil file(s) with either `.sqd` or `.mrk` extension.
The marker coil file(s) contain coil positions in the *acquisition system's native space*.
Head points and marker points in *head space* are acquired using third-party hardware.

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "sub-control01_ses-001_scans.tsv": "",
            "meg": {
                "sub-control01_ses-001_coordsystem.json": "",
                "sub-control01_ses-001_headshape.txt": "",
                "sub-control01_ses-001_task-rest_run-01_meg": "",
                "sub-control01_ses-001_task-rest_run-01_meg.json": "",
                "sub-control01_ses-001_task-rest_run-01_channels.tsv": "",
                "sub-control01_ses-001_task-rest[_acq-<label>]_run-01_markers.<mrk,sqd>": "",
                "sub-control01_ses-001_task-rest_run-01_meg.<con,sqd>": "",
                },
            },
        },
   }
) }}

To understand why both `.sqd` and `.con`, as well as both `.sqd` and `.mrk` are valid
extensions, we provide a brief historical perspective on the evolution of the data format:
The original extension for KIT/Yokogawa/Ricoh continuous data was `.sqd`.
This was later modernized to `.con` (to denote "continuous").
However, to preserve backwards compatibility, `.sqd` is still a valid extension for the raw, continuous data file.
The original extension for KIT/Yokogawa/Ricoh marker files was `.sqd` as well.
That lead to the ambiguous situation where both the raw data and the marker file(s) could end on `.sqd`.
To distinguish between continuous data and marker file(s), the internal header of the files needed to be read first.
For this reason, the marker file extension was later modernized to `.mrk` to better disambiguate files.
However again, to preserve backwards compatibility, `.sqd` is still a valid extension for the marker file(s).

If there are multiple files with marker coils, the marker files must have the
`acq-<label>` parameter and no more that two marker files may be associated with
one raw data file.
While the acquisition parameter can take any value, it is RECOMMENDED that if
the two marker measurements occur before and after the raw data acquisition,
`pre` and `post` are used to differentiate the two situations.

More about the KIT/Yokogawa/Ricoh data organization at:
[https://www.fieldtriptoolbox.org/getting_started/yokogawa](https://www.fieldtriptoolbox.org/getting_started/yokogawa)

## KRISS

Each experimental run on the KRISS system produces a file with extension
`.kdf`. Additional files can be available in the same directory: the digitized
positions of the head points (`\_digitizer.txt`), the position of the center of
the MEG coils (`.chn`) and the event markers (`.trg`).

```Text
[sub-<label>[_ses-<label>]_headshape.txt]
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.kdf
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.chn
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.trg
sub-<label>[_ses-<label>]_task-<label>[_acq-<label>]_digitizer.txt
```

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "sub-control01_ses-001_scans.tsv": "",
            "meg": {
                "sub-control01_ses-001_coordsystem.json": "",
                "sub-control01_ses-001_headshape.txt": "",
                "sub-control01_ses-001_task-rest_run-01_meg": "",
                "sub-control01_ses-001_task-rest_run-01_meg.json": "",
                "sub-control01_ses-001_task-rest_run-01_channels.tsv": "",
                "sub-control01_ses-001_task-rest_run-01_meg.chn": "",
                "sub-control01_ses-001_task-rest_run-01_meg.kdf": "",
                "sub-control01_ses-001_task-rest_run-01_meg.trg": "",
                "sub-control01_ses-001_task-rest_digitizer.txt": "",
                },
            },
        },
   }
) }}

## ITAB

Each experimental run on a ITAB-ARGOS153 system yields a raw (`.raw`) data file
plus an associated binary header file (`.mhd`). The raw data file has an ASCII
header that contains detailed information about the data acquisition system,
followed by binary data. The associated binary header file contains part of the
information from the ASCII header, specifically the one needed to process data,
plus other information on offline preprocessing performed after data acquisition
(for example, sensor position relative to subject’s head, head markers, stimulus
information).

Example:

<!-- This block generates a file tree.
A guide for using macros can be found at
 https://github.com/bids-standard/bids-specification/blob/master/macros_doc.md
-->
{{ MACROS___make_filetree_example(
   {
    "sub-control01": {
        "ses-001":{
            "meg": {
                "sub-control01_ses-001_coordsystem.json": "",
                "sub-control01_ses-001_headshape.txt": "",
                "sub-control01_ses-001_task-rest_run-01_meg": "",
                "sub-control01_ses-001_task-rest_run-01_meg.json": "",
                "sub-control01_ses-001_task-rest_run-01_channels.tsv": "",
                "sub-control01_ses-001_task-rest_run-01_meg.raw": "",
                "sub-control01_ses-001_task-rest_run-01_meg.raw.mhd": "",
                },
            },
        },
   }
) }}

## Aalto MEG–MRI

For stand-alone MEG data, the Aalto hybrid device uses the standard `.fif` data
format and follows the conventions of Elekta/Neuromag as described
[above](06-meg-file-formats.md#neuromagelektamegin). The `.fif` files may
contain unreconstructed MRI data. The inclusion of MRI data and information for
accurate reconstruction will be fully standardized at a later stage.
