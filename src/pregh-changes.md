## [1.1.1](https://doi.org/10.5281/zenodo.3759805) (2018-06-06)

-   Improved the MEG landmark coordinates description.
-   Replaced `ManufacturersCapModelName` in `meg.json` with `CapManufacturer` and `CapManufacturersModelName`.
-   Remove `EEGSamplingFrequency` and `ManufacturersAmplifierModelName` from the `meg.json.`
-   Improved the behavioral data description.

## [1.1.0](https://doi.org/10.5281/zenodo.3759802) (2018-04-19)

-   Added support for MEG data (merged BEP008)
-   Added `SequenceName` field.
-   Added support for describing events with Hierarchical Event Descriptors [[4.3 Task events](04-modality-specific-files/05-task-events.md)].
-   Added `VolumeTiming` and `AcquisitionDuration` fields [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `DwellTime` field.

## [1.0.2](https://doi.org/10.5281/zenodo.3759801) (2017-07-18)

-   Added support for high resolution (anatomical) T2star images [[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added support for multiple defacing masks [[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added optional key and metadata field for contrast enhanced structural scans [[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)]
-   Added `DelayTime` field [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added support for multi echo BOLD data [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].

## [1.0.1](https://doi.org/10.5281/zenodo.3759788) (2017-03-13)

-   Added `InstitutionName` field [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `InstitutionAddress` field [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `DeviceSerialNumber` field [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `NumberOfVolumesDiscardedByUser` and `NumberOfVolumesDiscardedByScanner` field [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].
-   Added `TotalReadoutTime to` functional images metadata list [[4.1 Task (including resting state) imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#task-including-resting-state-imaging-data)].

## 1.0.1-rc1

-   Added T1 Rho maps [[4.1 Anatomy imaging data](04-modality-specific-files/01-magnetic-resonance-imaging-data.md#anatomy-imaging-data)].
-   Added support for phenotypic information split into multiple files [[3.2 Participant key file](03-modality-agnostic-files.md#participants-file)].
-   Added recommendations for multi site datasets
-   Added `SoftwareVersions`
-   Added `run-<run_index>` to the phase encoding maps. Improved the description.
-   Added `InversionTime` metadata key.
-   Clarification on the source vs raw language.
-   Added `trial_type` column to the event files.
-   Added missing `sub-<participant_label>` in behavioral data file names
-   Added ability to store stimuli files.
-   Clarified the language describing allowed subject labels.
-   Added quantitative proton density maps.

## [1.0.0](https://doi.org/10.5281/zenodo.3686062) (2016-06-23)

-   Added ability to specify fieldmaps acquired with multiple parameter sets.
-   Added ability to have multiple runs of the same fieldmap.
-   Added FLASH anatomical images.

## 1.0.0-rc4

-   Replaced links to neurolex with explicit DICOM Tags.
-   Added sourcedata.
-   Added data dictionaries.
-   Be more explicit about contents of JSON files for structural (anatomical) scans.

## 1.0.0-rc3

-   Renamed `PhaseEncodingDirection` values from "x", "y", "z" to "i", "j", "k" to avoid confusion with FSL parameters
-   Renamed `SliceEncodingDirection` values from "x", "y", "z" to "i", "j", "k"

## 1.0.0-rc2

-   Removed the requirement that TSV files cannot include more than two consecutive spaces.
-   Refactor of the definitions sections (copied from the manuscript)
-   Make support for uncompressed `.nii` files more explicit.
-   Added `BIDSVersion` to `dataset.json`
-   Remove the statement that `SliceEncodingDirection` is necessary for slice time correction
-   Change dicom converter recommendation from dcmstack to dcm2nii and dicm2nii following interactions with the community (see [https://github.com/moloney/dcmstack/issues/39](https://github.com/moloney/dcmstack/issues/39) and [https://github.com/neurolabusc/dcm2niix/issues/4](https://github.com/neurolabusc/dcm2niix/issues/4)).
-   Added section on behavioral experiments with no accompanying MRI acquisition
-   Add `_magnitude.nii[.gz]` image for GE type fieldmaps.
-   Replaced EchoTimeDifference with EchoTime1 and EchoTime2 (SPM toolbox requires this input).
-   Added support for single band reference image for DWI.
-   Added DatasetDOI field in the dataset description.
-   Added description of more metadata fields relevant to DWI fieldmap correction.
-   PhaseEncodingDirection is now expressed in "x", "y" etc. instead of "PA" "RL" for DWI scans (so it's the same as BOLD scans)
-   Added `rec-<label>` flag to BOLD files to distinguish between different reconstruction algorithms (analogous to anatomical scans).
-   Added recommendation to use `_physio` suffix for continuous recordings of motion parameters obtained by the scanner side reconstruction algorithms.

## 1.0.0-rc1

-   Initial release
