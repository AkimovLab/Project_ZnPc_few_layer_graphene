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

# Lets read in the files
ham_dir = "/home/mahdipor_hamid.physics.sharif/jobs/g_znpc/libra/dlg/step2/res-lib-dlg-p/"

# read in the files
# In my case, the files contain 32 x 32 matrices, which are composed of 16 x 16 blocks of alpha and beta orbitals.
# In this set of spin-orbitals, the orbital with index 7 is the alpha-HOMO.
# Assume we only need HOMO-1, HOMO, LUMO and LUMO+1 alpha-spin orbitals,
#  so we can define this by setting the "active_space" parameter to the list [6, 7, 8, 9]
params = { "data_set_paths" : [ham_dir],
           "data_dim":32, "active_space":[3,4,5,6,7,8,9,10,11,12,13],
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


# How the KS orbitals are re-indexed before making SD states
# 3 ZnPc (H-4)  -> 1
# 4  G   (H-3)  -> 2
# 5  G   (H-2)  -> 3
# 6  G   (H-1)  -> 4
# 7  G    (H)   -> 5
# 8  G    (L)   -> 6
# 9  G   (L+1)  -> 7
# 10  G   (L+2)  -> 8
# 11  G   (L+3)  -> 9
# 12 ZnPc (L+4)  -> 10
# 13 ZnPc (L+5)  -> 11

# Define SD bases -indexing here begings from 1
params.update( { "SD_basis" : [ 
                           # Omega 3 electron transfer
                                 # S0: 1 -> 6
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -6],
                                 # S1: 1 -> 7
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -7],
                                 # S2: 1 -> 8
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -8],
                                 # S3: 1 -> 9
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -9],
                           
                           # Omega 4 initial excited
                                 # S4: 1 -> 10
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -10],
                                 # S5: 1 -> 11
                           [ 1, 2, -2, 3, -3, 4, -4, 5, -5, -11],
                           ],
                }  )
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
                 "do_orthogonalization" : 1,  # 1
                 "do_state_reordering" : 2,   # 2
                 "state_reordering_alpha": 0.0,
                 "do_phase_correction" : 1,   # 1
                 "do_output" : 1,
                 "Hvib_re_prefix":"Hvib_",  "Hvib_re_suffix":"_re",
                 "Hvib_im_prefix":"Hvib_",  "Hvib_im_suffix":"_im",
              }  )

Hvib = step3.run(S, St, Hvib_ks, params)

# rescaling of NACs of pairs of SD states corresponding to the shift of ZnPc's energy levels
data_conv.scale_NAC(Hvib, 0, 2, 0.20/0.50) # - rescale NAC between Phi_0 and Phi_2
data_conv.scale_NAC(Hvib, 2, 0, 0.20/0.50) # - rescale NAC between Phi_0 and Phi_2
data_conv.scale_NAC(Hvib, 0, 3, 0.30/0.50) # - rescale NAC between Phi_0 and Phi_3
data_conv.scale_NAC(Hvib, 3, 0, 0.30/0.50) # - rescale NAC between Phi_0 and Phi_3
data_conv.scale_NAC(Hvib, 0, 4, 0.50/0.30) # - rescale NAC between Phi_0 and Phi_4
data_conv.scale_NAC(Hvib, 4, 0, 0.50/0.30) # - rescale NAC between Phi_0 and Phi_4
data_conv.scale_NAC(Hvib, 0, 5, 0.60/0.40) # - rescale NAC between Phi_0 and Phi_5
data_conv.scale_NAC(Hvib, 5, 0, 0.60/0.40) # - rescale NAC between Phi_0 and Phi_5
data_conv.scale_NAC(Hvib, 1, 2, 0.20/0.50) # - rescale NAC between Phi_1 and Phi_2
data_conv.scale_NAC(Hvib, 2, 1, 0.20/0.50) # - rescale NAC between Phi_1 and Phi_2
data_conv.scale_NAC(Hvib, 1, 3, 0.20/0.50) # - rescale NAC between Phi_1 and Phi_3
data_conv.scale_NAC(Hvib, 3, 1, 0.20/0.50) # - rescale NAC between Phi_1 and Phi_3
data_conv.scale_NAC(Hvib, 1, 4, 0.50/0.30) # - rescale NAC between Phi_1 and Phi_4
data_conv.scale_NAC(Hvib, 4, 1, 0.50/0.30) # - rescale NAC between Phi_1 and Phi_4
data_conv.scale_NAC(Hvib, 1, 5, 0.60/0.40) # - rescale NAC between Phi_1 and Phi_5
data_conv.scale_NAC(Hvib, 5, 1, 0.60/0.40) # - rescale NAC between Phi_1 and Phi_5
data_conv.scale_NAC(Hvib, 2, 4, 0.30/0.30) # - rescale NAC between Phi_2 and Phi_4
data_conv.scale_NAC(Hvib, 4, 2, 0.30/0.30) # - rescale NAC between Phi_2 and Phi_4
data_conv.scale_NAC(Hvib, 2, 5, 0.40/0.20) # - rescale NAC between Phi_2 and Phi_5
data_conv.scale_NAC(Hvib, 5, 2, 0.40/0.20) # - rescale NAC between Phi_2 and Phi_5
data_conv.scale_NAC(Hvib, 3, 4, 0.30/0.30) # - rescale NAC between Phi_3 and Phi_4
data_conv.scale_NAC(Hvib, 4, 3, 0.30/0.30) # - rescale NAC between Phi_3 and Phi_4
data_conv.scale_NAC(Hvib, 3, 5, 0.40/0.20) # - rescale NAC between Phi_3 and Phi_5
data_conv.scale_NAC(Hvib, 5, 3, 0.40/0.20) # - rescale NAC between Phi_3 and Phi_5


shift_factor_1=-1.02/27.2114
shift_factor_2=+0.2/27.2114
shift_factor_3=-0.42/27.2114   # -0.52
# shifting the energy levels
data_conv.scissor(Hvib, 0, shift_factor_1) # all SD state energies are lowered by -1.06 eV as a result of lowering energy of ZnPc's H state by -1.02 eV
data_conv.scissor(Hvib, 2, shift_factor_2) # energies of  2 and 3 SD states are made larger by +0.4 eV as a result of getting the two extra states above ZnPc's L+1
data_conv.scissor(Hvib, 4, shift_factor_3) # energies of SD states 4 and 5 (initial excitations) are lowered to get ZnPc's conductions below the DLG's extra states 

# Compute tNAC map
opt = 2
Hvib_ave = data_stat.cmat_stat2(Hvib[0], opt)
data_outs.show_matrix_splot((1000.0/units.ev2Ha)*Hvib_ave.imag(), "_tnac_dlg_61p1_pc1sr1.txt", set_diag_to_zero=0)

tau, rates = decoherence_times.decoherence_times_ave(Hvib, [0], params["fsnap"], 0)
avg_deco = tau*units.au2fs
avg_deco.show_matrix()

# 5. Nonadiabatic Dynamics
params = {}

params["nfiles"] = 5997 # Ex # of Hvib files to read for a given traj


nmicrost = len(Hvib[0])
for i in [0, 2, 3]:
    for j in [4]:


        params["nstates"] = 6

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
        params["istate"] = j               # indexing here begins from 0, the last is 5
        
        # Set initial Times
        init_times = []
        for k in xrange(20):
             init_times.append(k*50+1000)
        params["init_times"] = init_times     # starting points for sub-trajectories
        
        # Set output file
        params["outfile"] = "_out_"+str(params["decoherence_method"])+"_"+str(params["istate"])+".txt"    # output file

        # For running NA-MD
#        Hvib = step4.get_Hvib2(params)    # get the Hvib for all datat sets, Hvib is a list of lists
        res = step4.run(Hvib, params)

