#!/usr/bin/env bash
for i in 0{1..9} {10..12}; do
    python -c "from a6_hourProductivity import process_file; process_file('10$i')" &
done
