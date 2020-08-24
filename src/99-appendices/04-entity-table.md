# Appendix IV: Entity table

This section compiles the entities (key-value pairs) described throughout this
specification, and establishes a common order within a filename. 
For example, if a file has an acquisition and reconstruction label, the
acquisition entity must precede the reconstruction entity.
REQUIRED and OPTIONAL entities for a given file type are denoted.
Entity formats indicate whether the value is alphanumeric
(`<label>`) or numeric (`<index>`).

A general introduction to entities is given in the section on
[file name structure](../02-common-principles.md#file-name-structure)

## Magnetic Resonance Imaging

| Entity                                                                                         | Subject       | Session       | Task           | Acquisition   | Contrast Enhancing Agent   | Reconstruction   | Phase-Encoding Direction   | Run           | Corresponding Modality   | Echo           | Recording           | Part           |
|------------------------------------------------------------------------------------------------|---------------|---------------|----------------|---------------|----------------------------|------------------|----------------------------|---------------|--------------------------|----------------|---------------------|----------------|
| Format                                                                                         | `sub-<label>` | `ses-<label>` | `task-<label>` | `acq-<label>` | `ce-<label>`               | `rec-<label>`    | `dir-<label>`              | `run-<index>` | `mod-<label>`            | `echo-<index>` | `recording-<label>` | `part-<label>` |
| anat<br>(T1w T2w T1rho T1map T2map T2star FLAIR FLASH PD PDmap PDT2 inplaneT1 inplaneT2 angio) | REQUIRED      | OPTIONAL      |                | OPTIONAL      | OPTIONAL                   | OPTIONAL         |                            | OPTIONAL      |                          |                |                     | OPTIONAL       |
| anat<br>(defacemask)                                                                           | REQUIRED      | OPTIONAL      |                | OPTIONAL      | OPTIONAL                   | OPTIONAL         |                            | OPTIONAL      | OPTIONAL                 |                |                     |                |
| dwi<br>(dwi sbref)                                                                             | REQUIRED      | OPTIONAL      |                | OPTIONAL      |                            |                  | OPTIONAL                   | OPTIONAL      |                          |                |                     | OPTIONAL       |
| fmap<br>(phasediff phase1 phase2 magnitude1 magnitude2 magnitude fieldmap)                     | REQUIRED      | OPTIONAL      |                | OPTIONAL      |                            |                  |                            | OPTIONAL      |                          |                |                     |                |
| fmap<br>(epi)                                                                                  | REQUIRED      | OPTIONAL      |                | OPTIONAL      | OPTIONAL                   |                  | REQUIRED                   | OPTIONAL      |                          |                |                     |                |
| func<br>(cbv sbref)                                                                            | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL                   | OPTIONAL         | OPTIONAL                   | OPTIONAL      |                          | OPTIONAL       |                     | OPTIONAL       |
| func<br>(bold phase events)                                                                    | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL                   | OPTIONAL         | OPTIONAL                   | OPTIONAL      |                          | OPTIONAL       |                     |                |
| func<br>(physio stim)                                                                          | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      |                            | OPTIONAL         |                            | OPTIONAL      |                          |                | OPTIONAL            |                |

## Encephalography (EEG, iEEG, and MEG)

| Entity                     | Subject       | Session       | Task           | Acquisition   | Run           | Processed (on device)   | Space           | Split           |
|----------------------------|---------------|---------------|----------------|---------------|---------------|-------------------------|-----------------|-----------------|
| Format                     | `sub-<label>` | `ses-<label>` | `task-<label>` | `acq-<label>` | `run-<index>` | `proc-<label>`          | `space-<label>` | `split-<index>` |
| eeg<br>(eeg)               | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL      |                         |                 |                 |
| ieeg<br>(ieeg)             | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL      |                         |                 |                 |
| meg<br>(meg)               | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL      | OPTIONAL                |                 | OPTIONAL        |
| meg<br>(headshape)         | REQUIRED      | OPTIONAL      |                | OPTIONAL      |               |                         | OPTIONAL        |                 |
| meg<br>(markers)           | REQUIRED      | OPTIONAL      | OPTIONAL       | OPTIONAL      |               |                         | OPTIONAL        |                 |
| channels<br>(meg eeg ieeg) | REQUIRED      | OPTIONAL      | REQUIRED       |               | OPTIONAL      |                         |                 |                 |
| electrodes<br>(eeg ieeg)   | REQUIRED      | OPTIONAL      |                | OPTIONAL      |               |                         | OPTIONAL        |                 |
| events<br>(meg eeg ieeg)   | REQUIRED      | OPTIONAL      | REQUIRED       |               | OPTIONAL      |                         |                 |                 |
| photo<br>(meg eeg ieeg)    | REQUIRED      | OPTIONAL      |                | OPTIONAL      |               |                         |                 |                 |

## Behavioral Data

| Entity               | Subject       | Session       | Task           | Acquisition   | Run           | Recording           |
|----------------------|---------------|---------------|----------------|---------------|---------------|---------------------|
| Format               | `sub-<label>` | `ses-<label>` | `task-<label>` | `acq-<label>` | `run-<index>` | `recording-<label>` |
| beh<br>(stim physio) | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL      | OPTIONAL            |
| beh<br>(events beh)  | REQUIRED      | OPTIONAL      | REQUIRED       | OPTIONAL      | OPTIONAL      |                     |
