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
	C="2**($2)"
	PREFIX="heladas.${PROB}"
	#gen_net "ej2.knn" "$PREFIX.knn" DIMS "$DIMS" SEED "$RUN" KNE "1"
	$NB "$PREFIX" "$C" > "$PREFIX.report"
    
    #cat "$PREFIX.report"

	#ERR=$(cat $PREFIX.report)
	ERR=$(grep Test "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
    echo "$C","$ERR"

	echo "$C","$ERR" >> discrete-error.csv
}
export -f run_test

mkdir -p "$WORKDIR"
cd "$WORKDIR"

truncate -s0 discrete-error.csv

for i in $(seq 0 9); do
	for j in $(seq -5 15); do
		run_test $i $j
	done
done
#parallel run_test ::: $(seq -5 15) ::: $(seq -5 15)
#Rscript ../show-eja.r
