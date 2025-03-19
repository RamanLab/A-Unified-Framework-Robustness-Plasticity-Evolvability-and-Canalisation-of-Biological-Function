import pandas as pd
from scipy.spatial.distance import cdist, squareform
import itertools
import numpy as np

def get_parametric_diversity(id, sampled_id):

    df_temp0 = pd.read_csv('../../data/v0/dataset'+str(sampled_id)+'_lhs/input_sim_data/dataset_model'+str(id)+'.csv', dtype={'param_index': str})
    df_temp0.loc[:, ['gparam_index']] = df_temp0['param_index'].apply(lambda x: '0.' + x)
    df_temp0 = df_temp0.drop(columns='param_index')
    df_temp1 = pd.read_csv('../../data/v1/dataset'+str(sampled_id)+'_lhs/input_sim_data/dataset_model'+str(id)+'.csv', dtype={'param_index': str})
    df_temp1.loc[:, ['gparam_index']] = df_temp1['param_index'].apply(lambda x: '1.' + x)
    df_temp1 = df_temp1.drop(columns='param_index')
    df_temp2 = pd.read_csv('../../data/v2/dataset'+str(sampled_id)+'_lhs/input_sim_data/dataset_model'+str(id)+'.csv', dtype={'param_index': str})
    df_temp2.loc[:, ['gparam_index']] = df_temp2['param_index'].apply(lambda x: '2.' + x)
    df_temp2 = df_temp2.drop(columns='param_index')

    df_temp = pd.concat([df_temp0, df_temp1, df_temp2], axis=0).reset_index(drop=True)
    ckt_pairs = list(itertools.combinations(df_temp['gparam_index'], 2))
    df_ckt_pairs = pd.DataFrame(ckt_pairs, columns=['circuit_index1', 'circuit_index2'])

    df_temp = df_temp.set_index('gparam_index')
    df_temp = df_temp.drop(columns=['x[0]', 'x[1]', 'x[2]', 'nI', 'KI', 'v0', 'v1', 'v2'])
    df_distance = cdist(df_temp.to_numpy(), df_temp.to_numpy(), metric='euclidean')
    df_distance = squareform(df_distance)
    df_ckt_pairs['distance'] = df_distance.astype(np.float32)

    return df_ckt_pairs