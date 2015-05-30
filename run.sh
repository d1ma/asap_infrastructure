#!/bin/bash

# Exit on any failure
set -e

# Check for uninitialized variables
set -o nounset

ctrlc() {
    killall -9 python
    mn -c
    exit
}

trap ctrlc SIGINT

start=`date`
exptid=`date +%b%d-%H:%M`



for run in 1; do

    python simpleperf.py --bw-host 3 \
       --delay-host 80 \
        --delay-dns 40 \
        --delay-server 0
       
done

cat $rootdir/*/result.txt | sort -n -k 1
python plot-results.py --dir $rootdir -o $rootdir/result.png
echo "Started at" $start
echo "Ended at" `date`
