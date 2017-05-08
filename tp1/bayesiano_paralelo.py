#! /usr/bin/env python
import sys

n=0
wrong=0
for i, line in enumerate(sys.stdin):
    line = [float(s) for s in line.split(',') if s.strip()]
    clase = line[-1]
    x = line[:-1]
    pred = x[0]>=0
    if pred!=clase:
        wrong+=1
    n+=1

print(wrong/float(n)*100, end=' ')

