import pandas as pd
import numpy as np
from scipy.spatial.distance import pdist


def get_hamming_dist(X):
    hamm_dist = pdist(X, 'hamming')
    return hamm_dist[0]

def get_pairwise_hamming_distance_all_networks():
    adjacency_mat_list = pd.read_csv('../../data/common/adjacency_matrix_file.csv', header=None)
    adjacency_mat_list = [row.reshape(3,3) for row in adjacency_mat_list.values]
    nmodels = len(adjacency_mat_list)
    ind = np.triu_indices(nmodels, 1)
    netk_id1 = []
    netk_id2 = []
    dist_list = []

    for i, j in zip(ind[0], ind[1]):
        dist = get_hamming_dist([adjacency_mat_list[i].flatten(), adjacency_mat_list[j].flatten()])
        netk_id1.append(i)
        netk_id2.append(j)
        dist_list.append(dist)

    df = pd.DataFrame()
    df['Network1'] = netk_id1
    df['Network2'] = netk_id2
    df['Hamming Distance'] = dist_list
    df = df.sort_values(by='Hamming Distance')

    return df

df_pairwise_hamming_distance = get_pairwise_hamming_distance_all_networks()
df_pairwise_hamming_distance.to_csv('../../data/common/hamming_distance_all_networks.csv', header=True, index=None)