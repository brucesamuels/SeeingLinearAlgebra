#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"

python -m py_compile \
  engine/orthogonal_matrices.py \
  scenes/orthogonal_matrices_presentation.py \
  tests/test_orthogonal_matrices.py \
  tests/test_orthogonal_matrices_presentation.py

PYTHONPATH=. pytest -q \
  tests/test_orthogonal_matrices.py \
  tests/test_orthogonal_matrices_presentation.py
