
# coding: utf-8

# In[1]:


import pandas as pd
import os
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from LoadData import load_data


# In[2]:


dirname = os.getcwd()
pth = os.path.join(dirname, 'CMAPSSData')

print('loading data...')
dc = load_data(pth)
print('done')


# In[3]:


# get the first data set training data
df = dc['FD_001']['df_train'].copy()


# In[4]:


# get the time of the last available measurement for each unit
mapper = {}
for unit_nr in df['unit_nr'].unique():
    mapper[unit_nr] = df['time'].loc[df['unit_nr'] == unit_nr].max()
    
# calculate RUL = time.max() - time_now for each unit
df['RUL'] = df['unit_nr'].apply(lambda nr: mapper[nr]) - df['time']


# In[5]:


cols_nan = df.columns[df.isna().any()].tolist()
print('Columns with all nan: \n' + str(cols_nan) + '\n')

cols_const = [ col for col in df.columns if len(df[col].unique()) <= 2 ]
print('Columns with all const values: \n' + str(cols_const) + '\n')


# In[6]:


df = df.drop(columns=cols_const + cols_nan)


# In[11]:


length = [(nr, d.RUL.max()) for nr, d in df.groupby('unit_nr')]
#plt.plot(df.unit_nr.unique(), length)
plt.plot(df.unit_nr.unique()[60:70], length[60:70])
print()


# In[19]:


df_sub = None

for nr, d in df.groupby('unit_nr'):
    if df_sub is None or d.RUL.max() > df_sub.RUL.max():
        df_sub = d

df_sub = df_sub.set_index('time')


# In[20]:


_ = df_sub.plot(subplots=True, figsize=(15,15))


# In[23]:


df_sub2 = df_sub[[c for c in df_sub.columns if c.startswith('s')]]
_ = df_sub2.plot(subplots=True, figsize=(15,15))


# In[ ]:


def rolling_mean(df, n):
    cols_sensors = [c for c in df.columns if c.startswith('sensor')]
    df_new = pd.DataFrame(columns=df.columns)
    
    for nr, d in df.groupby('unit_nr'):
        d.loc[:,cols_sensors] = d[cols_sensors].rolling(n, min_periods=1).mean()
        df_new.append(d)
    return df_new


d = rolling_mean(df, 10)
    
fig, axes = plt.subplots(len(d.columns), 1, figsize=(15,15))
axes = axes.flatten()
for ax, col in zip(axes, df_sub2.columns):
    ax.plot(d.index, d[col].values, linestyle='--')
    ax.plot(df.index, df[col].values)
            