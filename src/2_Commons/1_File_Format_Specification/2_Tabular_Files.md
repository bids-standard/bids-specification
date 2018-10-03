Tabular files
-------------

Tabular data MUST be saved as tab delimited values (`.tsv`) files, i.e. csv files where commas are replaced by tabs. Tabs MUST  be true tab characters and MUST NOT be a series of space characters. Each TSV file MUST start with a header line listing the names of all columns (with the exception of physiological and other continuous acquisition data - see below for details). Names MUST be separated with tabs. String values containing tabs MUST be escaped using double quotes. Missing and non-applicable values MUST be coded as `n/a`.

### 1 Example:
```
onset duration  response_time correct stop_trial  go_trial
200 200 0 n/a n/a n/a
```

Tabular files MAY be optionally accompanied by a simple data dictionary in a JSON format (see below). The data dictionaries MUST have the same name as their corresponding tabular files but with `.json` extensions. Each entry in the data dictionary has a name corresponding to a column name and the following fields:

| Field name  | Definition                                                     |
|:------------|:---------------------------------------------------------------|
| LongName    | Long (unabbreviated) name of the column.                       |
| Description | Description of the column.                                     |
| Levels      | For  categorical variables: a dictionary of possible values (keys) and their descriptions (values). |
| Units       | Measurement units.  `[<prefix symbol>] <unit symbol>` format following the SI standard is RECOMMENDED (see Appendix V). |
| TermURL     | URL pointing to a formal definition of this type of data in an ontology available on the web. |

### 2 Example:

```JSON
{
  "test": {
    "LongName": "Education level",
    "Description": "Education level, self-rated by participant",
    "Levels": {
      "1": "Finished primary school",
      "2": "Finished secondary school",
      "3": "Student at university",
      "4": "Has degree from university"
    }
  },
  "bmi": {
    "LongName": "Body mass index",
    "Units": "kilograms per squared meters",
    "TermURL": "http://purl.bioontology.org/ontology/SNOMEDCT/60621009"
  }
}
```
