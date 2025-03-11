import pandas as pd
from parameters import Parameters
from ode_model import solve_ode
from three_node_models import *

def simulate_model(number_of_nodes, model_inputs, I, time_start, time_initial_equilibrium, time_end, time_steps,
                   adj_matrix_filename, param_dataset_filename, ss_filepath, output_conc_filepath, output_conc_filename,
                   model):

    pr = Parameters(number_of_nodes)
    # **************************************************************************************
    #  G E T  A D J A C E N C Y  M A T R I C E S  F R O M  F I L E
    # **************************************************************************************
    adjacency_matrix_list = pd.io.parsers.read_csv(adj_matrix_filename, index_col=None, header=None).to_numpy()
    df_initial_conds = pd.read_csv(ss_filepath + '/model'+ str(model) +'_ss.csv', header=0)
    initial_conds = df_initial_conds.drop(columns=['param_index','steady_state_found'])

    current_model = 'model' + str(model)

    # Number of parameters
    n_params = model_inputs.shape[0]

    # Number of initial conditions
    n_ics = initial_conds.shape[0]

    df_ics = pd.DataFrame()
    df_output_conc = pd.DataFrame()
    df_x2 = pd.DataFrame()
    df_paramid = pd.DataFrame()

    ic_list = []
    paramid_list = []
    params_list = []

    # Iterate over the list of parameters
    for j in range(n_params):
        ic = initial_conds.iloc[j, :]
        ss_found = df_initial_conds.loc[df_initial_conds['param_index'] == j].steady_state_found.values[0]
        if ss_found == 1:
            skip = 0
        else:
            ic, skip = solve_ode(current_model, ic, model_inputs.iloc[j, :], I[0], time_start, time_initial_equilibrium,
                                 time_steps, j, ss_check=1)

        if skip == 0:
            concentrations, skip1 = solve_ode(current_model, ic, model_inputs.iloc[j, :], I[1], time_start, time_end,
                                              time_steps, j, ss_check=0)

            if skip1 == 0:
                paramid_list.append(str(model) + '.' + str(j))
                df_x2_temp = pd.DataFrame(concentrations[:, 2])
                df_x2 = pd.concat([df_x2, df_x2_temp], axis=1).reset_index(drop=True)

                params_list.append(model_inputs.iloc[j, :])
                ic_list.append(concentrations[0, :])

    df_output_conc = pd.DataFrame(df_x2.T).reset_index(drop=True)

    # Populate parameter id
    df_paramid['param_index'] = paramid_list

    # Get adjacency matrix elements into dataframe
    df_network = pr.get_network_as_dataframe(adjacency_matrix_list[model], len(paramid_list)).reset_index(drop=True)

    # Populate initial conditions
    df_ics = pd.DataFrame(ic_list, columns=['x[0]', 'x[1]', 'x[2]'])

    # Populate parameters
    df_parameters = pd.DataFrame(params_list).reset_index(drop=True)

    # Populate simulation input dataset
    df_sim_input_dataset = pd.concat([df_paramid, df_network, df_ics, df_parameters], axis=1)
    # Make parameters corresponding to missing edges zero
    df_sim_input_dataset = pr.make_unnecessary_params_zero(df_sim_input_dataset)
    df_sim_input_dataset = df_sim_input_dataset.drop(columns=['Adj0_0', 'Adj0_1', 'Adj0_2', 'Adj1_0', 'Adj1_1',
                                                              'Adj1_2', 'Adj2_0', 'Adj2_1', 'Adj2_2'])

    df_sim_input_dataset.to_csv(param_dataset_filename +'/dataset_model'+ str(model) + '.csv', header=True, index=None)

    # Populate output concentration dataset
    df_output_conc = pd.concat([df_paramid, df_output_conc], axis=1).reset_index(drop=True)

    df_output_conc.to_csv(output_conc_filepath + '/model' + str(model) + '_' + output_conc_filename, index=None,
                          header=True)

    return
