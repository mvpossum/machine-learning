/*
nb_n.c : Clasificador Naive Bayes usando la aproximacion de funciones normales para features continuos
Formato de datos: c4.5
La clase a predecir tiene que ser un numero comenzando de 0: por ejemplo, para 3 clases, las clases deben ser 0,1,2

PMG - Ultima revision: 20/06/2001
*/

#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <time.h>
#include <vector>
#include <algorithm>
using namespace std;

#define LOW 1.e-14                 /*Minimo valor posible para una probabilidad*/
#define PI  3.141592653
#define SQUARED(x) ((x)*(x))

int N_IN;           /*Total numbre of inputs*/
int N_Class;        /*Total number of classes (outputs)*/

int PTOT;           /* cantidad TOTAL de patrones en el archivo .data */
int PR;             /* cantidad de patrones de ENTRENAMIENTO */
int PTEST;          /* cantidad de patrones de TEST (archivo .test) */
                    /* cantidad de patrones de VALIDACION: PTOT - PR*/

int SEED;           /* semilla para la funcion rand(). Los posibles valores son:*/
                    /* SEED: -1: No mezclar los patrones: usar los primeros PR para entrenar
                                 y el resto para validar.Toma la semilla del rand con el reloj.
                              0: Seleccionar semilla con el reloj, y mezclar los patrones.
                             >0: Usa el numero leido como semilla, y mezcla los patrones. */

int CONTROL;        /* nivel de verbosity: 0 -> solo resumen, 1 -> 0 + pesos, 2 -> 1 + datos*/
int NBINS;        /* cantidad de bins (divisiones del histograma), default=0 (no usa hisogramas)*/

int N_TOTAL;                      /*Numero de patrones a usar durante el entrenamiento*/

/*matrices globales  DECLARAR ACA LAS MATRICES NECESARIAS */

double **data;                     /* train data */
double **test;                     /* test  data */
int    *pred;                     /* clases predichas */

int *count_clase;
double *prob_clase;

int *seq;      	       		  /* sequencia de presentacion de los patrones*/

/*variables globales auxiliares*/
char filepat[100];
/*bandera de error*/
int error;

struct SupervisedHistogram{
  vector<double> delimiters;
  int total;
  vector<int> freq;
  SupervisedHistogram() {}
  SupervisedHistogram(const vector<double> &delimiters, const vector<double> &points) : delimiters(delimiters){    
    total = points.size();
    freq = vector<int>(delimiters.size()+1, 0);
    for (auto &p: points)
      freq[which(p)]++;
  }
  int which(double x)
  {
    return upper_bound(delimiters.begin(), delimiters.end(), x)-delimiters.begin();
  }
  /* Calcula P(x|C)  */
  double prob(double x)
  {
    if (total == 0)
      return 0;
    return (freq[which(x)] + 1) / (double)(total + NBINS);
  }
} **histograms;

/* -------------------------------------------------------------------------- */
/*define_matrix: reserva espacio en memoria para todas las matrices declaradas.
  Todas las dimensiones son leidas del archivo .nb en la funcion arquitec()  */
/* -------------------------------------------------------------------------- */
int define_matrix(){

  int i,max;
  if(PTOT>PTEST) max=PTOT;
  else max=PTEST;

  seq =(int *)calloc(max,sizeof(int));
  pred=(int *)calloc(max,sizeof(int));
  if(seq==NULL||pred==NULL) return 1;
  
  data=(double **)calloc(PTOT,sizeof(double *));
  if(PTEST) test=(double **)calloc(PTEST,sizeof(double *));
  if(data==NULL||(PTEST&&test==NULL)) return 1;

  for(i=0;i<PTOT;i++){
    data[i]=(double *)calloc(N_IN+1,sizeof(double));
    if(data[i]==NULL) return 1;
  }
  for(i=0;i<PTEST;i++){
    test[i]=(double *)calloc(N_IN+1,sizeof(double));
	if(test[i]==NULL) return 1;
  }

/*ALLOCAR ESPACIO PARA LAS MATRICES DEL ALGORITMO*/
  count_clase=(int *)calloc(N_Class,sizeof(int));
  if(count_clase==NULL) return 1;
  prob_clase=(double *)calloc(N_Class,sizeof(double));
  if(prob_clase==NULL) return 1;
  
  histograms=(SupervisedHistogram **)calloc(N_Class,sizeof(SupervisedHistogram *));
  if(histograms==NULL) return 1;
  for(i=0;i<N_Class;i++){
    histograms[i]=(SupervisedHistogram *)calloc(N_IN,sizeof(SupervisedHistogram));
    if(histograms[i]==NULL) return 1;
  }
  
  return 0;
}
/* ---------------------------------------------------------------------------------- */
/*arquitec: Lee el archivo .nb e inicializa el algoritmo en funcion de los valores leidos
  filename es el nombre del archivo .nb (sin la extension) */
/* ---------------------------------------------------------------------------------- */
int arquitec(char *filename){
  FILE *b;
  /*Paso 1:leer el archivo con la configuracion*/
  sprintf(filepat,"%s.nb",filename);
  b=fopen(filepat,"r");
  error=(b==NULL);
  if(error){
    printf("Error al abrir el archivo de parametros\n");
    return 1;
  }

  /* Dimensiones */
  fscanf(b,"%d",&N_IN);
  fscanf(b,"%d",&N_Class);

  /* Archivo de patrones: datos para train y para validacion */
  fscanf(b,"%d",&PTOT);
  fscanf(b,"%d",&PR);
  fscanf(b,"%d",&PTEST);

  /* Semilla para la funcion rand()*/
  fscanf(b,"%d",&SEED);

  /* Nivel de verbosity*/
  fscanf(b,"%d",&CONTROL);
  
  fclose(b);

  /*Paso 2: Definir matrices para datos y parametros (e inicializarlos*/
  error=define_matrix();
  if(error){
    printf("Error en la definicion de matrices\n");
    return 1;
  }

  /* Chequear semilla para la funcion rand() */
  if(SEED==0)
		SEED = time(NULL) ^ (clock() << 16) ^ (getpid() << 8);

  /*Imprimir control por pantalla*/
  
  printf("\nNaive Bayes con particiones de minima entropia:\nCantidad de entradas:%d", N_IN);
  printf("\nCantidad de clases:%d",N_Class);
  printf("\nArchivo de patrones: %s",filename);
  printf("\nCantidad total de patrones: %d",PTOT);
  printf("\nCantidad de patrones de entrenamiento: %d",PR);
  printf("\nCantidad de patrones de validacion: %d",PTOT-PR);
  printf("\nCantidad de patrones de test: %d",PTEST);
  printf("\nSemilla para la funcion rand(): %d",SEED);

  return 0;
}
/* -------------------------------------------------------------------------------------- */
/*read_data: lee los datos de los archivos de entrenamiento(.data) y test(.test)
  filename es el nombre de los archivos (sin extension)
  La cantidad de datos y la estructura de los archivos fue leida en la funcion arquitec()
  Los registros en el archivo pueden estar separados por blancos ( o tab ) o por comas    */
/* -------------------------------------------------------------------------------------- */
int read_data(char *filename){

  FILE *fpat;
  double valor;
  int i,k,separador;

  sprintf(filepat,"%s.data",filename);
  fpat=fopen(filepat,"r");
  error=(fpat==NULL);
  if(error){
    printf("Error al abrir el archivo de datos\n");
    return 1;
  }

  if(CONTROL>1) printf("\n\nDatos de entrenamiento:");

  for(k=0;k<PTOT;k++){
    if(CONTROL>1) printf("\nP%d:\t",k);
    for(i=0;i<N_IN+1;i++){
      fscanf(fpat,"%lf",&valor);
      data[k][i]=valor;
      if(CONTROL>1) printf("%lf\t",data[k][i]);
      separador=getc(fpat);
      if(separador!=',') ungetc(separador,fpat);
    }
  }
  fclose(fpat);

  if(!PTEST) return 0;

  sprintf(filepat,"%s.test",filename);
  fpat=fopen(filepat,"r");
  error=(fpat==NULL);
  if(error){
    printf("Error al abrir el archivo de test\n");
    return 1;
  }

  if(CONTROL>1) printf("\n\nDatos de test:");

  for(k=0;k<PTEST;k++){
    if(CONTROL>1) printf("\nP%d:\t",k);
    for(i=0;i<N_IN+1;i++){
      fscanf(fpat,"%lf",&valor);
      test[k][i]=valor;
      if(CONTROL>1) printf("%lf\t",test[k][i]);
      separador=getc(fpat);
      if(separador!=',') ungetc(separador,fpat);
    }
  }
  fclose(fpat);

  return 0;

}
/* ------------------------------------------------------------ */
/* shuffle: mezcla el vector seq al azar.
   El vector seq es un indice para acceder a los patrones.
   Los patrones mezclados van desde seq[0] hasta seq[hasta-1]
   Esto permite separar la parte de validacion de la de train   */
/* ------------------------------------------------------------ */
void shuffle(int hasta){
   double x;
   int tmp;
   int top,select;

   top=hasta-1;
   while (top > 0) {
	x = (double)rand();
	x /= RAND_MAX;
	x *= (top+1);
	select = (int)x;
	tmp = seq[top];
	seq[top] = seq[select];
	seq[select] = tmp;
	top --;
   }
  if(CONTROL>3) {printf("End shuffle\n");fflush(NULL);}
}

/* ------------------------------------------------------------------- */
/*Prob:Calcula la probabilidad de obtener el valor x para el input feature y la clase clase
  Aproxima las probabilidades por distribuciones normales */
/* ------------------------------------------------------------------- */
double prob(double x,int feature,int clase)  {
    return histograms[clase][feature].prob(x);
}
/* ------------------------------------------------------------------------------ */
/*output: calcula la probabilidad de cada clase dado un vector de entrada *input
  usa el log(p(x)) (sumado)
  devuelve la de mayor probabilidad                                               */
/* ------------------------------------------------------------------------------ */
int output(double *input){
   	
  double prob_de_clase;
	double max_prob = numeric_limits<double>::lowest();
  int i,k,clase_MAP=rand()%N_Class;
  
  for(k=0;k<N_Class;k++) {
    prob_de_clase=0.;

    /*calcula la probabilidad de cada feature individual dada la clase y la acumula*/
    for(i=0;i<N_IN;i++) prob_de_clase += log( prob( input[i] ,i ,k ) );
  
    /*agrega la probabilidad a priori de la clase*/
    prob_de_clase += log(prob_clase[k]);

    /*guarda la clase con prob maxima*/
    if (prob_de_clase>=max_prob){
      max_prob=prob_de_clase;
      clase_MAP=k;
    }
  }

  return clase_MAP;
}
/* ------------------------------------------------------------------------------ */
/*propagar: calcula las clases predichas para un conjunto de datos
  la matriz S tiene que tener el formato adecuado ( definido en arquitec() )
  pat_ini y pat_fin son los extremos a tomar en la matriz
  usar_seq define si se accede a los datos directamente o a travez del indice seq
  los resultados (las propagaciones) se guardan en la matriz seq                  */
/* ------------------------------------------------------------------------------ */
double propagar(double **S,int pat_ini,int pat_fin,int usar_seq){

  double mse=0.0;
  int nu;
  int patron;
  
  for (patron=pat_ini; patron < pat_fin; patron ++) {

   /*nu tiene el numero del patron que se va a presentar*/
    if(usar_seq) nu = seq[patron];
    else         nu = patron;

    /*clase MAP para el patron nu*/
    pred[nu]=output(S[nu]);

    /*actualizar error*/
    if(S[nu][N_IN]!=(double)pred[nu]) mse+=1.;
  }
    

  mse /= ( (double)(pat_fin-pat_ini));

  if(CONTROL>3) {printf("End prop\n");fflush(NULL);}

  return mse;
}

/*Dado un arreglo, eta estructura permite calcular la suma en un rango de indices contiguos en O(1).*/
template <typename T>
struct PrefixSum{
  vector<T> acum;
  PrefixSum() : acum(1, 0) {}
  /*Agrega un elemento al final*/
  void push_back(T value){
    T old_sum=*--acum.end();
    acum.push_back(old_sum+value);
  }
  /*Retorna la suma de los elementos con indice en [i, j)*/
  T sum(int i, int j) const {
    assert(i<=j), assert(i>=0), assert(j<(int)acum.size());
    return acum[j]-acum[i];
  }
  T total() const {return *--acum.end();}
};

//Esta clase procesa los datos ordenados
class EntropyCalculator{
  vector<PrefixSum<int>> sums;
  vector<double> divs;
public:
  EntropyCalculator(int feature): sums(N_Class), divs(PR) {   
    //ordernar por la feature
    vector<double*> ord(PR);
    for(int i=0; i<PR; i++)
      ord[i]=data[seq[i]];
    auto sortByFeature = [feature] (double *a, double *b) {
      return a[feature]<b[feature];
    };
    sort(ord.begin(), ord.end(), sortByFeature);
    for(int i=0; i<PR; i++)
      divs[i]=ord[i][feature];
    //calcular prefix sums para entropia
    for(int i=0; i<PR; i++){
      int clase = round(ord[i][N_IN]);
      for(int j=0; j<N_Class; j++)
        sums[j].push_back(j==clase?1:0);
    }
  }
  
  double entropy(int i, int j) const {
    assert(i<j), assert(i>=0), assert(j<=PR);
    double ent=0;
    for(int c=0; c<N_Class; c++){
      double p=sums[c].sum(i, j)/double(j-i);
      ent-=p*log2(p);
    }
    return ent;
  }
  
  int class_represented(int i, int j) const {
    assert(i<=j), assert(i>=0), assert(j<=PR);
    int count=0;
    for(int c=0; c<N_Class; c++)
      if(sums[c].sum(i, j)>0)
        count++;
    return count;
  }
  double get_div(int p) const {
    assert(p>=0), assert(p<=PR);
    return divs[p];
  }
};

void make_partitions_recursive(int a, int b, const EntropyCalculator &calc, vector<double> &delimiters){
  int N=b-a;
  if(N<=1) return;
  int Tmax=-1;
  double E=1e18;
  for(int t=a+1; t<b; t++){
    double curE=(t-a)/double(N)*calc.entropy(a, t);
    curE+=(b-t)/double(N)*calc.entropy(t, b);
    if(curE<=E) E=curE, Tmax=t;
  }
  if(Tmax==-1)
    return;
  double EntS = calc.entropy(a, b),
         EntS1 = calc.entropy(a, Tmax),
         EntS2 = calc.entropy(Tmax, b);
  int k = calc.class_represented(a, b),
      k1 = calc.class_represented(a, Tmax),
      k2 = calc.class_represented(Tmax, b);
  double Delta = log2(pow(3, k)-2) - (k*EntS - k1*EntS1 - k2*EntS2);
  double Gain=EntS-E;
  if(Gain < log2(N-1)/N + Delta/N)
    return;
  make_partitions_recursive(a, Tmax, calc, delimiters);
  delimiters.push_back(calc.get_div(Tmax));
  make_partitions_recursive(Tmax, b, calc, delimiters);
}

/* --------------------------------------------------------------------------------------- */
/*train: ajusta los parametros del algoritmo a los datos de entrenamiento
         guarda los parametros en un archivo de control
         calcula porcentaje de error en ajuste y test                                      */
/* --------------------------------------------------------------------------------------- */
int train(char *filename){

  int i,j,k;
  double train_error,valid_error,test_error;
  FILE *fpredic;

  N_TOTAL=PR;
  for(k=0;k<PTOT;k++) seq[k]=k;  /* inicializacion del indice de acceso a los datos */

  /*efectuar shuffle inicial de los datos de entrenamiento si SEED != -1 (y hay validacion)*/
  if(SEED>-1 && N_TOTAL<PTOT){
    srand((unsigned)SEED);   
    shuffle(PTOT);
  } 

  for(i=0;i<N_Class;i++)
    count_clase[i]=0;

  /*Calcular probabilidad intrinseca de cada clase*/
  for(i=0;i<PR;i++){
    int clase = round(data[seq[i]][N_IN]);
    count_clase[clase]++;
  }
  if(PR) for(i=0;i<N_Class;i++)
    prob_clase[i]=count_clase[i]/(double)PR;
  
  for(j=0;j<N_IN;j++){
    vector<double> tmps[N_Class];
    for(i=0;i<PR;i++){
      int clase = round(data[seq[i]][N_IN]);
      tmps[clase].push_back(data[seq[i]][j]);        
    }
    
    EntropyCalculator calc(j);
    vector<double> delimiters;
    make_partitions_recursive(0, PR, calc, delimiters);
    if(CONTROL){
      printf("\nLimites para atributo %d:\n", j);
      for(unsigned i=0; i<delimiters.size(); i++)
        printf("%s%.2f", i==0? "":", ", delimiters[i]);
    }
    
    for(i=0;i<N_Class;i++)
      histograms[i][j] = SupervisedHistogram(delimiters, tmps[i]);
  }
  
  
  /*calcular error de entrenamiento*/
  train_error=propagar(data,0,PR,1);
  /*calcular error de validacion; si no hay, usar mse_train*/
  if(PR==PTOT) valid_error=train_error;
  else         valid_error=propagar(data,PR,PTOT,1);
  /*calcular error de test (si hay)*/
  if (PTEST>0) test_error =propagar(test,0,PTEST,0);
  else         test_error =0.;
  /*mostrar errores*/
  printf("\nFin del entrenamiento.\n\n");
  printf("Errores:\nEntrenamiento:%f%%\n",train_error*100.);
  printf("Validacion:%f%%\nTest:%f%%\n",valid_error*100.,test_error*100.);
  if(CONTROL) fflush(NULL);

  /* archivo de predicciones */
  sprintf(filepat,"%s.predic",filename);
  fpredic=fopen(filepat,"w");
  error=(fpredic==NULL);
  if(error){
    printf("Error al abrir archivo para guardar predicciones\n");
    return 1;
  }
  for(k=0; k < PTEST ; k++){
    for( i = 0 ;i< N_IN;i++) fprintf(fpredic,"%f\t",test[k][i]);
    fprintf(fpredic,"%d\n",pred[k]);
  }
  fclose(fpredic);

  return 0;
}

/* ----------------------------------------------------------------------------------------------------- */
/* ----------------------------------------------------------------------------------------------------- */
int main(int argc, char **argv){

  if(argc!=2){
    printf("Modo de uso: nb <filename>\ndonde filename es el nombre del archivo (sin extension)\n");
    return 0;
  }

  /* defino la estructura*/
  error=arquitec(argv[1]);
  if(error){
    printf("Error en la definicion de parametros\n");
    return 1;
  }

  /* leo los datos */
  error=read_data(argv[1]);                 
  if(error){
    printf("Error en la lectura de datos\n");
    return 1;
  }

  /* ajusto los parametros y calcula errores en ajuste y test*/
  error=train(argv[1]);                     
  if(error){
    printf("Error en el ajuste\n");
    return 1;
  }


  return 0;

}
/* ----------------------------------------------------------------------------------------------------- */

