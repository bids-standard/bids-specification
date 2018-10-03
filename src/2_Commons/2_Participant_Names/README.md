Participant names and other labels
==================================

BIDS uses custom user-defined labels in several situations (naming of participants, sessions, acquisition schemes, etc.) Labels are strings and MUST only consist of letters (lower or upper case) and/or numbers. If numbers are used we RECOMMEND  zero padding (e.g., `01` instead of `1` if you have more than nine subjects) to make alphabetical sorting more intuitive. Please note that the sub- prefix is not part of the subject label, but must be included in file names (similarly to other key names).
In contrast to other labels, run and echo labels MUST be integers. Those labels MAY include zero padding, but this is NOT RECOMMENDED to maintain their uniqueness.
