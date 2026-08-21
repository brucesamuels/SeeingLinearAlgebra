#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/why_change_basis.py scenes/why_change_basis_presentation.py
python -m pytest -q tests/test_why_change_basis.py tests/test_why_change_basis_presentation.py

