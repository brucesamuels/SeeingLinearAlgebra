#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"; cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/transformation_matrix_basis.py scenes/transformation_matrix_basis_presentation.py
python -m pytest -q tests/test_transformation_matrix_basis.py tests/test_transformation_matrix_basis_presentation.py
