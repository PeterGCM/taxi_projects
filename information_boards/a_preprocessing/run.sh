#!/usr/bin/env bash
for i in 100{1..9} 10{11..12}; do
#for i in 090{1..9} 09{10..11}; do
    python -c "from a4_ap_entering_exiting import run; run('$i')" &
done
