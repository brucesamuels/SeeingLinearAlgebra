#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused CP32 presentation tests..."
python -m pytest -q \
    tests/test_linear_combination_native_3d_smoke.py \
    tests/test_full_rank_linear_combination_3d_presentation.py

print "Running complete test suite..."
python -m pytest -q
