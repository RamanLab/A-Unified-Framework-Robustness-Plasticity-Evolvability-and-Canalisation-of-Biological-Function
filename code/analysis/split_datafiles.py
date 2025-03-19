import pandas as pd
import itertools
import os
import time

def split_files_networkwise_for_zero_sd():
    # Load the dataset
    df_func_cat = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/circuitwise_function_category_codes.csv')

    # Extract the 'model_index' from 'circuit_index'
    df_func_cat['model_index'] = df_func_cat['circuit_index'].str.split('.').str[1]

    # Create the output directory if it doesn't exist
    output_dir = '../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_analysis/pairwise_pd_fd_zero_sd/networkwise_circuits/'
    os.makedirs(output_dir, exist_ok=True)

    # Group the DataFrame by 'model_index'
    grouped = df_func_cat.groupby('model_index')

    # Write each group to a separate CSV file
    for model_index, group in grouped:
        print(model_index)
        file_path = os.path.join(output_dir, f'function_category_codes_model{model_index}.csv')

        # Writing to CSV without checking if the file exists
        group.to_csv(file_path, header=True, index=False)