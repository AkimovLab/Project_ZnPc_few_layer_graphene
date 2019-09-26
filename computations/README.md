0-opt: QE input files to run geometry optimization of ground state (gs) and excited states (es). The output files are also included. The .xyz files contains the relaxed geometries

1-pdos: QE input file to calculate the pdos. The results of pDOS for ZnPc/FLG interfaces. The files' name indicate which figure in the paper displays the data

2-md: QE input files to run ab initio molecular dynamicsfor bringing the system from 0K to 300K and perform post-heating the dynamics step (NVE-trajectory).

3-nac-step2: python-base libra/pyxaid and QE files to perform the step2 (NAC calculation)

4-NA-MD: electron-no-soc.py - script for electron intraband relaxation without SOC electron-soc.py - script for electron intraband relaxation with SOC hole-no-soc.py - script for hole intraband relaxation without SOC hole-soc.py - script for hole intraband relaxation with SOC
