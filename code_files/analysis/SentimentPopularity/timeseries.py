# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 22:04:38 2019

@author: lliu9
"""

import pandas as pd
import matplotlib.pyplot as plt
import sys
import numpy as np
import six

def timeseries(lang):
    mon, sentiment, popularity, counts = [], [], [], []
    file = "results_"+lang+".txt"
    with open(file) as f:
        for line in f:
            pair = line.split("\t")
            mon.append(pair[0][1:-1])
            
            sentiment.append(pair[1].split(",")[0][1:])
            popularity.append(pair[1].split(",")[1][1:])
            counts.append(pair[1].split(",")[2][:-3])
            
    df = pd.DataFrame({"Sentiment": sentiment,
                       "Popularity": popularity,
                       'QnsCts':counts}).astype('float')
    df['Index'] = df.index
    df.index= pd.to_datetime(mon)
    
    #months elaspsed
    def timefactor(df):
        return  df['Popularity']*(1.1 **df["Index"])
    df['ViewCts'] = df.apply(timefactor, axis=1)
    
    #normalize data
    normdf = df.drop(columns=['Popularity', 'Index'], inplace=True)
    normdf=(df-df.mean())/df.std()
    
    plt.style.use('ggplot')
    
    plt.figure(figsize=(80,80))
    
    fig, ax = plt.subplots()
    ax.plot(normdf.index, normdf.ViewCts, label='Views Cts')
    ax.plot(normdf.index, normdf.Sentiment,  label='Ans Sentiment')
    ax.plot(normdf.index, normdf.QnsCts,  label='#Qn Accepted')
    
    legend = ax.legend()
    title = "Sentiment and Popularity for "+lang
    plt.title(title)
    legend.get_frame().set_facecolor('C0')
    plt.savefig(lang)
    
    
    norm=normdf.corr().round(2)
    
    def render_mpl_table(data, col_width=3.0, row_height=0.625, font_size=14,
                     header_color='#40466e', row_colors=['#f1f1f2', 'w'], edge_color='w',
                     bbox=[0, 0, 1, 1], header_columns=0,
                     ax=None, **kwargs):
        if ax is None:
            size = (np.array(data.shape[::-1]) + np.array([0, 1])) * np.array([col_width, row_height])
            fig, ax = plt.subplots(figsize=size)
            ax.axis('off')
    
        mpl_table = ax.table(cellText=data.values, bbox=bbox, colLabels=data.columns, **kwargs)
    
        mpl_table.auto_set_font_size(False)
        mpl_table.set_fontsize(font_size)
    
        for k, cell in  six.iteritems(mpl_table._cells):
            cell.set_edgecolor(edge_color)
            if k[0] == 0 or k[1] < header_columns:
                cell.set_text_props(weight='bold', color='w')
                cell.set_facecolor(header_color)
            else:
                cell.set_facecolor(row_colors[k[0]%len(row_colors) ])
        return ax

    render_mpl_table(norm, header_columns=0, col_width=2.0)
    name = lang+"corr.png"
    plt.savefig(name)


    
if __name__ == "__main__": 

    timeseries(sys.argv[1])