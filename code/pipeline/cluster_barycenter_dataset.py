"""
Description: This program clusters barycenter dataset using KMeans clustering
with pairwise Dynamic Time Warping (DTW) distance calculation
Inputs:
    Iteration_number: Iteration number that generated the barycenter dataset
    sampled_dataset_id: Sampled Dataset ID
    barycenter_dataset_path: Path to "barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv" file
    random_seed_kmeans: Random seed to be used in KMeans clustering
    fun_cluster_label_data_path: Path to save the
    fun_cluster_labels<Iteration_number>_barycenter<Iteration_number>_sampled_dataset<sampled_dataset_id>.csv file
    with functional cluster labels for the barycenter dataset
Output:
    A csv file with two columns: 'param_index': "b.f<functional_cluster_label in last iteration>" and 'label'
"""
import pandas as pd
# import numpy as np
from dtaidistance import dtw
from scipy.spatial.distance import squareform
from cuml.cluster import KMeans as cuKMeans
from kneed import KneeLocator
import time
import argparse


def min_max_scaling(df_conc):
    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

def main(args):
    # Parse arguments
    arg1 = args.iteration_number
    sampled_dataset_id = args.sampled_dataset_id
    kmax = args.kmax
    barycenter_dataset_path = args.barycenter_dataset_path+ '/sampled_dataset' + str(sampled_dataset_id)+'/barycenter_dataset'
    random_seed = args.random_seed_kmeans
    func_cluster_label_data_path = args.func_cluster_label_data_path+ '/sampled_dataset' + str(sampled_dataset_id)+'/functional_cluster_labels'

    # Record start time
    start_time = time.time()

    # Read output concentration time course dataset for model over all parameter sets
    df_data = pd.read_csv(barycenter_dataset_path + '/barycenter'+str(arg1)+'_sampled_dataset'+str(sampled_dataset_id)+'.csv', dtype={'param_index': str})

    df_data = df_data.set_index('param_index')
    df_data = min_max_scaling(df_data)
    if kmax > len(df_data):
        kmax = len(df_data)

    distance = dtw.distance_matrix(df_data.to_numpy(), compact=True, parallel=True, use_c=True, show_progress=True)
    distance_matrix = squareform(distance)

    wcss = []
    for k in range(2, kmax):
        kmeans = cuKMeans(n_clusters=k, random_state=random_seed)
        labels = kmeans.fit_predict(distance_matrix)
        wcss.append(kmeans.inertia_)

    kn = KneeLocator(
            range(2, kmax),
            wcss,
            curve='convex',
            direction='decreasing',
            interp_method='polynomial')

    kmeans = cuKMeans(n_clusters=kn.elbow + 2, random_state=random_seed)
    labels = kmeans.fit_predict(distance_matrix)

    df_cluster_labels = pd.DataFrame(columns=['param_index', 'label'])
    df_cluster_labels['param_index'] = df_data.index
    df_cluster_labels['label'] = labels
    df_cluster_labels.to_csv(func_cluster_label_data_path+'/fun_cluster_labels'+str(arg1)+'_barycenter'+str(arg1)+'_sampled_dataset'+str(sampled_dataset_id)+'.csv', index=None, header=True)

    # Record end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)

def default_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration_number", help="Iteration Number", required=True)
    parser.add_argument("--sampled_dataset_id", help="Sampled Dataset ID", required=True)
    parser.add_argument("--kmax", default=100, help="Maximum number of clusters to consider for Elbow point determination")
    parser.add_argument("--barycenter_dataset_path", default='/home/user/PycharmProjects/data/v2/csvs',
                        help="Path to 'barycenter<Iteration Number>_sampled_dataset<Sampled Dataset ID>.csv' dataset file")
    parser.add_argument("--random_seed_kmeans", default=27, help="Random seed to be used in KMeans clustering")
    parser.add_argument("--func_cluster_label_data_path", default='/home/user/PycharmProjects/data/v2/csvs',
                        help="Path to save the 'fun_cluster_labels<Iteration Number>_barycenter<Iteration Number>_sampled_dataset<Sampled Dataset ID>.csv' "
                             "file with functional cluster labels")

    return parser


if __name__ == '__main__':

    args = default_argument_parser().parse_args()
    main(args)