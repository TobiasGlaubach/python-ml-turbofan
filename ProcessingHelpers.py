import numpy as np
import pandas as pd
from scipy.signal import filtfilt

def rolling_mean_by_unit(df, n, verbose=False):
    cols_sensors = [c for c in df.columns if c.startswith('sensor')]
    df_new = df.copy()
    unit_nrs = df['unit_nr'].unique()
    
    for nr in unit_nrs:
        if verbose:
            print('processing unit nr: {}'.format(nr))
        idx = df['unit_nr'] == nr
        df_new.loc[idx,cols_sensors] = df.loc[idx, cols_sensors].rolling(n, min_periods=1).mean()
    return df_new

def apply_filtfilt_by_unit(df, b, a=1.0):
    cols_data = [col for col in df.columns if col.startswith('sen') or col.startswith('os')]
    df_new = pd.DataFrame(columns=df.columns)
    
    for unit_nr, df_sub in df.groupby('unit_nr'):
        n = len(df_sub)            
        for col in df_sub.columns:
            if col.startswith('s'):
                df_sub[col] = filtfilt(b, a, df_sub[col].copy().values, padlen=5 * len(b))
        df_new = df_new.append(df_sub)
        
    return df_new

def apply_rolling_by_unit(df, fun, win_size_p=0.05, subsample=0):
    cols_data = [col for col in df.columns if col.startswith('sen') or col.startswith('os')]
    df_new = pd.DataFrame(columns=df.columns)

    for unit_nr, df_sub in df.groupby('unit_nr'):
        n = len(df_sub)
        if isinstance(win_size_p, int):
            win_size_n = int(win_size_p)
        else:
            win_size_n = int(n * win_size_p)
            
        df_windowed = df_sub.copy()
        df_windowed[cols_data] = df_windowed[cols_data].rolling(win_size_n).apply(fun)
        if subsample > 0:
            df_windowed = df_windowed[::subsample]
        df_new = df_new.append(df_windowed)
    
    return df_new

def normalize_col_by_unit(df, col):
    df_sub = df.copy()

    rul_abs = df_sub[col].copy().values
    rul_rel = np.array([])
    for unit_nr in df_sub['unit_nr'].unique():
        tmp = np.array(rul_abs[df_sub['unit_nr']==unit_nr], copy=True)    
        tmp = tmp - tmp.min()
        tmp = tmp / tmp.max()
        rul_rel = np.append(rul_rel, tmp)

    df_sub[col] = rul_rel
    return df_sub

def resample_fixed(df, n_new):
    n_old, m = df.values.shape
    mat_old = df.values
    mat_new = np.zeros((n_new, m))
    x_old = np.linspace(df.index.min(), df.index.max(), n_old)
    x_new = np.linspace(df.index.min(), df.index.max(), n_new)
        
    for j in range(m):
        y_old = mat_old[:, j]
        y_new = np.interp(x_new, x_old, y_old)
        mat_new[:, j] = y_new
        
    return pd.DataFrame(mat_new, index=x_new, columns=df.columns)
    