import os
import sys
import math
import copy

if sys.platform=="cygwin":
    from cyglibra_core import *
elif sys.platform=="linux" or sys.platform=="linux2":
    from liblibra_core import *

from libra_py import units
from libra_py import hpc_utils
from libra_py import data_read
from libra_py import data_outs
from libra_py import data_conv
from libra_py import QE_methods
import libra_py.workflows.nbra.step3 as step3
import libra_py.workflows.nbra.step4 as step4
import libra_py.workflows.nbra.decoherence_times as decoherence_times
from libra_py import data_conv
from libra_py import fit
from libra_py import influence_spectrum as infsp
from libra_py import data_stat

# Remove the previous results and temporary working directory from the previous runs
os.system("rm -r traj1_out_pyxaid")

# Create the new results directory
os.system("mkdir traj1_out_pyxaid")

# read in the files
# In my case, the files contain 22 x 22 matrices, which are composed of 11 x 11 blocks of alpha and beta orbitals.
# In this set of spin-orbitals, the orbital with index 5 is the alpha-HOMO.
# Assume we only need HOMO-1, HOMO, LUMO and LUMO+1 alpha-spin orbitals,
#  so we can define this by setting the "active_space" parameter to the list [4, 5, 6, 7]

ham_dir = "/home/mahdipor_hamid.physics.sharif/jobs/g_znpc/libra/slg/step2/res-lib-slg-p/"
params = { "data_set_paths" : [ham_dir],
           "data_dim":22, "active_space":[3,4,5,6,7,8,9],
           "isnap":0,  "fsnap":5997,           
           "data_re_prefix" : "S_dia_ks_", "data_re_suffix" : "_re",
           "data_im_prefix" : "S_dia_ks_", "data_im_suffix" : "_im"          
         }
S = data_read.get_data_sets(params)

params.update({ "data_re_prefix" : "St_dia_ks_", "data_re_suffix" : "_re",
                "data_im_prefix" : "St_dia_ks_", "data_im_suffix" : "_im"  } ) 
St = data_read.get_data_sets(params)
 
params.update({ "data_re_prefix" : "hvib_dia_", "data_re_suffix" : "_re",
                "data_im_prefix" : "hvib_dia_", "data_im_suffix" : "_im"  } ) 
Hvib_ks = data_read.get_data_sets(params)


# How, the KS orbitals are re-indexed as:
# 3 ZnPc (H-2)  -> 1
# 4   G  (H-1)  -> 2
# 5   G   (H)   -> 3
# 6   G   (L)   -> 4
# 7   G  (L+1)  -> 5
# 8 ZnPc (L+2)  -> 6
# 9 ZnPc (L+3)  -> 7

# Define SD bases -indexing here begings from 1
params.update( { "SD_basis" : [ 
                           # Omega 3 electron transfer
                                 # S0:1 -> 4        
                          [ 1, 2, -2, 3, -3, -4],
                                 # S1:1 -> 5
                          [ 1, 2, -2, 3, -3, -5],
                           # Omega 4 initial excited
                                 # S2:1 -> 6
                          [ 1, 2, -2, 3, -3, -6],
                                 # S3:1 -> 7
                          [ 1, 2, -2, 3, -3, -7],
                         ],
                } )
CI_basis = []
SD_energy_corr = [0.0]*len(params["SD_basis"])
for i in xrange(len(params["SD_basis"])):
     
    CI_basis.append( [] )

    for j in xrange(len(params["SD_basis"])):

        if i == j:
           CI_basis[i].append(1.0)
        else:
           CI_basis[i].append(0.0)

params.update( { "CI_basis": CI_basis,
                 "SD_energy_corr": SD_energy_corr,
             } )
          
# Update parameters
params.update( { "output_set_paths" : [os.getcwd()+"/traj1_out_pyxaid/"],
                 "dt" : 1.0*units.fs2au,
                 "do_orthogonalization" : 1,   # 1
                 "do_state_reordering" : 2,   # 2
                 "state_reordering_alpha": 0.0,
                 "do_phase_correction" : 1,   # 1
                 "do_output" : 1,
                 "Hvib_re_prefix":"Hvib_",  "Hvib_re_suffix":"_re",
                 "Hvib_im_prefix":"Hvib_",  "Hvib_im_suffix":"_im",
              }  )

Hvib = step3.run(S, St, Hvib_ks, params)

# To make the shift and rescaling not working just uncomment """ before and after rescaling lines
# """  # to switch on and off the shifting/rescaling

# rescaling the SD NACs corresponding to the shifts of ZnPc's energy levels
data_conv.scale_NAC(Hvib, 0, 2, 0.70/0.30) # - rescale NAC between Phi_0 and Phi_2
data_conv.scale_NAC(Hvib, 2, 0, 0.70/0.30) # - rescale NAC between Phi_0 and Phi_2
data_conv.scale_NAC(Hvib, 0, 3, 0.80/0.40) # - rescale NAC between Phi_0 and Phi_3
data_conv.scale_NAC(Hvib, 3, 0, 0.80/0.40) # - rescale NAC between Phi_0 and Phi_3
data_conv.scale_NAC(Hvib, 1, 2, 0.60/0.20) # - rescale NAC between Phi_1 and Phi_2
data_conv.scale_NAC(Hvib, 2, 1, 0.60/0.20) # - rescale NAC between Phi_1 and Phi_2
data_conv.scale_NAC(Hvib, 1, 3, 0.70/0.30) # - rescale NAC between Phi_1 and Phi_3 
data_conv.scale_NAC(Hvib, 3, 1, 0.70/0.30) # - rescale NAC between Phi_1 and Phi_3

data_conv.scale_NACs(Hvib, 1.053) # this rescaling (of NACs) is performed as the SLG did get thermalized aroung 260-280K rather than 300K 

# shifting the energy levels
data_conv.scissor(Hvib, 0, -1.00/27.2114) # all SD state energies are lowered by -1.06 eV as a result of lowering energy of ZnPc's H state by -1.06 eV
data_conv.scissor(Hvib, 2, -0.40/27.2114) # energies of  2 and 3 SD states are lowered more by -0.33 eV as a result of lowering energies of ZnPc's L and L+1 states by -0.33 eV 

# """  # to switch on and off the shifting/rescaling


# Compute tNAC map
opt = 2
Hvib_ave = data_stat.cmat_stat2(Hvib[0], opt)
data_outs.show_matrix_splot((1000.0/units.ev2Ha)*Hvib_ave.imag(), "_tnac_61_pc1sr1.txt", set_diag_to_zero=0)

#  calculations of the decoherence times

tau, rates = decoherence_times.decoherence_times_ave(Hvib, [0], params["fsnap"], 0)
avg_deco = tau*units.au2fs
avg_deco.show_matrix()

# Compute average band gap:
# avg_gap = decoherence_times.energy_gaps_ave(Hvib, [0], nsteps)

# 5. Nonadiabatic Dynamics
params = {}

params["nfiles"] = 5997 # ex # of Hvib files to read for a given traj

for i in [0, 2, 3]:
    for j in [2, 3]:
        


        params["nstates"] = 4                 # Ex set equal to the total # of states. indexing here begins from 1

        # General simulation parameters
        params["T"] = 300.0                   # Temperature, in K
        params["ntraj"] = 1000                 #number of stochatsic trajectories 
        # TSH:
        params["sh_method"] = 1               # 0 - MSSH, 1 - FSSH
        params["decoherence_method"] = i      # 0 (no), 1 (ID-A), 2 (mSDM), 3 (DISH)
        params["dt"] = 1.0*units.fs2au        # Nuclear dynamics integration timestep. in a.u.
        params["nsteps"] = 4000               # can not be larger than len(Hvib)
        params["Boltz_opt"] = 1               # options: 0 (no), 1 (Pyxaid), 2 (Classical), 3 (N-state Boltzmann)
        
        # Set initial Electronic states
        params["istate"] = j               # indexing here begins from 0, the last is 16
        
        # Set initial Times
        init_times = []
        for k in xrange(20):
            init_times.append(k*50+1000)
        params["init_times"] = init_times  # starting points for sub-trajectories
       
        # Set  output file
        params["outfile"] = "_out_"+str(params["decoherence_method"])+"_"+str(params["istate"])+".txt"   # output file

        # For running NA-MD
#        Hvib = step4.get_Hvib2(params)      # get the Hivib for all data stes. Hvib is a list of lists
        
        # Compute avergae band gap:
        # avg_gap = decoherence_times.energy_gaps_av(Hvib, params["init_times"], params["nsteps"])

        # Apply rigid energy shift to data
        # data_con.scissor(Hvib, 1, shift)

        # Optional: Print decoherence times
        
        # Run NA-MD
        res = step4.run(Hvib, params)

