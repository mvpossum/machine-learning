#!/bin/bash

SIZES="$(seq 100 50 499) $(seq 500 500 5000)"
REP=60

table_name=`basename "$0"`
table_name="${table_name%.*}_$(date +%s).txt"

avg(){
    awk '{ sum += $'$1'; n++ } END { printf sum / n" "; }'
}

echo Generando tabla para ${table_name}... 
for n in $SIZES; do
    printf '\r'$n >&0
    printf $n\ 
    for col in {2,6,10,14}; do
        avg $col <stats$n.txt
    done
    echo
done > ${table_name}
echo

echo Generando gráfica para $table_name...
./plot_table.py $table_name "Test Diagonal" "Train Diagonal" "Test Paralelo" "Train Paralelo"
