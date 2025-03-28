import pandas as pd
from calculate_sd_pd import calculate_sd_pd_network_pairwise
import sys
import multiprocessing as mp
from functools import partial
import time

# Get Functional Cluster ID and network ID
program, arg1, arg2 = sys.argv

# Get the sampled ID for all the networks
df_lhs0 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis0.csv')
df_lhs1 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis1.csv')
df_lhs2 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis2.csv')
df_lhs3 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis3.csv')
df_lhs4 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis4.csv')
df_lhs5 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis5.csv')
df_lhs6 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis6.csv')
df_lhs7 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis7.csv')
df_lhs8 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis8.csv')
df_lhs9 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis9.csv')

df_lhs0 = df_lhs0['model_index'].apply(lambda x: '0.' + str(x))
df_lhs1 = df_lhs1['model_index'].apply(lambda x: '1.' + str(x))
df_lhs2 = df_lhs2['model_index'].apply(lambda x: '2.' + str(x))
df_lhs3 = df_lhs3['model_index'].apply(lambda x: '3.' + str(x))
df_lhs4 = df_lhs4['model_index'].apply(lambda x: '4.' + str(x))
df_lhs5 = df_lhs5['model_index'].apply(lambda x: '5.' + str(x))
df_lhs6 = df_lhs6['model_index'].apply(lambda x: '6.' + str(x))
df_lhs7 = df_lhs7['model_index'].apply(lambda x: '7.' + str(x))
df_lhs8 = df_lhs8['model_index'].apply(lambda x: '8.' + str(x))
df_lhs9 = df_lhs9['model_index'].apply(lambda x: '9.' + str(x))

df_model_idx = pd.DataFrame(columns=['model_index'])
df_model_idx['model_index'] = pd.concat(
    [df_lhs0, df_lhs1, df_lhs2, df_lhs3, df_lhs4, df_lhs5, df_lhs6, df_lhs7, df_lhs8, df_lhs9], axis=0).reset_index(
    drop=True)
df_model_idx.loc[:, ['sampled_id']] = df_model_idx['model_index'].apply(lambda x: x.split('.')[0])
df_model_idx.loc[:, ['model_index']] = df_model_idx['model_index'].apply(lambda x: x.split('.')[1]).astype(
    dtype=int)
df_model_idx = df_model_idx.sort_values(by='model_index').reset_index(drop=True)

# Get the adjacency matrices for all the networks
adjacency_mat_list = pd.read_csv('../../data/common/adjacency_matrix_file.csv', header=None)
adjacency_mat_list = [row.reshape(3, 3) for row in adjacency_mat_list.values]

# Get pairs of networks
df_pairs = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                       'robustness_evolvability_plasticity_canalisation_analysis/'
                       'pairwise_sd_pd_zero_fd/groups' + str(
            arg1) + '/' + str(arg2) + '.csv')
df_pairs = df_pairs.drop(columns='network1')

start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
print("Jobs start time = ", start_time)

df_stats = pd.DataFrame()
netk1_list = []
netk2_list = []
sd_list = []
size_list = []
mean_list = []
var_list = []
skew_list = []

# Get all circuits in the functional cluster (arg1) for the current network (arg2) being processed
df1 = pd.read_csv(
    '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
    'pairwise_sd_pd_zero_fd/networkwise_circuits/fid' + arg1 + '/final_func_cluster' + arg1 + '_model' + str(
        arg2) + '.csv', dtype={'gparam_index': str})

# Get the Sampled ID for the network being processed
sampled_id1 = df_model_idx.loc[df_model_idx['model_index'] == int(arg2)].sampled_id.values[0]

# Get the parameter sets data for all the three versions for the network being processed
df1_temp_params_v0 = pd.read_csv(
    '../../data/v0/dataset' + str(sampled_id1) + '_lhs/input_sim_data/dataset_model' + str(
        arg2) + '.csv', dtype={'param_index': str})
df1_temp_params_v1 = pd.read_csv(
    '../../data/v1/dataset' + str(sampled_id1) + '_lhs/input_sim_data/dataset_model' + str(
        arg2) + '.csv', dtype={'param_index': str})
df1_temp_params_v2 = pd.read_csv(
    '../../data/v2/dataset' + str(sampled_id1) + '_lhs/input_sim_data/dataset_model' + str(
        arg2) + '.csv', dtype={'param_index': str})


calculate_sd_pd_partial = partial(calculate_sd_pd_network_pairwise, arg1, df_model_idx, adjacency_mat_list,
                                      arg2, df1, df1_temp_params_v0, df1_temp_params_v1, df1_temp_params_v2)

with mp.Pool(mp.cpu_count()) as pool:
    results = pool.map(calculate_sd_pd_partial, df_pairs.network2.values)

# For a given network get the pair with all other networks in a functional cluster. For every such network pair get the
# Structural Diversity and the number of circuit pairs the two networks share, and the mean, variance, and skew of the
# Parametric Diversities across all such circuit pairs
df_stats = pd.DataFrame(results, columns=['netkwork_index1', 'netkwork_index2', 'structural_diversity', 'n', 'mean',
                                          'variance', 'skew'])

df_stats.to_csv(
    '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
    'pairwise_sd_pd_zero_fd/pairwise_sd_pd_fid' + str(arg1) + '/pairwise_sd_pd_fid' + str(arg1) + '_model' +
    str(arg2) + '.csv', header=True, index=None)

print(arg2)

end_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
print("Jobs end time = ", end_time)