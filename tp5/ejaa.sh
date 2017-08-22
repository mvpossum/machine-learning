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
	RUN="$1"

	PREFIX="heladas.$RUN"
	#gen_net "ej2.knn" "$PREFIX.knn" DIMS "$DIMS" SEED "$RUN" KNE "1"
	#$NB "$PREFIX" "2**5" "2**(-5)" > "$PREFIX.report"
	$NB "$PREFIX" > "$PREFIX.report"
    #../c4.5 -u -f "$PREFIX"  | ../parse_stats.py > "$PREFIX.report"

    #cat "$PREFIX.report"

	#ERR=$(cat $PREFIX.report)
	ERR=$(grep Test "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
    #echo "$C","$GAMMA","$ERR"

	echo "$ERR" >> discrete-error.csv
}
export -f run_test

mkdir -p "$WORKDIR"
cd "$WORKDIR"

truncate -s0 discrete-error.csv

parallel run_test ::: $(seq 0 9)

cat discrete-error.csv
Rscript ../show-eja.r
