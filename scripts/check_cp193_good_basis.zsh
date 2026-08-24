#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"; cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile engine/good_basis.py scenes/good_basis_presentation.py
python -m pytest -q tests/test_good_basis.py tests/test_good_basis_presentation.py
