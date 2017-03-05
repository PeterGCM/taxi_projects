#!/usr/bin/env bash
for i in {0..6}; do
    python -c "from f2_regressionCommunityMembers import run; run($i)" &
done

