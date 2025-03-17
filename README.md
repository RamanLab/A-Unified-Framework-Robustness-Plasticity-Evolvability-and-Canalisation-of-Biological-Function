# UNFOLDing-Robustness-Plasticity-Evolvability-and-Canalisation-of-Biological-Function

This repository contains code to reproduce the work from the manuscript "A Unified Framework To Dissect Robustness Plasticity Evolvability and Canalisation of Biological Function." (https://www.biorxiv.org/content/10.1101/2025.03.03.641119v1.full.pdf) \
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

## Analysis of Computational Pipeline Output
### Map  Network Structures to Functional Clusters
In our analysis, we stopped the computational pipeline after two iterations (i.e., iteration_number = 1). The last barycenter dataset created is `barycenter2_v<version_id>_combined0_9.csv`
   - Run `code/analysis/map_structures_to_func_clusters.py`
   - Input file `fun_labels_v<version_id>_combined0_9.csv`
   - This will create files `final_func_cluster<bary_id>_model_params.csv` with bary_id given by the label in `fun_labels_v<version_id>_combined0_9.csv`
   - The output files will be created in the `data/v<version_id>/csvs/combined0_9/final_func_model_param_map` folder
     
**Get Text IDs of Barycenters**
For each version \
   - Plot the barycenters from the last run of the computational pipeline using the function `plot_conc_vs_time_in_dataset_one_by_one` in `code/analysis/visualize.py`
   - Create a file named `text_id_desc.csv` with two columns: 'text_id' and 'desc'. The 'text_id' column should be populated with a four-letter string for each function and the 'desc' column should have a description of the function based on inspection of the plots. The order of the 'text_id' in this file should follow the bary_id
   - Put this file in the `data/v<version_id>/csvs/combined0_9` folder
  
**Get Functional Cluster Sizes & Mapping of Function IDs with Barycenter IDs**
   - Run `get_fcluster_sizes_bary_id_text_id_maps_combined0_9_datasets.py` with nfunc = number of functional clusters (or number of barycenters) in the last iteration
   - This will create a file `func_id_bary_id_text_id.csv` with the sizes of each functional cluster identified by the corresponding bary_id and text_id. The function_id is assigned according to descending order of the number of circuits in the functional cluster, i.e., the function exhibited by the highest number of circuits is assigned function_id '01', second highest as '02', and so on
   - Furthermore, this program will create a file `parameter_count_per_model_fcluster<bary_id>.csv` with the count of the number of parameters for which each network exhibits a given function
   - The output files are created at `data/v<version_id>/csvs/combined0_9`


### Integrate Results Across Versions
   1. Run `get_pairwise_dtw_distances` for pairs of versions passed in version_id1 and version_id2 in the code to find barycenter matches across versions. This calculates the pairwise Dynamic Time Warping (DTW) distance between the barycenter datasets
   2. The file with pairwise DTW distances will be created in `data/integrated_results_v0_v1_v2/csvs/pairwise_barycenter_distances`
   3. Run `compare_barycenters_datasets.py` to plot heatmaps for pairwise DTW distances among the barycenters of pairs of versions
   4. Take the union of barycenters based on the DTW distances, i.e., for small DTW distances, the barycenter pairs can be considered identical, else they are considered unique
   5. The text_id for identical barycenters across versions identified in the above step should be identical in the `text_id_desc.csv` file in each of the `data/v<version_id>/csvs/combined0_9` folders for the three version_id
   6. Take the union of the text_id across versions by running the function `get_union_of_functions_from_different_versions` in `code/analysis/get_integrated_results_from_versions.py`
   7. This creates the file `text_id_desc.csv` in the `data/integrated_results_v0_v1_v2/csvs` folder
   8. Next run the function `get_fcluster_sizes_bary_id_text_id_maps_after_merge_across_versions` in `code/analysis/get_integrated_results_from_versions.py`. This gives the mapping of the integrated functional cluster function_id, text_id and the sizes of functional clusters after merging them over the three versions

**Summary of results across the 10 partitions of networks and the three versions**
![Consistency of results](https://github.com/user-attachments/assets/25d71102-174d-44b6-a9b8-e76d8cafc7a2)


##Analysis of Robustness, Plasticity, Evolvability And Canalisation

![insights](https://github.com/user-attachments/assets/e2dc45cd-9172-4ac3-bf83-8db783ba4c37)  ![insights_legend](https://github.com/user-attachments/assets/d78820a3-bde9-42bd-bbc0-b2b752235511)










