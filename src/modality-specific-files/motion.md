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

A wide variety of motion capture systems are used in human research, resulting in different proprietary data formats.
This BIDS extension deals with common outputs from motion capture systems such as positions, orientations, or their time derivatives.

The extension is not limited to motion data in physical space but also encompasses simulated movement in virtual space, as far as these are comparable to movements in physical space.
The extension is also not limited to the positions and orientations of human body parts.
Other dynamic objects in the environment whose motion is tracked may be included as additional tracked objects.
This specification does not include raw camera fotages, either from camera-based motion captures or optical system recordigns
(where typically the positions and orientations of objects derived from the video data are formatted in BIDS, but not the raw camera footage).
In this specification, positions (and their time derivatives) are represented as Cartesian coordinates along up to three spatial axes,
and orientations (and their time derivatives) are represented as Euler angles.
However, to cover recordings from computer graphics applications (for example, virtual 3D motion or immersive virtual reality recording in physical space),
orientations are also allowed to be represented as quaternions.
In this case, the quaternion channels can be distinguished from channels containing Euler angles based on the entries in columns `component` and `units` in the `*_channels.tsv` file.
See subsection on `Channels description` for further details.

Motion data from one tracking system MUST be stored in a `*_motion.tsv` file.
A tracking system is defined as a group of motion channels that share hardware properties (the recording device) and software properties (the recording duration and sampling rate).
For example, if the position time series of multiple optical markers is processed via one recording unit, this can be defined as a single tracking system.
Note that it is not uncommon to have multiple tracking systems to record at the same time.
Each tracking system should have its own `*tracksys-<label>_motion.tsv` file.
One column in the `*tracksys-<label>_motion.tsv` file is intended to represent one data channel.
The ordering of columns has to match the order of rows in the `*channels.tsv` file for unambiguous assignment.
All relevant metadata about a tracking systems is stored in accompanying sidecar `*tracksys-<label>_motion.json` file.
The source data from each tracking system in their original format, if different from `.tsv`,
can be stored in the [`/sourcedata` directory](../common-principles.md#source-vs-raw-vs-derived-data).
The original data format MAY hold more metadata than currently specified in the `*_motion.json` file.

When multiple tracking systems are used to record motion or motion capture is used alongside the recording of other BIDS modalities, it is possible to temporally synchronise the recordings.
A guideline to time synchronization between multiple modalities using recording onset and event time offset is described later in the specifications.
To store the differences between recording onsets, `scans.tsv` files can be used.

To store events which relate to a tracking system, it is recommended to use designated events files per tracking system.
Such an events file name would include the tracksys key and look like `sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_events.tsv`.
The onsets in the event file can be related to the starting time of the tracking system in the `scans.tsv` file.

### Sidecar JSON (`*_motion.json`)

#### Task information

{{ MACROS___make_sidecar_table("motion.motionHardware") }}

#### Hardware information

{{ MACROS___make_sidecar_table("motion.motionHardware") }}

#### Insitution information

{{ MACROS___make_sidecar_table("motion.motionInstitutionInformation") }}

#### Motion specific fiels

Motion specific fields MUST be present:

{{ MACROS___make_sidecar_table("motion.motionRequired") }}

Motion specific fields SHOULD be present:

{{ MACROS___make_sidecar_table("motion.motionMoreRecommended") }}

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

In this example, the `*_motion.json` contains data from one tracking system consisting of two [inertial measurement units (imu)](https://en.wikipedia.org/wiki/Motion_capture#Inertial_systems).
If there are additional, for example optical [motion capture (omc)](https://en.wikipedia.org/wiki/Motion_capture#Optical_systems), tracking systems,
data from each tracking system would be stored in different files (`*_tracksys-<label>_motion.tsv`, `*_tracksys-<label>_motion.json`, `*_tracksys-<label>_channels.tsv`.
All specified tracking systems can share `tracked_point` defined in `*_channels.tsv`, when tracking devices are placed on the same location.

Note that the onsets of the recordings SHOULD be stored in the study key file [(`scans.tsv`)](../modality-agnostic-files.md#scans-file).
Here, date-time information MUST be expressed as indicated in [Units](../common-principles.md#units).
The [`scans.tsv`](../modality-agnostic-files.md#scans-file) file contains the filename and the acquisition time of a recording, which can be used to synchronize multiple recordings.
However, synchronization information between the two systems can also be stored using channel `latency` in the `*_motion.tsv` if available.

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

This file is REQUIRED as it makes it easy to browse or query over larger collections of datasets. The REQUIRED columns are channel `component`, `name`, `tracked_point`, `type` and `unit`.
Any number of additional columns may be added to provide additional information about the channels.
The `*tracksys-<label>_channels.tsv` file should give additional information about individual recorded channel, some of which my not be found summarized in `*motion.json`.

The columns of the channels description table stored in `*_channels.tsv` are:

{{ MACROS___make_columns_table("motion.motionChannels") }}

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
name        tracked_point   type  component units
t1_acc_x    LeftFoot        ACCEL x         m/s^2
t1_acc_y    LeftFoot        ACCEL y         m/s^2
t1_acc_z    LeftFoot        ACCEL z         m/s^2
t1_gyro_x   LeftFoot        GYRO  x         rad/s
t1_gyro_y   LeftFoot        GYRO  y         rad/s
t1_gyro_z   LeftFoot        GYRO  z         rad/s
…
t2_acc_x    RightWrist      ACCEL x         m/s^2
t2_acc_y    RightWrist      ACCEL y         m/s^2
t2_acc_z    RightWrist      ACCEL z         m/s^2
t2_gyro_x   RightWrist      GYRO  x         rad/s
t2_gyro_y   RightWrist      GYRO  y         rad/s
t2_gyro_z   RightWrist      GYRO  z         rad/s
```
