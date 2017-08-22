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

#~ legend_name = ["Iteracion",
    #~ "Mse estocástico (Entrenamiento)",
    #~ "Mse (Entrenamiento)",
    #~ "Mse (Validación)",
    #~ "Mse (Test)",
    #~ "Error de clasificación (Entrenamiento)",
    #~ "Error de clasificación (Validación)",
    #~ "Error de clasificación (Test)"]
legend_name = ["Iteracion",
    "Entrenamiento (estocástico)",
    "Entrenamiento",
    "Validación",
    "Test",
    "Entrenamiento",
    "Validación",
    "Test",
    "Penalidad"]
cols = list(map(int, argv[2:]))
ERROR = min(cols)>4

linestyles = ['-', '-', '-', '-']
colors = ['r', 'b', 'g', 'y']
    

x = []
y = [[] for _ in range(len(cols))]

for i,line in enumerate(open(FILE)):
    if line.strip():
        line = [float(s) for s in line.split('\t') if s.strip()]
        x.append(line[0])
        for j in range(5, 8):
            line[j]*=100
        for j in range(len(cols)):
            y[j].append(line[cols[j]])

fig, ax = plt.subplots()

FONT_SIZE = 17
for label in (ax.get_xticklabels() + ax.get_yticklabels()):
    label.set_fontsize(FONT_SIZE)

for yv in range(len(cols)):
    ax.plot(x, y[yv], label=legend_name[cols[yv]], linestyle=linestyles[yv], color=colors[yv])
#~ if ERROR:
    #~ ax.set_ylim(5,15)
#~ else:
    #~ ax.set_ylim(0,30)
#~ ax.set_xlim(0,5000)

plt.gcf().subplots_adjust(bottom=0.15)
ax.legend(prop={'size':FONT_SIZE})

plt.xlabel('Época', size=FONT_SIZE)
ylabel = 'Error (%)' if ERROR else 'MSE'
plt.ylabel(ylabel, size=FONT_SIZE)
plt.savefig(PLOT_FILE)
plt.show()
