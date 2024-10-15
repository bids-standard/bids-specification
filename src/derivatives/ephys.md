# Electrophysiology data types

This section pertains to human electrophysiological data, including EEG, MEG and iEEG, which characteristically have channels and time.
This includes minimally processed data, but excludes data that has undergone extensive processing, such as source reconstruction.

## Minimally processed  electrophysiological data

A minimally processed EEG, MEG or iEEG data can be stored as a derivative using the same file formats as specified for raw EEG, MEG, or iEEG.
Examples of this are MaxFiltered MEG data or re-referenced and bandpass-filtered EEG data.
Certain file formats that are allowed in BIDS for raw data have limited representation to some extent,
for example, the EDF and BDF formats cannot be used to store epoched (or "segmented") data in a standardized way,
whereas the EEGLAB .set, the BrainVision Core Data Format 1.0 and the FIF file formats can.
These limitations should be taken into account when writing derivative data back to disk.
The representation of the data MUST follow the general derivative conventions and the Common file-level metadata fields,
notably the use of the [`desc` entity](../appendices/entities.md#desc).

If minimally processed data is the result of processing a BIDS dataset, then it MUST be marked as a derivative dataset in the dataset_description.json file, and the source data must be specified.
The processing steps MUST be indicated in the [`desc` entity](../appendices/entities.md#desc),
where the label is a description identifier that distinguishes it from the original raw data.

If minimal processing was performed on the source data,
but the raw data itself does not exist as a BIDS dataset,
then the minimally processed data MAY be marked as a raw BIDS dataset.
When represented as a raw BIDS dataset,
the [`desc` entity](../appendices/entities.md#desc) is not needed to distinguish the data and MUST NOT be used.

The description of the processing in the derivative MUST be clarified in the [descriptions.tsv](common-data-types.md#descriptions-tsv) file,
with at least two columns for desc_id and the actual description.
Other columns MAY be added but are, at this moment, not standardized.
The [descriptions.tsv](common-data-types.md#descriptions-tsv) file SHOULD include sufficient information to document the details of the data processing that resulted in the derivative.

The `_eeg.json`, `_meg.json`, or `_ieeg.json` sidecar files MUST be replicated alongside the respective derivative `_eeg.<ext>`, `_meg.<ext>`, or `_ieeg.<ext>` data files,
so that they can be processed as if it were a raw BIDS dataset.
The JSON sidecar file must be compliant with those for raw data and SHOULD NOT include fields that are specific to the processing that was done on the data.

## MaxFiltered MEG data

to be done

## Other sections (to be done)

to be done
