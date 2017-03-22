CPPFLAGS=-std=c++11 -O3 -g -I.
all: eja ejb ejc datasets analyze_dataset

eja: eja/eja.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 

ejb: ejb/ejb.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
ejc: ejc/ejc.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
ejb/ejb.data ejb/ejb.names: ejb
	./ejb/ejb 2 200 0.75 ejb/ejb
	
eja/eja.data eja/eja.names: eja
	./eja/eja 2 200 0.75 eja/eja
	
ejc/ejc.data ejc/ejc.names: ejc
	./ejc/ejc 10000 ejc/ejc

datasets: eja/eja.data ejb/ejb.data ejc/ejc.data
	
analyze_dataset: analyze_dataset.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS)
	
%.o: %.cpp
	$(CXX) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

.PHONY: clean

clean:
	-rm -f eja/*.o
	-rm -f eja/eja
	-rm -f eja/*.names eja/*.data
	-rm -f ejb/*.o
	-rm -f ejb/ejb
	-rm -f ejb/*.names ejb/*.data
	-rm -f ejc/*.o
	-rm -f ejc/ejc
	-rm -f ejc/*.names ejc/*.data
	-rm -f analyze_dataset
	-rm -f *.o
