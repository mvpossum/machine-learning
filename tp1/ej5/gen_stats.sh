#!/bin/bash

SIZES="$(seq 100 50 499) $(seq 500 500 5000)"
REP=60

echo Generando stats... 
for n in $SIZES; do
    printf '\r'$n >&0
    rm -f stats$n.txt
    for j in $(seq 1 $REP); do
        ../c4.5 -u -f diagonal${n}_$j | ../parse_stats.py >> stats$n.txt
        ../c4.5 -u -f paralelo${n}_$j | ../parse_stats.py >> stats$n.txt
        printf $'\n' >> stats$n.txt
    done
done
echo
