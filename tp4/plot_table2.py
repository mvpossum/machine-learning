#! /usr/bin/env python
import sys
import os
from sys import argv
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

FILE = argv[1]
PLOT_FILE = os.path.splitext(FILE)[0]+'.png'
ERROR = 'er' in FILE.lower()

legend = argv[2:]
cols = len(legend)
if cols>=4:
    linestyles = ['--', '-', '--', '-', '--', '-', '--', '-', '--', '-', '--', '-']
    colors = ['r', 'r', 'b', 'b', 'g', 'g', 'orange', 'orange', 'purple', 'purple', 'y', 'y', 'gray', 'gray']
elif cols==3:
    linestyles = ['-', '-', '-']
    colors = ['b', 'g', 'r']

else:
    linestyles = ['-','-']
    colors = ['r', 'b']
    
x = []
y = [[] for _ in range(cols)]

for line in open(FILE):
    if line.strip():
        line = [float(s) for s in line.split(' ') if s.strip()]
        x.append(line[0])
        for j in range(cols):
            y[j].append(line[j+1])
        

fig, ax = plt.subplots()
ax = plt.subplot(111)

FONT_SIZE = 18
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(FONT_SIZE)

for yv in range(cols):
    ax.plot(x, y[yv], label=legend[yv], linestyle=linestyles[yv], color=colors[yv])
#~ if ERROR:
#ax.set_ylim(9,60)
#~ else:
    #~ ax.set_ylim(0,30)
#ax.set_xlim(0,128)
#~ box = ax.get_position()
#~ ax.set_position([box.x0, box.y0, box.width * 0.62, box.height])

#~ ax.legend(prop={'size':FONT_SIZE}, bbox_to_anchor=(1, 1.0))
ax.legend(prop={'size':FONT_SIZE})

plt.xlabel('Dimensiones', size=FONT_SIZE)
#~ plt.xscale('log')
ylabel = 'Error (%)' if ERROR else 'K óptimo'
plt.ylabel(ylabel, size=FONT_SIZE)
plt.savefig(PLOT_FILE)
plt.show()
