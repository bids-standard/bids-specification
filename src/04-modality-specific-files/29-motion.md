# Motion
This specification extends the Brain Imaging Data Structure (BIDS) Specification
to motion data [BIDS Extension Proposal (BEP029)](../07-extensions.md#bids-extension-proposals).
By default, these data consist of time series of object positions,
orientations, or their time derivatives described by a coordinate system of up to
three spatial dimensions.

A wide variety of motion capture systems are used in human research, resulting in
different native data modalities depending on the system. The current BEP specifically
deals with positions,orientations, and their time derivatives. For camera-based
motion capture the raw camera footage falls out of scope. To share motion data
recorded using an optical system, one would only represent the (position)
output, not the input camera footage.

The extension is not limited to motion data in physical space but also encompasses
simulated movement in virtual space, as far as these are comparable to movements
in physical space. The extension is also not limited to the positions/orientations
of human body parts, other dynamic objects (physical or virtual) in the environment
whose motion is tracked may be included as additional sources of motion.

Several [example Motion datasets](https://github.com/bids-standard/bids-examples)
have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

## BIDS-Motion terminology
Some of the most important notions in BIDS-motion are defined below. The terminology
is inherited from BIDS-Raw.

| **Keyword**                   | **Description**                                              |
| -----------                   | ------------------------------------------------------------ |
| Space                         | BIDS defines “space”  as an artificial frame of reference, created to describe different anatomies in a unifying manner (see Appendix VIII). However, data collected in studies of physical or virtual motion usually have a reference frame that is anchored to the physical lab space or the virtual environment. |
| Spatial axes                  | Describes the three spatial axes as forward-backward, left-right, and up-down, which respectively correspond to the anterior-posterior, left-right, and superior-inferior axes in Appendix VIII. Although the anatomical nomenclature can be mapped and generalized unambiguously to other types of spaces, the conventional usage where the spatial data are interpreted with respect to the body may cause confusion in interpreting motion data recorded with respect to the recording space. |
| Position (POS)                | The spatial location of an object in relation to an arbitrary origin |
| Velocity (VEL)                | The speed of an object in relation to an arbitrary origin                                    |
| Acceleration (ACC)            | The rate of change of velocity of an object in relation to an arbitrary origin                                    |
| Orientation (ORNT)            | The spatial orientation of an object in relation to its center of rotation independent of the choice of origin            |
| Angular velocity (ANGVEL)     | The speed of rotation of an object |
| Angular acceleration (ANGACC) | The change in speed of rotation of an object |
| Tracking system               | A group of tracking devices that share hardware properties (specifically manufacturers model name) and original (nominal) sampling rate.|
| Tracked Point                 | A specific point on an object that is being tracked, which can be a body part or an inanimate object. |
| Channel                       | A  time series of scalar values representing position coordinates or rotation angles among |

## Motion recording data

Template:
```
└─ sub-<label>\
   └─ [ses-<label>]\
      └─ motion\
         ├─ sub-<label>[_ses-<label>]_task-<label>[_tracksys-<label>]_motion.tsv
         ├─ sub-<label>[_ses-<label>]_task-<label>_motion.json
         ├─ sub-<label>[_ses-<label>]_task-<label>_channels.tsv
         ├─ sub-<label>[_ses-<label>]_task-<label>_coordsystem.json
         ├─ sub-<label>[_ses-<label>]_task-<label>_events.tsv
         └─ sub-<label>[_ses-<label>]_task-<label>_events.json
```
As there are a variety of data formats in which motion data is recorded and there is no single standard that all researchers agree on this BEP proposes one format. For BIDS, EEG data MUST be stored in `.tsv` format. The data in their original format, if different from the supported formats, can be stored in the [`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data). The original data format can be valuable as it might contain more metadata than currently being specified in the `*_track_sys.json` file.

**Paragraph about stream synchronisation**

### Sidecar JSON (`*_motion.json`)
Generic fields MUST be present:

| **Key name**	| **Requirement level**	| **Data type**	| **Description**  |
| --------------|-----------------------|---------------|----------------- |
| TaskName  | REQUIRED          | string    | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric `[a-zA-Z0-9]` characters. For example TaskName "faces n-back" will correspond to task label facesnback. A RECOMMENDED convention is to name resting state task using labels beginning with `rest`. |

SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

| **Key name**	| **Requirement level**	| **Data type**	| **Description**  |
| --------------|-----------------------|---------------|----------------- |
| InstitutionAddress  | RECOMMENDED          | string    | The address of the institution in charge of the equipment that produced the composite instances.  |
| InstitutionalDepartmentName  | RECOMMENDED          | string    | The department in the institution in charge of the equipment that produced the composite instances.  |
| InstitutionName  | RECOMMENDED          | string    | The name of the institution in charge of the equipment that produced the composite instances.  |
| Instructions  | RECOMMENDED          | string    | Text of the instructions given to participants before the recording. |
| TaskDescription  | RECOMMENDED          | string    | Longer description of the task. |


Specific fields MUST be present:

| **Key name**	| **Requirement level**	| **Data type**	| **Description**  |
| --------------|-----------------------|---------------|----------------- |
| TrackingSystems  | REQUIRED          | string    | List of tracking systems used to record data in the corresponding *_motion.tsv file.  |
| TrackingSystemCount  | REQUIRED          | number    | Number of tracking systems in the corresponding *_motion.tsv file. This number should match the number of entries in the field “TrackingSystems”.  |

Specific fields SHOULD be present:

| **Key name**	| **Requirement level**	| **Data type**	| **Description**  |
| --------------|-----------------------|---------------|----------------- |
| EpochLength  | RECOMMENDED          | number    | Duration of individual epochs in seconds (e.g., 1) in case of epoched data. If recording was continuous,  leave out the field.  |
| MotionChannelCount  | RECOMMENDED          | number    | Number of motion channels included in the recording. A channel corresponds to a time series that has one value per time point. (e.g., a time series of coordinates for positions in 3D consists of 3 channels, each corresponding to the x, y, and z coordinates, respectively.)    |
| RecordingType  | RECOMMENDED          | string    | Defines whether the recording is  “continuous” or  “epoched”; this latter limited to time windows about events of interest (e.g., stimulus presentations, subject responses etc.)   |
| SubjectArtefactDescription  | RECOMMENDED          | string    | Freeform description of the observed subject artefact and its possible cause (e.g., “nausea from 20 min”, ”fall at 10 min”). If this field is left empty, it will be interpreted as absence of artifacts. |

Note that the field `TrackingSystems` has some required and RECOMMENDED fields in a nested json structure. These are to be described as follows:

Specific fields in `TrackingSystems` :

| **Key name**	| **Requirement level**	| **Data type**	| **Description**  |
| --------------|-----------------------|---------------|----------------- |
| SamplingFrequencyEffective  | REQUIRED          | number    | Effective sampling rate of the tracking system in Hz.  |
| SamplingFrequencyNominal  | REQUIRED          | number    | Nominal sampling rate of the tracking system in Hz.  |
| SoftwareVersions         | RECOMMENDED | string  | Manufacturer’s   designation of the acquisition software.
| StartTime                | RECOMMENDED | number  | Start time in   seconds in relation to the start of acquisition of the first data sample in   the corresponding neural dataset (negative values are allowed).|
| RecordingDuration        | RECOMMENDED | number  | Length of the   recording in seconds (e.g., 3600).|
| TrackedPointsCount       | RECOMMENDED | number  | Number of   different tracked points tracked in the system.|
| POSChannelCount          | RECOMMENDED | number  | Number of   position channels recorded by the system.|
| ORNTChannelCount         | RECOMMENDED | number  | Number of   orientation channels recorded by the system. |
| VELChannelCount          | RECOMMENDED | number  | Number of linear   velocity channels recorded by the system. |
| ANGVELChannelCount       | RECOMMENDED | number  | Number of   angular velocity channels recorded by the system. |
| ACCChannelCount          | RECOMMENDED | number  | Number of   acceleration channels recorded by the system.  |
| ANGACCChannelCount       | RECOMMENDED | number  | Number of   angular acceleration channels recorded by the system. |
| MAGNChannelCount         | RECOMMENDED | number  | Number of   magnetic field strength channels recorded by the system. |
| JNTANGChannelCount       | RECOMMENDED | number  | Number of joint   angle channels recorded by the system.  |
| ExternalSoftwareVersions | OPTIONAL    | string  | Names and   versions of additional software used for presentation or recording, other   than the software designated by the manufacture of the motion capture system   in field “SoftwareVersions”. |
| Manufacturer             | OPTIONAL    | string  | Manufacturer of   the motion tracking system.  |
| ManufacturersModelName   | OPTIONAL    | string  | Manufacturer’s   designation of the motion tracking hardware model.  |     

## Coordinate System JSON (`*_coordsystem.json`)
One important consideration for full description of motion data is the definition
of the system. The same position or orientation can be represented
in multiple ways depending on how the spatial axes in a coordinate system are defined
and which representational system is used. These aspects, while being crucial for
interpretability of shared data sets, are not addressed by BIDS for general continuous
data.
