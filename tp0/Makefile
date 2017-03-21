all: eja analyze_dataset

eja: eja.cpp common.cpp common.h
	$(CXX) $(CFLAGS) -o $@ $(LFLAGS) $(LIBS) $?

analyze_dataset: analyze_dataset.cpp common.cpp common.h
	$(CXX) $(CFLAGS) -o $@ $(LFLAGS) $(LIBS) $?

.PHONY: clean

clean:
	-rm -f eja
	-rm -f analyze_dataset
