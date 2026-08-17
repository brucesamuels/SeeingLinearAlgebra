#!/bin/zsh
set -euo pipefail

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m py_compile \
  engine/projection_matrices.py \
  scenes/projection_matrices_presentation.py \
  tests/test_projection_matrices.py \
  tests/test_projection_matrices_presentation.py

PYTHONPATH=. pytest -q \
  tests/test_projection_matrices.py \
  tests/test_projection_matrices_presentation.py
