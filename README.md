# Project_ZnPc_few_layer_graphene
This repository includes all input files created and used for NAMD study of electron transfer at Zn-phthalocyanine/few-layer graphene

1-The file named graphene.80r.8k is an input quantum espresso (QE) job which does the pre-dos (nscf) calculations for optimized graphene.

2-The file named graph_znpc.70r.6k.ns is an input QE file job which does pre-dos (nscf) calculations for optimized ZnPc/single-layer graphene interface.

3-The file named 2lgraph_znpc.80r.6k.ns is an input QE file job which does pre-dos (nscf) calculations for optimized ZnPc/double-layer graphene interface.

4-The file named graph_znpc.60r.3k.thnr8 is an input QE file job which does thermalization of for optimized ZnPc/single-layer graphene interface.

5-The file named 2lgraph_znpc.60r.3k.thnr8 is an input QE file job which does thermalization of for optimized ZnPc/double-layer graphene interface.

6-The file named graph_znpc.60r.3k.dyn is an input QE file job which does dynamics step for optimized ZnPc/single-layer graphene interface.

7-The file named 2lgraph_znpc.60r.3k.thnr8 is an input QE file job which does dynamics for optimized ZnPc/double-layer graphene interface.

8-files named graphene.xyz, graph_znpc.xyz and 2dgraph_znpc.xyz are cordinates of relaxed graphen, znpc/single-layer graphene and znpc/double-layer graphene, respectively.

9-files named graph_znpc-pyxaid-setp2-py-src2.py and 2lgraph_znpc-pyxaid-setp2-submit_temple are used to perform step2, hamiltonian construction for each MD step for ZnPc/single-layer graphene interface

10-files named 2lgraph_znpc-pyxaid-setp2-py-src2.py and 2lgraph_znpc-pyxaid-setp2-submit_temple are used to perform step2, hamiltonian construction for each MD step for ZnPc/double-layer graphene interface

11-files named graph_znpc-pyxaid-step3-py-scr3.py and 2lgraph_znpc-pyxaid-step3-py-scr3.py do the step3 of namd calculations for ZnPc/singel-layer graphene and ZnPc/double-layer graphene, respectively
