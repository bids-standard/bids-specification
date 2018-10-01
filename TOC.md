2 Table of contents
=======================

[1 Changelog](#heading=h.17phlwhk50et)

[2 Table of contents](#heading=h.zeylawffkwh9)

[3 Introduction](#heading=h.ehs58l1sp5l0)
> [3.1 Motivation](#heading=h.nn0wr5qmclie)
> [3.2 Definitions](#heading=h.ld293tqw9us4)
> [3.3 Compulsory, optional, and additional data and
metadata](#heading=h.yic0v7leqtf3)
> [3.4 Source vs. raw vs. derived data](#heading=h.juzchuxblakl)
> [3.5 The Inheritance Principle](#heading=h.l5zwpkcouhem)
> [3.6 Extensions](#heading=h.18rh5sozhnxy)
> [3.7 Citing BIDS](#heading=h.bw5qroscmvib)

[4 File Format specification](#heading=h.nx8ar720y0tv)
> [4.1 Imaging files](#heading=h.y0f2axq397vt)
> [4.2 Tabular files](#heading=h.r85srnfs3y24)
>> [4.2.1 Example:](#heading=h.fpjccp3z8lxv)
>> [4.2.2 Example:](#heading=h.o9t9l483hwh7)

> [4.3 Key/value files (dictionaries)](#heading=h.c75m812a750g)
>> [4.3.1 Example:](#heading=h.str6bi80689r)

[5 Participant names and other labels](#heading=h.8mzv4iyo50ug)

[6 Units](#heading=h.ltev6sakv13v)

[7 Directory structure](#heading=h.1vzzcnz6wczd)
> [7.1 Single session example](#heading=h.6hp4sl1q6arb)

[8 Detailed file descriptions](#heading=h.v9uqdvt04vsf)
> [8.1 Dataset description](#heading=h.ie43v2mfgaeq)
>> [8.1.1 dataset_description.json](#heading=h.qza727avafid)
>> [8.1.2 README](#heading=h.yizt58dn4hby)
>> [8.1.3 CHANGES](#heading=h.732zmmqh1yq7)

> [8.2 Code](#heading=h.csdrm1qizwq9)
> [8.3 Magnetic Resonance Imaging data](#heading=h.5k5g55vj6iy6)
>> [8.3.1 Common metadata fields](#heading=h.5u721tt1h9pe)
>> [8.3.2 Anatomy imaging data](#heading=h.fm6ipijipc08)
>> [8.3.3 Task (including resting state) imaging
data](#heading=h.r8mrcau3kkcq)
>>> [8.3.3.1 Example:](#heading=h.1q8p210od2f)

>> [8.3.4 Diffusion imaging data](#heading=h.xfuiufnb319)
>>> [8.3.4.1 bvec example:](#heading=h.r9czn8f0t58k)
>>> [8.3.4.2 bval example:](#heading=h.e948atq2ku1n)
>>> [8.3.4.3 JSON example:](#heading=h.hxcaki8xqrp6)

>> [8.3.5 Fieldmap data](#heading=h.fcegd01wpsf8)
>>> [8.3.5.1 Case 1: Phase difference image and at least one magnitude
image](#heading=h.fexn37cr2yum)
>>> [8.3.5.2 Case 2: Two phase images and two magnitude
images](#heading=h.dytrqt3rfo2y)
>>> [8.3.5.3 Case 3: A single, real fieldmap image (showing the field
inhomogeneity in each voxel)](#heading=h.9wqqfa1lqctc)
>>> [8.3.5.4 Case 4: Multiple phase encoded directions
(“pepolar”)](#heading=h.6gef31kvsx0l)

>[8.4 Magnetoencephalography (MEG)](#heading=h.y1yw5l9a04g2)
>> [8.4.1 MEG recording data](#heading=h.ln9qkltewtqa)
>>>[8.4.1.1 Sidecar JSON document
(\*\_meg.json)](#heading=h.wmua3ist46l2)

>> [8.4.2 Channels description table
(\*\_channels.tsv)](#heading=h.2ng8e4h6db4p)
>> [8.4.3 Coordinate System JSON document
(\*\_coordsystem.json)](#heading=h.vz4gpcbftsuu)
>> [8.4.4 Photos of the anatomical landmarks and/or head localization
coils  (\*\_photo.jpg)](#heading=h.li6xt1s6zgjs)
>> [8.4.5 3-D head point /electrode locations file
(\*\_headshape.<manufacturer_specific_format>)](#heading=h.jrc7wyqvlzpp)
>> [8.4.6 Empty-room files (sub-emptyroom)](#heading=h.i7qifoac3vgf)

> [8.5 Task events](#heading=h.daip42kp5ndz)
>> [8.5.1 Example:](#heading=h.akoyjl6f4i1e)
>> [8.5.2 Example:](#heading=h.gsp1xuuo09tb)
>> [8.5.3 Example:](#heading=h.8leve31f2d03)

> [8.6 Physiological and other continuous
recordings](#heading=h.usbya6fhiy5v)
>> [8.6.1 Example:](#heading=h.mtd2764i6ii1)

> [8.7 Behavioral experiments (with no
MRI)](#heading=h.cpt8jqa5g0y7)

> [8.8 Scans file](#heading=h.rw11qtsldsuw)
>> [8.8.1 Example:](#heading=h.xtaf7kerpvji)

> [8.9 Participant file](#heading=h.pi5iigxxt8vy)
>> [8.9.1 participants.tsv example:](#heading=h.rsax9zcpo17t)

[9 Longitudinal studies with multiple sessions
(visits)](#heading=h.5c3b4lpzj5cn)
> [9.1 Sessions file](#heading=h.yba5gfw0vmht)
>> [9.1.1 Multiple sessions example:](#heading=h.ia2iiqnuitj)

[10 Multi-site or multi-center studies](#heading=h.29tn5cduh4ci)
> [10.1 Option 1: Treat each site/center as a separate
dataset.](#heading=h.totu2lw0gxlj)
> [10.2 Option 2: Combining sites/centers into one
dataset](#heading=h.1t5ygwr3qrpq)

[11 Appendix I: Contributors](#heading=h.hds2i7ii7hjo)

[12 Appendix II: Licenses](#heading=h.8bxgvc9yrtig)

[13 Appendix III: Hierarchical Event Descriptor (HED)
Tags](#heading=h.5sn36nhoj1fw)
> [13.1 Example:](#heading=h.rqz45nlfb5rx)
> [13.2 Example:](#heading=h.b382e7m2jzvb)

[14 Appendix IV: Entity table](#heading=h.hj3w5z9pw4n7)

[15 Appendix V: Units](#heading=h.h112sr17n2m2)

[16 Appendix  VI: MEG file formats](#heading=h.l5rpo9atl5qp)
> [16.1 CTF](#heading=h.kzx3m7s518x2)
> [16.2 Elekta/Neuromag](#heading=h.a7ggx48p7aaf)
> [16.3 4D neuroimaging/BTi](#heading=h.gy0kbzisg1f1)
> [16.4 KIT/Yokogawa](#heading=h.2gmmxawyna7r)
> [16.5 KRISS](#heading=h.ts11elruq7kt)
> [16.6 ITAB](#heading=h.sgxhj770nor)
> [16.7 Aalto/MEG–MRI](#heading=h.moujhgczbkr9)

[17 Appendix VII: preferred names of MEG
systems](#heading=h.bp5mugaep86u)

[18 Appendix VIII: preferred names of Coordinate
systems](#heading=h.snhwsmgj62e1)
> [18.1 MEG specific Coordinate Systems](#heading=h.kfm2qyo3x0mo)
> [18.2 EEG specific Coordinate Systems](#heading=h.z9g5132tdpry)
> [18.2 Template based Coordinate Systems](#heading=h.qrh9iqfvccq5)
