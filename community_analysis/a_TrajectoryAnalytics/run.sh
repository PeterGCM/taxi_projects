#!/usr/bin/env bash
#for i in 0{1..9} {10..12}; do
#    python -c "from a1_roamingNinterTravel import process_month; process_month('11$i')" &
#done

#for i in 0{1..9} {10..11}; do
#    python -c "from a2_prevDrivers import process_month; process_month('09$i')" &
#done

#python -c "from a2_prevDrivers import roamingTimeFiltering; roamingTimeFiltering('2009')" &
#python -c "from a2_prevDrivers import interTravelTimeFiltering; interTravelTimeFiltering('2009')" &


#for i in 0{1..9} {10..12}; do
#    python -c "from a3_log_extraction import get_driver_log; get_driver_log('09$i', 17742)" &
#done

#for i in 0{1..9} {10..11}; do
#    python -c "from a3_log_extraction import get_drivers_log; get_drivers_log('09$i', [20318, 15078, 35650, 3413, 13851, 37446, 35685, 33796])" &
#done

for i in 0{1..9} {10..11}; do
    python -c "from a3_log_extraction import get_drivers_log; get_drivers_log('09$i', [40970, 35716, 30309, 22412, 17695, 17637, 16606, 14969, 12887, 3413])" &
done


#for i in 0{1..9} {10..12}; do
#    python -c "from a4_trip_extraction import get_drivers_trip; get_drivers_trip('09$i', [1, 32768])" &
#done

#for i in 0{1..9} {10..12}; do
#    python -c "from a4_trip_extraction import get_drivers_trip_month; get_drivers_trip_month('09$i', [1, 32768])" &
#done