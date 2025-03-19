import pandas as pd



def get_functional_cluster_size(df_data):

    df_data.loc[:, ['model']] = df_data['param_index'].apply(lambda x: x.split('.')[0])
    df_data.loc[:, ['param_index']] = df_data['param_index'].apply(lambda x: x.split('.')[1])

    ncircuits = len(df_data)
    nmodels = len(df_data.model.unique())

    netk_list = []
    nparam_list = []
    for netk in df_data.model.unique():
        df_param = df_data.loc[df_data['model'] == netk]
        netk_list.append(netk)
        nparam_list.append(len(df_param))
    nparam_per_netk = pd.DataFrame()
    nparam_per_netk['model'] = netk_list
    nparam_per_netk['number_of_parameters'] = nparam_list

    return ncircuits, nmodels, nparam_per_netk

baryid = []
ncircuits_list = []
nmodels_list = []
nfunc = 18
version = '2'

df_text = pd.read_csv('../../data/v'+version+'/csvs/combined0_9/text_id_desc.csv')

for i in range(nfunc):
    df_data = pd.read_csv('../../data/v'+version+'/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(i) +'_model_params.csv', dtype={'param_index': str})
    ncircuits, nmodels, df_nparam_per_netk = get_functional_cluster_size(df_data)
    df_nparam_per_netk.to_csv('../../data/v'+version+'/csvs/combined0_9/parameter_count_per_model_fcluster'+str(i)+'.csv', header=True, index=None)
    baryid.append(i)
    ncircuits_list.append(ncircuits)
    nmodels_list.append(nmodels)

df_fcluster_sizes = pd.DataFrame()
df_fcluster_sizes['bary_id'] = baryid
df_fcluster_sizes['number_of_circuits'] = ncircuits_list
df_fcluster_sizes['number_of_networks'] = nmodels_list
df_fcluster_sizes['text_id'] = df_text.text_id.values
df_fcluster_sizes = df_fcluster_sizes.sort_values(by='number_of_circuits', ascending=False)
df_fcluster_sizes.index = [f'{i+1:02d}' for i in range(len(df_fcluster_sizes))]
df_fcluster_sizes.to_csv('../../data/v'+version+'/csvs/combined0_9/func_id_bary_id_text_id.csv', header=True, index=True, index_label='function_id')