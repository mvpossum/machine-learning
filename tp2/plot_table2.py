#! /usr/bin/env python
import sys
import os
from sys import argv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

FILE = argv[1]
PLOT_FILE = os.path.splitext(FILE)[0]+'.png'

legend = argv[2:]
cols = len(legend)
if cols==4:
    linestyles = ['-', '-', '--', '-']
    colors = ['r', 'r', 'b', 'b']
else:
    linestyles = ['-','-']
    colors = ['r', 'b']
    
vals= {}

for line in open(FILE):
    if line.strip():
        line = [float(s) for s in line.split(',') if s.strip()]
        if not line[0] in vals:
            vals[line[0]]=[]
        vals[line[0]].append(line[1])

x = []
y = [[]]
for k,v in vals.items():
    x.append(k)
    y[0].append(np.array(v).mean()*100)
    
fig, ax = plt.subplots()

FONT_SIZE = 18
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(FONT_SIZE)

for yv in range(cols):
    ax.plot(x, y[yv], label=legend[yv], linestyle=linestyles[yv], color=colors[yv])
#~ if ERROR:
    #~ ax.set_ylim(5,15)
#~ else:
    #~ ax.set_ylim(0,30)
#~ ax.set_xlim(0,5000)

#~ ax.legend(prop={'size':FONT_SIZE})
plt.gcf().subplots_adjust(bottom=0.15, left=0.15)
plt.xscale('log')
plt.xlabel('Gamma', size=FONT_SIZE)
plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
ylabel = 'Penalización'
plt.ylabel(ylabel, size=FONT_SIZE)
plt.savefig(PLOT_FILE)
plt.show()
