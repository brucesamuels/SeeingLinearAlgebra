#!/bin/zsh
set -euo pipefail

script_dir="${0:A:h}"
repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-${script_dir:h}}"
cd "$repo_root"

python -m py_compile \
  engine/eigenvector_special_directions.py \
  scenes/eigenvector_special_directions_presentation.py \
  tests/test_eigenvector_special_directions.py \
  tests/test_eigenvector_special_directions_presentation.py

python -m pytest -q \
  tests/test_eigenvector_special_directions.py \
  tests/test_eigenvector_special_directions_presentation.py
