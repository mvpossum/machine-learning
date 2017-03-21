#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <cassert>
#include <string>
#include "common.h"
using namespace std;


int main(int argc, char *argv[]){
	set_rand_seed();
	if(argc!=5){
		cout << "Usage: " << argv[0] << " <d> <n> <C> <out_name>" << endl;
		cout << "\td = Dimension del output" << endl; 
		cout << "\tn = Cantidad de puntos" << endl; 
		cout << "\tC = Varianza de los datos (sigma = C*sqrt(D))" << endl; 
		cout << "\tout_name = Nombre del dataset" << endl; 
		return 1;
	}
	
	//Read arguments
	int d=atoi(argv[1]);
	int n=atoi(argv[2]);
	assert(n>=0);
	assert(d>0);
	double C;
	sscanf(argv[3], "%lf", &C);
    string prefix=argv[4];
	
	//Generate data
	DatasetBinaryClassifier dataset(n);
	for(int i=0; i<n/2; i++)
		dataset[i]=SampleBinaryClassifier(rnd_normal_vec(d, 1, C*sqrt(d)), 1);
	for(int i=n/2; i<n; i++)
		dataset[i]=SampleBinaryClassifier(rnd_normal_vec(d, -1, C*sqrt(d)), 0);	
	random_shuffle(dataset.begin(), dataset.end());
	
	//Save data
    string names=prefix+".names";
    save_names_binary_classifier(names.c_str(), d);
    string data=prefix+".data";
    save_data_binary_classifier(data.c_str(), dataset);
	return 0;
}
