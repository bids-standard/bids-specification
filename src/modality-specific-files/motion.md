# Motion

<!--Here insert link to actual manuscript?-->

For information on how to cite this extension when referencing it in the context of the academic literature, please read [Citing BIDS](../introduction.md#citing-bids).

This specification has been used to format a number of [example Motion datasets](https://github.com/bids-standard/bids-examples), which can be used as helpful guidance when curating new datasets.

## Motion recording data

{{ MACROS___make_filename_template(
"raw",
datatypes=["motion"],
suffixes=["motion", "channels", "events"])
}}

Template:

```markdown
└─ sub-<label>\
  └─ \[ses-<label>]\
    └─ motion\
   ├─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_motion.tsv
      ├─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_motion.json
      ├─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_channels.tsv
      ├─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_events.tsv
      └─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_events.json
```

A wide variety of motion capture systems are used in human research, resulting in different proprietary data formats. This BIDS extension deals with common outputs from motion capture systems such as positions, orientations, or their time derivatives. 

The extension is not limited to motion data in physical space but also encompasses simulated movement in virtual space, as far as these are comparable to movements in physical space. The extension is also not limited to the positions and orientations of human body parts. Other dynamic objects in the environment
whose motion is tracked may be included as additional tracked objects.

In MOTION-BIDS, positions (and their time derivatives) are represented as Cartesian coordinates along up to three spatial axes, and orientations (and their time derivatives) are represented as Euler angles. However, to cover recordings from computer graphics applications (for example, virtual 3D motion or immersive virtual reality recording in physical space), orientations are also allowed to be represented as quaternions. In this case, the quaternion channels can be distinguished from channels containing Euler angles based on the entries in columns `component` and `units` in the `*_channels.tsv` file . See subsection on `Channels description` for further details.

Motion data from one tracking system MUST be stored in a `*_motion.tsv` file. A tracking system is defined as a group of motion channels that share hardware properties (the recording device) and software properties (the recording duration and sampling rate). For example, if the position time series of multiple optical markers is processed via one recording unit, this can be defined as a single tracking system. Note that it is not uncommon to have multiple tracking systems to record at the same time. Each tracking system should have its own `*tracksys-<label>_motion.tsv` file. One column in the `*tracksys-<label>_motion.tsv` file is intended to represent one data channel. The ordering of columns has to match the order of rows in the `*channels.tsv` file for unambiguous assignment. All relevant metadata about a tracking systems is stored in accompanying sidecar `*tracksys-<label>_motion.json` file. The source data from each tracking system in their original format, if different from `.tsv`, can be stored in the [`/sourcedata` directory](../common-principles.md#source-vs-raw-vs-derived-data). The original data format may hold more metadata than currently specified in the `*_motion.json` file.

When multiple tracking systems are used to record motion or motion capture is used alongside the recording of other BIDS modalities, it is possible to temporally synchronise the recordings. A guideline to time synchronization between multiple modalities using recording onset and event time offset is described later in the specifications. To store the differences between recording onsets, `scans.tsv` files can be used.

To store events which relate to a tracking system, it is recommended to use designated events files per tracking system. Such an events file name would include the tracksys key and look like `sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_events.tsv`. The onsets in the event file can be related to the starting time of the tracking system in the `scans.tsv` file.

### Sidecar JSON (`*_motion.json`)

Generic fields (shared with other BIDS modalities) MUST be present:

{{ MACROS___make_sidecar_table("motion.motionGeneric") }}

| **Key name** | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                   |
| ------------ | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TaskName     | REQUIRED              | string        | Name of the task. No two tasks should have the same name. The task label included in the file name is derived from this TaskName field by removing all non-alphanumeric `[a-zA-Z0-9]` characters. |

Generic fields (shared with other BIDS modalities) SHOULD be present: For consistency between studies and institutions, we
encourage users to extract the values of these fields from the actual raw data.
Whenever possible, please avoid using ad hoc wording.

{{ MACROS___make_sidecar_table("motion.motionRecommended") }}

| **Key name**                | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                  |
| --------------------------- | --------------------- | ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| InstitutionAddress          | RECOMMENDED           | string        | The address of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                                                                 |
| InstitutionalDepartmentName | RECOMMENDED           | string        | The department in the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                                                              |
| InstitutionName             | RECOMMENDED           | string        | The name of the institution in charge of the equipment that produced the composite instances.                                                                                                                                                                                                                    |
| Instructions                | RECOMMENDED           | string        | Text of the instructions given to participants before the recording.                                                                                                                                                                                                                                             |
| TaskDescription             | RECOMMENDED           | string        | Longer description of the task.                                                                                                                                                                                                                                                                                  |
| DeviceSerialNumber          | OPTIONAL              | string        | The serial number of the equipment that produced the composite instances. This would be the serial number of the tracking system, rather than the single recording units. A pseudonym can also be used to prevent the equipment from being identifiable, as long as each pseudonym is unique within the dataset. |
| ExternalSoftwareVersions    | OPTIONAL              | string        | Names and versions of additional software used for presentation or recording, other than the software designated by the manufacture of the motion capture system in field `SoftwareVersions`.                                                                                                                    |
| Manufacturer                | OPTIONAL              | string        | Manufacturer of the motion tracking system.                                                                                                                                                                                                                                                                      |
| ManufacturersModelName      | OPTIONAL              | string        | Manufacturer’s designation of the motion tracking hardware model.                                                                                                                                                                                                                                                |
| SoftwareVersions            | OPTIONAL              | string        | Manufacturer’s designation of the acquisition software.                                                                                                                                                                                                                                                          |

Motion specific fields MUST be present:

{{ MACROS___make_sidecar_table("motion.motionRequired") }}

| **Key name**       | **Requirement level** | **Data type** | **Description**                                                                                                     |
| ------------------ | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------- |
| SamplingFrequency  | REQUIRED              | number        | Nominal sampling rate of the tracking system in Hz.                                                                 |
| TrackingSystemName | REQUIRED              | string        | Name of the tracking system. The value must match the `tracksys` label of the corresponding *_motion.tsv file name. |

Motion specific fields SHOULD be present:

{{ MACROS___make_sidecar_table("motion.motionMoreRecommended") }}

| **Key name**               | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| -------------------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| MissingValues              | RECOMMENDED           | string        | How missing values are represented in the given tracking system, for example, "NaN", "0".                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| MotionChannelCount         | RECOMMENDED           | number        | Number of motion channels included in the recording. A channel corresponds to a time series that has one value per time point. (for example, a time series of coordinates for positions in 3D consists of 3 channels, each corresponding to the x, y, and z coordinates, respectively.)                                                                                                                                                                                                                                         |
| RotationRule               | RECOMMENDED           | string        | In case orientation channels are present, indicate whether rotations are applied clockwise around an axis when seen from the positive direction (left-hand rule) or counter-clockwise (right-hand rule). Must be one of: "left-hand", "right-hand" or "n/a".                                                                                                                                                                                                                                                                    |
| RotationOrder              | RECOMMENDED           | string        | Specify the sequence in which the elemental rotations are applied around the extrinsic axes. A 3D rotation is represented about 3 different axes (Tait-Bryan convention). Must be one of: "XYZ", "XZY", "YXZ", "YZX", "ZXY", "ZYX" or "n/a".                                                                                                                                                                                                                                                                                    |
| SamplingFrequencyEffective | RECOMMENDED           | number        | Effective sampling rate of the tracking system in Hz. If duration of the corresponding recording is available, effective sampling rate is computed by dividing the `RecordingDuration` in seconds by the number of samples included in the time series. If not available, the field takes the same value as field `SamplingFrequency`.                                                                                                                                                                                          |
| SpatialAxes                | RECOMMENDED           | string        | Refers to the coordinate system in which the motion data are to be interpreted, if the recorded data can be mapped to a fixed reference frame. A sequence of characters F/B (forward-backward), L/R (left-right), and U/D (up-down). The position of a character in the sequence determines which of the X,Y,Z axes it maps to. For example, "FRD" for  X-forward, Y-right, Z-down. For 1D or 2D cases, only specify the used axes and use the character "_" for unused axes ("F_R" when the Y axis is not used, for instance). |
| SubjectArtefactDescription | RECOMMENDED           | string        | Freeform description of the observed subject artefact and its possible cause (for example: "stopped at 20 min", "fall at 10 min"). If this field is left empty, it will be interpreted as absence of artifacts.                                                                                                                                                                                                                                                                                                                 |
| TrackedPointsCount         | RECOMMENDED           | number        | Number of different points tracked in a motion tracking system.                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ACCELChannelCount          | RECOMMENDED           | number        | Number of acceleration channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| ANGACCChannelCount         | RECOMMENDED           | number        | Number of angular acceleration channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| GYROChannelCount           | RECOMMENDED           | number        | Number of angular velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| JNTANGChannelCount         | RECOMMENDED           | number        | Number of joint angle channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| LATENCYChannelCount        | RECOMMENDED           | number        | Number of latency channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| MAGNChannelCount           | RECOMMENDED           | number        | Number of magnetic field strength channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| MISCChannelCount           | RECOMMENDED           | number        | Number of miscellaneous channels whose types are not covered by restricted keywords for *_channels.tsv column `type`.                                                                                                                                                                                                                                                                                                                                                                                                           |
| POSChannelCount            | RECOMMENDED           | number        | Number of position channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ORNTChannelCount           | RECOMMENDED           | number        | Number of orientation  channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| VELChannelCount            | RECOMMENDED           | number        | Number of linear velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| StartTime                  | OPTIONAL              | number        | Start time in seconds in relation to the start of acquisition of the first data sample in the corresponding neural dataset (negative values are allowed). Can also be found in `*scans.tsv`.                                                                                                                                                                                                                                                                                                                                    |

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

Example `*_tracksys-<label>_motion.json`:

```JSON
{
 "SamplingFrequency": 60,
 "SamplingFrequencyEffective": 60.00197437,
 "TaskName": "BIDS Motion fictive example",
 "TrackingSystemName": "imu1",
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
 "ACCELChannelCount": 6,
 "ANGACCChannelCount": 0,
 "GYROChannelCount": 6,
 "JNTANGChannelCount": 0,
 "MAGNChannelCount": 6,
 "ORNTChannelCount": 0,
 "POSChannelCount": 0,
 "VELChannelCount": 0,
 "Manufacturer": "BWSensing",
 "ManufacturersModelName": "BW-IMU600",
}
```

In this example, the `*_motion.json` contains data from one tracking system consisting of two [inertial measurement units (imu)](https://en.wikipedia.org/wiki/Motion_capture#Inertial_systems). If there are additional, for example optical [motion capture (omc)](https://en.wikipedia.org/wiki/Motion_capture#Optical_systems), tracking systems, data from each tracking system would be stored in different files (`*_tracksys-<label>_motion.tsv`, `*_tracksys-<label>_motion.json`, `*_tracksys-<label>_channels.tsv`. All specified tracking systems can share  `tracked_point` defined in `*_channels.tsv`, when tracking devices are placed on the same location.

Note that the onsets of the recordings SHOULD be stored in the study key file [(`scans.tsv`)](../modality-agnostic-files.md#scans-file). Here, date-time information MUST be expressed as indicated in [Units](../common-principles.md#units). The [`scans.tsv`](../modality-agnostic-files.md#scans-file) file contains the filename and the acquisition time of a recording, which can be used to synchronize multiple recordings. However, synchronization information between the two systems can also be stored using channel `latency` in the `*_motion.tsv` if available.

## Channels description (`*_channels.tsv`)

{{ MACROS___make_filename_template(
"raw",
datatypes=["motion"],
suffixes=["channels"])
}}

```markdown
└─ sub-<label>\
  └─ \[ses-<label>]\
    └─ motion\
      └─ sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_channels.tsv
```

This file is REQUIRED as it makes it easy to browse or query over larger collections of datasets. The REQUIRED columns are channel  `component`, `name`,  `tracked_point`, `type` and `unit`. Any number of additional columns may be added to provide additional information about the channels. The `*tracksys-<label>_channels.tsv` file should give additional information about individual recorded channel, some of which my not be found summarized in `*motion.json`.

The columns of the channels description table stored in `*_channels.tsv` are:

MUST be present:

| **Key name**  | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                |   |
| ------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | - |
| component     | REQUIRED              | string        | Component of the representational system described in `*_motion.json` that the channel contains. Must be one of: "x" ,"y", "z", "quat_x", "quat_y", "quat_z", "quat_w", "n/a".                                                                                                                                                                                                                                                                                                 |   |
| name          | REQUIRED              | string        | Label of the channel.                                                                                                                                                                                                                                                                                                                                                                                                                                                          |   |
| tracked_point | REQUIRED              | string        | Label of the point that is being tracked, for example, label of a tracker or a marker (`LeftFoot`, `RightWrist`).                                                                                                                                                                                                                                                                                                                                                              |   |
| type          | REQUIRED              | string        | Type of data. Position, orientation, acceleration or any related format. Can also be latency. Must be one of: "ACCEL", "ANGACC", "GYRO", "JNTANG", "LATENCY", "MAGN", "MISC", "ORNT", "POS", "TIME", "VEL".                                                                                                                                                                                                                                                                    |   |
| units         | REQUIRED              | string        | Physical or virtual unit of the value represented in this channel, for example, `rad` radian or `deg` degrees for angular quantities or `m` for position data. See the BIDS spec for guidelines for Units and Prefixes. If motion data is recorded in a virtual space and deviate from standard SI units, the unit used MUST be specified in the sidecar `*_motion.json` file (for example `vm` for virtual meters). `rad` is used for euler angles and `n/a` for quaternions. |   |

SHOULD be present:

| **Key name**       | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                              |
| ------------------ | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| placement          | RECOMMENDED           | string        | Placement of the tracked point on the body (for example, participant, avatar centroid, torso, left arm). It can refer to an external vocabulary for describing body parts.                                                                                                                   |
| description        | OPTIONAL              | string        | Brief free-text description of the channel, or other information of interest.                                                                                                                                                                                                                |
| sampling_frequency | OPTIONAL              | number        | Nominal sampling rate of the channel in Hz. In case the sampling rates differ between channels or from SamplingFrequency in *_motion.json file, this can be specified here.                                                                                                                  |
| status_description | OPTIONAL              | string        | Brief free-text description of the channel, or other information of interest.                                                                                                                                                                                                                |
| status             | OPTIONAL              | string        | Data quality observed on the channel. A channel is considered bad if its data quality is compromised by excessive noise. If quality is unknown, then a value of n/a may be used. Description of noise type SHOULD be provided in [status_description]. Must be one of: "good", "bad", "n/a". |

Restricted keyword list for column `component`. When using quaternions to represent orientations, the axial components that corresponds to the three spatial axes must be specified as "quat_x", "quat_y", "quat_z", and the non-axial component as "quat_w".

| **Keyword** | **Description**                                                                                                                                            |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x           | position along the X-axis, or rotation about the X-axis among the Euler angles that represent the orientation, or magnetic field strength along the X-axis |
| y           | position along the Y-axis or rotation about the Y-axis among the Euler angles that represent the orientation, or magnetic field strength along the Y-axis  |
| z           | position along the Z-axis or rotation about the Z-axis among the Euler angles that represent the orientation, or magnetic field strength along the Z-axis  |
| quat_x      | quaternion component associated with the X-axis                                                                                                            |
| quat_y      | quaternion component associated with the Y-axis                                                                                                            |
| quat_z      | quaternion component associated with the Z-axis                                                                                                            |
| quat_w      | non-axial quaternion component                                                                                                                             |
| n/a         | channels that have no corresponding spatial axis                                                                                                           |

Restricted keyword list for column `type` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword** | **Description**               |
| ----------- | ----------------------------- |
| ACCEL       | Acceleration                  |
| ANGACC      | Angular acceleration          |
| GYRO        | Angular velocity              |
| LATENCY     | Latency of samples in seconds |
| MAGN        | Magnetic field                |
| MISC        | Miscellaneous channels        |
| ORNT        | Orientation                   |
| POS         | Position in space             |
| VEL         | Velocity                      |

Example `*channels.tsv`:

```Text
name        tracked_point  type   component units
t1_acc_x    LeftFoot      ACCEL    x         m/s^2
t1_acc_y  LeftFoot     ACCEL    y         m/s^2
t1_acc_z  LeftFoot      ACCEL    z         m/s^2
t1_gyro_x   LeftFoot      GYRO x      rad/s
t1_gyro_y   LeftFoot      GYRO y      rad/s
t1_gyro_z   LeftFoot      GYRO z      rad/s
…
t2_acc_x  RightWrist    ACCEL  x  m/s^2
t2_acc_y  RightWrist    ACCEL  y  m/s^2
t2_acc_z  RightWrist    ACCEL  z  m/s^2
t2_gyro_x  RightWrist    GYRO x   rad/s
t2_gyro_y   RightWrist  GYRO y   rad/s
t2_gyro_z   RightWrist   GYRO z   rad/s
```

{{ MACROS___make_columns_table("motion.motionChannels") }}
