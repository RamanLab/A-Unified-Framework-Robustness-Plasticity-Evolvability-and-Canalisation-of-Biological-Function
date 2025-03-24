import pandas as pd
from functools import partial
import multiprocessing as mp
from calculate_fd_pd import calculate_fd_pd
import time

def get_fd_pd_networkwise(overall_mean_pd, output_filename):

    df_weights = pd.read_csv(
        '../../data/integrated_results_v0_v1_v2/csvs/robustness_evolvability_plasticity_canalisation_analysis/function_category_combination_weights.csv')

    df_lhs0 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis0.csv')
    df_lhs1 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis1.csv')
    df_lhs2 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis2.csv')
    df_lhs3 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis3.csv')
    df_lhs4 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis4.csv')
    df_lhs5 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis5.csv')
    df_lhs6 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis6.csv')
    df_lhs7 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis7.csv')
    df_lhs8 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis8.csv')
    df_lhs9 = pd.read_csv('../../data/common/lhs_models_sampled_for_analysis9.csv')

    df_lhs0 = df_lhs0['model_index'].apply(lambda x: '0.' + str(x))
    df_lhs1 = df_lhs1['model_index'].apply(lambda x: '1.' + str(x))
    df_lhs2 = df_lhs2['model_index'].apply(lambda x: '2.' + str(x))
    df_lhs3 = df_lhs3['model_index'].apply(lambda x: '3.' + str(x))
    df_lhs4 = df_lhs4['model_index'].apply(lambda x: '4.' + str(x))
    df_lhs5 = df_lhs5['model_index'].apply(lambda x: '5.' + str(x))
    df_lhs6 = df_lhs6['model_index'].apply(lambda x: '6.' + str(x))
    df_lhs7 = df_lhs7['model_index'].apply(lambda x: '7.' + str(x))
    df_lhs8 = df_lhs8['model_index'].apply(lambda x: '8.' + str(x))
    df_lhs9 = df_lhs9['model_index'].apply(lambda x: '9.' + str(x))

    df_model_idx = pd.DataFrame(columns=['model_index'])
    df_model_idx['model_index'] = pd.concat(
        [df_lhs0, df_lhs1, df_lhs2, df_lhs3, df_lhs4, df_lhs5, df_lhs6, df_lhs7, df_lhs8, df_lhs9], axis=0).reset_index(
        drop=True)
    df_model_idx.loc[:, ['sampled_id']] = df_model_idx['model_index'].apply(lambda x: x.split('.')[0])
    df_model_idx.loc[:, ['model_index']] = df_model_idx['model_index'].apply(lambda x: x.split('.')[1]).astype(
        dtype=int)
    df_model_idx = df_model_idx.sort_values(by='model_index').reset_index(drop=True)

    start_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
    print("Jobs start time = ", start_time)

    pool = mp.Pool(processes=64)
    calculate_fd_pd_partial = partial(calculate_fd_pd, df_model_idx, df_weights, overall_mean_pd, output_filename)
    pool.map(calculate_fd_pd_partial, df_model_idx.model_index.values)

    end_time = time.strftime('%l:%M%p %Z on %b %d, %Y')
    print("Jobs end time = ", end_time)


# Overall Mean Parametric Diversity. If the value is not known yet pass 0
overall_mean_pd = 54.8527
output_filename = 'fd_pd.csv'
get_fd_pd_networkwise(overall_mean_pd, output_filename)
