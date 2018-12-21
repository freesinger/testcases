import numpy as np
import pandas as pd
import statsmodels as sm
import matplotlib.pyplot as plt

from statistics import mode
from sklearn.preprocessing import MinMaxScaler

ORIGIN_DATA = '~/Desktop/Codes/Python_Testcases/Readmission_Prediction/dataset_diabetes/processed_data.csv'

df = pd.read_csv(ORIGIN_DATA)
print(df.shape)