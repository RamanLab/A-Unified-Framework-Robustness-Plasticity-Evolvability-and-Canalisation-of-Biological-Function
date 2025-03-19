import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist
from scipy.spatial import distance



def get_hamming_dist(X):
    # Get Hamming Distance
    hamm_dist = pdist(X, 'hamming')
    return hamm_dist[0]

def min_max_scaling(df_data):

    df_data = df_data.T
    for column in df_data.columns:
        df_data[column] = (df_data[column] - df_data[column].min()) / (df_data[column].max() - df_data[column].min())
    return df_data.T

def get_one_hot_function_codes():
    # Every circuit exhibits one out of 20 functions. Get the circuit function as a one-hot code with length 20
    df_func_codes = pd.DataFrame()
    for id in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:

        func_code = '0' * 20
        df_temp = pd.DataFrame()
        df_func_cluster_members = pd.read_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster'  + id + '_model_params.csv', dtype={'gparam_index': str})
        df_temp['circuit_index'] = df_func_cluster_members["gparam_index"]
        func_code = func_code[:int(id)-1] + '1' + func_code[int(id):]
        df_temp['function_code'] = np.repeat(func_code, len(df_func_cluster_members))
        df_func_codes = pd.concat([df_func_codes, df_temp], axis=0).reset_index(drop=True)

    df_func_codes.to_csv('../../data/integrated_results_v0_v1_v2/csvs/function_codes.csv', header=True, index=None)

def get_k_hot_function_codes():
    # Every network exhibits multiple functions (k out of 20 functions). Get the k-hot function code with length 20
    network_list = []
    df_k_hot_codes = pd.DataFrame()
    for id in range(20):

        df_temp = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_'+ str(id + 1) +'function.csv')
        if len(df_temp) != 0:
            network_ids = df_temp.id
            network_list.extend(network_ids)
            df_func_code = df_temp.drop(columns='id')
            df_func_code = df_func_code.astype(int)
            k_hot_codes = df_func_code.apply(lambda row: ''.join(row.astype(str)), axis=1)
            df_k_hot_codes = pd.concat([df_k_hot_codes, k_hot_codes], axis=0).reset_index(drop=True)

    df_k_hot_codes['network_index'] = network_list
    df_k_hot_codes = df_k_hot_codes.sort_values(by='network_index').reset_index(drop=True)
    df_k_hot_codes.rename(columns={0: 'k_hot_code'}, inplace=True)

    df_k_hot_codes.to_csv('../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/k_hot_function_codes.csv', header=True, index=None)


def get_pairwise_network_hd_k_hot_codes():

    # Get the Hamming Distance (HD) between the k-hot function codes of network pairs
    df_k_hot_codes = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/k_hot_function_codes.csv', dtype={'k_hot_code': str})
    nmodels = len(df_k_hot_codes)
    ind = np.triu_indices(nmodels, 1)
    netk_id1 = []
    netk_id2 = []
    dist_list = []

    for i, j in zip(ind[0], ind[1]):
        code1 = list(df_k_hot_codes.iloc[i, 0])
        code2 = list(df_k_hot_codes.iloc[j, 0])
        dist = distance.hamming(code1, code2)
        netk_id1.append(df_k_hot_codes.iloc[i, 1])
        netk_id2.append(df_k_hot_codes.iloc[j, 1])
        dist_list.append(dist)

    df = pd.DataFrame()
    df['Network1'] = netk_id1
    df['Network2'] = netk_id2
    df['Hamming Distance'] = dist_list
    df.to_csv('../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/pairwise_network_hd_k_hot_codes.csv', header=True, index=False)

def get_circuitwise_function_category():

    # The circuit functions fall into 5 categories (I-V) with the first category having two subcategories (IA, IB).
    # Get the category code for each circuit
    df_func_cat_codes = pd.DataFrame()
    for id in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']:

        df_temp = pd.DataFrame()
        df_func_cluster_members = pd.read_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster'  + id + '_model_params.csv', dtype={'gparam_index': str})
        df_temp['circuit_index'] = df_func_cluster_members["gparam_index"]
        if id in ['01', '03', '05']:
            func_category = 'IA'
        elif id in ['02', '04', '06']:
            func_category = 'IB'
        elif id in ['08', '09', '11', '12', '14', '16', '17', '19']:
            func_category = 'II'
        elif id in ['07', '13']:
            func_category = 'III'
        elif id in ['20']:
            func_category = 'IV'
        elif id in ['10', '15', '18']:
            func_category = 'V'

        df_temp['function_category'] = np.repeat(func_category, len(df_func_cluster_members))
        df_func_cat_codes = pd.concat([df_func_cat_codes, df_temp], axis=0).reset_index(drop=True)

    df_func_cat_codes.to_csv('../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/circuitwise_function_category_codes.csv', header=True, index=None)




