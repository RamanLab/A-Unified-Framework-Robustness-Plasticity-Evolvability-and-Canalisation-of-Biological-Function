import pandas as pd
import itertools
import os
import time

def split_files_networkwise_for_zero_sd(input_file, file_data_type):
    # Load the dataset
    df_func_cat = pd.read_csv(input_file)

    # Extract the 'model_index' from 'circuit_index'
    df_func_cat['model_index'] = df_func_cat['circuit_index'].str.split('.').str[1]

    # Create the output directory if it doesn't exist
    output_dir = '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/' \
                 'pairwise_pd_fd_zero_sd/networkwise_circuits/'
    os.makedirs(output_dir, exist_ok=True)

    # Group the DataFrame by 'model_index'
    grouped = df_func_cat.groupby('model_index')

    # Write each group to a separate CSV file
    for model_index, group in grouped:
        print(model_index)
        file_path = os.path.join(output_dir, f'function_{file_data_type}_model{model_index}.csv')

        # Writing to CSV without checking if the file exists
        group.to_csv(file_path, header=True, index=False)

def split_files_fclusterwise_for_zero_fd():

    for fid in ['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07', '06', '05', '04',
                '03', '02', '01']:

        start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
        print("Jobs start time = ", start_time)

        output_dir = '../../data/integrated_results_v0_v1_v2/csvs/' \
                     'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/' \
                     'networkwise_circuits/fid' + fid + '/'

        df_ckts = pd.read_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' + fid +
            '_model_params.csv')

        df_ckts.loc[:, ['version']] = df_ckts['gparam_index'].apply(lambda x: x.split('.')[0])
        df_ckts.loc[:, ['network']] = df_ckts['gparam_index'].apply(lambda x: x.split('.')[1])
        df_ckts.loc[:, ['gparam_index']] = df_ckts['gparam_index'].apply(lambda x: x.split('.', 1)[1])

        netk_list = df_ckts.network.unique()

        count = 0
        for netk in netk_list:
            count = count + 1
            print(str(count) + ' of ' + str(len(netk_list)))
            df_temp = df_ckts[df_ckts['network'] == netk]
            df_temp = df_temp.drop(columns='network')
            df_temp.to_csv(output_dir+'final_func_cluster' + fid + '_model'+str(netk)+'.csv', header=True, index=None)

        end_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
        print("Jobs end time = ", end_time)

def split_files_networkwise_for_zero_fd(arg1):

    df_ckts = pd.read_csv \
        ('../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' + arg1 +
         '_model_params.csv')

    df_ckts.loc[:, ['version']] = df_ckts['gparam_index'].apply(lambda x: x.split('.')[0])
    df_ckts.loc[:, ['network']] = df_ckts['gparam_index'].apply(lambda x: x.split('.')[1])
    df_ckts.loc[:, ['gparam_index']] = df_ckts['gparam_index'].apply(lambda x: x.split('.', 1)[1])
    df_ckts = df_ckts.drop(columns=['version', 'gparam_index'])
    df_ckts = df_ckts.drop_duplicates().reset_index(drop=True)

    # **********************************************

    df_pairs = list(itertools.combinations(df_ckts['network'], 2))
    df_pairs = pd.DataFrame(df_pairs, columns=['network1', 'network2'])
    df_pairs_grouped = df_pairs.groupby(['network1'])

    print('Number of networks:', df_pairs_grouped.ngroups)
    tot_pairs = df_pairs_grouped.ngroups * (df_pairs_grouped.ngroups - 1) / 2
    print('Total pairs:', tot_pairs)

    df_pairs_grouped = [(id, group) for id, group in df_pairs_grouped]

    start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
    print("Jobs start time = ", start_time)

    for netk1, group in df_pairs_grouped:

        dataset_filename = '../../data/integrated_results_v0_v1_v2/csvs/' \
                           'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/' \
                           'pairwise_sd_pd_fid' + str(arg1) + '/pairwise_sd_pd_fid' + str(arg1) + '_model' + \
                           str(netk1[0]) + '.csv'
        file_exists = os.path.isfile(dataset_filename)
        if file_exists:
            continue
        print(netk1[0])
        file_path = '../../data/integrated_results_v0_v1_v2/csvs/' \
                    'robustness_evolvability_plasticity_canalisation_analysis/pairwise_sd_pd_zero_fd/groups' + \
                    str(arg1) + '/' + str(netk1[0]) + '.csv'
        group.to_csv(file_path, header=True, index=False)

    end_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
    print("Jobs end time = ", end_time)




# Split the file containing function category codes for all circuits into network-wise files containing function
# category codes for circuits sharing a particular network
input_file1 = '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/' \
              'circuitwise_function_category_codes.csv'
file_data_type1 = 'category_codes'
split_files_networkwise_for_zero_sd(input_file1, file_data_type1)

# Split the file containing the function codes for all circuits into network-wise files containing function
# codes for circuits sharing a particular network
input_file2 = '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/' \
              'circuitwise_function_codes.csv'
file_data_type2 = 'codes'
split_files_networkwise_for_zero_sd(input_file2, file_data_type2)

# Split the file containing the circuits in a functional cluster into network-wise files containing circuits that share
# the same network for a particular functional cluster
split_files_fclusterwise_for_zero_fd()

for fid in ['20', '19', '18', '17', '16', '15', '14', '13', '12', '11', '10', '09', '08', '07', '06', '05', '04',
                '03', '02', '01']:
    split_files_networkwise_for_zero_fd(fid)