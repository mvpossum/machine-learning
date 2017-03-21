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

void print_vec(const vector<double> &x){
    cout << "(";
    for(unsigned i=0; i<x.size(); i++)
        cout << (i?", ":"") << x[i];
    cout << ")";
}
void print_stats(int samples, const vector<double> &mean, double var){
    cout << "\tsamples = " << samples << endl;
    cout << "\tmean = ";
    print_vec(mean);
    cout << endl;
    cout << "\tvariance = " << var << endl;
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
    DatasetBinaryClassifier dataset=read_data_binary_classifier(data.c_str());
    int n=dataset.size();
	assert(n>0);
    int d=dataset[0].input.size();
	assert(d>0);
    
	//Analyze data
    map<int, vector<double> > u_class;
    map<int, int > n_class;
    for(int i=0; i<n; i++){
        n_class[dataset[i].output]++;
        u_class[dataset[i].output]=vector<double>(d, 0);
    }
    
    vector<double> u(d, 0);
    for(int j=0; j<d; j++){
        for(int i=0; i<n; i++){
            u[j]+=dataset[i].input[j];
            u_class[dataset[i].output][j]+=dataset[i].input[j];
        }
        u[j]/=n;
        for(map<int, vector<double> >::iterator it=u_class.begin(); it!=u_class.end(); ++it)
            it->second[j]/=n_class[it->first];
    }
    
    //Print results
    cout << "Dataset: " << endl;
    print_stats(n, u, 0);
    
    for(map<int, int>::iterator it=n_class.begin(); it!=n_class.end(); ++it){
        cout << "Clase " << it->first << ":" << endl;
        print_stats(it->second, u_class[it->first], 0);
    }
    
    
	return 0;
}
