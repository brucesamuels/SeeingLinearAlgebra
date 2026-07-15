#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPOSITORY_ROOT=${SCRIPT_DIR:h}

cd "$REPOSITORY_ROOT"
export PYTHONPATH="$REPOSITORY_ROOT${PYTHONPATH:+:$PYTHONPATH}"

print "Running focused equation-callout integration tests..."
python -m pytest -q \
    tests/test_manim_equation_callout.py \
    tests/test_manim_linear_combination_labels.py \
    tests/test_manim_linear_combination_presentation.py \
    tests/test_linear_combination_presentation_smoke.py \
    tests/test_linear_combination_labeled_presentation_smoke.py \
    tests/test_linear_combination_equation_callout_smoke.py

print "Running complete test suite..."
python -m pytest -q
