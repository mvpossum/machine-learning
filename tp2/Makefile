CPPFLAGS=-std=c++11 
CFLAGS=-O3 -I.
LDFLAGS=-lm
all: alter_net bp bpcl discretiza separa_clases datasets

alter_net: alter_net.o
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 
	
bp: bp.o
	$(CC) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 

bpcl: bpcl.o
	$(CC) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 

discretiza: discretiza.o
	$(CC) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 

separa_clases: separa_clases.o
	$(CC) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS) 
	
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
