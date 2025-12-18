## Raw Physiological Data

### 1. File formats and directory structure

#### 1.1 General principles

The file and dataset naming conventions for physiological data follow the common principles of BIDS. When present, physiological recordings **SHOULD** be stored as compressed tabular files (`.tsv.gz` format) along with corresponding JSON files for storing metadata fields (see below).

An example of the physio directory structure is shown below:

{{ MACROS___make_filename_template(
       "raw",
       placeholders=True,
       show_entities=["recording"],
       suffixes=["physio"]
   )
}}

```
{{ MACROS___make_filetree_example(
{
"dataset":{
   "sub-<label>": {
      "ses-<label>": {
         "physio": {
            "sub-<label>[_ses-<label>]_task-<label>_[recording-<label>]_physio.json": "",
            "sub-<label>[_ses-<label>]_task-<label>_[recording-<label>]_physio.tsv.gz": "",
            },
         },
      }
   }
}
) }}

{{ MACROS___make_filetree_example(
{
"dataset":{
   "sub-<label>": {
      "ses-<label>": {
         "func": {
            "<matches>_[recording-<label>]_physio.json": "",
            "<matches>_[recording-<label>]_physio.tsv.gz": "",
            },
         },
      }
   }
}
) }}

```

When recording physiological data, we **RECOMMEND** to always record and save the data with the least amount of processing possible applied to it following this specification. If derivatives are computed in real time, we **RECOMMEND** to save them following the derivatives BEP, and to also store raw data following this concBEP.

#### 1.2 Splitting concurrently acquired data into multiple files

Recorded physio data **MUST** be split into separate data files in case of difference in top-level metadata like `SamplingFrequency`, `Software`, and `Manufacturer` of the main recording device (i.e., data source). These top-level metadata are discussed in the following section.

Data with common top-level metadata **MAY** be kept aggregated in one file otherwise, or split based on channel type, if preferred. The sole exception is eye tracking data, that **MUST** be split in its own file, following BEP020 specifications.

We generally recommend keeping different files from different recording devices separate, but the option to keep data together acknowledges not only current standards in data collection, but also the fact that often physiological data is inspected and analysed together to get a clearer picture of what the fluctuations describe (e.g., looking at ventilation and respiration together, or PPG and ECG for motion artifacts).

Moreover, the set of metadata we are proposing managed to consider most, if not all, possible channel types - with the exception of eye tracking. Thus, the choice to aggregate physiological data with common key metadata in a single file is left to user preference.

We **RECOMMEND** to store trigger signals recorded alongside physiological channels in the same file when concurrent modalities are collected (e.g. functional MRI or EEG).

**For example:**

**Splitting recorded data into separate physio data files**

{{ MACROS___make_filetree_example(
   {
   "sub-001": {
      "ses-01": {
         "physio": {
            "sub-001_ses-01_recording-scr_physio.json": "",
            "sub-001_ses-01_recording-scr_physio.tsv.gz": "",
            "sub-001_ses-01_recording-ecg_physio.json": "",
            "sub-001_ses-01_recording-ecg_physio.tsv.gz": "",
            "sub-001_ses-01_recording-resp_physio.json": "",
            "sub-001_ses-01_recording-resp_physio.tsv.gz": ""
            },
         },
      }
   }
) }}
```
dataset/
[...]
sub-<label>/[ses-<label>/]
physio/
sub-001_ses-01_recording-scr_physio.json
sub-001_ses-01_recording-scr_physio.tsv.gz
sub-001_ses-01_recording-ecg_physio.json
sub-001_ses-01_recording-ecg_physio.tsv.gz
sub-001_ses-01_recording-resp_physio.json
sub-001_ses-01_recording-resp_physio.tsv.gz
```

**Combining recorded data into one pair of physio data files**

{{ MACROS___make_filetree_example(
   {
   "sub-001": {
      "ses-01": {
         "physio": {
            "sub-001_ses-01_physio.json": "",
            "sub-001_ses-01_physio.tsv.gz": ""
            },
         },
      }
   }
) }}
```
{{ MACROS___make_filetree_example(
{
"dataset":{
   "sub-<label>": {
      "ses-<label>": {
         "physio": {
            "sub-001_ses-01_physio.json": "",
            "sub-001_ses-01_physio.tsv.gz": "",
            },
         },
      }
   }
}
) }}

```

It is possible that the `recording-<label>` entity uses terms that could be confused with metadata field values, such as `MeasurementType` or `SamplingFrequency`. In that case, the lowest metadata level available should always be interpreted as the most reliable information. For instance, if the file name contains `recording-1000hz` but the `SamplingFrequency` metadata indicates a sampling frequency of 100Hz, data **MUST** be interpreted as being sampled at 100 Hz. Similarly, if the entity `recording-ecg` is used, but the `MeasurementType` metadata of the contained columns indicate “ppg” and “Ventilation”, the data **MUST** be interpreted as PPG and Ventilation, and not ECG.

---

### 2. JSON Data files

Metadata sidecar files (`<matches>_physio.json`) **SHOULD** define the field `PhysioType`. This field indicates a specific type of formatting, rather than a physiological modality. The `PhysioType` `"generic"` value, being the default, **MUST** be assumed if the `PhysioType` metadata is not defined.

All metadata we are proposing are either **OPTIONAL** or **RECOMMENDED**, and they are meant to enrich the current `"generic"` `PhysioType`. However, we are also suggesting the introduction of a `"specified"` `PhysioType`, that will differ from `"generic"` because one proposed metadata, `MeasureType`, will be **REQUIRED** rather than **RECOMMENDED**. Equally, the `Units` metadata will be **REQUIRED** instead of **RECOMMENDED** in this case.

Compared to the current BIDS specification (1.10.0), at the file level we are adding one metadata, the **OPTIONAL** `SubjectPosition`, indicating the position of the subject during the data collection (see section 2.1).

When specifying column names, columns **MUST** have unique names. All such data columns **MUST** be appropriately defined in the JSON metadata.

**Example:**

```json
{
  "Columns": ["screda1", "screda2", "ecg", "ppg"],
  "SamplingFrequency": 1000,
  "SubjectPosition": "sitting",
  "PhysioType": "specified",
  ...
  "screda1": {
    "MeasureType": "EDA-phasic",
    "Units": "mS",
    "Placement": "Thenar",
    ...
  },
  "screda2": {
    "MeasureType": "EDA-tonic",
    "Units": "mS",
    "Placement": "Hypothenar",
    ...
  },
  "ecg": {
    "MeasureType": "ECG",
    "Units": "mV",
    "Placement": "II",
    ...
  },
  "ppg": {
    "MeasureType": "PPG",
    "Units": "au",
    "Placement": "Right earlobe",
    ...
  },
  ...
}
```

As described in the following table (Section 2.2), this BEP is adding a few metadata to describe columns.

- The most important one is `MeasureType`, a **RECOMMENDED** metadata that indicates the actual nature of the data in the column. 
    - This metadata value is a string that **MUST** come from a set of keywords (see table 2.2).
    - This set of keywords can be expanded in the future to include more physiological modalities. 
    - When the file-level metadata `PhysioType` is `"specified"`, `MeasureType` becomes a **REQUIRED** field for each column.

This metadata is meant to be the most reliable indicator of the type of data contained in the described column. Having a reliable and standardized indication of what type of data is being handled allows automated modality specific data processing and prevents data misuse.

Furthermore, we are proposing that `Units` becomes a **REQUIRED** metadata when `PhysioType` is `"Specified"`. Not only this helps to better reflect the possible quantitative nature of physiological data, but since similarly labelled data (e.g. Ventilation) can be expressed in different units, indicating different underlying processes, sensors, or levels of real-time preprocessing and data manipulation (e.g. transformation from Volts to millimeters of Mercury), making this field more explicit in the section regarding physiological data will help improve data interpretation. Specification of units **SHOULD** follow the International System of Units (see BIDS specification).

We are also introducing a `Placement` **RECOMMENDED** metadata, that describes the position of the sensor during data collection. For instance, a file could have three columns of ventilation data, one collected at the navel, one at the diaphragm, and one at the armpit level, in which case `Placement` values would be “Navel”, “Diaphragm”, and “Armpit” respectively. In case the data describes gas concentration, such as CO2 or O2, `Placement` **SHOULD** be used to indicate if a “Nose” cannula versus a “Mouth” mouthpiece or a “Mask” was used.

The three metadata at this level describing hardware are:

- `ChannelManufacturersModelName` (**RECOMMENDED**)
- `ChannelManufacturers` (**RECOMMENDED**)
- `ChannelDeviceSerialNumber` (**OPTIONAL**)

These metadata are meant to describe the nature of the equipment used to record data. Different components from different manufacturers could be used at the same time in a “patchwork” approach in which a sensor or amplifier from manufacturer A is connected to the recording device of manufacturer B, and even the same manufacturer could provide two or more options to measure the same type of data. Many setups that differ in this way introduce a potential difference in data processing (e.g. digital vs analogical lags, delays and sharpness of the recording, quantification, …).

Thus, we **RECOMMEND** to increase the granularity of the setup description for each column, and we **RECOMMEND** to report names and manufacturers (when different from the main unit) of sensors, connective elements (e.g. cannulae or cables), and amplifiers. Serial numbers **MAY** be reported as well.

In this framework, it is crucial to distinguish between the different fields available for specifying recording equipment in the meta-data: at the top-level, the main recording device and software are characterized in meta-data fields such as `SoftwareModels` and `DeviceSerialNumber`, while at the column-level, information about channel-specific hardware is characterized in meta-data fields such as `ChannelDeviceSerialNumber`.

We provide the example shown above to assist in determining the main recording device in common physiological acquisition set-ups. In the example shown above, three different recording systems are being used to concurrently acquire physiological data. The first system acquires two channels of physiological data with software A and main recording device ‘a’, which both would be specified using the top-level fields in the accompanying meta-data. Upstream, hardware such as amplifiers, filters, cables, and sensors would be specified using column-level fields specific to each channel in the accompanying meta-data. In the second system, one channel of physiological data is being acquired by main recording device ‘b’ and wirelessly transmitted to software B. In this case, the sensor attached to device ‘b’ can still be specified using column-level meta-data fields if it is an independent product. In the third system, data is acquired by a physiological monitoring unit which is integrated with an MRI scanner (device ‘c’), which itself acts as the main recording device. In case of using networked middleware systems such as the lab streaming layer, where the data may be centrally recorded, the central recording computer itself **MAY** be considered the main recording device.

Finally, the `AmplifierSettings` is a dictionary meant to be filled with potential amplifier settings that can manipulate the data collection at the source, e.g. low-pass filters or DC/AC currents. Because each amplifier and each manufacturer have different settings, we cannot define further the content of this dictionary, but we suggest using manufacturer specific pairs of keys and values. In this dictionary, we also **SUGGEST** reporting eventual data transformations (e.g. the exact formula used to transform gas pressure from measured Voltage to millimetres of Mercury).

More information about the metadata entities contained in the JSON files can be found in the tables below.

---

### 2.1 Metadata fields used in top level metadata 

{{ MACROS___make_sidecar_table(["continuous.Continuous"]) }}

### 2.2 Metadata fields for column description

---
