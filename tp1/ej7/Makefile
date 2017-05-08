all: datasets stats plots

datasets:
	./gen_datasets.sh

stats:
	./gen_stats.sh

plots:
	./ej7_error_pruned.sh

.PHONY: clean datasets stats plots

clean: 
	-rm -f *.names *.data *.test
	-rm -f *.tree *.prediction *.unpruned
	-rm -f stats*.txt
	-rm -f ej7_*.txt
