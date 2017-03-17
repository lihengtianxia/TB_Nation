
#-*- coding: utf-8 -*-

import os
os.chdir('/Users/Evan/DataScience/TB_GM/')
files = os.listdir()

from GM11 import GM11

import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
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

# print(u'后残差比:',f[4],';',u'小残差率',f[5])
