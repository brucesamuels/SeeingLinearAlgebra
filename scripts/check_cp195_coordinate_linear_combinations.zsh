#!/bin/zsh
set -euo pipefail
export PATH="/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin${PATH:+:$PATH}"

repo_root="${SEEING_LINEAR_ALGEBRA_ROOT:-$(pwd)}"
cd "$repo_root"
export PYTHONPATH="$repo_root${PYTHONPATH:+:$PYTHONPATH}"

python -m py_compile \
  engine/coordinate_linear_combinations.py \
  scenes/coordinate_linear_combinations_presentation.py
python -m pytest -q \
  tests/test_coordinate_linear_combinations.py \
  tests/test_coordinate_linear_combinations_presentation.py

print -- "Checkpoint 195 checks passed."

