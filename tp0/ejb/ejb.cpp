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
		cout << "\tC = Varianza de los datos (sigma = C*sqrt(d))" << endl; 
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
	DatasetClassifier dataset(n, d);
    vector<int> perm(n);
    for(int i=0; i<n; i++) perm[i]=i;
	random_shuffle(perm.begin(), perm.end());
    
    VectorXd u=VectorXd::Zero(d);
    u(0)=1;
    VectorXd var=VectorXd::Constant(d, C);
	for(int i=0; i<n/2; i++)
		dataset.input.row(perm[i])=rnd_normal_vec(u, var), dataset.output(perm[i])=1;
    u(0)=-1;
	for(int i=n/2; i<n; i++)
		dataset.input.row(perm[i])=rnd_normal_vec(u, var), dataset.output(perm[i])=0;
	
	//Save data
    string names=prefix+".names";
    dataset.save_names(names.c_str());
    string data=prefix+".data";
    dataset.save_data(data.c_str());
	return 0;
}
