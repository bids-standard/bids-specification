# Eye-tracking including gaze position and pupil size

Support for eye-tracking dataset developed as a [BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals). Please see [Citing BIDS](../01-introduction.md#citing-bids) on how to appropriately credit this extension when referring to it in the context of the academic literature.

## Terminology and conventions

Eye-tracking-BIDS is fully consistent with the BIDS specification as a whole. However, BIDS was initially developed in the context of MRI, so some terminology may be unfamiliar to researchers from other fields. This section adds clarifications to [Common Principles - Definitions](../02-common-principles.html) for the eye-tracking context.

-  __Eye-tracker__ - refer to the apparatus allowing the records of gaze position and/or pupil size. 
-	__Screen__ - Video display used to present visual stimulation (for example projector, monitor, tablet).

## Eye-tracking data

```Text
sub-<label>/
    [ses-<label>/]
        <datatype>/
            sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_run-<index>]_eyetrack.<datatype>
            sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_run-<index>]_eyetrack.json
            sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_run-<index>]_events.json
            sub-<label>[_ses-<label>][_task-<label>][_acq-<label>][_run-<index>]_events.tsv
```

The eye-tracking data files generally contain gaze position (x/y coordinates) and pupil size data. With Eye-Tracking-BIDS, we wish to promote the adoption of good practices in the management of scientific data. Hence, the current emphasis of Eye-Tracking-BIDS is not to impose a generic data format for the modality, but to standardize the way data is stored in repositories. 

Eye-tracking data MUST be stored in the main data recording modality or `<datatype>` directory (for example func, anat, dwi, meg, eeg, ieeg, or beh). The current version of this extension *does not* include a specification of the extension format and data formatting of recorded eye-tracking data. Thus, data must be stored in an open format (for example EDF file converted in ASCII `.asc` format or `.tsv` etc) with the `_eyetrack` suffix.

We encourage every user to put the raw data before conversion within the `/sourcedata` folder (for example put property EDF files in the sourcedata folder).

The OPTIONAL [`task-<label>`](../99-appendices/09-entities.md#task) is used to indicate a task subject were asked to perform while eye-tracking records were obtained. Those labels MUST be consistent across subjects and sessions. For task based eye-tracking, a corresponding [task events](../04-modality-specific-files/05-task-events.md) file MUST be provided (please note that this file is not necessary for resting state tasks).

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) refers to a custom label the user MAY use to distinguish a different set of parameters used for acquiring the same modality. Acquisition labels corresponds mostly to imaging records (for example eye-tracking with fMRI) but can also be specified when combining eye-tracking and imaging methods.

If more than one run of the same task and acquisition are acquired during the same session, the [`run-<index>`](../99-appendices/09-entities.md#run) entity MUST be used: _run-1, _run-2, _run-3, and so on. If only one run was acquired the run-<index> can be omitted.

### Sidecar JSON document (`*_eyetrack.json`)

Generic fields MUST be present:

{{ MACROS___make_metadata_table(
   {
      "TaskName": ("REQUIRED", "A RECOMMENDED convention is to name resting state task using labels beginning with `rest`."),
   }
) }}

SHOULD be present: 

For consistency between studies and institutions, we encourage users to extract the values of these fields from the actual raw data. Whenever possible, please avoid using ad hoc wording.

{{ MACROS___make_metadata_table(
   {
      "InstitutionName": "RECOMMENDED",
      "InstitutionAddress": "RECOMMENDED",
      "Manufacturer": (
         "RECOMMENDED",
         "Manufacturer of the eye-tracking system (for example "
         '`"SR-Research"`, `"Tobii"`, `"SMI"`, `"Gazepoint"`, '
         '`"Pupil Labs"`, `"Custom built"`, `"Other"`) '
      ),
      "ManufacturersModelName": (
         "RECOMMENDED",
         "Manufacturer's designation of the eye-tracker model (for example"
         '`"Eye-link 1000"`).'
         ),
      "SoftwareVersion": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "Instructions": (
         "RECOMMENDED", 
         "Text of the instructions given to participants before the experiment."),
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
   }
) }}


Specific ET fields MUST be present:

{{ MACROS___make_metadata_table(
   {
      "SamplingFrequency_eyetrack": "REQUIRED",
      "SampleCoordinateUnit": "REQUIRED",
      "SampleCoordinateSystem": "REQUIRED",
      "EnvironmentCoordinates": "REQUIRED",
      "ScreenSize": "REQUIRED",
      "ScreenResolution": "REQUIRED",
      "ScreenDistance": (
         "REQUIRED",
         "Screen distance in cm (e.g 60 for a screen distance of 60 cm), "
         'if no screen use "n/a". '
         "For MRI, it corresponds to the distance between the head-coil mirror "
         "to the projection screen for example."),
   }
) }}

Specific ET fields SHOULD be present:

{{ MACROS___make_metadata_table(
   {
      "IncludedEyeMovementEvents": "RECOMMENDED",
      "DetectionAlgorithm": "RECOMMENDED",
      "DetectionAlgorithmSettings": "RECOMMENDED",
      "StartMessage": "RECOMMENDED",
      "EndMessage": "RECOMMENDED",
      "KeyPressMessage": "RECOMMENDED",
      "CalibrationType": "RECOMMENDED",
      "CalibrationUnit": "RECOMMENDED",
      "CalibrationPosition": "RECOMMENDED",
      "MaximalCalibrationError": "RECOMMENDED",
      "AverageCalibrationError": "RECOMMENDED",
      "CalibrationList": "RECOMMENDED",
      "RecordedEye": "RECOMMENDED",
      "EyeCameraSettings": "RECOMMENDED",
      "FeatureDetectionSettings": "RECOMMENDED",
      "GazeMappingSettings": "RECOMMENDED",
      "RawDataFilters": "RECOMMENDED",
      "ScreenRefreshRate": "RECOMMENDED",
      "AOIDefinition": "RECOMMENDED",
      "PupilFitMethod": "RECOMMENDED",
   }
) }}

### Example:

```JSON
{"TaskName": "PSC_train",
"InstitutionName": "Goethe-University of Frankfurt; Department of Psychology",
"InstitutionAdress": "Theodor-W.-Adorno-Platz 6 60323 Frankfurt am Main; Germany",
"Manufacturer": "SR-Research",
"ManufacturersModelName": "EYELINK II CL v4.56 Aug 18 2010",
"SoftwareVersion": "SREB1.10.1630 WIN32 LID:F2AE011 Mod:2017.04.21 15:19 CEST",
"TaskDescription": "Sentence reading",
"Instructions": "Read sentences as you would read a book or a newspaper",
"SamplingFrequency": 1000,
"SampleCoordinateUnit": "pixel",
"SampleCoordinateSystem": "gaze-on-screen",
"EnvironmentCoordinates": "top-left",
"IncludedEyeMovementEvents": [["Start of fixation", "SFIX"],["End of fixation", "EFIX"],["Start of saccade", "SSACC"], ["End of saccade", "ESACC"],["Start of blink", "SBLINK"], ["End of blink", "EBLINK"]],
"DetectionAlgorithm": "SR-Research",
"StartMessage": "SENTENCESTART",
"EndMessage": "SENTENCESTOP",
"KeyPressMessage": "ANSWER",
"RecordedEye": "Both",
"ScreenSize": [38.6, 29],
"ScreenResolution": [1024, 768],
"ScreenDistance": 60,
"AOIDefinition": ["square",["x_start", "x_stop", "y_start", "y_stop"]] ,
}
```

### Example Dataset

**Potsdam Sentence Corpus Dataset**

Eye-tracking data, measured with an Eyelink, from 2 German speaker learners reading 36 sentences from the Potsdamer Sentence Corpus ([Kliegl et al., 2004](https://doi.org/10.1080/09541440340000213)). They were measured on four occasions, in a randomized controlled design (that is, before and after a control and experimental training). The sentences appeared after the calibration check on the fixation cross and disappeared as soon as a saccade crossed the invisible boundary on the right sight of the screen. The participants were asked to fixate the fixation cross and then read the sentences naturally as they would read a book or a newspaper. After they have read the sentence, they should look to a fixation cross in the right down corner of the screen. With this action they automatically passed the boundary and the sentence disappeared. After some sentences a question sign appeared and the experimenter asked the participant a question about the content of the sentence to check if the participant understood it. The correctness of the answer was recorded by the experimenter by pressing the key "r" ("correct") or "f" ("false").

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/PSC_train/PSC_train_raw_data_BIDS)<br />
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/PSC_train/from_asc_to_BIDS_asc.Rmd)


**Reading Hyperlinks Dataset**

Eye-tracking data, measured with an Eyelink, from 8 subjects reading sentences with 320 embedded target words and invisible boundary manipulation. The task of participants was similar as in the Dataset in 4.1, silent reading with comprehension questions. The main interest of the study was to investigate word recognition processes of the target word under different conditions (for example, was the word presented in blue or black). The invisible boundary manipulation allowed the investigation of parafoveal preview benefits in relation to the conditions of interest. Here, the predominant characteristics of Hyperlinks. 
For details see [here](https://doi.org/10.7717/peerj.2467).

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/hyperlink/hyperlinks_raw_data_BIDS)<br />
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/hyperlink/from_asc_to_BIDS_asc.Rmd)

**Emotional Faces Dataset**

Eye-tracking data, measured with an Eyelink, from 4 subjects viewing a grid of sixteen faces showing different emotions without any explicit task. The procedure resembled that described by Lazarov and colleagues (2018). Grids of 4x4 stimulus matrices of 16 color photographs of human faces displaying emotional expressions were presented. Photos were taken from the FACES database (Ebner et al., 2010). The paradigm was divided into two tasks:
-  Task 1 (happy + sad): 8 faces with happy and 8 faces with sad expression.
-  Task 2 (happy/sad + neutral): 8 faces with happy or sad and 8 faces with neutral expression.
In both tasks, 64 stimulus matrices in 2 blocks of 32 matrices were presented. Participants were asked to just look at the photos. Each matrix was presented for 6s.

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/emotional_faces/freeviewfaces_raw_data_BIDS)<br />
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/emotional_faces/from_asc_to_BIDS_asc.Rmd)

**Resting State inside MRI Dataset**

Eye-tracking data, measured with an Eyelink 2000 in a 3T Philips Achieva scanner. 20 participants were 
invited to fixate at the screen center during 2 runs. They were told to keep the eyes open 
and to let their mind wander. 
Here we use this example dataset to present how to deal with eyetracking data when the main recording 
modality is fMRI, therefore we provide T1w/T2w, functional and field map data in addition to eye tracking records.

[BIDS dataset](https://openneuro.org/datasets/ds004158/versions/1.0.1)