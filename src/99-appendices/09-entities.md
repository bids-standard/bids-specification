# Appendix IX: Entities

This appendix defines the entities available in the specification.

## sub

The `sub-<label>` key/value pair refers to the subject identifier.

## ses

The `ses-<label>` key/value pair refers to the session identifier.

## task

Each task has a unique label that MUST only consist of letters and/or numbers (other characters, including spaces and underscores, are not allowed).
Those labels MUST be consistent across subjects and sessions.

## acq

The `acq-<label>` key/value pair corresponds to a custom label one may use to distinguish different set of parameters used for acquiring the same task.
For example this should be used when a study includes two resting state images - one single band and one multiband.
In such case two files could have the following names: `sub-01_task-rest_acq-singleband_bold.nii.gz` and `sub-01_task-rest_acq-multiband_bold.nii.gz`, however the user is MAY choose any other label than singleband and multiband as long as they are consistent across subjects and sessions and consist only of the legal label characters.

## ce

The `ce-<label>` key/value pair can be used to distinguish sequences using different contrast enhanced images.
The label is the name of the contrast agent.
The key `ContrastBolusIngredient` MAY be also be added in the JSON file, with the same label.

## rec

The `rec-<label>` key/value pair can be used to distinguish different reconstruction algorithms (for example ones using motion correction).

## dir

The `dir-<label>` key/value pair can be set to arbitrary alphanumeric label (`[a-zA-Z0-9]+` for example `LR` or `AP`) that can help users to distinguish between different files, but should not be used to infer any scanning parameters (such as phase encoding directions) of the corresponding sequence.

## run

If more than one run of the same task has been acquired a key/value pair: `_run-1`, `_run-2`, `_run-3` etc. MUST be used.
If only one run was acquired the `run-<index>` can be omitted.
In the context of functional imaging a run is defined as the same task, but in some cases it can mean different set of stimuli (for example randomized order) and participant responses.

## mod

The `mod-<label>` key/value pair is used to denote the modality suffix of the origin of a defacemask file.
If the structural images included in the dataset were defaced (to protect identity of participants) one MAY provide the binary mask that was used to remove facial features in the form of `_defacemask` files.
In such cases, the OPTIONAL `mod-<label>` key/value pair corresponds to modality suffix, such as T1w or inplaneT1, referenced by the defacemask image.
For example, `sub-01_mod-T1w_defacemask.nii.gz`.

## echo

Multi-echo data MUST be split into one file per echo.
Each file shares the same name with the exception of the `echo-<index>` key/value.

## recording

## proc

The `proc-<label>` key/value pair is analogous to `rec` for MR and denotes a variant of a file that was a result of particular processing performed on the device.
This is useful for files produced in particular by Elekta’s MaxFilter (e.g. sss, tsss, trans, quat, mc, etc.), which some installations impose to be run on raw data because of active shielding software corrections before the MEG data can actually be exploited.

## space

The final frontier.

## split

Some manufacturers' data storage conventions use folders which contain data files of various nature: for example, CTF's .ds format, or BTi/4D.
Yet other manufacturers split their files once they exceed a certain size limit.
For example Neuromag/Elekta/Megin, which can produce several files for a single recording.
Both some_file.fif and some_file-1.fif would belong to a single recording.
In BIDS, the `split-<index>` key/value pair is RECOMMENDED to deal with split files.
