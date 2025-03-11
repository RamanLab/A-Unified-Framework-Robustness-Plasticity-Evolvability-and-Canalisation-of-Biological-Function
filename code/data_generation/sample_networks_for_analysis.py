import numpy as np
import pandas as pd


def sample_networks(df_adj_mat, num_samples, df_adj_mat_already_sampled):
    num_vars = len(df_adj_mat.T)
    samples = set()

    df_edge_probab = pd.DataFrame(columns=['AA', 'AB', 'AC', 'BA', 'BB', 'BC', 'CA', 'CB', 'CC'])

    aa = df_adj_mat.iloc[:, 0].value_counts()
    df_edge_probab['AA'] = aa
    ab = df_adj_mat.iloc[:, 1].value_counts()
    df_edge_probab['AB'] = ab
    ac = df_adj_mat.iloc[:, 2].value_counts()
    df_edge_probab['AC'] = ac
    ba = df_adj_mat.iloc[:, 3].value_counts()
    df_edge_probab['BA'] = ba
    bb = df_adj_mat.iloc[:, 4].value_counts()
    df_edge_probab['BB'] = bb
    bc = df_adj_mat.iloc[:, 5].value_counts()
    df_edge_probab['BC'] = bc
    ca = df_adj_mat.iloc[:, 6].value_counts()
    df_edge_probab['CA'] = ca
    cb = df_adj_mat.iloc[:, 7].value_counts()
    df_edge_probab['CB'] = cb
    cc = df_adj_mat.iloc[:, 8].value_counts()
    df_edge_probab['CC'] = cc

    df_edge_probab = df_edge_probab.sort_index(ascending=True)
    df_edge_probab = df_edge_probab / len(df_adj_mat)

    model_indices = []

    while (len(samples) < num_samples):
        sample = ''
        for i in range(num_vars):
            value = np.random.choice([2, 0, 1], p=df_edge_probab.iloc[:, i])
            sample += str(value)
        sample1 = list(map(int, sample))
        sample1 = [-1 if s == 2 else s for s in sample1]
        idx = df_adj_mat[(df_adj_mat[:] == sample1).all(1)].index.tolist()
        rep = 0
        # Check if the sampled network is already a part of previous sets of networks
        if idx in df_adj_mat_already_sampled['model_index'].values:
            rep = 1
        # The new set of sampled networks are disjoint from other sampled sets
        if len(idx) != 0 and rep == 0:
            samples.add(sample)
            model_indices.append(idx)

    return samples, model_indices

# Get the adjacency matrices of all the networks (after filtering out the ones that are
# not connected directly or indirectly from input to output). There are 16038 such networks
df_adj_mat = pd.read_csv('../../data/common/adjacency_matrix_file.csv', header=None)
sample_id_to_generate = 0

# To divide the total of 16038 networks into 10 sets, we take 1604 samples for the first 9 sets
# and 1602 samples for the 10th set
if sample_id_to_generate < 9:
    num_samples = 1604
else:
    num_samples = 1602

df_adj_mat1 = pd.DataFrame()
df_adj_mat2 = pd.DataFrame()
df_adj_mat3 = pd.DataFrame()
df_adj_mat4 = pd.DataFrame()
df_adj_mat5 = pd.DataFrame()
df_adj_mat6 = pd.DataFrame()
df_adj_mat7 = pd.DataFrame()
df_adj_mat8 = pd.DataFrame()
df_adj_mat9 = pd.DataFrame()

if sample_id_to_generate == 1:
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
elif sample_id_to_generate == 2:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
elif sample_id_to_generate == 3:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)

elif sample_id_to_generate == 4:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)


elif sample_id_to_generate == 5:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)
    df_adj_mat5 = pd.read_csv('lhs_models_sampled_for_analysis4.csv', header=0)

elif sample_id_to_generate == 6:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)
    df_adj_mat5 = pd.read_csv('lhs_models_sampled_for_analysis4.csv', header=0)
    df_adj_mat6 = pd.read_csv('lhs_models_sampled_for_analysis5.csv', header=0)

elif sample_id_to_generate == 7:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)
    df_adj_mat5 = pd.read_csv('lhs_models_sampled_for_analysis4.csv', header=0)
    df_adj_mat6 = pd.read_csv('lhs_models_sampled_for_analysis5.csv', header=0)
    df_adj_mat7 = pd.read_csv('lhs_models_sampled_for_analysis6.csv', header=0)

elif sample_id_to_generate == 8:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)
    df_adj_mat5 = pd.read_csv('lhs_models_sampled_for_analysis4.csv', header=0)
    df_adj_mat6 = pd.read_csv('lhs_models_sampled_for_analysis5.csv', header=0)
    df_adj_mat7 = pd.read_csv('lhs_models_sampled_for_analysis6.csv', header=0)
    df_adj_mat8 = pd.read_csv('lhs_models_sampled_for_analysis7.csv', header=0)

elif sample_id_to_generate == 9:
    # Already sampled networks
    df_adj_mat1 = pd.read_csv('lhs_models_sampled_for_analysis0.csv', header=0)
    df_adj_mat2 = pd.read_csv('lhs_models_sampled_for_analysis1.csv', header=0)
    df_adj_mat3 = pd.read_csv('lhs_models_sampled_for_analysis2.csv', header=0)
    df_adj_mat4 = pd.read_csv('lhs_models_sampled_for_analysis3.csv', header=0)
    df_adj_mat5 = pd.read_csv('lhs_models_sampled_for_analysis4.csv', header=0)
    df_adj_mat6 = pd.read_csv('lhs_models_sampled_for_analysis5.csv', header=0)
    df_adj_mat7 = pd.read_csv('lhs_models_sampled_for_analysis6.csv', header=0)
    df_adj_mat8 = pd.read_csv('lhs_models_sampled_for_analysis7.csv', header=0)
    df_adj_mat9 = pd.read_csv('lhs_models_sampled_for_analysis8.csv', header=0)

    df_adj_mat_already_sampled = pd.concat([df_adj_mat1, df_adj_mat2, df_adj_mat3, df_adj_mat4, df_adj_mat5,
                                            df_adj_mat6, df_adj_mat7, df_adj_mat8, df_adj_mat9],
                                           axis=0).reset_index(drop=True)

samples, model_indices = sample_networks(df_adj_mat, num_samples, df_adj_mat_already_sampled)

if len(samples) == len(model_indices):
    model_indices = sorted(model_indices)
else:
    mat_samples = [list(map(int, sample)) for sample in samples]
    df_mat_samples = pd.DataFrame(mat_samples)
    df_mat_samples = df_mat_samples.replace({2: -1})

    model_indices = []
    for i in range(len(df_mat_samples)):
        sample = df_mat_samples.iloc[i, :]
        idx = df_adj_mat[(df_adj_mat[:] == sample).all(1)].index.tolist()
        if len(idx) != 0:
            model_indices.append(*idx)
    model_indices = sorted(model_indices)

df_model_indices = pd.DataFrame()
df_model_indices['model_index'] = model_indices
df_model_indices.to_csv('../../data/common/lhs_models_sampled_for_analysis9.csv', header=True, index=False)