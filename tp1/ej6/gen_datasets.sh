#!/bin/bash

CS="$(seq 0.5 0.2 2.5)"
REP=60

echo Generando datasets... 
for c in $CS; do
    printf '\r'$c >&0
    ../eja 5 10000 $c diagonal${c}
    ../ejb 5 10000 $c paralelo${c}
    for j in $(seq 1 $REP); do
        ../eja 5 250 $c diagonal${c}_$j
        cp diagonal${c}.data diagonal${c}_$j.test
        
        ../ejb 5 250 $c paralelo${c}_$j
        cp paralelo${c}.data paralelo${c}_$j.test
    done
done
echo
