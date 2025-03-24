import pandas as pd
import numpy as np
from get_parametric_diversity import get_parametric_diversity
import os

def calculate_fd_pd(df_model_idx, df_weights, overall_mean_pd, output_filename, id):

    # Get the function categories of all circuits sharing the structure given by the index 'id'
    df_func_cat = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_pd_fd_zero_sd/'
        'networkwise_circuits/function_category_codes_model' + str(id) + '.csv')
    df_func_cat = df_func_cat.drop(columns='model_index')

    # Get the function codes of all circuits sharing the structure given by the index 'id'
    df_func_code = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_pd_fd_zero_sd/'
        'networkwise_function_codes/function_codes_model' + str(id) + '.csv',
        dtype={'function_code': str})
    df_func_code = df_func_code.drop(columns='model_index')


    # Get the sampled dataset ID for the network given by the index 'id'
    sampled_id = df_model_idx.loc[df_model_idx['model_index'] == id].sampled_id.values[0]

    # Get parametric diversity for circuit pairs
    df_pd = pd.DataFrame()
    df_pd = get_parametric_diversity(id, sampled_id)

    # Get the function category for the circuits in each pair
    df_pd = df_pd.merge(df_func_cat, left_on='circuit_index1', right_on='circuit_index'
                        ).drop('circuit_index', axis=1)
    df_pd = df_pd.merge(df_func_cat, left_on='circuit_index2', right_on='circuit_index',
                        suffixes=('1', '2')).drop('circuit_index', axis=1)

    # Rename the columns to match the weights dataframe
    df_pd.rename(columns={'function_category1': 'circuit1_category', 'function_category2': 'circuit2_category',
                          'distance': 'parametric_diversity'}, inplace=True)

    # Get the weights (w_ij) for the circuit pairs based on the function category combination for the pair
    df_pd = pd.merge(df_pd, df_weights, on=['circuit1_category', 'circuit2_category'], how='left')
    df_pd = df_pd.drop(columns=['circuit1_category', 'circuit2_category'])

    # Get the one-hot function codes for the circuits in each pair
    df_pd = df_pd.merge(df_func_code, left_on='circuit_index1', right_on='circuit_index').drop('circuit_index',
                                                                                               axis=1)
    df_pd = df_pd.merge(df_func_code, left_on='circuit_index2', right_on='circuit_index',
                        suffixes=('1', '2')).drop('circuit_index', axis=1)

    # Calculate the Hamming Distance between the one-hot function codes for the circuits in each pair. In this case,
    # the Hamming Distance is 0 if the function codes are identical or 1 if they are different
    df_pd['hd_1_hot'] = np.where(df_pd['function_code1'] == df_pd['function_code2'], 0, 1)

    # Calculate Functional Diversity
    df_pd['functional_diversity'] = df_pd['weight'] * df_pd['hd_1_hot']
    df_pd['functional_diversity'] = df_pd['functional_diversity'].astype(np.float32)
    df_pd = df_pd.drop(
        columns=['circuit_index1', 'circuit_index2', 'function_code1', 'function_code2', 'weight', 'hd_1_hot'])

    # Get the statistics of the Parametric Diversity over all circuits sharing the structure 'id'
    df_stats = pd.DataFrame(df_pd['parametric_diversity'].describe())
    df_stats = df_stats.T.reset_index(drop=True)
    df_stats['model_index'] = [id]

    if overall_mean_pd != 0:
        # Find number of circuit pairs that are:
        # 1. Robust: FD = 0, and PD > Overall Mean Parametric Diversity
        # 2. Plastic: FD = 0.5 or 1.0 and PD < Overall Mean Parametric Diversity
        for fd in df_weights.weight.unique():
            temp = df_pd.loc[df_pd['functional_diversity'] == fd.astype(np.float32)].parametric_diversity.values
            if len(temp) > 0:
                if fd == np.float32(0.0):
                    df_stats['nckts_FD_0.0'] = [len(temp)]
                    df_stats['nckts_robust'] = [len(temp[temp > overall_mean_pd])]

                elif fd == np.float32(0.5):
                    df_stats['nckts_FD_0.5'] = [len(temp)]
                    df_stats['nckts_plastic_0.5'] = [len(temp[temp < overall_mean_pd])]

                elif fd == np.float32(1.0):
                    df_stats['nckts_FD_1.0'] = [len(temp)]
                    df_stats['nckts_plastic_1.0'] = [len(temp[temp < overall_mean_pd])]
            else:
                if fd == np.float32(0.0):
                    df_stats['nckts_FD_0.0'] = [0]
                    df_stats['nckts_robust'] = [0]

                elif fd == np.float32(0.5):
                    df_stats['nckts_FD_0.5'] = [0]
                    df_stats['nckts_plastic_0.5'] = [0]

                elif fd == np.float32(1.0):
                    df_stats['nckts_FD_1.0'] = [0]
                    df_stats['nckts_plastic_1.0'] = [0]

    file_exists = os.path.isfile(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_pd_fd_zero_sd/'+output_filename)
    if not file_exists:
        df_stats.to_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_pd_fd_zero_sd/'+output_filename,
            header=True, index=None)
    else:
        df_stats.to_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/pairwise_pd_fd_zero_sd/'+output_filename,
            header=False, index=None, mode='a')

    print(id)
