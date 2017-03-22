CPPFLAGS=-std=c++11 -O3 -I.
all: eja ejb ejc datasets analyze_dataset

eja: eja/eja.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 

ejb: ejb/ejb.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
ejc: ejc/ejc.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
eja/eja_200.data eja/eja_200.names: eja analyze_dataset
	./eja/eja 2 200 0.75 eja/eja_200
	./analyze_dataset eja/eja_200
	
eja/eja_400.data eja/eja_400.names: eja analyze_dataset
	./eja/eja 4 400 2.0 eja/eja_400
	./analyze_dataset eja/eja_400
	
ejb/ejb_200.data ejb/ejb_200.names: ejb analyze_dataset
	./ejb/ejb 2 200 0.75 ejb/ejb_200
	./analyze_dataset ejb/ejb_200

ejb/ejb_400.data ejb/ejb_400.names: ejb analyze_dataset
	./ejb/ejb 4 400 2.0 ejb/ejb_400
	./analyze_dataset ejb/ejb_400

ejc/ejc.data ejc/ejc.names: ejc analyze_dataset
	./ejc/ejc 3000 ejc/ejc
	./analyze_dataset ejc/ejc

datasets: eja/eja_200.data ejb/ejb_200.data eja/eja_400.data ejb/ejb_400.data ejc/ejc.data
	
analyze_dataset: analyze_dataset.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS)
	
%.o: %.cpp
	$(CXX) $(CFLAGS) $(CPPFLAGS) -c $< -o $@

.PHONY: clean

clean_binaries:
	-rm -f eja/*.o
	-rm -f eja/eja
	-rm -f ejb/*.o
	-rm -f ejb/ejb
	-rm -f ejc/*.o
	-rm -f ejc/ejc
	-rm -f analyze_dataset
	-rm -f *.o

clean_datasets:
	-rm -f eja/*.names eja/*.data
	-rm -f ejb/*.names ejb/*.data
	-rm -f ejc/*.names ejc/*.data

clean: clean_binaries clean_datasets
