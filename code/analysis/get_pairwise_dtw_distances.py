import pandas as pd
from dtaidistance import dtw

version_id1 = '0'
version_id2 = '1'

df_conc1 = pd.read_csv('../../data/v'+version_id1+'/csvs/combined0_9/barycenter2_v'+version_id1+'_combined0_9.csv', dtype={'param_index': str})
df1 = df_conc1.drop(columns='param_index')

df_conc2 = pd.read_csv('../../data/v'+version_id2+'/csvs/combined0_9/barycenter2_v'+version_id2+'_combined0_9.csv', dtype={'param_index': str})
df2 = df_conc2.drop(columns='param_index')


def min_max_scaling(df_conc):

    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

df1 = min_max_scaling(df1)
df2 = min_max_scaling(df2)

param_id1_list = []
param_id2_list = []
distance_list = []
for i in range(len(df1)):
    for j in range(len(df2)):
        distance = dtw.distance_fast(df1.iloc[i, :].to_numpy(), df2.iloc[j, :].to_numpy())
        param_id1_list.append(df_conc1.iloc[i].param_index)
        param_id2_list.append(df_conc2.iloc[j].param_index)
        distance_list.append(distance)

df_output = pd.DataFrame()
df_output['param_index1'] = param_id1_list
df_output['param_index2'] = param_id2_list
df_output['DTW_distance'] = distance_list

df_output.to_csv('../../data/integrated_results_v0_v1_v2/csvs/pairwise_barycenter_distances/pairwise_distances_barycenter2_v'+version_id1+'_and_v'+version_id2+'.csv', header=True, index=None)


