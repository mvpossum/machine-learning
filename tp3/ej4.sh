#!/bin/bash
export LC_NUMERIC=C

if [ $# -ne 2 ]; then
	echo "Usage: $0 [NB binary] [output dir]"
	exit 1
fi

export NB=$(readlink -f $1)
export DATADIR=$PWD
export WORKDIR=$2

if [ ! -f "$NB" ]; then
	echo "NB binary does not exist!" >&2
	exit 1
fi

source "$DATADIR/utils.sh"


export NOMBRE=dos_elipses
export OUTFILE="../$NOMBRE-error.csv"
run_test () {
	NBINS="$1"

	PREFIX="${NBINS}"
    ln -sf "$NOMBRE.data" "$PREFIX.data"
    ln -sf "$NOMBRE.test" "$PREFIX.test"
	gen_net "$NOMBRE.nb" "$PREFIX.nb" NBINS "$NBINS" SEED 3737

	$NB "$PREFIX" > "$PREFIX.report"
    out=$NBINS
    for PROB in Entrenamiento Validacion Test; do
        ERR=$(grep "$PROB" "$PREFIX.report" | awk -F ':' '{gsub(/(%| )/,""); print $2}')
        out="$out $ERR"
    done
    echo $out >> "$OUTFILE"
}
export -f run_test

mkdir -p "$WORKDIR"
cd "$WORKDIR"

truncate -s0 "$OUTFILE"

parallel run_test ::: $(seq 1 100)
