#!/usr/bin/env zsh
set -euo pipefail

REPO="${0:A:h:h}"
cd "$REPO"

python -m pytest -q \
  tests/test_elimination_matrix_multiplication.py \
  tests/test_elimination_matrix_multiplication_presentation.py
