import pandas as pd

df = pd.DataFrame()
for i in range(10):
    df_temp = pd.read_csv('../../data/v2/csvs/sampled_dataset'+ str(i)
                          +'/barycenter_dataset/barycenter1_sampled_dataset'+ str(i) +'.csv')
    df_temp['param_index'] = df_temp.param_index.apply(lambda row: 'd'+ str(i) +'.'+row)
    df = pd.concat([df, df_temp], axis=0).reset_index(drop=True)

df.to_csv('../../data/v2/csvs/combined0_9/barycenter1_v2_combined0_9.csv', header=True, index=None)