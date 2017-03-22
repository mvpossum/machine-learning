#! /usr/bin/env python
#Read arguments
from sys import argv

if len(argv)!=2:
    print("Usage: {} <dataset_name>".format(argv[0]))
    exit(1)
PREFIX=argv[1]

#Read data
import csv

DATA_FILE=PREFIX+'.data'
x,y,clase=[],[],[]
with open(DATA_FILE,'r') as f:
    reader = csv.reader(f)
    for row in reader:
        clase.append(row[-1])
        x.append(float(row[0]))
        y.append(float(row[1]))

#Draw graph
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set(color_codes=True)
df = pd.DataFrame(dict(X=x, Y=y, clase=clase))
lm = sns.lmplot('X', 'Y', data=df, hue='clase', markers='o', palette="Set1", aspect=1, legend=False, fit_reg=False, scatter_kws={"s": 15} )
ax = lm.axes[0,0]
ax.set_aspect('equal')
#~ ax.set_ylim(0,)

plt.show()
