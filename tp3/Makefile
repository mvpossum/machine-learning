CPPFLAGS=-std=c++11 
CFLAGS=-O3 -I. -g
LDFLAGS=-lm
all: nb_n nb_n_cubes nb_n_entropy
	
nb_n: nb_n.o
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 

nb_n_cubes: nb_n_cubes.o
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 
	
nb_n_entropy: nb_n_entropy.o
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 

	
datasets: 
	

%.o: %.cpp
	$(CXX) $(CFLAGS) $(CPPFLAGS) -c $< -o $@
	
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

.PHONY: clean

clean_binaries:
	-rm -f *.o

clean_datasets:


clean: clean_binaries clean_datasets
