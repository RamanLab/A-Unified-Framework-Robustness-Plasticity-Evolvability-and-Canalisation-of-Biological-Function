import numpy as np
import pandas as pd
from generate_adjacency_matrices import generate_all_nxn_adjacency_matrices, filter_adjacency_matrices
from ode_model import OdeModel as GenOdes
from parameters import Parameters
import time

start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
# **********************************************************************************************************************
#                                      I       N       P       U       T       S
# **********************************************************************************************************************
# Inputs for parameter and initial conditions samples file generation
number_of_nodes = 3
# Number of parameters to sample
n_params = 10000
# Number of initial conditions to sample
n_ics = 20

# ***************************************************************************************
#                               F  I  L  E  N  A  M  E  S
# ***************************************************************************************
#                           ******************************************
#                                 D E F A U L T   F I L E N A M E S
#                           ******************************************
adj_matrix_filename = 'adjacency_matrix_file.csv'
# ***********************************************
model_filename = 'three_node_models.py'
# ************************************************
model_input_samples_file = 'model_input_samples_lhs.csv'
initial_conds_samples_file = 'initial_conditions_samples_lhs.csv'
# ************************************************
# **********************************************************************************************************************
#                           E   N   D       O   F       I   N   P   U   T   S
# **********************************************************************************************************************
# *************************************************************************
#  G E N E R A T E   A D J A C E N C Y   M A T R I C E S
# *************************************************************************
adjacency_matrix_list = generate_all_nxn_adjacency_matrices(number_of_nodes)
adjacency_matrix_list = filter_adjacency_matrices(adjacency_matrix_list)
adj_matrix_flat = pd.DataFrame(
    np.reshape(adjacency_matrix_list.flatten(), (len(adjacency_matrix_list), number_of_nodes * number_of_nodes)))
# Get adjacency matrices into a CSV file
adj_matrix_flat.to_csv(adj_matrix_filename, index=False, header=False)
print('Number of adjacency matrices generated = ' + str(len(adjacency_matrix_list)))

# ***************************************************************************************
#  G E N E R A T E   M O D E L S   B A S E D   O N   A D J A C E N C Y   M A T R I C E S
# ***************************************************************************************
def create_file(file_name):
    with open(file_name, 'w') as f:
        f.write("import numpy as np")

create_file(model_filename)

for i in range(len(adjacency_matrix_list)):
    adj_matrix = adjacency_matrix_list[i]
    # *******************************************************************************************
    #  G E N E R A T E  M O D E L  F O R  G E N E R A T E D  A D J A C E N C Y  M A T R I C E S
    # *******************************************************************************************
    Odes = GenOdes(adj_matrix)
    equations = Odes.get_model()
    # equations = Odes.get_non_dimensionalised_model()
    key_value_string_list = ['        ' + key + " = " + value + '\n' for key, value in equations.items()]

    def generate_model_in_file(file_name):
        with open(file_name, 'a') as f:
            f.write(
                "\n" + "def model" + str(i)
                + "(t, x, I, params):" + "\n        " + "dot_x = np.zeros(len(x))" + "\n" +
                "".join(key_value_string_list) + "\n        " + "return dot_x"
            )
        print("Model Number = " + str(i) + " Generation completed.")

    generate_model_in_file(model_filename)

pr = Parameters(number_of_nodes)
model_inputs = pr.sample_parameters_lhs(n_params)
model_inputs.to_csv(model_input_samples_file, index=None, header=True)
print('File ' + model_input_samples_file + ' created.')
initial_conds = pr.sample_initial_conditions_lhs(n_ics)
initial_conds.to_csv(initial_conds_samples_file, index=None, header=True)
print("File 'initial_conditions_samples_lhs.csv' created..")

print("Start time = ", start_time)
print("End time = ", time.strftime('%l:%M%p %Z on %b %d, %Y'))