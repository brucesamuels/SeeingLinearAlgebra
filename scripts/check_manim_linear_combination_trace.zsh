#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}

cd "$REPO_ROOT"
export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running ManimLinearCombinationTrace tests..."
python -m pytest tests/test_manim_linear_combination_trace.py -q

print "Running complete test suite..."
python -m pytest -q
