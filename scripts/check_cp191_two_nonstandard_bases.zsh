#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/two_basis_coordinates.py scenes/two_basis_coordinates_presentation.py
python -m pytest -q tests/test_two_basis_coordinates.py tests/test_two_basis_coordinates_presentation.py
