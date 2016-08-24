import os
import pandas as pd
os.chdir('/Users/Evan/DataScience/TB_Nation/Datasets/')
files = os.listdir()

datasets = pd.DataFrame()
for i in range(1,len(files)):
    for j in os.listdir(files[i]):
        data = pd.read_excel(files[i]+'/'+ j ,skiprows=1).iloc[:1,0:5]
        data = data.rename(columns={'Unnamed: 0':'Area','发病数':'Incidence','死亡数':'Death','发病率':'Incidence_rate','死亡率':'Death_rate'})
        data['Year'],data['Month'],data['Day'] = files[i],j[4:6],'01'
        datasets = pd.concat([datasets,data])
# datasets.index=range(0,len(datasets))
datasets['Date'] = datasets['Year'] + datasets['Month'] + datasets['Day']
datasets.index = pd.to_datetime(datasets['Date'])
datasets = datasets.drop(['Day','Date'],axis=1)
datasets.head()

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline

from statsmodels.tsa.seasonal import seasonal_decompose
datasets = pd.read_excel('TB_nation.xlsx',index_col='Date')
datasets.head()
datasets.Incidence_rate.plot(figsize=(12,8), title= 'Monthly TB Incidence Rate', fontsize=14)
# plt.savefig('month_TB.png', bbox_inches='tight')
datasets_pred = datasets[datasets.index>='2014-01-1']
datasets = datasets[datasets.index<'2014-01-01']
datasets.shape
decomposition = seasonal_decompose(datasets.Incidence_rate,freq=12)
fig = plt.figure()
fig = decomposition.plot()
fig.set_size_inches(12,6)


