#!/usr/bin/env bash

#python -c "from c1_graphPartition import run; run()" &

for i in {0..6}; do
    python -c "from c2_comTrips import run; run($i)" &
done