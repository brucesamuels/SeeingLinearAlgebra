#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/coordinates_relative_to_basis.py scenes/coordinates_relative_to_basis_presentation.py
python -m pytest -q tests/test_coordinates_relative_to_basis.py tests/test_coordinates_relative_to_basis_presentation.py

