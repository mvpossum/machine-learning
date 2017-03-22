#include <cmath>
#include <ctime>
#include <cassert>
#include <fstream>
#include <sstream>
#include <iostream>
#include "common.h"
using Eigen::Map;
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
	return exp(-0.5*SQ((x-u)/(2*sigma*sigma)))/(sqrt(2*M_PI)*sigma);
}

double rnd_normal(double u, double sigma){
	assert(abs(sigma)>EPS);
    // Acceptance-Rejection Method by Karl Sigman
    // http://www.columbia.edu/~ks20/4703-Sigman/4703-07-Notes-ARM.pdf
    double y1, y2;
    do{
        y1 = -log(rnd_uniform(0, 1));
        y2 = -log(rnd_uniform(0, 1));
    }while(y2*2<SQ(y1-1));
    double S=rand()%2?-1:1;
    double Z=S*abs(y1);
    return sigma*Z+u;
    
    //Not working Method
	//~ double y,x;
	//~ do{
		//~ y = rnd_uniform(0, 1/(sqrt(2*M_PI)*sigma));
		//~ x = rnd_uniform(u-5*sigma, u+5*sigma);
	//~ } while(normal_distribution(x, u, sigma)>=y);
	//~ return x;
}

VectorXd mean(const MatrixXd &x){
	assert(x.size());
    return x.colwise().mean();
}

VectorXd variance(const MatrixXd &x){
	assert(x.size());
    MatrixXd centered= (x.rowwise() - x.colwise().mean());
    MatrixXd r=(centered.cwiseProduct(centered)).colwise().mean();
    return Map<VectorXd>(r.data(), r.size());
}

VectorXd rnd_normal_vec(VectorXd u, VectorXd sigma){
    int n=u.size();
	VectorXd r(n);
	for(int i=0; i<n; i++){
        assert(abs(sigma(i))>EPS);
		r(i)=rnd_normal(u(i), sigma(i));
	}
    return r;
}

void DatasetClassifier::save_names(const char *file, vector<string> names){
    ofstream f(file);
    f << "0,1." << endl;
    f << endl;
    if(names.size()){
        assert(names.size()==input.cols());
        for(auto it: names)
            f << it << ": continuous." << endl;
    }
    else{
        for(int i=1; i<=input.cols(); i++)
            f << "x" << i << ": continuous." << endl;
    }
}

void DatasetClassifier::save_data(const char *file){
    ofstream f(file);
    for(unsigned i=0; i<input.rows(); i++){
        for(unsigned j=0; j<input.cols(); j++){
            f << (j?", ":"") << input(i, j); 
        }
        if(input.cols()) f << ", ";
        f << output(i) << endl;
    }
}

DatasetClassifier::DatasetClassifier(const char *file){
    ifstream f(file);
    string line;
    int lastd=-1;
    vector<vector<double> > inputs;
    vector<double> outputs;
    while(getline(f, line)){
        int d=0;
        for(unsigned i=0; i<line.size(); i++) if(line[i]==',') d++;
        if(d){
            if(lastd==-1) lastd=d;
            else assert(lastd==d);
            vector<double> s_input(d);
            stringstream ss(line);
            for(int i=0; i<d; i++){
                ss >> s_input[i];
                ss.ignore();//ignora la ,
            }
            inputs.push_back(s_input);
            double s_output;
            ss >> s_output;
            outputs.push_back(s_output);
        }
    }
    assert(lastd>0);
    input=MatrixXd(inputs.size(), lastd);
    output=VectorXd(inputs.size());
    for(unsigned i=0; i<inputs.size(); i++)
        input.row(i)=Map<VectorXd>(inputs[i].data(), inputs[i].size());
    output=Map<VectorXd>(outputs.data(), outputs.size());
}

set<double> DatasetClassifier::classes(){
    set<double> s;
    for(int i=0; i<output.size(); i++)
        s.insert(output(i));
    return s;
}

MatrixXd DatasetClassifier::filter_by_class(double which){
    int n=0;
    for(int i=0; i<output.size(); i++)
        if(abs(which-output(i))<EPS) n++;
    MatrixXd filtered(n, input.cols());
    int q=0;
    for(int i=0; i<output.size(); i++){
        if(abs(which-output(i))<EPS){
            filtered.row(q++)=input.row(i);
        }
    }
    return filtered;
}
