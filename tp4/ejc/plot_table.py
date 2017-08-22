#! /usr/bin/env python
import sys
import os
from sys import argv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

FILE = argv[1]
PLOT_FILE = os.path.splitext(FILE)[0]+'.png'
ERROR = 'error' in FILE.lower()

legend = argv[2:]
cols = len(legend)
if cols>=4:
    linestyles = ['--', '-', '--', '-', '--', '-']
    colors = ['r', 'r', 'b', 'b', 'g', 'g']
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

FONT_SIZE = 18
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(FONT_SIZE)
    
for yv in range(cols):
    ax.plot(x, y[yv], label=legend[yv], linestyle=linestyles[yv], color=colors[yv])
    
if ERROR:
    ax.set_ylim(0,50)
else:
    ax.set_ylim(0,30)
ax.set_xlim(2,32)

ax.legend(prop={'size':FONT_SIZE})

plt.xlabel('d', size=FONT_SIZE)
ylabel = 'Error (%)' if ERROR else 'Cantidad de nodos del árbol'
plt.ylabel(ylabel, size=FONT_SIZE)
plt.savefig(PLOT_FILE)
#~ plt.show()
