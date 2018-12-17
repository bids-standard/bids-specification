# Electroencephalography (EEG)

Support for EEG was developed as a BIDS Extension Proposal. Please cite the
following paper when referring to this part of the standard in context of the
academic literature:

> Pernet, C. R., Appelhoff, S., Flandin, G., Phillips, C., Delorme, A., &
> Oostenveld, R. (2018, December 6). BIDS-EEG: an extension to the Brain
> Imaging Data Structure (BIDS) Specification for electroencephalography.
> [https://doi.org/10.31234/osf.io/63a4y](https://doi.org/10.31234/osf.io/63a4y)

## EEG recording data

Template:

```Text
sub-<label>/
    [ses-<label>]/
      eeg/
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_eeg.<manufacturer_specific_extension>
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_eeg.json
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_channels.tsv
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_electrodes.tsv
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_coordsystem.json
        sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_photo.jpg

```

While there are many file formats to store EEG data, there are two officially
supported data formats in EEG-BIDS: The [European data format](https://www.edfplus.info/)
(`.edf`), and the [BrainVision data format](https://www.brainproducts.com/productdetails.php?id=21&tab=5)
(`.vhdr`, `.vmrk`, `.eeg`) by Brain Products GmbH. There are also two
*unofficial* data formats that are currently accepted: The format used by the
MATLAB toolbox [EEGLAB](https://sccn.ucsd.edu/eeglab) (`.set` and `.fdt` files)
and the [Biosemi](https://www.biosemi.com/) data format (`.bdf`). The original
data format, if different from the supported formats, can be stored in the
`/sourcedata` directory.

The original data format is especially valuable in case conversion elicits the
loss of crucial metadata specific to manufacturers and specific EEG systems. We
also encourage users to provide additional meta information extracted from the
manufacturer specific data files in the sidecar JSON file. Other relevant files
MAY be included alongside the EEG data.

Note that for proper documentation of EEG recording metadata it is important to
understand the difference between electrode and channel: An EEG electrode is
attached to the skin, whereas a channel is the combination of the analog
differential amplifier and analog-to-digital converter that result in a
potential (voltage) difference that is stored in the EEG dataset. We employ
the following short definitions:

- Electrode = A single point of contact between the acquisition system and the
  recording site (e.g., scalp, neural tissue, ...). Multiple electrodes can be
  organized as caps (for EEG), arrays, grids, leads, strips, probes, shafts,
  etc.
- Channel = A single analogue-digital-converter in the recording system that
  regularly samples the value of a transducer, which results in a signal being
  represented as a time series in the data. This can be connected to two
  electrodes (to measure the potential difference between them), a magnetic
  field or magnetic gradient sensor,  temperature sensor, accelerometer, etc.

Although the "reference" and "ground" are often referred to as channels, they
are in most common EEG systems not amplified and recorded by themselves, and
therefore should not be represented as channels but as electrodes. The type of
referencing and optionally the location of the reference electrode and the
location of the ground electrode MAY be specified.  
