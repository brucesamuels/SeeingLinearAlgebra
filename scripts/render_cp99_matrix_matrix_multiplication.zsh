#!/bin/zsh
set -euo pipefail

SCRIPT_DIR=${0:A:h}
REPO_ROOT=${SCRIPT_DIR:h}
cd "$REPO_ROOT"

export PYTHONPATH="$REPO_ROOT${PYTHONPATH:+:$PYTHONPATH}"

manim -pql \
  scenes/matrix_matrix_multiplication_presentation.py \
  MatrixMatrixMultiplicationPresentation
