import numpy as np
import pandas as pd
import statsmodels as sm
import matplotlib.pyplot as plt
import warnings

from statistics import mode
from sklearn.preprocessing import MinMaxScaler
from sklearn.exceptions import DataConversionWarning

ORIGIN_DATA = '~/Desktop/Codes/Python_Testcases/Readmission_Prediction/dataset_diabetes/processed_data.csv'

df = pd.read_csv(ORIGIN_DATA)
df = df.drop(['Unnamed: 0'], axis=1)
print(df.shape)

# ignore some warnings
pd.set_option('display.max_columns', None)
pd.options.mode.chained_assignment = None
warnings.filterwarnings(action='ignore', category=DataConversionWarning)
warnings.filterwarnings(action='ignore', category=FutureWarning)
# print(df.head(10).T)
# print(df.dtypes)

# convert data type of nominal features in dataframe to 'object' type

i = ['encounter_id', 'patient_nbr', 'gender', 'age', 'admission_type_id', 'discharge_disposition_id', 'admission_source_id',\
     'A1Cresult', 'max_glu_serum', 'metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', \
     'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose','miglitol', 'troglitazone', \
     'tolazamide', 'insulin', 'glyburide-metformin', 'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone',\
     'metformin-pioglitazone', 'change', 'diabetesMed', 'dummy_diag1']
df[i] = df[i].astype('object')
# print(df.dtypes)

L1 = np.random.randint(1,10,20)
L2 = np.random.randint(1,20,20)

datframe = pd.DataFrame()
datframe['L1'] = L1
datframe['L2'] = L2
# Compute pairwise correlation of columns

# print(datframe.corr())
scaler = MinMaxScaler()
datframe = pd.DataFrame(scaler.fit_transform(datframe), columns=['L1', 'L2'])
# print(datframe.corr())

# convert age type back to int

df['age'] = df['age'].astype('int64')
# map

age_dict = {1:5, 2:15, 3:25, 4:35, 5:45, 6:55, 7:65, 8:75, 9:85, 10:95}
df['age'] = df.age.map(age_dict)
# print(df.age.value_counts())

# get all numeric feat
num_col = list(set(list(df._get_numeric_data().columns)) - {'readmitted'})
# print(num_col)

# Removing skewness and kurtosis using log transformation if it is above a threshold value (2)
statdataframe = pd.DataFrame()
statdataframe['numeric_column'] = num_col
skew_bef, skew_after = list(), list()
kurt_bef, kurt_after = list(), list()
standard_deviation_before, standard_deviation_after = list(), list()
log_transform_needed, log_type = list(), list()

for i in num_col:
    skewval = df[i].skew()
    skew_bef.append(skewval)

    kurtval = df[i].kurtosis()
    kurt_bef.append(kurtval)

    sdval = df[i].std()
    standard_deviation_before.append(sdval)

    if (abs(skewval) > 2) & (abs(kurtval) > 2):
        log_transform_needed.append("Yes")
        
        if len(df[df[i] == 0]) / len(df) <= 0.02:
            log_type.append('log')
            skewvalnnew = np.log(pd.DataFrame(df[df[i] > 0]))
            kurtvalnew = np.log(pd.DataFrame(df[df[i] > 0])[i]).kurtosis()
            kurt_after.append(kurtvalnew)
            
            sdvalnew = np.log(pd.DataFrame(df[df[i] > 0])[i]).std()
            standard_deviation_after.append(sdvalnew)
            
        else:
            log_type.append('log1p')
            skewvalnew = np.log1p(pd.DataFrame(df[df[i] >= 0])[i]).skew()
            skew_after.append(skewvalnew)
        
            kurtvalnew = np.log1p(pd.DataFrame(df[df[i] >= 0])[i]).kurtosis()
            kurt_after.append(kurtvalnew)
            
            sdvalnew = np.log1p(pd.DataFrame(df[df[i] >= 0])[i]).std()
            standard_deviation_after.append(sdvalnew)
            
    else:
        log_type.append('NA')
        log_transform_needed.append('No')
        
        skew_after.append(skewval)
        kurt_after.append(kurtval)
        standard_deviation_after.append(sdval)

statdataframe['skew_before'] = skew_bef
statdataframe['kurtosis_before'] = kurt_bef
statdataframe['standard_deviation_before'] = standard_deviation_before
statdataframe['log_transform_needed'] = log_transform_needed
statdataframe['log_type'] = log_type
statdataframe['skew_after'] = skew_after
statdataframe['kurtosis_after'] = kurt_after
statdataframe['standard_deviation_after'] = standard_deviation_after
# print(statdataframe)

# performing the log transformation for the columns determined to be needing it above.

for i in range(len(statdataframe)):
    if statdataframe['log_transform_needed'][i] == 'Yes':
        colname = str(statdataframe['numeric_column'][i])
        
        if statdataframe['log_type'][i] == 'log':
            df = df[df[colname] > 0]
            df[colname + "_log"] = np.log(df[colname])
            
        elif statdataframe['log_type'][i] == 'log1p':
            df = df[df[colname] >= 0]
            df[colname + "_log1p"] = np.log1p(df[colname])

df = df.drop(['number_outpatient', 'number_inpatient', 'number_emergency', 'number_treatment'], axis = 1)
# print(df.shape)

# get list of only numeric features
numerics = list(set(list(df._get_numeric_data().columns))- {'readmitted'})
# print(numerics, num_col)

# show list of features that are categorical
df.encounter_id = df.encounter_id.astype('int64')
df.patient_nbr = df.patient_nbr.astype('int64')
df.diabetesMed = df.diabetesMed.astype('int64')
df.change = df.change.astype('int64')

# convert data type of nominal features in dataframe to 'object' type for aggregating
i = ['metformin', 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'acetohexamide', \
     'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone', 'rosiglitazone', 'acarbose','miglitol', \
     'troglitazone', 'tolazamide', 'insulin', 'glyburide-metformin', 'glipizide-metformin', \
     'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone','A1Cresult']
df[i] = df[i].astype('int64')
# print(df.dtypes)

# print(df.A1Cresult.value_counts())

dfcopy = df.copy(deep=True)
df = dfcopy.copy(deep=True)
df['readmitted'] = df['readmitted'].apply(lambda x: 0 if x == 2 else x)

# drop individual diagnosis columns that have too granular disease information
df.drop(['diag_1', 'diag_2', 'diag_3'], axis=1, inplace=True)
# print(df.head(5), df.shape)

# Possible actual co-variance
interactionterms = [('num_medications','time_in_hospital'),
('num_medications','num_procedures'),
('time_in_hospital','num_lab_procedures'),
('num_medications','num_lab_procedures'),
('num_medications','number_diagnoses'),
('age','number_diagnoses'),
('change','num_medications'),
('number_diagnoses','time_in_hospital'),
('num_medications','num_med_changed')]

for inter in interactionterms:
    name = inter[0] + '|' + inter[1]
    df[name] = df[inter[0]] * df[inter[1]]
# print(df[['num_medications','time_in_hospital', 'num_medications|time_in_hospital']].head())

#-------------------------------
datf = pd.DataFrame()
datf['features'] = numerics
datf['std_dev'] = datf['features'].apply(lambda x: df[x].std())
datf['mean'] = datf['features'].apply(lambda x: df[x].mean())

# Logical order: duplicate removal, then outlier removal followed by scaling

# dropping multiple encounters while keeping either first or last encounter of these patients
df2 = df.drop_duplicates(subset= ['patient_nbr'], keep = 'first')
# print(df2.shape)
# (70435, 55)

# standardize function
def standardize(raw_data):
    return ((raw_data - np.mean(raw_data, axis = 0)) / np.std(raw_data, axis = 0))

df2[numerics] = standardize(df2[numerics])
import scipy as sp
df2 = df2[(np.abs(sp.stats.zscore(df2[numerics])) < 3).all(axis=1)]

import seaborn as sns
from matplotlib.colors import ListedColormap
# my_cmap = ListedColormap(sns.color_palette("RdYlGn", n_colors=15).as_hex())
# my_cmap = ListedColormap(sns.diverging_palette(150, 250, sep=120, n=28, center="light").as_hex())

my_cmap = ListedColormap(sns.light_palette((250, 100, 50), input="husl", n_colors=50).as_hex())
# drop some columns due to their means is round to 0
# table = df.drop(['acetohexamide','tolbutamide', 'troglitazone', 'glipizide-metformin', 
#                  'glimepiride-pioglitazone', 'metformin-rosiglitazone', 'metformin-pioglitazone',
#                  'patient_nbr', 'encounter_id', 'service_utilization_log1p'], axis = 1).corr(method='pearson')
table = df2.drop(['patient_nbr', 'encounter_id'], axis=1).corr(method='pearson')
table.style.background_gradient(cmap=my_cmap, axis = 0)


pd.options.display.max_rows = 400

c = df2.corr().abs()
s = c.unstack()
# print(s.shape)
# (2304,)
so = s.sort_values(ascending=False)
# print(so[38:120])

df2['dummy_diag1'] = df2['dummy_diag1'].astype('object')
df_pd = pd.get_dummies(df2, columns=['race', 'gender', 'admission_type_id', 'discharge_disposition_id',
                                     'admission_source_id', 'max_glu_serum', 'A1Cresult', 'dummy_diag1'], drop_first = True)

non_num_cols = ['race', 'gender', 'admission_type_id', 'discharge_disposition_id', 'admission_source_id', 'max_glu_serum', 'A1Cresult', 'dummy_diag1' ]
num_cols = list(set(list(df._get_numeric_data().columns))- {'readmitted', 'change'})
# print(num_cols) 

# new_non_num_cols 
new_non_num_cols = []
for i in non_num_cols:
    for j in df_pd.columns:
        if i in j:
            new_non_num_cols.append(j)
# print(new_non_num_cols)

l = []
for feature in list(df_pd.columns):
    if '|' in feature:
        l.append(feature)
# print(l)

#--------------------------------------
# Modeling
feature_set_1 = ['age', 'time_in_hospital', 'num_procedures', 'num_medications', 'number_outpatient_log1p', 
                 'number_emergency_log1p', 'number_inpatient_log1p', 'number_diagnoses', 'metformin', 
                 'repaglinide', 'nateglinide', 'chlorpropamide', 'glimepiride', 'glipizide', 'glyburide',
                 'pioglitazone', 'rosiglitazone', 'acarbose', 'tolazamide', 'insulin', 'glyburide-metformin',
                 'race_AfricanAmerican', 'race_Asian', 'race_Caucasian', 'race_Hispanic', 'race_Other', 
                 'gender_1', 'admission_type_id_3', 'admission_type_id_4', 'admission_type_id_5', 
                 'discharge_disposition_id_2', 'discharge_disposition_id_7', 'discharge_disposition_id_10', 
                 'discharge_disposition_id_18', 'discharge_disposition_id_27', 'discharge_disposition_id_28', 
                 'admission_source_id_4', 'admission_source_id_7', 'admission_source_id_8', 'admission_source_id_9', 
                 'admission_source_id_11', 'max_glu_serum_0', 'max_glu_serum_1', 'A1Cresult_0', 'A1Cresult_1', 
                 'dummy_diag1_1.0', 'dummy_diag1_2.0', 'dummy_diag1_3.0', 'dummy_diag1_4.0', 'dummy_diag1_5.0', 
                 'dummy_diag1_6.0', 'dummy_diag1_7.0', 'dummy_diag1_8.0', 'dummy_diag1_9.0', 'dummy_diag1_10.0', 
                 'dummy_diag1_11.0', 'dummy_diag1_12.0', 'dummy_diag1_13.0', 'dummy_diag1_14.0', 'dummy_diag1_16.0', 
                 'dummy_diag1_17.0']
# print(len(feature_set_1)) : 61

feature_set_2 = ['age', 'time_in_hospital', 'num_lab_procedures', 'num_procedures', 'service_utilization_log1p', 
                 'number_diagnoses', 'num_med_taken', 'race_AfricanAmerican', 'race_Asian', 'race_Caucasian', 'race_Hispanic',
                 'race_Other', 'gender_1', 'A1Cresult_0', 'A1Cresult_1', 'admission_type_id_3', 'admission_type_id_4',
                 'admission_type_id_5', 'discharge_disposition_id_2', 'discharge_disposition_id_7',
                 'discharge_disposition_id_10', 'discharge_disposition_id_18', 'admission_source_id_4',
                 'admission_source_id_7', 'admission_source_id_8', 'admission_source_id_9', 'admission_source_id_11',
                 'num_med_changed','num_medications|time_in_hospital', 'num_medications|num_procedures', 
                 'time_in_hospital|num_lab_procedures', 'num_medications|num_lab_procedures', 
                 'num_medications|number_diagnoses', 'age|number_diagnoses', 'change|num_medications', 
                 'number_diagnoses|time_in_hospital', 'num_medications|num_med_changed', 'dummy_diag1_1.0', 
                 'dummy_diag1_2.0', 'dummy_diag1_3.0', 'dummy_diag1_4.0', 'dummy_diag1_5.0', 'dummy_diag1_6.0', 
                 'dummy_diag1_7.0', 'dummy_diag1_8.0', 'dummy_diag1_9.0', 'dummy_diag1_10.0', 'dummy_diag1_11.0', 
                 'dummy_diag1_12.0', 'dummy_diag1_13.0', 'dummy_diag1_14.0', 'dummy_diag1_16.0', 'dummy_diag1_17.0']                 
# print(len(feature_set_2)) : 53

'''
Apply Feature Set 1
'''
train_input = df_pd[feature_set_1]
train_output = df_pd['readmitted']

# print(df_pd['readmitted'].value_counts())

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

X_train, X_dev, Y_train, Y_dev = train_test_split(train_input, train_output, test_size=0.20, random_state=0)
log_reg = LogisticRegression(fit_intercept=True, penalty='l1')
print("Cross Validation Score: {:.2%}". format(np.mean(cross_val_score(log_reg, X_train, Y_train, cv=10))))
log_reg.fit(X_train, Y_train)
print("Dev Set score: {:.2%}".format(log_reg.score(X_dev, Y_dev)))