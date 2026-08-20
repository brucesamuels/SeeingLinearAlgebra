#!/bin/zsh
set -euo pipefail
script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"
python -m py_compile \
  engine/diagonalization.py \
  scenes/diagonalization_presentation.py \
  tests/test_diagonalization.py \
  tests/test_diagonalization_presentation.py
python -m pytest -q \
  tests/test_diagonalization.py \
  tests/test_diagonalization_presentation.py
