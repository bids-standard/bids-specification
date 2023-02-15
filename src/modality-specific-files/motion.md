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

The extension is not limited to motion data in physical space but also encompasses simulated movement in virtual space.
Other dynamic objects than human body parts whose motion is tracked may as well be included as tracked objects.
This specification does not include raw camera footages (from camera-based or optical motion capture recordings), but includes the positions or orientations computed computed using such data.
In this specification, positions (and their time derivatives) are represented as Cartesian coordinates along up to three spatial axes,
and orientations (and their time derivatives) are represented as Euler angles.
However, to cover recordings from computer graphics applications (for example, virtual 3D motion or immersive virtual reality recording in physical space),
orientations are may optionally be represented as quaternions.
In this case, the quaternion channels can be distinguished from channels containing Euler angles based on the entries in columns `component` and `units` in the `*_channels.tsv` file.
See subsection on `Channels description` for further details.

Motion data from one tracking system MUST be stored in a single `*_motion.tsv` file.
A tracking system is defined as a group of motion channels that share hardware properties (the recording device) and software properties (the recording duration and number of samples).
For example, if the position time series of multiple optical markers is processed via one recording unit, this can be defined as a single tracking system.
Note that it is not uncommon to have multiple tracking systems to record at the same time.
Each tracking system has its own `*tracksys-<label>_motion.tsv` file.
One column in the `*tracksys-<label>_motion.tsv` file represents one data channel.
The ordering of columns MUST match the order of rows in the `*channels.tsv` file for unambiguous assignment.
All relevant metadata about a tracking systems is stored in accompanying sidecar `*tracksys-<label>_motion.json` file.
The source data from each tracking system in their original format, if different from `.tsv`,
can be stored in the [`/sourcedata` directory](../common-principles.md#source-vs-raw-vs-derived-data).
The original data format MAY hold more metadata than currently specified in the `*_motion.json` file.

When multiple tracking systems are used to record motion or motion capture is used alongside the recording of other BIDS modalities, it may be necessary to temporally synchronize the recordings. To save the differences between recording onsets, column [`acq_time`](https://bids-specification.readthedocs.io/en/stable/glossary.html#objects.columns.acq_time__scans) of the [`scans.tsv`](https://bids-specification.readthedocs.io/en/stable/03-modality-agnostic-files.html#scans-file) file can be used.


To store events alongside motion data when there are multiple tracking systems simultaneously in use, it is recommended to assign a tracking system to the events file. 
Such an events file name would include the `tracksys` key and look like `sub-<label>[_ses-<label>]_task-<label>[_acq-<label>][_run-<index>]_tracksys-<label>_events.tsv`. Event latencies can then be related to motion samples of multiple tracking systems also by using `acq_time` column entries in the `scans.tsv`. The same principle applies when the events file is saved alongside a simultaneously recorded non-motion data (for example EEG).

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

{{ MACROS___make_sidecar_table("motion.motionRecommended") }}

Restricted keyword list for field `RotationRule`:

| **Keyword** | **Description**                                                                                                                                        |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------                           |
| left-hand   | Rotation is following the left-hand convention, such that the left thumb points to the positive end of the spatial axis, and the fingers curl along the orientation rotation.     |
| right-hand  | Rotation is following the right-hand convention, such that the right thumb points to the positive end of the spatial axis, and the fingers curl along the orientation rotation. |

Restricted keyword list for field `RotationOrder`:

| **Keyword** | **Description**                                                                         |
| ----------- | --------------------------------------------------------------------------------------- |
| XYZ         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |
| XZY         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |
| YXZ         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |
| YZX         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |
| ZXY         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |
| ZYX         | Sequence in which elemental rotations are applied to define an orientation in 3D space. |

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

| **Keyword** | **Description**                                                                                                                                             |
| ----------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| x           | Position along the X-axis, or rotation about the X-axis among the Euler angles that represent the orientation, or magnetic field strength along the X-axis. |
| y           | Position along the Y-axis or rotation about the Y-axis among the Euler angles that represent the orientation, or magnetic field strength along the Y-axis.  |
| z           | Position along the Z-axis or rotation about the Z-axis among the Euler angles that represent the orientation, or magnetic field strength along the Z-axis.  |
| quat_x      | Quaternion component associated with the X-axis.                                                                                                            |
| quat_y      | Quaternion component associated with the Y-axis.                                                                                                            |
| quat_z      | Quaternion component associated with the Z-axis.                                                                                                            |
| quat_w      | Non-axial quaternion component.                                                                                                                             |
| n/a         | Channels that have no corresponding spatial axis.                                                                                                           |

Restricted keyword list for column `type` in alphabetic order (shared with the other BIDS modalities?). Note that upper-case is REQUIRED:

| **Keyword** | **Description**                                                                                                                                                                                                              |
| ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ACCEL       | Accelerometer channel, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y, or z).                                                                           |
| ANGACC      | Angular acceleration channel, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y, or z).                                                                    | 
| GYRO        | Gyrometer channel, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y, or z).                                                                               |
| LATENCY     | Latency of samples in seconds from recording onset.                                                                                                                                                                          |
| MAGN        | Magnetic field strength, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z)                                                                           |
| MISC        | Miscellaneous channels.                                                                                                                                                                                                      |
| ORNT        | Orientation channel, one channel for each spatial axis or quaternion component. Column `component` for the axis or quaternion label MUST be added to the `*_channels.tsv` file (x, y, z, quat_x, quat_y, quat_z, or quat_w). |
| POS         | Position in space, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z).                                                                                |
| VEL         | Velocity, one channel for each spatial axis. Column `component` for the axis MUST be added to the `*_channels.tsv` file (x, y or z).                                                                                         |

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
