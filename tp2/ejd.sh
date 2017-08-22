#!/bin/bash
export LC_NUMERIC=C

if [ $# -ne 2 ]; then
	echo "Usage: $0 [BP binary] [output dir]"
	exit 1
fi

export BP=$(readlink -f $1)
export DATADIR=$PWD
export WORKDIR=$2

if [ ! -f "$BP" ]; then
	echo "BP binary does not exist!" >&2
	exit 1
fi

source "$DATADIR/utils.sh"

run_test () {
	GAMMA="$1"
	RUN="$2"

	PREFIX="ejd-g-$GAMMA-$RUN"
	#gen_net "ejd.net" "$PREFIX.net" GAMMA "$GAMMA" SEED "$(rand)"

	#ln -f "ssp.data" "$PREFIX.data"
	#ln -f "ssp.test" "$PREFIX.test"

	#$BP "$PREFIX" > "$PREFIX.report"

	DECAY=$(cat "$PREFIX.mse" | tail -n1 | awk '{print $8}')
	echo "$GAMMA,$DECAY" >> decay.csv
    
	ERR=$(grep discreto "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
	echo "$GAMMA,$RUN,$ERR" >>  errores.csv
}
export -f run_test

mkdir -p "$WORKDIR"
cd "$WORKDIR"

truncate -s0 errores.csv
truncate -s0 decay.csv

#get_data 'https://sites.google.com/site/aprendizajeautomatizadounr/Inicio/datasets/ssp.zip?attredirects=0&d=1'

parallel run_test ::: 0.00000001 0.0000001 0.000001 0.00001 0.0001 0.001 0.01 0.1 1 ::: $(seq 1 21)

cat errores.csv
clean_test "ssp"
