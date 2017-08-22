#! /usr/bin/env python2
import sys
import collections
import random
import csv
import numpy as np
from sklearn.utils import shuffle

config_keys = ["DIMS", "NCLASS", "TRAIN_SIZE", "NOT_VAL_SIZE", "TEST_SIZE", "SEED", "DEBUG", "MAX_K"]

def dist(x, y):
    return np.linalg.norm(y-x)

def nearest_neighbors(k, sample, in_dataset, class_dataset):
    dists = np.array([(dist(sample, p),c) for p,c in zip(in_dataset, class_dataset)], dtype=[('dist', 'float'), ('clase', int)])
    sorted_neighbors = np.sort(dists, order='dist')
    return sorted_neighbors[:k]

def predict_sample(k, sample, in_dataset, class_dataset, ignore_first=False):
    #Busca los k mas cercanos
    diff = 1 if ignore_first else 0
    knn = nearest_neighbors(k+diff, sample, in_dataset, class_dataset)
    knn_classes = knn[diff:]['clase']
    
    #Retorna la clase que mas aparece (si hay empate, una al azar)
    most_common = collections.Counter(knn_classes).most_common()
    max_count = most_common[0][1]
    max_count_classes = list(filter(lambda x: x[1] == max_count, most_common))
    return random.choice(max_count_classes)[0]

def get_predictions(k, samples, in_dataset, class_dataset, ignore_first=False):
    return np.array([predict_sample(k, sample, in_dataset, class_dataset, ignore_first) for sample in samples])

def get_error(predictions, clases):
    return np.sum([p!=c for p,c in zip(predictions, clases)])/float(clases.shape[0])*100

def optimize_k(in_train, class_train, in_val, class_val, in_test, class_test):
    errors = []
    for k in range(1, config["MAX_K"]+1):
        preds_val = get_predictions(k, in_val, in_train, class_train)
        error_val = get_error(preds_val, class_val)
        if config["DEBUG"]:
            print("K = {}, validacion = {:f}".format(k, error_val))
        errors.append((k, error_val))
    best_k = min(errors, key = lambda x: x[1])[0]
    return best_k

def load_config(path):
    with open(path) as config_file:
        values = config_file.readlines()[:len(config_keys)]
        values = [ int(attr.strip()) for attr in values ]
        config =  dict(zip(config_keys, values))
        for k,v in config.items(): print "{}: {}".format(k,v)
        return config

def read_data(path):
    rawdata = np.genfromtxt(path, delimiter=',')
    return rawdata[:,:-1], rawdata[:,-1].astype(int)

def save_prediction(path, in_test, predics):
    with open(path, "w") as predic_file:
        for sample,pred in zip(in_test, predics):
            attrs = ", ".join(map(str,sample))
            predic_file.write("{},{}\n".format(attrs, pred))

def main():
    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " <dataset>"
        sys.exit(0)
    STEM = sys.argv[1]
    config_file = STEM + ".knn"
    test_file   = STEM + ".test"
    train_file  = STEM + ".data"
    predic_file = STEM + ".predic"

    global config
    config = load_config(config_file)
    if config["SEED"]>0:
        random.seed(config["SEED"])

    #Carga el dataset
    in_train, class_train = read_data(train_file)
    if config["SEED"]!=-1:
        in_train, class_train = shuffle(in_train, class_train)
    
    #Separa conj de entrenamiento y validacion
    [in_train, in_val] = np.split(in_train, [config["NOT_VAL_SIZE"]], axis=0)
    [class_train, class_val] = np.split(class_train, [config["NOT_VAL_SIZE"]], axis=0)
    
    #Carga conj de test
    in_test, class_test = read_data(test_file)

    #Optimiza el k
    #~ best_k = optimize_k(in_train, class_train, in_val, class_val, in_test, class_test)
    best_k=16
    print("Best K: {}".format(best_k))

    print("Errores:")
    #Predice train
    pred_train = get_predictions(best_k, in_train, in_train, class_train, True)
    error_train = get_error(pred_train, class_train)
    print("Entrenamiento: {}%".format(error_train))
    
    #Predice val
    pred_val = get_predictions(best_k, in_val, in_train, class_train)
    error_val = get_error(pred_val, class_val)
    print("Validacion: {}%".format(error_val))
    
    #Predice test
    pred_test = get_predictions(best_k, in_test, in_train, class_train)
    error_test = get_error(pred_test, class_test)
    print("Test: {}%".format(error_test))
    
    save_prediction(predic_file, in_test, pred_test)

if __name__ == "__main__":
    main()
