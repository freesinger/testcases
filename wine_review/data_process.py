import pandas as pd
import numpy as np

DATAPATH = './data/'
FORMAL = DATAPATH + 'winemag-data_first150k.csv'
LATER = DATAPATH + 'winemag-data-130k-v2.csv'

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

data = pd.read_csv(FORMAL)
df = data.copy(deep=True)
print('--Data Shape--')
print(df.shape)
# (150930, 11)

print('\n--Features--')
print(df.columns.values)

df = df.drop(['description', 'Unnamed: 0'], axis=1)
print('\n--Basic Info--')
for col in df.columns:
    print('*', col, '*: ', df[col].dtype, df[col].unique())
# print(df.info)

print('\n--Variety--')
variety = df['variety'].value_counts()
print(variety[: 50])