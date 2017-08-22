#! /usr/bin/env python
import subprocess
from shutil import copyfile
import numpy as np
import random
from scipy.optimize import minimize
from multiprocessing import Process
import matplotlib.pyplot as plt


DATASET = "dos_elipses"
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
    u=x[0]; eta=x[1]
    subprocess.call(["../alter_net", DATASET+".net", TMPD+".net", "u="+str(u), "ETA="+str(eta),])
    proc = subprocess.Popen(["../bp", TMPD],stdout=subprocess.PIPE)
    error = get_error(proc.stdout)
    print('{} {} {}'.format(u, eta, error))
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
    #~ SEED=625922 #dat seed
    
    #~ x0 = np.array([0.45, 0.0703])
    #~ res = minimize(evaluate, x0, method='nelder-mead', options={'xtol': 1e-8, 'disp': True})
    
    #~ for i in range(200):
        #~ SEED=random.randint(0, 1000000)
        #~ evaluate([0.45, 0.1])

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
            
    u=np.linspace(0., 0.9, 16)
    eta=np.linspace(0.001, 0.1, 16)
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
            
    tester=np.load('tester3.npy')
    trainmed=np.load('trainmed3.npy')
    testfunc=np.load('testfunc3.npy')
    
    fig, ax = plt.subplots()
    plt.gcf().subplots_adjust(bottom=0.15)

    FONT_SIZE = 18
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(FONT_SIZE)
    plt.xlabel('Momentum', size=FONT_SIZE)
    plt.ylabel('Learning rate', size=FONT_SIZE)
    #~ np.save('tester.npy', tester)
    #~ np.save('trainmed.npy', trainmed)
    #~ np.save('testfunc.npy', testfunc)
    im = plt.imshow(tester, cmap=plt.cm.RdBu,interpolation='bilinear')  
    cbar=plt.colorbar(im)
    cbar.ax.tick_params(labelsize=FONT_SIZE)
    plt.savefig('tester.png')
    plt.show()
    #~ im = plt.imshow(trainmed, cmap=plt.cm.RdBu,interpolation='bilinear')  
    #~ plt.colorbar(im)
    #~ plt.show()
    #~ im = plt.imshow(testfunc, cmap=plt.cm.RdBu,interpolation='bilinear')  
    #~ plt.colorbar(im)
    #~ plt.show()
    #~ im = plt.imshow(zz, cmap=plt.cm.RdBu, extent=(-3, 3, 3, -3))  
    #~ cset = plt.contour(zz, linewidths=2,
                       #~ cmap=plt.cm.Set2)
    #~ plt.clabel(cset, inline=True, fmt='%1.1f', fontsize=16)


if __name__ == "__main__":
    main()

