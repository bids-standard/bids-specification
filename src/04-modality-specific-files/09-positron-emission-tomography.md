# Positron Emission Tomography

Support for Positron Emission Tomography (PET) was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

The following example PET datasets have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

-   One subject single dynamic scan (pet, mri, blood):
	[`pet_example1`](https://www.dropbox.com/sh/dmjmaxfswatptpm/AACw31cTyChLA1kwM4Vhqueja?dl=0)
-   One subject single dynamic scan (pet, mri):
	[`pet_example2`](https://www.dropbox.com/sh/i95a71rpq2unks7/AACby5XcYQp9vcwgx3cNXBhza?dl=0)
-   One subject single dynamic scan (pet, blood):
	[`pet_example3`](https://www.dropbox.com/sh/i0c3iq50id4s0d3/AABSjaczHM1SQnMRvh3fc7fna?dl=0)

Further PET datasets are available from [OpenNeuro](https://openneuro.org).

## PET recording data

Template:

```Text
sub-<participant_label>/
      [ses-<session_label>/]
        pet/
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.nii[.gz]
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.json
```

**Shared MRI data along with PET:**
To share structural magnetic resonance (MR) images with your PET data,
please follow the original BIDS specification
([LINK](https://bids-specification.readthedocs.io/en/stable)).
Please pay specific attention to whether the MR images have been unwarped to correct for gradient non-linearities. This should be specified in a specific field of the MRI-BIDS .json file named "NonLinearGradientCorrection". For more information please see the appendix regarding cross modality correspondence
 ([LINK](../99-appendices/13-cross-modality-correspondence.md)).

**Units**: In general, SI units must be used (we refer to [LINK](https://bids-specification.readthedocs.io/en/stable/99-appendices/05-units.html)) and we recommend to use the CMIXF style formatting for SI units, for example, "kBq/mL"
rather than "kilobecquerel per ml".
An overview of a common PET experiment (with blood data) can be seen in Figure 1,
defined on a single time scale relative to a predefined “time zero”
(which should be defined either to be scan start or injection time;
please note an exception to this definition is possible if a pharmacological
within-scan challenge is performed).

![Figure 1](images/PET_scan_overview.svg "Overview of PET recording data")

Figure 1: Overview of a common PET experiment, including blood measurements,
and defined on a common time scale.
Note, “time zero” can either be defined as time of injection or scan start,
and all the PET and blood data should be decay-corrected to this time point.
Furthermore, although in this example tracer injection coincides with scan start,
this is not always the case and hence we allow for the flexibility of specifying
either time of injection or scan start as “time zero”.

PET data belong to the `pet` directory. PET imaging data SHOULD be stored in 4D
(or 3D if only one volume was acquired) NIfTI files with `_pet` suffix.
Volumes should be stored in chronological order (the order they were acquired in).

Following the [BIDS Common Principles](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html), here we summarize how different labels are organized for PET data. Please, check the Common Principles section for further details.
**Sessions**: Multiple sessions (visits) are encoded by adding an extra layer of directories
and file names in the form of `ses-<label>`.
Session labels can consist only of alphanumeric characters [a-zA-Z0-9]
and should be consistent across subjects.
If numbers are used in session labels we recommend using zero padding
(for example, `ses-01`, `ses-11` instead of `ses-1`, `ses-11`).
This makes results of alphabetical sorting more intuitive.
The extra session layer (at least one `ses-<label>` subfolder) should be added
for all subjects if at least one subject in the dataset has more than one session.
Skipping the session layer for only some subjects in the dataset is not allowed.
If a `ses-<label>` subfolder is included as part of the directory hierarchy,
then the same `ses-<label>` tag must also be included as part of the file names themselves.
In general, we assume that a new session with respect to PET starts with either a new injection
(probably most common case) or with the subject being taken out of the scanner
(same injection, but subject leaves the scanner and returns).
However, for example, if a subject has to leave the scanner room and
then be re-positioned on the scanner bed, for example, to use the bathroom,
the set of PET acquisitions will still be considered as a session and match
sessions acquired in other subjects.
Similarly, in situations where different data types are obtained over several
visits (for example, FDG PET on one day followed by amyloid PET a couple days after)
those can be grouped in one session.
Please see the difference with the `run-<label>` below.

**Task:** With respect to the `task-<label>`, data is arranged in a similar way as task-based
and resting state BOLD fMRI data.
In case of studies using combined PET/fMRI, subject-specific tasks may be carried out
during the acquisition within the same session.
Therefore, it is possible to specify `task-<label>` in accordance with the fMRI data.
For more information please see the [BIDS specification for MRI](https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#task-including-resting-state-imaging-data).

**Acquisition:** In case of studies with multiple acquisitions per subject using different tracers,
the `acq-<label>` must be used to distinguish between different tracers.
Please keep in mind that the label used is arbitrary and each file requires
a separate JSON sidecar with details of the tracer used (see below).
Examples are `acq-18FFDG` for fludeoxyglucose, `acq-11CPIB` for Pittsburgh compound B, etc.

**Reconstruction:** The reconstruction key (`recon-<label>`) has four reserved values:
- `acdyn`, for reconstructions with attenuation correction of dynamic data;
- `acstat`, for reconstructions with attenuation correction of static data;
- `nacdyn`, for reconstructions without attenuation correction of dynamic data;
- `nacstat`, for reconstructions without attenuation correction of static data.
Further details regarding reconstruction are in the `_pet.json` file.
In case of multiple reconstructions of the data with the same type,
we allow for using a number after the `<label>` in order to distinguish,
for example `recon-acdyn1` and `recon-acdyn2`.

**Run:** The run entity is used if one scan type/contrast is repeated multiple times
within the same scan session/visit.
If several scans of the same modality are acquired they MUST be indexed
with a key-value pair: `_run-1`, `_run-2`, `_run-3` etc. (only integers are allowed as run labels).
When there is only one scan of a given type the run key MAY be omitted.
An example of this would be two consecutive scans performed within the same session,
for example two short FDG scans right after each other.
It is our assumption that the `run-<label>` is used in PET for the cases
where the subject does not leave the scanner.
Otherwise, we refer to the `ses-<label>` definition.

In addition to the imaging data (*.nii) a `_pet.json` sidecar file needs to be provided.
The included metadata are divided into sections described below.

### PET sidecar JSON (`*_pet.json`)

#### Information

This section is mandatory and contains general information about the imaging experiment.

Some of the fields are marked optional (MAY), for example anaesthesia; for those fields
the [BIDS validator](https://github.com/bids-standard/bids-validator) will not throw an error even if they are not present.
Note, although bodyweight is a recommended information in (Knudsen et al. 2020, [doi:10.1177/0271678X20905433](https://doi.org/10.1177/0271678X20905433)),
this consists of meta information at the participant level and should hence
be part of the `participants.tsv` or `session.tsv` file in case of multiple measurements.

| **Key name**              | **Requirement level** | **Data type**                          | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ------------------------- | --------------------- | -------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Manufacturer              | REQUIRED              | [string][]                             | Scanner manufacturer (for example, "Siemens").                                                                                                                                                                                                                                                                                                                                                                                   |
| ManufacturersModelName    | REQUIRED              | [string][]                             | PET scanner model name (for example, "mMR Biograph").                                                                                                                                                                                                                                                                                                                                                                            |
| Unit                      | REQUIRED              | [string][]                             | Unit of the image file; please see BIDS main spec section 6. SI unit for radioactivity (Becquerel) should be used (for example, "Bq/mL"). Corresponds to DICOM Tag 0054, 1001 Units.                                                                                                                                                                                                                                             |
| TracerName                | REQUIRED              | [string][]                             | Name of the tracer compound used (for example, "CIMBI-36")                                                                                                                                                                                                                                                                                                                                                                       |
| TracerRadionuclide        | REQUIRED              | [string][]                             | Radioisotope labelling tracer (for example, "C11").                                                                                                                                                                                                                                                                                                                                                                              |
| InstitutionName           | RECOMMENDED           | [string][]                             | The name of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0080 InstitutionName.                                                                                                                                                                                                                                                                               |
| InstitutionAddress        | RECOMMENDED           | [string][]                             | The address of the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 0081 InstitutionAddress.                                                                                                                                                                                                                                                                         |
| InstitutionDepartmentName | RECOMMENDED           | [string][]                             | The department in the institution in charge of the equipment that produced the composite instances. Corresponds to DICOM Tag 0008, 1040 Institutional Department Name.                                                                                                                                                                                                                                                           |
| BodyPart                  | RECOMMENDED           | [string][]                             | Body part of the organ / body region scanned. Corresponds to DICOM Tag 0018, 0015 Body Part Examined                                                                                                                                                                                                                                                                                                                             |
| TracerRadLex              | RECOMMENDED           | [string][]                             | ID of the tracer compound from the RadLex Ontology.                                                                                                                                                                                                                                                                                                                                                                              |
| TracerSNOMED              | RECOMMENDED           | [string][]                             | ID of the tracer compound from the SNOMED Ontology (subclass of Radioactive isotope).                                                                                                                                                                                                                                                                                                                                            |
| TracerMolecularWeight     | RECOMMENDED           | [number][]                             | Accurate molecular weight of the tracer used.                                                                                                                                                                                                                                                                                                                                                                                    |
| TracerMolecularWeightUnit | RECOMMENDED           | [string][]                             | Unit of the molecular weights measurement (for example, "g/mol").                                                                                                                                                                                                                                                                                                                                                                |
| PharmaceuticalName        | RECOMMENDED           | [string][]                             | Name of pharmaceutical coadministered with tracer.                                                                                                                                                                                                                                                                                                                                                                               |
| PharmaceuticalDoseAmount  | RECOMMENDED           | [number][] or [array][] of [numbers][] | Dose amount of pharmaceutical coadministered with tracer.                                                                                                                                                                                                                                                                                                                                                                        |
| PharmaceuticalDoseUnit    | RECOMMENDED           | [string][]                             | Unit format relating to pharmaceutical dose (for example, "mg" or "mg/kg").                                                                                                                                                                                                                                                                                                                                                      |
| PharmaceuticalDoseRegimen | RECOMMENDED           | [string][]                             | Details of the pharmaceutical dose regimen. Either adequate description or short-code relating to regimen documented elsewhere (for example, "single oral bolus").                                                                                                                                                                                                                                                               |
| PharmaceuticalDoseTime    | RECOMMENDED           | [number][] or [array][] of [numbers][] | Time of administration of pharmaceutical dose, relative to time zero (please see below). For an infusion, this should be a vector with two elements specifying the start and end of the infusion period. For more complex dose regimens, the regimen description should be complete enough to enable unambiguous interpretation of the DoseTime vector. Unit format of the specified pharmaceutical dose time should be seconds. |
| Anaesthesia               | OPTIONAL              | [string][]                             | Details of anaesthesia used, if any.                                                                                                                                                                                                                                                                                                                                                                                             |

#### Radiochemistry

This section is mandatory and contains information regarding the radioactive
material used in the experiment.

| **Key name**                  | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                       |
| ----------------------------- | --------------------- | ------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| InjectedRadioactivity         | REQUIRED              | [number][]    | Total amount of radioactivity injected into the patient (for example, 400). Corresponds to DICOM Tag (0018,1074) Radionuclide Total Dose.                                                                                                             |
| InjectedRadioactivityUnit     | REQUIRED              | [string][]    | Unit format of the specified injected radioactivity (for example, "MBq").                                                                                                                                                                             |
| InjectedMass                  | REQUIRED              | [number][]    | Total mass of radiolabeled compound injected into subject (for example, 10). This can be derived as the ratio of the `InjectedRadioactivity` and `MolarRadioactivity`. **Note for an FDG acquisition this is not available and should be set to -1.** |
| InjectedMassUnit              | REQUIRED              | [string][]    | Unit format of the mass of compound injected (for example, "ug" or "umol"). **Note this is not required for an FDG acquisition, since it is not available, and can be set to "-1"**.                                                                  |
| SpecificRadioactivity         | REQUIRED              | [number][]    | Specific activity of compound injected. **Note this is not required for an FDG acquisition, since it is not available, and can be set to -1**.                                                                                                        |
| SpecificRadioactivityUnit     | REQUIRED              | [string][]    | Unit format of specified specific radioactivity (for example, "Bq/g"). **Note this is not required for an FDG acquisition, since it is not available, and can be set to "-1"**.                                                                       |
| ModeOfAdministration          | REQUIRED              | [string][]    | Mode of administration of the injection (for example, "bolus" or "infusion").                                                                                                                                                                         |
| InjectedMassPerWeight         | RECOMMENDED           | [number][]    | Injected mass per kilogram bodyweight.                                                                                                                                                                                                                |
| InjectedMassPerWeightUnit     | RECOMMENDED           | [string][]    | Unit format of the injected mass per kilogram bodyweight (for example, "ug/kg").                                                                                                                                                                      |
| SpecificRadioactivityMeasTime | RECOMMENDED           | [string][]    | Time to which specific radioactivity measurement above applies in the default unit "hh:mm:ss".                                                                                                                                                        |
| MolarActivity                 | RECOMMENDED           | [number][]    | Molar activity of compound injected. Corresponds to DICOM Tag (0018,1077) Radiopharmaceutical Specific Activity.                                                                                                                                      |
| MolarActivityUnit             | RECOMMENDED           | [string][]    | Unit of the specified molar radioactivity (for example, "Bq/g").                                                                                                                                                                                      |
| MolarActivityMeasTime         | RECOMMENDED           | [string][]    | Time to which molar radioactivity measurement above applies in the default unit "hh:mm:ss".                                                                                                                                                           |
| InfusionSpeed                 | RECOMMENDED           | [number][]    | If given, infusion speed.                                                                                                                                                                                                                             |
| InjectedVolumeUnit            | RECOMMENDED           | [string][]    | Unit of the injected volume of the radiotracer (for example, "mL").                                                                                                                                                                                   |
| Purity                        | RECOMMENDED           | [number][]    | Purity of the radiolabeled compound (for example, 90).                                                                                                                                                                                                |

#### Time

This section is mandatory and contains timing information about the imaging experiment. We refer to the common principles for the standards for describing dates and timestamps, including possibilities for anonymization ([LINK](https://bids-specification.readthedocs.io/en/stable/02-common-principles.html)).

| **Key name**    | **Requirement level** | **Data type**            | **Description**                                                                                                                                                           |
| --------------- | --------------------- | ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TimeZero        | REQUIRED              | [string][]               | Time zero to which all scan and/or blood measurements have been adjusted to, in the unit “hh:mm:ss”. This should be equal to `InjectionStart` or `ScanStart`.             |
| ScanStart       | REQUIRED              | [number][]               | Time of start of scan with respect to `TimeZero` in the default unit seconds.                                                                                             |
| InjectionStart  | REQUIRED              | [number][]               | Time of start of injection with respect to `TimeZero` in the default unit seconds. This corresponds to DICOM Tag (0018,1042) converted to seconds relative to `timeZero`. |
| FrameTimesStart | REQUIRED              | [array][] of [numbers][] | Start times for all frames relative to `TimeZero` in default unit seconds.                                                                                                |
| FrameDuration   | REQUIRED              | [array][] of [numbers][] | Time duration of each frame in default unit seconds. This corresponds to DICOM Tag (0018,1242) converted to seconds.                                                      |
| ScanDate        | RECOMMENDED           | [string][]               | Date of scan in the default unit “yyyy:mm:dd”.                                                                                                                            |
| InjectionEnd    | RECOMMENDED           | [number][]               | Time of end of injection with respect to `TimeZero` in the default unit seconds.                                                                                          |

#### Reconstruction

This optional section includes information about the image reconstruction.

All reconstruction specific parameters that are not specified, but one wants to include, should go into the `ReconMethodParameterValues` field.

| **Key name**                         | **Requirement level** | **Data type**                          | **Description**                                                                                                 |
| ------------------------------------ | --------------------- | -------------------------------------- | --------------------------------------------------------------------------------------------------------------- |
| AcquisitionMode                      | REQUIRED              | [string][]                             | Type of acquisition of the PET data (for example, `"list mode"`)                                                |
| ImageDecayCorrected                  | REQUIRED              | [boolean][]                            | Boolean flag specifying whether the image data have been decay-corrected.                                       |
| ImageDecayCorrectionTime             | REQUIRED              | [number][]                             | Point in time from which the decay correction was applied with respect to TimeZero in the default unit seconds. |
| ReconMethodName                      | REQUIRED              | [string][]                             | Reconstruction method or algorithm (for example, `"3d-op-osem"`).                                               |
| ReconMethodParameterLabels           | REQUIRED              | [array][] of [strings][]               | Names of reconstruction parameters (for example, `["subsets", "iterations"]`)                                   |
| ReconMethodParameterUnit             | REQUIRED              | [array][] of [strings][]               | Unit of reconstruction parameters (for example, `["none", "none"]`).                                            |
| ReconMethodParameterValues           | REQUIRED              | [array][] of [numbers][]               | Values of reconstruction parameters (for example, `[21, 3]`)                                                    |
| ReconFilterType                      | REQUIRED              | [string][] or [array][] of [strings][] | Type of post-recon smoothing (for example, `["Shepp"]`)                                                         |
| ReconFilterSize                      | REQUIRED              | [number][] or [array][] of [numbers][] | Kernel size of post-recon filter (FWHM).                                                                        |
| AttenuationCorrection                | REQUIRED              | [string][]                             | Short description of the attenuation correction method used.                                                    |
| ReconMethodImplementationVersion     | RECOMMENDED           | [string][]                             | Identification for the software used, such as name and version.                                                 |
| AttenuationCorrectionMethodReference | RECOMMENDED           | [string][]                             | Reference paper for the attenuation correction method used.                                                     |
| ScaleFactor                          | RECOMMENDED           | [array][] of [numbers][]               | Scale factor for each frame.                                                                                    |
| ScatterFraction                      | RECOMMENDED           | [array][] of [numbers][]               | Scatter fraction for each frame.                                                                                |
| DecayCorrectionFactor                | RECOMMENDED           | [array][] of [numbers][]               | Decay correction factor for each frame.                                                                         |
| PromptRate                           | RECOMMENDED           | [array][] of [numbers][]               | Prompt rate for each frame.                                                                                     |
| RandomRate                           | RECOMMENDED           | [array][] of [numbers][]               | Random rate for each frame.                                                                                     |
| SinglesRate                          | RECOMMENDED           | [array][] of [numbers][]               | Singles rate for each frame.                                                                                    |

#### Example (`*_pet.json`)

```JSON
{
	"Manufacturer": "Siemens",
	"ManufacturersModelName": "High-Resolution Research Tomograph (HRRT, CTI/Siemens)",
	"BodyPart": "Brain",
	"BodyWeight": 21,
	"BodyWeightUnit": "kg",
	"Unit": "Bq/mL",
	"TracerName": "CIMBI-36",
	"TracerRadionuclide": "C11",
	"TracerMolecularWeight": 380.28,
	"TracerMolecularWeightUnit": "g/mol",
	"TracerInjectionType": "bolus",
	"InjectedRadioactivity": 573,
	"InjectedRadioActivityUnit": "MBq",
	"InjectedMass": 0.62,
	"InjectedMassUnit": "ug",
	"SpecificRadioactivity": 929.6,
	"SpecificRadioactivityUnit": "MBq/ug",
	"ModeOfAdministration": "bolus",
	"MolarActivity": 353.51,
	"MolarActivityUnit": "GBq/umol",
	"MolarActivityMeasTime": "13:04:42",
	"TimeZero": "13:04:42",
	"ScanStart": 0,
	"InjectionStart": 0,
	"FrameTimesStart": [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 240, 300, 360, 420, 480, 540, 660, 780, 900, 1020, 1140, 1260, 1380, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100, 5400, 5700, 6000, 6300, 6600, 6900],
	"FrameDuration": [10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 60, 60, 60, 60, 60, 60, 120, 120, 120, 120, 120, 120, 120, 120, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
	"AcquisitionMode": "list mode",
	"ImageDecayCorrected": true,
	"ImageDecayCorrectionTime": 0,
	"ReconMethodName": "3D-OSEM-PSF",
	"ReconMethodParameterLabels": ["subsets","iterations"],
	"ReconMethodParameterUnit": ["none","none"],
	"ReconMethodParameterValues": [16,10],
	"ReconFilterType": "none",
	"AttenuationCorrection": "[137Cs]transmission scan-based"
}
```

## Blood recording data

This section includes all data needed to perform blood analysis for PET data.
The section may be omitted completely if blood measurements of radioactivity were not made.

Template:

```Text
sub-<participant_label>/
 	[ses-<session_label>/]
	pet/
	sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.tsv
	sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.json

```

Blood data belongs in the /pet folder along with the corresponding PET data.
However, the blood data also follows the [inheritance principle](../02-common-principles.md#the-inheritance-principle) and may be moved to an upper level folder
if it does not change, for example, with multiple reconstructions.
The blood data is most often recorded using an autosampler for continuous blood samples,
or manually for discrete blood samples.
Therefore, the recording key (`recording-<label>`) has two reserved values:
`autosampler`,
for continuous blood data measurements;
and `manual`, for discrete blood data.
All blood measurements should be reported according to a single time-scale
in relation to time zero defined by the PET data (Figure 1).
All definitions used below are in accordance with Innis et al. 2007 ([doi:10.1038/sj.jcbfm.9600493](https://doi.org/10.1038/sj.jcbfm.9600493)).

## Blood sidecar JSON (`*recording-(manual|autosampler)_blood.json`)

If blood measurements were made a `*recording-<label>_blood.json` file is expected that contains
information about which blood data (plasma, whole blood, and metabolites) is available as well as some blood measurement details.
These are detailed in the next sections. Different fields are customary depending on if manual or automatic blood sampling is carried out.

| **Key name**                        | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                               |
| ----------------------------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| PlasmaAvail                         | REQUIRED              | [boolean][]   | Boolean that specifies if plasma measurements are available. If this is false, all of the plasma fields should be excluded.                                                                                                                                   |
| PlasmaFreeFraction                  | RECOMMENDED           | [number][]    | Measured free fraction in plasma, meaning the concentration of free compound in plasma divided by total concentration of compound in plasma.                                                                                                                  |
| PlasmaFreeFractionMethod            | RECOMMENDED           | [string][]    | Method used to estimate free fraction.                                                                                                                                                                                                                        |
| WholeBloodAvail                     | REQUIRED              | [boolean][]   | Boolean that specifies if whole blood measurements are available.                                                                                                                                                                                             |
| MetaboliteAvail                     | REQUIRED              | [boolean][]   | Boolean that specifies if metabolite measurements are available. If this is false, all of the metabolite fields should be excluded.                                                                                                                           |
| MetaboliteMethod                    | REQUIRED              | [string][]    | Method used to measure metabolites.                                                                                                                                                                                                                           |
| MetaboliteRecoveryCorrectionApplied | REQUIRED              | [boolean][]   | Metabolite recovery correction from the HPLC, for tracers where it changes with time postinjection. If `true` please include a column named "metabolite_recovery_fractions" in the table with blood data (`*_blood.tsv`) of recovery fractions from the HPLC. |
| DispersionCorrected                 | REQUIRED              | [boolean][]   | Boolean flag specifying whether the blood data have been dispersion-corrected. NOTE: not customary for manual samples, and hence should be set to false.                                                                                                      |
| WithdrawalRate                      | RECOMMENDED           | [number][]    | The rate at which the blood was withdrawn from the subject. The unit of the specified withdrawal rate should be in mL/s.                                                                                                                                      |
| TubingType                          | RECOMMENDED           | [string][]    | Description of the type of tubing used, ideally including the material and (internal) diameter.                                                                                                                                                               |
| TubingLength                        | RECOMMENDED           | [number][]    | The length of the blood tubing, from the subject to the detector in the default unit centimeter.                                                                                                                                                              |
| DispersionConstant                  | RECOMMENDED           | [number][]    | External dispersion time constant resulting from tubing in default unit seconds.                                                                                                                                                                              |
| Haematocrit                         | RECOMMENDED           | [number][]    | Measured haematocrit, meaning the volume of erythrocytes divided by the volume of whole blood.                                                                                                                                                                |
| BloodDensity                        | RECOMMENDED           | [number][]    | Measured blood density. Unit of blood density should be in g/mL.                                                                                                                                                                                              |

### Time

If manual blood samples, for example, using a COBRA counter are available,
then time information as detailed below should be added to the `*recording-manual_blood.tsv`
and the values below should be added to the `*recording-manual_blood.json`.
If blood samples using an autosampler, for example, using an Allogg autosampler are available,
then time information as detailed below should be added to the `*recording-autosampler_blood.tsv`
and the values below should be added to the `*recording-autosampler_blood.json`.

| **Column name** | **Description**                                                              | **Units**                             |
| --------------- | ---------------------------------------------------------------------------- | ------------------------------------- |
| time            | Time in relation to `TimeZero` defined by the `*_pet.json`. (for example, 5) | Unit of time steps (for example, "s") |

### Radioactivity in plasma

This section may be omitted if plasma measurements of radioactivity were not made.
It contains information regarding sampled plasma data.
If plasma measurements are available by manual sampling, they should be added to the `*recording-blood_discrete.tsv`
and the values below should be added to the `*recording-blood_discrete.json`.
If plasma measurements are available by an autosampler, they should be added to the `*recording-blood_continous.tsv`
and the values below should be added to the `*recording-blood_continous.json`.

| **Column name**      | **Description**         | **Units**                                         |
| -------------------- | ----------------------- | ------------------------------------------------- |
| plasma_radioactivity | Radioactivity in plasma | Unit of parent fraction (for example, "unitless") |

### Metabolites

This section may be omitted if metabolite measurements were not made.
If metabolite measurements are available by manual sampling
they should be added to the `*recording-blood_discrete.tsv`
and the values below should be added to the `*recording-blood_discrete.json`.
If metabolite measurements are available by an autosampler they should be added to the `*recording-blood_continous.tsv`
and the values below should be added to the `*recording-blood_continous.json`.
Hence, it may contain information regarding metabolite info, such as the following three column examples:

| **Column name**            | **Description**                                                                   | **Units**                                                   |
| -------------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| metabolite_parent_fraction | Parent fraction of the radiotracer (0-1)                                          | Unit of parent fraction (for example, "unitless")           |
| metabolite_polar_fraction  | Polar metabolite fraction of the radiotracer (0-1)                                | Unit of polar metabolite fraction (for example, "unitless") |
| hplc_recovery_fractions    | HPLC recovery fractions (the fraction of activity that gets loaded onto the HPLC) | Unit of recovery fractions (for example, "unitless")        |

### Radioactivity in whole blood

This section may be omitted if whole blood measurements of radioactivity were not made.
It contains information regarding sampled whole blood data.
If whole blood measurements are available by manual sampling they should be added to the `*recording-manual_blood.tsv`
and the values below should be added to the `*recording-manual_blood.json`.
If whole blood measurements are available by an autosampler, they should be added to the `*recording-autosampler_blood.tsv`
and the values below should be added to the `*recording-autosampler_blood.json`.

| **Column name**           | **Description**                      | **Units**                                                                         |
| ------------------------- | ------------------------------------ | --------------------------------------------------------------------------------- |
| whole_blood_radioactivity | Radioactivity in whole blood samples | Unit of radioactivity measurements in whole blood samples (for example, "kBq/mL") |

### Example (`*_recording-manual_blood.json`)

```JSON
{
	"PlasmaAvail": true,
	"WholeBloodAvail": true,
	"MetaboliteAvail": true,
	"MetaboliteMethod": "",
	"MetaboliteRecoveryCorrectionApplied": false,
	"DispersionCorrected": false,

    "time": {
        "Description": "Time in relation to time zero defined by the _pet.json",
        "Units": "s"
    },
    "plasma_radioactivity": {
        "Description": "Radioactivity in plasma samples. Measured using COBRA counter.",
        "Units": "kBq/mL"
    },
    "whole_blood_radioactivity": {
        "Description": "Radioactivity in whole blood samples. Measured using COBRA counter.",
        "Units": "kBq/mL"
    },
    "metabolite_parent_fraction": {
        "Description": "Parent fraction of the radiotracer.",
        "Units": "arbitrary"
    },
    "metabolite_polar_fraction": {
        "Description": "Polar metabolite fraction of the radiotracer.",
        "Units": "arbitrary"
    },
    "metabolite_lipophilic_fraction": {
        "Description": "Lipophilic metabolite fraction of the radiotracer.",
        "Units": "arbitrary"
    }
}
```

### Example (`*_recording-manual_blood.tsv`)
```Text
time plasma_radioactivity whole_blood_radioactivity metabolite_parent_fraction metabolite_polar_fraction
0    0    0    1    0
145    43.31    33.79    0.5749    0.1336
292    48.96    37.42    0.3149    0.2746
602    39.84    32.05    0.1469    0.3548
1248    37.38    31.52    0.073    0.444
1785    36.40    28.83    0.078    0.429
2390    33.13    26.32    0.061    0.453
3059    30.83    25.22    0.049    0.473
4196    27.28    21.98    0.036    0.503
5407    22.70    19.49    0.032    0.523
7193    19.71    15.70    0.02    0.559
```

<!-- Link Definitions -->

[deprecated]: ../02-common-principles.md#definitions
[string]: https://www.w3schools.com/js/js_json_datatypes.asp
[strings]: https://www.w3schools.com/js/js_json_datatypes.asp
[integer]: https://www.w3schools.com/js/js_json_datatypes.asp
[number]: https://www.w3schools.com/js/js_json_datatypes.asp
[numbers]: https://www.w3schools.com/js/js_json_datatypes.asp
[boolean]: https://www.w3schools.com/js/js_json_datatypes.asp
[array]: https://www.w3schools.com/js/js_json_arrays.asp
[arrays]: https://www.w3schools.com/js/js_json_arrays.asp
[object]: https://www.json.org/json-en.html
[uri]: ../02-common-principles.md#uniform-resource-indicator
