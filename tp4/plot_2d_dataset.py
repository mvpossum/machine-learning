#! /usr/bin/env python
#Read arguments
from sys import argv

if len(argv)!=2:
    print("Usage: {} <dataset_name>".format(argv[0]))
    exit(1)
PREFIX=argv[1]

#Read data
import csv

DATA_FILE=PREFIX
x,y,clase=[],[],[]
with open(DATA_FILE,'r') as f:
    reader = csv.reader(f)
    for row in reader:
        if '\t' in row[0]:
            row=row[0].split('\t');
        clase.append(row[-1])
        x.append(float(row[0]))
        y.append(float(row[1]))

#Draw graph
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(color_codes=True)
df = pd.DataFrame(dict(X=x, Y=y, clase=clase))
lm = sns.lmplot('X', 'Y', data=df, hue='clase', markers='o', palette="Set1", aspect=1, legend=False, fit_reg=False, scatter_kws={"s": 20} )
ax = lm.axes[0,0]
ax.set_aspect('equal')
LIMI= round(np.array(x).max(), 1)+0.1
print(LIMI)
ax.set_ylim(-LIMI,LIMI)
#~ LIMI=1.1
ax.set_xlim(-LIMI,LIMI)


#~ FONT_SIZE = 18
#~ for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    #~ label.set_fontsize(FONT_SIZE)

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
ax.set_frame_on(False) #Remove both axes

plt.savefig(PREFIX+'.png', bbox_inches='tight', pad_inches=0)

ax.xaxis.set_visible(True)
ax.yaxis.set_visible(True)
ax.set_frame_on(True) #Remove both axes

plt.show()

