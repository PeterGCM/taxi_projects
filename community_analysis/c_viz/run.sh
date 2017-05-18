#!/usr/bin/env bash

for i in 0{1..9} {10..12}; do
    python -c "from c1_log_extraction import get_driver_log; get_driver_log('09$i', 1)" &
done

