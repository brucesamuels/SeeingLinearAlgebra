#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q \
  tests/test_determinant_invertibility.py \
  tests/test_determinant_invertibility_presentation.py \
  tests/test_cp140_scripts.py
