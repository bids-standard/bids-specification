# Positron Emission Tomography

Support for Positron Emission Tomography (PET) was developed as a [BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please cite the following paper when referring to this part of the standard in
context of the academic literature:

> Knudsen GM, Ganz M, Appelhoff S, Boellaard R, Bormans G, Carson RE, Catana C, Doudet D, Gee AD, Greve DN, Gunn RN, Halldin C, Herscovitch P, Huang H, Keller SH, Lammertsma AA, Lanzenberger R, Liow JS, Lohith TG, Lubberink M, Lyoo CH, Mann JJ, Matheson GJ, Nichols TE, Nørgaard M, Ogden T, Parsey R, Pike VW, Price J, Rizzo G, Rosa-Neto P, Schain M, Scott PJH, Searle G, Slifstein M, Suhara T, Talbot PS, Thomas A, Veronese M, Wong DF, Yaqub M, Zanderigo F, Zoghbi S, Innis RB. Guidelines for Content and Format of PET Brain Data in Publications and in Archives: A Consensus Paper. Journal of Cerebral Blood Flow and Metabolism, 2020 Aug;40(8):1576-1585. 
> doi: [10.1177/0271678X20905433](https://doi.org/10.1177/0271678X20905433)

The following example PET datasets have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

-   Single dynamic scan (pet, blood): [`pet_example_1`](https://doi.org/10.17605/OSF.IO/CJ2DR)
-   Single dynamic scan (pet, mri): [`pet_example_2`](https://doi.org/10.5281/zenodo.1490922)


Further datasets are available from the [BIDS examples repository](https://github.com/bids-standard/bids-examples).

## PET recording data

As specified above, this extension is relevant for PET imaging and its associated data, such as blood data. In addition, the extension is in accordance with the guidelines for reporting and sharing brain PET data (Knudsen et al. 2020, [1]). If you want to share structural magnetic resonance (MR) images with your PET data, please distribute them according to the original BIDS specification (https://bids-specification.readthedocs.io/en/stable). Please pay specific attention to the format the MR images are in, such as if they have been unwarped in order to correct for gradient non-linearities. There is a specific field in the MRI BIDS (https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html) called “NonlinearGradientCorrection” which indicates this. The reason for this is that the MRI needs to be corrected for nonlinear gradients in order to fit the accompanying PET scans for co-registration [1, 2]. In general, SI units must be used (we refer to https://bids-specification.readthedocs.io/en/stable/99-appendices/05-units.html) and we recommend to use the CMIXF style formatting for SI units e.g. "kBq/mL" rather than "kilobecquerel per ml". An overview of a common PET experiment (with blood data) can be seen in Figure 1, defined on a single time scale relative to a predefined “time zero” (which should be defined either to be scan start or injection time; please note an exception to this definition is possible if a pharmacological within-scan challenge is performed).


![Figure 1](images/PET_scan_overview.png "placement of NAS fiducial")

Figure 1: Overview of a common PET experiment, including blood measurements, and defined on a common time scale. Note, “time zero”can either be defined as time of injection or scan start, and all the PET and blood data should be decay-corrected to this time point. Furthermore, although in this example tracer injection coincides with scan start, this is not always the case and hence we allow for the flexibility of specifying either time of injection or scan start as “time zero”. 

## PET Imaging data

Template:

```Text
sub-<participant_label>/
      [ses-<session_label>/]
        pet/
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.nii[.gz]
        sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_pet.json
```

PET data belongs in the /pet folder. PET imaging data SHOULD be stored in 4D (or 3D if only one volume was acquired) NifTI files with _pet suffix. Volumes should be stored in chronological order (the order they were acquired in).

Multiple sessions (visits) are encoded by adding an extra layer of directories and file names in the form of ses-<label>. Session labels can consist only of alphanumeric characters [a-zA-Z0-9] and should be consistent across subjects. If numbers are used in session labels we recommend using zero padding (for example ses-01, ses-11 instead of ses-1, ses-11). This makes results of alphabetical sorting more intuitive. The extra session layer (at least one /ses-<label> subfolder) should be added for all subjects if at least one subject in the dataset has more than one session. Skipping the session layer for only some subjects in the dataset is not allowed. If a /ses-<label> subfolder is included as part of the directory hierarchy, then the same ses-<label> tag must also be included as part of the file names themselves. In general, we assume that a new session wrt PET starts with either a new injection (probably most common case) or with the subject being taken out of the scanner (same injection, but subject leaves the scanner and returns). However, for example, if a subject has to leave the scanner room and then be re-positioned on the scanner bed e.g. to use the bathroom, the set of PET acquisitions will still be considered as a session and match sessions acquired in other subjects. Similarly, in situations where different data types are obtained over several visits (for example FDG PET on one day followed by amyloid PET a couple days after) those can be grouped in one session. Please see the difference with the run-<label> below.

With respect to the task-<label>, data is arranged in a similar way as task-based and resting state BOLD fMRI data. In case of studies using combined PET/fMRI, subject-specific tasks may be carried out during the acquisition within the same session. Therefore, it is possible to specify task-<label> in accordance with the fMRI data. For more information please see https://bids-specification.readthedocs.io/en/stable/04-modality-specific-files/01-magnetic-resonance-imaging-data.html#task-including-resting-state-imaging-data. 

In case of studies with multiple acquisitions per subject using different tracers, the acq-<label> must be used to distinguish between different tracers. Please keep in mind that the label used is arbitrary and each file requires a separate JSON sidecar with details of the tracer used (see below). Examples are e.g. acq-18FFDG for fludeoxyglucose, acq-11CPIB for Pittsburgh compound B, etc.

The reconstruction key (rec-<label>) has four reserved values: acdyn, for reconstructions with attenuation correction of dynamic data; acstat, for reconstructions with attenuation correction of static data; nacdyn, for reconstructions without attenuation correction of dynamic data; and nacstat, for reconstructions without attenuation correction of static data. Further details regarding reconstruction are in the _pet.json file. In case of multiple reconstructions of the data with the same type, we allow for using a number after the <label> in order to distinguish, e.g. rec-acdyn1 and rec-acdyn2. 

The run entity is used if one scan type/contrast is repeated multiple times within the same scan session/visit. If several scans of the same modality are acquired they MUST be indexed with a key-value pair: _run-1, _run-2, _run-3 etc. (only integers are allowed as run labels). When there is only one scan of a given type the run key MAY be omitted. An example of this would be two consecutive scans performed within the same session, e.g. two short FDG scans right after each other. It is our assumption that the run-<label> is used in PET for the cases where the subject does not leave the scanner. Otherwise, we refer to the ses-<label> definition.

In addition to the imaging data a _pet.json sidecar file needs to be provided. The included metadata are divided into sections described below.


### Sidecar JSON (`*_pet.json`)

#### The "Info" section
This section is mandatory and contains general information about the imaging experiment. Some of the fields are marked optional (MAY), e.g. anaesthesia; for those fields a BIDS PET validator will not throw an error even if they are not present. Note, although bodyweight is a recommended information in (Knudsen et al. 2020, JCBFM [1]), this consists of meta information at the participant level and should hence be part of the participants.tsv or session.tsv file in case of multiple measurements.
| Field name | Definition                                                                                                                                                                                                                                                                                                                              |
|------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Modality   | REQUIRED. Name of the modality. Example values could be "PET", "PETMR", or "PETCT". |

#### The "Radiochem" section
This section is mandatory and contains information regarding the radioactive material used in the experiment.

#### The "Time" section
This section is mandatory and contains timing information about the imaging experiment.

#### The "Recon" section
This optional section includes information about the image reconstruction. All reconstruction specific parameters that are not specified, but one wants to include, should go into the ReconMethodParameterVal field. 

#### The "Blood" section
In order to simplify a distinction between PET data acquired with and without blood measurements, we have added a specific section detailing blood measurements in the _pet.json. If blood data is available, meaning some of the “Avail” below with a given prefix are true, the following fields with the given prefix are required and at the same time we require the presence of a *_blood.tsv with a corresponding *_blood.json detailing the column content. If true, please see the section 2.2 Blood data.
#### Example (`*_pet.json`)

```JSON
{       
	"Modality": "PET",
	"Manufacturer": "Siemens",
	"ManufacturersModelName": "High-Resolution Research Tomograph (HRRT, CTI/Siemens)",
	"BodyPart": "Brain",
	"BodyWeight": 21,
	"BodyWeightUnit": "kg",
	"unit": "Bq/ml", 
	"TracerName": "CIMBI-36",
	"TracerRadionuclide": "C11",
	"TracerMolecularWeight": 380.28,
	"TracerMolecularWeightUnit": "g/mol",
	"TracerInjectionType": "bolus",
	"InjectedRadioactivity": 573,
	"InjectedRadioActivityUnit": "MBq",
	"InjectedMass": 0.62,
	"InjectedMassUnit": "ug",
	"SpecificRadioactivity": 353.51,
	"SpecificRadioactivityUnit": "GBq/umol",
	"ModeOfAdministration": "bolus",
	"MolarActivity": 1.62,
	"MolarActivityUnit": "nmol",
	"MolarActivityMeasTime": "12:59:00",
	"TimeZero": "13:04:42",
	"ScanStart": 0,
	"InjectionStart": 0,
	"FrameTimesStart": [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 140, 160, 180, 240, 300, 360, 420, 480, 540, 660, 780, 900, 1020, 1140, 1260, 1380, 1500, 1800, 2100, 2400, 2700, 3000, 3300, 3600, 3900, 4200, 4500, 4800, 5100, 5400, 5700, 6000, 6300, 6600, 6900],
	"FrameDuration": [10, 10, 10, 10, 10, 10, 20, 20, 20, 20, 20, 20, 60, 60, 60, 60, 60, 60, 120, 120, 120, 120, 120, 120, 120, 120, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300, 300],
	"AcquisitionMode": "list mode",
	"ImageDecayCorrected": "true",
	"ImageDecayCorrectionTime": 0,
	"ReconMatrixSize": [256,256,207,45],
	"ImageVoxelSize": [1.2188,1.2188,1.2188],
	"ReconMethodName": "3D-OSEM-PSF",
	"ReconMethodParameterLabels": ["subsets","iterations"],
	"ReconMethodParameterUnit": ["none","none"],
	"ReconMethodParameterValues": [16,10],
	"ReconFilterType": "none",
	"AttenuationCorrection": "[137Cs]transmission scan-based",
	"PlasmaAvail": "false",
	"MetaboliteAvail": "false",
	"ContinuousBloodAvail": "false",
	"DiscreteBloodAvail": "false"
}
```

## Blood data (`*_blood.tsv`)
This section includes all data needed to perform blood analysis for PET data. The section may be omitted if blood measurements of radioactivity were not made. It contains the values and information regarding plasma samples, discrete blood samples, continuous blood samples from an autosampler, and metabolite fractions. All these measurements should be defined according to a single time-scale in relation to time zero defined by the PET data (Figure 1). Additionally, if blood and metabolite measurements were made one should always report radioactivity in plasma and corresponding parent fraction measurements, including fractions of radiometabolites. All definitions used below are in accordance with Innis et al. 2007 [3]. All method specific information related to the measurements can be stated in the field “description”. 

Template:

```Text
sub-<participant_label>/
      [ses-<session_label>/]
        pet/
          sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.tsv
          sub-<participant_label>[_ses-<session_label>][_task-<task_label>][_acq-<label>][_rec-<label>][_run-<index>]_recording-<label>_blood.json
```

Blood data belongs in the /pet folder along with the corresponding PET data. However, the blood data also follows the inheritance principle (https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#the-inheritance-principle) and may be moved to an upper level folder if it does not change e.g. with multiple reconstructions. The blood data is most often recorded using an autosampler for continuous blood samples, or manually for discrete blood samples. Therefore, the recording key (recording-<label>) has two reserved values: continuous, for continuous whole blood data measurements (2.2.4); and discrete, for discrete blood data, including whole blood (2.2.4), plasma (2.2.2), parent fraction and metabolite fractions (2.2.3). Blood data will be stored in tabular *_.tsv files with a _blood suffix (https://bids-specification.readthedocs.io/en/stable/02-common-principles.html#tabular-files). 
The first column in the *_.tsv file should be a time column (2.2.1), defined in relation to time zero defined by the _pet.json file. All other information relevant to the blood measurements are recommended, and can be added as an additional column. It is expected that all values are (if relevant) decay corrected to time zero. 

### Time

### The "Plasma" section
This section may be omitted if discrete plasma measurements of radioactivity were not made. It contains information regarding discretely sampled plasma data.

### The "Metabolite" section
This section may be omitted if metabolite measurements were not made. It may contain information regarding metabolite info, such as the following three column examples:

### The "WholeBlood" section
This section may be omitted if whole blood measurements of radioactivity were not made. It contains information regarding sampled whole blood data.

### Example (`*_recording-discrete_blood.tsv`)
```JSON
{
    "time": {
        "Description": "Time in relation to time zero defined by the _pet.json",
        "Units": "s"
    },
    "plasma_radioactivity": {
        "Description": "Radioactivity in plasma samples. Measured using COBRA counter.", 
        "Units": "kBq/ml"
    },
    "whole_blood_radioactivity": {
        "Description": "Radioactivity in whole blood samples. Measured using COBRA counter.",
        "Units": "kBq/ml"
    },
    "metabolite_parent_fraction": {
        "Description": "Parent fraction of the radiotracer.",
        "Units": "unitless"
    },
    "metabolite_polar_fraction": {
        "Description": "Polar metabolite fraction of the radiotracer.",
        "Units": "unitless"
    },
    "metabolite_lipophilic_fraction": {
        "Description": "Lipophilic metabolite fraction of the radiotracer.",
        "Units": "unitless"
    }
}
```

![Figure 2](images/blood_discrete_tsv.png "Screenshot of the discrete blood tsv file.")

Figure 2: Caption of the corresponding _blood.tsv file. 

# Appendix: Useful resources
This website is an extremely useful resource: http://www.turkupetcentre.net/petanalysis/quantification.html

An extensive resource for background knowledge on kinetic modeling can be found here: https://nru.dk/index.php/misc/category/3-pet-kinetic-course

# References
[1] Knudsen, G. M., Ganz, M., Appelhoff, S., Boellaard, R., Bormans, G., Carson, R. E., … Innis, R.B. (2020). Guidelines for the content and format of PET brain data in publications and archives : A consensus paper. Journal of Cerebral Blood Flow and Metabolism. https://doi.org/10.1177/0271678X20905433

[2] Nørgaard, M., Ganz, M., Svarer, C., Frokjaer, V. G., Greve, D. N., Strother, S. C., & Knudsen, G. M. (2019). Optimization of preprocessing strategies in Positron Emission Tomography (PET) neuroimaging: A [11C]DASB PET study. NeuroImage, 199(October 2019), 466–479. https://doi.org/10.1016/j.neuroimage.2019.05.055 

[3] Innis, R. B., Cunningham, V. J., Delforge, J., Fujita, M., Gjedde, A., Gunn, R. N., … Carson, R. (2007). Consensus nomenclature for in vivo imaging of reversibly binding radioligands. Journal of Cerebral Blood Flow and Metabolism, 1–7. https://doi.org/10.1038/sj.jcbfm.9600493