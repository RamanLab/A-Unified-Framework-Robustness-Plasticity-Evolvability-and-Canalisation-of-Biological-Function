""""
Description: This program calculates the barycenters of either time course clusters or
barycenter clusters.
When the input dataset contains cluster labels of time courses, it finds the barycenters
of only those clusters that have a size greater than min_cluster_size.
If cluster size is less than min_cluster_size, it drops all the time course members of
that cluster.
Each barycenter is assigned an index given by "<model_ID>.<param_ID>"
when finding barycenters of time courses. When the input dataset contains cluster labels
of barycenters, each calculated barycenter is assigned an index given by
"b.f<functional_cluster_ID>".
Inputs:
    input_data_id: Model ID, if the input dataset contains time series cluster labels
               Iteration number of barycenter calculation, if the input dataset contains barycenter cluster labels
    sampled_dataset_id: Sampled Dataset ID
    min_cluster_size: Minimum size of time series cluster for which barycenter should be calculated
    barycenter_flag: Flag to indicate if input file contains time series "cluster labels (when 0) or barycenter
                     cluster labels (when 1)
    cluster_label_data_path: Path to cluster label data files "cluster_label_model<model_ID>.csv" or
                             "barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv"
    output_conc_dataset_path: Path to 'model<model_ID>_output_conc.csv' dataset file for first iteration and
                              barycenter dataset file from the last iteration for every next iteration
    barycenter_dataset_path: Path to save the file "barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv"
                             containing the calculated barycenters for each cluster
Outputs:
    A csv file with 101 columns giving the barycenter of time points [t0-t100] and one column 'param_index' indicating
    "<model_ID>.<cluster_ID>" if the input dataset is a time series clusters and "b.f<functional_cluster_ID>" if the
    input dataset consists of barycenters.
"""
import pandas as pd
from tslearn.barycenters import softdtw_barycenter
import argparse
import time
import os

def min_max_scaling(df_conc):
    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

def main(args):

    arg1 = args.input_data_id
    arg2 = args.sampled_dataset_id
    min_cluster_size = args.min_cluster_size
    barycenter_flag = args.barycenter_flag
    if barycenter_flag == 1:
        cluster_label_data_path = args.cluster_label_data_path + '/sampled_dataset' + str(arg2) + \
                                  '/functional_cluster_labels'
        output_conc_dataset_path = args.output_conc_dataset_path + '/csvs/sampled_dataset'+ str(arg2) + \
                                   '/barycenter_dataset'
    else:
        cluster_label_data_path = args.cluster_label_data_path + '/sampled_dataset' + str(arg2) + '/cluster_labels'
        output_conc_dataset_path = args.output_conc_dataset_path + '/dataset' + str(arg2) + '_lhs'

    barycenter_dataset_path = args.barycenter_dataset_path + '/sampled_dataset'+ str(arg2) + '/barycenter_dataset'

    # Record start time
    start_time = time.time()

    # Get cluster labels
    if barycenter_flag == 1:
        df_cluster_labels = pd.read_csv(cluster_label_data_path+'/fun_cluster_labels'+ str(arg1) +'_barycenter'+
                                        str(arg1) +'_sampled_dataset'+ str(arg2) +'.csv', dtype={'param_index': str})
    else:
        df_cluster_labels = pd.read_csv(cluster_label_data_path+'/cluster_label_model'+str(arg1)+'.csv',
                                        dtype={'param_index': str})

    # Get time course/barycenter dataset
    if barycenter_flag == 1:
        df_conc = pd.read_csv(output_conc_dataset_path + '/barycenter'+ str(arg1) +'_sampled_dataset'+ str(arg2)
                              + '.csv', dtype={'param_index': str})
    else:
        df_conc = pd.read_csv(output_conc_dataset_path+ '/model' + str(arg1) + '_output_conc.csv',
                              dtype={'param_index': str})

    df_conc = df_conc.set_index('param_index')

    # Scale time course or barycenter data between 0-1
    df_conc = min_max_scaling(df_conc)

    # If input dataset consists of time courses, handle NaN entries
    if barycenter_flag == 0:
        df_conc = df_conc.T
        nan_idx = df_conc.columns[df_conc.isna().any()].tolist()
        df_conc = df_conc.drop(columns=nan_idx)
        df_conc = df_conc.T

    # Get the data labels list
    labels = df_cluster_labels.label.unique()

    index = []
    barycenter_list = []
    for label in labels:
        df_labels_temp = df_cluster_labels.loc[df_cluster_labels['label'] == label]
        param_index_list = df_labels_temp.index
        if len(param_index_list) <= min_cluster_size and barycenter_flag == 0:
            continue
        cluster_conc = df_conc.iloc[param_index_list, :]
        cluster_conc = cluster_conc.reset_index(drop=True)

        cluster_barycenter = softdtw_barycenter(cluster_conc, gamma=1.0, max_iter=50, tol=1e-3)
        barycenter_list.append(cluster_barycenter.ravel())
        if barycenter_flag == 0:
            index.append(str(arg1) + '.' + str(label))
        else:
            index.append('b.f' + str(label))

    df_barycenter = pd.DataFrame(barycenter_list)
    df_barycenter['param_index'] = index

    if barycenter_flag == 1:
        itr = int(arg1) + 1
        df_barycenter.to_csv(barycenter_dataset_path+'/barycenter' + str(itr) + '_sampled_dataset'+ str(arg2)
                             +'.csv', index=None, header=True)

    else:
        itr = 0
        file_exists = os.path.isfile(barycenter_dataset_path+'/barycenter' + str(itr) + '_sampled_dataset'+ str(arg2)
                                     +'.csv')
        if not file_exists:
            df_barycenter.to_csv(barycenter_dataset_path+'/barycenter' + str(itr) + '_sampled_dataset'+ str(arg2)
                                 +'.csv', mode='a', index=None, header=True)
        else:
            df_barycenter.to_csv(barycenter_dataset_path+'/barycenter' + str(itr) + '_sampled_dataset'+ str(arg2)
                                 +'.csv', mode='a', index=None, header=False)

    # Record end time
    end_time = time.time()

    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

def default_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data_id", help="Model ID or Barycenter iteration number", required=True)
    parser.add_argument("--sampled_dataset_id", help="Sampled Dataset ID", required=True)
    parser.add_argument("--min_cluster_size", default=10, help="Minimum size of time series cluster for which "
                                                               "barycenter should be calculated. Not applicable if "
                                                               "barycenter_flag = 1")
    parser.add_argument("--barycenter_flag", type=int, help="Flag to indicate if input file contains time series "
                                                  "cluster labels (when 0) or barycenter cluster labels (when 1)",
                        required=True)
    parser.add_argument("--cluster_label_data_path", default='/home/user/PycharmProjects/data/v2/csvs',
                        help='Path to cluster label data files "cluster_label_model<model_ID>.csv" or '
                             '"barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv"')
    parser.add_argument("--output_conc_dataset_path", default='/home/user/PycharmProjects/data/v2',
                        help="Path to 'model<model_ID>_output_conc.csv' dataset file for first iteration and "
                             "barycenter dataset file from last iteration for every next iteration")
    parser.add_argument("--barycenter_dataset_path", default='/home/user/PycharmProjects/data/v2/csvs',
                help='Path to save the file "barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv" '
                     'containing the calculated barycenters for each cluster')

    return parser

if __name__ == '__main__':
    args = default_argument_parser().parse_args()
    main(args)
