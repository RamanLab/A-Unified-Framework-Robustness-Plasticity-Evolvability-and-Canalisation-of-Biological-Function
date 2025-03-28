import pandas as pd
import numpy as np
from scipy.stats import skew
from scipy.spatial.distance import cdist, pdist


def calculate_sd_pd_network_pairwise(arg1, df_model_idx, adjacency_mat_list, netk1, df1, df1_temp_params_v0, df1_temp_params_v1, df1_temp_params_v2, netk2):

    if netk1 != netk2:

        dist_list = []
        sd_temp = pdist([adjacency_mat_list[int(netk1)].flatten(), adjacency_mat_list[int(netk2)].flatten()],
                        'hamming')

        df2 = pd.read_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/networkwise_circuits/fid' + arg1 + '/final_func_cluster' + arg1 + '_model' + str(
                netk2) + '.csv', dtype={'gparam_index': str})

        sampled_id2 = df_model_idx.loc[df_model_idx['model_index'] == int(netk2)].sampled_id.values[0]
        ver1_list = df1.version.unique()
        ver2_list = df2.version.unique()
        for ver1 in ver1_list:
            df1_temp = df1[df1['version'] == ver1]

            if ver1 == 0:
                df1_temp_params = df1_temp_params_v0
            elif ver1 == 1:
                df1_temp_params = df1_temp_params_v1
            elif ver1 == 2:
                df1_temp_params = df1_temp_params_v2

            df_temp1 = df1_temp_params.loc[df1_temp_params['param_index'].isin(df1_temp.gparam_index.values)]
            df_temp1 = df_temp1.set_index('param_index')
            df_temp1 = df_temp1.drop(columns=['x[0]', 'x[1]', 'x[2]', 'nI', 'KI', 'v0', 'v1', 'v2'])

            for ver2 in ver2_list:
                df2_temp = df2[df2['version'] == ver2]

                df_temp2 = pd.read_csv(
                    '../../data/v' + str(ver2) + '/dataset' + str(sampled_id2) + '_lhs/input_sim_data/dataset_model' + str(
                        netk2) + '.csv', dtype={'param_index': str})
                df_temp2 = df_temp2.loc[df_temp2['param_index'].isin(df2_temp.gparam_index.values)]

                df_temp2 = df_temp2.set_index('param_index')
                df_temp2 = df_temp2.drop(columns=['x[0]', 'x[1]', 'x[2]', 'nI', 'KI', 'v0', 'v1', 'v2'])

                dist12 = cdist(df_temp1.to_numpy(), df_temp2.to_numpy(), metric='euclidean')
                dist12 = dist12.flatten()
                dist_list.extend(dist12)

        return [netk1, netk2, sd_temp[0], len(dist_list), np.mean(dist_list), np.var(dist_list, ddof=1), skew(dist_list)]
    else:
        return
