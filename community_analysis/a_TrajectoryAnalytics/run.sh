#!/usr/bin/env bash
#for i in 0{1..9} {10..12}; do
#    python -c "from a1_roamingNinterTravel import process_month; process_month('11$i')" &
#done

#for i in 0{1..9} {10..12}; do
#    python -c "from a2_prevDrivers import process_month; process_month('09$i')" &
#done

python -c "from a2_prevDrivers import roamingTimeFiltering; roamingTimeFiltering('2009')" &


