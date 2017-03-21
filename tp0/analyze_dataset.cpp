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

double norm(const vector<double> &x){
    double r=0;
    for(unsigned i=0; i<x.size(); i++)
        r+=SQ(x[i]);
    return sqrt(r);
}

void print_vec(const VectorXd &x){
    cout << "(";
    for(unsigned i=0; i<x.size(); i++)
        cout << (i?", ":"") << x(i);
    cout << ")";
}
void print_stats(int samples, const VectorXd &mean, const VectorXd &var){
    cout << "\tsamples = " << samples << endl;
    cout << "\tmean = ";
    print_vec(mean);
    cout << endl;
    cout << "\tvariance = ";
    print_vec(var);
    cout << endl;
    cout << "\tdesviacion estandar = ";
    print_vec(var.cwiseAbs().cwiseSqrt());
    cout << endl;
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
    
    for(auto it: dataset.classes()){
        cout << "Clase " << round(it) << ":" << endl;
        MatrixXd clase=dataset.filter_by_class(it);
        VectorXd u=mean(clase);
        VectorXd var=variance(clase);
        print_stats(clase.rows(), u, var);
    }
    
	return 0;
}
