#-*- coding: utf-8 -*-
import os
os.chdir('/Users/Evan/DataScience/TB_Nation/')
files = os.listdir()

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set_style('white')
import statsmodels.api as sm
from statsmodels.tsa.stattools import acf
from statsmodels.tsa.stattools import pacf
from statsmodels.tsa.stattools import adfuller
from neupy.estimators import mse
from datetime import date
import datetime
from dateutil.relativedelta import relativedelta
from test_stationarity import test_stationarity
from GM11 import GM11
import warnings
warnings.filterwarnings("ignore")

datasets = pd.read_excel('TB_nation.xlsx',index_col='Date')
datasets = datasets[datasets.index > '2004-12-01']

datasets_pred = datasets[datasets.index >= '2013-01-1']
datasets = datasets[datasets.index < '2013-01-01']

datasets['first_diff'] = datasets.Incidence_rate - datasets.Incidence_rate.shift(1)
datasets['seasonal_difference'] = datasets.Incidence_rate - datasets.Incidence_rate.shift(12)
datasets['seasonal_first_difference'] = datasets.first_diff-datasets.first_diff.shift(12)

fig = plt.figure(figsize=(8,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(datasets.seasonal_first_difference.iloc[13:],lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(datasets.seasonal_first_difference.iloc[13:],lags=40, ax=ax2)
fig.savefig('Autocorrection.png',dpi= 600)

mod = sm.tsa.SARIMAX(datasets.Incidence_rate, trend='n', order=(0,1,1), seasonal_order=(0,1,1,12))
results = mod.fit()
print(results.summary())

dta = pd.concat([datasets, datasets_pred])[['Incidence','Incidence_rate','Year','Month']]
dta['forecast'] = results.predict(start=13,end=131,dynamic=False)
dta['forecast'] = results.predict(start = 13, end= 131, dynamic= False)
dta[['Incidence_rate','forecast']].plot(figsize=(8, 6))

start = datetime.datetime.strptime("2015-01-01", "%Y-%m-%d")
date_list = [start + relativedelta(months=x) for x in range(0,132)]
future = pd.DataFrame(index=date_list, columns= dta.columns)
TB_future = pd.concat([dta,future])

TB_future['forecast'] = results.predict(start = 13, end = 263, dynamic= False)
TB_future['Year'] = TB_future.index.year
TB_future[['forecast','Incidence_rate','Year']].groupby('Year').apply(lambda x:np.sum(x))[['forecast','Incidence_rate']]
TB_future[['forecast','Incidence_rate']].plot(figsize=(10,6))

TB_year = TB_future.groupby('Year').apply(np.sum)[['forecast','Incidence_rate']]

#-*- coding: utf-8 -*-

import os
os.chdir('/Users/Evan/DataScience/TB_GM/')
files = os.listdir()

from GM11 import GM11

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
sns.set_style('white')

inputfile = './data/nation_TB1.csv'
nation = pd.read_csv(inputfile)[['incidence rate']]
nation.index=range(2005,2015)

for k in range(2015,2026):
    nation.loc[k] = None

nation['incidence_rate'] = None

for k in range(2005,2026):
    f = GM11(nation['incidence rate'].loc[range(2005,2015)].as_matrix())
    nation['incidence_rate'].loc[k] = f[0](k-2005+1).round(2)
nation

data = nation.join(TB_year,how='outer')
data['error_ARIMA']= data['incidence rate'] - data['forecast']
data['error_GM']= data['incidence rate'] - data['incidence_rate']

data['error_GM_rate'] = data['error_GM']/data['incidence rate']*100
data['error_ARIMA_rate'] = data['error_ARIMA']/data['incidence rate']*100
