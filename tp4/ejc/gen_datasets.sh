#!/bin/bash

DS="2 4 8 16 32"
REP=20

echo Generando datasets... 
for d in $DS; do
    printf '\r'$d >&0
    ../eja $d 10000 0.78 diagonal${d}
    ../ejb $d 10000 0.78 paralelo${d}
    for j in $(seq 1 $REP); do
        ../eja $d 250 0.78 diagonal${d}_$j
        cp diagonal${d}.data diagonal${d}_$j.test
        
        ../ejb $d 250 0.78 paralelo${d}_$j
        cp paralelo${d}.data paralelo${d}_$j.test
    done
done
echo
