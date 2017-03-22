from sys import argv
if len(argv)!=2:
    print("Usage: {} <dataset_name>".format(argv[0]))
    exit(1)
PREFIX=argv[1]

import csv
DATA_FILE=PREFIX+'.data'
x,y,clase=[],[],[]
with open(DATA_FILE,'r') as f:
    reader = csv.reader(f)
    for row in reader:
        clase.append(row[-1])
        x.append(float(row[0]))
        y.append(float(row[1]))

import pandas as pd
import numpy as np
#~ %matplotlib inline
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(color_codes=True)
#~ sns.axes_style({'axes.axisbelow':False})
#~ values = numpy.zeros(20, dtype=dtype)
#~ for clase,data in parsed_data.items():
    #~ data=np.array(data)
    #~ print(data.shape)
    #~ index = ['x', 'y']
    #~ df = pd.DataFrame(data)
    #~ ggplot(aes(x=carat, y=price, color=color),  #by setting color=color, ggplot automatically draw in different colors
       #~ data=diamonds) + geom_point(stat='summary', fun.y=median)
    #~ sns.jointplot(data=df);
    

df = pd.DataFrame(dict(X=x, Y=y, clase=clase))

lm = sns.lmplot('X', 'Y', data=df, hue='clase', markers="o", palette="Set1", aspect=1, legend=False, fit_reg=False, scatter_kws={"s": 15} )
#~ axes = lm.axes
#~ axes[0,0].set_ylim(0,)
#~ axes[0,1].set_ylim(0,)

plt.show()
