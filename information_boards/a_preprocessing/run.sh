#!/usr/bin/env bash
for i in 100{1..9} 10{11..12}; do
    python -c "from a1_log_location import run; run('$i')" &
done
