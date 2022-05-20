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
<<<<<<< HEAD

=======
>>>>>>> 57f8b1e39c8dfd69adeba5da25fd87b188940992
```markdown
└─ sub-<label>\
└─ \[ses-<label>]\
└─ motion\
├─ sub-<label>\[\_ses-<label>][\_task-<label>\]_tracksys-<label>\_motion.tsv
├─ sub-<label>\[\_ses-<label>][\_task-<label>\]_motion.json
├─ sub-<label>\[\_ses-<label>][\_task-<label>\]_channels.tsv
├─ sub-<label>\[\_ses-<label>][\_task-<label>\]_coordsys.json
├─ sub-<label>\[\_ses-<label>][\_task-<label>\]_events.tsv
└─ sub-<label>\[\_ses-<label>][\_task-<label>\]_events.json
```
<<<<<<< HEAD

=======
>>>>>>> 57f8b1e39c8dfd69adeba5da25fd87b188940992
A wide variety of motion capture systems are used in human research, resulting in
different native data formats. The current BEP specifically
deals with positions, orientations, and their time derivatives. For camera-based
motion capture the raw camera footage falls out of scope. To share motion data
recorded using an optical system, only the position or orientation output is
formatted in BIDS, not the input camera footage.

The extension is not limited to motion data in physical space but also encompasses
simulated movement in virtual space, as far as these are comparable to movements
in physical space. The extension is also not limited to the positions/orientations
of human body parts, other dynamic objects (physical or virtual) in the environment
whose motion is tracked may be included as additional indications of motion.

For the current BEP, motion data MUST be stored in a `*_motion.tsv` file. A tracking system is defined as a group of tracking devices that share hardware properties (same recording device) and/or software properties (for example same sampling rates). For example if the position of multiple optical markers is processed via one recording unit, this would be defined as a tracking system. Note that it is not uncommon to have multiple tracking systems to record at the same time. Each tracking system should have its own `*[tracksys-<label>]_motion.tsv` file. One column per channel per tracking system is intended in the `*[tracksys-<label>]_motion.tsv` file. The header of each column should correspond to one entry in a `*_channels.tsv` file. All relevant metadata about a tracking systems is stored in the sidecar `*_motion.json` file in the subfield trackingsystem. The data from each tracking system in their original format, if different from `.tsv`, can be stored in the [`/sourcedata` directory](../02-common-principles.md#source-vs-raw-vs-derived-data). The original data format might additionally hold more metadata than currently being specified in the `*_motion.json` file.

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

Motion specific fields MUST be present:

| **Key name**        | **Requirement level** | **Data type** | **Description**                                                                                          |
| ------------------- | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------- |
| TrackingSystems     | REQUIRED              | string        | List of tracking systems used to record data in the corresponding `*[tracksys-<label>]_motion.tsv` file. |
| TrackingSystemCount | REQUIRED              | number        | Number of tracking systems corresponding to the number of `*[tracksys-<label>]_motion.tsv` files.        |

Motion specific fields SHOULD be present:

| **Key name**               | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                         |
| -------------------------- | --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| EpochLength                | RECOMMENDED           | number        | Duration of individual epochs in seconds (for example, 1) in case of epoched data. If recording was continuous,  leave out the field.                                                                                                                                                   |
| MotionChannelCount         | RECOMMENDED           | number        | Number of motion channels included in the recording. A channel corresponds to a time series that has one value per time point. (for example, a time series of coordinates for positions in 3D consists of 3 channels, each corresponding to the x, y, and z coordinates, respectively.) |
| RecordingType              | RECOMMENDED           | string        | Defines whether the recording is  "continuous” or  "epoched”; this latter limited to time windows about events of interest (for example, stimulus presentations, subject responses, and so on)                                                                                          |
| SubjectArtefactDescription | RECOMMENDED           | string        | Freeform description of the observed subject artefact and its possible cause (for example, "nausea from 20 min”, ”fall at 10 min”). If this field is left empty, it will be interpreted as absence of artifacts.                                                                        |

Note that the field `TrackingSystems` has some REQUIRED and RECOMMENDED fields in a nested json structure. These are to be described as follows:

Specific fields in `TrackingSystems` :

<<<<<<< HEAD
| **Key name**               | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| -------------------------- | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TrackingSystemName         | REQUIRED              | string        | Name of the tracking system. The value should match the “tracksys” value of the corresponding `*_motion.tsv` file name.                                                                                                                                                                                                                                                                                                                                                                                                          |
| SamplingFrequencyEffective | REQUIRED              | number        | Effective sampling rate of the tracking system in Hz. If available, otherwise same as `SamplingFrequency`.                                                                                                                                                                                                                                                                                                                                                                                                                       |
| SamplingFrequency          | REQUIRED              | number        | Nominal sampling rate of the tracking system in Hz.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| MissingValues              | RECOMMENDED           | string        | How missing values are represented in the given tracking system, for example, “NaN”, “0”.                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| SoftwareVersions           | RECOMMENDED           | string        | Manufacturer’s   designation of the acquisition software.                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| RecordingDuration          | RECOMMENDED           | number        | Length of the   recording in seconds (for example 3600).                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| TrackedPointsCount         | RECOMMENDED           | number        | Number of   different tracked points tracked in the system. A tracked point is a specific point on an object that is being tracked, which can be a body part or an inanimate object.                                                                                                                                                                                                                                                                                                                                             |
| ANGACCChannelCount         | RECOMMENDED           | number        | Number of angular acceleration channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| ANGVELChannelCount         | RECOMMENDED           | number        | Number of angular velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| JNTANGChannelCount         | RECOMMENDED           | number        | Number of joint angle channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| MAGNChannelCount           | RECOMMENDED           | number        | Number of magnetic field strength channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ORNTChannelCount           | RECOMMENDED           | number        | Number of orientation channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| POSChannelCount            | RECOMMENDED           | number        | Number of position channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| VELChannelCount            | RECOMMENDED           | number        | Number of linear velocity channels recorded by the system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| ExternalSoftwareVersions   | OPTIONAL              | string        | Names and   versions of additional software used for presentation or recording, other   than the software designated by the manufacture of the motion capture system   in field "SoftwareVersions”.                                                                                                                                                                                                                                                                                                                              |
| Manufacturer               | OPTIONAL              | string        | Manufacturer of   the motion tracking system.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| ManufacturersModelName     | OPTIONAL              | string        | Manufacturer’s   designation of the motion tracking hardware model.                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| SpatialAxes                | RECOMMENDED           | string        | Refers to the coordinate system in which the motion data are to be interpreted, if the recorded data can be mapped to a fixed reference frame. A sequence of characters F/B (forward-backward), L/R (left-right), and U/D (up-down). The position of a character in the sequence determines which of the X,Y,Z axes it maps to. For example, “FRD” for  X-forward,  Y-right, Z-down. For 1D or 2D cases, only specify the used axes and use the character “_” for unused axes (“F_R” when the Y axis is not used, for instance). |
| RotationRule               | RECOMMENDED           | string        | In case orientation channels are present, indicate whether rotations are applied clockwise around an axis when seen from the positive direction (left-hand rule) or counter-clockwise (right-hand rule)                                                                                                                                                                                                                                                                                                                          |
| RotationOrder              | RECOMMENDED           | string        | Specify the sequence in which the elemental rotations are applied around the extrinsic axes. A 3D rotation is represented about 3 different axes (Tait-Bryan convention).                                                                                                                                                                                                                                                                                                                                                        |

Restricted keyword list for field `RotationRule`:

| **Keyword** | **Description**                |
| ----------- | ------------------------------ |
| left-hand   | Left-hand rule for rotations.  |
| right-hand  | Right-hand rule for rotations. |

Restricted keyword list for field `RotationOrder`:

| **Keyword** | **Description**                   |
| ----------- | --------------------------------- |
| XYZ         | Sequence of axis to do rotations. |
| XZY         | Sequence of axis to do rotations. |
| YXZ         | Sequence of axis to do rotations. |
| YZX         | Sequence of axis to do rotations. |
| ZXY         | Sequence of axis to do rotations. |
| ZYX         | Sequence of axis to do rotations. |
=======
| **Key name**               | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                     |
| -------------------------- | --------------------- | ------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| TrackingSystemName | REQUIRED              | string        | Name of the tracking system. The value should match the “tracksys” value of the corresponding `*_motion.tsv` file name.                                                                                    |
| SamplingFrequencyEffective | REQUIRED              | number        | Effective sampling rate of the tracking system in Hz. If available, otherwise same as `SamplingFrequency`.                                                                                   |
| SamplingFrequency   | REQUIRED              | number        | Nominal sampling rate of the tracking system in Hz.                                                                                                                                                 |
| MissingValues              | RECOMMENDED           | string        | How missing values are represented in the given tracking system, for example, “NaN”, “0”.                                                                                                           |
| SoftwareVersions           | RECOMMENDED           | string        | Manufacturer’s   designation of the acquisition software.                                                                                                                                           |
| RecordingDuration          | RECOMMENDED           | number        | Length of the   recording in seconds (for example 3600).                                                                                                                                            |
| TrackedPointsCount         | RECOMMENDED           | number        | Number of   different tracked points tracked in the system. A tracked point is a specific point on an object that is being tracked, which can be a body part or an inanimate object.                |
| ANGACCChannelCount         | RECOMMENDED           | number        | Number of angular acceleration channels recorded by the system.                                                                                                                                     |
| ANGVELChannelCount         | RECOMMENDED           | number        | Number of angular velocity channels recorded by the system.                                                                                                                                         |
| JNTANGChannelCount         | RECOMMENDED           | number        | Number of joint angle channels recorded by the system.                                                                                                                                              |
| MAGNChannelCount           | RECOMMENDED           | number        | Number of magnetic field strength channels recorded by the system.                                                                                                                                  |
| ORNTChannelCount           | RECOMMENDED           | number        | Number of orientation channels recorded by the system.                                                                                                                                              |
| POSChannelCount            | RECOMMENDED           | number        | Number of position channels recorded by the system.                                                                                                                                                 |
| VELChannelCount            | RECOMMENDED           | number        | Number of linear velocity channels recorded by the system.                                                                                                                                          |
| ExternalSoftwareVersions   | OPTIONAL              | string        | Names and   versions of additional software used for presentation or recording, other   than the software designated by the manufacture of the motion capture system   in field "SoftwareVersions”. |
| Manufacturer               | OPTIONAL              | string        | Manufacturer of   the motion tracking system.                                                                                                                                                       |
| ManufacturersModelName     | OPTIONAL              | string        | Manufacturer’s   designation of the motion tracking hardware model.                                                                                                                                 |
| SpatialAxes     | RECOMMENDED              | string        | Refers to the coordinate system in which the motion data are to be interpreted, if the recorded data can be mapped to a fixed reference frame. A sequence of characters F/B (forward-backward), L/R (left-right), and U/D (up-down). The position of a character in the sequence determines which of the X,Y,Z axes it maps to. For example, “FRD” for  X-forward,  Y-right, Z-down. For 1D or 2D cases, only specify the used axes and use the character “_” for unused axes (“F_R” when the Y axis is not used, for instance).                                                                                                                |
| RotationRule     | RECOMMENDED              | string        | In case orientation channels are present, indicate whether rotations are applied clockwise around an axis when seen from the positive direction (left-hand rule) or counter-clockwise (right-hand rule)                                                                                                                                 |
| RotationOrder     | RECOMMENDED              | string        | Specify the sequence in which the elemental rotations are applied around the extrinsic axes. A 3D rotation is represented about 3 different axes (Tait-Bryan convention).                                                                                                                                 |

Restricted keyword list for field `RotationRule`:

| **Keyword**  | **Description**                  |
| ------------ | -------------------------------- |
| left-hand    | Left-hand rule for rotations.    |
| right-hand   | Right-hand rule for rotations.   |

Restricted keyword list for field `RotationOrder`:

| **Keyword**  | **Description**                  |
| ------------ | -------------------------------- |
| XYZ          | Sequence of axis to do rotations.|
| XZY          | Sequence of axis to do rotations.|
| YXZ          | Sequence of axis to do rotations.|
| YZX          | Sequence of axis to do rotations.|
| ZXY          | Sequence of axis to do rotations.|
| ZYX          | Sequence of axis to do rotations.|
>>>>>>> 57f8b1e39c8dfd69adeba5da25fd87b188940992

Example:

```JSON
{
  "InstitutionName": "Kiel University",
  "InstitutionalDepartmentName": "Department of Neurology",
  "MotionChannelCount": 297,
  "RecordingType":"continuous",
  "TaskDescription": "walking backwards",
  "TaskName": "backwards",
  "TrackedPointsCountTotal": 67,
  "TrackingSystems": [
	   {
      "TrackingSystemName":"imu",
		  "Manufacturer": "Noraxon Inc.",
		  "ManufacturersModelName": "myoMOTION",
		  "SamplingFrequency": 200,
      "SamplingFrequencyEffective": 199.9105145,
		  "TrackedPointsCount": 16,
		  "POSChannelCount": 0,
		  "ORNTChannelCount": 0,
		  "VELChannelCount": 0,
		  "ANGVELChannelCount": 48,
		  "ACCChannelCount": 48,
		  "ANGACCChannelCount": 0,
		  "MAGNChannelCount": 48,
		  "JNTANGChannelCount": 0,
		  "DeviceSerialNumber": null,
		  "SoftwareVersions": null,
		  "ExternalSoftwareVersions": null,
		  "RecordingDuration": 11.18000224},

	  {
      "TrackingSystemName":"omc",
		  "Manufacturer": "Qualisys",
		  "ManufacturersModelName": "AB",
		  "SamplingFrequency": 200,
      "SamplingFrequencyEffective": 199.9070632,
		  "TrackedPointsCount": 51,
		  "POSChannelCount": 153,
		  "ORNTChannelCount": 0,
		  "VELChannelCount": 0,
		  "ANGVELChannelCount": 0,
		  "ACCChannelCount": 0,
		  "ANGACCChannelCount": 0,
		  "MAGNChannelCount": 0,
		  "JNTANGChannelCount": 0,
		  "DeviceSerialNumber": null,
		  "SoftwareVersions": null,
		  "ExternalSoftwareVersions": null,
		  "RecordingDuration": 10.76500232}
	]
}


```

In this example, the `*_motion.json` contains two `TrackingSystems`. One is a [inertial measurement uni (imu)](https://en.wikipedia.org/wiki/Motion_capture#Inertial_systems) system, the other is a optical [motion capture system (omc)](https://en.wikipedia.org/wiki/Motion_capture#Optical_systems). Both have three times as many channels as they have tracked points, because every tracked point is recorded along the x,y and z axis.

Note that the date and time information SHOULD be stored in the Study key file [(`scans.tsv`)](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file). Date time information MUST be expressed as indicated in Units. The [`scans.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file) file contains the filename and the acquisition time of a recording, which can be used to synchronize streams. *However, synchronization information between the two systems can also be stored using time stamps in the `*_motion.tsv` if available?.*

## Channels description (`*_channels.tsv`)
<<<<<<< HEAD

=======
>>>>>>> 57f8b1e39c8dfd69adeba5da25fd87b188940992
```markdown
└─ sub-<label>\
└─ \[ses-<label>]\
└─ motion\
└─ sub-<label>\[\_ses-<label>][\_task-<label>\]_channels.tsv
```

This file is REQUIRED as it makes it easy to browse or query over larger collections of datasets. The REQUIRED columns are channel `name`, `type`, `tracked_point`, `tracking_system`, `component` and `unit`. Any number of additional columns may be added to provide additional information about the channels. The `*_channels.tsv` file should give additional information about individual recorded channel, some of which my not be found summarised in `TrackingSystems`.

The columns of the channels description table stored in `*_channels.tsv` are:

MUST be present:

| **Key name**    | **Requirement level** | **Data type** | **Description**                                                                                                                                                                                                     |
| --------------- | --------------------- | ------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| name            | REQUIRED              | string        | Label of the channel. Entries have to match headers in (any) `*_motion.tsv.`                                                                                                                                        |
| tracked_point   | REQUIRED              | string        | Label of the point that is being tracked, for example, label of a tracker or a marker (“LeftFoot”, “RightWrist”).                                                                                                   |
| tracking_system | REQUIRED              | string        | Label of the tracking system the channel belongs to. Entry has to correspond to one of the entries in field `TrackingSystems` in `*_motion.json` and labels in key-value pair `*[_tracksys_<label>]` in file names. |
| type            | REQUIRED              | string        | Type of data.                                                                                                                                                                                                       |
| component       | REQUIRED              | string        | Component of the representational system described in `*_coordinatesystem.tsv` that the channel contains.                                                                                                           |
| units           | REQUIRED              | string        | Physical unit of the value represented in this channel, for example, vm for virtual meters, radian or degrees for angular quantities. See the BIDS spec for guidelines for Units and Prefixes.                      |

SHOULD be present:

| **Key name** | **Requirement level** | **Data type** | **Description**                                                                                                                                                            |
| ------------ | --------------------- | ------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| placement    | RECOMMENDED           | string        | Placement of the tracked point on the body (for example, participant, avatar centroid, torso, left arm). It can refer to an external vocabulary for describing body parts. |
| description  | OPTIONAL              | string        | Brief free-text description of the channel, or other information of interest.                                                                                              |

Restricted keyword list for column `type` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword**  | **Description**                  |
| ------------ | -------------------------------- |
| ACC          | Acceleration                     |
| ANGACC       | Angular acceleration             |
| ANGVEL       | Angular velocity                 |
| ORNT         | Orientation                      |
| POS          | Position in space                |
| VEL          | Velocity                         |
| *TIMESTAMPS* | *Timestamps of recorded samples* |

Restricted keyword list for column `component` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword** | **Description**         |
| ----------- | ----------------------- |
| X           | entity along the X-axis |
| Y           | entity along the Y-axis |
| Z           | entity along the Z-axis |

Example `channels.tsv`:

```Text
name		 tracked_point	tracking_system	type	  component	units
t1_acc_x	 LeftFoot	     IMU1acc		    ACC	    x		  m/s^2
t1_acc_y	 LeftFoot	     IMU1acc		    ACC	    y		  m/s^2
t1_acc_z	 LeftFoot	     IMU1acc		    ACC	    z		  m/s^2
t1_gyro_x	LeftFoot	     IMU1gyro	       ANGVEL	 x		  rad/s
t1_gyro_y	LeftFoot	     IMU1gyro	       ANGVEL	 y		  rad/s
t1_gyro_z	LeftFoot	     IMU1gyro	       ANGVEL	 z		  rad/s
…
t2_acc_x	 RightWrist 	  IMU2		       ACC	    x		  m/s^2
t2_acc_y	 RightWrist	   IMU2		       ACC	    y		  m/s^2
t2_acc_z	 RightWrist	   IMU2		       ACC	    z          m/s^2
t2_gyro_x    RightWrist	   IMU2		       ANGVEL	 x	      rad/s
…
m1_pos_x	 LeftThigh	    OPTpos		     POS	    x		  m
m1_pos_y	 LeftThigh	    OPTpos		     POS	    y		  m
m1_pos_z	 LeftThigh	    OPTpos		     POS	    z		  m

```
