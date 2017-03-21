#include <vector>
using namespace std;

void set_rand_seed();

double rnd_uniform(double m, double M);

#define SQ(x) ((x)*(x))

extern const double EPS;

double normal_distribution(double x, double u, double sigma);

double rnd_normal(double u, double sigma);

double mean(vector<double> x);

double variance(vector<double> x);

vector<double> rnd_normal_vec(int n, double u, double sigma);


struct SampleBinaryClassifier{
    vector<double> input;
    int output;
    SampleBinaryClassifier() {}
    SampleBinaryClassifier(vector<double> input, int output):input(input), output(output) {}
};
typedef vector<SampleBinaryClassifier> DatasetBinaryClassifier;

void save_names_binary_classifier(const char *file, int d);

void save_data_binary_classifier(const char *file, const DatasetBinaryClassifier &dataset);

DatasetBinaryClassifier read_data_binary_classifier(const char *file);
