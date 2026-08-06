#!/bin/zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"
export PYTHONPATH="$REPO${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_rectangular_matrices.py \
  tests/test_rectangular_matrices_presentation.py
