import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sn

def min_max_scaling(df_conc):

    df_conc = df_conc.T
    for column in df_conc.columns:
        df_conc[column] = (df_conc[column] - df_conc[column].min()) / (df_conc[column].max() - df_conc[column].min())
    return df_conc.T

# Compare the barycenter datasets across pairs of versions by plotting the pairwise DTW distances in a heatmap
version_id1 = '0'
version_id2 = '1'

df_output = pd.read_csv('../../data/integrated_results_v2_0_v2_1_v2_2/csvs/pairwise_distances/pairwise_distances_barycenter2_v'+version_id1+'_and_v'+version_id2+'.csv')
df_output = df_output.rename(columns={"param_index1": "Barycenter-V"+version_id1, "param_index2": "Barycenter-V"+version_id2})

heatmap_data = df_output.pivot(index="Barycenter-V"+version_id1, columns="Barycenter-V"+version_id2, values='DTW_distance')
min_value_index = heatmap_data.values.argmin()
min_value_row, min_value_col = divmod(min_value_index, heatmap_data.shape[1])

plt.figure(figsize=(8, 6))
sn.heatmap(heatmap_data, annot=True, cmap='binary', fmt=".2f", linewidths=.5)

# Annotate the cell with the minimum value in each row
for i, row in enumerate(heatmap_data.index):
    min_value = heatmap_data.loc[row].min()
    col_index = heatmap_data.loc[row].idxmin()

    plt.annotate(f'Min',
                 xy=(heatmap_data.columns.get_loc(col_index) + 0.5, i + 0.5),
                 xytext=(0, 10),
                 textcoords='offset points',
                 ha='center',
                 fontsize=8,
                 color='red',
                 bbox=dict(boxstyle='round,pad=0.3', edgecolor='red', facecolor='white'))
plt.show()