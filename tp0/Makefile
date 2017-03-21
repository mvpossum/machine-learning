CPPFLAGS=-std=c++11 -O2 -g
all: eja ejb analyze_dataset

eja: eja.o common.o
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS) 
	
ejb: ejb.o common.o
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS) 
	
analyze_dataset: analyze_dataset.o common.o
	$(CXX) $(LDFLAGS) -o $@ $^ $(LDLIBS) 
	
%.o: %.cpp
	$(CXX) $(CFLAGS) $(CPPFLAGS) -c $<

.PHONY: clean

clean:
	-rm -f eja
	-rm -f ejb
	-rm -f analyze_dataset
	-rm -f *.o
