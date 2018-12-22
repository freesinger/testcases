import numpy as np
import pandas as pd
import statsmodels
import matplotlib.pyplot as plt
import scipy as sp
import seaborn as sns
import warnings
import graphviz
import pydotplus

from statistics import mode
from sklearn import tree
from sklearn.preprocessing import MinMaxScaler
from sklearn.exceptions import DataConversionWarning
from matplotlib.colors import ListedColormap
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from imblearn.over_sampling import SMOTE
from sklearn.tree import DecisionTreeClassifier
from collections import Counter
from PIL import Image
from sklearn.ensemble import RandomForestClassifier

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

i = ['encounter_id', 'patient_nbr', 'gender', 'age', 'admission_type_id', 'discharge_disposition_id',
     'admission_source_id', 'A1Cresult', 'max_glu_serum', 'metformin', 'repaglinide', 'nateglinide',
     'chlorpropamide', 'glimepiride', 'acetohexamide', 'glipizide', 'glyburide', 'tolbutamide', 'pioglitazone',
     'rosiglitazone', 'acarbose','miglitol', 'troglitazone', 'tolazamide', 'insulin', 'glyburide-metformin', 
     'glipizide-metformin', 'glimepiride-pioglitazone', 'metformin-rosiglitazone','metformin-pioglitazone', 
     'change', 'diabetesMed', 'dummy_diag1']
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

df2 = df2[(np.abs(sp.stats.zscore(df2[numerics])) < 3).all(axis=1)]

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

X_train, X_dev, Y_train, Y_dev = train_test_split(train_input, train_output, test_size=0.20, random_state=0)
log_reg = LogisticRegression(fit_intercept=True, penalty='l1')
# print("Cross Validation Score: {:.2%}". format(np.mean(cross_val_score(log_reg, X_train, Y_train, cv=10))))
# Cross Validation Score: 91.50%
log_reg.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(log_reg.score(X_dev, Y_dev)))
# Dev Set score: 91.84%

Y_dev_predict = log_reg.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name='Actual'), pd.Series(Y_dev_predict, name='Predict'), margins=True))
# Predict     0  1   All
# Actual                
# 0        1602  1  1603
# 1         158  0   158
# All      1760  1  1761

# print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict))) # 0.92
# print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict))) # 0.00
# print("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict))) # 0.00

# Data balancing using SMOTE

# print('Original dataset shape {}'.format(Counter(train_output)))
sm = SMOTE(random_state=20)
train_input_new, train_output_new = sm.fit_resample(train_input, train_output)
# print('New dataset shape {}'.format(Counter(train_output_new)))

train_input_new = pd.DataFrame(train_input_new, columns=list(train_input.columns))
X_train, X_dev, Y_train, Y_dev = train_test_split(train_input_new, train_output_new, test_size=0.20, random_state=0)
log_reg = LogisticRegression(fit_intercept=True, penalty='l1')
# print("Cross Validation Score: {:.2%}". format(np.mean(cross_val_score(log_reg, X_train, Y_train, cv=10))))
# Cross Validation Score: 60.47%

log_reg.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(log_reg.score(X_dev, Y_dev)))
# Dev Set score: 60.43%

Y_dev_predict = log_reg.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name='Actual'), pd.Series(Y_dev_predict, name='Predict'), margins=True))
# Predict      0      1    All
# Actual                      
# 0         7120   4154  11274
# 1         4784   6530  11314
# All      11904  10684  22588

# print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict))) # 0.60
# print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict))) # 0.61
# print("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict))) # 0.58
# print('AUC is {0:.2f}'.format(roc_auc_score(Y_dev, Y_dev_predict))) # 0.60

accuracy_logreg = accuracy_score(Y_dev, Y_dev_predict)
precision_logreg = precision_score(Y_dev, Y_dev_predict)
recall_logreg = recall_score(Y_dev, Y_dev_predict)
auc_logreg = roc_auc_score(Y_dev, Y_dev_predict)

import statsmodels.api as sm
logit = sm.Logit(Y_train, X_train)

'''
result = logit.fit()
print(result.summary())

logit_coefs = pd.DataFrame(result.params)
logit_coefs.reset_index(inplace=True)
logit_coefs.columns = ["Feature", "Coefficient"]
logit_pvals = pd.DataFrame(result.pvalues)
logit_pvals.reset_index(inplace=True)
logit_pvals.columns = ["Feature", "pVal"]

logit_coefs = logit_coefs.merge(logit_pvals, how="inner", on=["Feature"])
logit_coefs = logit_coefs[logit_coefs.pVal <0.01]
logit_coefs.sort_values(by='Coefficient', ascending=False)
'''

#---------------------------------------------------------------
# Decision Tree
feature_set_1_no_int = ['age', 'time_in_hospital', 'num_procedures', 'num_medications', 'number_outpatient_log1p', 
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

feature_set_2_no_int = ['age', 'time_in_hospital', 'num_lab_procedures', 'num_procedures', 'service_utilization_log1p', 
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

train_input = df_pd[feature_set_1_no_int]
train_output = df_pd['readmitted']
# print(df_pd['readmitted'].value_counts())
# 0    56469
# 1     5199
# Name: readmitted, dtype: int64

# Data balancing applied using SMOTE
# print('Original dataset shape {}'.format(Counter(train_output)))
# Original dataset shape Counter({0: 56469, 1: 5199})
smt = SMOTE(random_state=20)
train_input_new, train_output_new = smt.fit_sample(train_input, train_output)
# print('New dataset shape {}'.format(Counter(train_output_new)))
# New dataset shape Counter({0: 56469, 1: 56469})
train_input_new = pd.DataFrame(train_input_new, columns = list(train_input.columns))
X_train, X_dev, Y_train, Y_dev = train_test_split(train_input_new, train_output_new, test_size=0.20, random_state=0)

dte = DecisionTreeClassifier(max_depth=28, criterion = "entropy", min_samples_split=10)
# print("Cross Validation score: {:.2%}".format(np.mean(cross_val_score(dte, X_train, Y_train, cv=10))))
# Cross Validation score: 91.27%
dte.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(dte.score(X_dev, Y_dev)))
# Dev Set score: 91.22%

Y_dev_predict = dte.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name = 'Actual'), pd.Series(Y_dev_predict, name = 'Predict'), margins = True))
# Predict      0      1    All
# Actual                      
# 0        10492    782  11274
# 1         1191  10123  11314
# All      11683  10905  22588

'''
print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict)))
print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict)))
print("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict)))
print("AUC is {0:.2f}".format(roc_auc_score(Y_dev, Y_dev_predict)))
'''
# Accuracy is 0.91
# Precision is 0.93
# Recall is 0.89
# AUC is 0.91

accuracy_dte = accuracy_score(Y_dev, Y_dev_predict)
precision_dte = precision_score(Y_dev, Y_dev_predict)
recall_dte = recall_score(Y_dev, Y_dev_predict)
auc_dte = roc_auc_score(Y_dev, Y_dev_predict)

dot_dt_q2 = tree.export_graphviz(dte, out_file="dt_q2.dot", feature_names=X_train.columns, max_depth=2,
                                 class_names=["No","Readm"], filled=True, rounded=True, special_characters=True)
graph_dt_q2 = pydotplus.graph_from_dot_file('dt_q2.dot')
# Image(graph_dt_q2.create_png())

# Create list of top most features based on importance
'''
feature_names = X_train.columns
feature_imports = dte.feature_importances_
most_imp_features = pd.DataFrame([f for f in zip(feature_names,feature_imports)], columns=["Feature", "Importance"]).nlargest(10, "Importance")
most_imp_features.sort_values(by="Importance", inplace=True)
# print(most_imp_features)
plt.figure(figsize=(10,6))
plt.barh(range(len(most_imp_features)), most_imp_features.Importance, align='center', alpha=0.8)
plt.yticks(range(len(most_imp_features)), most_imp_features.Feature, fontsize=14)
plt.xlabel('Importance')
plt.title('Most important features - Decision Tree (entropy function, complex model)')
plt.show()
'''

dtg = DecisionTreeClassifier(max_depth=28, criterion = "gini", min_samples_split=10)
# print("Cross Validation Score: {:.2%}".format(np.mean(cross_val_score(dtg, X_train, Y_train, cv=10))))
# Cross Validation Score: 91.21%
dtg.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(dtg.score(X_dev, Y_dev)))
# Dev Set score: 91.63%


Y_dev_predict = dtg.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name = 'Actual'), pd.Series(Y_dev_predict, name = 'Predict'), margins = True))
# Predict      0      1    All
# Actual                      
# 0        10557    717  11274
# 1         1151  10163  11314
# All      11708  10880  22588

# print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict))) # 0.92
# print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict))) # 0.93
# rint("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict))) # 0.90
# print("AUC is {0:.2f}".format(roc_auc_score(Y_dev, Y_dev_predict))) # 0.92

accuracy_dtg = accuracy_score(Y_dev, Y_dev_predict)
precision_dtg = precision_score(Y_dev, Y_dev_predict)
recall_dtg = recall_score(Y_dev, Y_dev_predict)
auc_dtg = roc_auc_score(Y_dev, Y_dev_predict)


#-----------------------------------------------
# Random Forest
train_input = df_pd[feature_set_1_no_int]
train_output = df_pd['readmitted']

# Data balancing applied using SMOTE

# print('Original dataset shape {}'.format(Counter(train_output)))
# Original dataset shape Counter({0: 56469, 1: 5199})
smt = SMOTE(random_state=20)
train_input_new, train_output_new = smt.fit_sample(train_input, train_output)
# print('New dataset shape {}'.format(Counter(train_output_new)))
# New dataset shape Counter({0: 56469, 1: 56469})
train_input_new = pd.DataFrame(train_input_new, columns = list(train_input.columns))
X_train, X_dev, Y_train, Y_dev = train_test_split(train_input_new, train_output_new, test_size=0.20, random_state=0)

forrest = RandomForestClassifier(n_estimators = 10, max_depth=25, criterion = "gini", min_samples_split=10)
# print("Cross Validation score: {:.2%}".format(np.mean(cross_val_score(forrest, X_train, Y_train, cv=10))))
# Cross Validation score: 94.12%
forrest.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(forrest.score(X_dev, Y_dev)))
# Dev Set score: 94.07%


Y_dev_predict = forrest.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name = 'Actual'), pd.Series(Y_dev_predict, name = 'Predict'), margins = True))
# Predict      0      1    All
# Actual                      
# 0        11067    207  11274
# 1         1120  10194  11314
# All      12187  10401  22588

'''
print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict)))
print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict)))
print("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict)))
print("AUC is {0:.2f}".format(roc_auc_score(Y_dev, Y_dev_predict)))
'''
# Accuracy is 0.94
# Precision is 0.98
# Recall is 0.90
# AUC is 0.94

accuracy_forreste = accuracy_score(Y_dev, Y_dev_predict)
precision_forreste = precision_score(Y_dev, Y_dev_predict)
recall_forreste = recall_score(Y_dev, Y_dev_predict)
auc_forreste = roc_auc_score(Y_dev, Y_dev_predict)

# Create list of top most features based on importance
'''
feature_names = X_train.columns
feature_imports = forrest.feature_importances_
most_imp_features = pd.DataFrame([f for f in zip(feature_names,feature_imports)], columns=["Feature", "Importance"]).nlargest(10, "Importance")
most_imp_features.sort_values(by="Importance", inplace=True)
plt.figure(figsize=(10,6))
plt.barh(range(len(most_imp_features)), most_imp_features.Importance, align='center', alpha=0.8)
plt.yticks(range(len(most_imp_features)), most_imp_features.Feature, fontsize=14)
plt.xlabel('Importance')
plt.title('Most important features - Random Forest (Gini function, complex model)')
plt.show()
'''

forrest = RandomForestClassifier(n_estimators = 10, max_depth=25, criterion = "gini", min_samples_split=10)
# print("Cross Validation score: {:.2%}".format(np.mean(cross_val_score(forrest, X_train, Y_train, cv=10))))
# Cross Validation score: 94.04%
forrest.fit(X_train, Y_train)
# print("Dev Set score: {:.2%}".format(forrest.score(X_dev, Y_dev)))
# Dev Set score: 94.03%

Y_dev_predict = forrest.predict(X_dev)
# print(pd.crosstab(pd.Series(Y_dev, name = 'Actual'), pd.Series(Y_dev_predict, name = 'Predict'), margins = True))
# Predict      0      1    All
# Actual
# 0        11060    214  11274
# 1         1134  10180  11314
# All      12194  10394  22588

'''
print("Accuracy is {0:.2f}".format(accuracy_score(Y_dev, Y_dev_predict)))
print("Precision is {0:.2f}".format(precision_score(Y_dev, Y_dev_predict)))
print("Recall is {0:.2f}".format(recall_score(Y_dev, Y_dev_predict)))
print("AUC is {0:.2f}".format(roc_auc_score(Y_dev, Y_dev_predict)))
'''
# Accuracy is 0.94
# Precision is 0.98
# Recall is 0.90
# AUC is 0.94

accuracy_forrestg = accuracy_score(Y_dev, Y_dev_predict)
precision_forrestg = precision_score(Y_dev, Y_dev_predict)
recall_forrestg = recall_score(Y_dev, Y_dev_predict)
auc_forrestg = roc_auc_score(Y_dev, Y_dev_predict)


# Create list of top most features based on importance
'''
feature_names = X_train.columns
feature_imports = forrest.feature_importances_
most_imp_features = pd.DataFrame([f for f in zip(feature_names,feature_imports)], columns=["Feature", "Importance"]).nlargest(10, "Importance")
most_imp_features.sort_values(by="Importance", inplace=True)
plt.figure(figsize=(10,6))
plt.barh(range(len(most_imp_features)), most_imp_features.Importance, align='center', alpha=0.8)
plt.yticks(range(len(most_imp_features)), most_imp_features.Feature, fontsize=14)
plt.xlabel('Importance')
plt.title('Most important features - Random Forest (gini) (Question 2 - complex model)')
plt.show()
'''


# plotting the accuracy for training and test
plt.figure(figsize=(14, 5))
ax = plt.subplot(111)

models = ['Logistic Regression', 'Decision Tree Gini', 'Decision Tree Entropy', 'Random Forests Gini', 'Random Forests Entropy' ]
values = [accuracy_logreg, accuracy_dtg, accuracy_dte, accuracy_forrestg, accuracy_forreste]
model = np.arange(len(models))

plt.bar(model, values, align='center', width = 0.15, alpha=0.7, color = 'red', label= 'accuracy')
plt.xticks(model, models)



ax = plt.subplot(111)

models = ['Logistic Regression', 'Decision Tree Gini', 'Decision Tree Entropy', 'Random Forests Gini', 'Random Forests Entropy' ]
values = [precision_logreg, precision_dtg, precision_dte, precision_forrestg, precision_forreste]
model = np.arange(len(models))

plt.bar(model+0.15, values, align='center', width = 0.15, alpha=0.7, color = 'blue', label = 'precision')
plt.xticks(model, models)



ax = plt.subplot(111)

models = ['Logistic Regression', 'Decision Tree Gini', 'Decision Tree Entropy', 'Random Forests Gini', 'Random Forests Entropy' ]
values = [recall_logreg, recall_dtg, recall_dte, recall_forrestg, recall_forreste]
model = np.arange(len(models))

plt.bar(model+0.3, values, align='center', width = 0.15, alpha=0.7, color = 'green', label = 'recall')
plt.xticks(model, models)



ax = plt.subplot(111)

models = ['Logistic Regression', 'Decision Tree Gini', 'Decision Tree Entropy', 'Random Forests Gini', 'Random Forests Entropy' ]
values = [auc_logreg, auc_dtg, auc_dte, auc_forrestg, auc_forreste]
model = np.arange(len(models))

plt.bar(model+0.45, values, align='center', width = 0.15, alpha=0.7, color = 'orange', label = 'AUC')
plt.xticks(model, models)



plt.ylabel('Performance Metrics for Different models')
plt.title('Model')
    
# removing the axis on the top and right of the plot window
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend()

plt.show()