# Appendix VIII: preferred names of Coordinate systems

To interpret a coordinate (x, y, z), it is required that you know relative to
which origin the coordinates are expressed, you have to know the interpretation
of the three axes, and you have to know the units in which the numbers are
expressed. This information is sometimes called the coordinate system.

These letters help describe the coordinate system definition:

A/P means anterior/posterior L/R means left/right S/I means superior/inferior

For example: `RAS` means that the first dimension (X) points towards the right
hand side of the head, the second dimension (Y) points towards the Anterior
aspect of the head, and the third dimension (Z) points towards the top of the
head.

Besides coordinate systems, defined by their origin and direction of the axes,
BIDS defines "spaces" as an artificial frame of reference, created to describe
different anatomies in a unifying manner (see e.g.
[https://doi.org/10.1016/j.neuroimage.2012.01.024](https://www.sciencedirect.com/science/article/pii/S1053811912000419?via%3Dihub)).
The "space" and all coordinates expressed in this space are by design a
transformation of the real world geometry, and nearly always different from the
individual subject space that it stems from. An example is the
Talairach-Tournoux space, which is constructed by piecewise linear scaling of an
individual's brain to that of the Talairach-Tournoux 1988 atlas. In the
Talairach-Tournoux space, the origin of the coordinate system is at the AC and
units are expressed in mm.

The coordinate systems below all relate to neuroscience and therefore to the
head or brain coordinates. Please be aware that all data acquisition starts with
"device coordinates" (scanner), which does not have to be identical to the
initial "file format coordinates" (DICOM), which are again different from the
"head" coordinates (e.g. NIFTI). Not only do device coordinate vary between
hardware manufacturers, but also the head coordinates differ, mostly due to
different conventions used in specific software packages developed by different
(commercial or academic) groups.

## MEG specific Coordinate Systems

The first two pieces of information (origin, orientation) are specified in
`XXXCoordinateSystem`, the units are specified in `XXXCoordinateSystemUnits`.

Restricted keywords for the XXXCoordinateSystem field in the
`coordinatesystem.json` file for MEG datasets:

-   CTF: ALS orientation and the origin between the ears

-   ElektaNeuromag: RAS orientation and the origin between the ears

-   4DBti: ALS orientation and the origin between the ears

-   KitYokogawa: ALS orientation and the origin between the ears

-   ChietiItab: RAS orientation and the origin between the ears

-   Other: Use this for other coordinate systems and specify further details in
  the `XXXCoordinateSystemDescription` field

Note that the short descriptions above do not capture all details, there are
detailed descriptions of these coordinate systems on the FieldTrip toolbox web
page:
[http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)

## EEG specific Coordinate Systems

The first two pieces of information (origin, orientation) are specified in
`XXXCoordinateSystem`, the units are specified in `XXXCoordinateSystemUnits`.

Restricted keywords for the `XXXCoordinateSystem` field in the
`coordsystem.json` file for EEG datasets:

-   `BESA`: Although natively this is a spherical coordinate system, the
    electrode positions should be expressed in Cartesian coordinates, with a RAS
    orientation. The X axis is the T8-T7 line, positive at T8. The Y axis is the
    Oz-Fpz line, positive at Fpz. The origin of the sphere fitted to the
    electrodes is approximately 4 cm above the point between the ears.

-   `Captrak`: RAS orientation and the origin between the ears

Note that the short descriptions above do not capture all details, There are
detailed extensive descriptions of these EEG coordinate systems on the FieldTrip
toolbox web page and on the BESA wiki:
[http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined](http://www.fieldtriptoolbox.org/faq/how_are_the_different_head_and_mri_coordinate_systems_defined)
[http://wiki.besa.de/index.php?title=Electrodes_and_Surface_Locations\#Coordinate_systems](http://wiki.besa.de/index.php?title=Electrodes_and_Surface_Locations#Coordinate_systems)

## Template based Coordinate Systems

The transformation of the real world geometry to an artificial frame of
reference is described in `XXXCoordinateSystem`. Unless otherwise specified
below, the origin is at the AC and the orientation of the axes is RAS. Unless
specified explicitly in the sidecar file in the `XXCoordinateSystemUnits` field,
the units are assumed to be mm.

| Coordinate System                                   | Description                                                                                                                                                                                                                                                                                                                                                      |
| ---------------------------------------------------   | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------   |
| MNI152Lin                                           | Also known as ICBM (version with linear coregistration) [http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152Lin](http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152Lin)                                                                                                                                                                                       |
| MNI152NLin6\[Sym&#124;Asym\]                        | Also known as ICBM 6th generation (non-linear coregistration). Used by SPM99 -   SPM8 and FSL (MNI152NLin6Sym). [http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin6](http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin6)                                                                                                                           |
| MNI152NLin2009\[a-c\]\[Sym&#124;Asym\]              | Also known as ICBM (non-linear coregistration with 40 iterations, released in 2009). It comes in either three different flavours each in symmetric or asymmetric version. [http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009](http://www.bic.mni.mcgill.ca/ServicesAtlases/ICBM152NLin2009)                                                           |
| MNIColin27                                          | Average of 27 T1 scans of a single subject [http://www.bic.mni.mcgill.ca/ServicesAtlases/Colin27Highres](http://www.bic.mni.mcgill.ca/ServicesAtlases/Colin27Highres)                                                                                                                                                                                            |
| MNI305                                              | Also known as avg305.                                                                                                                                                                                                                                                                                                                                            |
| NIHPD                                               | Pediatric templates generated from the NIHPD sample. Available for different age groups (4.5–18.5 y.o., 4.5–8.5 y.o., 7–11 y.o., 7.5–13.5 y.o., 10–14 y.o., 13–18.5 y.o. This template also comes in either -symmetric or -asymmetric flavor. [http://www.bic.mni.mcgill.ca/ServicesAtlases/NIHPD-obj1](http://www.bic.mni.mcgill.ca/ServicesAtlases/NIHPD-obj1) |
| Talairach                                           | Piecewise linear scaling of the brain is implemented as described in TT88. [http://www.talairach.org/](http://www.talairach.org/)                                                                                                                                                                                                                                |
| OASIS30AntsOASISAnts                                | [https://figshare.com/articles/ANTs_ANTsR_Brain_Templates/915436](https://figshare.com/articles/ANTs_ANTsR_Brain_Templates/915436)                                                                                                                                                                                                                               |
| OASIS30Atropos                                      | [http://www.mindboggle.info/data.html](http://www.mindboggle.info/data.html)                                                                                                                                                                                                                                                                                     |
| ICBM452AirSpace                                     | Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" with "linear transforms of the subjects into the atlas space using a 12-parameter affine transformation" [http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml](http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml)                              |
| ICBM452Warp5Space                                   | Reference space defined by the "average of 452 T1-weighted MRIs of normal young adult brains" "based on a 5th order polynomial transformation into the atlas space" [http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml](http://www.loni.usc.edu/ICBM/Downloads/Downloads_452T1.shtml)                                                                 |
| IXI549Space                                         | Reference space defined by the average of the "549 (...) subjects from the IXI dataset" linearly transformed to ICBM MNI 452.Used by SPM12. [http://www.brain-development.org/](http://www.brain-development.org/)                                                                                                                                               |
| fsaverage\[3&#124;4&#124;5&#124;6&#124;sym\]        | Images were sampled to the FreeSurfer surface reconstructed from the subject’s T1w image, and registered to an fsaverage template                                                                                                                                                                                                                                |
| UNCInfant\[0&#124;1&#124;2\]V\[21&#124;22&#124;23\] | Infant Brain Atlases from Neonates to 1-   and 2-year-olds. [https://www.nitrc.org/projects/pediatricatlas](https://www.nitrc.org/projects/pediatricatlas)                                                                                                                                                                                                       |

---
