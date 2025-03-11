# A-Unified-Framework-to-Dissect-Robustness-Plasticity-Evolvability-and-Canalisation-of-Biological-Function

This repository contains the code to reproduce the work in the manuscript "A Unified Framework To Dissect Robustness Plasticity Evolvability and Canalisation of Biological Function". The steps to reproduce the results reported in this manuscript are given below.

# Data Generation by Simulation
1. Run the '/data_generation/prerequisites_to_simulation.py' file \
   It will create the following .csv files: \
   i. Adjacency matrix file with 16038 networks (in /data/common/ folder) \
   ii. A file with 10000 parameter sets sampled using Latin Hypercube Sampling (LHS) with indices 0-10000 \
   iii. A file with initial guesses of initial conditions sampled using Latin Hypercube Sampling (To be used by 'fsolve' function for getting steady states for each model.) \
   iv. A .py file with the ODE models as Python functions for each of the 16038 networks for which the adjacency matrices have been listed in the .csv file above (i). 
   
3. Run the '/data_generation/sample_networks_for_analysis.py' file \
   It will create 10 partitions of the 16038 networks, each containing a set of 10% of all the networks but structurally representing the complete set of 16038 networks. This is done by  ensuring that the edge probabilities are preserved in all the 10 partitioned network sets. This program will generate files called 'lhs_models_sampled_for_analysis<sampled_dataset_id>.csv' (with <sampled_dataset_id> ranging from 0-9) in the /data/common/ folder.

4. Run the '/data_generation/get_steady_states.py' file \
   This will take the initial guesses from the file generated in point 1. (iii) above and use 'fsolve' to get the steady state for each network over all 10000 parameter sets sampled in 1. (ii) above. If 'fsolve' cannot find the steady state for the network for any of the parameter sets, it will indicate in the output file using a flag. The 'get_steady_states.py' code generates a file for every network containing the steady state concentrations for the three nodes of the genetic circuit in columns named x[0], x[1], x[2], the index of the parameter set from file generated in 1. {ii) and a 'steady_state_found' flag. At the end of running this code, there will be 16038 files with steady states for each of the 16038 networks.

5. Run the '/data_generation/main_dataset_generation.py' file \
   This will pick all the relevant files generated above, like parameter set files, ODE model containing files, and steady-state data to be used as initial conditions for ODE model simulation. This file will run for networks given in the 'lhs_models_sampled_for_analysis<sampled_dataset_id>.csv' file (generated above in 3.). The output files will be created in the folder /data/<version_id>/dataset<sampled_dataset_id>_lhs. The <version_id> in our case runs from 0-2 since we have done step 1 three times to get three sets of 10000 parameter sets each. For a given <version_id>, running the 'main_dataset_generation.py' file for <sampled_dataset_id> from 0-9 completes the simulation for all 16038 networks.\
The output concentration time course data is present in files named 'model<model_id>_output_conc.csv' file in the /data/<version_id>/dataset<sampled_dataset_id>_lhs folder with <model_id> from 'lhs_models_sampled_for_analysis<sampled_dataset_id>.csv' files. These files contain the parameter index in column 'param_index' followed by the concentration of the output gene product over time points 0-100 in the remaining columns. Another folder called 'input_sim_data' is created inside /data/<version_id>/dataset<sampled_dataset_id>_lhs for the values of the parameters by 'param_index' and initial conditions used for simulation for each network in files named 'dataset_model<model_id>.csv' with <model_id> from 'lhs_models_sampled_for_analysis<sampled_dataset_id>.csv' files.


# Computational Pipeline
## Iteration 1
1. Run the '/pipeline/cluster_time_series_handling_nan.py' file \
Now that the simulated time course data is ready in the /data/<version_id>/dataset<sampled_dataset_id>_lhs/ folders, the first iteration of the computational pipeline involves picking the file '/data/<version_id>/dataset<sampled_dataset_id>_lhs/model<model_id>_output_conc.csv' and clustering the time courses for a given <model_id>. The output of this code is a file '/data/csvs/sampled_dataset<sampled_dataset_id>/cluster_labels/cluster_label_model<model_id>.csv' with two columns 'param_index' and 'label'.

2. Run the '/pipeline/cluster_berycenter_dataset.py' file \
Since the first iteration involves finding clusters' barycenters containing time courses, we pass 'barycenter_flag = 0'. If a cluster contains less than 10 time courses, the code drops all the cluster members. At the end of running this code, a file /data/<version_id>/csvs/sampled_dataset<sampled_dataset_id>/barycenter_dataset/barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv' will be created. This file contains the barycenters of all the clusters from all networks in 'lhs_models_sampled_for_analysis<sampled_dataset_id>.csv'.

## Iteration 2 onwards
1. Run the '/pipeline/cluster_barycenter_dataset.py' file \
This code does the same clustering as point 1 in Iteration 1 except that it takes the barycenter dataset generated in the last iteration as input instead of time courses generated by the simulation.

2. Run the '/pipeline/cluster_berycenter_dataset.py' file \
From iteration 2 onwards, set 'barycenter_flag = 1'.

## Stop Iterations
After running an iteration, we plot the barycenters and find if the time courses are distinct. If yes, we stop.


After stopping the computational pipeline for a given <version_id> over <sampled_dataset_id> from 0-9, we merge the 10 barycenter datasets by running the '/pipeline/merge_barycenter_datasets.py file. We then rerun the pipeline with this merged barycenter dataset as the input. At the end of this, we get the final barycenter dataset for the given <version_id>.

