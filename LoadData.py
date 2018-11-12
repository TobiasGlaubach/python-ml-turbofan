# -*- coding: utf-8 -*-
"""
Created on Mon Nov 12 14:04:23 2018

@author: GLA_A
"""

#%%

import pandas as pd
import os
    
#%%
def load_data(pth, names=None, n_data_sets=4):
    
    if names is None:
        names = ['unit_nr', 'time', 'os_1', 'os_2', 'os_3']
        names += ['sensor_{0:02d}'.format(s + 1) for s in range(26)]
        
    dc = {}
    
    for i in range(n_data_sets):
        p = os.path.join(pth, 'RUL_FD00{}.txt'.format(i+1))
        df_RUL = pd.read_csv(p, sep= ' ', header=None, names=['RUL_actual'], index_col=False)
        p = os.path.join(pth, 'train_FD00{}.txt'.format(i+1))
        df_train = pd.read_csv(p, sep= ' ', header=None, names=names, index_col=False)
        p = os.path.join(pth, 'test_FD00{}.txt'.format(i+1))
        df_test = pd.read_csv(p, sep= ' ', header=None, names=names, index_col=False)
        s = 'FD_00{}'.format(i+1)
        dc[s] = {'df_RUL': df_RUL, 'df_train': df_train, 'df_test': df_test}
        
        
    return dc
    
        
        
    
    