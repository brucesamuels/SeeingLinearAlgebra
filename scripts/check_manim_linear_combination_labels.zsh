#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused Manim linear-combination labels tests..."
python -m pytest -q tests/test_manim_linear_combination_labels.py

print "Running complete test suite..."
python -m pytest -q
