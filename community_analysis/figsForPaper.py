import __init__
#
from community_analysis import chart_dpath
#
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


_rgb = lambda r, g, b: (r / float(255), g / float(255), b / float(255))

clists = (
    'blue', 'green', 'red', 'cyan', 'magenta', 'black',
    _rgb(255, 165, 0),  # orange
    _rgb(238, 130, 238),  # violet
    _rgb(255, 228, 225),  # misty rose
    _rgb(127, 255, 212),  # aqua-marine
    'yellow',
    _rgb(220, 220, 220),  # gray
    _rgb(255, 165, 0),  # orange
    'black'
)

mlists = (
    'o',  #    circle
    'v',  #    triangle_down
    '^',  #    triangle_up
    '<',  #    triangle_left
    '>',  #    triangle_right
    's',  #    square
    'p',  #    pentagon
    '*',  #    star
    '+',  #    plus
    'x',  #    x
    'D',  #    diamond
    'h',  #    hexagon1
    '1',  #    tri_down
    '2',  #    tri_up
    '3',  #    tri_left
    '4',  #    tri_right
    '8',  #    octagon
    'H',  #    hexagon2
    'd',  #    thin_diamond
    '|',  #    vline
    '_',  #    hline
    '.',  #    point
    ',',  #    pixel

    'D',  #    diamond
    '8',  #    octagon
          )

#
# The number of trips depending on hour
#
from taxi_common.file_handling_functions import load_pickle_file
hour_tripNum = load_pickle_file('_hour_tripNum.pkl')
#
_figsize = (8, 6)
_fontsize = 14
_data = hour_tripNum.values()
xTickMarks = hour_tripNum.keys()
_xlabel = 'Hour'
_ylabel = 'The number of trips'
#
fig = plt.figure(figsize=_figsize)
ax = fig.add_subplot(111)
ind = np.arange(len(_data))
width = 0.5  # the width of the bars
#
ax.bar(ind, _data, color='blue')
# axes and labels
ax.set_xlim(-width, len(ind)-width)
ax.set_ylabel(_xlabel)
ax.set_ylabel(_ylabel)
ax.set_xticks(ind)
xtickNames = ax.set_xticklabels(xTickMarks)
plt.setp(xtickNames, fontsize=_fontsize)

#
# Queueing time distribution
#
from community_analysis import ss_trips_dpath, ss_trips_prefix
df = pd.read_csv('%s/%s0901.csv' % (ss_trips_dpath, ss_trips_prefix))
cn = 'spendingTime'
outlier_set = set(np.where(df[cn] < 0)[0].tolist())
outlier_set = outlier_set.union(set(np.where(df[cn] > df[cn].quantile(0.95))[0].tolist()))
df = df.drop(df.index[list(outlier_set)])
df['queueingTime'] = df[cn] / 60
#
data = df['queueingTime']
_figsize = (8, 6)
_fontsize = 14
x_label, y_label = 'Queueing time (minute)', 'Percent'
num_bin = 10
#
plt.figure(figsize=_figsize)
_, bins, _ = plt.hist(data, num_bin, normed=1, histtype='bar', facecolor='green', alpha=0.75, edgecolor='black')
plt.xlabel(x_label, fontsize=_fontsize); plt.ylabel(y_label, fontsize=_fontsize)
plt.xlim(xmin=0, xmax=data.max())
plt.savefig('%s/%s.pdf' % (chart_dpath, 'queueTimeDist'), bbox_inches='tight', pad_inches=0)


#
# contributions for each year
#
from community_analysis import dpaths, prefixs

tm  = 'spendingTime'
years = []
year_contribution = []
for year in ['20%02d' % y for y in range(9,13)]:
    gp_dpath = dpaths[tm, year, 'groupPartition']
    gp_prefix = prefixs[tm, year, 'groupPartition']
    gp_summary_fpath = '%s/%ssummary.csv' % (gp_dpath, gp_prefix)
    df = pd.read_csv(gp_summary_fpath)
    contribution = []
    for i, v in enumerate(df.sort_values('contribution',ascending=False)['contribution']):
        contribution.append(v / 60)
        if i == 7:
            break
    years.append(year)
    year_contribution.append(contribution)
#
_figsize = (8, 6)
_ylabel = '$contribution$ (minute)'
_xlabel = 'Community name'
_fontsize = 14
#
fig = plt.figure(figsize=_figsize)
ax = fig.add_subplot(111)
ax.set_xlabel(_xlabel, fontsize=_fontsize)
ax.set_ylabel(_ylabel, fontsize=_fontsize)
ymax = 0
for i, y_data in enumerate(year_contribution):
    color_i = i % len(clists)
    marker_i = i % len(mlists)
    plt.plot(range(len(y_data)), y_data, linewidth=1, color=clists[color_i], marker=mlists[marker_i])
    ymax1 = max(y_data)
    if ymax < ymax1:
        ymax = ymax1
plt.legend(years, ncol=1, loc='upper right', fontsize=_fontsize)
ax.set_ybound(upper=ymax * 1.05)
plt.xticks(range(len(y_data)), ['$C_{%d}$' % (i+1) for i in range(len(y_data))])
ax.tick_params(axis='both', which='major', labelsize=_fontsize)
plt.savefig('%s/%s.pdf' % (chart_dpath, 'yearContribution'), bbox_inches='tight', pad_inches=0)
