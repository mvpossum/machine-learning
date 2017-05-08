#!/bin/bash

CS="$(seq 0.5 0.2 2.5)"
REP=60

echo Generando stats... 
for c in $CS; do
    printf '\r'$c >&0
    rm -f stats$c.txt
    for j in $(seq 1 $REP); do
        ../c4.5 -u -f diagonal${c}_$j | ../parse_stats.py >> stats$c.txt
        ../c4.5 -u -f paralelo${c}_$j | ../parse_stats.py >> stats$c.txt
        printf $'\n' >> stats$c.txt
    done
done
echo
