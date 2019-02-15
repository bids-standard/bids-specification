# Appendix IX: Glossary

A number of terms are used throughout the specification

- **file extension**:
   a portion of the the file name after the left-most period (`.`) preceded by
   any other alphanumeric (so `.gitignore` does not have a suffix)
- **<index>**:
   a numeric value, possibly prefixed with arbitrary number of 0s for consistent
   indentation, e.g. it is `01` in `run-01` following `run-<index>` specification
- **<label>**:
   an alphanumeric value, possibly prefixed with arbitrary number of 0s for consistent
   indentation, e.g. it is `rest` in `task-rest` following `task-<label>` specification
- **participant**:
   a participant of the experiment. Used interchangeably with **subject**
- **run**:
   a separate data sequence/acquisition. Typically present to disambiguate
   otherwise identically named data files
- **session**:
   a separate scanning/experiment session. Typically present if the same 
   subjects participate in multiple sessions of the experiment 
- **subject**:
   a participant of the experiment. Used interchangeably with **participant**
- **suffix**:
   a portion of the file name with `key-value_` pairs (thus after the final `_`),
   right before the **file extension**