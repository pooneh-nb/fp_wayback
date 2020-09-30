import csv
import pandas as pd

df = pd.read_csv('datasets/dataframes/cookie_df_third_parties_vanilla')

df2 =df[df['url']=='google-analytics.com']
df2.to_csv('df2')