# UNFOLDing-Robustness-Plasticity-Evolvability-and-Canalisation-of-Biological-Function

This repository contains code to reproduce the work from the manuscript "A Unified Framework To Dissect Robustness Plasticity Evolvability and Canalisation of Biological Function." (https://www.biorxiv.org/content/10.1101/2025.03.03.641119v1.full.pdf) 
**Workflow Diagram**
![workflow_diagram](https://github.com/user-attachments/assets/bcd67d8a-d91f-4365-a751-c789bc7d2553)

Follow these steps to reproduce the results:
## Data Generation by Simulation

### Step 1: Generate Prerequisites
Run `code/data_generation/prerequisites_to_simulation.py` to create:
- Adjacency matrix file with 16,038 networks (in `/data/common/` folder)
- A file with 10,000 parameter sets using Latin Hypercube Sampling (LHS), indexed 0-9999
- Initial condition guesses using LHS (for finding steady states with 'fsolve' in Step 3)
- A Python file containing ODE models as functions for all 16,038 networks

### Step 2: Sample Networks
Run `/data_generation/sample_networks_for_analysis.py` to:
- Create 10 partitions of the 16,038 networks
- Each partition contains 10% of all networks but preserves the edge probabilities of the complete set of 16038 networks
- Generates files named `lhs_models_sampled_for_analysis<sampled_dataset_id>.csv` (with <sampled_dataset_id> from 0-9) in `/data/common/`

### Step 3: Calculate Steady States
Run `code/data_generation/get_steady_states.py` to:
- Use 'fsolve' with the initial guesses to find steady states for each network across all parameter sets
- Generate one file per network (16,038 total) containing:
  - Steady-state concentrations for all three nodes (columns x[0], x[1], x[2])
  - Parameter set index (column param_index)
  - A 'steady_state_found' flag

### Step 4: Generate Time Course Dataset
Run `code/data_generation/main_dataset_generation.py` to:
- Use parameters, ODE models, and steady states as initial conditions
- Run for networks specified in the `lhs_models_sampled_for_analysis<sampled_dataset_id>.csv` files
- Output files go to `/data/v<version_id>/dataset<sampled_dataset_id>_lhs/` 
- In our case, `<version_id>` ranges from 0-2 (three sets of 10,000 parameter sets)
- Running this for all `<sampled_dataset_id>` values (0-9) completes the simulation for all 16038 networks
- Outputs include:
  - Concentration time course data in `model<model_id>_output_conc.csv`
  - Parameter values and initial conditions in `/input_sim_data/dataset_model<model_id>.csv`

## Computational Pipeline

### Iteration 0

1. **Cluster Time Series**
   - Run `code/pipeline/cluster_time_series_handling_nan.py`
   - Takes time course data from `/data/v<version_id>/dataset<sampled_dataset_id>_lhs/model<model_id>_output_conc.csv`
   - Clusters the time courses for each model
   - Outputs cluster labels to `/data/csvs/sampled_dataset<sampled_dataset_id>/cluster_labels/cluster_label_model<model_id>.csv`

2. **Calculate Cluster Barycenters**
   - Run `code/pipeline/cluster_berycenter_dataset.py` with `barycenter_flag = 0`
   - Drops clusters with fewer than 10 time courses
   - Creates file `/data/v<version_id>/csvs/sampled_dataset<sampled_dataset_id>/barycenter_dataset/barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv`
   - This file contains barycenters of all clusters from all networks in the sample

### Iteration 1 Onwards

1. **Cluster Barycenters**
   - Run `code/pipeline/cluster_barycenter_dataset.py`
   - Uses the barycenter dataset from the previous iteration as input (instead of simulation-generated time courses)
   - The output file `fun_cluster_labels<iteration_number>_barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv` is created in the folder `data/v<version_id>/csvs/sampled_dataset<sampled_dataset_id>/functional_cluster_labels`

2. **Calculate New Barycenters**
   - Run `code/pipeline/cluster_berycenter_dataset.py` with `barycenter_flag = 1`
   - The output file `barycenter<iteration_number + 1>_sampled_dataset<sampled_datast_id>.csv` is created in the `data/v<version_id>/csvs/sampled_dataset<sampled_dataset_id>/barycenter_dataset` folder

### When to Stop Iterations
- After each iteration, plot the barycenters
- Stop when time courses are visually distinct

### Final Steps & Last Pipeline Run
- After completing the pipeline iterations for all networks, i.e. <sampled_dataset_id> from 0-9 for a given `<version_id>`:
  - Run `code/pipeline/merge_barycenter_datasets.py` to merge the 10 barycenter datasets and save the `barycenter<iteration_number>_v<version_id>_combined0_9.csv` file in the `data/v<version_id>/csvs/combined0_9` folder
  - Rerun the pipeline with the merged barycenter dataset `barycenter<iteration_number>_v<version_id>_combined0_9.csv` as input
    For this:
    - Change paths in `code/pipeline/cluster_barycenter_dataset.py` to pick the input file from and write the output file `fun_labels_v<version_id>_combined0_9.csv` in the `data/v<version_id>/csvs/combined0_9` folder
    - Change paths in `code/pipeline/get_cluster_barycenters.py` to pick the input files from and write the output files in the `data/v<version_id>/csvs/combined0_9` folder
  - This produces the final barycenter dataset `barycenter<iteration_number + 1>_v<version_id>_combined0_9.csv` for the given `<version_id>`

**Summary of our results across the 10 partitions of networks and across the three versions**
![Consistency of results](https://github.com/user-attachments/assets/25d71102-174d-44b6-a9b8-e76d8cafc7a2)

## Analysis of Computational Pipeline Output
### Map  Network Structures to Functional Clusters
In our analysis, we stopped the computational pipeline after two iterations (i.e., iteration_number = 1). The last barycenter dataset created is `barycenter2_v<version_id>_combined0_9.csv`
   - Run `code/analysis/map_structures_to_func_clusters.py`
   - Input file `fun_labels_v<version_id>_combined0_9.csv`
   - This will create files `final_func_cluster<bary_id>_model_params.csv` with bary_id given by the label in `fun_labels_v<version_id>_combined0_9.csv`
   - The output files will be created in the `data/v<version_id>/csvs/combined0_9/final_func_model_param_map` folder
     
1. **Get Text IDs of Barycenters**
   - Plot the barycenters from the last run of the computational pipeline
   - Create a text file with four letter text IDs for each function and enter a description
   - Put this file in the `data/v<version_id>/csvs/combined0_9` folder
  
2. **Get Functional Cluster Sizes**
   - Run `get_fcluster_sizes_combined0_9_datasets.py` with nfunc = number of functional clusters (or number of barycenters) in the last iteration
   - This will create a file `fcluster_sizes.csv` with the sizes of each functional cluster identified by the corresponding bary_id
   - Furthermore, it will create a file `parameter_count_per_model_fcluster<bary_id>.csv` with the count of the number of parameters for which each network exhibits a given function
   - The output files are created at `data/v<version_id>/csvs/combined0_9`







