#!/bin/zsh
set -euo pipefail
script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile \
  engine/powers_of_diagonalizable_matrix.py \
  scenes/powers_of_diagonalizable_matrix_presentation.py \
  tests/test_powers_of_diagonalizable_matrix.py \
  tests/test_powers_of_diagonalizable_matrix_presentation.py
python -m pytest -q \
  tests/test_powers_of_diagonalizable_matrix.py \
  tests/test_powers_of_diagonalizable_matrix_presentation.py
