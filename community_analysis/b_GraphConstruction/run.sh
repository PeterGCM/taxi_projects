#!/usr/bin/env bash
#for i in {0..5}; do
#    python -c "from b1_priorPresence import run; run($i)" &
#done

#for i in {0..3}; do
#    python -c "from b2_influenceGraph import run; run($i)" &
#done


python -c "from b3_graphPartition import run; run()" &
