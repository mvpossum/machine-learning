#include <cstdlib>
#include <iostream>
#include <cmath>
#include <cassert>
#include <string>
#include "common.h"
using namespace std;

int main(int argc, char *argv[]){
	set_rand_seed();
	if(argc!=3){
		cout << "Usage: " << argv[0] << "<n> <out_name>" << endl;
		cout << "\tn = Cantidad de puntos" << endl; 
		cout << "\tout_name = Nombre del dataset" << endl; 
		return 1;
	}
	
	//Read arguments
	int n=atoi(argv[1]);
	assert(n>=0);
    string prefix=argv[2];
	
	//Generate data
	DatasetClassifier dataset(n, 2);
    int left[]={(n+1)/2, n/2};
    while(left[0]>0 || left[1]>0){
        double ro, theta;
        int clase;
        do{
            //(theta, ro) \in clase 0 <=> \exists k \in Z / (theta+2kpi)/(4pi) <= ro <= (theta+(2k+1)pi)/(4pi)
            //(theta, ro) \in clase 0 <=> \exists k \in Z / 2k <= 4ro-theta/pi <= 2k+1
            //(theta, ro) \in clase 0 <=> floor(4ro-theta/pi) es par
            ro=sqrt(rnd_uniform(0, 1));
            theta=rnd_uniform(0, 2*M_PI);
            if((int)floor(4*ro-theta/M_PI)%2==0)
                clase = 0;
            else
                clase = 1;
        }while(left[clase]<=0);
        double x=ro*cos(theta);
        double y=ro*sin(theta);
        int p=left[0]+left[1]-1;
        dataset.input.row(p) << x, y;
        dataset.output(p) = clase;
        left[clase]--;
    }
    
	//Save data
    string names=prefix+".names";
    dataset.save_names(names.c_str(), {"x", "y"});
    string data=prefix+".data";
    dataset.save_data(data.c_str());
	return 0;
}
