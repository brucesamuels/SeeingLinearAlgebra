#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/computing_eigenvectors.py \
  scenes/computing_eigenvectors_presentation.py \
  tests/test_computing_eigenvectors.py \
  tests/test_computing_eigenvectors_presentation.py

python -m pytest -q \
  tests/test_computing_eigenvectors.py \
  tests/test_computing_eigenvectors_presentation.py
