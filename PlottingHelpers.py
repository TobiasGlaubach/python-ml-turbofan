import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import colorsys

def plot_rolling_by_unit(df_sub):
    nrs = df_sub['unit_nr'].unique()[:5]
    N = len(nrs)    
    
    HSV_tuples = [(x*1.0/N, 0.5, 0.5) for x in range(N)]
    colors = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

    fig, axes = plt.subplots(len(df_sub.columns),1, figsize = (15,22))
    axes = axes.flatten()
    
    for unit_nr, color in zip(nrs, colors):
        idx = df_sub['unit_nr']==unit_nr
        df_sub2 = df_sub.loc[idx].copy()
        plot_rolling_stats(df_sub2, 0.1, color, axes)
    
    for ax in axes:
        ax.set_xlim((df_sub.index.max(), df_sub.index.min()))
        
def plot_rolling_stats(df_sub2, wind_p, color, axes):
    wind_n = int(len(df_sub2) * wind_p)    
    
    for col, ax in zip(df_sub2.columns, axes):
        ser_std = df_sub2[col].rolling(wind_n).std()[::wind_n]
        ser_mean = df_sub2[col].rolling(wind_n).mean()[::wind_n]
        plot_line(ser_mean+ser_std, ser_mean, ser_mean-ser_std, color, ax=ax)
    
def plot_line(ser_high, ser_mid, ser_low, col, ax=None, fig=None):
    if ax is None:
        ax = plt.gca
    ax.plot(ser_high.index, ser_high.values, marker='o', linestyle='dashed', color=col)
    ax.plot(ser_mid.index, ser_mid.values, marker='o', color=col)
    ax.plot(ser_low.index, ser_low.values, marker='o', linestyle='dashed', color=col)
    