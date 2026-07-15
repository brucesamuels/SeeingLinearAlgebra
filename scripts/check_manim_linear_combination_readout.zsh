#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running ManimLinearCombinationReadout tests..."
python -m pytest tests/test_manim_linear_combination_readout.py -q

print "Running complete test suite..."
python -m pytest -q
