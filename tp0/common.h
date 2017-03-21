#include <set>
#include "Eigen/Dense"
using Eigen::MatrixXd;
using Eigen::VectorXd;
using namespace std;

#define dprint(v) cout << #v"=" << (v) << endl
#define SQ(x) ((x)*(x))

void set_rand_seed();

double rnd_uniform(double m, double M);

extern const double EPS;

double normal_distribution(double x, double u, double sigma);

double rnd_normal(double u, double sigma);

VectorXd mean(const MatrixXd &x);

VectorXd variance(const MatrixXd &x);

VectorXd rnd_normal_vec(VectorXd u, VectorXd sigma);

struct DatasetClassifier{
    MatrixXd input;
    VectorXd output;
    DatasetClassifier(){}
    DatasetClassifier(int n, int d):input(n, d), output(n) {}
    DatasetClassifier(const char *file);
    set<double> classes();
    void save_names(const char *file);
    void save_data(const char *file);
    MatrixXd filter_by_class(double which);
};

