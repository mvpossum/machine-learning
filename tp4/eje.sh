#!/bin/bash
export LC_NUMERIC=C

if [ $# -ne 2 ]; then
	echo "Usage: $0 [NB binary] [output dir]"
	exit 1
fi

export NB=$(readlink -f $1)
export DATADIR=$PWD
export WORKDIR=$2

source "$DATADIR/utils.sh"

run_test () {
	PROB="$1"
	DIMS="$2"
	RUN="$3"

	PREFIX="$PROB${DIMS}_$RUN"
	gen_net "ej2.knn" "$PREFIX.knn" DIMS "$DIMS" SEED "$RUN" KNE "25"

	$NB "$PREFIX" > "$PREFIX.report"
    
    #cat "$PREFIX.report"

	ERR=$(grep Test "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
	BESTK=$(grep "Best " "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
    echo "$PREFIX.report" "$BESTK" "$ERR"
	echo "$PROB,$DIMS,$ERR" >> ../discrete-error-eje.csv
}
export -f run_test

mkdir -p "$WORKDIR"
cd "$WORKDIR"

truncate -s0 ../discrete-error-eje.csv

parallel run_test ::: diagonal paralelo ::: 2 4 8 16 32 ::: $(seq 1 20)
cd ..
Rscript show-eje.r
