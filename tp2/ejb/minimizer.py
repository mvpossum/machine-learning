#! /usr/bin/env python
import subprocess
from shutil import copyfile
import numpy as np
import random
from scipy.optimize import minimize
from multiprocessing import Process
import matplotlib.pyplot as plt


DATASET = "espirales"
TMPD = DATASET + "_tmp"
SEED=0

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
    subprocess.call(["../alter_net", DATASET+".net", TMPD+".net", "N2="+str(10), "SEED="+str(SEED),])
    proc = subprocess.Popen(["../bp", TMPD],stdout=subprocess.PIPE)
    error = get_error(proc.stdout)
    print('{}'.format(error))
    return error

def calc_error_prom(x):
    return np.array([calc_error(x) for _ in range(20)]).mean(axis=0)

def evaluate(params):
    global best, best_params
    cur = calc_error(params)
    if cur[0]<best[0]:
        best = cur
        best_params = [SEED]
        print(best)
        print(', '.join(["{0:.8f}".format(p) if isinstance(p,float) else str(p) for p in best_params]))
        open('best.txt','w').write(str(SEED)+"  = "+str(best[0]))
    return cur
    

copyfile(DATASET+".data", TMPD+".data")
copyfile(DATASET+".test", TMPD+".test")


def main():
    #~ SEED=625922 #dat seed
    
    #~ x0 = np.array([0.45, 0.0703])
    #~ res = minimize(evaluate, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
    global SEED
    
    for i in range(2000):
        SEED=random.randint(0, 1000000)
        evaluate([])

    #~ 4.55
    #~ [621044, 0.45000000000000001, 0.10000000000000001]
    #~ 4.15
    #~ [195367, 0.45, 0.0703]
    #~ 2.45
    #~ 625922, 0.45070392966270445, 0.07084909639596934
    #~ 2.65
    #~ [625922, 0.45, 0.0703]
    
    
    #~ evaluate([0.45, 0.0703])
    #~ for u in np.linspace(0., 0.9, 10):
        #~ for eta in np.linspace(0.001, 0.2, 10):
            #~ evaluate([u, eta])
            
    u=np.linspace(0., 0.9, 32)
    eta=np.linspace(0.001, 0.1, 32)
    U, ETA = np.meshgrid(u, eta)    
    tester = np.zeros(U.shape)
    trainmed = np.zeros(U.shape)
    testfunc = np.zeros(U.shape)
    
    #~ for i in range(U.shape[0]):
        #~ for j in range(U.shape[1]):
            #~ print(float(i*U.shape[0]+j)/tester.size*100, '%')
            #~ R = evaluate([U[i,j], ETA[i,j]])
            #~ tester[i,j]=R[0]
            #~ trainmed[i,j]=R[1]
            #~ testfunc[i,j]=R[2]
            
    tester=np.load('tester2.npy')
    trainmed=np.load('trainmed2.npy')
    testfunc=np.load('testfunc2.npy')
    #~ np.save('tester.npy', tester)
    #~ np.save('trainmed.npy', trainmed)
    #~ np.save('testfunc.npy', testfunc)
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

