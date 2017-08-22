
import sys
import collections
import random
import csv
import math

# Atributos del archivo de configuracion .knn. Todos enteros.
config_keys = [ "DIMS"              # Numero de dimensiones a cargar.
              , "TRAIN_SIZE"        # Cantidad de muestras de entrenamiento.
              , "TEST_SIZE"         # Cantidad de muestras de prueba.
              , "TRAIN_VAL_RATIO"   # Porcentaje de muestras usadas para
                                    # entrenamiento. El resto a validacion.
              , "DIST_INTERVALS"    # Cantidad de intervalos de distancia.
                                    # Debe ser mayor que 0.
              , "DEBUG"             # Nivel de debug.
              ]


# Calcula la distancia al cuadrado entre dos muestras.
def dist(x, y):
    dims = config["DIMS"]
    factors = [ (x[0][attr] - y[0][attr])**2 for attr in range(dims) ]
    return sum(factors)

# Retorna los vecinos que se encuentren en _dataset_ en un radio de hasta
# _radius_ unidades de distancia de _sample_. Si no se encuentra ningun vecino,
# se devuelve el mas cercano.
def nearest_neighbors(radius, sample, dataset):
    distances = [ (dist(sample, x), x) for x in dataset if x != sample ]
    min_dist_sample = min(distances, key = lambda x: x[0])

    if min_dist_sample[0] > radius:
        return [min_dist_sample[1]]
    else:
        return [x[1] for x in distances if x[0] <= radius]


# Retorna la lista de distancias a testear dado un dataset.
def distance_intervals(dataset):
    dist_intervals = config["DIST_INTERVALS"]

    distances = [ dist(x,y) for x in dataset for y in dataset if x != y ]

    min_d = min(distances)
    max_d = max(distances)
    interval = (max_d - min_d) / dist_intervals

    return [min_d + interval * i for i in range(dist_intervals + 1)]


# Predice la clase de _sample_ usando los datos presentes en _dataset_.
# Si existe un empate entre una o varias clases, se retorna una de ellas al
# azar.
def predict_sample(d, sample, dataset):

    knn = nearest_neighbors(d, sample, dataset)
    knn_classes = [ x[1] for x in knn ]

    counter = collections.Counter(knn_classes)
    most_common = counter.most_common()

    max_count = max([ x[1] for x in most_common ])
    max_count_classes = list(filter(lambda x: x[1] == max_count, most_common))

    if len(max_count_classes) == 1:
        return (sample[0], max_count_classes[0][0])
    else:
        some_class = random.choice(max_count_classes)
        return (sample[0], some_class[0])


# Optimiza el valor K minimizando el error de validacion.
# Retorna los errores en entrenamiento, validacion y prueba para cada K bajo
# prueba. Ademas retorna las predicciones sobre el conjunto de prueba para el
# mejor K obtenido.
def optimize_dist(train_data, val_data, test_data):

    dists = distance_intervals(train_data)
    print "\nDistance intervals: ", dists

    print "\nOptimizing distance value:"

    errors = []
    for d in dists:

        train_preds = [ (sample[1], predict_sample(d,sample,train_data)[1])
                        for sample in train_data ]

        val_preds = [ (sample[1], predict_sample(d,sample,train_data)[1])
                      for sample in val_data ]

        test_preds = [ (sample[1], predict_sample(d,sample,train_data)[1])
                       for sample in test_data ]

        train_errors = len(list(filter(lambda x: x[0] != x[1], train_preds)))
        val_errors   = len(list(filter(lambda x: x[0] != x[1], val_preds)))
        test_errors  = len(list(filter(lambda x: x[0] != x[1], test_preds)))

        train_error = float(train_errors) / float(len(train_data)) * 100
        val_error   = float(val_errors)   / float(len(val_data))   * 100
        test_error  = float(test_errors)  / float(len(test_data))  * 100

        print """Distance = {:f}, Train = {:f}, Validation = {:f}, Test = {:f}""".format(d, train_error, val_error, test_error)

        errors.append((d, train_error, val_error, test_error))


    best_d = min(errors, key = lambda x: x[2])[0]
    print "\nBest distance found: {}".format(best_d)

    best_d_predic = [ predict_sample(d,sample,train_data)
                      for sample in test_data ]

    return (errors, best_d_predic)


# Carga la configuracion desde el archivo .knn.
def load_config(path):
    with open(path) as config_file:
        values = config_file.readlines()
        values = [ int(attr.strip()) for attr in values ]

        if len(values) != len(config_keys):
            sys.exit("Error parsing config file.")

        config =  dict(zip(config_keys, values))

        print "\nConfiguration loaded:"
        for k,v in config.items(): print "{} = {}".format(k,v)

        return config

# Lee el archivo con los datos de prueba.
def read_test_data(path):
    print "Opening test data from {}".format(path)
    with open(path) as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)

        test_data = []

        for sample in range(config["TEST_SIZE"]):

            dims = config["DIMS"]
            attrs = [ float(attr) for attr in dataset[sample][0:dims] ]
            class_ = dataset[sample][-1].strip()
            test_data.append((attrs, class_))

        if config["DEBUG"]: print "\nTest data: ", test_data

        return test_data

# Lee el archivo con los datos de entrenamiento y validacion.
# Se utiliza un valor aleatorio ponderado para decidir si cada muestra se usara
# para entrenamiento o validacion.
def read_train_val_data(path):
    print "Opening training data from {}".format(path)
    with open(path) as csvfile:
        lines = csv.reader(csvfile)
        dataset = list(lines)

        train_data = []
        val_data = []

        for sample in range(config["TRAIN_SIZE"]):

            dims = config["DIMS"]
            attrs = [ float(attr) for attr in dataset[sample][0:dims] ]
            class_ = dataset[sample][-1].strip()

            if random.random() * 100 < config["TRAIN_VAL_RATIO"]:
                train_data.append((attrs, class_))
            else:
                val_data.append((attrs, class_))

        if config["DEBUG"]:
            print "\nTraining data:\n", train_data
            print "\nValidation data:\n", val_data

        return train_data, val_data


# Guarda la tabla de errores de entrenamiento, validacion y prueba vs. K en el
# archivo .error.
def save_errors(path, errors):
    print "Saving errors table to {}".format(path)
    with open(path, "w") as error_file:
        for k, train, val, test in errors:
            line = "{:f},{:f},{:f},{:f}\n".format(k, train, val, test)
            error_file.write(line)

# Guarda la prediccion del conjunto de prueba en el archivo .predic.
def save_prediction(path, predics):
    print "Saving test predictions to {}".format(path)
    with open(path, "w") as predic_file:
        for pred in predics:
            attrs = ", ".join(map(str,pred[0]))
            class_ = pred[1]
            line = "{},{}\n".format(attrs, class_)
            predic_file.write(line)



if __name__ == "__main__":

    if len(sys.argv) != 2:
        print "Usage: " + sys.argv[0] + " stem"
        sys.exit(0)

    config_file = sys.argv[1] + ".knn"
    test_file   = sys.argv[1] + ".test"
    train_file  = sys.argv[1] + ".data"
    predic_file = sys.argv[1] + ".predic"
    errors_file = sys.argv[1] + ".error"

    # Cargo la configuracion de entrenamiento.
    config = load_config(config_file)

    # Cargo los conjuntos de entrenamiento/validacion y test.
    train_data, val_data = read_train_val_data(train_file)
    test_data = read_test_data(test_file)

    # Optimizo la cantidad de vecinos prediciendo el conjunto de validacion
    # usando los datos en el conjunto de entrenamiento. Ademas obtengo la
    # prediccion del conjunto de prueba usando el mejor k obtenido.
    errors, best_dist_predic = optimize_dist(train_data, val_data, test_data)

    # Guardo los errores en entrenamiento, validacion y prueba vs. k.
    save_errors(errors_file, errors)

    # Guardo las predicciones obtenidas sobre el conjunto de prueba
    # usando el mejor valor k obtenido mediante validacion.
    save_prediction(predic_file, best_dist_predic)

    print "Finished"


