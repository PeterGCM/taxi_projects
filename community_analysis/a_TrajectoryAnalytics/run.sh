#!/usr/bin/env bash
for i in 0{1..9} {10..12}; do
    python -c "from a2_prevDriversDefined import process_month; process_month('12$i')" &
done

#python -c "from a2_prevDriversDefined import filtering; filtering('2011')"
#python -c "from a2_prevDriversDefined import find_driversRelations; find_driversRelations('2011')"
