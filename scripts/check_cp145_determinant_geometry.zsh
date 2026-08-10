#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q \
  tests/test_determinant_geometry.py \
  tests/test_determinant_geometry_presentation.py \
  tests/test_cp145_scripts.py
