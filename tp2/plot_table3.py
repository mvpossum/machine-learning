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
ERROR = 'er' in FILE.lower()

legend = argv[2:]
cols = len(legend)
if cols==4:
    linestyles = ['--', '-', '--', '-']
    colors = ['r', 'r', 'b', 'b']
else:
    linestyles = ['-','-']
    colors = ['r', 'b']
    
paralelo = {}
diagonal = {}

for line in open('discrete-error.csv'):
    if line.strip():
        line = [s for s in line.split(',') if s.strip()]
        ds = paralelo if line[0]=='paralelo' else diagonal
        if int(line[1]) not in ds:
            ds[int(line[1])]=[]
        ds[int(line[1])].append(float(line[2]))
        
x = []
y = [[] for _ in range(cols)]

for line in open(FILE):
    if line.strip():
        line = [float(s) for s in line.split(' ') if s.strip()]
        x.append(line[0])
        for j in range(len(line)-1):
            y[j].append(float(line[j+1]))

for k,v in sorted(diagonal.items()):
    y[2].append(np.array(v).mean())
for k,v in sorted(paralelo.items()):
    y[3].append(np.array(v).mean())
    
        

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

ax.legend(prop={'size':FONT_SIZE})

plt.xlabel('C', size=FONT_SIZE)
ylabel = 'Error (%)' if ERROR else 'Cantidad de nodos del árbol'
plt.ylabel(ylabel, size=FONT_SIZE)
plt.savefig(PLOT_FILE)
plt.show()
