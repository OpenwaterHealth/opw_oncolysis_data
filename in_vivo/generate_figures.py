import pzfx_parser as pzfx
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import sys
import os
mpl.use("Agg")

filename = sys.argv[1]

pz = pzfx.read_pzfx(filename)
print(f'loading {filename}...')
cwd = os.getcwd()
(fname, ext) = os.path.splitext(filename)
dfpz = pz['OW']
d1 = {}
sample = 0
for column in dfpz.columns[2:]:
    [group, mouse] = column.split('_')
    if group == '1000KHz':
        group = '100KHz'
    group = group.replace('KHz','kHz')
    for timestep in range(len(dfpz[column])):
        sample_entry = {'group':group, 'mouse':mouse, 'timestep':timestep, 'day':int(dfpz['_0'][timestep]), 'volume':dfpz[column][timestep]}
        d1[sample] = sample_entry
        sample += 1
df = pd.DataFrame.from_dict(d1, orient='index')
df['relative volume'] = df.apply(lambda row: row['volume']/df.loc[(df['mouse']==row['mouse']) & (df.timestep==0)].iloc[0]['volume'], axis='columns')
df['volume (cm$^2$)'] = df['volume']*1e-3
groups = sorted(set(df.group))
days = sorted(set(df['day']))
context = {'font.size':14,
           'font.weight':'bold', 
           'axes.titlesize':16, 
           'axes.titleweight':'bold', 
           'axes.labelsize':14, 
           'axes.labelweight':'bold'}

print('generating boxplot...')
with mpl.rc_context(context):
    fig, ax = plt.subplots(1,1,figsize=(max(days),6))
    sns.boxplot(data=df, x='day', y='volume (cm$^2$)', hue='group', hue_order=sorted(groups), ax=ax, order=np.arange(max(days)+1), width=0.6)
    plt.grid(axis='y')
    outname = os.path.join(cwd, f'{fname}_boxplot.png')
    fig.savefig(outname, format='png')
    print(f'saved {outname}')
    
print('generating swarmplot...')
with mpl.rc_context(context):
    fig, ax = plt.subplots(1,1,figsize=(max(days),6))
    sns.stripplot(data=df, x='day', y='volume (cm$^2$)', hue='group', legend='auto', ax=ax, order=np.arange(max(days)+1))
    plt.grid()
    outname = os.path.join(cwd, f'{fname}_swarmplot.png')
    fig.savefig(outname, format='png')
    print(f'saved {outname}')

print('generating lineplot...')
with mpl.rc_context(context):
    fig, ax = plt.subplots(1,len(groups),figsize=(16,6), gridspec_kw={'wspace':0.4})
    for group, axi in zip(sorted(groups), ax):
        sns.lineplot(data=df.loc[df.group==group], x='day', y='volume (cm$^2$)', legend=False, ax=axi, size=18, color='black')
        sns.lineplot(data=df.loc[df.group==group], x='day', y='volume (cm$^2$)', hue='mouse', legend=False, ax=axi)
        if not (group=='Control'):
            axi.set_ylim([0, 0.8])
            if not (group=='100kHz'):
                axi.set_ylabel('')
        else:
            axi.set_ylim([0, 2])
            axi.yaxis.label.set_color('red')
            axi.tick_params(axis='y', colors='red') 
            axi.spines['left'].set_color('red')
        axi.set_title(group)
        axi.grid()
    outname = os.path.join(cwd, f'{fname}_lines.png')
    fig.savefig(outname, format='png')
    print(f'saved {outname}')

print('generating relative lineplot...')
groups = set(df.group)
with mpl.rc_context(context):
    fig, ax = plt.subplots(1,len(groups), figsize=(16,6), gridspec_kw={'wspace':0.4})
    for group, axi in zip(sorted(groups), ax):
        sns.lineplot(data=df.loc[df.group==group], x='day', y='relative volume', legend=False, ax=axi, size=18, color='black')
        sns.lineplot(data=df.loc[df.group==group], x='day', y='relative volume', hue='mouse', legend=False, ax=axi)
        if not (group=='Control'):
            axi.set_ylim([0, 20])
            if not (group=='100kHz'):
                axi.set_ylabel('')
        else:
            axi.set_ylim([0, 70])
            axi.yaxis.label.set_color('red')
            axi.tick_params(axis='y', colors='red') 
            axi.spines['left'].set_color('red')
        axi.set_title(group)
        axi.grid()
    outname = os.path.join(cwd, f'{fname}_relative_lines.png')
    fig.savefig(outname, format='png')
    print(f'saved {outname}')

    
print('done')