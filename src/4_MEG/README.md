Magnetoencephalography (MEG)
----------------------------

Support for MEG was developed as a BIDS Extension Proposal. Please cite the following paper when referring to this part of the standard in context of the academic literature:

> Niso Galan, J.G., Gorgolewski, K.J., Bock, E., Brooks, T.L., Flandin, G., Gramfort, A., Henson, R.N., Jas, M., Litvak, V., Moreau, J., Oostenveld, R., Schoffelen, J.-M., Tadel, F., Wexler, J., Baillet, S., 2018. [MEG-BIDS, the brain imaging data structure extended to
> magnetoencephalography](https://www.nature.com/articles/sdata2018110). Scientific Data volume 5, Article number: 180110 (2018)

### 8.4.1 MEG recording data
Template:

```
sub-<participant_label>/
    [ses-<label>]/
      meg/
        sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_meg.<manufacturer_specific_extension>
        [sub-<participant_label>[_ses-<label>]_task-<task_label>[_acq-<label>][_run-<index>][_proc-<label>]_meg.json]
```


Unprocessed MEG data MUST be stored in the native file format of the MEG instrument with which the data was collected. With MEG-BIDS, we wish to promote the adoption of good practices in the management of scientific data. Hence, the emphasis of MEG-BIDS is not to impose a new, generic data format for the  modality, but rather to standardize the way data is stored in repositories. Further, there is currently no widely accepted standard file format for MEG, but major software applications, including free and open-source solutions for MEG data analysis provide readers of such raw files.

Some software reader may skip important metadata that is specific to MEG system manufacturers. It is therefore RECOMMENDED that users provide additional meta information extracted from the manufacturer raw data files in a sidecar JSON file. This allows for easy searching and indexing of key metadata elements without the need to parse files in proprietary data format. Other relevant files MAY be included alongside the MEG data; examples are provided below.

This template is for MEG data of any kind, including but not limited to task-based, resting-state, and noise recordings. If multiple Tasks were performed within a single Run, the task description can be set to `task-multitask`.  The _meg.json SHOULD contain details on the Tasks. Some manufacturers data storage conventions use folders which contain data files of various nature: e.g., CTF’s .ds format, or 4D/BTi. Please refer to Appendix VI for examples from a selection of MEG manufacturers.

The `proc` label is analogous to `rec` for MR and denotes a variant of a file that was a result of particular processing performed on the device. This is useful for files produced in particular by Elekta’s MaxFilter (e.g. sss, tsss, trans, quat, mc, etc.), which some installations impose to be run on raw data because of active shielding software corrections before the MEG data can actually be exploited.
