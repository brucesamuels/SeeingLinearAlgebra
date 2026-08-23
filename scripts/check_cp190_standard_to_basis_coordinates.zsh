#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/standard_to_basis_coordinates.py scenes/standard_to_basis_coordinates_presentation.py
python -m pytest -q tests/test_standard_to_basis_coordinates.py tests/test_standard_to_basis_coordinates_presentation.py
