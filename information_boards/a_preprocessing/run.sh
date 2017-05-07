#!/usr/bin/env bash
for i in 090{1..9} 09{10..11}; do
    python -c "from a1_log_location import run; run('$i')" &
done
