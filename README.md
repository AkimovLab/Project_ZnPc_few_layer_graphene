# Project_ZnPc_few_layer_graphene
This repository includes all input files created and used for NAMD study of electron transfer at Zn-phthalocyanine/few-layer graphene

1-The file named slg.80r.8k is an input quantum espresso (QE) job which does the pre-dos (scf) calculations for optimized graphene.

2-The file named znpc-slg.70r.6k.ns is an input QE file job which does pre-dos (nscf) calculations for optimized ZnPc/single-layer graphene interface.

3-The file named znpc-dlg.80r.6k.ns is an input QE file job which does pre-dos (nscf) calculations for optimized ZnPc/double-layer graphene (DLG) interface.

4-The file named znpc-slg.60r.3k.thnr8 is an input QE file job which does thermalization of for optimized ZnPc/single-layer graphene (SLG) interface.

5-The file named znpc-dlg.60r.3k.thnr8 is an input QE file job which does thermalization of for optimized ZnPc/double-layer graphene interface.

6-The file named znpc-slg.60r.3k.dyn is an input QE file job which does dynamics step for optimized ZnPc/single-layer graphene interface.

7-The file named znpc-dlg.60r.3k.thnr8 is an input QE file job which does dynamics for optimized ZnPc/double-layer graphene interface.

8-files named slg.xyz, znpc-slg.xyz and znpc-dlg.xyz are cordinates of relaxed graphen, znpc/single-layer graphene and znpc/double-layer graphene, respectively.

9-files named znpc-slg-libra-setp2-py-src2.py and znpc-dlg-libra-setp2-submit_temple are used to perform step2, hamiltonian construction for each MD step for ZnPc/single-layer graphene interface

10-files named znpc-dlg-libra-setp2-py-src2.py and znpc-dlg-pyxaid-setp2-submit_temple are used to perform step2, hamiltonian construction for each MD step for ZnPc/double-layer graphene interface

11-files named znpc-slg-libra-step3&4-py-scr3.py and znpc-dlg-libra-step3&4-py-scr3.py do the step3 of namd calculations for ZnPc/singel-layer graphene and ZnPc/double-layer graphene, respectively

12-files named "znpcslgdft.xyz", "znpcdlgdft.xyz", are the relaxed geometries of ZnPc/SLG and ZnPc/DLG systems, respectively, using pure DFT method.

13-file named znpcslgdftu-'element'.xyz contains relaxed geometry of ZnPc/SLG interface using DFT+U method for 'element'.
