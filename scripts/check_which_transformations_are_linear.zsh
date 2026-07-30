#!/bin/zsh
set -euo pipefail
SCRIPT_DIR="${0:A:h}"; REPO="${SCRIPT_DIR:h}"; cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q tests/test_linearity_tests.py tests/test_which_transformations_are_linear_presentation.py
python -m pytest -q
