#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}
cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

python -m pytest -q \
  tests/test_matrix_matrix_multiplication.py \
  tests/test_matrix_matrix_multiplication_presentation.py
