# A-Unified-Framework-to-Dissect-Robustness-Plasticity-Evolvability-and-Canalisation-of-Biological-Function

This repository contains code to reproduce the work from the manuscript "A Unified Framework To Dissect Robustness Plasticity Evolvability and Canalisation of Biological Function." Follow these steps to reproduce the results:

## Data Generation by Simulation

### Step 1: Generate Prerequisites
Run `code/data_generation/prerequisites_to_simulation.py` to create:
- Adjacency matrix file with 16,038 networks (in `/data/common/` folder)
- A file with 10,000 parameter sets using Latin Hypercube Sampling (LHS), indexed 0-10000
- Initial condition guesses using LHS (for finding steady states with 'fsolve')
- A Python file containing ODE models as functions for all 16,038 networks

### Step 2: Sample Networks
Run `/data_generation/sample_networks_for_analysis.py` to:
- Create 10 partitions of the 16,038 networks
- Each partition contains 10% of all networks but preserves the structural properties
- Generates files named `lhs_models_sampled_for_analysis<sampled_dataset_id>.csv` (with IDs 0-9) in `/data/common/`

### Step 3: Calculate Steady States
Run `code/data_generation/get_steady_states.py` to:
- Use 'fsolve' with the initial guesses to find steady states for each network across all parameter sets
- Generate one file per network (16,038 total) containing:
  - Steady-state concentrations for all three nodes (columns x[0], x[1], x[2])
  - Parameter set index
  - A 'steady_state_found' flag

### Step 4: Generate Time Course Dataset
Run `code/data_generation/main_dataset_generation.py` to:
- Use parameters, ODE models, and steady states as initial conditions
- Run for networks specified in the `lhs_models_sampled_for_analysis<sampled_dataset_id>.csv` files
- Output files go to `/data/<version_id>/dataset<sampled_dataset_id>_lhs/` 
- In our case, `<version_id>` ranges from 0-2 (three sets of 10,000 parameter sets)
- Running this for all `<sampled_dataset_id>` values (0-9) completes the simulation for all networks
- Outputs include:
  - Concentration time course data in `model<model_id>_output_conc.csv`
  - Parameter values and initial conditions in `/input_sim_data/dataset_model<model_id>.csv`

## Computational Pipeline

### Iteration 1

1. **Cluster Time Series**
   - Run `code/pipeline/cluster_time_series_handling_nan.py`
   - Takes time course data from `/data/<version_id>/dataset<sampled_dataset_id>_lhs/model<model_id>_output_conc.csv`
   - Clusters the time courses for each model
   - Outputs cluster labels to `/data/csvs/sampled_dataset<sampled_dataset_id>/cluster_labels/cluster_label_model<model_id>.csv`

2. **Calculate Cluster Barycenters**
   - Run `code/pipeline/cluster_berycenter_dataset.py` with `barycenter_flag = 0`
   - Drops clusters with fewer than 10 time courses
   - Creates file `/data/<version_id>/csvs/sampled_dataset<sampled_dataset_id>/barycenter_dataset/barycenter<iteration_number>_sampled_dataset<sampled_dataset_id>.csv`
   - This file contains barycenters of all clusters from all networks in the sample

### Iteration 2 Onwards

1. **Cluster Barycenters**
   - Run `code/pipeline/cluster_barycenter_dataset.py`
   - Uses the barycenter dataset from previous iteration as input (instead of simulation time courses)

2. **Calculate New Barycenters**
   - Run `code/pipeline/cluster_berycenter_dataset.py` with `barycenter_flag = 1`

### When to Stop Iterations
- After each iteration, plot the barycenters
- Stop when time courses are visually distinct

### Final Steps
- After completing iterations for all samples (0-9) for a given `<version_id>`:
  - Run `code/pipeline/merge_barycenter_datasets.py` to merge the 10 barycenter datasets
  - Rerun the pipeline with the merged dataset as input
  - This produces the final barycenter dataset for the given `<version_id>`
After stopping the computational pipeline for a given <version_id> over <sampled_dataset_id> from 0-9, we merge the 10 barycenter datasets by running the 'code/pipeline/merge_barycenter_datasets.py file. We then rerun the pipeline with this merged barycenter dataset as the input. At the end of this, we get the final barycenter dataset for the given <version_id>.

