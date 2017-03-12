#!/usr/bin/env bash

for i in {0..6}; do
    python -c "from e1_regressionComMembers import run; run($i)" &
done