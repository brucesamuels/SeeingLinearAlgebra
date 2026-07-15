#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused complete linear-combination presentation tests..."
python -m pytest -q \
  tests/test_linear_combination_trace.py \
  tests/test_linear_combination_trace_display.py \
  tests/test_manim_linear_combination_trace.py \
  tests/test_manim_linear_combination_readout.py \
  tests/test_linear_combination_trace_smoke.py \
  tests/test_linear_combination_readout_smoke.py \
  tests/test_linear_combination_presentation_smoke.py

print "Running complete test suite..."
python -m pytest -q
