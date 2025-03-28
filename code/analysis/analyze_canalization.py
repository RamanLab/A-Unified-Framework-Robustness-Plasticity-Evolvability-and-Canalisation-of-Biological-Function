import pandas as pd
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
import seaborn as sns


def split_networkpairs_by_sd():

    df_hd = pd.read_csv('../../data/common/hamming_distance_all_networks.csv')
    df_hd.loc[:, ['Hamming_Distance']] = df_hd['Hamming_Distance'].apply(lambda x: round(x, 4))

    sd_list = df_hd.Hamming_Distance.unique()
    for sd in sd_list:
        df_temp = df_hd.loc[df_hd['Hamming_Distance'] == sd]
        df_temp.to_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                       'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/'
                       'network_pairs_hd_'+str(sd)[2:3]+'.csv', header=True, index=False)

def get_number_of_canalised_circuits_by_fid_hd():

    df_zero_k_hot_hd = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
        'pairwise_sd_pd_zero_fd/network_pairs_with_zero_k_hot_hd.csv',
        dtype={'k_hot_code': str})
    for fid in ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17',
                '18', '19', '20']:
        print(fid)
        df_fid = pd.read_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' + fid +
            '_model_params.csv')
        print(len(df_fid))
        df_fid.loc[:, ['model_index']] = df_fid['gparam_index'].apply(lambda x: x.split('.')[1]).astype(np.int64)
        df_fid_grouped = df_fid.groupby(['model_index'])
        group_keys = df_fid_grouped.groups.keys()
        group_sizes = pd.DataFrame(df_fid_grouped.size(), columns=['group_size']).reset_index(names=['group_key'])
        df_pairs = pd.DataFrame(list(combinations(group_keys, 2)), columns=['Network1', 'Network2'])
        df_canalised_temp = df_pairs.merge(df_zero_k_hot_hd, on=['Network1', 'Network2'])

        for i in range(1, 10):
            df_sd = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                                'robustness_evolvability_plasticity_canalisation_analysis/'
                                'pairwise_sd_pd_zero_fd/network_pairs_hd_'+
                                str(i)+ '.csv', dtype={'Network1': np.int64, 'Network2': np.int64})

            df_canalised = df_canalised_temp.merge(df_sd, on=['Network1', 'Network2'])
            print(len(df_canalised))

            nckts_list = []
            for _, row in df_canalised.iterrows():

                nckt1 = group_sizes.loc[group_sizes['group_key'] == np.int64(row['Network1'])].group_size.values[0]
                nckt2 = group_sizes.loc[group_sizes['group_key'] == np.int64(row['Network2'])].group_size.values[0]
                nckts_list.append(nckt1 * nckt2)

            df_canalised['number_of_circuits'] = nckts_list
            df_canalised['Hamming_Distance'] = round(9 * (df_canalised['Hamming_Distance']))
            df_canalised.to_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                                'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/'
                                'canalization/fid'+fid+'_network_pairs_hd_'+str(i)+'.csv', header=True, index=None)

def get_number_of_canalised_circuits_by_fcat_hd(fcat):

    df_zero_k_hot_hd = pd.read_csv(
        '../../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
        'pairwise_sd_pd_zero_fd/network_pairs_with_zero_k_hot_hd.csv',
        dtype={'k_hot_code': str})

    df_fcat_ckt = pd.DataFrame()

    # Function Category I
    if fcat == 'I':
        flist = ['01', '02', '03', '04', '05', '06']
    # Function Category II
    if fcat == 'II':
        flist = ['08', '09', '11', '12', '14', '16', '17', '19']
    # Function Category III
    if fcat == 'III':
        flist = ['07', '13']
    # Function Category IV
    if fcat == 'IV':
        flist = ['20']
    # # Function Category V
    if fcat == 'V':
        flist = ['10', '15', '18']

    for fid in flist:
        print(fid)
        df_fid_temp = pd.read_csv(
            '../../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' +
            fid + '_model_params.csv')
        df_fid_temp.loc[:, ['model_index']] = df_fid_temp['gparam_index'].apply(lambda x: x.split('.')[1]
                                                                                ).astype(np.int64)
        df_fcat_ckt = pd.concat([df_fcat_ckt, df_fid_temp], axis=0).reset_index(drop=True)

    df_fid_grouped = df_fcat_ckt.groupby(['model_index'])
    group_keys = df_fid_grouped.groups.keys()
    group_sizes = pd.DataFrame(df_fid_grouped.size(), columns=['group_size']).reset_index(names=['group_key'])
    df_pairs = pd.DataFrame(list(combinations(group_keys, 2)), columns=['Network1', 'Network2'])
    df_canalised_temp = df_pairs.merge(df_zero_k_hot_hd, on=['Network1', 'Network2'])

    for i in range(1, 10):
        df_sd = pd.read_csv(
            '../../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
            'pairwise_sd_pd_zero_fd/network_pairs_hd_' + str(
                i) + '.csv', dtype={'Network1': np.int64, 'Network2': np.int64})

        df_canalised = df_canalised_temp.merge(df_sd, on=['Network1', 'Network2'])
        print(len(df_canalised))

        nckts_list = []
        for _, row in df_canalised.iterrows():

            nckt1 = group_sizes.loc[group_sizes['group_key'] == np.int64(row['Network1'])].group_size.values[0]
            nckt2 = group_sizes.loc[group_sizes['group_key'] == np.int64(row['Network2'])].group_size.values[0]
            nckts_list.append(nckt1 * nckt2)

        df_canalised['number_of_circuits'] = nckts_list
        df_canalised['Hamming_Distance'] = round(9 * (df_canalised['Hamming_Distance']))
        df_canalised.to_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
            'pairwise_sd_pd_zero_fd/canalization/fcat_wise/fcat_'+fcat+'_network_pairs_hd_' + str(
                i) + '.csv', header=True, index=None)

def plot_freq_of_canalised_circuits_vs_sd_for_fcat(fcat):

    freq_list = []
    for i in range(1, 10):
        df_temp = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                              'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/'
                              'canalization/fcat_wise/fcat_'+fcat+'_network_pairs_hd_'+str(i)+'.csv')
        freq_list.append(df_temp['number_of_circuits'].sum())

    df_data = pd.DataFrame(range(1, 10), columns=['Structural Diversity'])
    df_data['Number of canalised circuit pairs'] = freq_list
    df_data.to_csv('../../data/integrated_results_v0_v1_v2/csvs/'
                   'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/canalization/'
                   'fcat_wise/fcat_'+fcat+'_sd_vs_ncanalised_ckt_pairs.csv', header=True, index=None)
    plt.figure()
    sns.barplot(data=df_data, x='Structural Diversity', y='Number of canalised circuit pairs', color='#E4C0C0')

    plt.xlabel('Structural Diversity', fontsize=18)
    plt.ylabel('Number of canalised circuit pairs', fontsize=18)
    plt.tight_layout()
    plt.show()

def plot_freq_of_canalised_circuits_vs_sd_overall():
    freq_list = []

    for i in range(1, 10):
        df_fcat = pd.DataFrame()
        for fcat in ['I', 'II', 'III', 'IV', 'V']:
            df_temp = pd.read_csv(
                '../../data/integrated_results_v0_v1_v2/csvs/'
                'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/'
                'canalization/fcat_wise/fcat_' + fcat + '_network_pairs_hd_' + str(
                    i) + '.csv')
            df_fcat = pd.concat([df_fcat, df_temp], axis=0)

        freq_list.append(df_temp['number_of_circuits'].sum())
    df_data = pd.DataFrame(range(1, 10), columns=['Structural Diversity'])
    df_data['Number of canalised circuit pairs'] = freq_list
    df_data.to_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/'
        'pairwise_sd_pd_zero_fd/canalization/fcat_wise/overall_fcat_sd_vs_ncanalised_ckt_pairs.csv',
        header=True, index=None)
    plt.figure()
    sns.barplot(data=df_data, x='Structural Diversity', y='Number of canalised circuit pairs', color='#E4C0C0')

    plt.xlabel('Structural Diversity', fontsize=18)
    plt.ylabel('Number of canalised circuit pairs', fontsize=18)
    plt.tight_layout()
    plt.show()

split_networkpairs_by_sd()
get_number_of_canalised_circuits_by_fid_hd()
for fcat in ['I', 'II', 'III', 'IV', 'V']:
    get_number_of_canalised_circuits_by_fcat_hd(fcat)

plot_freq_of_canalised_circuits_vs_sd_for_fcat(fcat)
plot_freq_of_canalised_circuits_vs_sd_overall()