#!/bin/bash

DS="2 4 8 16 32"
REP=20

table_name=`basename "$0"`
table_name="${table_name%.*}_$(date +%s).txt"

avg(){
    awk '{ sum += $'$1'; n++ } END { printf sum / n" "; }'
}

echo Generando tabla para ${table_name}... 
for d in $DS; do
    printf '\r'$d >&0
    printf $d\ 
    for col in {4,8,12,16}; do
        avg $col < stats$d.txt
    done
    ../bayesiano_diagonal.py < diagonal${d}.data
    ../bayesiano_paralelo.py < paralelo${d}.data
    echo
done > ${table_name}
echo

echo Generando gráfica para $table_name...
./plot_table.py $table_name "Test Diagonal" "Train Diagonal" "Test Paralelo" "Train Paralelo" "Bayesiano Diagonal" "Bayesiano Paralelo"
