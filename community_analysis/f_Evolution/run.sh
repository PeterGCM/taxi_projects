#!/usr/bin/env bash
for i in {0..6}; do
    python -c "from f1_communityTrips import run; run($i)" &
done

