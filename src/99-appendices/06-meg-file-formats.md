# Appendix VI: MEG file formats

Each MEG system brand has specific file organization and data formats.
RECOMMENDED values for `manufacturer_specific_extensions`:

| Value                                                 | Definition                                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------------------------- |
| [`ctf`](06-meg-file-formats.md#ctf)                   | CTF (folder with `.ds` extension)                                                     |
| [`fif`](06-meg-file-formats.md#neuromagelektamegin)   | Neuromag / Elekta / MEGIN  and BabyMEG (file with extension `.fif`)                   |
| [`4d`](06-meg-file-formats.md#bti4d-neuroimaging)     | BTi / 4D Neuroimaging (folder containing multiple files without extensions)           |
| [`kit`](06-meg-file-formats.md#kityokogawaricoh)      | KIT / Yokogawa / Ricoh (file with extension `.sqd`, `.con`, `.raw`, `.ave` or `.mrk`) |
| [`kdf`](06-meg-file-formats.md#kriss)                 | KRISS (file with extension `.kdf`)                                                    |
| [`itab`](06-meg-file-formats.md#itab)                 | Chieti system (file with extension `.raw` and `.mhd`)                                 |

Below are specifications for each system brand.

## CTF

Each experimental run with a CTF system yields a folder with a `.ds` extension,
containing several files. The OPTIONAL digitized positions of the head points
are usually stored in a separate `.pos` file, not necessarily within the `.ds`
folder.

```Text
[sub-<label>[_ses-<label>]_headshape.pos]
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.ds>
```

CTF's data storage is therefore via directories containing multiple files. The
files contained within a `.ds` directory are named such that they match the
parent directory, but preserve the original file extension (e.g., `.meg4`,
`.res4`, etc.). The renaming of CTF datasets SHOULD be done with a specialized
software such as the CTF newDs command-line application or
[MNE-BIDS](https://github.com/mne-tools/mne-bids).

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_scans.tsv
        meg/
            sub-control01_ses-001_coordsystem.json
            sub-control01_ses-001_headshape.pos
            sub-control01_ses-001_task-rest_run-01_meg.ds
            sub-control01_ses-001_task-rest_run-01_meg.json
            sub-control01_ses-001_task-rest_run-01_channels.tsv
```

To learn more about  CTF’s data organization:
[http://www.fieldtriptoolbox.org/getting_started/ctf](http://www.fieldtriptoolbox.org/getting_started/ctf)

## Neuromag/Elekta/MEGIN

Neuromag/Elekta/MEGIN data and Tristan Technologies BabyMEG data is stored with
file extension `.fif`. The digitized positions of the head points are saved
inside the fif file along with the MEG data, with typically no `_headshape`
file.

```Text
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg.fif
```

Note that we do not provide specifications for cross-talk and
fine-calibration matrix files in the current version of BIDS.

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_scans.tsv
        meg/
            sub-control01_ses-001_coordsystem.json
            sub-control01_ses-001_task-rest_run-01_meg.fif
            sub-control01_ses-001_task-rest_run-01_meg.json
            sub-control01_ses-001_task-rest_run-01_channels.tsv
```

After applying the MaxFilter pre-processing tool, files should be renamed with
the corresponding label (e.g., `proc-sss`) and placed into a `derivatives`
subfolder.

Example:

```Text
sub-control01_ses-001_task-rest_run-01_proc-sss_meg.fif
sub-control01_ses-001_task-rest_run-01_proc-sss_meg.json
```

In the case of long data recordings that exceed a file size of 2Gb, the `.fif`
files are conventionally split into multiple parts. For example:

```Text
some_file.fif
some_file-1.fif
```

Each of these files has an internal pointer to the next file.
This is important when renaming these split recordings to the BIDS convention.
Instead of a simple renaming, files should be read in and saved under their new
names with dedicated tools like [MNE](https://mne.tools), which will ensure
that not only the file names, but also the internal file pointers will be
updated.

It is RECOMMENDED that `.fif` files with multiple parts use the `split-<index>`
entity to indicate each part.

Example:

```Text
sub-control01_ses-001_task-rest_run-01_split-01_meg.fif
sub-control01_ses-001_task-rest_run-01_split-02_meg.fif
```

More information can be found under the following links:

-   [Neuromag/Elekta/MEGIN data organization](http://www.fieldtriptoolbox.org/getting_started/neuromag)
-   [BabyMEG](http://www.fieldtriptoolbox.org/getting_started/babysquid)

## BTi/4D neuroimaging

Each experimental run on a 4D neuroimaging/BTi system results in a folder
containing multiple files without extensions.

```Text
[sub-<label>[_ses-<label>]_headshape.pos]
sub-<label>[_ses-<label>]_task-<label>[_run-<index>]_meg>
```

One SHOULD rename/create a father run specific directory and keep the original
files for each run inside (e.g., `c,rfhp0.1Hz`, `config` and `hs_file`).

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_scans.tsv
        meg/
            sub-control01_ses-001_coordsystem.json
            sub-control01_ses-001_headshape.pos
            sub-control01_ses-001_task-rest_run-01_meg
            sub-control01_ses-001_task-rest_run-01_meg.json
            sub-control01_ses-001_task-rest_run-01_channels.tsv
```

Where:

```Text
sub-control01_ses-001_task-rest_run-01_meg/
    config
    hs_file
    e,rfhp1.0Hz.COH
    c,rfDC
```

More about the 4D neuroimaging/BTi data organization at:
[http://www.fieldtriptoolbox.org/getting_started/bti](http://www.fieldtriptoolbox.org/getting_started/bti)

## KIT/Yokogawa/Ricoh

Each experimental run on a KIT/Yokogawa/Ricoh system yields a raw
(`.sqd`, `.con`) file with its associated marker coil file(s) (`.sqd`, `.mrk`),
which contains coil positions in the acquisition system’s native space.
Head points and marker points in head space are acquired using third-party
hardware.

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_scans.tsv
        meg/
            sub-control01_ses-001_coordsystem.json
            sub-control01_ses-001_headshape.txt
            sub-control01_ses-001_task-rest_run-01_meg
            sub-control01_ses-001_task-rest_run-01_meg.json
            sub-control01_ses-001_task-rest_run-01_channels.tsv
            sub-control01_ses-001_task-rest[_acq-<label>]_run-01_markers.<mrk,sqd>
            sub-control01_ses-001_task-rest_run-01_meg.<con,sqd>
```

If there are files with multiple marker coils, the marker files must have the
`acq-<label>` parameter and no more that two marker files may be associated with
one raw data file.
While the acquisition parameter can take any value, it is RECOMMENDED that if
the two marker measurements occur before and after the raw data acquisition,
`pre` and `post` are used to differentiate the two situations.

More about the KIT/Yokogawa/Ricoh data organization at:
[http://www.fieldtriptoolbox.org/getting_started/yokogawa](http://www.fieldtriptoolbox.org/getting_started/yokogawa)

## KRISS

Each experimental run on the KRISS system produces a file with extension
`.kdf`. Additional files can be available in the same folder: the digitized
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

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_scans.tsv
        meg/
            sub-control01_ses-001_coordsystem.json
            sub-control01_ses-001_headshape.txt
            sub-control01_ses-001_task-rest_run-01_meg
            sub-control01_ses-001_task-rest_run-01_meg.json
            sub-control01_ses-001_task-rest_run-01_channels.tsv
            sub-control01_ses-001_task-rest_run-01_meg.chn
            sub-control01_ses-001_task-rest_run-01_meg.kdf
            sub-control01_ses-001_task-rest_run-01_meg.trg
            sub-control01_ses-001_task-rest_digitizer.txt
```

## ITAB

Each experimental run on a ITAB-ARGOS153 system yields a raw (`.raw`) data file
plus an associated binary header file (`.mhd`). The raw data file has an ASCII
header that contains detailed information about the data acquisition system,
followed by binary data. The associated binary header file contains part of the
information from the ASCII header, specifically the one needed to process data,
plus other information on offline preprocessing performed after data acquisition
(e.g., sensor position relative to subject’s head, head markers, stimulus
information).

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_coordsystem.json
        sub-control01_ses-001_headshape.txt
        sub-control01_ses-001_task-rest_run-01_meg
        sub-control01_ses-001_task-rest_run-01_meg.json
        sub-control01_ses-001_task-rest_run-01_channels.tsv
        sub-control01_ses-001_task-rest_run-01_meg.raw
        sub-control01_ses-001_task-rest_run-01_meg.raw.mhd
```

## Aalto MEG–MRI

For stand-alone MEG data, the Aalto hybrid device uses the standard `.fif` data
format and follows the conventions of Elekta/Neuromag as described
[above](06-meg-file-formats.md#neuromagelektamegin). The `.fif` files may
contain unreconstructed MRI data. The inclusion of MRI data and information for
accurate reconstruction will be fully standardized at a later stage.
