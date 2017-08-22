#!/bin/bash

DS="2 4 8 16 32"
REP=20

echo Generando stats...  
for d in $DS; do
    printf '\r'$d >&0
    rm -f stats$d.txt
    for j in $(seq 1 $REP); do
        ../c4.5 -u -f diagonal${d}_$j | ../parse_stats.py >> stats$d.txt
        ../c4.5 -u -f paralelo${d}_$j | ../parse_stats.py >> stats$d.txt
        printf $'\n' >> stats$d.txt
    done
done
echo
