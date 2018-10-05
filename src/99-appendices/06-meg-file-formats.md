# Appendix VI: MEG file formats

Each MEG system brand has specific file organization and data formats.
RECOMMENDED values for `manufacturer_specific_extensions`:

| Value  | Definition                                                                            |
| ------ | ------------------------------------------------------------------------------------- |
| `ctf`  | CTF (folder with `.ds` extension)                                                     |
| `fif`  | Neuromag / Elekta / MEGIN  and BabyMEG (file with extension `.fif`)                   |
| `4d`   | BTi / 4D Neuroimaging (folder containing multiple files without extensions)           |
| `kit`  | KIT / Yokogawa / Ricoh (file with extension `.sqd`, `.con`, `.raw`, `.ave` or `.mrk`) |
| `kdf`  | KRISS (file with extension `.kdf`)                                                    |
| `itab` | Chieti system (file with extension `.raw` and `.mhd`)                                 |

Below are specifications for each system brand.

## CTF

Each experimental run with a CTF system yields a folder with a `.ds` extension,
containing several files. The (optional) digitized positions of the head points
are usually stored in a separate `.pos` file, not necessarily within the `.ds`
folder.

```Text
[sub-<participant_label>[_ses-<label>]_headshape.pos]
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.ds>
```

CTF’s data storage is therefore via directories containing multiple files. The
files contained within a .ds directory are named such that they match the parent
directory, but conserve the original file extension (e.g., `.meg4`, `.res4`,
etc.). The renaming of CTF datasets SHOULD be done using the CTF newDs
command-line application.

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
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.fif
```

Note that we do not provide specific specifications for cross-talk and
fine-calibration matrix files in the present MEG-BIDS version.

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
the corresponding label (e.g. `proc-sss`) and placed into a `derivatives`
subfolder.

Example:

```Text
sub-control01_ses-001_task-rest_run-01_proc-sss_meg.fif
sub-control01_ses-001_task-rest_run-01_proc-sss_meg.json
```

In the case of data runs exceeding 2Gb, the data is stored in two separate
files:

```Text
sub-control01_ses-001_task-rest_run-01_meg.fif
sub-control01_ses-001_task-rest_run-01_meg-1.fif
```

Each of these two files has a pointer to the next file. In some software
applications, like MNE, one can simply specify the name of the first file, and
data will be read in both files via this pointer. For this reason, it is
RECOMMENDED to rename and write back the file once read, to avoid the
persistence of a pointer associated with the old file name.

Naming convention:

```Text
sub-control01_ses-001_task-rest_run-01_part-01_meg.fif
sub-control01_ses-001_task-rest_run-01_part-02_meg.fif
```

More about the Neuromag/Elekta/MEGIN data organization at:
[http://www.fieldtriptoolbox.org/getting_started/neuromag](http://www.fieldtriptoolbox.org/getting_started/neuromag)
And BabyMEG :
[http://www.fieldtriptoolbox.org/getting_started/babysquid](http://www.fieldtriptoolbox.org/getting_started/babysquid)

## BTi/4D neuroimaging

Each experimental run on a 4D neuroimaging/BTi system results in a folder
containing multiple files without extensions.

```Text
[sub-<participant_label>[_ses-<label>]_headshape.pos]
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg>
```

One SHOULD rename/create a father run specific directory and keep the original
files for each run inside (e.g. "c,rfhp0.1Hz", "config" and "hs_file").

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

Each experimental run on a KIT/Yokogawa/Ricoh system yields a raw (`.sqd`,
`.con`) file with its associated marker coil file (`.mrk`), which contains coil
positions in the acquisition system’s native space. Head points and marker
points in head space are acquired using third-party hardware. One SHOULD
rename/create a father run specific directory and keep the original files for
each run inside.

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
```

Where:

```Text
sub-control01_ses-001_task-rest_run-01_meg/
    sub-control01_ses-001_task-rest_run-01_markers.<mrk,sqd>
    sub-control01_ses-001_task-rest_run-01_meg.<con,sqd>
```

More about the KIT/Yokogawa/Ricoh data organization at:
[http://www.fieldtriptoolbox.org/getting_started/yokogawa](http://www.fieldtriptoolbox.org/getting_started/yokogawa)

## KRISS

Each experimental run on the KRISS system produces a file with extension .kdf.
Additional files can be available in the same folder: the digitized positions of
the head points (\_digitizer.txt), the position of the center of the MEG coils
(.chn) and the event markers (.trg).

```Text
[sub-<participant_label>[_ses-<label>]_headshape.txt]
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.kdf
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.chn
sub-<participant_label>[_ses-<label>]_task-<task_label>[_run-<index>]_meg.trg
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
```

Where:

```Text
sub-control01_ses-001_task-rest_run-01_meg/
    sub-control01_ses-001_task-rest_run-01_meg.chn
    sub-control01_ses-001_task-rest_run-01_meg.kdf
    sub-control01_ses-001_task-rest_run-01_meg.trg
```

## ITAB

Each experimental run on a ITAB-ARGOS153 system yields a raw (`.raw`) data file
plus an associated binary header file (`.mhd`). The raw data file has an ASCII
header that contains detailed information about the data acquisition system,
followed by binary data. The associated binary header file contains part of the
information from the ASCII header, specifically the one needed to process data,
plus other information on offline preprocessing performed after data acquisition
(e.g., sensor position relative to subject’s head, head markers, stimulus
information). One should rename/create a father run specific directory and keep
the original files for each run inside.

Example:

```Text
sub-control01/
    ses-001/
        sub-control01_ses-001_coordsystem.json
        sub-control01_ses-001_headshape.txt
        sub-control01_ses-001_task-rest_run-01_meg
        sub-control01_ses-001_task-rest_run-01_meg.json
        sub-control01_ses-001_task-rest_run-01_channels.tsv
```

Where:

```Text
sub-control01_ses-001_task-rest_run-01_meg/
    sub-control01_ses-001_task-rest_run-01_meg.raw
    sub-control01_ses-001_task-rest_run-01_meg.raw.mhd
```

## Aalto MEG–MRI

For stand-alone MEG data, the Aalto hybrid device uses the standard `.fif` data
format and follows the conventions of Elekta/Neuromag as described above in
section 5.2. The `.fif` files may contain unreconstructed MRI data. The
inclusion of MRI data and information for accurate reconstruction will be fully
standardized at a later stage.
