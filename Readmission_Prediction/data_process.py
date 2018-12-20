import numpy as np
import pandas as pd

from statistics import mode

NUM_RECORDS = 101766
NUM_FEATURE = 50
ORIGNAL_DATA = '~/Desktop/Codes/Python_Testcases/Readmission_Prediction/dataset_diabetes/diabetic_data.csv'
RESULT_DATA = '~/Desktop/Codes/Python_Testcases/Readmission_Prediction/dataset_diabetes/processed_data.csv'

# load original data into dataframe and check shape
# output: (101766, 50)
dataframe_ori = pd.read_csv(ORIGNAL_DATA)
print(dataframe_ori.shape)

# examine the data types and descriptive stats
print("--Data Type--")
pd.set_option('display.max_columns', None)
print(dataframe_ori.info())
print("\n--Data Info--")
print(dataframe_ori.describe())

# make a copy of the dataframe for preprocessing
df = dataframe_ori.copy(deep = True)

"""
# explore unique values in each column
print("\n--Unique Values in Each Column--")
for col in dataframe_ori.columns:
    print(col, dataframe_ori[col].unique())
"""

# deal with missing values
print("\n--Missing Values Set--")
for col in df.columns:
    if df[col].dtype == object:
        missingNum = df[col][df[col] == '?'].count()
        if missingNum > 0:
            print(col, missingNum, '%.2f' % (missingNum / NUM_RECORDS * 100))
# gender
print('gender', df['gender'][df['gender'] == 'Unknown/Invalid'].count())

# process readmitted data
print('\n--Readmission Data--')
df['readmitted'] = df['readmitted'].replace('>30', 2)
df['readmitted'] = df['readmitted'].replace('<30', 1)
df['readmitted'] = df['readmitted'].replace('NO', 0)
# calculate number of readmmited and print
print('>30 readmmission', df['readmitted'][df['readmitted'] == 2].count())
print('<30 readmmission', df['readmitted'][df['readmitted'] == 1].count())
print('Never readmmission', df['readmitted'][df['readmitted'] == 0].count())

"""
Drop features
"""
print('\n--Drop Useless Features--')
# drop features with too much values missing
df = df.drop(['weight', 'payer_code', 'medical_specialty'], axis = 1)
# drop 'examide' and 'citoglipton' with same value 'No'
df = df.drop(['examide', 'citoglipton'], axis = 1)
# drop bad data with 3 '?' in diag
# drop died patient data which 'discharge_disposition_id' == 11 | 19 | 20 | 21 indicates 'Expired'
# drop 3 data with 'Unknown/Invalid' gender
drop_ID = set(df[(df['diag_1'] == '?') & (df['diag_2'] == '?') & (df['diag_3'] == '?')].index)
# drop_ID = set()
drop_ID = drop_ID.union(set(df[(df['discharge_disposition_id'] == 11) | (df['discharge_disposition_id'] == 19) | \
                               (df['discharge_disposition_id'] == 20) | (df['discharge_disposition_id'] == 21)].index))
drop_ID = drop_ID.union(df['gender'][df['gender'] == 'Unknown/Invalid'].index)
new_ID = list(set(df.index) - set(drop_ID))
df = df.iloc[new_ID]
print('Filtered numbers: ', df['encounter_id'].count())

"""
Creating/Merging features
"""
# merge total visits number
df['number_treatment'] = df['number_outpatient'] + df['number_emergency'] + df['number_inpatient']
# map
df['change'] = df['change'].replace('No', 0)
df['change'] = df['change'].replace("Ch", 1)

df['gender'] = df['gender'].replace('Male', 1)
df['gender'] = df['gender'].replace('Female', 0)

df['diabetesMed'] = df['diabetesMed'].replace('Yes', 1)
df['diabetesMed'] = df['diabetesMed'].replace('No', 0)

print('\n--Ages Counts--')
for i in range(10):
    df['age'] = df['age'].replace('[' + str(10 * i) + '-' + str((i + 1) * 10) + ')', i + 1)
print(df['age'].value_counts())

# calculate change times through 23 kinds of medicines
# high change times refer to higher prob to readmit
# 'num_med_changed' to counts medicine change
medicine = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'glipizide', 'glyburide', 
            'pioglitazone', 'rosiglitazone', 'acarbose', 'miglitol', 'insulin', 'glyburide-metformin', 'tolazamide', 
            'metformin-pioglitazone','metformin-rosiglitazone', 'glimepiride-pioglitazone', 'glipizide-metformin', 
            'troglitazone', 'tolbutamide', 'acetohexamide']

for med in medicine:
    tmp = med + 'temp'
    df[tmp] = df[med].apply(lambda x: 1 if (x == 'Down' or x == 'Up') else 0)

print('\n--Medicine Change Counts--')
df['num_med_changed'] = 0
for med in medicine:
    tmp = med + 'temp'
    df['num_med_changed'] += df[tmp]
    del df[tmp]
print(df['num_med_changed'].value_counts())

for med in medicine:
    df[med] = df[med].replace('No', 0)
    df[med] = df[med].replace('Steady', 1)
    df[med] = df[med].replace('Up', 1)
    df[med] = df[med].replace('Down', 1)

print('\n--Medicine Taken Counts--')
df['num_med_taken'] = 0
for med in medicine:
    df['num_med_taken'] += df[med]
print(df['num_med_taken'].value_counts())

# map
df['A1Cresult'] = df['A1Cresult'].replace('None', -1)
df['A1Cresult'] = df['A1Cresult'].replace('>8', 1)
df['A1Cresult'] = df['A1Cresult'].replace('>7', 1)
df['A1Cresult'] = df['A1Cresult'].replace('Norm', 0)

df['max_glu_serum'] = df['max_glu_serum'].replace('>200', 1)
df['max_glu_serum'] = df['max_glu_serum'].replace('>300', 1)
df['max_glu_serum'] = df['max_glu_serum'].replace('Norm', 0)
df['max_glu_serum'] = df['max_glu_serum'].replace('None', -1)

# simplify
# admission_type_id : [2, 7] -> 1, [6, 8] -> 5
print('\n--Admission Type Counts--')
a, b = [2, 7], [6, 8]
for i in a:
    df['admission_type_id'] = df['admission_type_id'].replace(i, 1)
for j in b:
    df['admission_type_id'] = df['admission_type_id'].replace(j, 5)
print(df['admission_type_id'].value_counts())

# discharge_disposition_id : [6, 8, 9, 13] -> 1, [3, 4, 5, 14, 22, 23, 24] -> 2,
#                            [12, 15, 16, 17] -> 10, [19, 20, 21] -> 11, [25, 26] -> 18
print('\n--Discharge Disposition Counts--')
a, b, c, d, e = [6, 8, 9, 13], [3, 4, 5, 14, 22, 23, 24], [12, 15, 16, 17], \
                [19, 20, 21], [25, 26]
for i in a:
    df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(i, 1)
for j in b:
    df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(j, 2)
for k in c:
    df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(k, 10)
# data of died patients have been dropped
# for p in d:
#     df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(p, 11)
for q in e:
    df['discharge_disposition_id'] = df['discharge_disposition_id'].replace(q, 18)
print(df['discharge_disposition_id'].value_counts())
# print(df['discharge_disposition_id'][df['discharge_disposition_id'] == 11].count())

# admission_source_id : [3, 2] -> 1, [5, 6, 10, 22, 25] -> 4,
#                       [15, 17, 20, 21] -> 9, [13, 14] -> 11
print('\n--Admission Source Counts--')
a, b, c, d = [3, 2], [5, 6, 10, 22, 25], [15, 17, 20, 21], [13, 14]
for i in a:
    df['admission_source_id'] = df['admission_source_id'].replace(i, 1)
for j in b:
    df['admission_source_id'] = df['admission_source_id'].replace(j, 4)
for k in c:
    df['admission_source_id'] = df['admission_source_id'].replace(k, 9)
for p in d:
    df['admission_source_id'] = df['admission_source_id'].replace(p, 11)
print(df['admission_source_id'].value_counts())

"""
Classify Diagnoses by ICD-9
"""
# create copy of diagnose
DUMMY = 'dummy_diag1'
df[DUMMY] = df['diag_1']
df[DUMMY] = df[DUMMY].replace('?', -1)
df.loc[df['diag_1'].str.contains('V'), [DUMMY]] = 0
df.loc[df['diag_1'].str.contains('E'), [DUMMY]] = 0
df[DUMMY] = df[DUMMY].astype(float)

# iterate
# iteritems(): Iterate over (column name, Series) pairs.
print('\n--Classify Diagnoses Counts--')
for index, row in df.iterrows():
    if (row[DUMMY] >= 1 and row[DUMMY] < 140):
        df.loc[index, DUMMY] = 1
    elif (row[DUMMY] >= 140 and row[DUMMY] < 240):
        df.loc[index, DUMMY] = 2
    elif (row[DUMMY] >= 240 and row[DUMMY] < 280):
        df.loc[index, DUMMY] = 3
    elif (row[DUMMY] >= 280 and row[DUMMY] < 290):
        df.loc[index, DUMMY] = 4
    elif (row[DUMMY] >= 290 and row[DUMMY] < 320):
        df.loc[index, DUMMY] = 5
    elif (row[DUMMY] >= 320 and row[DUMMY] < 390):
        df.loc[index, DUMMY] = 6
    elif (row[DUMMY] >= 390 and row[DUMMY] < 460):
        df.loc[index, DUMMY] = 7
    elif (row[DUMMY] >= 460 and row[DUMMY] < 520):
        df.loc[index, DUMMY] = 8
    elif (row[DUMMY] >= 520 and row[DUMMY] < 580):
        df.loc[index, DUMMY] = 9
    elif (row[DUMMY] >= 580 and row[DUMMY] < 630):
        df.loc[index, DUMMY] = 10
    elif (row[DUMMY] >= 630 and row[DUMMY] < 680):
        df.loc[index, DUMMY] = 11               
    elif (row[DUMMY] >= 680 and row[DUMMY] < 710):
        df.loc[index, DUMMY] = 12
    elif (row[DUMMY] >= 710 and row[DUMMY] < 740):
        df.loc[index, DUMMY] = 13
    elif (row[DUMMY] >= 740 and row[DUMMY] < 760):
        df.loc[index, DUMMY] = 14
    elif (row[DUMMY] >= 760 and row[DUMMY] < 780):
        df.loc[index, DUMMY] = 15
    elif (row[DUMMY] >= 780 and row[DUMMY] < 800):
        df.loc[index, DUMMY] = 16
    elif (row[DUMMY] >= 800 and row[DUMMY] < 1000):
        df.loc[index, DUMMY] = 17
    else:
        df.loc[index, DUMMY] = 0
print(df[DUMMY].value_counts())
# print(df[['diag_1', DUMMY]].head(15).T)

# save to csv
df.to_csv(RESULT_DATA)
