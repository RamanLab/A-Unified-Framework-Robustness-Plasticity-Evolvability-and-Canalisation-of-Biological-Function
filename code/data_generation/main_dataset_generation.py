import pandas as pd
from functools import partial
import multiprocessing
import time
from simulate_model import simulate_model
import os

start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
print("Start time = ", start_time)
# **********************************************************************************************************************
#                                      I       N       P       U       T       S
# **********************************************************************************************************************

# **********************************************************************************************************************
# Inputs for simulation
number_of_nodes = 3
time_start = 0
time_initial_equilibrium = 20
time_end = 100
time_steps = 1
# Step input
I = [0.06, 0.6]
# # Specify a range or list of model indices
model_indices_to_simulate = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis9.csv', header=0)
model_indices_to_simulate = model_indices_to_simulate.model_index.values

# ***************************************************************************************
#                               F  I  L  E  N  A  M  E  S
# ***************************************************************************************
#                           ******************************************
#                                 D E F A U L T   F I L E N A M E S
#                           ******************************************
adj_matrix_filename = '../../data/common/adjacency_matrix_file.csv'
# ***********************************************
model_filename = 'three_node_models.py'
# ************************************************

model_input_samples_file = '../../data/common/model_input_samples_lhs.csv'
# Path to find steady state concentrations
ss_filepath = '../../data/v2/ss/'

# ************************************************
# Path to store the files containing simulation parameters for each model
param_dataset_filename = '../../data/v2/dataset9_lhs/input_sim_data'

# Path to store time course data
output_conc_filepath = '../../data/v2'

# The time course data files for each model will have this suffix
output_conc_filename = 'output_conc.csv'
#                           *******************************************************
#                                  U S E R - D E F I N E D    F I L E N A M E S
#                           ********************************************************

# adj_matrix_filename =
# model_filename =
# dataset_filename =

# **********************************************************************************************************************
#                   E   N   D       O   F       I       N       P       U       T       S
# **********************************************************************************************************************

model_inputs = pd.read_csv(model_input_samples_file, header=0)

pool = multiprocessing.Pool(processes=os.cpu_count())
simulate_model_partial = partial(simulate_model, number_of_nodes, model_inputs, I, time_start, time_initial_equilibrium,
                                 time_end, time_steps, adj_matrix_filename, param_dataset_filename, ss_filepath,
                                 output_conc_filepath, output_conc_filename)
pool.map(simulate_model_partial, model_indices_to_simulate)

print("End time = ", time.strftime('%l:%M%p %Z on %b %d, %Y'))