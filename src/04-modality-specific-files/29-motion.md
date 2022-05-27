# Motion

Support for Motion was developed as a
[BIDS Extension Proposal](../07-extensions.md#bids-extension-proposals).
Please see [Citing BIDS](../01-introduction.md#citing-bids)
on how to appropriately credit this extension when referring to it in the
context of the academic literature.

Several [example Motion datasets](https://github.com/bids-standard/bids-examples)
have been formatted using this specification
and can be used for practical guidance when curating a new dataset.

## Motion recording data

Template:

```markdown
└─ sub-<label>\
  └─ \[ses-<label>]\
    └─ motion\
      ├─ sub-<label>\[\_ses-<label>]_task-<label>_tracksys-<label>_motion.tsv
      ├─ sub-<label>\[\_ses-<label>]_task-<label>_tracksys-<label>_motion.json
      ├─ sub-<label>\[\_ses-<label>]_task-<label>_tracksys-<label>_channels.tsv
      ├─ sub-<label>\[\_ses-<label>]_task-<label>_tracksys-<label>_coordsys.json
      ├─ sub-<label>\[\_ses-<label>]_task-<label>_events.tsv
      └─ sub-<label>\[\_ses-<label>]_task-<label>_events.json
```

A wide variety of motion capture systems are used in human research, resulting in
different native data formats. The current BEP specifically
deals any standard outputs from motion capture systems such as positions, orientations, acceleration among others. For camera-based
motion capture the raw camera footage falls out of scope. To share motion data
recorded using an optical system, typically the position or orientation or likewise system output is
formatted in BIDS, not the raw camera footage.

The extension is not limited to motion data in physical space but also encompasses
simulated movement in virtual space, as far as these are comparable to movements
in physical space. The extension is also not limited to the positions/orientations
of human body parts, other dynamic objects (physical or virtual) in the environment
whose motion is tracked may be included as additional indications of motion.

For the current BEP, motion data coming from one tracking system MUST be stored in a `*_motion.tsv` file. A tracking system is defined as a group of tracking devices that share hardware properties (same recording device) and/or software properties (for example same sampling rates). For example if the position of multiple optical markers is processed via one recording unit, this would be defined as a tracking system. Note that it is not uncommon to have multiple tracking systems to record at the same time. Each tracking system should have its own `*tracksys-<label>_motion.tsv` file. One column per channel per tracking system is intended in the `*tracksys-<label>_motion.tsv` file. The header of each column should correspond to one entry in a `*tracksys-<label>_channels.tsv` file. All relevant metadata about a tracking systems is stored in accompanying sidecar `*tracksys-<label>_motion.json` file. The data from each tracking system in their original format, if different from `.tsv`, can be stored in the [`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data). The original data format might additionally hold more metadata than currently being specified in the `*_motion.json` file.

### Sidecar JSON (`*_motion.json`)

Generic fields (shared with other BIDS modalities) MUST be present:

| **Key name** | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                   |
| ------------ | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TaskName     | REQUIRED              | string        | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric `[a-zA-Z0-9]` characters. |

Generic fields (shared with other BIDS modalities) SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

| **Key name**                | **Requirement level** | **Data type** | **Description**                                                                                     |
| --------------------------- | --------------------- | ------------- | --------------------------------------------------------------------------------------------------- |
| InstitutionAddress          | RECOMMENDED           | string        | The address of the institution in charge of the equipment that produced the composite instances.    |
| InstitutionalDepartmentName | RECOMMENDED           | string        | The department in the institution in charge of the equipment that produced the composite instances. |
| InstitutionName             | RECOMMENDED           | string        | The name of the institution in charge of the equipment that produced the composite instances.       |
| Instructions                | RECOMMENDED           | string        | Text of the instructions given to participants before the recording.                                |
| TaskDescription             | RECOMMENDED           | string        | Longer description of the task.                                                                     |

Specific MOTION fields MUST be present:

| **Key name**       | **Requirement level** | **Data type** | **Description**                                                                                                       |
| ------------------ | --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------- |
| SamplingFrequency  | REQUIRED              | number        | Nominal sampling rate of the tracking system in Hz.                                                                   |
| TrackingSystemName | REQUIRED              | string        | Name of the tracking system. The value should match the `tracksys` value of the corresponding *_motion.tsv file name. |

Motion specific fields SHOULD be present:

| **Key name**               | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| DeviceSerialNumber         | RECOMMENDED           | string        | The serial number of the equipment that produced the composite instances. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset.                                                                                                                                                                                                                                                                                                                 |
| MissingValues              | RECOMMENDED           | string        | How missing values are represented in the given tracking system, for example, “NaN”, “0”.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| MotionChannelCount         | RECOMMENDED           | number        | Number of motion channels included in the recording. A channel corresponds to a time series that has one value per time point. (e.g., a time series of coordinates for positions in 3D consists of 3 channels, each corresponding to the x, y, and z coordinates, respectively.)                                                                                                                                                                                                                                                 |
| RotationRule               | RECOMMENDED           | string        | In case orientation channels are present, indicate whether rotations are applied clockwise around an axis when seen from the positive direction (left-hand rule) or counter-clockwise (right-hand rule). Must be one of: “left-hand”, “right-hand”.                                                                                                                                                                                                                                                                              |
| RotationOrder              | RECOMMENDED           | string        | Specify the sequence in which the elemental rotations are applied around the extrinsic axes. A 3D rotation is represented about 3 different axes (Tait-Bryan convention). Must be one of: “XYZ”, ”XZY”, ”YXZ”, “YZX”, “ZXY”, “ZYX”.                                                                                                                                                                                                                                                                                              |
| SamplingFrequencyEffective | REQUIRED              | number        | Effective sampling rate of the tracking system in Hz. If duration of the corresponding recording is available, effective sampling rate is computed by dividing the `RecordingDuration` in seconds by the number of samples included in the time series. If not available, the field takes the same value as field `SamplingFrequency`.                                                                                                                                                                                           |
| SoftwareVersions           | RECOMMENDED           | string        | Manufacturer’s designation of the acquisition software.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| SpatialAxes                | RECOMMENDED           | string        | Refers to the coordinate system in which the motion data are to be interpreted, if the recorded data can be mapped to a fixed reference frame. A sequence of characters F/B (forward-backward), L/R (left-right), and U/D (up-down). The position of a character in the sequence determines which of the X,Y,Z axes it maps to. For example, “FRD” for  X-forward,  Y-right, Z-down. For 1D or 2D cases, only specify the used axes and use the character “_” for unused axes (“F_R” when the Y axis is not used, for instance). |
| SubjectArtefactDescription | RECOMMENDED           | string        | Freeform description of the observed subject artefact and its possible cause (e.g., “stopped at 20 min”, ”fall at 10 min”). If this field is left empty, it will be interpreted as absence of artifacts.                                                                                                                                                                                                                                                                                                                         |
| TrackedPointsCount         | RECOMMENDED           | number        | Number of different tracked points tracked in the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| ACCChannelCount            | RECOMMENDED           | number        | Number of acceleration channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ANGACCChannelCount         | RECOMMENDED           | number        | Number of angular acceleration channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ANGVELChannelCount         | RECOMMENDED           | number        | Number of angular velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| JNTANGChannelCount         | RECOMMENDED           | number        | Number of joint angle channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| LATENCYChannelCount        | RECOMMENDED           | number        | Number of latency channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| MAGNChannelCount           | RECOMMENDED           | number        | Number of magnetic field strength channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| MISCChannelCount           | RECOMMENDED           | number        | Number of miscellaneous channels whose types are not covered by restricted keywords for *_channels.tsv column `type`.                                                                                                                                                                                                                                                                                                                                                                                                            |
| POSChannelCount            | RECOMMENDED           | number        | Number of position channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| ORNTChannelCount           | RECOMMENDED           | number        | Number of orientation  channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| VELChannelCount            | RECOMMENDED           | number        | Number of linear velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ExternalSoftwareVersions   | OPTIONAL              | string        | Names and versions of additional software used for presentation or recording, other than the software designated by the manufacture of the motion capture system in field `SoftwareVersions`.                                                                                                                                                                                                                                                                                                                                    |
| StartTime                  | OPTIONAL              | number        | Start time in seconds in relation to the start of acquisition of the first data sample in the corresponding neural dataset (negative values are allowed). Can also be found in `*scans.tsv`.                                                                                                                                                                                                                                                                                                                                     |
| Manufacturer               | OPTIONAL              | string        | Manufacturer of the motion tracking system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| ManufacturersModelName     | OPTIONAL              | string        | Manufacturer’s designation of the motion tracking hardware model.                                                                                                                                                                                                                                                                                                                                                                                                                                                                |

Restricted keyword list for field `RotationRule`:

| **Keyword** | **Description**                                                                                                                                        |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| left-hand   | Rotation is following the left hand convention, such that the left thumb points in a direction, and the fingers curl along the orientation rotation.   |
| right-hand  | Rotation is following the right hand convention, such that the right thumb points in a direction, and the fingers curl along the orientation rotation. |

Restricted keyword list for field `RotationOrder`:

| **Keyword** | **Description**                   |
| ----------- | --------------------------------- |
| XYZ         | Sequence to follow for rotations. |
| XZY         | Sequence to follow for rotations. |
| YXZ         | Sequence to follow for rotations. |
| YZX         | Sequence to follow for rotations. |
| ZXY         | Sequence to follow for rotations. |
| ZYX         | Sequence to follow for rotations. |

Example \*tracksys-<label>\_motion.json :

```JSON
{
	"SamplingFrequency": 60,
	"SamplingFrequencyEffective": 60.00197437,
	"TaskName": "BIDS Motion fictive example",
	"TrackingSystemName": "IMU1",
	"TaskDescription": "walking and talking",
	"InstitutionAddress": "Fictive address",
	"InstitutionName": "Fictive Institution",
	"MotionChannelCount": 18,
	"RecordingDuration": 4667.641106,
	"RotationRule": "right-hand",
	"RotationOrder": "ZXY",
	"SpatialAxes": "FRU",
	"SubjectArtefactDescription": "n/a",
	"TrackedPointsCount" : 2,
	"ACCChannelCount": 6,
	"ANGACCChannelCount": 0,
	"ANGVELChannelCount": 6,
	"JNTANGChannelCount": 0,
	"MAGNChannelCount": 6,
	"ORNTChannelCount": 0,
	"POSChannelCount": 0,
	"VELChannelCount": 0,
	"Manufacturer": "BWSensing",
	"ManufacturersModelName": "BW-IMU600",
}
```

In this example, the `*_motion.json` contains data from one [inertial measurement uni (imu)](https://en.wikipedia.org/wiki/Motion_capture#Inertial_systems) tracking system. If there is an additional, e.g. optical [motion capture (omc)](https://en.wikipedia.org/wiki/Motion_capture#Optical_systems), tracking system, data would be stored in different files (`*motion.tsv`, `*motion.json`, `*channels.tsv`. Both systems can share one or multiple `tracked_point`, when tracking devices are placed on the same location.

Note that the date and time information SHOULD be stored in the Study key file [(`scans.tsv`)](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file). Date time information MUST be expressed as indicated in Units. The [`scans.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file) file contains the filename and the acquisition time of a recording, which can be used to synchronize streams. However, synchronization information between the two systems can also be stored using time stamps in the `*_motion.tsv` if available?.

## Channels description (`*_channels.tsv`)

```markdown
└─ sub-<label>\
  └─ \[ses-<label>]\
    └─ motion\
      └─ sub-<label>\[\_ses-<label>][\_task-<label>\]_channels.tsv
```

This file is REQUIRED as it makes it easy to browse or query over larger collections of datasets. The REQUIRED columns are channel  `component`, `name`,  `tracked_point`, `type` and `unit`. Any number of additional columns may be added to provide additional information about the channels. The `*tracksys-<label>_channels.tsv` file should give additional information about individual recorded channel, some of which my not be found summarized in `*motion.json`.

The columns of the channels description table stored in `*_channels.tsv` are:

MUST be present:

| **Key name**  | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                |
| ------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| component     | REQUIRED              | string        | Component of the representational system described in `*_coordinatesystem.tsv` that the channel contains.                                                                                      |
| name          | REQUIRED              | string        | Label of the channel. Entries have to match headers in (any) `*_motion.tsv.`                                                                                                                   |
| tracked_point | REQUIRED              | string        | Label of the point that is being tracked, for example, label of a tracker or a marker (`LeftFoot`, `RightWrist`).                                                                              |
| type          | REQUIRED              | string        | Type of data.                                                                                                                                                                                  |
| units         | REQUIRED              | string        | Physical unit of the value represented in this channel, for example, vm for virtual meters, radian or degrees for angular quantities. See the BIDS spec for guidelines for Units and Prefixes. |

SHOULD be present:

| **Key name**       | **Requirement level** | **Data type** | **Description**                                                                                                                                                             |
| ------------------ | --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| placement          | RECOMMENDED           | string        | Placement of the tracked point on the body (for example, participant, avatar centroid, torso, left arm). It can refer to an external vocabulary for describing body parts.  |
| description        | OPTIONAL              | string        | Brief free-text description of the channel, or other information of interest.                                                                                               |
| sampling_frequency | OPTIONAL              | number        | Nominal sampling rate of the channel in Hz. In case the sampling rates differ between channels or from SamplingFrequency in *_motion.json file, this can be specified here. |
| status_description | OPTIONAL              | string        | Brief free-text description of the channel, or other information of interest.                                                                                               |

Restricted keyword list for column `component` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword** | **Description**                                                                                                                                            |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x           | position along the X-axis, or rotation about the X-axis among the Euler angles that represent the orientation, or magnetic field strength along the X-axis |
| y           | position along the Y-axis or rotation about the Y-axis among the Euler angles that represent the orientation, or magnetic field strength along the Y-axis  |
| z           | position along the Z-axis or rotation about the z-axis among the Euler angles that represent the orientation, or magnetic field strength along the Z-axis  |
| n/a         | channels that have no corresponding spatial axis                                                                                                           |

Restricted keyword list for column `type` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword** | **Description**               |
| ----------- | ----------------------------- |
| ACC         | Acceleration                  |
| ANGACC      | Angular acceleration          |
| ANGVEL      | Angular velocity              |
| LATENCY     | Latency of samples in seconds |
| MAGN        | Magnetic field                |
| MISC        | Miscellaneous channels        |
| ORNT        | Orientation                   |
| POS         | Position in space             |
| VEL         | Velocity                      |

Example `channels.tsv`:

```Text
name        tracked_point  type   component units
t1_acc_x    LeftFoot      ACC    x         m/s^2
t1_acc_y	 LeftFoot     ACC    y         m/s^2
t1_acc_z	 LeftFoot      ACC    z         m/s^2
t1_gyro_x	  LeftFoot   	  ANGVEL	x 		   rad/s
t1_gyro_y	  LeftFoot   	  ANGVEL	y 		   rad/s
t1_gyro_z	  LeftFoot   	  ANGVEL	z 		   rad/s
…
t2_acc_x	 RightWrist    ACC		x		m/s^2
t2_acc_y	 RightWrist    ACC		y		m/s^2
t2_acc_z	 RightWrist    ACC		z		m/s^2
t2_gyro_x 	RightWrist    ANGVEL	x 		rad/s
t2_gyro_y	  RightWrist	 ANGVEL	y 		rad/s
t2_gyro_z	  RightWrist 	 ANGVEL	z 		rad/s
```
