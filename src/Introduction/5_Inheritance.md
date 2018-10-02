The Inheritance Principle
-------------------------

Any metadata file (`.json`, `.bvec`, `.tsv`, etc.) may be defined at any directory level, but no more than one applicable file may be defined at a given level (Example 1).  The values from the top level are inherited by all lower levels unless they are overridden by a file at the lower level. For example, `sub-*_task-rest_bold.json` may be specified at the participant level, setting TR to a specific value. If one of the runs has a different TR than the one specified in that file, another `sub-*_task-rest_bold.json` file can be placed within that specific series directory specifying the TR for that specific run.
There is no notion of "unsetting" a key/value pair. For example if there is a JSON file corresponding to particular participant/run defining a key/value and there is a JSON file on the root level of the dataset that does not define this key/value it will not be "unset" for all subjects/runs.
Files for a particular participant can exist only at participant level directory, i.e
`/dataset/sub-*[/ses-*]/sub-*_T1w.json`. Similarly, any  file that is not specific to a participant is to be declared only at top level of dataset for eg: `task-sist_bold.json` must be placed under `/dataset/task-sist_bold.json`

Example 1: Two JSON files at same level that are applicable for NIfTI
file.

```
sub-01/
    ses-test/
        sub-test_task-overtverbgeneration_bold.json
        sub-test_task-overtverbgeneration_run-2_bold.json
        anat/
            sub-01_ses-test_T1w.nii.gz
        func/
            sub-01_ses-test_task-overtverbgeneration_run-1_bold.nii.gz
            sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz
```

In the above example, two JSON files are listed under
`sub-01/ses-test/`, which are each applicable to `sub-01_ses-test_task-overtverbgeneration_run-2_bold.nii.gz`, violating the constraint that no more than one file may be defined at a given level of the directory structure. Instead `task-overtverbgeneration_run-2_bold.json` should have been under `sub-01/ses-test/func/`.

Example 2:  Multiple run and rec with same acquisition (acq) parameters acq-test1

```
sub-01/
    anat/
    func/
        sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
        sub-01_task-xyz_acq-test1_run-2_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
        sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
        sub-01_task-xyz_acq-test1_bold.json
```

For the above example, all NIfTI files are acquired with same scanning parameters (`acq-test1`). Hence a JSON file describing the acq parameters will apply to different runs and rec files. Also if the JSON file (`task-xyz_acq-test1_bold.json`) is defined at dataset top level  directory, it  will be applicable to all task runs with `test1` acquisition parameter.

Case 2:  Multiple json files at different levels for same task and acquisition parameters
```
sub-01/
   sub-01_task-xyz_acq-test1_bold.json
         anat/
         func/
             sub-01_task-xyz_acq-test1_run-1_bold.nii.gz
             sub-01_task-xyz_acq-test1_rec-recon1_bold.nii.gz
             sub-01_task-xyz_acq-test1_rec-recon2_bold.nii.gz
```

In the above example, the fields from `task-xyz_acq-test1_bold.json` file will apply to all bold runs. However, if there is a key with different value in `sub-01/func/sub-01_task-xyz_acq-test1_run-1_bold.json`,
the new value will be applicable for that particular run/task NIfTI
file/s.
