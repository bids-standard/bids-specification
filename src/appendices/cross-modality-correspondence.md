# Appendix XIII: Cross modality correspondence

## PET-MRI correspondence

When sharing MRI data alongside with PET data,
please pay specific attention to the format the MR images are in.
It is important to note whether the MR images have been unwarped
in order to correct for gradient non-linearities,
indicated by the `NonlinearGradientCorrection` metadata field
(see [Magnetic Resonance Imaging Data - Sequence Specifics](../04-modality-specific-files/01-magnetic-resonance-imaging-data.md#sequence-specifics)).
The reason for this is that the MRI needs to be corrected for nonlinear gradients
in order to fit the accompanying PET scans for co-registration
(Knudsen et al. 2020, [doi:10.1177/0271678X20905433](https://doi.org/10.1177/0271678X20905433);
Norgaard et al. 2019, [doi:10.1016/j.neuroimage.2019.05.055](https://doi.org/10.1016/j.neuroimage.2019.05.055)).
