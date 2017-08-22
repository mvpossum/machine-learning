#!/bin/bash

DATASET=dos_elipses
TMPD="${DATASET}_tmp"

function get_error {
    grep "Test discreto" | awk -F ':' '{print $2;}' | sed 's/.$//'
}

cp $DATASET.data $TMPD.data
cp $DATASET.test $TMPD.test

MOMENTUMS="$(../linspace 0. 0.1 10)"
ETAS="$(../linspace 0.001 0.1 10)"

#~ 0.45 0.0703

BEST=100
BEST_PARAMS=""
for momentum in $MOMENTUMS; do
    for eta in $ETAS; do
        PARAMS="$momentum\t$eta\t"
        ../alter_net "${DATASET}.net" "${TMPD}.net" u=$momentum ETA=$eta
        CUR=$(../bp "$TMPD" | get_error)
        #~ printf "${PARAMS}${CUR}\n"
        if (( $(bc <<< "$CUR <= $BEST") ))
        then
            BEST=$CUR
            BEST_PARAMS=$PARAMS
            printf "BEST\t${BEST_PARAMS}${BEST}\n"
        fi
        
    done
done
