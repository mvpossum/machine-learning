#!/bin/bash

SIZES="$(seq 100 50 499) $(seq 500 500 5000)"
REP=60

echo Generando datasets... 
../eja 2 10000 0.78 diagonal10000
../ejb 2 10000 0.78 paralelo10000

for n in $SIZES; do
    printf '\r'$n >&0
    for j in $(seq 1 $REP); do
        ../eja 2 $n 0.78 diagonal${n}_$j
        cp diagonal10000.data diagonal${n}_$j.test
        
        ../ejb 2 $n 0.78 paralelo${n}_$j
        cp paralelo10000.data paralelo${n}_$j.test
    done
done
echo
