#include <cmath>
#include <ctime>
#include <cassert>
#include <fstream>
#include <sstream>
#include "common.h"
using namespace std;

const double EPS=1e-9;

void set_rand_seed(){
	srand(clock());
}

double rnd_uniform(double m, double M){
	assert(M>m);
	double x=rand()/(double)RAND_MAX;
	return m+(M-m)*x;
}

double normal_distribution(double x, double u, double sigma){
	assert(abs(sigma)>EPS);
	return exp(-0.5*SQ((x-u)/sigma))/(sqrt(2*M_PI)*sigma);
}

double rnd_normal(double u, double sigma){
	assert(abs(sigma)>EPS);
	double y,x;
	do{
		y = rnd_uniform(0, 1/(sqrt(2*M_PI)*sigma));
		x = rnd_uniform(u-5*sigma, u+5*sigma);
	} while(normal_distribution(x, u, sigma)>=y);
	return x;
}

double mean(vector<double> x){
	assert(x.size());
	double sum=0;
	for(vector<double>::iterator it=x.begin(); it!=x.end(); ++it)
		sum+=*it;
	return sum/x.size();
}

double variance(vector<double> x){
	assert(x.size());
	double u=mean(x);
	double sum=0;
	for(vector<double>::iterator it=x.begin(); it!=x.end(); ++it)
		sum+=SQ(*it-u);
	return sum/x.size();
}

vector<double> rnd_normal_vec(int n, double u, double sigma){
	assert(n>=0);
	assert(abs(sigma)>EPS);
	vector<double> r(n);
	for(int i=0; i<n; i++)
		r[i]=rnd_normal(u, sigma);
	return r;
}

void save_names_binary_classifier(const char *file, int d){
    ofstream f(file);
    f << "0,1." << endl;
    f << endl;
    for(int i=1; i<=d; i++){
        f << "x" << i << ": continuous." << endl;
    }
}

void save_data_binary_classifier(const char *file, const DatasetBinaryClassifier &dataset){
    ofstream f(file);
    for(unsigned i=0; i<dataset.size(); i++){
        for(unsigned j=0; j<dataset[i].input.size(); j++){
            f << (j?", ":"") << dataset[i].input[j]; 
        }
        if(dataset[i].input.size()) f << ", ";
        f << dataset[i].output << endl;
    }
}


DatasetBinaryClassifier read_data_binary_classifier(const char *file){
    DatasetBinaryClassifier dataset;
    ifstream f(file);
    string line;
    while(getline(f, line)){
        int d=0;
        for(unsigned i=0; i<line.size(); i++) if(line[i]==',') d++;
        if(d){
            SampleBinaryClassifier s(vector<double>(d), 0);
            stringstream ss(line);
            for(int i=0; i<d; i++){
                ss >> s.input[i];
                ss.ignore();//ignora la ,
            }
            ss >> s.output;
            dataset.push_back(s);
        }
    }
    return dataset;
}

