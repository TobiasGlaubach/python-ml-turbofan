import numpy as np
import pandas as pd

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
    