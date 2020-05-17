> :warning: This `temporary` appendix is intended to provide a conversion guideline between
different versions of BEP001. 

## Changes to `acq` entity

### Previous convention

In the previous version, the `acq` entity was used to define custom `tags` that 
specify different combinations of multiple entities:

| Grouping suffix | Labels           | Respective metadata fields and values   |
|-------------|------------------|------------------------------|
| MTR         | `MTon`, `MToff`      | MTState [`On`, `Off`] |
| MTS         | `MTon`, `MToff`, `T1w` | MTstate [`On`,`Off`,`Off`], FlipAngle [`lower`,`lower`,`higher`] |
| MPM         | `MTon`, `MToff`, `T1w` | MTstate [`On`,`Off`,`Off`], FlipAngle [`lower`,`lower`,`higher`] |

The table above uses `acq` entity to this end for `MTS` and `MTR` by combining 
two entities (`fa` and non-existing `mt`). 

### New convention

As the previous convention imposed a specific role to a free-from entity, the 
solution was not ideal and did not receive positive feedback.

To free `acq` tag, we introduced a new entity `mt`, for the suffixes described in BEP001 so far. This limitation applied to `MTR`, `MTS` and `MPM` suffixes. 

These entities will appear in the filenames in the following (alphabetical) order: 

`echo` --> `fa` --> `inv` --> `mt` 

#### Changes for MTR

```diff
--- MTState on
- sub-01_acq-MTon_MTR.nii.gz
+ sub-01_mt-on_MTR.nii.gz


--- MTState off
- sub-01_acq-MToff_MTR.nii.gz
+ sub-01_mt-off_MTR.nii.gz
```

#### Changes for MTS

```diff

--- MTState on | FlipAngle lower
------ a.k.a MTw
- sub-01_acq-MTon_MTS.nii.gz
+ sub-01_fa-1_mt-on_MTS.nii.gz


--- MTState off | FlipAngle lower
------ a.k.a PDw
- sub-01_acq-MToff_MTS.nii.gz
+ sub-01_fa-1_mt-off_MTS.nii.gz


--- MTState off | FlipAngle higher
------ a.k.a T1w
- sub-01_acq-T1w_MTS.nii.gz
+ sub-01_fa-2_mt-off_MTS.nii.gz
```

> :warning: **fa-2 > fa-1**

#### Changes for MPM
```diff

--- MTState on | FlipAngle lower | Echo 1
------ a.k.a MTw
- sub-01_echo-1_acq-MTon_MPM.nii.gz
+ sub-01_echo-1_fa-1_mt-on_MPM.nii.gz


--- MTState off | FlipAngle lower | Echo 1
------ a.k.a PDw
- sub-01_echo-1_acq-MToff_MPM.nii.gz
+ sub-01_echo-1_fa-1_mt-off_MPM.nii.gz


--- MTState off | FlipAngle higher | Echo 1
------ a.k.a T1w
- sub-01_echo-1_acq-T1w_MPM.nii.gz
+ sub-01_echo-1_fa-2_mt-off_MPM.nii.gz
```

> :warning: **fa-2 > fa-1**

### Other considerations

#### 1) `RepetitionTime` --> `RepetitionTimeExcitation`

Please use `RepetitionTimeExcitation` for `TR` in anatomical imaging data json files. 

For anatomical acquisitions with multiple readout blocks within a `TR` (e.g. `MP2RAGE`), `RepetitionTimeExcitation` is used along with `RepetitionTimePreparation`.  

#### 2) Ordering of the `metadata` values with respect to the `index` 

##### Ascending order indexing 
|entity| respective `EchoTime` value in JSON|
|-------------|------------------|
|echo-1|          0.005        | 
|echo-2|          0.010        | 
|echo-3|          0.015        | 
etc. 

|entity| respective `FlipAngle` value in JSON|
|-------------|------------------|
|fa-1|          5        |
|fa-2|          25       |
etc.

> :warning: Indexes MUST correspond to the same value throughout the dataset. For example, `fa-2` MUST NOT point to `FlipAngle = 5` for `echo-1` and to something else (e.g. `FlipAngle = 25`) for `echo-2`.

#### 3) `index` numeric format 

Use format `%03d` (`001`,`002`,etc) instead of `%d` (`1`,`2`,etc.) for better listing. 
