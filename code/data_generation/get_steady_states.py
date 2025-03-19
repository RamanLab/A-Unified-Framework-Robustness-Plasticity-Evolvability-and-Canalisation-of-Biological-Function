import numpy as np
from scipy.optimize import fsolve
import pandas as pd
import multiprocessing
from functools import partial
from three_node_models import *
import time
import os

start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
print("Start time = ", start_time)

model_inputs = pd.read_csv('../../data/v2_2/model_input_samples_lhs.csv', header=0)
initial_conds = pd.read_csv('../../data/v2_2/initial_conditions_samples_lhs.csv', header=0)
output_file_path = '../../data/v2_2/ss_v2_2/'

# Specify number of time points for simulation
time_start = 0
time_end = 100
time_steps = 1
t = np.linspace(time_start, time_end, int(((time_end - time_start)/time_steps))+1)

# Input applied at time 't = 0'
I = 0.06

# Specify a range or list of model indices
model_indices = list(range(0, 16038, 1))

def find_steady_state(initial_conds, t, I, model_inputs, output_file_path, model):

    current_model = 'model' + str(model)
    model = globals()[current_model]
    n_params = model_inputs.shape[0]
    n_ics = initial_conds.shape[0]
    param_index_list = []
    ic_list = []
    found_list = []

    for j in range(n_params):
        found = 0

        for i in range(n_ics):
            ss = fsolve(model, initial_conds.iloc[i, :], args=(t, I, model_inputs.iloc[j, :]))
            val = model(ss, t, I, model_inputs.iloc[j, :])

            if all(elem < 1e-7 for elem in val):
                if all(s >= 0.001 for s in ss):
                    found = 1
                    param_index_list.append(str(j))
                    ic_list.append(ss)
                    found_list.append(found)
                    break
        if found == 0:
            param_index_list.append(str(j))
            ic_list.append(ss)
            found_list.append(found)

    df_ss = pd.DataFrame(ic_list, columns=['x[0]', 'x[1]', 'x[2]'])
    df_ss['param_index'] = param_index_list
    df_ss['steady_state_found'] = found_list
    df_ss.to_csv(output_file_path + current_model+'_ss.csv', header=True, index=None)

pool = multiprocessing.Pool(processes=os.cpu_count())
find_ss_partial = partial(find_steady_state, initial_conds, t, I, model_inputs, output_file_path)
pool.map(find_ss_partial, model_indices)

print("End time = ", time.strftime('%l:%M%p %Z on %b %d, %Y'))