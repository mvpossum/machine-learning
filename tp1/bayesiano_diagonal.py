#! /usr/bin/env python
import sys
import numpy as np

def dist(a, b):
    return np.linalg.norm(a-b)

n=0
wrong=0
for i, line in enumerate(sys.stdin):
    line = [float(s) for s in line.split(',') if s.strip()]
    clase = line[-1]
    x = np.array(line[:-1])
    t = x.shape[0]
    pred = dist(np.ones(t), x)<dist(-np.ones(t), x)
    if pred!=clase:
        wrong+=1
    n+=1

print(wrong/float(n)*100, end=' ')

