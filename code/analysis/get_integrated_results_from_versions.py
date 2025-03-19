import pandas as pd
from tslearn.barycenters import softdtw_barycenter
import matplotlib.pyplot as plt
from upsetplot import UpSet, from_contents
import operator as op


def min_max_scaling(df_conc):

    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

def get_union_of_functions_from_different_versions():

    df_text0 = pd.read_csv('../../data/v0/csvs/combined0_9/text_id_desc.csv')
    df_text1 = pd.read_csv('../../data/v1/csvs/combined0_9/text_id_desc.csv')
    df_text2 = pd.read_csv('../../data/v2/csvs/combined0_9/text_id_desc.csv')

    df_text_merged = pd.merge(df_text0, df_text1, how='outer')
    df_text_merged = pd.merge(df_text_merged, df_text2, how='outer')
    df_text_merged.to_csv('../../data/integrated_results_v0_v1_v2/csvs/text_id_desc.csv', header=True, index=None)

def get_fcluster_sizes_bary_id_text_id_maps_after_merge_across_versions():

    df_text0 = pd.read_csv('../../data/v0/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text1 = pd.read_csv('../../data/v1/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text2 = pd.read_csv('../../data/v2/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})

    df_text = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/text_id_desc.csv')

    final_nckt = []
    final_nnetk = []
    desc_list = []

    text_set0 = df_text0.text_id.unique()
    text_set1 = df_text1.text_id.unique()
    text_set2 = df_text2.text_id.unique()

    for i in range(len(df_text)):

        df_temp0 = pd.DataFrame()
        df_temp1 = pd.DataFrame()
        df_temp2 = pd.DataFrame()
        nckt_fc0 = 0
        nckt_fc1 = 0
        nckt_fc2 = 0
        desc = df_text.iloc[i].text_id

        if desc in text_set0:
            bary_id0 = df_text0.loc[df_text0['text_id'] == desc].bary_id.values[0]
            df_temp0 = pd.read_csv('../../data/v0/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(bary_id0) +'_model_params.csv', dtype={'param_index': str})
            nckt_fc0 = len(df_temp0)
            df_temp0.loc[:, ['model']] = df_temp0['param_index'].apply(lambda x: x.split('.')[0])
            df_temp0 = df_temp0.drop(columns='param_index')

        if desc in text_set1:
            bary_id1 = df_text1.loc[df_text1['text_id'] == desc].bary_id.values[0]
            df_temp1 = pd.read_csv('../../data/v1/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(bary_id1) + '_model_params.csv', dtype={'param_index': str})
            nckt_fc1 = len(df_temp1)
            df_temp1.loc[:, ['model']] = df_temp1['param_index'].apply(lambda x: x.split('.')[0])
            df_temp1 = df_temp1.drop(columns='param_index')

        if desc in text_set2:
            bary_id2 = df_text2.loc[df_text2['text_id'] == desc].bary_id.values[0]
            df_temp2 = pd.read_csv('../../data/v2/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(bary_id2) + '_model_params.csv', dtype={'param_index': str})
            nckt_fc2 = len(df_temp2)
            df_temp2.loc[:, ['model']] = df_temp2['param_index'].apply(lambda x: x.split('.')[0])
            df_temp2 = df_temp2.drop(columns='param_index')

        df_netks = pd.concat([df_temp0, df_temp1, df_temp2], axis=0).reset_index(drop=True)

        nnetks = len(df_netks.model.unique())

        desc_list.append(desc)
        final_nckt.append(nckt_fc0 + nckt_fc1 + nckt_fc2)
        final_nnetk.append(nnetks)

    df_fcsize = pd.DataFrame()
    df_fcsize['text_id'] = desc_list
    df_fcsize['number_of_circuits'] = final_nckt
    df_fcsize['number_of_networks'] = final_nnetk
    df_fcluster_sizes = df_fcsize.sort_values(by='number_of_circuits', ascending=False)
    df_fcluster_sizes.index = [f'{i + 1:02d}' for i in range(len(df_fcluster_sizes))]
    df_fcsize.to_csv('../../data/integrated_results_v2_0_v2_1_v2_2/csvs/func_id_bary_id_text_id.csv', header=True, index=None)

def get_overall_barycenter():

    df_text = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/text_id_desc.csv')
    df_text_id_fid = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/func_id_bary_id_text_id.csv', dtype={'function_id': str})

    df_text0 = pd.read_csv('../../data/v0/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text1 = pd.read_csv('../../data/v1/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text2 = pd.read_csv('../../data/v2/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})

    text_set0 = df_text0.text_id.unique()
    text_set1 = df_text1.text_id.unique()
    text_set2 = df_text2.text_id.unique()

    df_bary0 = pd.read_csv('../../data/v0/csvs/combined0_9/barycenter2_v0_combined0_9.csv')
    df_bary0 = df_bary0.set_index('param_index')

    df_bary1 = pd.read_csv('../../data/v1/csvs/combined0_9/barycenter2_v1_combined0_9.csv')
    df_bary1 = df_bary1.set_index('param_index')

    df_bary2 = pd.read_csv('../../data/v2/csvs/combined0_9/barycenter2_v2_combined0_9.csv')
    df_bary2 = df_bary2.set_index('param_index')

    df_bary0 = min_max_scaling(df_bary0)
    df_bary1 = min_max_scaling(df_bary1)
    df_bary2 = min_max_scaling(df_bary2)
    barycenter_list = []
    fid_list = []

    for i in range(len(df_text)):
        df_temp0 = pd.DataFrame()
        df_temp1 = pd.DataFrame()
        df_temp2 = pd.DataFrame()

        textid = df_text.iloc[i].text_id

        if textid in text_set0:
            bary_id0 = df_text0.loc[df_text0['text_id'] == textid].bary_id.values[0]
            df_temp0 = df_bary0.loc[df_bary0.index == 'b.f' + str(bary_id0)]

        if textid in text_set1:
            bary_id1 = df_text1.loc[df_text1['text_id'] == textid].bary_id.values[0]
            df_temp1 = df_bary1.loc[df_bary1.index == 'b.f' + str(bary_id1)]

        if textid in text_set2:
            bary_id2 = df_text2.loc[df_text2['text_id'] == textid].bary_id.values[0]
            df_temp2 = df_bary2.loc[df_bary2.index == 'b.f' + str(bary_id2)]

        df_bary = pd.concat([df_temp0, df_temp1, df_temp2], axis=0).reset_index(drop=True)
        if len(df_bary) > 1:
            barycenter = softdtw_barycenter(df_bary, gamma=1.0, max_iter=50, tol=1e-3)
        else:
            barycenter = df_bary.values.transpose()
        fid = df_text_id_fid.loc[df_text_id_fid['text_id'] == textid].function_id.values[0]
        barycenter_list.append(barycenter.ravel())
        fid_list.append(fid)

    df_overall_barycenters = pd.DataFrame(barycenter_list)
    df_overall_barycenters['function_id'] = fid_list
    df_overall_barycenters.to_csv('../../data/integrated_results_v0_v1_v2/csvs/overall_barycenters_v0_and_v1_and_v2.csv', header=True, index=None)


def get_final_model_params_after_merge_across_versions():

    df_text0 = pd.read_csv('../../data/v0/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text1 = pd.read_csv('../../data/v1/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})
    df_text2 = pd.read_csv('../../data/v2/csvs/combined0_9/func_id_bary_id_text_id.csv', dtype={'function_id': str})

    df_text = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/text_id_desc.csv')
    df_text_id_fid = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/fcluster_sizes_func_id_text_id.csv.csv',
        dtype={'function_id': str})

    text_set0 = df_text0.text_id.unique()
    text_set1 = df_text1.text_id.unique()
    text_set2 = df_text2.text_id.unique()

    for i in range(len(df_text)):
        df_temp0 = pd.DataFrame()
        df_temp1 = pd.DataFrame()
        df_temp2 = pd.DataFrame()
        df_cicuits = pd.DataFrame()

        textid = df_text.iloc[i].text_id

        if textid in text_set0:
            bary_id0 = df_text0.loc[df_text0['text_id'] == textid].bary_id.values[0]
            df_temp0 = pd.read_csv(
                '../../data/v0/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(
                    bary_id0) + '_model_params.csv', dtype={'param_index': str})
            df_temp0.loc[:, ['gparam_index']] = df_temp0['param_index'].apply(lambda x: '0.' + x)
            df_temp0 = df_temp0.drop(columns=['param_index'])

        if textid in text_set1:
            bary_id1 = df_text1.loc[df_text1['text_id'] == textid].bary_id.values[0]
            df_temp1 = pd.read_csv(
                '../../data/v1/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(
                    bary_id1) + '_model_params.csv', dtype={'param_index': str})
            df_temp1.loc[:, ['gparam_index']] = df_temp1['param_index'].apply(lambda x: '1.' + x)
            df_temp1 = df_temp1.drop(columns=['param_index'])

        if textid in text_set2:
            bary_id2 = df_text2.loc[df_text2['text_id'] == textid].bary_id.values[0]
            df_temp2 = pd.read_csv(
                '../../data/v2/csvs/combined0_9/final_func_model_param_map/final_func_cluster' + str(
                    bary_id2) + '_model_params.csv', dtype={'param_index': str})
            df_temp2.loc[:, ['gparam_index']] = df_temp2['param_index'].apply(lambda x: '2.' + x)
            df_temp2 = df_temp2.drop(columns=['param_index'])

        df_cicuits = pd.concat([df_temp0, df_temp1, df_temp2], axis=0).reset_index(drop=True)
        fid = df_text_id_fid.loc[df_text_id_fid['text_id'] == textid].function_id.values[0]
        df_cicuits.to_csv(
            '../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' + fid + '_model_params.csv',
            header=True, index=None)

def get_netk_distribution_over_func_cluster_upset_plots():

    df_text_id_fid = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/fcluster_sizes_func_id_text_id.csv', dtype={'function_id': str})
    fcluster_dict = {}
    for fid_key in df_text_id_fid.function_id:
        df_func_cluster = pd.read_csv('../../data/integrated_results_v0_v1_v2/csvs/final_func_model_param_map/final_func_cluster' + fid_key + '_model_params.csv', dtype={'gparam_index': str})
        df_func_cluster.loc[:, ['model_index']] = df_func_cluster['gparam_index'].apply(lambda x: x.split('.')[1])
        df_func_cluster = df_func_cluster.drop(columns='gparam_index')
        df_func_cluster = df_func_cluster.drop_duplicates().reset_index(drop=True)
        fcluster_dict['F' + fid_key] = df_func_cluster.values[:, 0]

    fcluster = from_contents(fcluster_dict)
    fcluster_1func = pd.DataFrame()
    fcluster_2func = pd.DataFrame()
    fcluster_3func = pd.DataFrame()
    fcluster_4func = pd.DataFrame()
    fcluster_5func = pd.DataFrame()
    fcluster_6func = pd.DataFrame()
    fcluster_7func = pd.DataFrame()
    fcluster_8func = pd.DataFrame()
    fcluster_9func = pd.DataFrame()
    fcluster_10func = pd.DataFrame()
    fcluster_11func = pd.DataFrame()
    fcluster_12func = pd.DataFrame()
    fcluster_13func = pd.DataFrame()
    fcluster_14func = pd.DataFrame()
    fcluster_15func = pd.DataFrame()
    fcluster_16func = pd.DataFrame()
    fcluster_17func = pd.DataFrame()
    fcluster_18func = pd.DataFrame()
    fcluster_19func = pd.DataFrame()
    fcluster_20func = pd.DataFrame()

    id1 = []
    id2 = []
    id3 = []
    id4 = []
    id5 = []
    id6 = []
    id7 = []
    id8 = []
    id9 = []
    id10 = []
    id11 = []
    id12 = []
    id13 = []
    id14 = []
    id15 = []
    id16 = []
    id17 = []
    id18 = []
    id19 = []
    id20 = []

    for i in range(len(fcluster)):
        fcluster_list = list(fcluster.index.values[i])
        num_true = op.countOf(fcluster_list, True)
        if num_true == 1:
            id1.append(i)
        elif num_true == 2:
            id2.append(i)
        elif num_true == 3:
            id3.append(i)
        elif num_true == 4:
            id4.append(i)
        elif num_true == 5:
            id5.append(i)
        elif num_true == 6:
            id6.append(i)
        elif num_true == 7:
            id7.append(i)
        elif num_true == 8:
            id8.append(i)
        elif num_true == 9:
            id9.append(i)
        elif num_true == 10:
            id10.append(i)
        elif num_true == 11:
            id11.append(i)
        elif num_true == 12:
            id12.append(i)
        elif num_true == 13:
            id13.append(i)
        elif num_true == 14:
            id14.append(i)
        elif num_true == 15:
            id15.append(i)
        elif num_true == 16:
            id16.append(i)
        elif num_true == 17:
            id17.append(i)
        elif num_true == 18:
            id18.append(i)
        elif num_true == 19:
            id19.append(i)
        elif num_true == 20:
            id20.append(i)

    fcluster_1func = fcluster.iloc[id1]
    fcluster_2func = fcluster.iloc[id2]
    fcluster_3func = fcluster.iloc[id3]
    fcluster_4func = fcluster.iloc[id4]
    fcluster_5func = fcluster.iloc[id5]
    fcluster_6func = fcluster.iloc[id6]
    fcluster_7func = fcluster.iloc[id7]
    fcluster_8func = fcluster.iloc[id8]
    fcluster_9func = fcluster.iloc[id9]
    fcluster_10func = fcluster.iloc[id10]
    fcluster_11func = fcluster.iloc[id11]
    fcluster_12func = fcluster.iloc[id12]
    fcluster_13func = fcluster.iloc[id13]
    fcluster_14func = fcluster.iloc[id14]
    fcluster_15func = fcluster.iloc[id15]
    fcluster_16func = fcluster.iloc[id16]
    fcluster_17func = fcluster.iloc[id17]
    fcluster_18func = fcluster.iloc[id18]
    fcluster_19func = fcluster.iloc[id19]
    fcluster_20func = fcluster.iloc[id20]


    fcluster_1func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_1function.csv',
                          header=True, index=True)
    fcluster_2func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_2function.csv',
                          header=True, index=True)
    fcluster_3func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_3function.csv',
                          header=True, index=True)
    fcluster_4func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_4function.csv',
                          header=True, index=True)
    fcluster_5func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_5function.csv',
                          header=True, index=True)
    fcluster_6func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_6function.csv',
                          header=True, index=True)
    fcluster_7func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_7function.csv',
                          header=True, index=True)
    fcluster_8func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_8function.csv',
                          header=True, index=True)
    fcluster_9func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_9function.csv',
                          header=True, index=True)
    fcluster_10func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_10function.csv',
                           header=True, index=True)
    fcluster_11func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_11function.csv',
                           header=True, index=True)
    fcluster_12func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_12function.csv',
                           header=True, index=True)
    fcluster_13func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_13function.csv',
                           header=True, index=True)
    fcluster_14func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_14function.csv',
                           header=True, index=True)
    fcluster_15func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_15function.csv',
                           header=True, index=True)
    fcluster_16func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_16function.csv',
                           header=True, index=True)
    fcluster_17func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_17function.csv',
                           header=True, index=True)
    fcluster_18func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_18function.csv',
                           header=True, index=True)
    fcluster_19func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_19function.csv',
                           header=True, index=True)
    fcluster_20func.to_csv('../../data/integrated_results_v0_v1_v2/csvs/distribution_of_network/fc_model_distribution_20function.csv',
                           header=True, index=True)

    # 'Single Function Network Distribution Across Functional Clusters'
    if len(fcluster_1func) > 0:
        ax_dict1 = UpSet(fcluster_1func, show_counts=True, sort_by='degree', shading_color=0.2, totals_plot_elements=15,
                         with_lines=True, show_percentages=False, subset_size='count', min_subset_size=1,
                         include_empty_subsets=False).plot()
        plt.show()

    # 'Two Function Network Distribution Across Functional Clusters'
    if len(fcluster_2func) > 0:
        ax_dict2 = UpSet(fcluster_2func, show_counts=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Three Function Network Distribution Across Functional Clusters'
    if len(fcluster_3func) > 0:
        ax_dict3 = UpSet(fcluster_3func, show_counts=True, sort_by='degree', shading_color=0.2,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Four Function Network Distribution Across Functional Clusters'
    if len(fcluster_4func) > 0:
        ax_dict4 = UpSet(fcluster_4func, show_counts=True, sort_by='degree', shading_color=0.2,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Five Function Network Distribution Across Functional Clusters'
    if len(fcluster_5func) > 0:
        ax_dict5 = UpSet(fcluster_5func, show_counts=True, sort_by='degree', shading_color=0.2,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Six Function Network Distribution Across Functional Clusters'
    if len(fcluster_6func) > 0:
        ax_dict6 = UpSet(fcluster_6func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=20,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Seven Function Network Distribution Across Functional Clusters'
    if len(fcluster_7func) > 0:
        ax_dict7 = UpSet(fcluster_7func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Eight Function Network Distribution Across Functional Clusters'
    if len(fcluster_8func) > 0:
        ax_dict8 = UpSet(fcluster_8func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Nine Function Network Distribution Across Functional Clusters'
    if len(fcluster_9func) > 0:
        ax_dict9 = UpSet(fcluster_9func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Ten Function Network Distribution Across Functional Clusters'
    if len(fcluster_10func) > 0:
        ax_dict10 = UpSet(fcluster_10func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                        totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                        min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Eleven Function Network Distribution Across Functional Clusters'
    if len(fcluster_11func) > 0:
        ax_dict11 = UpSet(fcluster_11func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=5,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Twelve Function Network Distribution Across Functional Clusters'
    if len(fcluster_12func) > 0:
        ax_dict12 = UpSet(fcluster_12func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Thirteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_13func) > 0:
        ax_dict13 = UpSet(fcluster_13func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Fourteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_14func) > 0:
        ax_dict14 = UpSet(fcluster_14func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Fifteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_15func) > 0:
        ax_dict15 = UpSet(fcluster_15func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                        totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                        min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Sixteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_16func) > 0:
        ax_dict16 = UpSet(fcluster_16func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Seventeen Function Network Distribution Across Functional Clusters'
    if len(fcluster_17func) > 0:
        ax_dict17 = UpSet(fcluster_17func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=8,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Eighteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_18func) > 0:
        ax_dict18 = UpSet(fcluster_18func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Nineteen Function Network Distribution Across Functional Clusters'
    if len(fcluster_19func) > 0:
        ax_dict19 = UpSet(fcluster_19func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                          totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                          min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()

    # 'Twenty Function Network Distribution Across Functional Clusters'
    if len(fcluster_20func) > 0:
        ax_dict20 = UpSet(fcluster_20func, show_counts=True, sort_by='degree', shading_color=0.2, element_size=10,
                         totals_plot_elements=15, with_lines=True, show_percentages=False, subset_size='count',
                         min_subset_size=1, include_empty_subsets=False).plot()
        plt.show()


get_union_of_functions_from_different_versions()
get_fcluster_sizes_bary_id_text_id_maps_after_merge_across_versions()
get_overall_barycenter()
get_final_model_params_after_merge_across_versions()
get_netk_distribution_over_func_cluster_upset_plots()