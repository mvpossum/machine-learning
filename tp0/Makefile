CPPFLAGS=-std=c++11 -O3 -g -I.
all: eja ejb analyze_dataset datasets

eja: eja/eja.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
ejb: ejb/ejb.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@/$@ $(filter %.o, $^) $(LDLIBS) 
	
analyze_dataset: analyze_dataset.o common.o common.h
	$(CXX) $(LDFLAGS) -o $@ $(filter %.o, $^) $(LDLIBS)
	
datasets: eja ejb 
	./eja/eja 2 2000 1.5 eja/eja
	./ejb/ejb 2 2000 1.5 ejb/ejb
	
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
	-rm -f analyze_dataset
	-rm -f *.o
