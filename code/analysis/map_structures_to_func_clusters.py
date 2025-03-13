import pandas as pd

version_id = '2'
df_func_labels2 = pd.read_csv('../../data/v'+version_id+'/csvs/combined0_9/fun_labels_v2_combined0_9.csv', header=0, dtype={'param_index': str})

label2_list = sorted(df_func_labels2.label.unique())
for label2 in label2_list:
    model_paramid_list = []
    df_temp1 = df_func_labels2.loc[df_func_labels2['label']==label2]
    split_result = df_temp1['param_index'].str.split('.', n=1, expand=True)
    df_temp1.loc[:, ['sampled_dataset_id']] = split_result.iloc[:, 0].apply(lambda x: x[1])
    df_temp1.loc[:, ['label1']] = split_result.iloc[:, 1].apply(lambda x: x[3:])
    df_temp1 = df_temp1.astype({'label1': int})
    for temp1 in df_temp1.sampled_dataset_id.unique():
        label1_list = df_temp1.loc[df_temp1['sampled_dataset_id']==temp1].label1
        df_data1 = pd.read_csv('../../data/v'+version_id+'/csvs/sampled_dataset'+ str(temp1) +'/functional_cluster_labels/fun_cluster_labels0_barycenter0_sampled_dataset'+ str(temp1) +'.csv', dtype={'param_index': str})
        label0_list = df_data1.loc[df_data1['label'].isin(label1_list)].param_index
        df_temp2 = pd.DataFrame(label0_list)
        df_temp2.loc[:, ['model']] = df_temp2['param_index'].apply(lambda x: x.split('.')[0])
        df_temp2.loc[:, ['cluster_label']] = df_temp2['param_index'].apply(lambda x: x.split('.')[1])
        df_temp2 = df_temp2.astype({'model': int, 'cluster_label': int})

        for model in df_temp2.model.unique():
            model_paramid_list_temp = []
            label_list = df_temp2.loc[df_temp2['model'] == model].cluster_label
            df_model_param = pd.read_csv('../../data/v'+version_id+'/csvs/sampled_dataset'+ str(temp1) +'/cluster_labels/cluster_label_model'+ str(model) + '.csv', dtype={'param_index': str})
            model_paramid_list_temp = df_model_param.loc[df_model_param['label'].isin(label_list)].param_index
            model_paramid_list.extend(model_paramid_list_temp)
    df_model_paramid = pd.DataFrame()
    df_model_paramid['param_index'] = model_paramid_list
    df_model_paramid.to_csv('../../data/v'+version_id+'/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(label2) + '_model_params.csv', header=True, index=None)
