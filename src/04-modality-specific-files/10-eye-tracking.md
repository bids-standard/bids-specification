
{{ MACROS___make_filename_template(datatypes=["eyetrack"], suffixes=["eyetrack", "events"]) }}


{{ MACROS___make_metadata_table(
   {
      "TaskName": ("REQUIRED", "A RECOMMENDED convention is to name resting state task using labels beginning with rest."),
   }
) }}



{{ MACROS___make_metadata_table(
   {
      "InstitutionName": "RECOMMENDED",
      "InstitutionAddress": "RECOMMENDED",
      "Manufacturer_eyetrack": "RECOMMENDED",
      "ManufacturersModelName_eyetrack": "RECOMMENDED",
      "SoftwareVersion_eyetrack": "RECOMMENDED",
      "TaskDescription": "RECOMMENDED",
      "Instructions": ("RECOMMENDED", "If no instruction is given, write `none`."),
      "CogAtlasID_eyetrack": "RECOMMENDED",
      "CogPOID_eyetrack": "RECOMMENDED",
      "DeviceSerialNumber": "RECOMMENDED",
   }
) }}


{{ MACROS___make_metadata_table(
   {
      "SamplingFrequency_eyetrack": "REQUIRED",
      "SampleCoordinateUnit": "REQUIRED",
      "SampleCoordinateSystem": "REQUIRED",
      "EnvironmentCoordinates": "REQUIRED",
      "EventIdentifier": "REQUIRED",
      "ScreenSize": "REQUIRED",
      "ScreenResolution": "REQUIRED",
      "ScreenDistance": "REQUIRED",
   }
) }}


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
