#! /usr/bin/env python2
import sys
import collections
import random
import csv
import numpy as np
from sklearn.utils import shuffle

config_keys = ["DIMS", "NCLASS", "TRAIN_SIZE", "NOT_VAL_SIZE", "TEST_SIZE", "SEED", "DEBUG"]

def dist(x, y):
    return np.linalg.norm(y-x)

def nearest_neighbors(d, sample, in_dataset, class_dataset):
    dists = np.array([(dist(sample, p),c) for p,c in zip(in_dataset, class_dataset)], dtype=[('dist', 'float'), ('clase', int)])
    min_dist_sample = dists[np.argmin(dists['dist'])]
    if min_dist_sample[0] > d:
        return np.array([min_dist_sample])
    else:
        return np.array([x for x in dists if x[0] <= d])

def get_random_most_common(classes):
    #Retorna el elemento que mas aparece (si hay empate, uno al azar)
    most_common = collections.Counter(classes).most_common()
    max_count = most_common[0][1]
    max_count_classes = list(filter(lambda x: x[1] == max_count, most_common))
    return random.choice(max_count_classes)[0]
    
def predict_sample(d, sample, in_dataset, class_dataset, ignore_first=False):
    #Busca los con distancia < d
    diff = 1 if ignore_first else 0
    knn = nearest_neighbors(d, sample, in_dataset, class_dataset)
    classes = knn[diff:]['clase']
    if not len(classes):
        return random.randint(0, config["NCLASS"])
    #Devuelve el que mas aparece
    return get_random_most_common(classes)

def get_predictions(d, samples, in_dataset, class_dataset, ignore_first=False):
    return np.array([predict_sample(d, sample, in_dataset, class_dataset, ignore_first) for sample in samples])

def get_error(predictions, clases):
    return np.sum([p!=c for p,c in zip(predictions, clases)])/float(clases.shape[0])*100

def optimize_d(in_train, class_train, in_val, class_val, in_test, class_test):
    errors = []
    diagonal = "diagonal" in sys.argv[1]
    values = np.linspace(0.9, 1.5, num=25) * (config["DIMS"] if diagonal else np.sqrt(config["DIMS"]))
    for d in values:
        preds_val = get_predictions(d, in_val, in_train, class_train)
        error_val = get_error(preds_val, class_val)
        if config["DEBUG"]:
            print("D = {}, validacion = {:f}".format(d, error_val))
        errors.append((d, error_val))
    best_d = min(errors, key = lambda x: x[1])[0]
    return best_d

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

    #Optimiza el d
    best_d = optimize_d(in_train, class_train, in_val, class_val, in_test, class_test)
    print("Best D: {}".format(best_d))

    print("Errores:")
    #Predice train
    #~ pred_train = get_predictions(best_d, in_train, in_train, class_train, True)
    #~ error_train = get_error(pred_train, class_train)
    #~ print("Entrenamiento: {}%".format(error_train))
    
    #Predice val
    #~ pred_val = get_predictions(best_d, in_val, in_train, class_train)
    #~ error_val = get_error(pred_val, class_val)
    #~ print("Validacion: {}%".format(error_val))
    
    #Predice test
    pred_test = get_predictions(best_d, in_test, in_train, class_train)
    error_test = get_error(pred_test, class_test)
    print("Test: {}%".format(error_test))
    
    save_prediction(predic_file, in_test, pred_test)

if __name__ == "__main__":
    main()
