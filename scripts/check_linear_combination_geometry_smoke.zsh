#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused Manim adapter and smoke-scene tests..."
python -m pytest -q \
  tests/test_manim_linear_combination_geometry.py \
  tests/test_linear_combination_geometry_smoke.py

print "Running complete test suite..."
python -m pytest -q
