#!/usr/bin/env bash
#for i in 0{1..9} {10..12}; do
#    python -c "from a1_roamingNinterTravel import process_month; process_month('11$i')" &
#done

#for i in 0{1..9} {10..11}; do
#    python -c "from a2_prevDrivers import process_month; process_month('09$i')" &
#done

python -c "from a2_prevDrivers import roamingTimeFiltering; roamingTimeFiltering('2009')" &
python -c "from a2_prevDrivers import interTravelTimeFiltering; interTravelTimeFiltering('2009')" &

#for i in 0{1..9} {10..12}; do
#    python -c "from a4_trip_extraction import get_drivers_trip; get_drivers_trip('09$i', [1, 32768])" &
#done

#for i in 0{1..9} {10..12}; do
#    python -c "from a4_trip_extraction import get_drivers_trip_month; get_drivers_trip_month('09$i', [1, 32768])" &
#done