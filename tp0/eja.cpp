#include <cstdio>
#include <cstdlib>
#include <iostream>
#include <cmath>
#include <ctime>
#include <algorithm>
#include <vector>
#include <cassert>
#include <random>
using namespace std;

double rnd_uniform(double m, double M){
	assert(M>m);
	double x=rand()/(double)RAND_MAX;
	return m+(M-m)*x;
}

#define SQ(x) ((x)*(x))
const double EPS=1e-9;
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

int main(int argc, char *argv[]){
	srand(clock());
	if(argc!=4){
		cout << "Usage: " << argv[0] << " <d> <n> <C>" << endl;
		cout << "\td = Dimension del output" << endl; 
		cout << "\tn = Cantidad de puntos" << endl; 
		cout << "\tC = Varianza de los datos (sigma = C*sqrt(D))" << endl; 
		return 1;
	}
	
	//Read arguments
	int d=atoi(argv[1]);
	int n=atoi(argv[2]);
	assert(n>=0);
	assert(d>0);
	double C;
	sscanf(argv[3], "%lf", &C);
	
	//Generate data
	vector< vector<double > > data(n, vector<double>(d));
	for(int i=0; i<n/2; i++)
		data[i]=rnd_normal_vec(d, 1, C*sqrt(d));
	for(int i=n/2; i<n; i++)
		data[i]=rnd_normal_vec(d, -1, C*sqrt(d));	
	//~ random_shuffle(d.begin(), d.end());
	
	//Save data
	for(int i=0; i<n; i++){
	
	}
	return 0;
}
