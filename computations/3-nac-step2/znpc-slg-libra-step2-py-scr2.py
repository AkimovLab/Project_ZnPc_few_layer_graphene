import os
import sys
import time
import math

# Fisrt, we add the location of the library to test to the PYTHON path
if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *
    

from libra_py import *



# We have already produced a QE MD trajectory and it is stored in the file x0.md.out
# (which we copied in the present directory).
# We need to also create a x0.scf.in file that contains the parameters for QE calculations
# (the type of calculation should be scf). The file should not contain the atomic coordiantes
# section, but should contain the cell parameters sections or occupations if they are used.
# Place the file in the current directory.

# Also create a x0.exp.in file (also to be placed in the present directory). It shall describe 
# the procedured for the wavefunction "export" operation - mainly the location and names of 
# atomic pseudopotentials and the correct prefix for the files.

# The following section will clean up the previous results and temporary directory (BEWARE!!! 
# you may not always want to do this for it will delete expensive results)
# Remove the previous results and temporary working directory from the previous runs

nsteps_per_job = 500
tot_nsteps = 2000

# tot_nsteps = total simulation time
# tot_nsteps /nsteps_per_job = total number of jobs submitted

os.system("mkdir res")

# We'll use QE_methods.out2inp() function to convert the MD trajectory into a bunch of input 
# files for SCF calculation - this is something we'll need for NAC calculations.
# In this case, you need to setup the iinit and ifinal variables which determine which steps of 
# the original MD trajectory will be used to produce the input files and subsequenctly used in
#  the NACs calculations

# All these files will be generated in the temporarily-created wd directory. The system then "cd"
# into that directory to start the consecutive operations in that directory

QE_methods.out2inp("x0.md.out","x0.scf.in","wd","x0.scf",0,tot_nsteps,1)
os.system("cp submit_templ.pbs wd"); os.system("cp x0.exp.in wd"); os.chdir("wd")
hpc_utils.distribute(0,tot_nsteps,nsteps_per_job,"submit_templ.pbs",["x0.exp.in"],["x0.scf"],2)
