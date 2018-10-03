Definitions
-----------

The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT",
"SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in
[[RFC2119](https://www.ietf.org/rfc/rfc2119.txt)].

Throughout this protocol we use a list of terms. To avoid misunderstanding we clarify them here.

1.  Dataset - a set of neuroimaging and behavioural data acquired for a purpose of a particular study. A dataset consists of data acquired from one or more subjects, possibly from multiple sessions.
2.  Subject - a person or animal participating in the study.
3.  Session - a logical grouping of neuroimaging and behavioural data consistent across subjects. Session can (but doesn't have to) be synonymous to a visit in a longitudinal study. In general, subjects will stay in the scanner during one session. However, for example, if a subject has to leave the scanner room and then be re-positioned on the scanner bed, the set of MRI acquisitions will still be considered as a session and match sessions acquired in other subjects. Similarly, in situations where different data types are obtained over several visits (for example fMRI on one day followed by DWI the day after) those can be grouped in one session. Defining multiple sessions is appropriate when several identical or similar data acquisitions are planned and performed on all -or most- subjects, often in the case of some intervention between sessions (e.g., training).
4.  Data acquisition - a continuous uninterrupted block of time during which a brain scanning instrument was acquiring data according to particular scanning sequence/protocol.
5.  Data type - a functional group of different types of  data. In BIDS we define five data types: func (task based and resting state functional MRI), dwi (diffusion weighted imaging), fmap (field inhomogeneity mapping data such as field maps), anat (structural imaging such as T1, T2, etc.), meg (magnetoencephalography).
6.  Task - a set of structured activities performed by the participant. Tasks are usually accompanied by stimuli and responses, and can greatly vary in complexity. For the purpose of this protocol we consider the so-called “resting state” a task. In the context of brain scanning, a task is always tied to one data acquisition. Therefore, even if during one acquisition the subject performed multiple conceptually different behaviours (with different sets of instructions) they will be considered one (combined) task.
7.  Event - a stimulus or subject response recorded during a task. Each event has an onset time and duration. Note that not all tasks will have recorded events (e.g., resting state).
8.  Run - an uninterrupted repetition of data acquisition that has the same acquisition parameters and task (however events can change from run to run due to different subject response or randomized nature of the stimuli). Run is a synonym of a data acquisition.
