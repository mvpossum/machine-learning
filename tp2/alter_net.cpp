#include <iostream>
#include <fstream>
#include <map>
#include <set>
#include <cassert>
using namespace std;

typedef map<string, string> Config;
const string params[] = {"N1", "N2", "N3", "PTOT", "PR", "PTEST", "ITER", "ETA", "u", "NERROR", "WTS", "SEED", "CONTROL"};
const int cant_params = sizeof(params)/sizeof(params[0]);
set<string> s_params;

Config read(const char *path){
    Config conf;
    ifstream in(path);
    assert(in);
    for(int i=0; i<cant_params; i++)
        assert(in >> conf[params[i]]);
    return conf;
}

void write(const char *path, const Config& conf){
    ofstream out(path);
    assert(out);
    for(int i=0; i<cant_params; i++){
        Config::const_iterator it = conf.find(params[i]);
        assert(it!=conf.end());
        assert(out << it->second << endl);
    }
}

int main(int argc, char *argv[]){
    if(argc<3){
        cout << "Uso: " << argv[0] << " <entrada.net> <salida.net> ETA=3 N1=2..." << endl;
        cout << "Posibles parametros:" << endl;
        cout << "	N1:     NEURONAS EN CAPA DE ENTRADA" << endl;
        cout << "	N2:     NEURONAS EN CAPA INTERMEDIA" << endl;
        cout << "	N3:     NEURONAS EN CAPA DE SALIDA" << endl;
        cout << "	PTOT:   cantidad TOTAL de patrones en el archivo .data" << endl;
        cout << "	PR:     cantidad de patrones de ENTRENAMIENTO" << endl;
        cout << "	PTEST:  cantidad de patrones de test (archivo .test)" << endl;
        cout << "	ITER:   Total de Iteraciones" << endl;
        cout << "	ETA:    learning rate" << endl;
        cout << "	u:      Momentum" << endl;
        cout << "	NERROR: graba error cada NERROR iteraciones" << endl;
        cout << "	WTS:    numero de archivo de sinapsis inicial" << endl;
        cout << "	SEED:   semilla para el rand()" << endl;
        cout << "	CONTROL:verbosity" << endl;
        cout << endl;
        cout << "	Comentarios:" << endl;
        cout << "	WTS=0 implica empezar la red con valores al azar" << endl;
        cout << "	cantidad de patrones de validacion: PTOT - PR" << endl;
        cout << "	SEED: -1: No mezclar los patrones: usar los primeros PR para entrenar y" << endl;
        cout << "	          el resto para validar." << endl;
        cout << "	       0: Seleccionar semilla con el reloj, y mezclar los patrones." << endl;
        cout << "	      >0: Usa el numero como semilla, y mezcla los patrones." << endl;
        cout << "	verbosity: 0:resumen, 1:0 + pesos, 2:1 + datos" << endl;
        return 1;
    }
    for(int i=0; i<cant_params; i++) s_params.insert(params[i]);
    Config conf = read(argv[1]);
    for(int i=3; i<argc; i++){
        string arg(argv[i]);
        size_t eq = arg.find('=');
        assert(eq!=string::npos);
        string param=arg.substr(0, eq), val=arg.substr(eq+1);
        assert(s_params.count(param));
        assert(val.size());
        conf[param]=val;
    }
    write(argv[2], conf);
    return 0;
}
