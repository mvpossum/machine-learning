#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <cmath>
#include <algorithm>
#include <vector>
#include <map>
#include <cassert>
#include <string>
#include "common.h"
using namespace std;

void print_stats(int samples, const VectorXd &mean, const VectorXd &var){
    cout << "\tsamples = " << samples << endl;
    cout << "\tmean = " << mean.transpose() << endl;
    cout << "\tvariance = " << var.transpose() << endl;
    cout << "\tdesviacion estandar = " << var.cwiseAbs().cwiseSqrt().transpose() << endl;
}

int main(int argc, char *argv[]){
	set_rand_seed();
	if(argc!=2){
		cout << "Usage: " << argv[0] << " <in_name>" << endl;
		cout << "\tin_name = Nombre del dataset" << endl; 
		return 1;
	}
	
	//Read arguments
    string prefix=argv[1];
	
	//Read data
    string data=prefix+".data";
    DatasetClassifier dataset(data.c_str());
    int n=dataset.input.rows();
	assert(n>0);
    int d=dataset.input.cols();
	assert(d>0);
    
	//Analyze data
    VectorXd u=mean(dataset.input);
    VectorXd var=variance(dataset.input);
    cout << "Dataset: " << endl;
    print_stats(n, u, var);
    cout << endl;
    
    for(auto it: dataset.classes()){
        MatrixXd clase=dataset.filter_by_class(it);
        VectorXd u=mean(clase);
        VectorXd var=variance(clase);
        cout << "Clase " << round(it) << ":" << endl;
        print_stats(clase.rows(), u, var);
        cout << endl;
    }
    
	return 0;
}
