# Motion

For information on how to cite this extension when referencing it in the context of the academic literature, please read [Citing BIDS](../introduction.md#citing-bids).

Motion datasets formatted using this specification are available on the
[BIDS examples repository](https://github.com/bids-standard/bids-examples#motion-datasets)
and can be used as helpful guidance when curating new datasets.

## Motion recording data

{{ MACROS___make_filename_template(
"raw",
datatypes=["motion"],
suffixes=["motion", "channels", "events"])
}}

A wide variety of motion capture systems are used in human research, resulting in different proprietary data formats.

This BIDS extension deals with common outputs from motion capture systems such as positions, orientations, or their time derivatives.

The extension is not limited to motion data in physical space but also encompasses simulated movement in virtual space, as far as these are comparable to movements in physical space.
Other dynamic objects than human body parts whose motion is tracked may as well be included as tracked objects.
This specification does not include raw camera footages (from camera-based or optical motion capture recordings), but includes the positions or orientations computed using such data.

In this specification, positions (and their time derivatives) are represented as Cartesian coordinates along up to three spatial axes,
and orientations (and their time derivatives) are represented as Euler angles.
However, to cover recordings from computer graphics applications (for example, virtual 3D motion or immersive virtual reality recording in physical space),
orientations are also allowed to be represented as [quaternions](https://en.wikipedia.org/wiki/Quaternion).

In this case, the quaternion channels can be distinguished from channels containing Euler angles based on the entries in columns `component` and `units` in the `*_channels.tsv` file.
See subsection on `Channels description` for further details.

Motion data from one tracking system MUST be stored in a single `*_motion.tsv` file.
A tracking system is defined as a group of motion channels that share hardware properties (the recording device) and software properties (the recording duration and number of samples).
For example, if the position time series of multiple optical markers is processed via one recording unit, this MAY be defined as a single tracking system.
Note that it is not uncommon to have multiple tracking systems to record at the same time.

Each tracking system MUST have its own `*_tracksys-<label>_motion.tsv` file, where `<label>` is a user-defined keyword to be used to identify each file belonging to a tracking system.
This is especially helpful when more than one tracking system is used.
Data from different tracking systems MUST be stored in different `*_tracksys-<label>_motion.tsv` files,
each of which is accompanied by `*_tracksys-<label>_motion.json` and `*_tracksys-<label>_channels.tsv` files.
Between `tracksys-<label>` entity and `*_motion.tsv`, `*_motion.json`, or `*_channels.tsv` suffixes, optional [`acq-<label>`](../appendices/entities.md#acq) or [`run-<index>`](../appendices/entities.md#run) entity MAY be inserted.

One column in the `*_tracksys-<label>_motion.tsv` file represents one data channel.
The ordering of columns MUST match the order of rows in the `*_channels.tsv` file for unambiguous assignment.
All relevant metadata about a tracking systems is stored in accompanying sidecar `*_tracksys-<label>_motion.json` file.

The source data from each tracking system in their original format, if different from `.tsv`,
can be stored in the [`/sourcedata` directory](../common-principles.md#source-vs-raw-vs-derived-data).
The original data format MAY hold more metadata than currently specified in the `*_motion.json` file.

When multiple tracking systems are used to record motion or motion capture is used alongside the recording of other BIDS modalities and recordings should be interpreted together,
it is advised to provide a possibility to synchronize recordings.
The preferred way to do so is to use the acquisition time of the first data point of recordings and
to store this information in the `acq_time` column of the [`*_scans.tsv`](../modality-agnostic-files.md#scans-file) file.
The Note that the [BIDS date time format](../common-principles.md#units) allows optional fractional seconds, which SHOULD be used to maximize the precision of the synchronization.
Only if the precision of the synchronization is not high enough, the `*_events.tsv` file SHOULD be used to synchronize recordings.
In this file, the start- and stop time of the recording of a system are specified in relation to a system to synchronize with.
If more than two systems are to be synchronized, it is up to the user to indntify the "main" system.

In case a tracking system provides time information with every recorded sample,
these time information MAY be stored in form of latencies to recording onset (first sample) in the `*_motion.tsv` file.
If a system has uneven sampling rate behavior, the `LATENCY` channel can be used to share these information.

To store events alongside motion data when there are multiple tracking systems simultaneously in use, it is RECOMMENDED to designate a tracking system to the events file.
Such an events file name SHOULD include the `tracksys` key and looks like `sub-<label>[_ses-<label>]_task-<label>[_acq-<label>]_tracksys-<label>[_run-<index>]_events.tsv`.
Event latencies can then be related to motion samples of multiple tracking systems also by using `acq_time` column entries in the `*_scans.tsv`.
The same principle applies when the events file is saved alongside a simultaneously recorded non-motion data (for example EEG).

### Sidecar JSON (`*_motion.json`)

#### Task information

{{ MACROS___make_sidecar_table("motion.motionTaskInformation") }}

#### Hardware information

{{ MACROS___make_sidecar_table("motion.motionHardware") }}

#### Institution information

{{ MACROS___make_sidecar_table("motion.motionInstitutionInformation") }}

#### Motion specific fields

Motion specific fields MUST be present:

{{ MACROS___make_sidecar_table("motion.motionRequired") }}

Motion specific fields SHOULD be present:

{{ MACROS___make_sidecar_table("motion.motionRecommended") }}

#### Example `*_tracksys-<label>_motion.json`

```JSON
{
 "SamplingFrequency": 60,
 "SamplingFrequencyEffective": 60.00197437,
 "TaskName": "BIDS Motion fictive example",
 "TrackingSystemName": "IMU Right Hand",
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
 "GYROChannelCount": 6,
 "MAGNChannelCount": 6,
 "Manufacturer": "BWSensing",
 "ManufacturersModelName": "BW-IMU600",
}
```

In this example, the `*_motion.json` contains data from one tracking system consisting of two
[inertial measurement units (imu)](https://en.wikipedia.org/wiki/Motion_capture#Inertial_systems).
If there are additional tracking systems (for example [optical motion capture](https://en.wikipedia.org/wiki/Motion_capture#Optical_systems)),
data from these MUST be stored as separate files like `*_tracksys-omcA_motion.tsv` and `*_tracksys-omcB_motion.tsv`.
All specified tracking systems MAY share `tracked_point` defined in `*_channels.tsv`, when tracking devices are placed on the same object or body part.

Note that the onsets of the recordings SHOULD be stored in the study key file [(`scans.tsv`)](../modality-agnostic-files.md#scans-file).
Here, date-time information MUST be expressed as indicated in [Units](../common-principles.md#units).
The [`scans.tsv`](../modality-agnostic-files.md#scans-file) file contains the filename and the acquisition time of a recording,
which MAY be used to synchronize multiple recordings.

## Channels description (`*_channels.tsv`)

{{ MACROS___make_filename_template(
"raw",
datatypes=["motion"],
suffixes=["channels"])
}}

This file is REQUIRED as it makes it easy to browse or query over larger collections of datasets.
The REQUIRED columns are channel `name`, `component`, `type`, `tracked_point` and `units`.
Any number of additional columns MAY be added to provide additional information about the channels.
The `*_tracksys-<label>_channels.tsv` file SHOULD give additional information about individual recorded channel,
some of which my not be found summarized in `*_motion.json`.

The columns of the channels description table stored in `*_channels.tsv` are:

{{ MACROS___make_columns_table("motion.motionChannels") }}

### Restricted keyword list for channel component

Restricted keyword list for column `component`.
When using quaternions to represent orientations,
the axial components that corresponds to the three spatial axes MUST be specified as "quat_x", "quat_y", "quat_z", and the non-axial component as "quat_w".

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

### Restricted keyword list for channel type

Restricted keyword list for column `type` in alphabetic order.
Note that upper-case is REQUIRED:

| **Keyword** | **Description**                                                                                                                                                                                                              |
|-------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| ACCEL   | Accelerometer channel, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y, or z).                                                                           |
| ANGACC  | Angular acceleration channel, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y, or z).                                                                    |
| ANGVEL  | Angular velocity channel, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y, or z).                                                                        |
| GYRO    | Gyrometer channel, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y, or z).                                                                               |
| JNTANG  | Joint angle channel between two fixed axis belonging to two bodyparts. Angle SHOULD be defined between proximal and distal bodypart in deg.                                                                              |
| LATENCY | Latency of samples in seconds from recording onset. MUST be in form of `s[.000000]`, where `s` reflects whole seconds, and `.000000` reflects OPTIONAL fractional seconds.                                               |
| MAGN    | Magnetic field strength, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y or z).                                                                          |
| MISC    | Miscellaneous channels.                                                                                                                                                                                                  |
| ORNT    | Orientation channel, one channel for each spatial axis or quaternion component. Column component for the axis or quaternion label MUST be added to the *_channels.tsv file (x, y, z, quat_x, quat_y, quat_z, or quat_w). |
| POS     | Position in space, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y or z).                                                                                |
| VEL     | Velocity, one channel for each spatial axis. Column component for the axis MUST be added to the *_channels.tsv file (x, y or z).                                                                                         |

### Example `*_channels.tsv`

```Text
name        component   type   tracked_point   units
t1_acc_x    x           ACCEL  LeftFoot        m/s^2
t1_acc_y    y           ACCEL  LeftFoot        m/s^2
t1_acc_z    z           ACCEL  LeftFoot        m/s^2
t1_gyro_x   x           GYRO   LeftFoot        rad/s
t1_gyro_y   y           GYRO   LeftFoot        rad/s
t1_gyro_z   z           GYRO   LeftFoot        rad/s
…
t2_acc_x    x           ACCEL  RightWrist      m/s^2
t2_acc_y    y           ACCEL  RightWrist      m/s^2
t2_acc_z    z           ACCEL  RightWrist      m/s^2
t2_gyro_x   x           GYRO   RightWrist      rad/s
t2_gyro_y   y           GYRO   RightWrist      rad/s
t2_gyro_z   z           GYRO   RightWrist      rad/s
```
