#! /usr/bin/env python
import subprocess
from shutil import copyfile
import numpy as np
import random
from scipy.optimize import minimize
from multiprocessing import Process
import matplotlib.pyplot as plt


DATASET = "ikeda"
TMPD = DATASET + "_tmp"

best=[100]
best_params=None

def get_error(output):
    FIND=["Test discreto:","Entrenamiento(med):","Test:"] 
    res = [-1 for _ in range(len(FIND))]
    for line in output:
        line = str(line)
        #~ print(line)
        #~ print(line)
        for i,busq in enumerate(FIND):
            if busq in line:
                error=line[line.find(busq)+len(busq):-3]
                if error[-1]=='%':
                    error=error[:-1]
                res[i]=float(error)
    return res

def calc_error(x):
    pr=x[0]
    subprocess.call(["../alter_net", DATASET+".net", TMPD+".net", "PR="+str(pr),])
    proc = subprocess.Popen(["../bp", TMPD],stdout=subprocess.PIPE)
    error = get_error(proc.stdout)
    print('{} {}'.format(pr, error))
    return error

def calc_error_prom(x):
    return np.array([calc_error(x) for _ in range(5)]).mean(axis=0)

def evaluate(params):
    global best, best_params
    cur = calc_error_prom(params)
    if cur[0]<best[0]:
        best = cur
        best_params = params
        print(best)
        print(', '.join(["{0:.8f}".format(p) if isinstance(p,float) else str(p) for p in best_params]))
    return cur
    

copyfile(DATASET+".data", TMPD+".data")
copyfile(DATASET+".test", TMPD+".test")


def main():
            
    pr=np.linspace(0.1, 1.0, 32)
    tester=np.zeros(pr.shape)
    trainmed=np.zeros(pr.shape)
    testfunc=np.zeros(pr.shape)
    
    #~ for i in range(pr.shape[0]):
        #~ print(float(i)/pr.size*100, '%')
        #~ R = evaluate([pr[i]])
        #~ tester[i]=R[0]
        #~ trainmed[i]=R[1]
        #~ testfunc[i]=R[2]
            
    tester=np.load('tester.npy')
    trainmed=np.load('trainmed.npy')
    testfunc=np.load('testfunc.npy')
    #~ np.save('tester.npy', tester)
    #~ np.save('trainmed.npy', trainmed)
    #~ np.save('testfunc.npy', testfunc)
    
    with open('tester.txt', 'w') as out:
        for i in range(pr.shape[0]):
            out.write('{} {}\n'.format(pr[i], tester[i]))
    with open('trainmed.txt', 'w') as out:
        for i in range(pr.shape[0]):
            out.write('{} {}\n'.format(pr[i], trainmed[i]))
    with open('testfunc.txt', 'w') as out:
        for i in range(pr.shape[0]):
            out.write('{} {}\n'.format(pr[i], testfunc[i]))
            
    im = plt.imshow(tester, cmap=plt.cm.RdBu,interpolation='bilinear')  
    plt.colorbar(im)
    plt.show()
    im = plt.imshow(trainmed, cmap=plt.cm.RdBu,interpolation='bilinear')  
    plt.colorbar(im)
    plt.show()
    im = plt.imshow(testfunc, cmap=plt.cm.RdBu,interpolation='bilinear')  
    plt.colorbar(im)
    plt.show()
    #~ im = plt.imshow(zz, cmap=plt.cm.RdBu, extent=(-3, 3, 3, -3))  
    #~ cset = plt.contour(zz, linewidths=2,
                       #~ cmap=plt.cm.Set2)
    #~ plt.clabel(cset, inline=True, fmt='%1.1f', fontsize=16)


if __name__ == "__main__":
    main()

