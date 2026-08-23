#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/basis_matrix.py scenes/basis_matrix_presentation.py
python -m pytest -q tests/test_basis_matrix.py tests/test_basis_matrix_presentation.py

