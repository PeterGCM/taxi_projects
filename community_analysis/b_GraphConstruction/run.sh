#!/usr/bin/env bash
for i in {0..5}; do
    python -c "from b1_priorPresence import run; run($i)" &
done
