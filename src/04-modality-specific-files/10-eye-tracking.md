# Eye-tracking including gaze position and pupil size

Support for eye-tracking dataset developed as a [BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals). Please see [Citing BIDS](../01-introduction.md#citing-bids) on how to appropriately credit this extension when referring to it in the context of the academic literature.

## Terminology and conventions

Eye-tracking-BIDS is fully consistent with the BIDS specification as a whole. However, BIDS was initially developed in the context of MRI, so some terminology may be unfamiliar to researchers from other field. This section adds clarifications to [Common Principles - Definitions](../02-common-principles.html) for the eye-tracking context.

-  Eye-tracker - refer to the apparatus allowing the records of gaze position and/or pupil size. 
-	Screen - Video display used to present visual stimulation (for example projector, monitor, tablet).

## Eye-tracking data

{{ MACROS___make_filename_template(datatypes=["eyetrack"], suffixes=["eyetrack", "events"]) }}

The eye-tracking data files generally contain gaze position (x/y coordinates) and pupil size data. With Eye-Tracking-BIDS, we wish to promote the adoption of good practices in the management of scientific data. Hence, the current emphasis of Eye-Tracking-BIDS is not to impose a generic data format for the modality, but to standardize the way data is stored in repositories. 

Eye-tracking data MUST be stored in the `eyetrack` directory. The current version of this extension *does not* include a specification of the extension format and data formatting of recorded eye-tracking data. Thus, data must be stored in an open format (for example EDF file converted in ASCII `.asc` format or `.tsv` etc) with the `_eyetrack` suffix.

The OPTIONAL [`task-<label>`](../99-appendices/09-entities.md#task) is used to indicate a task subject were asked to perform while eye-tracking records were obtained. Those labels MUST be consistent across subjects and sessions. For task based eye-tracking, a corresponding [task events](../04-modality-specific-files/05-task-events.md) file MUST be provided (please note that this file is not necessary for resting state tasks).

The OPTIONAL [`acq-<label>`](../99-appendices/09-entities.md#acq) refers to a custom label the user MAY use to distinguish a different set of parameters used for acquiring the same modality. Acquisition labels corresponds mostly to imaging records (for example eye-tracking with fMRI) but can also be specified when combining eye-tracking and imaging methods.

If more than one run of the same task and acquisition are acquired during the same session, the [`run-<index>`](../99-appendices/09-entities.md#run) entity MUST be used: _run-1, _run-2, _run-3, and so on. If only one run was acquired the run-<index> can be omitted.

### Sidecar JSON document (`*_eyetrack.json`)

Generic fields MUST be present:

{{ MACROS___make_metadata_table(
   {
      "TaskName": ("REQUIRED", "Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric ([a-zA-Z0-9]) characters. For example TaskName "faces n-back" will correspond to task label facesnback. A RECOMMENDED convention is to name resting state task using labels beginning with rest."),
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
         "`"SR-Research"`, `"Tobii"`, `"SMI"`,`"Gazepoint"`, `"Pupil Labs"`, "
         "`"Custom built"`, ... , `"Other"`)"),
      "ManufacturersModelName": (
         "RECOMMENDED",
         "Manufacturer's designation of the eye-tracker model "
         "(for example `"Eye-link 1000"`)."),
      "SoftwareVersion": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "Instructions": (
         "RECOMMENDED", 
         "Text of the instructions given to participants before the experiment. "
         "If no instruction is given, write `none`."),
      "CogAtlasID": "RECOMMENDED",
      "CogPOID": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
   }
) }}

Specific ET fields MUST be present:

{{ MACROS___make_metadata_table(
   {
      "SamplingFrequency": (
         "REQUIRED",
         "Sampling frequency (in Hz) of the corresponding data in the recording "
         "(for example, 1000). If the sampling frequency change across run, "
         "sidecar JSON document must be created specifying the run number."),
      "SampleCoordinateUnit": "REQUIRED",
      "SampleCoordinateSystem": "REQUIRED",
      "EnvironmentCoordinates": "REQUIRED",
      "ScreenSize": "REQUIRED",
      "ScreenResolution": "REQUIRED",
      "ScreenDistance": (
         "REQUIRED",
         "Screen distance in cm (e.g 60 for a screen distance of 60 cm), "
         "if no screen use "n/a". "
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
      "CalibrationPosition": "RECOMMENDED",
      "CalibrationUnit": "RECOMMENDED",
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
      "PupilPositionType": "RECOMMENDED",
      "PupilFitMethod": "RECOMMENDED",
   }
) }}

Example:

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
"EnvironmentCoordinates": [["0,0", "top left"], ["1,1", "bottom right"]],
"EventIdentifier": ["ID_73_7","ID_74_7","ID_75_7","ID_76_7","ID_77_7","ID_78_9","ID_79_8","ID_80_8","ID_81_8","ID_82_5","ID_83_6","ID_84_8","ID_85_7","ID_86_8","ID_87_5","ID_88_8","ID_89_5","ID_90_8","ID_91_6","ID_92_8","ID_93_8","ID_94_8","ID_95_7","ID_96_6","ID_97_8","ID_98_7","ID_99_9","ID_100_7","ID_101_6","ID_102_8","ID_103_7","ID_104_7","ID_105_10","ID_106_7","ID_107_6","ID_108_7"],
"IncludedEyeMovementEvents": [["Start of fixation", "SFIX"],["End of fixation", "EFIX"],["Start of saccade", "SSACC"], ["End of saccade", "ESACC"],["Start of blink", "SBLINK"], ["End of blink", "EBLINK"]],
"DetectionAlgorithm": "SR-Research",
"StartMessage": "SENTENCESTART",
"EndMessage": "SENTENCESTOP",
"KeyPressMessage": "ANSWER",
"RecordedEye": "BOTH",
"ScreenSize": [38.6, 29],
"ScreenResolution": [1024, 768],
"ScreenDistance": 60,
"AOIDefinition": ["square",["x_start", "x_stop", "y_start", "y_stop"]] ,
"PupilPositionType": "raw pupil position on screen",
"CalibrationList":[["H3", "LEFT", 0.71, 0.41, -425.49],["H3", "RIGHT", 0.51, 0.35, -425.49],["H3", "LEFT", 0.21, 0.16, -108.696],["H3", "RIGHT", 0.73, 0.42, -108.696],["H3", "LEFT", 0.39, 0.33, -99.545],["H3", "RIGHT", 1.08, 0.41, -99.545],["H3", "LEFT", 0.57, 0.31, -79.831],["H3", "RIGHT", 0.43, 0.21, -79.831],["H3", "LEFT", 0.51, 0.36, -72.362],["H3", "RIGHT", 0.27, 0.2, -72.362],["H3", "LEFT", 0.58, 0.44, -35.031],["H3", "RIGHT", 0.59, 0.44, -35.031],["H3", "LEFT", 0.42, 0.25, -25.399],["H3", "RIGHT", 0.42, 0.3, -25.399]]
}
```

### Example Dataset

**Potsdam Sentence Corpus Dataset**

Eye-tracking data, measured with an Eyelink, from 2 German speaker learners reading 36 sentences from the Potsdamer Sentence Corpus (Kliegl et al., 2004). They were measured on four occasions, in a randomized controlled design (that is, before and after a control and experimental training). The sentences appeared after the calibration check on the fixation cross and disappeared as soon as a saccade crossed the invisible boundary on the right sight of the screen. The participants were asked to fixate the fixation cross and then read the sentences naturally as they would read a book or a newspaper. After they have read the sentence, they should look to a fixation cross in the right down corner of the screen. With this action they automatically passed the boundary and the sentence disappeared. After some sentences a question sign appeared and the experimenter asked the participant a question about the content of the sentence to check if the participant understood it. The correctness of the answer was recorded by the experimenter by pressing the key "r" ("correct") or "f" ("false").

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/PSC_train/PSC_train_raw_data_BIDS) 
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/PSC_train/from_asc_to_BIDS_asc.Rmd)


**Reading Hyperlinks Dataset**

Eye-tracking data, measured with an Eyelink, from 8 subjects reading sentences with 320 embedded target words and invisible boundary manipulation. The task of participants was similar as in the Dataset in 4.1, silent reading with comprehension questions. The main interest of the study was to investigate word recognition processes of the target word under different conditions (for example, was the word presented in blue or black). The invisible boundary manipulation allowed the investigation of parafoveal preview benefits in relation to the conditions of interest. Here, the predominant characteristics of Hyperlinks. 
For details see [here](https://doi.org/10.7717/peerj.2467)

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/hyperlink/hyperlinks_raw_data_BIDS) 
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/hyperlink/from_asc_to_BIDS_asc.Rmd)

**Emotional Faces Dataset**

Eye-tracking data, measured with an Eyelink, from 4 subjects viewing a grid of sixteen faces showing different emotions without any explicit task. The procedure resembled that described by Lazarov and colleagues (2018). Grids of 4x4 stimulus matrices of 16 color photographs of human faces displaying emotional expressions were presented. Photos were taken from the FACES database (Ebner et al., 2010). The paradigm was divided into two tasks:
-  Task 1 (happy + sad): 8 faces with happy and 8 faces with sad expression.
-  Task 2 (happy/sad + neutral): 8 faces with happy or sad and 8 faces with neutral expression.
In both tasks, 64 stimulus matrices in 2 blocks of 32 matrices were presented. Participants were asked to just look at the photos. Each matrix was presented for 6s.

[BIDS dataset](https://github.com/greckla/Eye-Tracking-BIDS/tree/master/emotional_faces/freeviewfaces_raw_data_BIDS) 
[Conversion script](https://github.com/greckla/Eye-Tracking-BIDS/blob/master/emotional_faces/from_asc_to_BIDS_asc.Rmd)

**Resting State inside MRI Dataset**

Eye-tracking data, measured from 3 healthy subjects by an EyeLink 1000 Plus eye-tracking system (SR Research Ltd. Ottawa, ON, Canada) inside a Siemens 3.0T MAGNETOM Prisma MRI. Two resting state scans were acquired for each subject. Subjects were instructed to stay still, think of nothing in particular, and maintain fixation on the cross. All lights were turned off except an assistant front-light inside the scanner room. Total duration of each fMRI scan was 6:50 min. The start of MRI acquisition was automatically recorded in the eye-tracking data using MRI trigger (e.g.  MSG `<time-stamp>` RS_starts.). The end of MRI acquisition was manually recorded by human operator by pressing button after the MRI acquisition was finished (e.g. MSG `<time-stamp>` RS_endtime_recorded_maually). For details see [here](https://doi.org/10.1101/2021.07.12.452041)


