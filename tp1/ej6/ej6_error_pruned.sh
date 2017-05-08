#!/bin/bash

CS="$(seq 0.5 0.2 2.5)"
REP=60

table_name=`basename "$0"`
table_name="${table_name%.*}_$(date +%s).txt"

avg(){
    awk '{ sum += $'$1'; n++ } END { printf sum / n" "; }'
}

echo Generando tabla para ${table_name}... 
for c in $CS; do
    printf '\r'$c >&0
    printf $c\ 
    for col in {4,8,12,16}; do
        avg $col < stats$c.txt
    done
    ../bayesiano_diagonal.py < diagonal${c}.data
    ../bayesiano_paralelo.py < paralelo${c}.data
    echo
done > ${table_name}
echo

echo Generando gráfica para $table_name...
./plot_table.py $table_name "Test Diagonal" "Train Diagonal" "Test Paralelo" "Train Paralelo" "Bayesiano Diagonal" "Bayesiano Paralelo"
