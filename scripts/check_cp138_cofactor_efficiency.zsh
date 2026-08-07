#!/bin/zsh
set -euo pipefail
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m pytest -q \
  tests/test_determinant_cofactor_efficiency.py \
  tests/test_determinant_cofactor_efficiency_presentation.py \
  tests/test_cp138_scripts.py
python -m compileall -q engine scenes tests
