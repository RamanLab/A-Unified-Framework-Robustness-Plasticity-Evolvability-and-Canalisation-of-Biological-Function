import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def min_max_scaling(df_conc):

    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

def plot_conc_vs_time(df_data, name_of_index_column):

    time_start = 0
    time_end = 100
    time_steps = 1
    t = np.linspace(time_start, time_end, int(((time_end - time_start) / time_steps)) + 1)

    df_data = df_data.set_index(name_of_index_column)
    df_data = min_max_scaling(df_data)

    plt.plot(t, df_data.T)
    plt.xlabel("Time")
    plt.ylabel("Normalized Concentration")
    plt.show()

def plot_conc_vs_time_in_dataset_one_by_one(df_data, name_of_index_column):

    time_start = 0
    time_end = 100
    time_steps = 1
    t = np.linspace(time_start, time_end, int(((time_end - time_start) / time_steps)) + 1)

    df_data = df_data.set_index(name_of_index_column)
    df_data = min_max_scaling(df_data)
    df_data = df_data.T

    cols = df_data.columns.values.tolist()
    for i in range(len(df_data.T)):
        plt.figure()

        plt.plot(t, df_data.iloc[:, i], linewidth=3)
        plt.xlabel("Time")
        plt.ylabel("Normalized Concentration")
        plt.legend(cols[i:], fontsize=18)
        plt.xticks([])
        plt.yticks([])
        plt.show()


function_to_call = 'plot_conc_vs_time_in_dataset_one_by_one'
# file = '../../../data/integrated_results_v0_v1_v2/csvs/overall_barycenters_v2_0_and_v2_1_and_v2_2.csv'
file = '/home/user/PycharmProjects/data/integrated_results_v2_0_v2_1_v2_2/csvs/overall_barycenters_v2_0_and_v2_1_and_v2_2.csv'
name_of_index_column = 'function_id'
df = pd.read_csv(file, dtype={name_of_index_column:str})
globals()[function_to_call](df, name_of_index_column)