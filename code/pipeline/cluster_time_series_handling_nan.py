"""
Description: This program clusters time courses using KMeans clustering
with pairwise Dynamic Time Warping (DTW) distance calculation
Inputs:
    model: Model ID
    sampled_dataset_id: Sampled Dataset ID
    output_conc_dataset_path: Path to "model<model_ID>_output_conc.csv" dataset file
    nrows: Number of rows (i.e. parameter sets) from "model<model_ID>_output_conc.csv" dataset file to process, default='all'
    kmax: Maximum number of clusters to consider for Elbow point determination
    sim_input_dataset_path: Path to "dataset_model<model_ID>.csv" file
                            (for deleting a parameter set from simulation input data file
                            in case the time course corresponding to it contains NaN)
    random_seed_kmeans: Random seed to be used in KMeans clustering
    cluster_label_data_path: Path to save the "cluster_label_model<model_ID>.csv" file with cluster labels
Output:
    A csv file with two columns: 'param_index': <model_ID>.<param_ID> and label named "cluster_label_model<model_ID>.csv"
"""

import pandas as pd
from dtaidistance import dtw
from scipy.spatial.distance import squareform
from cuml.cluster import KMeans as cuKMeans
from kneed import KneeLocator
import time
import argparse

# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D


def min_max_scaling(df_conc):
    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

def process_data(df_data, model, sim_input_dataset_path, sampled_dataset_id):
    # Scale time courses between 0-1
    df_data = min_max_scaling(df_data)

    # Check if for any parameter, the scaled concentration time course has a NaN
    df_data = df_data.T
    nan_idx = df_data.columns[df_data.isna().any()].tolist()
    if len(nan_idx) > 0:

        # If NaN is present, read the simulation inputs file and remove the parameter set for which NaN is found
        df_param_dataset = pd.read_csv(
            sim_input_dataset_path + '/dataset' + str(sampled_dataset_id) + '_lhs/input_sim_data/dataset_model' +
            str(model) + '.csv', dtype={'param_index': str})
        df_param_dataset = df_param_dataset.loc[~df_param_dataset['param_index'].isin(nan_idx)].reset_index(drop=True)
        df_param_dataset.to_csv(sim_input_dataset_path + '/dataset' + str(sampled_dataset_id) +
                                '_lhs/input_sim_data/dataset_model' + str(model) + '.csv', header=True, index=False)

        # Update dataframe by removing Paramater ID of time course containing NaN
        df_data = df_data.loc[~df_data.index.isin(nan_idx)]
        df_data = df_data.drop(columns=nan_idx)
    df_data = df_data.transpose()
    return df_data


def main(args):
    # Parse arguments
    model = args.model
    sampled_dataset_id = args.sampled_dataset_id
    output_conc_dataset_path = args.output_conc_dataset_path+'/dataset' + str(sampled_dataset_id) + '_lhs'
    nrows = args.nrows
    kmax = args.kmax
    sim_input_dataset_path = args.sim_input_dataset_path
    random_seed = args.random_seed_kmeans
    cluster_label_data_path = args.cluster_label_data_path+'/sampled_dataset'+str(sampled_dataset_id)+'/cluster_labels'

    # Record start time
    start_time = time.time()

    # Read output concentration time course dataset for model over all parameter sets
    df_data = pd.read_csv(output_conc_dataset_path + '/model' + str(model) + '_output_conc.csv', dtype={'param_index': str})
    df_data = df_data.set_index('param_index')

    # Process output concentration time courses of a model for only 'nrows' number of parameter sets
    if nrows != 'all':
        df_data = df_data.head(nrows)

    # Process data and update simulation inputs file where applicable (i.e., if NaN is found in time course)
    df_data = process_data(df_data, model, sim_input_dataset_path, sampled_dataset_id)


    # Calculate pairwise DTW distance for concentration time courses
    distance = dtw.distance_matrix( df_data.to_numpy(), compact=True, parallel=True, use_c=True, show_progress=True)
    distance_matrix = squareform(distance)

    # # Maximum number of clusters to calculate Within-cluster-sum-of-squared distances for determining the elbow point
    if kmax == 'all' or kmax > len(df_data):
        kmax = len(df_data)
    wcss = []
    for k in range(2, kmax):
        kmeans = cuKMeans(n_clusters=k, random_state=random_seed)
        labels = kmeans.fit_predict(distance_matrix)
        wcss.append(kmeans.inertia_)

    # Locate the elbow point
    kn = KneeLocator(
            range(2, kmax),
            wcss,
            curve='convex',
            direction='decreasing',
            interp_method='polynomial')

    # Do KMeans clustering with number of clusters = elbow point
    kmeans = cuKMeans(n_clusters=kn.elbow+2, random_state=random_seed)
    labels = kmeans.fit_predict(distance_matrix)

    # Get dataframe with Parameter ID and its corresponding Label found by clustering
    df_cluster_labels = pd.DataFrame(columns=['param_index', 'label'])
    df_cluster_labels['param_index'] = df_data.index
    df_cluster_labels['label'] = labels

    # Write cluster label dataframe to csv
    df_cluster_labels.to_csv(cluster_label_data_path+'/cluster_label_model' + model + '.csv', header=True, index=None)

    # Record end time
    end_time = time.time()
    # Calculate elapsed time
    elapsed_time = end_time - start_time
    print("Elapsed time: ", elapsed_time)


def default_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", help="Model ID", required=True)
    parser.add_argument("--sampled_dataset_id", help="Sampled Dataset ID", required=True)
    parser.add_argument("--output_conc_dataset_path", default='/home/data',
                        help="Path to 'model<model_ID>_output_conc.csv' dataset file")
    parser.add_argument("--nrows", default='all',
                        help="Number of rows (i.e. parameter sets) from 'model<model_ID>_output_conc.csv' dataset file to process")
    parser.add_argument("--kmax", default=100,
                        help="Maximum number of clusters to consider for Elbow point determination")
    parser.add_argument("--sim_input_dataset_path", default='/home/data',
                        help="Path to 'dataset_model<model_ID>.csv' file (for deleting a parameter set from simulation input data file in case the time course corresponding to it contains NaN)")
    parser.add_argument("--random_seed_kmeans", default=27, help="Random seed to be used in KMeans clustering")
    parser.add_argument("--cluster_label_data_path", default='/home/output',
                        help="Path to save the 'cluster_label_model<model_ID>.csv' file with cluster labels")

    return parser


if __name__ == '__main__':

    args = default_argument_parser().parse_args()
    main(args)