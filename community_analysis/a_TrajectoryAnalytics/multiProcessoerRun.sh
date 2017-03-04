#!/usr/bin/env bash
for i in 0{1..9} {10..12}; do
    python -c "from a1_trip_ss_drivers import process_month; process_month('10$i')" &
done